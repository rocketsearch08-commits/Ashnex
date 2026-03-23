# ========================================
# ASHNEX AGROTRADE - FLASK APPLICATION
# Backend API Server
# ========================================

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# ===== CONFIGURATION =====
# Enable CORS (Cross-Origin Resource Sharing) for frontend access
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Database configuration (MongoDB)
MONGO_DB_URI = os.getenv('MONGO_DB_URI', 'mongodb://localhost:27017/')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'ashnex_agrotrade')

# API Keys (for admin operations)
ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'admin_key_change_in_production')

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== DATABASE CONNECTION =====
# This is a placeholder structure. For production, use PyMongo
# from pymongo import MongoClient
# client = MongoClient(MONGO_DB_URI)
# db = client[MONGO_DB_NAME]

# For development/testing, we'll use in-memory storage
# Replace this with actual MongoDB connection for production
in_memory_data = {
    'products': [],
    'contacts': [],
    'orders': []
}

# ===== SAMPLE PRODUCTS DATA =====
# This is loaded on startup for demonstration
SAMPLE_PRODUCTS = [
    {
        'id': 1,
        'name': 'Premium Cashew',
        'category': 'Cashew',
        'description': 'High-quality cashew nuts, perfectly roasted and graded for premium export',
        'price': 450,
        'unit': 'kg',
        'minOrder': '500 kg',
        'image': 'cashew.jpg'
    },
    {
        'id': 2,
        'name': 'Organic Ginger',
        'category': 'Ginger',
        'description': 'Fresh, organic ginger from Indian farms, ideal for spice markets worldwide',
        'price': 80,
        'unit': 'kg',
        'minOrder': '1 ton',
        'image': 'ginger.jpg'
    },
    {
        'id': 3,
        'name': 'Pure Turmeric Powder',
        'category': 'Turmeric',
        'description': 'Fine turmeric powder with high curcumin content, globally certified',
        'price': 150,
        'unit': 'kg',
        'minOrder': '500 kg',
        'image': 'turmeric.jpg'
    }
]

# ===== FLASK ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    """Handle 404 - Page Not Found"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 - Internal Server Error"""
    logger.error(f'Internal Server Error: {error}')
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

# ===== HEALTH CHECK ENDPOINT =====
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    API Endpoint: Health Check
    Returns server status
    """
    return jsonify({
        'status': 'ok',
        'message': 'Ashnex Agrotrade Server is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ===== PRODUCTS ENDPOINTS =====

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    API Endpoint: GET /api/products
    
    Retrieve all products with optional filtering
    
    Query Parameters:
    - category: Filter by category (optional)
    
    Returns:
    - List of products
    """
    try:
        category = request.args.get('category', None)
        
        # If category provided, filter products
        if category:
            products = [p for p in in_memory_data['products'] if p.get('category') == category]
        else:
            products = in_memory_data['products']
        
        return jsonify({
            'status': 'success',
            'products': products,
            'count': len(products)
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching products: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch products'
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    API Endpoint: GET /api/products/<id>
    
    Retrieve a specific product by ID
    
    Returns:
    - Single product details
    """
    try:
        product = next((p for p in in_memory_data['products'] if p.get('id') == product_id), None)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'product': product
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching product: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch product'
        }), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """
    API Endpoint: POST /api/products
    
    Add a new product (ADMIN ONLY)
    
    Required Headers:
    - Authorization: Bearer <ADMIN_API_KEY>
    
    Request Body:
    {
        "name": "Product Name",
        "category": "Category",
        "description": "Description",
        "price": 100,
        "unit": "kg",
        "minOrder": "500 kg"
    }
    """
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - Invalid API Key'
        }), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'category', 'description', 'price', 'unit']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {required_fields}'
            }), 400
        
        # Create new product
        new_product = {
            'id': len(in_memory_data['products']) + 1,
            'name': data.get('name'),
            'category': data.get('category'),
            'description': data.get('description'),
            'price': data.get('price'),
            'unit': data.get('unit'),
            'minOrder': data.get('minOrder', ''),
            'image': data.get('image', ''),
            'createdAt': datetime.utcnow().isoformat()
        }
        
        in_memory_data['products'].append(new_product)
        logger.info(f'New product added: {new_product["name"]}')
        
        return jsonify({
            'status': 'success',
            'message': 'Product added successfully',
            'product': new_product
        }), 201
    
    except Exception as e:
        logger.error(f'Error adding product: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to add product'
        }), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    API Endpoint: PUT /api/products/<id>
    
    Update an existing product (ADMIN ONLY)
    """
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - Invalid API Key'
        }), 401
    
    try:
        product = next((p for p in in_memory_data['products'] if p.get('id') == product_id), None)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
        
        data = request.get_json()
        
        # Update product fields
        product.update({
            'name': data.get('name', product.get('name')),
            'category': data.get('category', product.get('category')),
            'description': data.get('description', product.get('description')),
            'price': data.get('price', product.get('price')),
            'unit': data.get('unit', product.get('unit')),
            'minOrder': data.get('minOrder', product.get('minOrder')),
            'updatedAt': datetime.utcnow().isoformat()
        })
        
        logger.info(f'Product updated: {product["name"]}')
        
        return jsonify({
            'status': 'success',
            'message': 'Product updated successfully',
            'product': product
        }), 200
    
    except Exception as e:
        logger.error(f'Error updating product: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to update product'
        }), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    API Endpoint: DELETE /api/products/<id>
    
    Delete a product (ADMIN ONLY)
    """
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - Invalid API Key'
        }), 401
    
    try:
        product = next((p for p in in_memory_data['products'] if p.get('id') == product_id), None)
        
        if not product:
            return jsonify({
                'status': 'error',
                'message': 'Product not found'
            }), 404
        
        in_memory_data['products'].remove(product)
        logger.info(f'Product deleted: {product["name"]}')
        
        return jsonify({
            'status': 'success',
            'message': 'Product deleted successfully'
        }), 200
    
    except Exception as e:
        logger.error(f'Error deleting product: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete product'
        }), 500

# ===== CONTACT ENDPOINTS =====

@app.route('/api/contact', methods=['POST'])
def add_contact():
    """
    API Endpoint: POST /api/contact
    
    Add a new contact/inquiry
    
    Request Body:
    {
        "name": "Name",
        "email": "email@example.com",
        "phone": "+91 9999999999",
        "company": "Company Name",
        "subject": "product-inquiry",
        "message": "Message"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {missing}'
            }), 400
        
        # Create new contact
        new_contact = {
            'id': len(in_memory_data['contacts']) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'company': data.get('company', ''),
            'subject': data.get('subject', 'general'),
            'message': data.get('message'),
            'createdAt': datetime.utcnow().isoformat(),
            'status': 'new'
        }
        
        in_memory_data['contacts'].append(new_contact)
        logger.info(f'New contact received from: {new_contact["name"]} ({new_contact["email"]})')
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you! Your message has been received. We will get back to you within 24 hours.',
            'contact_id': new_contact['id'],
            'timestamp': new_contact['createdAt']
        }), 201
    
    except Exception as e:
        logger.error(f'Error adding contact: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to save contact inquiry. Please try again.'
        }), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """
    API Endpoint: GET /api/contacts
    
    Retrieve all contact inquiries (ADMIN ONLY)
    
    Required Headers:
    - Authorization: Bearer <ADMIN_API_KEY>
    """
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - Invalid API Key'
        }), 401
    
    try:
        return jsonify({
            'status': 'success',
            'contacts': in_memory_data['contacts'],
            'count': len(in_memory_data['contacts'])
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching contacts: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch contacts'
        }), 500

