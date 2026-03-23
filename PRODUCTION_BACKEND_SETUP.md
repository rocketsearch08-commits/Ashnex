# 🛠️ BACKEND: PRODUCTION-READY SETUP

This file contains production-optimized code for your Flask backend.

---

## 📋 TABLE OF CONTENTS

1. Requirements.txt (Updated)
2. Production app.py
3. Environment Configuration
4. Gunicorn Setup
5. Error Handling
6. Logging Setup
7. Security Headers
8. Rate Limiting

---

---

## 1️⃣ UPDATED requirements.txt

Replace your `backend/requirements.txt` with this:

```
Flask==2.3.2
Flask-CORS==4.0.0
pymongo==4.4.0
python-dotenv==1.0.0
gunicorn==21.2.0
flask-restx==0.5.1
Flask-Compress==1.13
Flask-Limiter==3.5.0
requests==2.31.0
python-dateutil==2.8.2
```

Install:
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

---

---

## 2️⃣ PRODUCTION app.py

Replace your `backend/app.py` with this production-ready version:

```python
import os
import logging
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
Compress(app)

# Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'admin_key_change_in_production')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8000')
MONGO_DB_URI = os.getenv('MONGO_DB_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'ashnex_agrotrade')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CORS Configuration (Production-ready)
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://ashnex.vercel.app",    # Vercel production
        "https://ashnex.netlify.app",   # Netlify alternative
        "https://ashnex.com",           # Custom domain
        "http://localhost:8000",        # Local development
        "http://localhost:3000"         # Local dev
    ],
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "supports_credentials": True
}})

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["500 per day", "100 per hour"],
    in_memory_fallback_enabled=True
)

# Security Headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
    return response

# Database Connection (MongoDB)
def get_db():
    """Get MongoDB connection"""
    try:
        client = MongoClient(MONGO_DB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[MONGO_DB_NAME]
        return db
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

# Authentication Decorator
def require_admin_key(f):
    """Decorator for admin-only endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '').strip()
        
        if not token or token != ADMIN_API_KEY:
            return jsonify({
                'status': 'error',
                'message': 'Unauthorized: Invalid API Key'
            }), 401
        
        return f(*args, **kwargs)
    return decorated

# In-Memory Data (Development)
in_memory_data = {
    'products': [
        {
            'id': 1,
            'name': 'Premium Cashew',
            'category': 'Cashew',
            'description': 'High-quality cashew nuts from India',
            'price': 450,
            'unit': 'kg',
            'minOrder': '500 kg',
            'image': 'cashew.jpg'
        },
        {
            'id': 2,
            'name': 'Organic Ginger',
            'category': 'Ginger',
            'description': 'Fresh ginger powder with natural oils',
            'price': 80,
            'unit': 'kg',
            'minOrder': '1 ton',
            'image': 'ginger.jpg'
        },
        {
            'id': 3,
            'name': 'Pure Turmeric',
            'category': 'Turmeric',
            'description': 'High-curcumin turmeric powder',
            'price': 120,
            'unit': 'kg',
            'minOrder': '500 kg',
            'image': 'turmeric.jpg'
        }
    ],
    'contacts': [],
    'orders': []
}

# ======================
# API ENDPOINTS
# ======================

# 1. Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    """API Health Check"""
    return jsonify({
        'status': 'ok',
        'message': 'Ashnex Agrotrade Backend is running',
        'environment': FLASK_ENV,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# 2. Get All Products
@app.route('/api/products', methods=['GET'])
@limiter.limit("30 per minute")
def get_products():
    """Get all products with optional category filter"""
    try:
        category = request.args.get('category')
        products = in_memory_data['products']
        
        if category:
            products = [p for p in products if p['category'].lower() == category.lower()]
        
        return jsonify({
            'status': 'success',
            'data': products,
            'count': len(products)
        }), 200
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve products'
        }), 500

# 3. Get Single Product
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        product = next((p for p in in_memory_data['products'] if p['id'] == product_id), None)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': product
        }), 200
    except Exception as e:
        logger.error(f"Error getting product: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve product'
        }), 500

# 4. Add Product (Admin Only)
@app.route('/api/products', methods=['POST'])
@require_admin_key
@limiter.limit("10 per minute")
def add_product():
    """Add new product (Admin only)"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'category', 'price', 'unit']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        new_product = {
            'id': max([p['id'] for p in in_memory_data['products']], default=0) + 1,
            'name': data['name'],
            'category': data['category'],
            'description': data.get('description', ''),
            'price': data['price'],
            'unit': data['unit'],
            'minOrder': data.get('minOrder', ''),
            'image': data.get('image', '')
        }
        
        in_memory_data['products'].append(new_product)
        logger.info(f"Product added: {new_product['name']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Product added successfully',
            'data': new_product
        }), 201
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to add product'
        }), 500

# 5. Update Product (Admin Only)
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@require_admin_key
@limiter.limit("10 per minute")
def update_product(product_id):
    """Update product (Admin only)"""
    try:
        product = next((p for p in in_memory_data['products'] if p['id'] == product_id), None)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
        
        data = request.get_json()
        product.update({k: v for k, v in data.items() if k != 'id'})
        
        logger.info(f"Product updated: {product['name']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Product updated successfully',
            'data': product
        }), 200
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to update product'
        }), 500

# 6. Delete Product (Admin Only)
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@require_admin_key
@limiter.limit("10 per minute")
def delete_product(product_id):
    """Delete product (Admin only)"""
    try:
        product = next((p for p in in_memory_data['products'] if p['id'] == product_id), None)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
        
        in_memory_data['products'].remove(product)
        logger.info(f"Product deleted: {product['name']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Product deleted successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete product'
        }), 500

# 7. Submit Contact (No Auth)
@app.route('/api/contact', methods=['POST'])
@limiter.limit("5 per minute")
def add_contact():
    """Submit contact inquiry"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'email', 'product', 'quantity', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        # Email validation
        if '@' not in data['email']:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email format'
            }), 400
        
        contact = {
            'id': len(in_memory_data['contacts']) + 1,
            'name': data['name'],
            'email': data['email'],
            'product': data['product'],
            'quantity': data['quantity'],
            'message': data['message'],
            'status': 'new',
            'createdAt': datetime.utcnow().isoformat()
        }
        
        in_memory_data['contacts'].append(contact)
        logger.info(f"Contact received from {data['email']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you! We will contact you soon.',
            'data': contact
        }), 201
    except Exception as e:
        logger.error(f"Error adding contact: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to submit contact'
        }), 500

# 8. Get All Contacts (Admin Only)
@app.route('/api/contacts', methods=['GET'])
@require_admin_key
def get_contacts():
    """Get all contacts (Admin only)"""
    try:
        return jsonify({
            'status': 'success',
            'data': in_memory_data['contacts'],
            'count': len(in_memory_data['contacts'])
        }), 200
    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve contacts'
        }), 500

# 9. Create Bulk Order
@app.route('/api/bulk-order', methods=['POST'])
@limiter.limit("10 per minute")
def create_bulk_order():
    """Create bulk order"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'company', 'product', 'quantity', 'unit']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400
        
        order = {
            'id': len(in_memory_data['orders']) + 1,
            'name': data['name'],
            'email': data['email'],
            'company': data['company'],
            'product': data['product'],
            'quantity': data['quantity'],
            'unit': data['unit'],
            'status': 'pending',
            'createdAt': datetime.utcnow().isoformat()
        }
        
        in_memory_data['orders'].append(order)
        logger.info(f"Bulk order created by {data['company']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Bulk order created successfully',
            'data': order
        }), 201
    except Exception as e:
        logger.error(f"Error creating bulk order: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to create bulk order'
        }), 500

# 10. Get All Orders (Admin Only)
@app.route('/api/orders', methods=['GET'])
@require_admin_key
def get_orders():
    """Get all orders (Admin only)"""
    try:
        return jsonify({
            'status': 'success',
            'data': in_memory_data['orders'],
            'count': len(in_memory_data['orders'])
        }), 200
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve orders'
        }), 500

# 11. Admin Dashboard
@app.route('/api/admin/dashboard', methods=['GET'])
@require_admin_key
def admin_dashboard():
    """Admin dashboard statistics"""
    try:
        stats = {
            'totalProducts': len(in_memory_data['products']),
            'totalContacts': len(in_memory_data['contacts']),
            'totalOrders': len(in_memory_data['orders']),
            'pendingOrders': len([o for o in in_memory_data['orders'] if o['status'] == 'pending']),
            'newContacts': len([c for c in in_memory_data['contacts'] if c['status'] == 'new']),
            'environment': FLASK_ENV,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'data': stats
        }), 200
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve dashboard stats'
        }), 500

# 12. Error Handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

# ======================
# STARTUP
# ======================

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🌾 ASHNEX AGROTRADE - FLASK BACKEND")
    logger.info("=" * 50)
    logger.info(f"🔧 Environment: {FLASK_ENV}")
    logger.info(f"🔐 Debug Mode: {DEBUG_MODE}")
    logger.info(f"📊 Products: {len(in_memory_data['products'])}")
    logger.info("=" * 50)
    
    # Production: Use gunicorn
    # gunicorn app:app --bind 0.0.0.0:5000
    
    # Development: Use Flask dev server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=DEBUG_MODE
    )
```

