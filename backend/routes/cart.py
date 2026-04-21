@cart_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}

        if not data.get('product_id'):
            return jsonify({'message': 'Product ID required'}), 400

        product_id = data['product_id']
        quantity = data.get('quantity', 1)

        if quantity < 1:
            return jsonify({'message': 'Invalid quantity'}), 400

        product = Product.get_by_id(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        if product.stock < quantity:
            return jsonify({'message': 'Insufficient stock'}), 400

        user = User.query.get(user_id)
        cart = user.cart

        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        cart.add_item(product_id, quantity)
        db.session.commit()

        return jsonify({
            'message': 'Item added',
            'cart': cart.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Cart error: {str(e)}")
        return jsonify({'message': 'Failed to add item'}), 500
