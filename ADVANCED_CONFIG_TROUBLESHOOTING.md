# 🛡️ ADVANCED CONFIGURATION & TROUBLESHOOTING

Production deployment advanced setup, customization, and problem-solving.

---

## 📋 TABLE OF CONTENTS

1. WhatsApp Integration
2. Email Notifications
3. MongoDB Migration from In-Memory
4. Advanced Security
5. Performance Tuning
6. Troubleshooting
7. Monitoring & Logging

---

---

## 📞 WHATSAPP INTEGRATION

### 1.1 Setup WhatsApp Business

**Option A: Direct WhatsApp Link (Free)**

```html
<!-- Add to your HTML -->
<a href="https://wa.me/+923334751234?text=Hello%20Ashnex" target="_blank">
    <i class="fab fa-whatsapp"></i> Chat with us
</a>
```

Format:
```
https://wa.me/+[COUNTRY_CODE][PHONE_WITHOUT_PLUS]?text=[MESSAGE]
```

Example:
```
https://wa.me/+923334751234?text=Hello%20Ashnex%20Agrotrade
```

**Country Codes:**
- Pakistan: +92
- India: +91
- USA: +1
- UK: +44

### 1.2 WhatsApp API (Advanced - Paid)

For automated WhatsApp messages:

```python
# backend/whatsapp_service.py
import requests

WHATSAPP_API = "https://graph.instagram.com/v17.0/YOUR_PHONE_ID/messages"
WHATSAPP_TOKEN = "YOUR_ACCESS_TOKEN"

def send_whatsapp_message(phone, message):
    """Send WhatsApp message via WhatsApp Cloud API"""
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(WHATSAPP_API, json=payload, headers=headers)
    return response.json()
```

Setup: https://www.twilio.com/en-us/messaging/whatsapp

---

---

## 📧 EMAIL NOTIFICATIONS

### 2.1 Send Email with Flask-Mail

```bash
# Add to requirements.txt
Flask-Mail==0.9.1
```

```python
# backend/app.py
from flask_mail import Mail, Message
import os

# Configure email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

mail = Mail(app)

def send_contact_email(contact_data):
    """Send email when contact form is submitted"""
    try:
        msg = Message(
            subject=f"New Contact: {contact_data['name']}",
            sender=os.getenv('EMAIL_USER'),
            recipients=['admin@ashnex.com'],
            body=f"""
New contact inquiry:

Name: {contact_data['name']}
Email: {contact_data['email']}
Product: {contact_data['product']}
Quantity: {contact_data['quantity']}
Message: {contact_data['message']}
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Email error: {e}")
        return False
```

### 2.2 .env Configuration

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

**Get Gmail App Password:**
1. Go to myaccount.google.com
2. Security → 2-factor authentication
3. App passwords → Select "Mail" and "Windows Computer"
4. Google generates a 16-character password
5. Use this in EMAIL_PASSWORD

---

---

## 🗄️ MONGODB MIGRATION (From In-Memory to Cloud)

### 3.1 Export In-Memory Data

```python
# backend/export_data.py
import json
from app import in_memory_data

# Export to JSON
with open('data_backup.json', 'w') as f:
    json.dump(in_memory_data, f, indent=2)

print("Data exported to data_backup.json")
```

### 3.2 Import to MongoDB

```python
# backend/import_to_mongodb.py
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGO_DB_URI'))
db = client[os.getenv('MONGO_DB_NAME')]

# Load data
with open('data_backup.json', 'r') as f:
    data = json.load(f)

# Insert collections
for collection_name, documents in data.items():
    if documents:
        db[collection_name].insert_many(documents)
        print(f"Inserted {len(documents)} documents into {collection_name}")

client.close()
print("✅ Data imported to MongoDB!")
```

### 3.3 Use MongoDB in Backend

```python
# backend/app.py - Replace in-memory with MongoDB

def get_db():
    """Get MongoDB connection"""
    client = MongoClient(os.getenv('MONGO_DB_URI'))
    db = client[os.getenv('MONGO_DB_NAME')]
    return db

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get products from MongoDB"""
    db = get_db()
    
    try:
        category = request.args.get('category')
        query = {}
        
        if category:
            query['category'] = category
        
        products = list(db.products.find(query, {'_id': 0}))
        
        return jsonify({
            'status': 'success',
            'data': products,
            'count': len(products)
        }), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500

@app.route('/api/contact', methods=['POST'])
def add_contact():
    """Submit contact to MongoDB"""
    db = get_db()
    
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'email', 'product', 'quantity', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
        
        contact = {
            'name': data['name'],
            'email': data['email'],
            'product': data['product'],
            'quantity': data['quantity'],
            'message': data['message'],
            'status': 'new',
            'createdAt': datetime.utcnow()
        }
        
        result = db.contacts.insert_one(contact)
        contact['_id'] = str(result.inserted_id)
        
        # Optional: Send email
        # send_contact_email(contact)
        
        return jsonify({
            'status': 'success',
            'message': 'Contact submitted successfully',
            'data': contact
        }), 201
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to submit'}), 500
```

