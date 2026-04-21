"""
Green Haven Nursery - Authentication Routes
Handles user registration and login
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.cart import Cart
from utils.validators import validate_email, validate_password, validate_phone

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json() or {}

        required_fields = ['name', 'email', 'password', 'phone', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field.capitalize()} is required'}), 400

        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        phone = data['phone'].strip()
        address = data['address'].strip()

        if not validate_email(email):
            return jsonify({'message': 'Invalid email format'}), 400

        if not validate_password(password):
            return jsonify({'message': 'Password must be at least 6 characters long'}), 400

        if not validate_phone(phone):
            return jsonify({'message': 'Invalid phone number format'}), 400

        if User.find_by_email(email):
            return jsonify({'message': 'Email already registered'}), 409

        user = User.create_user(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address
        )

        db.session.add(user)
        db.session.commit()

        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({'message': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}

        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400

        email = data['email'].strip().lower()
        password = data['password']

        user = User.find_by_email(email)

        if not user or not user.check_password(password):
            return jsonify({'message': 'Invalid email or password'}), 401

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Login failed'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'user': user.to_dict()}), 200

    except Exception as e:
        print(f"Profile error: {str(e)}")
        return jsonify({'message': 'Failed to fetch profile'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        data = request.get_json() or {}

        if data.get('name'):
            user.name = data['name'].strip()

        if data.get('phone'):
            if not validate_phone(data['phone']):
                return jsonify({'message': 'Invalid phone number'}), 400
            user.phone = data['phone'].strip()

        if data.get('address'):
            user.address = data['address'].strip()

        db.session.commit()

        return jsonify({
            'message': 'Profile updated',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Update profile error: {str(e)}")
        return jsonify({'message': 'Failed to update profile'}), 500
