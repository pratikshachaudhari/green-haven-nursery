# 🚀 Green Haven Nursery - Deployment Checklist

## Pre-Deployment Checklist

### 📋 Code Quality
- [ ] All features tested locally
- [ ] No console errors in browser
- [ ] Backend tests pass (if written)
- [ ] Code is clean and commented
- [ ] No debugging code left (console.log, etc.)
- [ ] .gitignore properly configured
- [ ] No sensitive data in code

### 🔐 Security Review
- [ ] Environment variables used for all secrets
- [ ] Strong SECRET_KEY and JWT_SECRET_KEY generated
- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens configured correctly
- [ ] CORS origins restricted to production domains
- [ ] Input validation in place
- [ ] SQL injection protection verified
- [ ] XSS protection verified

### 💾 Database
- [ ] Database schema finalized
- [ ] Sample data ready for production (if needed)
- [ ] Database backup strategy planned
- [ ] PostgreSQL connection string obtained
- [ ] Database migrations tested

### 📧 Email Configuration
- [ ] Gmail App Password generated
- [ ] SMTP credentials secured
- [ ] Email templates ready
- [ ] Test emails sent successfully

---

## Backend Deployment (Render)

### Step 1: Prepare Repository
```bash
# Ensure .gitignore includes:
- [ ] .env
- [ ] __pycache__/
- [ ] *.pyc
- [ ] venv/
- [ ] *.db

# Commit all changes
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### Step 2: Add Production Dependencies
```bash
# Add to requirements.txt:
- [ ] gunicorn==21.2.0

# Verify requirements.txt has all packages:
pip freeze > requirements.txt
```

### Step 3: Create Render Account
- [ ] Sign up at render.com
- [ ] Verify email address
- [ ] Connect GitHub account

### Step 4: Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect your repository
- [ ] Select the repository branch (main)

### Step 5: Configure Build Settings
```
Name: green-haven-nursery-api
Region: [Choose closest to users]
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT run:app
```

### Step 6: Add Environment Variables
```
FLASK_ENV=production
SECRET_KEY=[generate strong 32+ char random string]
JWT_SECRET_KEY=[generate strong 32+ char random string]
DATABASE_URL=[PostgreSQL connection string from Supabase]
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=[your Gmail address]
SMTP_PASSWORD=[your Gmail app password]
CORS_ORIGINS=https://your-frontend-domain.netlify.app
```

**Generate strong keys:**
```bash
# On Mac/Linux:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Or online:
# Use: https://randomkeygen.com/
```

### Step 7: Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Note your backend URL: `https://your-app.onrender.com`

### Step 8: Verify Backend
```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Should return: {"status":"healthy",...}
```

---

## Database Deployment (Supabase)

### Step 1: Create Supabase Project
- [ ] Go to supabase.com
- [ ] Sign up / Login
- [ ] Click "New Project"
- [ ] Fill in:
  - Name: green-haven-nursery
  - Database Password: [strong password]
  - Region: [closest to users]
- [ ] Wait for project creation (2-3 minutes)

### Step 2: Get Connection String
- [ ] Go to Settings → Database
- [ ] Copy "Connection string" (URI format)
- [ ] It looks like: `postgresql://postgres:[password]@[host]:5432/postgres`
- [ ] Replace `[password]` with your actual password

### Step 3: Initialize Database
- [ ] Go to SQL Editor in Supabase
- [ ] Copy contents of `database/schema.sql`
- [ ] Paste into SQL Editor
- [ ] Click "Run"
- [ ] Verify tables created in Table Editor

### Step 4: Update Backend
- [ ] Add DATABASE_URL to Render environment variables
- [ ] Restart Render service

### Step 5: Verify Database Connection
```bash
# Test products endpoint
curl https://your-app.onrender.com/api/products

# Should return: Array of 5 products
```

---

## Frontend Deployment (Netlify)

### Step 1: Prepare Frontend
```bash
cd frontend

# Create _redirects file for SPA routing
echo "/*    /index.html   200" > _redirects
```

### Step 2: Update API URL
Edit `frontend/js/main.js`:
```javascript
// Change from:
const API_BASE_URL = 'http://localhost:5000/api';

// To:
const API_BASE_URL = 'https://your-backend.onrender.com/api';
```

### Step 3: Test Locally
```bash
python3 -m http.server 8000
# Open browser, test all features with production API
```

### Step 4: Deploy to Netlify

**Option A: Drag & Drop**
- [ ] Go to netlify.com
- [ ] Sign up / Login
- [ ] Click "Add new site" → "Deploy manually"
- [ ] Drag the `frontend` folder
- [ ] Wait for deployment
- [ ] Note your URL: `https://random-name.netlify.app`

**Option B: Git Integration**
- [ ] Click "Add new site" → "Import from Git"
- [ ] Connect GitHub
- [ ] Select repository
- [ ] Configure:
  - Base directory: `frontend`
  - Build command: (leave empty)
  - Publish directory: `.`
