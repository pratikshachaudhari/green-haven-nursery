# 📡 Green Haven Nursery - API Documentation

## Base URL
```
Development: http://localhost:5000
Production:  https://your-app.onrender.com
```

All endpoints are prefixed with `/api` unless noted otherwise.

---

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Tokens expire after 7 days.

---

## Response Format

### Success Response
```json
{
  "data": {...},
  "message": "Success message"
}
```

### Error Response
```json
{
  "message": "Error description"
}
```

---

## Endpoints

### 🏥 Health Check

#### `GET /health`
Check if API is running.

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "service": "Green Haven Nursery API"
}
```

---

## 👤 Authentication Endpoints

### Register User

#### `POST /api/register`

Create a new user account.

**Authentication:** Not required

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "phone": "(555) 123-4567",
  "address": "123 Main St, City, State 12345"
}
```

**Validation Rules:**
- `name`: Required, 1-100 characters
- `email`: Required, valid email format, unique
- `password`: Required, minimum 6 characters
- `phone`: Required, valid phone format
- `address`: Required, 1-500 characters

**Success Response (201):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "address": "123 Main St, City, State 12345",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error Responses:**
- `400`: Missing required fields or validation failed
- `409`: Email already registered

---

### Login

#### `POST /api/login`

Authenticate user and receive JWT token.

**Authentication:** Not required

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "address": "123 Main St, City, State 12345"
  }
}
```

**Error Responses:**
- `400`: Missing email or password
- `401`: Invalid credentials

---

### Get Profile

#### `GET /api/profile`

Get current user's profile.

**Authentication:** Required

**Success Response (200):**
```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "address": "123 Main St, City, State 12345",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Error Responses:**
- `401`: Not authenticated or invalid token
- `404`: User not found

---

### Update Profile

#### `PUT /api/profile`

Update user profile information.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "John Updated",
  "phone": "(555) 987-6543",
  "address": "456 New St, City, State 12345"
}
```

**Note:** All fields are optional. Only provided fields will be updated.

**Success Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "name": "John Updated",
    "email": "john@example.com",
    "phone": "(555) 987-6543",
    "address": "456 New St, City, State 12345"
  }
}
```

**Error Responses:**
- `400`: Invalid phone format
- `401`: Not authenticated

---

## 🌱 Product Endpoints

### Get All Products

#### `GET /api/products`

Retrieve all products.

**Authentication:** Not required

**Success Response (200):**
```json
[
  {
    "id": 1,
    "name": "Peace Lily",
    "description": "Elegant white blooms with glossy dark green leaves...",
    "price": 24.99,
    "image_url": "https://images.unsplash.com/...",
    "stock": 15,
    "category": "flowering"
  },
  {
    "id": 2,
    "name": "Orchid Phalaenopsis",
    "description": "Stunning exotic flowers in vibrant pink...",
    "price": 39.99,
    "image_url": "https://images.unsplash.com/...",
    "stock": 10,
    "category": "flowering"
  }
]
```

---

### Get Single Product

#### `GET /api/products/<id>`

Get details of a specific product.

**Authentication:** Not required

**Parameters:**
- `id` (path): Product ID (integer)

**Success Response (200):**
```json
{
  "id": 1,
  "name": "Peace Lily",
  "description": "Elegant white blooms with glossy dark green leaves...",
  "price": 24.99,
  "image_url": "https://images.unsplash.com/...",
  "stock": 15,
  "category": "flowering"
}
```

**Error Responses:**
- `404`: Product not found

---

## 🛒 Cart Endpoints

### Get Cart

#### `GET /api/cart`

Get current user's cart with all items.

**Authentication:** Required

**Success Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Peace Lily",
        "description": "Elegant white blooms...",
        "price": 24.99,
        "image_url": "https://...",
        "stock": 15,
        "category": "flowering"
      },
      "quantity": 2,
      "subtotal": 49.98
    },
    {
      "id": 2,
      "product": {
        "id": 3,
        "name": "African Violet",
        "description": "Charming purple flowers...",
        "price": 18.99,
        "image_url": "https://...",
        "stock": 20,
        "category": "flowering"
      },
      "quantity": 1,
      "subtotal": 18.99
    }
  ],
  "total": 68.97,
  "item_count": 2
}
```

**Error Responses:**
- `401`: Not authenticated

---

### Add Item to Cart

#### `POST /api/cart/add`

Add a product to the cart or increase quantity if already exists.

**Authentication:** Required

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Validation Rules:**
- `product_id`: Required, must exist
- `quantity`: Required, must be positive integer

**Success Response (200):**
```json
{
  "message": "Item added to cart",
  "cart_item": {
    "id": 1,
    "product": {
      "id": 1,
      "name": "Peace Lily",
      "price": 24.99
    },
    "quantity": 2,
    "subtotal": 49.98
  }
}
```

**Error Responses:**
- `400`: Invalid product_id or quantity
- `401`: Not authenticated
- `404`: Product not found
- `409`: Product out of stock

---

### Remove Item from Cart

#### `POST /api/cart/remove`

Remove a product from the cart completely.

**Authentication:** Required

**Request Body:**
```json
{
  "product_id": 1
}
```

**Success Response (200):**
```json
{
  "message": "Item removed from cart"
}
```

**Error Responses:**
- `400`: Invalid product_id
- `401`: Not authenticated
- `404`: Item not in cart

---

### Update Cart Item Quantity

#### `PUT /api/cart/update`

Update the quantity of an item in the cart.

**Authentication:** Required

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 5
}
```

