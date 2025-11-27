# recommend.py
import pandas as pd
import lightgbm as lgb
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
from models import Product, Purchase

_model = None
_model_load_error = None
_product_features_df = None
_similarity_matrix = None

def _load_model():
    """Attempt to load the LightGBM model once. If loading fails, store the error and
    keep _model as None so callers can fallback to a safe behaviour."""
    global _model, _model_load_error
    if _model is not None or _model_load_error is not None:
        return
    try:
        # model file is located in the same directory as this module
        import os
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'hm_recommender.txt')
        _model = lgb.Booster(model_file=path)
    except Exception as e:
        # store the exception so callers can inspect/log it; do not raise here
        _model_load_error = e

def get_product_features():
    """Compute product feature DataFrame on demand and cache it.
    This function must be called within an application context because it queries
    the database via the SQLAlchemy models."""
    global _product_features_df
    if _product_features_df is not None:
        return _product_features_df

    products = Product.query.all()
    df = pd.DataFrame([{
        'article_id': p.article_id,
        'product_type_no': hash(p.product_type_name) % 1000 if p.product_type_name is not None else 0,
        'colour_group_code': hash(p.colour_group_name) % 50 if p.colour_group_name is not None else 0,
        'index_group_no': hash(p.index_group_name) % 20 if p.index_group_name is not None else 0,
        'garment_group_no': hash(p.garment_group_name) % 100 if p.garment_group_name is not None else 0
    } for p in products])

    _product_features_df = df
    return _product_features_df

def get_similar_products(article_id, top_k=5):
    # ensure product features are computed
    df = get_product_features()
    try:
        if df.empty:
            return []
            
        # Get feature vector for target product
        feature_cols = ['product_type_no', 'colour_group_code', 'index_group_no', 'garment_group_no']
        
        # Find the target product
        target_matches = df[df['article_id'] == article_id]
        if target_matches.empty:
            return []
            
        target_idx = target_matches.index[0]
        target_features = df.iloc[target_idx][feature_cols].values.reshape(1, -1)
        
        # Calculate similarities in batches to save memory
        batch_size = 1000
        similarities = []
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_features = batch[feature_cols].values
            batch_sims = cosine_similarity(target_features, batch_features)[0]
            similarities.extend(zip(batch.index, batch_sims))
        
        # Sort by similarity and get top k*2 for diversity
        similarities.sort(key=lambda x: x[1], reverse=True)
        similar_indices = [x[0] for x in similarities[1:top_k*3]]  # Skip first (self), get more
        
        # Mix similarity-based with some random diverse products
        similar_ids = [int(df.iloc[i]['article_id']) for i in similar_indices[:top_k]]
        
        # Add some random diverse products if we have room
        if len(similar_ids) < top_k:
            all_article_ids = df['article_id'].tolist()
            random.shuffle(all_article_ids)
            for aid in all_article_ids:
                if aid not in similar_ids and len(similar_ids) < top_k:
                    similar_ids.append(int(aid))
        
        return similar_ids
    except Exception as e:
        print(f"Error in get_similar_products: {str(e)}")
        return []

def get_personalized_recommendations(user_id, top_k=50):
    from models import User  # Import here to avoid circular import
    
    # Get user and their gender
    user = User.query.get(user_id)
    if not user:
        return []
    
    # Get user's purchase history
    purchases = Purchase.query.filter_by(user_id=user_id).all()
    
    # Get all products first, then filter by gender
    all_products = Product.query.all()
    
    # If user has no purchases, return empty list (no recommendations for new users)
    if not purchases:
        return []
    
    # Build candidate set from similar products to user's purchases
    purchased_ids = [p.article_id for p in purchases]
    
    # Get products similar to what user bought
    candidate_scores = {}
    
    for article_id in purchased_ids:
        similar = get_similar_products(article_id, top_k=20)
        for sim_id in similar:
            if sim_id not in purchased_ids:  # Don't recommend already purchased
                candidate_scores[sim_id] = candidate_scores.get(sim_id, 0) + 1
    
    # Sort by frequency (how many times it appeared as similar)
    sorted_candidates = sorted(candidate_scores.items(), key=lambda x: -x[1])
    top_ids = [aid for aid, _ in sorted_candidates[:top_k * 3]]
    
    if not top_ids:
        # Fallback: popular items
        products = Product.query.order_by(Product.article_id).limit(top_k * 3).all()
    else:
        # Get products
        products = Product.query.filter(Product.article_id.in_(top_ids)).all()
    
    # Gender filtering - include unisex items for everyone
    filtered_products = []
    for product in products:
        category_str = (product.index_group_name or '').lower() + ' ' + (product.garment_group_name or '').lower()
        
        is_male_product = any(term in category_str for term in ['men', 'boy', 'male'])
        is_female_product = any(term in category_str for term in ['women', 'girl', 'lady', 'female'])
        is_unisex = not is_male_product and not is_female_product
        
        # Skip suits
        if 'suit' in (product.product_type_name or '').lower():
            continue
        
        # Include product if it matches user gender or is unisex
        if (user.gender == 'male' and (is_male_product or is_unisex)) or \
           (user.gender == 'female' and (is_female_product or is_unisex)):
            filtered_products.append(product)
        
        if len(filtered_products) >= top_k:
            break
    
    return filtered_products[:top_k]


def model_status():
    """Return a small dict describing whether the model is loaded and any load error."""
    _load_model()
    return {
        'loaded': _model is not None,
        'error': str(_model_load_error) if _model_load_error is not None else None
    }