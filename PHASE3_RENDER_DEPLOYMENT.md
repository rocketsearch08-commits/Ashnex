# 🚀 PHASE 3: RENDER BACKEND DEPLOYMENT

**Your backend will be deployed in 20 minutes**

---

## Step 1: Go to Render

Open: **https://render.com**

Click "Get Started"

---

## Step 2: Sign Up with GitHub

1. Click **"Sign up with GitHub"**
2. Authorize Render to access your GitHub account
3. You'll see your dashboard

---

## Step 3: Create Web Service

1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Under "GitHub", find **"Ashnex"** and select it
4. Click **"Connect"**

---

## Step 4: Configure Service

Fill in these exact values:

**Service Name:**
```
ashnex-backend
```

**Environment:**
```
Python 3
```

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
```

Leave other options as default. Click **"Create Web Service"**

⏳ **Wait 3-5 minutes** for deployment

---

## Step 5: Add Environment Variables

Once deployed, in your Render dashboard:

1. Click your **"ashnex-backend"** service
2. Go to the **"Environment"** tab
3. Add these 6 variables (click "Add Environment Variable" each time):

### Variable 1: FLASK_ENV
```
Name: FLASK_ENV
Value: production
```
Click Add

### Variable 2: FLASK_DEBUG
```
Name: FLASK_DEBUG
Value: False
```
Click Add

### Variable 3: MONGO_DB_URI ⭐ IMPORTANT
```
Name: MONGO_DB_URI
Value: mongodb+srv://rocketsearch08_db_user:ZcoRobFDFAnwsyns@ashnex.spbojur.mongodb.net/?appName=Ashnex
```
Click Add

### Variable 4: MONGO_DB_NAME
```
Name: MONGO_DB_NAME
Value: ashnex_agrotrade
```
Click Add

### Variable 5: ADMIN_API_KEY
```
Name: ADMIN_API_KEY
Value: admin_key_change_in_production
```
Click Add

### Variable 6: FRONTEND_URL
```
Name: FRONTEND_URL
Value: https://ashnex.vercel.app
```
Click Add

4. Scroll down and click **"Save Changes"**

⏳ **Service auto-redeploys** (2-3 minutes)

---

## Step 6: Test Backend

Once redeployed, open this in your browser:
```
https://ashnex-backend.onrender.com/api/health
```

You should see:
```json
{"status": "ok"}
```

✅ **Backend is LIVE!**

---

## 📝 IMPORTANT: Save Your Backend URL

Your backend URL is:
```
https://ashnex-backend.onrender.com
```

**⚠️ You'll need this URL in the next step to update the frontend**

---

## ⏭️ What's Next?

Once Step 6 works (API responds with JSON), **STOP and tell me:**
- ✅ Backend deployed successfully
- Your backend URL: https://ashnex-backend.onrender.com

Then I'll:
1. Update frontend API URL
2. Deploy to Vercel
3. Test everything

---

## 🆘 If Something Goes Wrong

Check **Render Logs**:
1. In Render dashboard, click your service
2. Click **"Logs"** tab
3. Look for error messages
4. Common issues in ADVANCED_CONFIG_TROUBLESHOOTING.md

---

## 🎯 Current Status

```
✅ Phase 1: GitHub - DONE
✅ Phase 2: MongoDB - DONE  
⏳ Phase 3: Render Backend - YOU ARE HERE
❌ Phase 4: Vercel Frontend - WAITING
❌ Phase 5: Testing - WAITING
```

---

**START NOW: Go to https://render.com and sign up! 🚀**

