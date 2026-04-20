# 🌱 Green Haven Nursery - Production Ecommerce System

## Project Overview

A production-grade plant ecommerce website for a senior citizen couple transitioning their 10-year offline nursery business online.

**Core Philosophy**: Real-world architecture, industry standards, clean minimal design.

---

## Architecture

### 3-Tier Architecture (Production Standard)

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
│  HTML5 + Tailwind CSS + Vanilla JavaScript              │
│  (Hosted: GitHub Pages / Netlify)                       │
└────────────────────┬────────────────────────────────────┘
                     │ REST API calls
                     │
┌────────────────────▼────────────────────────────────────┐
│                    BACKEND LAYER                         │
│  Python + Flask (REST API)                              │
│  JWT Auth + bcrypt                                      │
│  (Hosted: Render)                                       │
└────────────────────┬────────────────────────────────────┘
                     │ SQL queries
                     │
┌────────────────────▼────────────────────────────────────┐
│                    DATABASE LAYER                        │
│  SQLite (dev) / PostgreSQL (prod)                       │
│  (Hosted: Supabase / Railway)                           │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | HTML5, CSS3, Tailwind, Vanilla JS | Clean UI, responsive design |
| Backend | Python 3.x, Flask | REST API, business logic |
| Database | SQLite → PostgreSQL | Data persistence |
| Auth | bcrypt, JWT | Password hashing, sessions |
| Email | SMTP (Gmail) | Order confirmations |

---

## Features

### User Features
- ✅ Registration & Login (JWT-based)
- ✅ Browse 5 flowering plants
- ✅ Add/Remove from cart
- ✅ Checkout with COD
- ✅ Order confirmation email with delivery code
- ✅ Invoice generation (PDF)

### Admin Features (Future)
- Inventory management
- Order tracking
- Customer management

---

## Database Schema

```sql
Users: id, name, email, password_hash, address, phone, created_at
Products: id, name, description, price, image_url, stock, category
Cart: id, user_id, created_at
CartItems: id, cart_id, product_id, quantity
Orders: id, user_id, total_amount, status, delivery_code, created_at
OrderItems: id, order_id, product_id, quantity, price
Payments: id, order_id, method, status, created_at
```

---

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile (JWT required)

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get single product

### Cart
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/remove` - Remove item from cart
- `GET /api/cart` - Get user's cart
- `PUT /api/cart/update` - Update quantity

### Orders
- `POST /api/checkout` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/<id>` - Get order details

---

## Project Structure

```
green-haven-nursery/
├── frontend/
│   ├── index.html              # Home page
│   ├── pages/
│   │   ├── plants.html         # Products listing
│   │   ├── about.html          # About us
│   │   ├── contact.html        # Contact form
│   │   ├── cart.html           # Shopping cart
│   │   ├── checkout.html       # Checkout flow
│   │   └── auth.html           # Login/Register
│   ├── css/
│   │   └── styles.css          # Custom styles
│   ├── js/
│   │   ├── main.js             # Core functionality
│   │   ├── auth.js             # Authentication
│   │   ├── cart.js             # Cart logic
│   │   └── api.js              # API calls
│   └── images/                 # Plant images
│
├── backend/
│   ├── app/
│   │   └── __init__.py         # Flask app factory
│   ├── config/
│   │   └── config.py           # Configuration
│   ├── models/
│   │   ├── user.py             # User model
│   │   ├── product.py          # Product model
│   │   ├── cart.py             # Cart models
│   │   └── order.py            # Order models
│   ├── routes/
│   │   ├── auth.py             # Auth routes
│   │   ├── products.py         # Product routes
│   │   ├── cart.py             # Cart routes
│   │   └── orders.py           # Order routes
│   ├── utils/
│   │   ├── email_service.py    # Email sending
│   │   ├── pdf_generator.py    # Invoice PDF
│   │   └── validators.py       # Input validation
│   ├── tests/                  # Unit tests
│   ├── requirements.txt        # Python dependencies
│   └── run.py                  # Application entry point
│
└── database/
    └── schema.sql              # Database schema
```

---

## Development Phases

### Phase 1: Setup ✅
- Project structure
- Static frontend pages

### Phase 2: Backend API
- Flask setup
- Database models
- API routes

### Phase 3: Authentication
- User registration
- Login with JWT
- Protected routes

### Phase 4: Cart & Checkout
- Cart management
- Order processing
- Payment (COD)

### Phase 5: Email & Invoice
- Order confirmation emails
- PDF invoice generation

### Phase 6: Deployment
- Frontend → Netlify
- Backend → Render
- Database → Supabase

---

## Setup Instructions

### Frontend Development
```bash
cd frontend
# Use Live Server or Python HTTP server
python3 -m http.server 8000
```

### Backend Development
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Database Setup
```bash
sqlite3 database/ecommerce.db < database/schema.sql
```

---

## Environment Variables

```env
# Backend (.env)
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///database/ecommerce.db

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## Design Philosophy

### UI Principles
- **Minimal**: Clean, uncluttered interfaces
- **Natural**: Plant-inspired color palette (greens, whites, earthy tones)
- **Elegant**: Proper spacing, modern typography
- **Professional**: No generic AI template look

### Color Palette
- Primary: `#2D5016` (Forest Green)
- Secondary: `#7FB069` (Sage Green)
- Accent: `#E8C547` (Warm Yellow)
- Background: `#FAFAFA` (Off White)
- Text: `#333333` (Dark Gray)

### Typography
- Headings: 'Playfair Display' (elegant serif)
- Body: 'Inter' (clean sans-serif)

---

## Production Considerations

### Security
- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Input validation & sanitization
- ✅ HTTPS in production
- ✅ Environment variables for secrets

### Performance
- ✅ Database indexing
- ✅ API response caching
- ✅ Image optimization
- ✅ Minified CSS/JS

### Scalability
- ✅ Stateless API design
- ✅ Database connection pooling
- ✅ Horizontal scaling ready

---

## Future Enhancements
- Payment gateway integration (Stripe/Razorpay)
- Admin dashboard
- Product reviews
- Wishlist feature
- Search & filters
- Order tracking

---

## License
MIT License - Built with ❤️ for Green Haven Nursery
