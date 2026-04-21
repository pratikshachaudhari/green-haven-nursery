"""
Green Haven Nursery - Cart Routes
Handles shopping cart operations
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.cart import Cart
from models.product import Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

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
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}

        if not data.get('product_id'):
            return jsonify({'message': 'Product ID is required'}), 400

        product_id = data['product_id']
        quantity = data.get('quantity', 1)

        if quantity < 1:
            return jsonify({'message': 'Quantity must be at least 1'}), 400

        product = Product.get_by_id(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        if product.stock < quantity:
            return jsonify({
                'message': f'Only {product.stock} items available in stock'
            }), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        cart = user.cart
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

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
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}

        if not data.get('product_id'):
            return jsonify({'message': 'Product ID is required'}), 400

        product_id = data['product_id']

        user = User.query.get(user_id)
        if not user or not user.cart:
            return jsonify({'message': 'Cart not found'}), 404

        cart = user.cart

        if cart.remove_item(product_id):
            db.session.commit()
            return jsonify({
                'message': 'Item removed from cart',
                'cart': cart.to_dict()
            }), 200

        return jsonify({'message': 'Item not found in cart'}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Remove from cart error: {str(e)}")
        return jsonify({'message': 'Failed to remove item from cart'}), 500


@cart_bp.route('/cart/update', methods=['PUT'])
@jwt_required()
def update_cart_item():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}

        if not data.get('product_id') or 'quantity' not in data:
            return jsonify({'message': 'Product ID and quantity are required'}), 400

        product_id = data['product_id']
        quantity = data['quantity']

        if quantity < 0:
            return jsonify({'message': 'Quantity cannot be negative'}), 400

        if quantity > 0:
            product = Product.get_by_id(product_id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404

            if product.stock < quantity:
                return jsonify({
                    'message': f'Only {product.stock} items available in stock'
                }), 400

        user = User.query.get(user_id)
        if not user or not user.cart:
            return jsonify({'message': 'Cart not found'}), 404

        cart = user.cart

        if cart.update_item_quantity(product_id, quantity):
            db.session.commit()
            return jsonify({
                'message': 'Cart updated',
                'cart': cart.to_dict()
            }), 200

        return jsonify({'message': 'Item not found in cart'}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Update cart error: {str(e)}")
        return jsonify({'message': 'Failed to update cart'}), 500


@cart_bp.route('/cart/clear', methods=['POST'])
@jwt_required()
def clear_cart():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or not user.cart:
            return jsonify({'message': 'Cart not found'}), 404

        cart = user.cart
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
