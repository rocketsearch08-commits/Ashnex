# 🚀 ASHNEX GITHUB DEPLOYMENT GUIDE

**Connect GitHub → Deploy to Render + Vercel + MongoDB Atlas (ALL FREE)**

---

## ✅ STEP 1: PUSH CODE TO GITHUB

Your GitHub repository is created. Now push your project code.

### 1.1 Open Terminal

```bash
# Navigate to project
cd C:\Users\Suyash\OneDrive\Desktop\ashnex
```

### 1.2 Initialize Git (if not already done)

```bash
# Check if git is initialized
git status

# If NOT initialized, run:
git init
```

### 1.3 Configure Git User (First time only)

```bash
git config user.name "Your Name"
git config user.email "your.email@github.com"
```

### 1.4 Add All Files

```bash
git add .
```

### 1.5 Commit

```bash
git commit -m "Initial commit - Ashnex Agrotrade full-stack website"
```

### 1.6 Add Remote Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/Ashnex.git
```

**Example:**
```bash
git remote add origin https://github.com/john-doe/Ashnex.git
```

### 1.7 Rename Branch to Main

```bash
git branch -M main
```

### 1.8 Push to GitHub

```bash
git push -u origin main
```

✅ **Your code is now on GitHub!**

---

---

## 📦 STEP 2: SETUP MONGODB ATLAS (Cloud Database)

### 2.1 Go to MongoDB Atlas

```
https://www.mongodb.com/cloud/atlas
```

### 2.2 Create Account

- Click "Try Free"
- Sign up with email or GitHub
- Verify email

### 2.3 Create Organization

- Click "Create Organization"
- Name: Your Organization
- Click "Create"

### 2.4 Create Project

- Click "New Project"
- Project name: Ashnex
- Click "Next"
- Click "Create Project"

### 2.5 Build Cluster

- Click "Build a Database"
- Choose "M0 Free" (Always FREE)
- Cloud Provider: AWS
- Region: N. Virginia (or closest)
- Cluster name: ashnex-cluster
- Click "Create"

⏳ **Wait 5-10 minutes for cluster creation...**

### 2.6 Create Database User

Once cluster is ready:

- Click "SECURITY" → "Database Access"
- Click "Add New Database User"
- Username: `ashnex_user`
- Password: Click "Auto-generate Secure Password"
  - **SAVE THIS PASSWORD** 📝
- Built-in Role: `Editor`
- Click "Add User"

### 2.7 Get Connection String

- Go back to "Clusters"
- Click "Connect" button
- Choose "Drivers"
- Copy the MongoDB URI:

```
mongodb+srv://ashnex_user:PASSWORD@cluster-name.mongodb.net/?retryWrites=true&w=majority
```

**Replace:**
- `ashnex_user` = your username
- `PASSWORD` = your generated password
- Keep everything else

**👉 SAVE THIS CONNECTION STRING** 📝

### 2.8 Add IP Whitelist

- Go to "SECURITY" → "Network Access"
- Click "Add IP Address"
- Click "Allow Access from Anywhere"
- Click "Confirm"

✅ **MongoDB Atlas is ready!**

---

---

## 🚀 STEP 3: DEPLOY BACKEND ON RENDER

### 3.1 Go to Render

```
https://render.com
```

### 3.2 Create Account

- Click "Sign up"
- Choose "GitHub"
- Authorize Render to access GitHub

### 3.3 Deploy Backend Service

1. Click "New +" → "Web Service"
2. Select your GitHub repository: **Ashnex**
3. Configure:

```
Name: ashnex-backend
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
Publish: Yes
```

4. Click "Create Web Service"

⏳ **Wait 3-5 minutes for deployment...**

### 3.4 Add Environment Variables

Once deployed:

1. In Render dashboard, click your service
2. Go to "Environment" tab
3. Click "Add Environment Variable"

Add these variables one by one:

```
FLASK_ENV=production
FLASK_DEBUG=False
MONGO_DB_URI=mongodb+srv://ashnex_user:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=ashnex_agrotrade
ADMIN_API_KEY=admin_key_change_in_production
FRONTEND_URL=https://ashnex.vercel.app
```

4. Click "Save Changes"

⏳ **Service will auto-redeploy (2-3 min)**

### 3.5 Get Backend URL

Your backend URL is:
```
https://ashnex-backend.onrender.com
```

(You'll see it on the service page)

### 3.6 Test Backend

Open in browser:
```
https://ashnex-backend.onrender.com/api/health
```

Should see:
```json
{"status": "ok", "message": "..."}
```

✅ **Backend is LIVE!**

---

---

## 🎨 STEP 4: UPDATE FRONTEND API URL

### 4.1 Edit frontend/js/app.js

Find this line (around line 1):
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

Replace with:
```javascript
const API_BASE_URL = 'https://ashnex-backend.onrender.com';
```

### 4.2 Update WhatsApp Number (Optional)

Find:
```javascript
openWhatsApp() {
    const message = encodeURIComponent('Hello Ashnex Agrotrade!...');
    window.open(`https://wa.me/919876543210?text=${message}`, '_blank');
}
```

Replace `919876543210` with your WhatsApp number with country code:
- Pakistan: +92
- India: +91
- Example: `+923334751234` (without +)

### 4.3 Commit and Push

```bash
git add frontend/js/app.js
git commit -m "Update backend API URL for Render"
git push
```

✅ **Frontend code updated!**

---

---

## 🎯 STEP 5: DEPLOY FRONTEND ON VERCEL

### 5.1 Go to Vercel

```
https://vercel.com
```

### 5.2 Create Account

- Click "Sign up"
- Choose "GitHub"
- Authorize Vercel

### 5.3 Import Project

1. Click "New Project"
2. Click "Import Git Repository"
3. Find and select: **Ashnex**
4. Click "Import"

### 5.4 Configure

```
Framework: Other (Vue.js)
Root Directory: frontend
Build Command: (leave empty)
Output Directory: (leave empty)
Environment Variables: (leave empty)
```

Click "Deploy"

⏳ **Wait 2-3 minutes for deployment...**

### 5.5 Get Frontend URL

Your website URL:
```
https://ashnex.vercel.app
```

(Or check dashboard for your specific URL)

### 5.6 Test Website

Open in browser:
```
https://ashnex.vercel.app
```

Should see:
- Header with logo
- Hero section
- Products
- About
- Contact form
- Footer

✅ **Frontend is LIVE!**

---

---

## 🧪 STEP 6: TEST END-TO-END

### 6.1 Test Website

1. Open https://ashnex.vercel.app
2. Browse all sections
3. Check responsive design (resize browser)
4. Try submitting contact form
5. Should see "Thank you!" message

### 6.2 Test API Endpoints

```bash
# Test health
curl https://ashnex-backend.onrender.com/api/health

