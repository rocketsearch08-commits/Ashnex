# 🚀 ASHNEX AGROTRADE - COMPLETE FREE DEPLOYMENT GUIDE
## DevOps Expert Level - Production Ready

**Deploy your full-stack website for FREE using Vercel + Render + MongoDB Atlas**

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before starting, ensure you have:

- [x] GitHub account (free at github.com)
- [x] Vercel account (free at vercel.com)
- [x] Render account (free at render.com)
- [x] MongoDB Atlas account (free at mongodb.com)
- [x] Git installed locally
- [x] All source code ready
- [x] Tested locally (both servers running)

---

## 🎯 DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    INTERNET                             │
└────────────────┬──────────────────┬─────────────────────┘
                 │                  │
        ┌────────▼───────┐  ┌──────▼──────────┐
        │  VERCEL.APP    │  │    RENDER.COM   │
        │  (Frontend)    │  │    (Backend)    │
        │  Vue.js + HTML │  │  Flask API      │
        │                │  │  Python         │
        └────────┬───────┘  └──────┬──────────┘
                 │                 │
                 └────────┬────────┘
                          │
                   ┌──────▼──────────┐
                   │ MONGODB ATLAS   │
                   │ (Cloud Database)│
                   │ Free Tier       │
                   └─────────────────┘
```

---

## ⏱️ TIME ESTIMATE

- MongoDB Atlas Setup: 10 minutes
- Render Backend Deploy: 20 minutes
- Vercel Frontend Deploy: 15 minutes
- Configuration & Testing: 15 minutes
- **Total: ~60 minutes**

---

## 📁 FOLDER STRUCTURE (FOR DEPLOYMENT)

```
ashnex/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env               ← DO NOT commit to Git
│   ├── .env.example       ← Commit this
│   ├── models/
│   ├── routes/
│   └── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   │   └── app.js         ← Update API URL here
│   ├── images/
│   └── .env               ← DO NOT commit
│
├── .git/                  ← Git repository
├── .gitignore
└── README.md
```

---

---

# 🏗️ STEP 1: PREPARE LOCAL PROJECT FOR DEPLOYMENT

## 1.1 Initialize Git Repository

```bash
# Navigate to project root
cd C:\Users\Suyash\OneDrive\Desktop\ashnex

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Ashnex Agrotrade website"
```

## 1.2 Create .env Files

### Backend .env (DO NOT commit to Git)

Create `backend/.env`:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# MongoDB Atlas (you'll fill this after step 2)
MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/ashnex_agrotrade
MONGO_DB_NAME=ashnex_agrotrade

# Admin API Key (Change this!)
ADMIN_API_KEY=your_very_secure_random_key_here_change_in_production

# Frontend URL (update to your Vercel URL later)
FRONTEND_URL=http://localhost:8000
```

**Generate secure ADMIN_API_KEY:**
```bash
python -c "import secrets; print('ADMIN_API_KEY=' + secrets.token_hex(32))"
```

### Frontend .env (if needed)

Create `frontend/.env`:

```env
# Backend API URL (update after Render deployment)
VITE_API_URL=http://localhost:5000
```

## 1.3 Update .gitignore

Make sure `backend/.env` is ignored:

```
# .gitignore
backend/.env
frontend/.env
backend/venv/
node_modules/
.DS_Store
__pycache__/
*.pyc
.env.local
```

---

---

# 🌐 STEP 2: SETUP MONGODB ATLAS (Cloud Database)

## 2.1 Create MongoDB Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Try Free"
3. Sign up with email or GitHub
4. Verify email

## 2.2 Create First Project

1. Click "Create a Project"
2. Project name: `ashnex-agrotrade`
3. Click "Create Project"

## 2.3 Create First Cluster

1. Click "Create a Deployment"
2. Choose "M0 Free" tier
3. Cloud Provider: AWS (default)
4. Region: Select closest to you (or N. Virginia)
5. Cluster name: `ashnex-cluster`
6. Click "Create"

⏳ Wait 5-10 minutes for cluster to be created

## 2.4 Create Database User

1. Go to "Database Access" (left menu)
2. Click "Add New Database User"
3. Username: `ashnex_user`
4. Password: Click "Auto-generate secure password" (save this!)
5. Built-in Role: `Editor`
6. Click "Add User"

