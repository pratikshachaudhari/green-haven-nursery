# 🚀 Green Haven Nursery - Setup & Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Running the Application](#running-the-application)
3. [Testing the Application](#testing-the-application)
4. [Production Deployment](#production-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.8+ installed
- Node.js (optional, for frontend dev server)
- Git
- Text editor (VS Code recommended)

### Step 1: Clone/Download Project
```bash
cd green-haven-nursery
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment
```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use any text editor
```

**Minimum required .env configuration:**
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this
DATABASE_URL=sqlite:///database/ecommerce.db

# Email (Optional for testing, required for production)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### 2.4 Initialize Database
```bash
# Create database directory
mkdir -p database

# Run the application (will auto-create database and seed products)
python run.py
```

You should see:
```
✅ Database initialized!
✅ Database seeded successfully!
🌱 Green Haven Nursery - Backend Server
Running on: http://localhost:5000
```

### Step 3: Frontend Setup

#### 3.1 Update API URL (if needed)
If your backend runs on a different port, update `frontend/js/main.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

#### 3.2 Serve Frontend
**Option A: Python HTTP Server (Recommended for testing)**
```bash
cd frontend
python3 -m http.server 8000
```
Open: http://localhost:8000

**Option B: VS Code Live Server**
1. Install "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

**Option C: Node.js HTTP Server**
```bash
npx http-server frontend -p 8000
```

---

## Running the Application

### Start Backend Server
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python run.py
```
Backend runs on: http://localhost:5000

### Start Frontend Server
```bash
cd frontend
python3 -m http.server 8000
```
Frontend runs on: http://localhost:8000

### Access the Application
1. Open browser: http://localhost:8000
2. Register a new account
3. Browse plants and add to cart
4. Complete checkout

---

## Testing the Application

### Manual Testing Flow

#### Test 1: User Registration
1. Navigate to http://localhost:8000/pages/auth.html
2. Click "Register" tab
3. Fill in all fields:
   - Name: John Doe
   - Email: john@example.com
   - Phone: (555) 123-4567
   - Address: 123 Garden St, Green Valley, CA 12345
   - Password: password123
4. Click "Create Account"
5. Should see success message and redirect to login

#### Test 2: User Login
1. Enter email and password
2. Click "Login"
3. Should redirect to home page
4. Nav bar should show your name instead of "Login"

#### Test 3: Browse Products
1. Click "Plants" in navigation
2. Should see 5 flowering plants
3. Verify images, prices, and descriptions load

#### Test 4: Add to Cart
1. Click "Add to Cart" on any plant
2. Cart count should increment
3. Click cart icon to view cart
4. Verify product appears with correct quantity and price

#### Test 5: Cart Management
1. In cart, increase/decrease quantities
2. Remove an item
3. Verify totals update correctly

#### Test 6: Checkout
1. Click "Proceed to Checkout"
2. Review order details
3. Click "Place Order"
4. Should see success message with delivery code
5. Check email for confirmation (if SMTP configured)

### API Testing (Using curl or Postman)

#### Test Backend Health
```bash
curl http://localhost:5000/health
```
Expected response: `{"status": "healthy", "service": "Green Haven Nursery API"}`

#### Test Product Listing
```bash
curl http://localhost:5000/api/products
```
Should return JSON array of 5 products

#### Test Registration
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "phone": "(555) 123-4567",
    "address": "123 Test St"
  }'
```

#### Test Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```
Copy the `token` from response for authenticated requests.

---

## Production Deployment

### Backend Deployment (Render)

#### 1. Prepare for Production
Update `.env` for production:
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:port/database
CORS_ORIGINS=https://your-frontend-domain.com
```

#### 2. Deploy to Render
1. Create account on [Render](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Environment:** Python 3
5. Add environment variables from your .env file
6. Click "Create Web Service"

#### 3. Database Setup (Supabase/Railway)
**Option A: Supabase**
1. Create account on [Supabase](https://supabase.com)
2. Create new project
3. Get connection string
4. Update `DATABASE_URL` in Render

**Option B: Railway**
1. Create account on [Railway](https://railway.app)
2. Create PostgreSQL database
3. Get connection string
4. Update `DATABASE_URL` in Render

### Frontend Deployment (Netlify)

#### 1. Update API URL
In `frontend/js/main.js`:
```javascript
const API_BASE_URL = 'https://your-backend.onrender.com/api';
```

#### 2. Deploy to Netlify
1. Create account on [Netlify](https://www.netlify.com)
2. Drag and drop `frontend` folder
3. Or connect GitHub repository
4. Configure build settings:
   - **Build command:** (leave empty)
   - **Publish directory:** `frontend`
5. Click "Deploy"

#### 3. Configure Custom Domain (Optional)
1. Go to "Domain settings"
2. Add your custom domain
3. Update DNS records as instructed

---

## Email Configuration (Gmail SMTP)

### Setup Gmail App Password
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Go to "App passwords"
4. Generate password for "Mail"
5. Copy 16-character password
6. Update `.env`:
```env
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

---

## Troubleshooting

### Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Activate virtual environment
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### Issue: "Database is locked"
**Solution:** Close all connections to database
```bash
# Delete database and reinitialize
rm database/ecommerce.db
python run.py
```

#### Issue: "CORS error" in browser console
**Solution:** Verify CORS_ORIGINS in config matches frontend URL
```python
CORS_ORIGINS = ['http://localhost:8000']
```

### Frontend Issues

#### Issue: "Failed to fetch" error
**Solution:** Check backend is running on correct port
```bash
# Verify backend is running
curl http://localhost:5000/health
```

#### Issue: JWT token expired
**Solution:** Clear localStorage and login again
```javascript
// In browser console:
localStorage.clear();
location.reload();
```

#### Issue: Images not loading
**Solution:** Check image URLs in database, ensure internet connection

### Email Issues

#### Issue: Emails not sending
**Solution:** 
1. Verify SMTP credentials in `.env`
2. Check Gmail App Password is correct
3. Ensure "Less secure app access" is enabled (if not using App Password)
4. Check spam folder

---

## Database Management

### View Database Contents
```bash
cd backend/database
sqlite3 ecommerce.db

# SQLite commands:
.tables                    # List all tables
SELECT * FROM users;       # View users
SELECT * FROM products;    # View products
SELECT * FROM orders;      # View orders
.exit                      # Exit SQLite
```

### Reset Database
```bash
cd backend
rm database/ecommerce.db
python run.py
```

### Backup Database
```bash
cp database/ecommerce.db database/backup_$(date +%Y%m%d).db
```

---

## Security Checklist for Production

- [ ] Change SECRET_KEY and JWT_SECRET_KEY
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set FLASK_ENV=production
- [ ] Use strong passwords
- [ ] Enable rate limiting
- [ ] Regular database backups
- [ ] Monitor error logs
- [ ] Keep dependencies updated
- [ ] Use environment variables for all secrets

---

## Support & Resources

- **Frontend:** Tailwind CSS docs - https://tailwindcss.com/docs
- **Backend:** Flask docs - https://flask.palletsprojects.com/
- **Database:** SQLAlchemy docs - https://docs.sqlalchemy.org/
- **Authentication:** JWT docs - https://jwt.io/

---

## Next Steps / Future Enhancements

1. **Admin Dashboard**
   - Manage products (add/edit/delete)
   - View all orders
   - Manage users

2. **Enhanced Features**
   - Product search and filters
   - Product reviews and ratings
   - Wishlist functionality
   - Order tracking
   - Multiple payment methods (Stripe, PayPal)

3. **Performance Optimization**
   - Image CDN
   - API caching
   - Database query optimization
   - Frontend code minification

4. **Analytics**
   - Google Analytics integration
   - Sales reports
   - Customer behavior tracking

---

**✅ You're all set! Happy coding! 🌱**
