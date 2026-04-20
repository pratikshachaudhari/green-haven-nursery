"""
Green Haven Nursery - Flask Application Factory
Initializes the Flask app with all extensions and configurations
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config.config import get_config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app():
    """Application factory pattern"""
    
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.orders import orders_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(orders_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'Green Haven Nursery API'}, 200
    
    # Create database tables
    if app.config.get("DEBUG"):
        try:
            with app.app_context():
                db.create_all()
        except Exception as e:
            print(f"Database initialization warning: {e}")
    
    return app