## 2.5 Get Connection String

1. Go back to "Databases" (left menu)
2. Click "Connect" on your cluster
3. Choose "Drivers"
4. **Copy the connection string**

It will look like:
```
mongodb+srv://ashnex_user:PASSWORD@cluster-name.mongodb.net/?retryWrites=true&w=majority
```

**Replace**:
- `ashnex_user` → your username
- `PASSWORD` → your password (use the one generated)
- Keep everything else the same

## 2.6 Add Access

1. In MongoDB Atlas, go to "Network Access"
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere"
4. Confirm

---

---

# 🚀 STEP 3: DEPLOY BACKEND ON RENDER (Flask API)

## 3.1 Push Code to GitHub

```bash
# Create GitHub repository
# Go to github.com → Click "+" → New repository
# Repository name: ashnex
# Description: Ashnex Agrotrade - Full Stack Website
# Public or Private (your choice)
# Create repository

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/ashnex.git

# Rename branch to main
git branch -M main

# Push code
git push -u origin main
```

## 3.2 Create Render Account

1. Go to https://render.com
2. Click "Sign up"
3. Choose "GitHub" (easiest)
4. Authorize GitHub access
5. Done!

## 3.3 Create Backend WebService on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:

```
Name: ashnex-backend
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
Branch: main
Root Directory: (leave empty)
```

4. Click "Create Web Service"

## 3.4 Add Environment Variables (Render)

1. In Render dashboard for your service, go to "Environment"
2. Add these variables:

```
FLASK_ENV=production
FLASK_DEBUG=False
MONGO_DB_URI={Your connection string from Step 2.5}
MONGO_DB_NAME=ashnex_agrotrade
ADMIN_API_KEY=your_secure_key_from_earlier
FRONTEND_URL=http://localhost:8000
```

3. Click "Save"
4. Service will redeploy automatically

⏳ Wait 3-5 minutes for deployment

## 3.5 Test Backend

1. Get your Render URL:
   - In Render dashboard, you'll see a URL like:
   - `https://ashnex-backend.onrender.com`

2. Test in browser:
   - `https://ashnex-backend.onrender.com/api/health`
   - Should return: `{"status": "ok", "message": "..."}`

✅ **Backend is live!** Save this URL: `https://ashnex-backend.onrender.com`

---

---

# 🎨 STEP 4: DEPLOY FRONTEND ON VERCEL (Vue.js)

## 4.1 Update API URL

Before deploying, update your frontend to use the Render backend URL.

### Update frontend/js/app.js

Find this line (around line 200):
```javascript
const response = await fetch('http://localhost:5000/api/contact', {
```

Replace with:
```javascript
const response = await fetch('https://ashnex-backend.onrender.com/api/contact', {
```

**Also update all other API calls:**
- `/api/products` → `https://ashnex-backend.onrender.com/api/products`
- `/api/bulk-order` → `https://ashnex-backend.onrender.com/api/bulk-order`

Commit and push:
```bash
git add frontend/js/app.js
git commit -m "Update API URL to production backend"
git push
```

## 4.2 Deploy to Vercel

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Select: GitHub
5. Find and select the `ashnex` repository
6. Configure:

```
Framework: Other (since it's Vue.js HTML)
Root Directory: frontend
Build Command: (leave empty)
Output Directory: (leave empty)
Source: Use default
```

7. Click "Deploy"

⏳ Wait 2-3 minutes

8. You'll get a URL like: `https://ashnex.vercel.app`

✅ **Frontend is live!** Your website URL: `https://ashnex.vercel.app`

## 4.3 Test Frontend

1. Open `https://ashnex.vercel.app`
2. You should see your Ashnex website
3. Test the contact form
4. You should see success message (backend API working)

---

---

# ✅ STEP 5: ENABLE CORS (Fix Backend)

If you see CORS errors in browser console, we need to fix it.

### Update backend/app.py

Find this line (around line 20):
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Replace with:
```python
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://ashnex.vercel.app",  # Add your Vercel frontend URL
        "http://localhost:8000",       # For local testing
        "http://localhost:3000"        # For local dev
    ],
    "allow_headers": ["Content-Type"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}})
```

