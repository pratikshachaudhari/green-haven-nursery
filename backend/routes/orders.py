"""
Green Haven Nursery - Orders Routes
Handles checkout and order management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from models.user import User
from models.order import Order, Payment
from utils.email_service import send_order_confirmation
from utils.pdf_generator import generate_invoice

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
    Checkout and create order.

    Expects JSON:
    {
        "delivery_address": "123 Garden St, Green Valley, CA 12345",
        "phone": "(555) 123-4567"
    }
    """
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        cart = user.cart
        if not cart or not cart.items:
            return jsonify({'message': 'Cart is empty'}), 400

        # Validate stock before creating order
        for cart_item in cart.items:
            if not cart_item.product:
                return jsonify({'message': 'One or more products are unavailable'}), 400

            if cart_item.product.stock < cart_item.quantity:
                return jsonify({
                    'message': f'Insufficient stock for {cart_item.product.name}. Only {cart_item.product.stock} available.'
                }), 400

        data = request.get_json() or {}

        delivery_address = data.get('delivery_address', user.address)
        phone = data.get('phone', user.phone)

        if not delivery_address or not str(delivery_address).strip():
            return jsonify({'message': 'Delivery address is required'}), 400

        if not phone or not str(phone).strip():
            return jsonify({'message': 'Contact number is required'}), 400

        # Update latest user contact details from checkout form
        user.address = str(delivery_address).strip()
        user.phone = str(phone).strip()

        # Create order
        order = Order.create_from_cart(cart, user)
        order.delivery_address = user.address

        db.session.add(order)
        db.session.flush()

        # Create COD payment record
        payment = Payment(
            order_id=order.id,
            method='COD',
            status='pending',
            amount=order.total_amount
        )
        db.session.add(payment)

        # Clear cart after order creation
        cart.clear()

        db.session.commit()

        # Generate invoice PDF
        try:
            invoice_path = generate_invoice(order, user)
        except Exception as e:
            print(f"Invoice generation error: {str(e)}")
            invoice_path = None

        # Send confirmation email with delivery code
        try:
            send_order_confirmation(user, order, invoice_path)
        except Exception as e:
            print(f"Email sending error: {str(e)}")

        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Checkout error: {str(e)}")
        return jsonify({'message': 'Checkout failed. Please try again.'}), 500


@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders for the current user."""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        orders = (
            Order.query
            .filter_by(user_id=user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

        return jsonify({
            'orders': [order.to_dict(include_items=False) for order in orders]
        }), 200

    except Exception as e:
        print(f"Get orders error: {str(e)}")
        return jsonify({'message': 'Failed to fetch orders'}), 500


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get a specific order for the current user."""
    try:
        user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'message': 'Order not found'}), 404

        if order.user_id != user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        return jsonify({
            'order': order.to_dict(include_items=True)
        }), 200

    except Exception as e:
        print(f"Get order error: {str(e)}")
        return jsonify({'message': 'Failed to fetch order'}), 500


@orders_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order if it is still pending or confirmed."""
    try:
        user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'message': 'Order not found'}), 404

        if order.user_id != user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        if order.status not in ['pending', 'confirmed']:
            return jsonify({
                'message': f'Cannot cancel order with status: {order.status}'
            }), 400

        order.status = 'cancelled'

        # Restore stock
        for item in order.items:
            if item.product:
                item.product.stock += item.quantity

        # Update payment
        if order.payment:
            order.payment.status = 'cancelled'

        db.session.commit()

        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Cancel order error: {str(e)}")
        return jsonify({'message': 'Failed to cancel order'}), 500
