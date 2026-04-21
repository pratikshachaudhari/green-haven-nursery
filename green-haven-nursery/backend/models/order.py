"""
Green Haven Nursery - Order Models
Manages orders and order items
"""

from datetime import datetime
from app import db
import random
import string


class Order(db.Model):
    """Order model"""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    delivery_code = db.Column(db.String(20), unique=True)
    delivery_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', lazy=True, uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id} status={self.status}>'
    
    @staticmethod
    def generate_delivery_code():
        """Generate unique delivery code"""
        while True:
            code = 'GH-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Order.query.filter_by(delivery_code=code).first():
                return code
    
    def to_dict(self, include_items=True):
        """Convert order to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'delivery_code': self.delivery_code,
            'delivery_address': self.delivery_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'payment_method': self.payment.method if self.payment else None,
            'payment_status': self.payment.status if self.payment else None
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        
        return data
    
    @staticmethod
    def create_from_cart(cart, user):
        """Create order from cart"""
        order = Order(
            user_id=user.id,
            total_amount=cart.get_total(),
            delivery_code=Order.generate_delivery_code(),
            delivery_address=user.address,
            status='confirmed'
        )
        
        # Create order items from cart items
        for cart_item in cart.items:
            order_item = OrderItem(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            order.items.append(order_item)
            
            # Reduce product stock
            cart_item.product.reduce_stock(cart_item.quantity)
        
        return order


class OrderItem(db.Model):
    """Order item model"""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='order_items', lazy=True)
    
    def __repr__(self):
        return f'<OrderItem product_id={self.product_id} quantity={self.quantity}>'
    
    def get_subtotal(self):
        """Calculate item subtotal"""
        return round(float(self.price) * self.quantity, 2)
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': self.get_subtotal()
        }


class Payment(db.Model):
    """Payment model"""
    
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    method = db.Column(db.String(20), default='COD')  # COD (Cash on Delivery)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment order_id={self.order_id} method={self.method}>'
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'method': self.method,
            'status': self.status,
            'amount': float(self.amount),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