Commit and push:
```bash
git add backend/app.py
git commit -m "Fix CORS for production deployment"
git push
```

Render will auto-redeploy (wait 2 minutes).

---

---

# 🌐 STEP 6: SETUP CUSTOM DOMAIN (Optional)

## 6.1 Buy Domain

1. Go to https://www.namecheap.com (cheapest) or https://www.godaddy.com
2. Search for `ashnex.com` (or your domain)
3. Add to cart and buy
4. Cost: $1-15/year

## 6.2 Connect Domain to Vercel (Frontend)

1. In Vercel dashboard, go to your project settings
2. Go to "Domains" tab
3. Enter your domain: `ashnex.com`
4. Add domain
5. Vercel will show you DNS records to add
6. Go to your domain registrar (Namecheap)
   - Go to "Advanced DNS"
   - Add Vercel's DNS records
7. Wait 24-48 hours for DNS propagation

Once confirmed:
- `https://ashnex.com` → Frontend (Vercel)

## 6.3 Connect Domain to Render (Backend - Optional)

You can use a subdomain like `api.ashnex.com`:

1. In Render dashboard, go to service settings
2. Go to "Custom Domains"
3. Add: `api.ashnex.com`
4. Add DNS records to your registrar
5. Wait for verification

Then update frontend API URL from:
```javascript
'https://ashnex-backend.onrender.com/api/contact'
```

To:
```javascript
'https://api.ashnex.com/api/contact'
```

---

---

# 🔐 STEP 7: SECURE PRODUCTION SETUP

## 7.1 Update API Key

Generate a strong API key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Update in Render environment variables:
```
ADMIN_API_KEY={Your new strong key}
```

## 7.2 Enable HTTPS

✅ Vercel: Automatic (always HTTPS)
✅ Render: Automatic (always HTTPS)
✅ MongoDB: Automatic (always HTTPS)

## 7.3 Set Flask Debug to False

Already done in .env, but verify:

```env
FLASK_DEBUG=False
FLASK_ENV=production
```

## 7.4 Add Security Headers (Optional)

Update `backend/app.py`:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

---

# 📊 STEP 8: MONGODB SETUP (DETAILED)

## 8.1 Create Collections

1. In MongoDB Atlas, go to "Databases"
2. Click "Browse Collections"
3. Click "Create Database"
4. Database name: `ashnex_agrotrade`
5. Collection name: `products`
6. Create

Repeat for collections:
- `contacts`
- `orders`
- `logs` (optional)

## 8.2 Insert Sample Data

```javascript
// Open MongoDB shell in Atlas

// Insert products
db.products.insertMany([
  {
    id: 1,
    name: "Premium Cashew",
    category: "Cashew",
    description: "High-quality cashew nuts",
    price: 450,
    unit: "kg",
    minOrder: "500 kg"
  },
  {
    id: 2,
    name: "Organic Ginger",
    category: "Ginger",
    description: "Fresh ginger powder",
    price: 80,
    unit: "kg",
    minOrder: "1 ton"
  }
])

// Verify
db.products.find()
```

## 8.3 Create Indexes

```javascript
// Improve performance
db.products.createIndex({ "category": 1 })
db.contacts.createIndex({ "email": 1, "createdAt": -1 })
db.orders.createIndex({ "status": 1, "createdAt": -1 })
```

---

---

# ✨ STEP 9: PRODUCTION OPTIMIZATION

## 9.1 Add SEO Meta Tags

Update `frontend/index.html`:

```html
<head>
    <!-- SEO Meta Tags -->
    <meta name="description" content="Ashnex Agrotrade - Premium Indian Agricultural Products | Domestic & Global Supply 🌍">
    <meta name="keywords" content="cashew, ginger, turmeric, agricultural products, export, import, bulk supply">
    <meta name="author" content="Ashnex Agrotrade">
    
    <!-- Open Graph (Social Media) -->
    <meta property="og:title" content="Ashnex Agrotrade - Premium Agri Products">
    <meta property="og:description" content="Domestic & Global Supply 🌍">
    <meta property="og:image" content="https://ashnex.com/og-image.jpg">
    <meta property="og:url" content="https://ashnex.com">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Ashnex Agrotrade">
    <meta name="twitter:description" content="Premium Indian Agricultural Products">
    
    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Ashnex Agrotrade",
      "url": "https://ashnex.com",
      "description": "Premium Indian agricultural products supplier"
    }
    </script>
    
    <!-- Robots & Sitemap -->
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://ashnex.com">
</head>
```