---

---

## 🔒 ADVANCED SECURITY

### 4.1 JWT Authentication

```bash
# Add to requirements.txt
PyJWT==2.8.1
```

```python
# backend/auth.py
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_change_in_production')

def generate_token(user_id, expires_in=86400):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'status': 'error', 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'status': 'error', 'message': 'Token missing'}), 401
        
        payload = verify_token(token)
        
        if not payload:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated
```

### 4.2 Rate Limiting Configuration

```python
# backend/app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://"
)

# Apply to sensitive endpoints
@app.route('/api/contact', methods=['POST'])
@limiter.limit("5 per minute")
def add_contact():
    # Your code here
    pass

# Get remaining requests
@app.route('/api/rate-limit', methods=['GET'])
def check_rate_limit():
    """Check your current rate limit status"""
    return jsonify({
        'remaining': request.environ.get('flask_limiter.remaining', 'unknown'),
        'reset': request.environ.get('flask_limiter.reset', 'unknown')
    })
```

### 4.3 Input Sanitization

```python
# backend/security.py
import re
from bleach import clean

def sanitize_input(input_str, max_length=1000):
    """Sanitize user input"""
    # Remove HTML tags
    sanitized = clean(input_str, tags=[], strip=True)
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    # Remove special characters (keep safe ones)
    sanitized = re.sub(r'[<>{}\\]', '', sanitized)
    
    return sanitized.strip()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

---

---

## ⚡ PERFORMANCE TUNING

### 5.1 Caching

```python
# backend/app.py
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/products', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_products():
    # Products don't change often
    # Cache increases performance
    pass
```

### 5.2 Database Indexing

```javascript
// MongoDB - Create these indexes for performance

// Products collection
db.products.createIndex({ "category": 1 })
db.products.createIndex({ "name": "text" })

// Contacts collection
db.contacts.createIndex({ "email": 1 })
db.contacts.createIndex({ "createdAt": -1 })
db.contacts.createIndex({ "status": 1 })

// Orders collection
db.orders.createIndex({ "status": 1, "createdAt": -1 })
```

### 5.3 Query Optimization

```python
# Slow query
contacts = db.contacts.find({})
for contact in contacts:
    if contact['status'] == 'new':
        print(contact)

# Optimized query
contacts = db.contacts.find({ "status": "new" }, { "_id": 0 })
```

---

---

## 🐛 TROUBLESHOOTING

### Issue 1: CORS Error

**Error**: "Access to XMLHttpRequest blocked by CORS policy"

**Solution**:
```python
# In backend/app.py
CORS(app, resources={r"/api/*": {
    "origins": ["https://ashnex.vercel.app"],
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "PUT", "DELETE"]
}})
```

### Issue 2: MongoDB Connection Failed

**Error**: "Cannot connect to MongoDB Atlas"

**Solutions**:
1. Check connection string in .env file
2. Verify username/password correct
3. Check IP whitelist (Network Access)
4. Verify database exists
5. Check network connectivity

### Issue 3: Render Backend Sleeping

**Problem**: Backend goes to sleep after 15 min of inactivity (free tier)

**Solution 1**: Upgrade to paid tier ($7/month)

**Solution 2**: Keep alive with cron job
```python
# backend/keep_alive.py
import schedule
import time
import requests

def ping_backend():
    try:
        requests.get('https://ashnex-backend.onrender.com/api/health')
        print("✅ Backend pinged")
    except:
        print("❌ Ping failed")

schedule.every(10).minutes.do(ping_backend)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Issue 4: Contact Form Not Working

**Debug Steps**:
1. Open browser console (F12)
2. Go to Network tab
3. Submit form
4. Check POST request status
5. If error, note the status code:
   - 400: Bad request (missing field)
   - 401: Unauthorized (bad API key)
   - 500: Server error (check Render logs)