# ===== BULK ORDER ENDPOINTS =====

@app.route('/api/bulk-order', methods=['POST'])
def create_bulk_order():
    """
    API Endpoint: POST /api/bulk-order
    
    Create a new bulk order from customer
    
    Request Body:
    {
        "name": "Name",
        "email": "email@example.com",
        "product": "Product ID",
        "quantity": 1000,
        "message": "Special requirements"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'product', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {required_fields}'
            }), 400
        
        # Create new order
        new_order = {
            'id': len(in_memory_data['orders']) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'product': data.get('product'),
            'quantity': data.get('quantity'),
            'message': data.get('message', ''),
            'createdAt': datetime.utcnow().isoformat(),
            'status': 'pending'
        }
        
        in_memory_data['orders'].append(new_order)
        logger.info(f'New bulk order from: {new_order["name"]} - Quantity: {new_order["quantity"]}')
        
        return jsonify({
            'status': 'success',
            'message': 'Bulk order received. Our team will contact you with pricing details!',
            'order_id': new_order['id']
        }), 201
    
    except Exception as e:
        logger.error(f'Error creating bulk order: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to create bulk order'
        }), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """
    API Endpoint: GET /api/orders
    
    Retrieve all bulk orders (ADMIN ONLY)
    
    Required Headers:
    - Authorization: Bearer <ADMIN_API_KEY>
    """
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - Invalid API Key'
        }), 401
    
    try:
        return jsonify({
            'status': 'success',
            'orders': in_memory_data['orders'],
            'count': len(in_memory_data['orders'])
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching orders: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch orders'
        }), 500

# ===== ADMIN ENDPOINTS =====

@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    """
    API Endpoint: GET /api/admin/dashboard
    
    Get dashboard statistics (ADMIN ONLY)
    
    Required Headers:
    - Authorization: Bearer <ADMIN_API_KEY>
    """
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized - Invalid API Key'
        }), 401
    
    try:
        return jsonify({
            'status': 'success',
            'dashboard': {
                'totalProducts': len(in_memory_data['products']),
                'totalContacts': len(in_memory_data['contacts']),
                'totalOrders': len(in_memory_data['orders']),
                'pendingOrders': len([o for o in in_memory_data['orders'] if o.get('status') == 'pending']),
                'newContacts': len([c for c in in_memory_data['contacts'] if c.get('status') == 'new'])
            }
        }), 200
    
    except Exception as e:
        logger.error(f'Error fetching dashboard: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch dashboard'
        }), 500

# ===== INITIALIZATION =====

def init_data():
    """Initialize sample data on startup"""
    if not in_memory_data['products']:
        in_memory_data['products'] = SAMPLE_PRODUCTS
        logger.info(f'Sample data initialized with {len(SAMPLE_PRODUCTS)} products')

# ===== MAIN ENTRY POINT =====

if __name__ == '__main__':
    # Initialize data
    init_data()
    
    # Get Flask configuration
    debug_mode = os.getenv('FLASK_DEBUG', False)
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("\n" + "="*50)
    print("🌾 ASHNEX AGROTRADE - FLASK BACKEND")
    print("="*50)
    print(f"🚀 Server starting on {host}:{port}")
    print(f"🔧 Debug Mode: {debug_mode}")
    print(f"📊 Loaded Products: {len(in_memory_data['products'])}")
    print("="*50 + "\n")
    
    # Start Flask development server
    app.run(
        host=host,
        port=port,
        debug=debug_mode
    )
