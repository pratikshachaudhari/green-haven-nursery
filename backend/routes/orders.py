@orders_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        cart = user.cart
        if not cart or not cart.items:
            return jsonify({'message': 'Cart is empty'}), 400

        for item in cart.items:
            if item.product.stock < item.quantity:
                return jsonify({
                    'message': f'Insufficient stock for {item.product.name}'
                }), 400

        data = request.get_json() or {}
        delivery_address = data.get('delivery_address', user.address)

        order = Order.create_from_cart(cart, user)
        order.delivery_address = delivery_address

        db.session.add(order)
        db.session.flush()

        payment = Payment(
            order_id=order.id,
            method='COD',
            status='pending',
            amount=order.total_amount
        )
        db.session.add(payment)

        cart.clear()
        db.session.commit()

        try:
            invoice_path = generate_invoice(order, user)
        except Exception:
            invoice_path = None

        try:
            send_order_confirmation(user, order, invoice_path)
        except Exception:
            pass

        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Checkout error: {str(e)}")
        return jsonify({'message': 'Checkout failed'}), 500
