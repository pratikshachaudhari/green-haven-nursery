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
    """
    User registration endpoint
    
    Expects JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "phone": "(555) 123-4567",
        "address": "123 Garden St, Green Valley, CA 12345"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'phone', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field.capitalize()} is required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        phone = data['phone'].strip()
        address = data['address'].strip()
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Validate password strength
        if not validate_password(password):
            return jsonify({'message': 'Password must be at least 6 characters long'}), 400
        
        # Validate phone format
        if not validate_phone(phone):
            return jsonify({'message': 'Invalid phone number format'}), 400
        
        # Check if user already exists
        if User.find_by_email(email):
            return jsonify({'message': 'Email already registered'}), 409
        
        # Create new user
        user = User.create_user(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create cart for user
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
        return jsonify({'message': 'Registration failed. Please try again.'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Expects JSON:
    {
        "email": "john@example.com",
        "password": "password123"
    }
    
    Returns JWT token on success
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Find user
        user = User.find_by_email(email)
        
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Verify password
        if not user.check_password(password):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Login failed. Please try again.'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    Requires JWT token in Authorization header
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Profile error: {str(e)}")
        return jsonify({'message': 'Failed to fetch profile'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile
    Requires JWT token in Authorization header
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if data.get('name'):
            user.name = data['name'].strip()
        
        if data.get('phone'):
            if validate_phone(data['phone']):
                user.phone = data['phone'].strip()
            else:
                return jsonify({'message': 'Invalid phone number'}), 400
        
        if data.get('address'):
            user.address = data['address'].strip()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Update profile error: {str(e)}")
        return jsonify({'message': 'Failed to update profile'}), 500