### Issue 5: Images Not Loading

**Solutions**:
1. Check image paths (relative vs absolute)
2. Verify images are in frontend folder
3. Check file names are correct
4. Use CDN for images

### Issue 6: Website Slow

**Solutions**:
1. Compress images (TinyPNG)
2. Enable caching
3. Use CDN for assets
4. Optimize database queries
5. Check Vercel/Render performance metrics

---

---

## 📊 MONITORING & LOGGING

### 7.1 Render Logs

```
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs
5. Filter by level (INFO, ERROR, WARNING)
```

### 7.2 Backend Logging

```python
# backend/app.py
import logging

logger = logging.getLogger(__name__)

# Log levels
logger.debug("Debug info")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error")

# Example
if not user:
    logger.warning(f"User not found: {user_id}")
    return jsonify({'error': 'User not found'}), 404
```

### 7.3 Application Monitoring Tools

**Free Options**:
- **Vercel Analytics**: Built-in, free
- **Render Metrics**: Built-in, free  
- **Sentry**: Free tier for error tracking
- **LogRocket**: Free tier for session replay

**Sentry Setup**:
```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    "YOUR_SENTRY_DSN",
    traces_sample_rate=1.0
)
```

---

---

## 📱 ANALYTICS & TRACKING

### Google Analytics

```html
<!-- Add to frontend/index.html head -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Track Events

```javascript
// Track button clicks
document.getElementById('contact-btn').addEventListener('click', () => {
    gtag('event', 'contact_click', {
        'event_category': 'engagement',
        'event_label': 'Contact Button'
    });
});

// Track form submission
gtag('event', 'contact_form_submit', {
    'form_name': 'contact',
    'product': this.contactForm.product
});
```

---

---

## 🚀 DEPLOYMENT UPDATES

### Update Code After Deployment

```bash
# Make changes locally
# Test locally
# Commit to Git
git add .
git commit -m "Fix: Update API endpoint"
git push

# Vercel auto-deploys (wait 1-2 min)
# Render auto-deploys (wait 2-3 min)
```

### Zero-Downtime Deployment

```bash
# Create new version
git tag -a v1.1.0 -m "Release 1.1.0"
git push origin v1.1.0

# Vercel/Render detect tag
# Deploy new version
# Old version still accessible
```

---

---

## 💰 COST OPTIMIZATION

### Free Tier Limits

| Service | Limit | Solution |
|---------|-------|----------|
| Vercel | 100 GB bandwidth | Upgrade to Pro |
| Render | 750 hours/month | Upgrade to paid |
| MongoDB | 512 MB storage | Upgrade to Atlas |
| Bandwidth | Varies | Use CDN |

### Cost Estimation (Monthly)

```
Development:
- Vercel: $0
- Render: $0 (backend sleeps)
- MongoDB: $0
- Domain: $0/month ($15/year)
Total: $0/month

Production:
- Vercel: $20 (Pro tier)
- Render: $7 (Starter tier)
- MongoDB: $0 (free tier)
- Domain: $1.25/month ($15/year)
Total: $28.25/month
```

---

---

## ✨ ADVANCED FEATURES

### WhatsApp Automated Responses

```python
# backend/whatsapp_handler.py
def handle_incoming_whatsapp(message):
    """Handle incoming WhatsApp message"""
    
    if 'product' in message.lower():
        response = "Available products: Cashew, Ginger, Turmeric"
    elif 'price' in message.lower():
        response = "Please contact us for pricing"
    elif 'order' in message.lower():
        response = "You can place orders on our website"
    else:
        response = "Thank you for reaching out to Ashnex Agrotrade!"
    
    return response
```

### Automated Emails

```python
# Send automatic responses
@app.route('/api/contact', methods=['POST'])
def add_contact():
    # ... save contact ...
    
    # Send auto-reply
    send_email(
        to=contact['email'],
        subject="Thank you for contacting Ashnex",
        body="We will respond within 24 hours"
    )
```

---

---

## 🎯 PRODUCTION CHECKLIST

- [ ] HTTPS everywhere
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] API keys secure
- [ ] Database connection secure
- [ ] Environment variables set
- [ ] Error handling implemented
- [ ] Rate limiting enabled
- [ ] Input validation done
- [ ] Logging configured
- [ ] Backups automated
- [ ] Monitoring enabled
- [ ] Performance optimized
- [ ] Team trained on deployment

---

**🚀 Your production deployment is complete and secure!**
