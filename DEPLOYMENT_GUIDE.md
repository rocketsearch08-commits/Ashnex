# ASHNEX AGROTRADE - DEPLOYMENT GUIDE

**Production Deployment Instructions**

---

## 🌐 Deployment Options Overview

| Platform | Backend | Frontend | Cost | Ease |
|----------|---------|----------|------|------|
| **Render** | ✅ Free | Need separate | Free | Easy |
| **Vercel** | ❌ | ✅ Free | Free | Very Easy |
| **Netlify** | ❌ | ✅ Free | Free | Very Easy |
| **Heroku** | ✅ Paid | Need separate | $7+/month | Easy |
| **AWS** | ✅ | ✅ | Free tier | Medium |
| **DigitalOcean** | ✅ | ✅ | $5+/month | Medium |
| **Custom VPS** | ✅ | ✅ | $5+/month | Hard |

**Recommended for Beginners**: Render (Backend) + Vercel (Frontend)

---

## 🚀 OPTION 1: Deploy to Render (Free) + Vercel (Free)

### Backend Deployment to Render

#### Step 1: Prepare Repository

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit - Ashnex Agrotrade"

# Create GitHub repository
# Go to github.com and create new repo
# Then push code:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ashnex.git
git push -u origin main
```

#### Step 2: Create Render Account

1. Visit https://render.com
2. Sign up with GitHub account
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Configure:
   - **Name**: ashnex-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Root Directory**: . (current)

#### Step 3: Add Environment Variables

In Render dashboard:
1. Go to Environment
2. Add these variables:
   ```
   MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   MONGO_DB_NAME=ashnex_agrotrade
   ADMIN_API_KEY=your_strong_secret_key_here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. Click Deploy

⏳ Wait 2-3 minutes for deployment

✅ **Backend URL**: `https://ashnex-backend.onrender.com` (or your custom URL)

**Note**: Render free tier sleeps after 15 minutes of inactivity. To deploy paid version ($7/month) for 24/7 uptime.

---

### Frontend Deployment to Vercel

#### Step 1: Update API URL

**File**: `frontend/js/app.js`

Change this line:
```javascript
const response = await fetch('http://localhost:5000/api/contact', {
```

To this:
```javascript
const response = await fetch('https://ashnex-backend.onrender.com/api/contact', {
```

(Replace with your actual Render backend URL)

#### Step 2: Push Updated Code

```bash
git add frontend/js/app.js
git commit -m "Update API URL for production"
git push
```

#### Step 3: Deploy to Vercel