## 9.2 Create sitemap.xml

Create `frontend/sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ashnex.com</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://ashnex.com#/about</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://ashnex.com#/products</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://ashnex.com#/contact</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
```

## 9.3 Add robots.txt

Create `frontend/robots.txt`:

```
User-agent: *
Allow: /
Disallow: /admin
Disallow: /api

Sitemap: https://ashnex.com/sitemap.xml
```

## 9.4 Enable Compression

In `backend/app.py`, add:

```python
from flask_compress import Compress

Compress(app)
```

Add to `backend/requirements.txt`:
```
Flask-Compress==1.13
```

## 9.5 Add Rate Limiting

In `backend/app.py`, add:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/contact', methods=['POST'])
@limiter.limit("5 per minute")
def add_contact():
    # ... existing code
```

Add to `backend/requirements.txt`:
```
Flask-Limiter==3.5.0
```

---

---

# 🧪 STEP 10: TESTING CHECKLIST

## Frontend Testing
- [ ] Website loads on https://ashnex.vercel.app
- [ ] All pages accessible (Home, About, Products, Services, Contact)
- [ ] Products filter works
- [ ] Contact form submits without errors
- [ ] Success message displays
- [ ] Mobile responsive (resize browser)
- [ ] Hamburger menu works
- [ ] Links work

## Backend Testing
- [ ] Health check works: https://ashnex-backend.onrender.com/api/health
- [ ] Get products: https://ashnex-backend.onrender.com/api/products
- [ ] Contact form receives data
- [ ] Error handling works
- [ ] Admin endpoints protected

## Integration Testing
- [ ] Frontend can reach backend API
- [ ] Contact form data saves in MongoDB
- [ ] No CORS errors in console
- [ ] Network requests show 200 OK

## Performance Testing
- [ ] Website loads < 3 seconds
- [ ] API responses < 1 second
- [ ] Images optimized

## Security Testing
- [ ] HTTPS everywhere
- [ ] No sensitive data in frontend
- [ ] API key not exposed
- [ ] Database connection secure

---

---

# 📞 TEST API ENDPOINTS

### Test Health (No Auth)
```bash
curl https://ashnex-backend.onrender.com/api/health
```

### Test Get Products (No Auth)
```bash
curl https://ashnex-backend.onrender.com/api/products
```

### Test Get Products by Category
```bash
curl "https://ashnex-backend.onrender.com/api/products?category=Cashew"
```

### Test Submit Contact (No Auth)
```bash
curl -X POST https://ashnex-backend.onrender.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "product": "cashew",
    "quantity": "500",
    "message": "Testing the API"
  }'
```

### Test Admin Endpoint (With Auth)
```bash
curl https://ashnex-backend.onrender.com/api/admin/dashboard \
  -H "Authorization: Bearer YOUR_ADMIN_KEY"
