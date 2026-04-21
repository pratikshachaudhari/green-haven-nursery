"""
Green Haven Nursery - Application Entry Point
Starts the Flask development server
"""

import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()


def init_database():
    """Initialize database with tables"""
    with app.app_context():
        # Import all models to ensure they're registered
        from models.user import User
        from models.product import Product
        from models.cart import Cart, CartItem
        from models.order import Order, OrderItem, Payment
        
        # Create all tables
        db.create_all()
        
        # Check if products exist, if not, seed the database
        if Product.query.count() == 0:
            print("Seeding database with sample products...")
            
            products = [
                Product(
                    name='Peace Lily',
                    description='Elegant white blooms with glossy dark green leaves. Easy to care for and purifies air. Perfect for low-light conditions.',
                    price=24.99,
                    image_url='https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=800',
                    stock=15,
                    category='flowering'
                ),
                Product(
                    name='Orchid Phalaenopsis',
                    description='Stunning exotic flowers in vibrant pink. Long-lasting blooms that add elegance to any space. Moderate care required.',
                    price=39.99,
                    image_url='https://images.unsplash.com/photo-1516354535481-52a9144c6a44?w=800',
                    stock=10,
                    category='flowering'
                ),
                Product(
                    name='African Violet',
                    description='Charming purple flowers with velvety leaves. Compact size perfect for windowsills. Blooms year-round with proper care.',
                    price=18.99,
                    image_url='https://images.unsplash.com/photo-1594579875418-7cc2f6f3b11e?w=800',
                    stock=20,
                    category='flowering'
                ),
                Product(
                    name='Anthurium',
                    description='Heart-shaped red blooms that last for months. Glossy foliage adds tropical flair. Excellent air purifier for your home.',
                    price=34.99,
                    image_url='https://images.unsplash.com/photo-1598752116257-90a87c816359?w=800',
                    stock=12,
                    category='flowering'
                ),
                Product(
                    name='Begonia',
                    description='Vibrant coral-pink flowers with unique foliage patterns. Hardy and perfect for beginners. Thrives in partial shade.',
                    price=21.99,
                    image_url='https://images.unsplash.com/photo-1591958911259-bee2173bdccc?w=800',
                    stock=18,
                    category='flowering'
                )
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("✅ Database seeded successfully!")
        
        print("✅ Database initialized!")


if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Get configuration
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    print("\n" + "="*60)
    print("🌱 Green Haven Nursery - Backend Server")
    print("="*60)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Running on: http://localhost:{port}")
    print(f"API Base URL: http://localhost:{port}/api")
    print("="*60 + "\n")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