1. Visit https://vercel.com
2. Sign up with GitHub
3. Click "Add New..." → "Project"
4. Select your GitHub repository
5. Configure:
   - **Framework**: Other (since it's Vue.js with HTML)
   - **Root Directory**: frontend
   - **Build Command**: (leave empty)
   - **Output Directory**: . (current)

6. Click "Deploy"

⏳ Wait 1-2 minutes

✅ **Frontend URL**: `https://your-project.vercel.app`

---

## 💾 OPTION 2: Deploy MongoDB Database

### MongoDB Atlas (Cloud - Recommended)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create new cluster (free tier)
4. Get connection string:
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string
   
5. Update in Render environment:
```
MONGO_DB_URI=mongodb+srv://username:password@cluster-name.mongodb.net/ashnex_agrotrade?retryWrites=true&w=majority
```

---

## 🔒 Security Best Practices

### Before Going Live

- [ ] Change `ADMIN_API_KEY` to strong random string
  ```bash
  # Generate strong key
  python -c "import secrets; print(secrets.token_hex(16))"
  ```

- [ ] Enable HTTPS (Vercel/Render do this automatically)

- [ ] Set `FLASK_DEBUG=False` in production

- [ ] Add CORS validation to Flask:
  ```python
  CORS(app, resources={r"/api/*": {
      "origins": ["https://your-domain.vercel.app"]
  }})
  ```

- [ ] Setup rate limiting
- [ ] Add logging and monitoring
- [ ] Backup database regularly

---

## 📊 Setup Custom Domain

### Domain Registration

1. Buy domain from:
   - Namecheap: https://www.namecheap.com
   - GoDaddy: https://www.godaddy.com
   - Google Domains: https://domains.google

### Connect Domain to Vercel (Frontend)

1. In Vercel Dashboard → Settings → Domains
2. Enter your domain
3. Add DNS records shown by Vercel
4. Wait 24-48 hours for DNS propagation

### Connect Domain to Render (Backend)

1. Use subdomain like `api.yourdomain.com`
2. In Render → Settings → Custom Domain
3. Add DNS records
4. Wait for verification

### Final Setup

Update frontend API URL to:
```javascript
fetch('https://api.yourdomain.com/api/contact', {
```

---

## 📈 OPTION 3: Advanced - DigitalOcean App Platform

If you want everything on one platform:

### Create App on DigitalOcean

1. Go to https://www.digitalocean.com
2. Create account ($5-10/month)
3. Create App
4. Connect GitHub repo
5. Create two services:
   - **Web Service** (Frontend)
     - Source: frontend folder
     - Build: None
     - Run: `python -m http.server 8000`
   
   - **Web Service** (Backend)
     - Source: backend folder
     - Build: `pip install -r requirements.txt`
     - Run: `gunicorn app:app`

6. Add environment variables
7. Deploy

---

## 🖥️ OPTION 4: Virtual Private Server (Advanced)

### Deploy on Ubuntu VPS

#### Step 1: Setup Server

```bash
# SSH into server
ssh root@your_server_ip

# Update system
apt update && apt upgrade -y

# Install requirements
apt install -y python3 python3-pip python3-venv
apt install -y nodejs npm
apt install -y mongodb-org
apt install -y nginx
apt install -y git
```

#### Step 2: Clone Repository

```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/ashnex.git
cd ashnex
```

#### Step 3: Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### Step 4: Create Systemd Service

```bash
sudo nano /etc/systemd/system/ashnex.service
```

Paste this:
```ini
[Unit]
Description=Ashnex Agrotrade Flask App
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/ashnex/backend
Environment="PATH=/var/www/ashnex/backend/venv/bin"
ExecStart=/var/www/ashnex/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ashnex
sudo systemctl start ashnex
sudo systemctl status ashnex
```

#### Step 5: Setup Nginx

```bash
sudo nano /etc/nginx/sites-available/ashnex
```

Paste this:
```nginx
upstream ashnex_api {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /var/www/ashnex/frontend;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://ashnex_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ashnex /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 6: Setup SSL (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (free)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

#### Step 7: Setup MongoDB

```bash
# Start MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

---

## 📱 Mobile-Friendly Checklist

- [ ] Test on iPhone/Android
- [ ] Test touch interactions
- [ ] Verify responsive design
- [ ] Test contact form on mobile
- [ ] Test WhatsApp button
- [ ] Check font sizes are readable
- [ ] Verify button sizes (~44px minimum)

---

## 🧪 Post-Deployment Testing

### Test Checklist

1. **Website Load**
   - [ ] Open website in browsers
   - [ ] Check all pages load
   - [ ] Check images load

2. **Functionality**
   - [ ] Test contact form
   - [ ] Test product filtering
   - [ ] Test WhatsApp button
   - [ ] Test mobile menu

3. **Backend APIs**
   - [ ] Test `/api/health`
   - [ ] Test `/api/products`
   - [ ] Test contact submission
   - [ ] Test admin endpoints (with API key)

4. **Performance**
   - [ ] Check page load time (< 3 seconds)
   - [ ] Check server response time (< 1 second)
   - [ ] Check images are optimized

5. **SEO**
   - [ ] Check meta tags
   - [ ] Check sitemap.xml
   - [ ] Submit to Google Search Console

---

## 📊 Monitoring & Maintenance

### Set Up Monitoring

```bash
# Monitor logs on Render
# In Render dashboard: Logs tab

# Monitor backend (SSH into server)
tail -f /var/log/ashnex.log
```

### Regular Backups

```bash
# Backup MongoDB daily
mongodump --uri="mongodb+srv://..." --out=/backups/$(date +%Y%m%d)

# Backup to cloud storage (AWS S3, Google Cloud, etc.)
```

### Update Process

```bash
# Update code
cd /var/www/ashnex
git pull origin main

# Restart services
sudo systemctl restart ashnex
sudo systemctl restart nginx
```

---

## 🚨 Troubleshooting Deployments

| Issue | Solution |
|-------|----------|
| Backend returns 404 | Check API route paths, restart backend |
| Form doesn't work | Verify API URL in app.js, check CORS settings |
| Database connection error | Check MONGO_DB_URI in environment variables |
| Slow website | Optimize images, enable caching, add CDN |
| SSL certificate error | Renew certificate with certbot |
| Out of memory | Upgrade server plan, optimize code |

---

## 📞 Support Services

For 24/7 management:
- **Heroku**: Official support
- **AWS**: Premium support available
- **DigitalOcean**: Community + documentation
- **Render**: Email support

---

## 💰 Estimated Monthly Costs

### Option 1: Render + Vercel (Free Tier)
- Backend: **$0 - $7** (free tier sleeps)
- Frontend: **$0**
- Database: **$0 - 57** (MongoDB Atlas)
- **Total: $0 - $64/month**

### Option 2: DigitalOcean All-in-One
- Server: **$5 - 12/month**
- Database: Included
- **Total: $5 - 15/month**

### Option 3: AWS
- Server: **$0 - 10** (free tier)
- Database: **$0 - 20** (free tier)
- **Total: $0 - 30/month**

---

**Ready to go live? Start with Render + Vercel for easiest setup!** 🚀