- [ ] Deploy

### Step 5: Configure Custom Domain (Optional)
- [ ] Go to Site settings → Domain management
- [ ] Add custom domain
- [ ] Follow DNS configuration instructions
- [ ] Wait for SSL certificate (automatic)

### Step 6: Update Backend CORS
- [ ] Go to Render dashboard
- [ ] Update CORS_ORIGINS environment variable
- [ ] Add: `https://your-site.netlify.app`
- [ ] Restart service

---

## Post-Deployment Testing

### Backend Tests
```bash
# Health check
curl https://your-backend.onrender.com/health

# Register test user
curl -X POST https://your-backend.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"test123","phone":"5551234567","address":"123 Test St"}'

# Get products
curl https://your-backend.onrender.com/api/products
```

### Frontend Tests
- [ ] Open production URL in browser
- [ ] Register new account
- [ ] Login with credentials
- [ ] Browse products
- [ ] Add items to cart
- [ ] Complete checkout
- [ ] Verify order placed
- [ ] Check delivery code received

### Integration Tests
- [ ] Test on mobile device
- [ ] Test on different browsers
- [ ] Test all navigation flows
- [ ] Verify HTTPS working
- [ ] Check for console errors
- [ ] Test email notifications (if configured)

---

## Monitoring & Maintenance

### Set Up Monitoring
- [ ] Render: Enable auto-deploy on git push
- [ ] Supabase: Check database usage
- [ ] Netlify: Set up deploy notifications
- [ ] Consider adding: Sentry for error tracking

### Regular Maintenance
- [ ] Weekly: Check error logs
- [ ] Monthly: Review database size
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Security audit
- [ ] As needed: Database backups

### Performance Optimization
- [ ] Enable Render auto-scaling (if needed)
- [ ] Add database indexes for slow queries
- [ ] Optimize images if needed
- [ ] Consider CDN for static assets

---

## Rollback Plan

If deployment fails:

### Backend Rollback
1. Go to Render dashboard
2. Click on your service
3. Go to "Events" tab
4. Click "Rollback" on previous working deployment

### Frontend Rollback
1. Go to Netlify dashboard
2. Click "Deploys" tab
3. Find previous working deploy
4. Click "..." → "Publish deploy"

### Database Rollback
1. Restore from Supabase backup
2. Or re-run schema.sql with correct data

---

## Cost Estimates (Free Tier)

### Render (Backend)
- Free tier: 750 hours/month
- Sleeps after 15 min inactivity
- Cold start: ~30 seconds
- **Cost: $0/month**

### Supabase (Database)
- Free tier: 500MB database
- 2GB file storage
- Unlimited API requests
- **Cost: $0/month**

### Netlify (Frontend)
- Free tier: 100GB bandwidth/month
- Unlimited sites
- Automatic HTTPS
- **Cost: $0/month**

**Total: $0/month for small-scale production**

---

## Production URLs Template

Update these after deployment:

```
Frontend: https://green-haven-nursery.netlify.app
Backend:  https://green-haven-nursery-api.onrender.com
Database: [Supabase dashboard URL]

Admin Accounts:
- Email: admin@greenhaven.com
- Password: [Secure password]
```

---

## Troubleshooting Deployment

### Backend Not Starting
- Check Render logs for errors
- Verify all environment variables set
- Check gunicorn in requirements.txt
- Verify DATABASE_URL format

### CORS Errors
- Verify CORS_ORIGINS matches frontend URL
- Check for trailing slashes
- Restart backend after changes
- Test with curl first

### Database Connection Failed
- Verify DATABASE_URL is correct
- Check Supabase password
- Verify schema was run
- Check Supabase connection limit

### Frontend Not Loading API
- Check API_BASE_URL in main.js
- Verify backend is running (test /health)
- Check browser console for errors
- Verify CORS configured

---

## Security Hardening

### After Deployment
- [ ] Force HTTPS (should be automatic)
- [ ] Add security headers
- [ ] Set up rate limiting (if high traffic)
- [ ] Enable Render auto-scaling
- [ ] Regular security updates
- [ ] Monitor for suspicious activity

### Environment Security
- [ ] Never commit .env files
- [ ] Rotate secrets regularly
- [ ] Use strong database passwords
- [ ] Enable 2FA on hosting accounts
- [ ] Keep dependencies updated

---

## Success Criteria

✅ Deployment successful when:
- Backend health check returns 200
- Products load from database
- User registration works
- Login returns JWT token
- Cart operations successful
- Checkout creates order
- All pages load on frontend
- HTTPS enabled everywhere
- No console errors
- Mobile responsive
- All forms validate correctly

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Supabase Docs:** https://supabase.com/docs
- **Netlify Docs:** https://docs.netlify.com
- **Flask Deployment:** https://flask.palletsprojects.com/en/latest/deploying/

---

**You're Ready to Deploy! 🚀**

Follow this checklist step-by-step and you'll have a production-ready ecommerce site running in under an hour!