---

---

## 3️⃣ ENVIRONMENT CONFIGURATION

### Create backend/.env

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database
MONGO_DB_URI=mongodb+srv://ashnex_user:YOUR_PASSWORD@cluster-name.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=ashnex_agrotrade

# Security
ADMIN_API_KEY=generate_strong_key_with_python_secrets

# Frontend URL (Update after deployment)
FRONTEND_URL=https://ashnex.vercel.app
```

### Generate Secure Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Output: Copy this to ADMIN_API_KEY

---

---

## 4️⃣ GUNICORN SETUP (Production Server)

### Local Test with Gunicorn

```bash
cd backend
venv\Scripts\activate
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

### Render Configuration

In Render dashboard:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`

---

---

## 5️⃣ MONGODB INTEGRATION (Optional)

If you want to use MongoDB instead of in-memory storage:

```python
# In app.py, replace the in-memory data usage with:

@app.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    if not db:
        return jsonify({'status': 'error', 'message': 'Database error'}), 500
    
    products = list(db.products.find({}, {'_id': 0}))
    category = request.args.get('category')
    
    if category:
        products = [p for p in products if p['category'].lower() == category.lower()]
    
    return jsonify({
        'status': 'success',
        'data': products,
        'count': len(products)
    }), 200
```

---

---

## 🎯 SUMMARY

✅ Production-ready Flask app
✅ CORS for Vercel frontend
✅ Rate limiting protection
✅ Security headers
✅ Comprehensive logging
✅ Error handling
✅ Admin authentication
✅ 11 API endpoints
✅ Gunicorn ready
✅ MongoDB compatible
