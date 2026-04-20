# 🧪 Green Haven Nursery - Testing Guide

## Manual Testing Checklist

### 1. User Registration & Authentication

#### Registration Flow
- [ ] Navigate to Register tab
- [ ] Try submitting empty form (should show validation errors)
- [ ] Try invalid email format (should reject)
- [ ] Try password < 6 characters (should reject)
- [ ] Try mismatched passwords (should reject)
- [ ] Try invalid phone format (should reject)
- [ ] Register with valid data (should succeed)
- [ ] Try registering same email again (should reject - duplicate)

#### Login Flow
- [ ] Navigate to Login tab
- [ ] Try empty credentials (should show validation)
- [ ] Try wrong password (should reject)
- [ ] Try non-existent email (should reject)
- [ ] Login with correct credentials (should succeed)
- [ ] Verify token is stored in localStorage
- [ ] Verify user data is stored in localStorage
- [ ] Check that "Login" changes to username in nav

#### Session Management
- [ ] After login, refresh page (should stay logged in)
- [ ] Logout and verify redirect to home
- [ ] Verify token removed from localStorage
- [ ] Try accessing cart without login (should redirect to login)

---

### 2. Product Browsing

#### Plants Page
- [ ] Navigate to Plants page
- [ ] Verify all 5 products load
- [ ] Check product images display correctly
- [ ] Verify prices format correctly ($XX.XX)
- [ ] Check stock levels display
- [ ] Verify "Out of Stock" shows for stock = 0
- [ ] Check "Add to Cart" button is disabled when out of stock
- [ ] Hover over cards (should have hover effect)

#### Product Details
- [ ] Each product shows name, description, price
- [ ] Check responsive layout on mobile
- [ ] Verify loading state shows initially
- [ ] Test error handling (stop backend, reload page)

---

### 3. Shopping Cart

#### Adding Items
- [ ] Click "Add to Cart" on plants page (while logged in)
- [ ] Verify success message appears
- [ ] Check cart count badge updates in nav
- [ ] Add multiple different products
- [ ] Add same product multiple times (quantity should increase)
- [ ] Try adding without login (should redirect)

#### Cart Management
- [ ] Navigate to Cart page
- [ ] Verify all added items display
- [ ] Check quantities are correct
- [ ] Check subtotals calculate correctly
- [ ] Test quantity increase button
- [ ] Test quantity decrease button
- [ ] Decrease to 0 (should remove item)
- [ ] Click delete button (should ask confirmation)
- [ ] Verify order summary updates in real-time
- [ ] Check "FREE" shipping displays

#### Empty Cart
- [ ] Remove all items
- [ ] Verify empty cart message displays
- [ ] Check "Browse Plants" button works
- [ ] Verify checkout button is disabled

---

### 4. Checkout Process

#### Pre-Checkout
- [ ] Add items to cart
- [ ] Click "Proceed to Checkout"
- [ ] Verify redirects to checkout page
- [ ] Check user details pre-filled from profile

#### Checkout Form
- [ ] Try submitting empty form (validation)
- [ ] Fill all required fields
- [ ] Verify COD payment method is selected
- [ ] Check order summary displays correctly
- [ ] Verify total amount is correct

#### Order Placement
- [ ] Click "Place Order"
- [ ] Verify loading state on button
- [ ] Check success modal appears
- [ ] Verify delivery code is displayed
- [ ] Copy delivery code
- [ ] Click "Back to Home"
- [ ] Verify cart count is now 0
- [ ] Check cart is empty

---

### 5. Navigation & UI

#### Header Navigation
- [ ] Click logo (should go to home)
- [ ] Test all nav links (Home, Plants, About, Contact)
- [ ] Click cart icon (should go to cart)
- [ ] Verify cart badge shows correct count
- [ ] Test auth link (Login/Username)
- [ ] Test mobile menu button
- [ ] Test mobile menu links

#### Footer
- [ ] Verify footer displays on all pages
- [ ] Test all footer links
- [ ] Check contact information is correct
- [ ] Verify copyright year

#### Responsive Design
- [ ] Test on mobile (375px width)
- [ ] Test on tablet (768px width)
- [ ] Test on desktop (1280px+ width)
- [ ] Verify no horizontal scroll
- [ ] Check all buttons are tappable
- [ ] Test form inputs on mobile

---

### 6. About & Contact Pages

#### About Us
- [ ] Navigate to About page
- [ ] Verify story text displays
- [ ] Check values section
- [ ] Test "Browse Our Plants" CTA button
- [ ] Verify images/icons load

#### Contact
- [ ] Navigate to Contact page
- [ ] Fill contact form
- [ ] Submit form
- [ ] Verify success message
- [ ] Check form resets after submission
- [ ] Verify contact information displays

