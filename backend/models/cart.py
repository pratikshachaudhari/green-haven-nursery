"""
Green Haven Nursery - Cart Models
Manages shopping cart functionality
"""

from datetime import datetime
from app import db
from models.product import Product


class Cart(db.Model):
    """Shopping cart model"""
    
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cart user_id={self.user_id}>'
    
    def add_item(self, product_id, quantity=1):
        """Add item to cart or update quantity"""
        # Check if item already exists
        cart_item = CartItem.query.filter_by(
            cart_id=self.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=self.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        return cart_item
    
    def remove_item(self, product_id):
        """Remove item from cart"""
        cart_item = CartItem.query.filter_by(
            cart_id=self.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            db.session.delete(cart_item)
            return True
        return False
    
    def update_item_quantity(self, product_id, quantity):
        """Update item quantity"""
        cart_item = CartItem.query.filter_by(
            cart_id=self.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            if quantity <= 0:
                db.session.delete(cart_item)
            else:
                cart_item.quantity = quantity
            return True
        return False
    
    def clear(self):
        """Clear all items from cart"""
        CartItem.query.filter_by(cart_id=self.id).delete()
    
    def get_total(self):
        """Calculate cart total"""
        total = 0
        for item in self.items:
            if item.product:
                total += float(item.product.price) * item.quantity
        return round(total, 2)
    
    def to_dict(self):
        """Convert cart to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': self.get_total(),
            'item_count': len(self.items)
        }


class CartItem(db.Model):
    """Cart item model"""
    
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='cart_items', lazy=True)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
    )
    
    def __repr__(self):
        return f'<CartItem product_id={self.product_id} quantity={self.quantity}>'
    
    def get_subtotal(self):
        """Calculate item subtotal"""
        if self.product:
            return round(float(self.product.price) * self.quantity, 2)
        return 0
    
    def to_dict(self):
        """Convert cart item to dictionary"""
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': self.get_subtotal()
        }
