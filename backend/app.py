# ========================================
# ASHNEX AGROTRADE - FLASK APPLICATION
# Backend API Server with MongoDB
# ========================================

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from bson import ObjectId
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# ===== CONFIGURATION =====
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
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

db = None

def get_db():
    """Get MongoDB connection, create if not exists"""
    global db
    if db is not None:
        return db
    try:
        client = MongoClient(MONGO_DB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        db = client[MONGO_DB_NAME]
        logger.info(f'✅ Connected to MongoDB: {MONGO_DB_NAME}')
        return db
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f'❌ MongoDB connection failed: {e}')
        return None

# Helper to convert ObjectId to string for JSON serialization
def serialize_doc(doc):
    """Convert MongoDB document to JSON-friendly dict"""
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    return doc

def serialize_docs(docs):
    """Convert list of MongoDB documents"""
    return [serialize_doc(d) for d in docs]

# ===== SAMPLE PRODUCTS DATA =====
SAMPLE_PRODUCTS = [
    {
        'name': 'Premium Cashew',
        'category': 'Cashew',
        'description': 'High-quality cashew nuts, perfectly roasted and graded for premium export',
        'price': 450,
        'unit': 'kg',
        'minOrder': '500 kg',
        'image': 'cashew.jpg'
    },
    {
        'name': 'Organic Ginger',
        'category': 'Ginger',
        'description': 'Fresh, organic ginger from Indian farms, ideal for spice markets worldwide',
        'price': 80,
        'unit': 'kg',
        'minOrder': '1 ton',
        'image': 'ginger.jpg'
    },
    {
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
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal Server Error: {error}')
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# ===== HEALTH CHECK =====
@app.route('/api/health', methods=['GET'])
def health_check():
    db_inst = get_db()
    return jsonify({
        'status': 'ok',
        'message': 'Ashnex Agrotrade Server is running',
        'database': 'connected' if db_inst is not None else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ===== PRODUCTS ENDPOINTS =====

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        category = request.args.get('category', None)
        query = {'category': category} if category else {}
        
        products = serialize_docs(db_inst.products.find(query))
        return jsonify({'status': 'success', 'products': products, 'count': len(products)}), 200
    except Exception as e:
        logger.error(f'Error fetching products: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to fetch products'}), 500

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        product = db_inst.products.find_one({'_id': ObjectId(product_id)})
        if not product:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        return jsonify({'status': 'success', 'product': serialize_doc(product)}), 200
    except Exception as e:
        logger.error(f'Error fetching product: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to fetch product'}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        data = request.get_json()
        required_fields = ['name', 'category', 'description', 'price', 'unit']
        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': f'Missing required fields: {required_fields}'}), 400
        
        new_product = {
            'name': data.get('name'),
            'category': data.get('category'),
            'description': data.get('description'),
            'price': data.get('price'),
            'unit': data.get('unit'),
            'minOrder': data.get('minOrder', ''),
            'image': data.get('image', ''),
            'createdAt': datetime.utcnow().isoformat()
        }
        
        result = db_inst.products.insert_one(new_product)
        new_product['_id'] = str(result.inserted_id)
        logger.info(f'New product added: {new_product["name"]}')
        
        return jsonify({'status': 'success', 'message': 'Product added', 'product': new_product}), 201
    except Exception as e:
        logger.error(f'Error adding product: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to add product'}), 500

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        data = request.get_json()
        update_data = {k: v for k, v in data.items() if k != '_id'}
        update_data['updatedAt'] = datetime.utcnow().isoformat()
        
        result = db_inst.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        updated = serialize_doc(db_inst.products.find_one({'_id': ObjectId(product_id)}))
        logger.info(f'Product updated: {product_id}')
        return jsonify({'status': 'success', 'message': 'Product updated', 'product': updated}), 200
    except Exception as e:
        logger.error(f'Error updating product: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to update product'}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        result = db_inst.products.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        logger.info(f'Product deleted: {product_id}')
        return jsonify({'status': 'success', 'message': 'Product deleted'}), 200
    except Exception as e:
        logger.error(f'Error deleting product: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to delete product'}), 500

# ===== CONTACT ENDPOINTS =====

@app.route('/api/contact', methods=['POST'])
def add_contact():
    """Public endpoint — anyone can submit a contact inquiry"""
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available. Please try again later.'}), 503

        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return jsonify({'status': 'error', 'message': f'Missing required fields: {missing}'}), 400
        
        # Create contact document
        new_contact = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'company': data.get('company', ''),
            'subject': data.get('subject', 'general'),
            'message': data.get('message'),
            'createdAt': datetime.utcnow().isoformat(),
            'status': 'new'
        }
        
        result = db_inst.contacts.insert_one(new_contact)
        new_contact['_id'] = str(result.inserted_id)
        logger.info(f'📩 New contact from: {new_contact["name"]} ({new_contact["email"]})')
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you! Your message has been received. We will get back to you within 24 hours.',
            'contact_id': new_contact['_id'],
            'timestamp': new_contact['createdAt']
        }), 201
    except Exception as e:
        logger.error(f'Error adding contact: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to save contact inquiry. Please try again.'}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Admin only — retrieve all contact inquiries"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        contacts = serialize_docs(db_inst.contacts.find().sort('createdAt', -1))
        return jsonify({'status': 'success', 'contacts': contacts, 'count': len(contacts)}), 200
    except Exception as e:
        logger.error(f'Error fetching contacts: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to fetch contacts'}), 500