**Validation Rules:**
- `quantity`: Must be positive integer
- If quantity is 0, item will be removed

**Success Response (200):**
```json
{
  "message": "Cart updated",
  "cart_item": {
    "id": 1,
    "product": {
      "id": 1,
      "name": "Peace Lily",
      "price": 24.99
    },
    "quantity": 5,
    "subtotal": 124.95
  }
}
```

**Error Responses:**
- `400`: Invalid quantity
- `401`: Not authenticated
- `404`: Item not in cart
- `409`: Insufficient stock

---

## 📦 Order Endpoints

### Place Order (Checkout)

#### `POST /api/checkout`

Create an order from cart contents and process payment (COD).

**Authentication:** Required

**Request Body:**
```json
{
  "delivery_address": "123 Main St, City, State 12345",
  "payment_method": "COD"
}
```

**Validation Rules:**
- `delivery_address`: Required
- `payment_method`: Must be "COD"
- Cart must not be empty
- All products must be in stock

**Success Response (201):**
```json
{
  "message": "Order placed successfully",
  "order": {
    "id": 1,
    "user_id": 1,
    "total_amount": 68.97,
    "status": "confirmed",
    "delivery_code": "GH-A7K9X2M4",
    "delivery_address": "123 Main St, City, State 12345",
    "created_at": "2024-01-15T14:30:00",
    "payment_method": "COD",
    "payment_status": "pending",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Peace Lily",
          "description": "Elegant white blooms...",
          "price": 24.99,
          "image_url": "https://...",
          "stock": 13,
          "category": "flowering"
        },
        "quantity": 2,
        "price": 24.99,
        "subtotal": 49.98
      }
    ]
  }
}
```

**Error Responses:**
- `400`: Invalid request or empty cart
- `401`: Not authenticated
- `409`: Product out of stock

**Side Effects:**
- Cart is cleared
- Product stock is reduced
- Order email is sent (if configured)

---

### Get User Orders

#### `GET /api/orders`

Get all orders for the current user.

**Authentication:** Required

**Success Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "total_amount": 68.97,
    "status": "confirmed",
    "delivery_code": "GH-A7K9X2M4",
    "delivery_address": "123 Main St, City, State 12345",
    "created_at": "2024-01-15T14:30:00",
    "payment_method": "COD",
    "payment_status": "pending",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Peace Lily",
          "price": 24.99
        },
        "quantity": 2,
        "price": 24.99,
        "subtotal": 49.98
      }
    ]
  }
]
```

**Error Responses:**
- `401`: Not authenticated

---

### Get Single Order

#### `GET /api/orders/<id>`

Get details of a specific order.

**Authentication:** Required

**Parameters:**
- `id` (path): Order ID (integer)

**Success Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": 68.97,
  "status": "confirmed",
  "delivery_code": "GH-A7K9X2M4",
  "delivery_address": "123 Main St, City, State 12345",
  "created_at": "2024-01-15T14:30:00",
  "payment_method": "COD",
  "payment_status": "pending",
  "items": [...]
}
```

**Error Responses:**
- `401`: Not authenticated
- `403`: Not your order
- `404`: Order not found

---

## 📊 Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Not authorized to access resource |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (duplicate email, out of stock) |
| 500 | Internal Server Error | Server error |

---

## 🔐 Authentication Flow

1. **Register:** `POST /api/register` → Get user object
2. **Login:** `POST /api/login` → Get JWT token
3. **Store token:** Save in localStorage: `localStorage.setItem('token', token)`
4. **Use token:** Include in all authenticated requests
5. **Token expires:** After 7 days, user must login again

---

## 💡 Example Usage

### Complete User Journey

```javascript
// 1. Register
const registerResponse = await fetch('http://localhost:5000/api/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    password: 'test123',
    phone: '5551234567',
    address: '123 Test St'
  })
});

// 2. Login
const loginResponse = await fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'test123'
  })
});
const { token } = await loginResponse.json();

// 3. Get products
const products = await fetch('http://localhost:5000/api/products');

// 4. Add to cart
await fetch('http://localhost:5000/api/cart/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    product_id: 1,
    quantity: 2
  })
});

// 5. Checkout
const orderResponse = await fetch('http://localhost:5000/api/checkout', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    delivery_address: '123 Test St',
    payment_method: 'COD'
  })
});
const { order } = await orderResponse.json();
console.log('Delivery Code:', order.delivery_code);
```

---

## 🐛 Error Handling

Always check response status and handle errors:

```javascript
try {
  const response = await fetch(url, options);
  const data = await response.json();
  
  if (!response.ok) {
    // Handle error
    console.error(data.message);
    return;
  }
  
  // Handle success
  console.log(data);
} catch (error) {
  console.error('Network error:', error);
}
```

---

## 🔄 Rate Limiting

Currently no rate limiting implemented. For production, consider:
- 100 requests per minute per IP
- 1000 requests per hour per user
- Use flask-limiter package

---

## 📝 Notes

- All timestamps are in ISO 8601 format (UTC)
- Prices are in USD with 2 decimal places
- Stock levels are updated in real-time during checkout
- Delivery codes are unique 8-character alphanumeric strings
- Cart persists across sessions until checkout
- Orders cannot be modified after creation

---

**Happy coding! 🚀**