# Test products
curl https://ashnex-backend.onrender.com/api/products

# Test contact form
curl -X POST https://ashnex-backend.onrender.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "product": "cashew",
    "quantity": "500",
    "message": "Test message"
  }'
```

### 6.3 Check MongoDB

1. Go to MongoDB Atlas
2. Click "Browse Collections"
3. Should see data if tests worked

✅ **Everything is working!**

---

---

## ✅ DEPLOYMENT COMPLETE!

### Your Live Website

```
🌐 Frontend:  https://ashnex.vercel.app
🔌 Backend:   https://ashnex-backend.onrender.com
💾 Database:  MongoDB Atlas (Cloud)
```

### Access Points

| Component | URL | Status |
|-----------|-----|--------|
| Website | https://ashnex.vercel.app | ✅ Live |
| API | https://ashnex-backend.onrender.com | ✅ Live |
| Database | MongoDB Atlas | ✅ Live |
| Repo | https://github.com/YOUR_USER/Ashnex | ✅ Synced |

---

---

## 🔗 NEXT STEPS

### Update Code in Future

Any changes you make:

```bash
# Make changes to code
# Test locally
git add .
git commit -m "Your message"
git push
```

Both Render and Vercel will auto-deploy (1-2 minutes)

### Optional: Add Custom Domain

Later, you can:
1. Buy domain (ashnex.com)
2. Connect to Vercel
3. Update Render custom domain

See: DEVOPS_DEPLOYMENT_GUIDE.md (Step 6) for details

### Monitor & Maintain

- **Render**: View logs in dashboard
- **Vercel**: Check deployments in dashboard
- **MongoDB**: Monitor collections in Atlas

---

---

## 🐛 TROUBLESHOOTING

### Issue: "Cannot reach API"

**Solution:**
1. Check Render backend is running
2. Verify API URL in frontend
3. Check CORS in backend

### Issue: "CORS Error"

**Error shows in browser console**

**Solution:**
Update backend/app.py, find CORS config and add Vercel URL:

```python
CORS(app, resources={r"/api/*": {
    "origins": ["https://ashnex.vercel.app"],
    "allow_headers": ["Content-Type"],
    "methods": ["GET", "POST", "PUT", "DELETE"]
}})
```

Commit and push, Render will redeploy

### Issue: "Database Connection Failed"

**Solution:**
1. Check MongoDB connection string
2. Verify username/password correct
3. Check IP whitelist in MongoDB Atlas

---

---

## 💰 COSTS

### Monthly Cost: $0 (Free Tier)

- Vercel: $0 (100GB bandwidth free)
- Render: $0 (backend sleeps after 15 min)
- MongoDB: $0 (512MB free tier)
- **Total: $0/month**

### When You Need More

Upgrade anytime:
- Vercel: $20/month for unlimited
- Render: $7/month for always-on
- MongoDB: $57/month for production tier

---

---

## 🎉 SUCCESS!

Your Ashnex Agrotrade website is now:

✅ Live on the internet
✅ Globally accessible
✅ Production-ready
✅ Fully functional
✅ Completely FREE

**Share your URL:** https://ashnex.vercel.app

---

## 📞 SUPPORT

**Problem?** Check: ADVANCED_CONFIG_TROUBLESHOOTING.md

**Need details?** Read: DEVOPS_DEPLOYMENT_GUIDE.md

**Quick answers?** See: QUICK_REFERENCE_CARD.md

---

**🌾 Ashnex Agrotrade is LIVE!** 🚀

**Your business is now accessible to the world!**
