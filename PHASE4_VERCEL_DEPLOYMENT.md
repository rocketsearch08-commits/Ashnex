# 🎨 PHASE 4: VERCEL FRONTEND DEPLOYMENT

**Deploy your frontend website in 20 minutes**

---

## ⏳ Prerequisites

✅ Backend deployed on Render (from Phase 3)
✅ Backend URL obtained (e.g., https://ashnex-backend.onrender.com)

---

## Step 1: Update Frontend API URL

**You MUST have your Render backend URL from Phase 3**

Update this file: `frontend/js/app.js`

Find line:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

Replace with your Render URL (example):
```javascript
const API_BASE_URL = 'https://ashnex-backend.onrender.com';
```

**Save the file**

---

## Step 2: Commit and Push to GitHub

Open terminal:

```bash
cd C:\Users\Suyash\OneDrive\Desktop\ashnex
git add frontend/js/app.js
git commit -m "Update API URL to Render backend"
git push
```

You should see:
```
Enumerating objects: 3, done.
...
1 file changed
```

---

## Step 3: Sign Up for Vercel

Open: **https://vercel.com**

Click **"Sign Up"**
Choose **"Continue with GitHub"**
Authorize Vercel
You'll see your dashboard

---

## Step 4: Create New Project

1. Click **"Add New..."** (top right)
2. Click **"Project"**
3. Under "Import Git Repository", find **"Ashnex"**
4. Click **"Import"**

---

## Step 5: Configure Project

**Project Name:**
```
ashnex
```

**Framework Preset:**
```
Other
```

**Root Directory:**
```
frontend
```

Leave everything else default

Click **"Deploy"**

⏳ **Wait 2-3 minutes** for deployment

---

## Step 6: Get Your Website URL

Once deployed, Vercel shows your URL:
```
https://ashnex.vercel.app
```

(Your actual URL might be slightly different)

✅ **Your website is LIVE!**

---

## 📝 IMPORTANT: Save Your URLs

```
Frontend: https://ashnex.vercel.app
Backend:  https://ashnex-backend.onrender.com
```

---

## ⏭️ What's Next?

**Proceed to Phase 5: TESTING**

Open PHASE5_TESTING_VERIFICATION.md

---

## 🎯 Current Status

```
✅ Phase 1: GitHub - DONE
✅ Phase 2: MongoDB - DONE  
✅ Phase 3: Render Backend - DONE
⏳ Phase 4: Vercel Frontend - YOU ARE HERE
❌ Phase 5: Testing - NEXT
```

---

**START NOW: Go to https://vercel.com and deploy! 🚀**