---

### 7. Error Handling

#### Network Errors
- [ ] Stop backend server
- [ ] Try loading products (should show error)
- [ ] Try adding to cart (should show error)
- [ ] Try login (should show error)
- [ ] Restart backend, reload pages (should work)

#### Authentication Errors
- [ ] Delete token from localStorage
- [ ] Try accessing cart (should redirect)
- [ ] Try checkout (should redirect)
- [ ] Login again (should work)

#### Validation Errors
- [ ] Test all form validations
- [ ] Verify error messages are helpful
- [ ] Check errors clear on correction

---

## API Testing with cURL

### 1. Health Check
```bash
curl http://localhost:5000/health
# Expected: {"status":"healthy","service":"Green Haven Nursery API"}
```

### 2. Register User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123",
    "phone": "(555) 123-4567",
    "address": "123 Test St, City, ST 12345"
  }'
# Expected: 201 Created with user data
```

### 3. Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
# Expected: 200 OK with token
# Save token for next requests
```

### 4. Get Products
```bash
curl http://localhost:5000/api/products
# Expected: Array of 5 products
```

### 5. Add to Cart (requires token)
```bash
TOKEN="your-token-here"

curl -X POST http://localhost:5000/api/cart/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
# Expected: 200 OK
```

### 6. Get Cart
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/cart
# Expected: Cart with items
```

### 7. Checkout
```bash
curl -X POST http://localhost:5000/api/checkout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "delivery_address": "123 Test St",
    "payment_method": "COD"
  }'
# Expected: 201 Created with order and delivery code
```

---

## Database Testing

### 1. Verify Database Created
```bash
sqlite3 backend/database/ecommerce.db ".tables"
# Expected: List of 7 tables
```

### 2. Check Products Loaded
```sql
sqlite3 backend/database/ecommerce.db "SELECT name, price, stock FROM products;"
# Expected: 5 flowering plants
```

### 3. View Users
```sql
sqlite3 backend/database/ecommerce.db "SELECT id, name, email FROM users;"
# Expected: List of registered users
```

### 4. Check Orders
```sql
sqlite3 backend/database/ecommerce.db "SELECT id, delivery_code, total_amount, status FROM orders;"
# Expected: List of placed orders
```

---

## Performance Testing

### Load Time Checks
- [ ] Home page loads < 2 seconds
- [ ] Plants page loads < 2 seconds
- [ ] Cart operations < 500ms
- [ ] Checkout < 1 second
- [ ] Login/Register < 1 second

### Browser Console
- [ ] No JavaScript errors
- [ ] No 404 errors for resources
- [ ] CORS configured correctly
- [ ] API responses are JSON

---

## Security Testing

### Password Security
- [ ] Passwords are never visible in network tab
- [ ] Passwords are hashed in database (check with SQL)
- [ ] Login fails with wrong password
- [ ] Token expires after 7 days

### Authorization
- [ ] Cannot access cart without token
- [ ] Cannot checkout without token
- [ ] Invalid token returns 401
- [ ] Cannot access other user's data

### Input Validation
- [ ] SQL injection attempts fail
- [ ] XSS attempts are sanitized
- [ ] Long strings are rejected
- [ ] Special characters handled correctly

---

## Browser Compatibility

Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## Deployment Testing

### Pre-Deployment
- [ ] All tests pass locally
- [ ] No console errors
- [ ] Environment variables set
- [ ] Database migrated
- [ ] CORS configured for production domain

### Post-Deployment
- [ ] Frontend loads from production URL
- [ ] Backend API accessible
- [ ] Database connected
- [ ] Can register new user
- [ ] Can complete full checkout flow
- [ ] Email notifications work (if configured)

---

## Test Data

Use these test accounts:

```
Email: test1@example.com
Password: test123

Email: test2@example.com
Password: test123
```

Product IDs: 1-5 (Peace Lily, Orchid, African Violet, Anthurium, Begonia)

---

## Known Issues & Limitations

Current limitations (future enhancements):
- No product search/filter
- No order history page yet
- Email notifications require SMTP setup
- PDF invoices require additional configuration
- Payment is COD only (gateway integration future)

---

## Success Criteria

The application is ready for production when:
✅ All manual tests pass
✅ All API tests return expected responses
✅ No console errors
✅ Database properly initialized
✅ Authentication works correctly
✅ Full checkout flow completes
✅ Responsive on all devices
✅ Performance meets targets
✅ Security checks pass

---

## Test Automation (Future)

For production-grade testing, consider adding:
- Unit tests with pytest
- Integration tests with pytest-flask
- Frontend tests with Selenium/Playwright
- API tests with Postman/Newman
- Load testing with Locust

---

**Happy Testing! 🧪**