```

---

---

# 🐛 TROUBLESHOOTING

## Issue: "Cannot reach backend from frontend"
**Solution**: 
- Check CORS configuration in backend
- Verify Vercel URL in CORS allowed origins
- Check Render backend is running

## Issue: "CORS error in console"
**Error**: `Access to XMLHttpRequest blocked by CORS policy`
**Solution**:
```python
# In backend/app.py, add your Vercel URL
CORS(app, resources={r"/api/*": {
    "origins": ["https://ashnex.vercel.app"]
}})
```

## Issue: "MongoDB connection failed"
**Solution**:
- Verify connection string in Render environment
- Check MongoDB Atlas IP whitelist (should be "Allow from anywhere")
- Check username and password are correct

## Issue: "Form submission fails silently"
**Solution**:
- Check browser console (F12 → Console tab)
- Verify backend URL in frontend/js/app.js
- Check Render backend is running

## Issue: "Render backend always starting/restarting"
**Solution**:
- Check app.py syntax errors
- Verify requirements.txt has all dependencies
- Check environment variables are set
- Review Render logs for errors

## Issue: "Vercel deployment fails"
**Solution**:
- Check your GitHub repository is pushing correctly
- Verify .gitignore doesn't exclude important files
- Check frontend folder structure

---

---

# 📋 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] Code tested locally (both servers running)
- [ ] Git initialized and pushed to GitHub
- [ ] MongoDB Atlas account created
- [ ] Vercel account created
- [ ] Render account created
- [ ] API URL updated in frontend

### MongoDB Setup
- [ ] Cluster created
- [ ] Database user created
- [ ] Connection string copied
- [ ] IP whitelisting enabled
- [ ] Collections created

### Render Backend
- [ ] GitHub connected
- [ ] Environment variables added
- [ ] MONGO_DB_URI set
- [ ] ADMIN_API_KEY set
- [ ] CORS configured
- [ ] Health endpoint tested

### Vercel Frontend
- [ ] GitHub repository connected
- [ ] Frontend folder specified
- [ ] API URL updated to Render
- [ ] Website deployed
- [ ] Contact form tested

### Post-Deployment
- [ ] Frontend accessible at https://ashnex.vercel.app
- [ ] Backend accessible at https://ashnex-backend.onrender.com
- [ ] Contact form works end-to-end
- [ ] API endpoints tested
- [ ] Error handling verified
- [ ] Performance acceptable
- [ ] HTTPS everywhere

### Optimization
- [ ] SEO meta tags added
- [ ] sitemap.xml created
- [ ] robots.txt created
- [ ] Compression enabled
- [ ] Rate limiting added
- [ ] Security headers set

### Custom Domain (Optional)
- [ ] Domain purchased
- [ ] DNS records added to Namecheap/GoDaddy
- [ ] Domain connected to Vercel
- [ ] Domain connected to Render (optional)
- [ ] DNS propagation verified

---

---

# 🎯 DEPLOYMENT SUMMARY

## Your Live URLs

| Component | URL |
|-----------|-----|
| **Frontend** | https://ashnex.vercel.app |
| **Backend API** | https://ashnex-backend.onrender.com |
| **Custom Domain** | https://ashnex.com (after step 6) |
| **Database** | MongoDB Atlas (cloud) |

## Free Services Used
- ✅ Vercel (Frontend) - Free
- ✅ Render (Backend) - Free
- ✅ MongoDB Atlas (Database) - Free tier
- ✅ GitHub (Code hosting) - Free

## Monthly Costs
- **Frontend (Vercel)**: $0
- **Backend (Render)**: $0-7 (free tier sleeps after 15 min)
- **Database (MongoDB)**: $0
- **Domain (Optional)**: $1-15/year
- **Total**: $0/month (or $7 if you need backend always-on)

---

---

# 🚀 DEPLOYMENT COMPLETE!

## What You Did

✅ Deployed frontend on Vercel (FREE)
✅ Deployed backend on Render (FREE)
✅ Setup MongoDB database (FREE)
✅ Connected everything together
✅ Made website production-ready
✅ Added security & SEO

## Website is NOW LIVE!

**Access here**: https://ashnex.vercel.app

---

---

# ⚡ QUICK REFERENCE COMMANDS

### Update Code After Deployment

```bash
# Make changes to code

# Commit and push
git add .
git commit -m "Your changes"
git push

# Vercel auto-deploys (wait 1-2 min)
# Render auto-deploys (wait 2-3 min)
```

### View Render Backend Logs

```bash
# In Render dashboard, click your service
# Click "Logs" tab to see real-time logs
```

### Update Backend Environment Variables

```bash
# In Render dashboard
# Click your service → Environment
# Edit variables → Save
# Service auto-redeploys
```

### Monitor MongoDB

```bash
# In MongoDB Atlas
# Go to Databases → Collections → View Data
# See all inquiries and orders
```

---

---

# 📚 ADDITIONAL RESOURCES

- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [MongoDB Atlas Docs](https://docs.mongodb.com/manual/)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Vue.js Production Guide](https://vuejs.org/guide/best-practices/performance.html)

---

**🌾 Ashnex Agrotrade is LIVE on the internet!** 🎉

Your free, production-ready website is now accessible globally.

Celebrate, share, and start growing your business! 🚀
