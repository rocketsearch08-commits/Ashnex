# Ashnex Agrotrade - Professional Import-Export Website

A fully responsive, modern business website for premium agricultural products with Vue.js frontend, Flask backend, and MongoDB database.

**Company**: Ashnex Agrotrade  
**Tagline**: Domestic & Global Supply 🌍  
**Products**: Cashew, Ginger, Turmeric, and other premium agricultural commodities

---

## 📋 Project Structure

```
ashnex/
├── frontend/                    # Vue.js + HTML/CSS Frontend
│   ├── index.html              # Main HTML file
│   ├── css/
│   │   └── style.css           # Complete styling (1000+ lines)
│   ├── js/
│   │   └── app.js              # Vue.js 3 application
│   └── images/                 # Product images folder
│
├── backend/                     # Flask Python Backend
│   ├── app.py                  # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── models/
│   │   └── models_documentation.py  # MongoDB schemas
│   └── routes/                 # API routes (expandable)
│
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js/npm** (optional, for package management) - [Download](https://nodejs.org/)
- **MongoDB** (local or Atlas account) - [Download](https://www.mongodb.com/try/download/community)
- **Git** (optional) - [Download](https://git-scm.com/)

---

## 📦 Installation & Setup

### Step 1: Backend Setup (Flask)

#### 1.1 Navigate to backend folder
```bash
cd backend
```

#### 1.2 Create Python Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 1.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 1.4 Setup Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env file with your configuration
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
```

**Important settings in `.env`:**
```
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
MONGO_DB_URI=mongodb://localhost:27017/
MONGO_DB_NAME=ashnex_agrotrade
ADMIN_API_KEY=your_secure_key_here
```

#### 1.5 Start Flask Development Server
```bash
python app.py
```

You should see:
```
🌾 ASHNEX AGROTRADE - FLASK BACKEND
==================================================
🚀 Server starting on 0.0.0.0:5000
🔧 Debug Mode: True
📊 Loaded Products: 3
==================================================
```

✅ **Backend running at**: `http://localhost:5000`

---

### Step 2: Frontend Setup (Vue.js)

#### 2.1 Navigate to frontend folder
```bash
cd frontend
```

#### 2.2 Open Frontend in Browser

**Option A: Simple File Server (Recommended for beginners)**

Windows:
```bash
# Using Python built-in server
python -m http.server 8000
```

Mac/Linux:
```bash
# Using Python built-in server
python3 -m http.server 8000

# OR using Node.js http-server
npx http-server --port 8000
```

Then open: `http://localhost:8000`

**Option B: Visual Studio Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click on `index.html` → "Open with Live Server"

✅ **Frontend running at**: `http://localhost:8000`

---

### Step 3: MongoDB Setup (Optional for Development)

#### Option A: Local MongoDB

**Windows:**
1. Download MongoDB Community Edition: https://www.mongodb.com/try/download/community
2. Run the installer
3. MongoDB will start as a service
4. Verify: Open MongoDB Compass → Connect to `mongodb://localhost:27017`

**Mac (using Homebrew):**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

#### Option B: MongoDB Atlas (Cloud - Recommended)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a cluster
4. Get connection string
5. Update `.env`:
```
MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

---

## 🔗 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Available Endpoints

#### Health Check
```http
GET /api/health
```
Response: `{ "status": "ok" }`

---

#### Get All Products
```http
GET /api/products
GET /api/products?category=Cashew
```

Request:
```
curl http://localhost:5000/api/products
```

Response:
```json
{
  "status": "success",
  "products": [
    {
      "id": 1,
      "name": "Premium Cashew",
      "category": "Cashew",
      "description": "...",
      "price": 450,
      "minOrder": "500 kg"
    }
  ],
  "count": 3
}
```

---

#### Get Single Product
```http
GET /api/products/{id}
```

---

#### Submit Contact Form
```http
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "product": "Cashew",
  "quantity": 500,
  "message": "I'm interested in bulk orders"
}
```

Response:
```json
{
  "status": "success",
  "message": "Contact inquiry received. We will contact you soon!",
  "contact_id": 1
}
```

---

#### Create Bulk Order
```http
POST /api/bulk-order
Content-Type: application/json

{
  "name": "ABC Company",
  "email": "orders@abc.com",
  "product": "Ginger",
  "quantity": 1000,
  "message": "Monthly supply needed"
}
```

---

#### Admin: Get All Contacts
```http
GET /api/contacts
Authorization: Bearer admin_key_change_in_production
```

---

#### Admin: Get All Orders
```http
GET /api/orders
Authorization: Bearer admin_key_change_in_production
```

---

#### Admin: Add New Product
```http
POST /api/products
Authorization: Bearer admin_key_change_in_production
Content-Type: application/json

