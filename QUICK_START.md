# ASHNEX AGROTRADE - QUICK START GUIDE

**Get the website running in 5 minutes!**

## 🎯 What You'll Need

1. **Python 3.8+** installed
2. **A text editor** (VS Code recommended)
3. **A modern browser** (Chrome, Firefox, Edge, Safari)

## ⚡ Super Quick Start (2 Steps)

### Step 1: Start Backend (Flask)

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Mac/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

✅ You should see: `🚀 Server starting on 0.0.0.0:5000`

### Step 2: Start Frontend (Vue.js)

**In a new terminal:**

**Windows:**
```bash
cd frontend
python -m http.server 8000
```

**Mac/Linux:**
```bash
cd frontend
python3 -m http.server 8000
```

✅ Open browser: `http://localhost:8000`

---

## 🧪 Test It Works

### Test 1: Website Loads
- Open `http://localhost:8000`
- You should see the Ashnex Agrotrade homepage
- Try scrolling through sections
- Test hamburger menu on mobile view (resize browser)

### Test 2: Products Work
- Go to Products section
- Click "All", "Cashew", "Ginger", "Turmeric"
- Products should filter correctly

### Test 3: Contact Form Works
- Scroll to Contact section
- Fill in all fields
- Click "Send Message"
- You should see "Message sent successfully!"

### Test 4: Check Backend
- Open `http://localhost:5000/api/health`
- You should see:
```json
{
  "status": "ok",
  "message": "Ashnex Agrotrade Server is running"
}
```

---

## 🎨 Customization (10 minutes)

### Change Company Name
**File**: `frontend/index.html`
```html
<!-- Find this line around line 20 -->
<span class="logo-text">Ashnex Agrotrade</span>

<!-- Change to your company name -->
<span class="logo-text">Your Company Name</span>
```

### Change Tagline
**File**: `frontend/index.html`
```html
<!-- Find this line around line 40 -->
<p class="hero-tagline">Domestic & Global Supply 🌍</p>

<!-- Change to your tagline -->
<p class="hero-tagline">Your Tagline Here 🚀</p>
```

### Change Colors
**File**: `frontend/css/style.css`
```css
/* Find this section at the top (around line 10) */
:root {
    --primary-dark-green: #1b5e20;    /* Main green color */
    --accent-gold: #d4af37;           /* Gold accent */
    /* Change these HEX colors to yours */
}
```

### Change Contact Info
**File**: `frontend/index.html`
```html
<!-- Find Contact section and update these -->
<p><a href="tel:+919999999999">Your Phone</a></p>
<p><a href="mailto:your@email.com">Your Email</a></p>
<a href="https://wa.me/919999999999">WhatsApp Number</a>
```

---

## 📊 Test API Endpoints

**Open browser console** (`F12` → Console tab) and run these:

### Test 1: Get All Products
```javascript
fetch('http://localhost:5000/api/products')
  .then(r => r.json())
  .then(d => console.log(d))
```

### Test 2: Send Contact Message
```javascript
fetch('http://localhost:5000/api/contact', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Your Name',
    email: 'your@email.com',
    product: 'cashew',
    quantity: 500,
    message: 'I need bulk cashew'
  })
})
.then(r => r.json())
.then(d => console.log(d))
```

### Test 3: Create Bulk Order
```javascript
fetch('http://localhost:5000/api/bulk-order', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Company Name',
    email: 'company@email.com',
    product: 'ginger',
    quantity: 1000,
    message: 'Monthly supply needed'
  })
})
.then(r => r.json())
.then(d => console.log(d))
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Make sure Python 3.8+ is installed. Run `python --version` |
| "Port 5000 already in use" | Change `FLASK_PORT` in `.env` or kill process on port 5000 |
| Frontend won't load | Make sure you're in `frontend` folder. Run `python -m http.server 8000` |
| Form doesn't work | Check backend is running. Open `http://localhost:5000/api/health` |
| "Module not found" | Run `pip install -r requirements.txt` again |

---

## 📱 Responsive Testing

**Test Website on Different Screen Sizes:**

1. **Desktop** (1920x1080)
   - Press `F12` in browser
   - Check layout looks good

2. **Tablet** (768px)
   - Press `F12` → Click toggle device toolbar icon
   - Select "iPad"
   - Check layout adapts

3. **Mobile** (375px)
   - In device toolbar, select "iPhone"
   - Check hamburger menu works
   - Check buttons are clickable

---

## 🚀 Next: Deploy to Production

Once everything works:

1. **Create free MongoDB**: https://www.mongodb.com/cloud/atlas
2. **Deploy backend**: https://render.com (free)
3. **Deploy frontend**: https://vercel.com (free)
4. **Setup domain**: Use Namecheap or GoDaddy

See `README.md` for detailed deployment instructions.

---

## 💡 Tips

- Save files → browser auto-refreshes (Live Server extension)
- Use browser DevTools (`F12`) to debug
- Check browser console for JavaScript errors
- Check backend terminal for Python errors
- Clear browser cache if styles don't update (`Ctrl+Shift+Delete`)

---

## 📞 Need Help?

Check the full `README.md` for:
- Complete API documentation
- MongoDB setup guide
- Deployment instructions
- Security checklist
- Advanced customization

---

**Happy coding! 🎉**
