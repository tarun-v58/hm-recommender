# app.py
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from models import db, User, Product, Purchase
from recommend import get_personalized_recommendations, get_similar_products
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)

# Auth
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username exists"}), 400
    if 'gender' not in data or data['gender'] not in ['male', 'female']:
        return jsonify({"error": "Gender must be specified as 'male' or 'female'"}), 400
    user = User(username=data['username'], email=data['email'], gender=data['gender'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "gender": user.gender
        })
    return jsonify({"error": "Invalid credentials"}), 401

# Categories
@app.route('/api/categories')
def get_categories():
    try:
        categories = db.session.query(Product.index_group_name).distinct().filter(Product.index_group_name != None).all()
        category_list = sorted([cat[0] for cat in categories if cat[0]])
        return jsonify(category_list)
    except Exception as e:
        print(f"Error fetching categories: {str(e)}")
        return jsonify([])

# Products
@app.route('/api/products')
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')
    gender = request.args.get('gender')
    
    def get_gender_filter(query, gender):
        if gender == 'male':
            return query.filter(
                (Product.index_group_name.ilike('%men%')) |
                (Product.index_group_name.ilike('%boy%')) |
                (Product.garment_group_name.ilike('%men%')) |
                (Product.garment_group_name.ilike('%boy%'))
            )
        elif gender == 'female':
            return query.filter(
                (Product.index_group_name.ilike('%women%')) |
                (Product.index_group_name.ilike('%girl%')) |
                (Product.index_group_name.ilike('%lady%')) |
                (Product.garment_group_name.ilike('%women%')) |
                (Product.garment_group_name.ilike('%girl%')) |
                (Product.garment_group_name.ilike('%lady%'))
            )
        return query

    # Start with base query
    query = Product.query
    
    # Apply gender filter if provided
    if gender:
        query = get_gender_filter(query, gender)
    
    # Apply category filter
    if category:
        query = query.filter(Product.index_group_name == category)
    
    # Apply search filter
    if search:
        query = query.filter(Product.prod_name.ilike(f'%{search}%'))

    if not category and not search:
        # Get all products quickly (150+)
        if gender:
            products = query.limit(150).all()
        else:
            products = Product.query.limit(150).all()
    else:
        products = query.limit(100).all()

    return jsonify([{
        'article_id': int(p.article_id),
        'prod_name': p.prod_name,
        'image_path': p.image_path,
        'price': 29.99,
        'index_group_name': p.index_group_name,  # Add category name for frontend grouping
        'garment_group_name': p.garment_group_name
    } for p in products])

@app.route('/api/products/<int:article_id>')
def get_product(article_id):
    product = Product.query.get_or_404(article_id)
    try:
        similar = get_similar_products(article_id)
    except Exception as e:
        print(f"Error getting similar products: {str(e)}")
        similar = []

    response = {
        'article_id': int(product.article_id),  # Convert to Python int
        'prod_name': product.prod_name,
        'detail_desc': product.detail_desc,
        'image_path': product.image_path,
        'price': 29.99,  # Using fixed price for now
        'product_type_name': product.product_type_name,
        'colour_group_name': product.colour_group_name,
        'index_group_name': product.index_group_name,
        'garment_group_name': product.garment_group_name,
        'similar_products': [int(x) for x in similar]  # Convert to Python int
    }
    return jsonify(response)

# Buy and Purchase History
@app.route('/api/buy', methods=['POST'])
def buy():
    data = request.json
    purchase = Purchase(user_id=data['user_id'], article_id=data['article_id'])
    db.session.add(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase recorded"})

@app.route('/api/purchases')
def get_purchases():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify([]), 400
    
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    result = []
    for p in purchases:
        product = Product.query.get(p.article_id)
        if product:
            result.append({
                'article_id': p.article_id,
                'date': p.created_at.isoformat(),
                'product': {
                    'article_id': product.article_id,
                    'prod_name': product.prod_name,
                    'image_path': product.image_path,
                    'price': 29.99,  # Use fixed price or add to DB
                    'detail_desc': product.detail_desc
                }
            })
    return jsonify(result)

# Recommendations
@app.route('/api/recommendations')
def recommendations():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        print("No user_id provided")
        return jsonify({"error": "No user ID provided"}), 400
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        print(f"Fetching recommendations for user {user_id}")
        # Get user's purchase count
        purchase_count = Purchase.query.filter_by(user_id=user_id).count()
        print(f"User {user_id} has {purchase_count} purchases")
        
        recs = get_personalized_recommendations(user_id)
        print(f"Found {len(recs)} recommendations for user {user_id}")
        
        # Filter recommendations based on user's gender and exclude Ladies Suits
        filtered_recs = []
        for product in recs:
            # Skip Ladies Suits and other suits
            if 'suit' in (product.product_type_name or '').lower():
                continue
            
            # Filter based on index_group_name and garment_group_name
            is_male_product = any(male_term in (product.index_group_name or '').lower() + 
                                (product.garment_group_name or '').lower() 
                                for male_term in ['men', 'boy', 'male'])
            is_female_product = any(female_term in (product.index_group_name or '').lower() + 
                                  (product.garment_group_name or '').lower() 
                                  for female_term in ['women', 'girl', 'lady', 'female'])
            
            if (user.gender == 'male' and is_male_product) or \
               (user.gender == 'female' and is_female_product) or \
               (not is_male_product and not is_female_product):  # Unisex products
                filtered_recs.append(product)
        
        recs = filtered_recs[:80]  # Limit to top 80 filtered recommendations
        
        response = [{
            'article_id': int(p.article_id),
            'prod_name': p.prod_name,
            'image_path': p.image_path,
            'price': 29.99,
            'product_type_name': p.product_type_name,
            'colour_group_name': p.colour_group_name
        } for p in recs]
        
        return jsonify(response)
    except Exception as e:
        print(f"Error generating recommendations for user {user_id}: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# Images
@app.route('/images/<path:filename>')
def images(filename):
    try:
        return send_from_directory('images', filename)  # Changed from 'data/images' to 'images'
    except:
        # If image not found, return a default placeholder
        return send_from_directory('static', 'placeholder.jpg')

# Serve static files (for placeholder)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route('/')
def index():
    """Redirect to frontend on port 3000"""
    return redirect('http://localhost:3000', code=302)

@app.route('/api')
def api_info():
    """API info endpoint"""
    return jsonify({
        'message': 'H&M recommender API',
        'routes': [
            '/api/products',
            '/api/products/<article_id>',
            '/api/recommendations?user_id=<id>',
            '/api/signup',
            '/api/login',
            '/api/buy',
            '/status'
        ]
    })

@app.route('/status')
def status():
    from recommend import model_status
    # product count may require a DB context
    try:
        count = Product.query.count()
    except Exception:
        count = None
    return jsonify({
        'model': model_status(),
        'product_count': count
    })

if __name__ == '__main__':
    app.run(debug=True)