{
  "name": "New Product",
  "category": "Category",
  "description": "Description",
  "price": 100,
  "unit": "kg",
  "minOrder": "100 kg"
}
```

---

#### Admin: Update Product
```http
PUT /api/products/{id}
Authorization: Bearer admin_key_change_in_production
Content-Type: application/json

{
  "price": 250,
  "minOrder": "200 kg"
}
```

---

#### Admin: Delete Product
```http
DELETE /api/products/{id}
Authorization: Bearer admin_key_change_in_production
```

---

#### Admin: Dashboard Statistics
```http
GET /api/admin/dashboard
Authorization: Bearer admin_key_change_in_production
```

---

## 🧪 Testing the Website

### Frontend Features to Test

1. **Responsive Design**
   - [ ] Test on desktop (1920x1080)
   - [ ] Test on tablet (768px)
   - [ ] Test on mobile (375px)
   - [ ] Test hamburger menu on mobile

2. **Navigation**
   - [ ] Click all navigation links
   - [ ] Smooth scrolling works
   - [ ] Active menu items highlight

3. **Products Section**
   - [ ] Filter by category works
   - [ ] Product cards display correctly
   - [ ] Hover effects work

4. **Contact Form**
   - [ ] Form validation works
   - [ ] Required fields show error
   - [ ] Invalid email shows error
   - [ ] Form submission sends to backend
   - [ ] Success message displays

5. **WhatsApp Integration**
   - [ ] WhatsApp button opens chat window

### Example Test Case: Submit Contact Form

```javascript
// Open browser console and run:
// (Backend must be running on http://localhost:5000)

fetch('http://localhost:5000/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Test User',
        email: 'test@example.com',
        product: 'cashew',
        quantity: 500,
        message: 'Testing the API'
    })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🛠️ Customization Guide

### 1. Change Company Information

**In `frontend/index.html`:**
```html
<!-- Change company name in navbar -->
<span class="logo-text">Your Company Name</span>

<!-- Change tagline in hero section -->
<p class="hero-tagline">Your Tagline Here 🌍</p>

<!-- Update contact details -->
<p><a href="tel:+919999999999">+91 9999 999 999</a></p>
<p><a href="mailto:info@company.com">info@company.com</a></p>

<!-- Update WhatsApp number -->
<a href="https://wa.me/919999999999?text=Your%20Message">
```

### 2. Change Color Theme

**In `frontend/css/style.css`:**
```css
:root {
    --primary-dark-green: #1b5e20;    /* Main color */
    --primary-green: #2e7d32;         /* Secondary color */
    --accent-gold: #d4af37;           /* Accent color */
    /* ... more colors ... */
}
```

### 3. Add More Products

**In `frontend/js/app.js`:**
```javascript
productsData: [
    {
        id: 1,
        name: 'Product Name',
        category: 'Category',
        description: 'Description',
        bgColor: '#color',
        emoji: '🎁',
        minOrder: '100 kg'
    }
    // Add more products here
]
```

### 4. Update Product Images

```html
<!-- Replace emoji with actual image -->
<div class="product-image" :style="{ backgroundImage: `url(images/${product.image})` }">
    <img :src="`images/${product.image}`" :alt="product.name">
</div>
```

### 5. Connect Real MongoDB

**In `backend/app.py`:**
```python
# Uncomment these lines:
from pymongo import MongoClient
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

# Replace in_memory_data with actual MongoDB queries
```

---

## 📊 MongoDB Integration

### Full MongoDB Setup (Advanced)

1. **Update Flask to use MongoDB:**

Replace the in-memory data section in `app.py` with:

```python
from pymongo import MongoClient

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

def get_products():
    return list(db.products.find())

def add_contact(contact_data):
    return db.contacts.insert_one(contact_data)
```

2. **Initialize Database Collections:**

```bash
# Connect to MongoDB shell
mongo

# Select database
use ashnex_agrotrade

# Create collections
db.createCollection("products")
db.createCollection("contacts")
db.createCollection("orders")

# Create indexes for performance
db.products.createIndex({ "category": 1 })
db.contacts.createIndex({ "email": 1 })
db.orders.createIndex({ "status": 1 })

# Insert sample products
db.products.insertMany([
    { name: "Premium Cashew", category: "Cashew", price: 450 },
    { name: "Organic Ginger", category: "Ginger", price: 80 }
])
```

---

## 🚀 Deployment Guide

### Deploy to Render (Recommended Free Option)

#### Backend Deployment (Flask on Render)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Create Render account**: https://render.com

3. **Create New Web Service**
   - Connect GitHub repository
   - Runtime: Python 3
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && gunicorn app:app`

4. **Add Environment Variables** in Render dashboard:
   ```
   MONGO_DB_URI=your_mongodb_atlas_uri
   ADMIN_API_KEY=your_secret_key
   ```

5. **Deploy** → Get URL like `https://ashnex-backend.onrender.com`

