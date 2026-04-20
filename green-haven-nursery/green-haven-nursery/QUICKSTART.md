# 🌱 Green Haven Nursery - Quick Start Guide

## Get Running in 5 Minutes

### 1. Backend Setup (2 minutes)

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.template .env

# Edit .env - Add your Gmail app password (see SETUP_GUIDE.md for details)
# For now, you can use dummy values to test without email

# Start server
python run.py
```

✅ Backend running at `http://localhost:5000`

### 2. Frontend Setup (1 minute)

Open a new terminal:

```bash
cd frontend

# Start simple HTTP server
python3 -m http.server 8000
```

✅ Frontend running at `http://localhost:8000`

### 3. Test the Application (2 minutes)

1. Open browser: `http://localhost:8000`
2. Click "Register" and create account
3. Browse plants at "Plants" page
4. Add plants to cart
5. Go to Cart and proceed to Checkout
6. Complete your first order!

---

## What You Get

### ✅ Features Implemented

**User Features:**
- User registration with password hashing (bcrypt)
- JWT-based authentication
- Browse 5 beautiful flowering plants
- Add/remove items from cart
- Update quantities
- Secure checkout with COD payment
- Order confirmation with unique delivery code

**Technical Features:**
- 3-tier architecture (Frontend → Backend API → Database)
- RESTful API design
- SQLite database (dev) / PostgreSQL ready (prod)
- CORS-enabled for frontend-backend communication
- Input validation and error handling
- Clean, minimal, plant-inspired UI design

---

## Project Structure

```
green-haven-nursery/
├── frontend/                  # HTML/CSS/JS
│   ├── index.html            # Home page
│   ├── pages/
│   │   ├── plants.html       # Products listing
│   │   ├── auth.html         # Login/Register
│   │   ├── cart.html         # Shopping cart
│   │   ├── checkout.html     # Checkout flow
│   │   ├── about.html        # About us
│   │   └── contact.html      # Contact form
│   ├── css/
│   │   └── styles.css        # Custom styles
│   └── js/
│       ├── main.js           # Core functionality
│       └── auth.js           # Authentication
│
├── backend/                   # Python Flask API
│   ├── app/
│   │   └── __init__.py       # Flask app factory
│   ├── models/               # Database models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── routes/               # API endpoints
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   ├── config/
│   │   └── config.py         # Configuration
│   ├── utils/
│   │   └── validators.py     # Input validation
│   ├── requirements.txt
│   └── run.py                # Entry point
│
└── database/
    └── schema.sql            # Database schema
```

---

## API Endpoints

### Authentication
- `POST /api/register` - Create new user
- `POST /api/login` - Login and get JWT token
- `GET /api/profile` - Get user profile (requires auth)

### Products
- `GET /api/products` - List all plants

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/remove` - Remove item
- `PUT /api/cart/update` - Update quantity

### Orders
- `POST /api/checkout` - Place order
- `GET /api/orders` - Get user's orders

---

## Default Products

The system comes pre-loaded with 5 beautiful flowering plants:

1. **Peace Lily** - $24.99
   - White blooms, air purifying, low-light friendly

2. **Orchid Phalaenopsis** - $39.99
   - Exotic pink flowers, long-lasting blooms

3. **African Violet** - $18.99
   - Purple flowers, compact size, year-round blooms

4. **Anthurium** - $34.99
   - Heart-shaped red blooms, tropical flair

5. **Begonia** - $21.99
   - Coral-pink flowers, hardy, beginner-friendly

---

## Common Commands

### Backend

```bash
# Activate venv
source backend/venv/bin/activate

# Run server
python backend/run.py

# Install new package
pip install package-name
pip freeze > backend/requirements.txt
```

### Database

```bash
# Access SQLite database
sqlite3 backend/database/ecommerce.db

# View tables
.tables

# Query users
SELECT * FROM users;

# Query products
SELECT * FROM products;
```

---

## Troubleshooting

**Can't connect frontend to backend?**
- Check if backend is running on port 5000
- Look for CORS errors in browser console
- Verify API_BASE_URL in `frontend/js/main.js`

**Login not working?**
- Check browser console for errors
- Verify email and password are correct
- Try registering a new account

**Cart not updating?**
- Make sure you're logged in
- Check if JWT token is in localStorage
- Verify backend is running

---

## Next Steps

1. **Customize Products**
   - Edit `database/schema.sql`
   - Add your own plant images and descriptions
   - Update prices

2. **Add Features**
   - Product search and filtering
   - Order history page
   - Admin dashboard
   - Payment gateway integration

3. **Deploy to Production**
   - Follow `SETUP_GUIDE.md` deployment section
   - Use PostgreSQL database
   - Deploy frontend to Netlify
   - Deploy backend to Render

---

## Tech Stack Summary

- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend:** Python 3.x, Flask
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Authentication:** JWT tokens, bcrypt password hashing
- **API:** RESTful design
- **Architecture:** 3-tier (Presentation → Business → Data)

---

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Tailwind CSS: https://tailwindcss.com/
- JWT: https://jwt.io/
- SQLAlchemy: https://www.sqlalchemy.org/

---

**Built with ❤️ for plant lovers**

Need help? Check `SETUP_GUIDE.md` for detailed instructions!
