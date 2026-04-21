"""
Green Haven Nursery - Cart Routes
Handles shopping cart operations
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.cart import Cart, CartItem
from models.product import Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """
    Get current user's cart
    Requires JWT token
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get or create cart
        cart = user.cart
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        
        return jsonify(cart.to_dict()), 200
        
    except Exception as e:
        print(f"Get cart error: {str(e)}")
        return jsonify({'message': 'Failed to fetch cart'}), 500


@cart_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add item to cart
    
    Expects JSON:
    {
        "product_id": 1,
        "quantity": 1
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate input
        if not data.get('product_id'):
            return jsonify({'message': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        
        if quantity < 1:
            return jsonify({'message': 'Quantity must be at least 1'}), 400
        
        # Check if product exists
        product = Product.get_by_id(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        # Check stock availability
        if product.stock < quantity:
            return jsonify({
                'message': f'Only {product.stock} items available in stock'
            }), 400
        
        # Get or create cart
        user = User.query.get(user_id)
        cart = user.cart
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        
        # Add item to cart
        cart.add_item(product_id, quantity)
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to cart',
            'cart': cart.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Add to cart error: {str(e)}")
        return jsonify({'message': 'Failed to add item to cart'}), 500


@cart_bp.route('/cart/remove', methods=['POST'])
@jwt_required()
def remove_from_cart():
    """
    Remove item from cart
    
    Expects JSON:
    {
        "product_id": 1
    }
    """
    try:
       user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('product_id'):
            return jsonify({'message': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        
        # Get cart
        user = User.query.get(user_id)
        cart = user.cart
        
        if not cart:
            return jsonify({'message': 'Cart not found'}), 404
        
        # Remove item
        if cart.remove_item(product_id):
            db.session.commit()
            return jsonify({
                'message': 'Item removed from cart',
                'cart': cart.to_dict()
            }), 200
        else:
            return jsonify({'message': 'Item not found in cart'}), 404
        
    except Exception as e:
        db.session.rollback()
        print(f"Remove from cart error: {str(e)}")
        return jsonify({'message': 'Failed to remove item from cart'}), 500


@cart_bp.route('/cart/update', methods=['PUT'])
@jwt_required()
def update_cart_item():
    """
    Update item quantity in cart
    
    Expects JSON:
    {
        "product_id": 1,
        "quantity": 2
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('product_id') or 'quantity' not in data:
            return jsonify({'message': 'Product ID and quantity are required'}), 400
        
        product_id = data['product_id']
        quantity = data['quantity']
        
        if quantity < 0:
            return jsonify({'message': 'Quantity cannot be negative'}), 400
        
        # Check stock if increasing quantity
        if quantity > 0:
            product = Product.get_by_id(product_id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404
            
            if product.stock < quantity:
                return jsonify({
                    'message': f'Only {product.stock} items available in stock'
                }), 400
        
        # Get cart
        user = User.query.get(user_id)
        cart = user.cart
        
        if not cart:
            return jsonify({'message': 'Cart not found'}), 404
        
        # Update quantity
        if cart.update_item_quantity(product_id, quantity):
            db.session.commit()
            return jsonify({
                'message': 'Cart updated',
                'cart': cart.to_dict()
            }), 200
        else:
            return jsonify({'message': 'Item not found in cart'}), 404
        
    except Exception as e:
        db.session.rollback()
        print(f"Update cart error: {str(e)}")
        return jsonify({'message': 'Failed to update cart'}), 500


@cart_bp.route('/cart/clear', methods=['POST'])
@jwt_required()
def clear_cart():
    """
    Clear all items from cart
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        cart = user.cart
        
        if not cart:
            return jsonify({'message': 'Cart not found'}), 404
        
        cart.clear()
        db.session.commit()
        
        return jsonify({
            'message': 'Cart cleared',
            'cart': cart.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Clear cart error: {str(e)}")
        return jsonify({'message': 'Failed to clear cart'}), 500