#### Frontend Deployment (Vue.js on Vercel/Netlify)

**Option A: Vercel (Recommended)**

1. Create Vercel account: https://vercel.com
2. Connect GitHub repository
3. Set root directory: `frontend`
4. Deploy

**Option B: Netlify**

1. Create Netlify account: https://netlify.com
2. Connect GitHub repository
3. Build command: (leave empty for static site)
4. Publish directory: `frontend`
5. Deploy

5. **Update API URL in Frontend**

   Change in `frontend/js/app.js`:
   ```javascript
   const response = await fetch('https://ashnex-backend.onrender.com/api/contact', {
   ```

---

### Deploy to Own Server (VPS)

**Using Ubuntu VPS:**

```bash
# 1. SSH into server
ssh root@your_server_ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install required packages
sudo apt install -y python3 python3-pip nginx mongodb git

# 4. Clone repository
cd /var/www
git clone your_repository

# 5. Install Python dependencies
cd ashnex/backend
pip install -r requirements.txt
pip install gunicorn

# 6. Setup systemd service for Flask
sudo nano /etc/systemd/system/ashnex.service
```

**Systemd service file:**
```ini
[Unit]
Description=Ashnex Agrotrade Flask App
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/ashnex/backend
ExecStart=/usr/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 7. Enable service
sudo systemctl enable ashnex
sudo systemctl start ashnex

# 8. Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/ashnex
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        root /var/www/ashnex/frontend;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

```bash
# 9. Enable nginx site
sudo ln -s /etc/nginx/sites-available/ashnex /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔐 Security Checklist

- [ ] Change `ADMIN_API_KEY` in `.env`
- [ ] Set `FLASK_DEBUG=False` in production
- [ ] Use HTTPS (SSL certificate)
- [ ] Setup rate limiting for APIs
- [ ] Validate all form inputs
- [ ] Use environment variables for secrets
- [ ] Implement CSRF protection
- [ ] Add authentication for admin panel
- [ ] Setup monitoring and logging
- [ ] Regular security audits

---

## 📱 Features Included

### Frontend
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Smooth animations and transitions
- ✅ Mobile hamburger menu
- ✅ Product filtering by category
- ✅ Contact form with validation
- ✅ WhatsApp integration
- ✅ Professional color scheme (dark green & gold)
- ✅ SEO-friendly HTML
- ✅ Accessibility features
- ✅ Fast loading performance

### Backend
- ✅ RESTful API endpoints
- ✅ Contact form handling
- ✅ Bulk order management
- ✅ Product CRUD operations
- ✅ Admin authentication
- ✅ Error handling
- ✅ CORS support
- ✅ Logging system
- ✅ MongoDB ready

---

## 🐛 Troubleshooting

### Issue: "Backend server is not running"
**Solution**: Make sure Flask is running on `http://localhost:5000`
```bash
cd backend
python app.py
```

### Issue: CORS Error (Cross-Origin Request Blocked)
**Solution**: CORS is already enabled, but ensure API URL is correct in `app.js`

### Issue: MongoDB Connection Error
**Solution**: 
- Check MongoDB is running: `mongosh`
- Verify connection string in `.env`
- Check firewall settings

### Issue: Form not submitting
**Solution**:
- Check browser console for errors
- Verify backend is running
- Check network tab in browser DevTools
- Ensure all form fields are filled

### Issue: Products not showing
**Solution**:
- Backend might not be initialized
- Check browser console for API errors
- Verify productData in app.js

---

## 📚 Useful Commands

```bash
# Backend
python app.py              # Start Flask server
pip install -r requirements.txt   # Install dependencies
python -m flask shell      # Flask interactive shell

# Frontend (in browser console)
// Check if Vue is loaded
console.log(Vue)

// Check products
app.config.globalProperties.$data.productsData

# MongoDB
mongosh              # Connect to MongoDB
use ashnex_agrotrade # Select database
db.products.find()   # List all products

# Deployment
gunicorn app:app     # Production server
```

---

## 📧 Support & Contact

For issues or questions:
- Email: info@ashnexagrotrade.com
- WhatsApp: +91 9999 999 999
- GitHub: [Your Repository]

---

## 📄 License

This project is proprietary and confidential for Ashnex Agrotrade.

---

## 🎯 Next Steps

1. ✅ Test all features locally
2. ✅ Customize company information
3. ✅ Add real product images
4. ✅ Connect MongoDB database
5. ✅ Setup admin panel for managing products
6. ✅ Add email notifications for new inquiries
7. ✅ Setup deployment to production
8. ✅ Configure SSL/HTTPS
9. ✅ Setup domain name
10. ✅ Launch website!

---

**Last Updated**: March 2024  
**Version**: 1.0.0
