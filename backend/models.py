# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
    purchases = db.relationship('Purchase', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(200), nullable=False)
    product_type_name = db.Column(db.String(100))
    colour_group_name = db.Column(db.String(50))
    index_group_name = db.Column(db.String(50))
    garment_group_name = db.Column(db.String(100))
    detail_desc = db.Column(db.Text)
    image_path = db.Column(db.String(200))  # e.g., "010/010875015.jpg"

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('product.article_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())