@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Admin only — delete a contact message"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        result = db_inst.contacts.delete_one({'_id': ObjectId(contact_id)})
        if result.deleted_count == 0:
            return jsonify({'status': 'error', 'message': 'Contact not found'}), 404
        
        logger.info(f'Contact deleted: {contact_id}')
        return jsonify({'status': 'success', 'message': 'Contact deleted'}), 200
    except Exception as e:
        logger.error(f'Error deleting contact: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to delete contact'}), 500

# ===== BULK ORDER ENDPOINTS =====

@app.route('/api/bulk-order', methods=['POST'])
def create_bulk_order():
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        data = request.get_json()
        required_fields = ['name', 'email', 'product', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': f'Missing required fields: {required_fields}'}), 400
        
        new_order = {
            'name': data.get('name'),
            'email': data.get('email'),
            'product': data.get('product'),
            'quantity': data.get('quantity'),
            'message': data.get('message', ''),
            'createdAt': datetime.utcnow().isoformat(),
            'status': 'pending'
        }
        
        result = db_inst.orders.insert_one(new_order)
        new_order['_id'] = str(result.inserted_id)
        logger.info(f'📦 New bulk order from: {new_order["name"]} - Qty: {new_order["quantity"]}')
        
        return jsonify({
            'status': 'success',
            'message': 'Bulk order received. Our team will contact you with pricing!',
            'order_id': new_order['_id']
        }), 201
    except Exception as e:
        logger.error(f'Error creating bulk order: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to create bulk order'}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        orders = serialize_docs(db_inst.orders.find().sort('createdAt', -1))
        return jsonify({'status': 'success', 'orders': orders, 'count': len(orders)}), 200
    except Exception as e:
        logger.error(f'Error fetching orders: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to fetch orders'}), 500

# ===== ADMIN DASHBOARD =====

@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header.replace('Bearer ', '') != ADMIN_API_KEY:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        db_inst = get_db()
        if db_inst is None:
            return jsonify({'status': 'error', 'message': 'Database not available'}), 503

        return jsonify({
            'status': 'success',
            'dashboard': {
                'totalProducts': db_inst.products.count_documents({}),
                'totalContacts': db_inst.contacts.count_documents({}),
                'totalOrders': db_inst.orders.count_documents({}),
                'pendingOrders': db_inst.orders.count_documents({'status': 'pending'}),
                'newContacts': db_inst.contacts.count_documents({'status': 'new'})
            }
        }), 200
    except Exception as e:
        logger.error(f'Error fetching dashboard: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Failed to fetch dashboard'}), 500

# ===== INITIALIZATION =====

def init_data():
    """Seed sample products if collection is empty"""
    db_inst = get_db()
    if db_inst is not None:
        if db_inst.products.count_documents({}) == 0:
            db_inst.products.insert_many(SAMPLE_PRODUCTS)
            logger.info(f'🌱 Seeded {len(SAMPLE_PRODUCTS)} sample products')
        else:
            logger.info(f'📊 Existing products: {db_inst.products.count_documents({})}')
    else:
        logger.warning('⚠️ MongoDB not available — running without database')

# ===== MAIN ENTRY POINT =====

if __name__ == '__main__':
    init_data()
    
    debug_mode = os.getenv('FLASK_DEBUG', False)
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("\n" + "="*50)
    print("ASHNEX AGROTRADE - FLASK BACKEND")
    print("="*50)
    print(f"Server: {host}:{port}")
    print(f"MongoDB URI: {MONGO_DB_URI}")
    print(f"Database: {MONGO_DB_NAME}")
    print("="*50 + "\n")
    
    app.run(host=host, port=port, debug=debug_mode)
