"""
Green Haven Nursery - Products Routes
Handles product listing and details
"""

from flask import Blueprint, jsonify
from models.product import Product

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get all products
    Returns list of all flowering plants
    """
    try:
        products = Product.get_all_products()
        
        return jsonify([product.to_dict() for product in products]), 200
        
    except Exception as e:
        print(f"Get products error: {str(e)}")
        return jsonify({'message': 'Failed to fetch products'}), 500


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get single product by ID
    """
    try:
        product = Product.get_by_id(product_id)
        
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        print(f"Get product error: {str(e)}")
        return jsonify({'message': 'Failed to fetch product'}), 500


@products_bp.route('/products/available', methods=['GET'])
def get_available_products():
    """
    Get products that are in stock
    """
    try:
        products = Product.get_available_products()
        
        return jsonify([product.to_dict() for product in products]), 200
        
    except Exception as e:
        print(f"Get available products error: {str(e)}")
        return jsonify({'message': 'Failed to fetch available products'}), 500
