# init_db.py
import os
import pandas as pd
from app import app, db
from models import Product, User, Purchase
from datetime import datetime

# Resolve data paths relative to this file so the script can be run from any CWD
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_products():
    csv_path = os.path.join(DATA_DIR, 'articles.csv')
    df = pd.read_csv(csv_path)
    images_dir = os.path.join(BASE_DIR, 'images')
    
    def find_image_path(article_id):
        # Convert to string for manipulation
        aid = str(article_id).zfill(10)  # Pad to 10 digits with leading zeros
        # Try different folder formats (010, 011, etc.)
        possible_folders = [f"{i:03d}" for i in range(10, 96)]  # 010 to 095
        image_name = f"{aid}.jpg"
        
        for folder in possible_folders:
            path = os.path.join(images_dir, folder, image_name)
            if os.path.exists(path):
                return f"{folder}/{image_name}"
        return None
    
    df['image_path'] = df['article_id'].apply(find_image_path)
    
    for _, row in df.iterrows():
        product = Product(
            article_id=row['article_id'],
            prod_name=row['prod_name'],
            product_type_name=row['product_type_name'],
            colour_group_name=row['colour_group_name'],
            index_group_name=row['index_group_name'],
            garment_group_name=row['garment_group_name'],
            detail_desc=row['detail_desc'],
            image_path=row['image_path']
        )
        db.session.add(product)
    db.session.commit()
    print("[OK] Products loaded!")

if __name__ == '__main__':
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        load_products()