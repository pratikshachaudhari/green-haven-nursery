"""
Green Haven Nursery - Product Model
Manages plant products
"""

from datetime import datetime
from app import db


class Product(db.Model):
    """Product model for plants"""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), default='flowering')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'image_url': self.image_url,
            'stock': self.stock,
            'category': self.category
        }
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    def reduce_stock(self, quantity):
        """Reduce stock by quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    @staticmethod
    def get_all_products():
        """Get all products"""
        return Product.query.all()
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def get_available_products():
        """Get products that are in stock"""
        return Product.query.filter(Product.stock > 0).all()
