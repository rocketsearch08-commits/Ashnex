# 🎨 FRONTEND: PRODUCTION-READY SETUP

Complete production optimization guide for your Vue.js frontend.

---

## 📋 TABLE OF CONTENTS

1. Frontend Optimization
2. Environment Configuration
3. API Integration
4. SEO Optimization
5. Performance Optimization
6. Security Best Practices
7. Frontend Deployment

---

---

## 1️⃣ FRONTEND OPTIMIZATION

### Update frontend/js/app.js

Key changes for production:

```javascript
// Production API Configuration
const API_BASE_URL = 'https://ashnex-backend.onrender.com'; // Update to your Render URL

// Vue App
const { createApp } = Vue;

const app = createApp({
    data() {
        return {
            // Products
            productsData: [
                {
                    id: 1,
                    name: 'Premium Cashew',
                    category: 'Cashew',
                    description: 'High-quality cashew nuts from India',
                    price: 450,
                    unit: 'kg',
                    minOrder: '500 kg'
                },
                {
                    id: 2,
                    name: 'Organic Ginger',
                    category: 'Ginger',
                    description: 'Fresh ginger powder with natural oils',
                    price: 80,
                    unit: 'kg',
                    minOrder: '1 ton'
                },
                {
                    id: 3,
                    name: 'Pure Turmeric',
                    category: 'Turmeric',
                    description: 'High-curcumin turmeric powder',
                    price: 120,
                    unit: 'kg',
                    minOrder: '500 kg'
                }
            ],
            
            // Form Data
            contactForm: {
                name: '',
                email: '',
                product: '',
                quantity: '',
                message: ''
            },
            
            // UI State
            isMobileMenuOpen: false,
            loading: false,
            successMessage: '',
            errorMessage: '',
            selectedCategory: 'All'
        };
    },

    computed: {
        filteredProducts() {
            if (this.selectedCategory === 'All') {
                return this.productsData;
            }
            return this.productsData.filter(p => p.category === this.selectedCategory);
        },

        categories() {
            const cats = ['All', ...new Set(this.productsData.map(p => p.category))];
            return cats;
        }
    },

    methods: {
        async submitContactForm() {
            // Validation
            if (!this.validateForm()) return;

            this.loading = true;

            try {
                const response = await fetch(`${API_BASE_URL}/api/contact`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.contactForm)
                });

                const data = await response.json();

                if (response.ok) {
                    this.successMessage = 'Thank you! We will contact you soon. 🎉';
                    this.resetForm();
                    setTimeout(() => this.successMessage = '', 5000);
                } else {
                    this.errorMessage = data.message || 'Failed to submit form';
                    setTimeout(() => this.errorMessage = '', 5000);
                }
            } catch (error) {
                console.error('API Error:', error);
                this.errorMessage = 'Network error. Please check your connection.';
                setTimeout(() => this.errorMessage = '', 5000);
            } finally {
                this.loading = false;
            }
        },

        validateForm() {
            const { name, email, product, quantity, message } = this.contactForm;

            if (!name.trim()) {
                this.errorMessage = 'Please enter your name';
                return false;
            }

            if (!email.includes('@')) {
                this.errorMessage = 'Please enter a valid email';
                return false;
            }

            if (!product.trim()) {
                this.errorMessage = 'Please select a product';
                return false;
            }

            if (!quantity.trim()) {
                this.errorMessage = 'Please enter quantity';
                return false;
            }

            if (!message.trim()) {
                this.errorMessage = 'Please enter your message';
                return false;
            }

            return true;
        },

        resetForm() {
            this.contactForm = {
                name: '',
                email: '',
                product: '',
                quantity: '',
                message: ''
            };
        },

        toggleMobileMenu() {
            this.isMobileMenuOpen = !this.isMobileMenuOpen;
        },

        closeMobileMenu() {
            this.isMobileMenuOpen = false;
        },

        scrollTo(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
                this.closeMobileMenu();
            }
        },

        openWhatsApp() {
            const message = encodeURIComponent('Hello Ashnex Agrotrade! I am interested in your products.');
            window.open(`https://wa.me/919876543210?text=${message}`, '_blank');
        },

        async loadProducts() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/products`);
                if (response.ok) {
                    const data = await response.json();
                    this.productsData = data.data;
                }
            } catch (error) {
                console.error('Failed to load products:', error);
            }
        }
    },

    mounted() {
        // Close mobile menu on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar')) {
                this.closeMobileMenu();
            }
        });

        // Load products from backend
        this.loadProducts();

        // Log initialization
        console.log('Ashnex Agrotrade - Production Frontend Loaded');
        console.log(`API URL: ${API_BASE_URL}`);
    }
});

app.mount('#app');
```

---

---

## 2️⃣ ENVIRONMENT CONFIGURATION

### frontend/.env (if using build tool)

```env
VITE_API_URL=https://ashnex-backend.onrender.com
VITE_APP_NAME=Ashnex Agrotrade
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=production
```

---

---

## 3️⃣ API INTEGRATION

### Update API Calls in frontend/js/app.js

**Update WhatsApp Number:**
```javascript
openWhatsApp() {
    const message = encodeURIComponent('Hello Ashnex Agrotrade! I am interested in your products.');
    window.open(`https://wa.me/92334XX5210?text=${message}`, '_blank');
    // Replace 92334XX5210 with your actual WhatsApp number with country code
}
```

**Update Backend URL:**
```javascript
// At the top of app.js
const API_BASE_URL = 'https://ashnex-backend.onrender.com';

// Or for custom domain:
const API_BASE_URL = 'https://api.ashnex.com';
```

---

---

## 4️⃣ SEO OPTIMIZATION

### Update frontend/index.html with SEO Meta Tags

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Basic Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>Ashnex Agrotrade | Premium Indian Agricultural Products | Cashew, Ginger, Turmeric</title>
    <meta name="description" content="Ashnex Agrotrade - Premium Indian agricultural products supplier. Domestic and global supply of cashew, ginger, turmeric, and more. Bulk orders available.">
    <meta name="keywords" content="cashew, ginger, turmeric, agricultural products, export, import, bulk supply, Indian products, agro trade, spices">
    <meta name="author" content="Ashnex Agrotrade">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://ashnex.com">
    
    <!-- Open Graph (Social Media) -->
    <meta property="og:title" content="Ashnex Agrotrade | Premium Indian Agricultural Products">
    <meta property="og:description" content="High-quality cashew, ginger, turmeric. Bulk orders welcome. Domestic & Global Supply.">
    <meta property="og:url" content="https://ashnex.com">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://ashnex.com/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Ashnex Agrotrade">
    <meta name="twitter:description" content="Premium Indian agricultural products supplier">
    <meta name="twitter:image" content="https://ashnex.com/og-image.jpg">
    
    <!-- Language -->
    <meta http-equiv="content-language" content="en">
    
    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Ashnex Agrotrade",
      "url": "https://ashnex.com",
      "logo": "https://ashnex.com/logo.png",
      "description": "Premium Indian agricultural products supplier",
      "sameAs": [
        "https://www.facebook.com/ashnexagrotrade",
        "https://www.linkedin.com/company/ashnexagrotrade"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "Customer Service",
        "telephone": "+92-334-XXXXX",
        "email": "info@ashnex.com"
      }
    }
    </script>
    
    <!-- Additional JSON-LD for LocalBusiness -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Ashnex Agrotrade",
      "image": "https://ashnex.com/logo.png",
      "description": "Premium agricultural products",
      "address": {
        "@type": "PostalAddress",
        "addressCountry": "PK"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "Sales",
        "telephone": "+92-334-XXXXX"
      }
    }
    </script>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
    
    <!-- Preload Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Main CSS -->
    <link rel="stylesheet" href="css/style.css">
    
    <!-- Performance: DNS Prefetch -->
    <link rel="dns-prefetch" href="https://ashnex-backend.onrender.com">
    
    <!-- Performance: Preconnect to API -->
    <link rel="preconnect" href="https://ashnex-backend.onrender.com">
</head>
<body>
    <!-- Your existing HTML content here -->
</body>
</html>
```

### Create frontend/sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  
  <url>
    <loc>https://ashnex.com</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  
  <url>
    <loc>https://ashnex.com#products</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  
  <url>
    <loc>https://ashnex.com#about</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://ashnex.com#services</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://ashnex.com#contact</loc>
    <lastmod>2024-03-23</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Create frontend/robots.txt

```
# Robots.txt - Search Engine Crawling Instructions

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /*.json
Disallow: /hidden/

# Allow specific search engines for indexing
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Crawl delay to avoid overwhelming server
Crawl-delay: 1

# Sitemap location
Sitemap: https://ashnex.com/sitemap.xml
```

---

---

## 5️⃣ PERFORMANCE OPTIMIZATION

### Lazy Loading Images

```html
<!-- In your HTML, use lazy loading -->
<img src="products/cashew.jpg" alt="Premium Cashew" loading="lazy">
```

### Image Optimization Tips

```bash
# 1. Compress images before uploading
# Use tools like TinyPNG or ImageOptim

# 2. Use WebP format (more efficient)
# Image format: JPG/PNG → WebP

# 3. Responsive images
<img srcset="cashew-small.jpg 400w, cashew-medium.jpg 800w, cashew-large.jpg 1200w"
     sizes="(max-width: 600px) 100vw, 50vw"
     src="cashew.jpg"
     alt="Cashew">
```

### CSS Performance

```css
/* Remove unused CSS */
/* Minify CSS in production */
/* Use CSS variables for consistency */

:root {
    --color-primary: #1b5e20;
    --color-accent: #d4af37;
    --transition-speed: 0.3s;
}
```

### JavaScript Performance

```javascript
// 1. Debounce form submissions
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// 2. Lazy load comments/reviews
// Load on scroll or user interaction

// 3. Use requestAnimationFrame for animations
window.requestAnimationFrame(() => {
    // Smooth animations
});
```

---

---

## 6️⃣ SECURITY BEST PRACTICES

### Content Security Policy

```html
<!-- Add to frontend/index.html head -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' cdn.jsdelivr.net cdnjs.cloudflare.com unpkg.com;
               style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com;
               img-src 'self' data: https:;
               font-src 'self' fonts.gstatic.com cdnjs.cloudflare.com;
               connect-src 'self' https://ashnex-backend.onrender.com;
               frame-ancestors 'none';">
```

### Security Headers (set by backend)

```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### API Security

```javascript
// 1. Always use HTTPS
const API_BASE_URL = 'https://ashnex-backend.onrender.com';

// 2. Never expose sensitive data
// ❌ const API_KEY = 'secret_key_123';
// ✅ Get from backend environment

// 3. Validate all inputs
function sanitizeInput(input) {
    return input.replace(/[<>]/g, '');
}

// 4. Use Content-Type header
headers: {
    'Content-Type': 'application/json'
}
```

---

---

## 7️⃣ FRONTEND DEPLOYMENT

### Deploy to Vercel

```bash
# Step 1: Install Vercel CLI (optional)
npm i -g vercel

# Step 2: Login to Vercel
vercel login

# Step 3: Deploy
vercel

# Step 4: Follow prompts
# - Link to existing project? No
# - Project name: ashnex
# - Deploy source: ./frontend (if in root folder)
```

### Deploy to Netlify

```bash
# Step 1: Install Netlify CLI
npm install -g netlify-cli

# Step 2: Login
netlify login

# Step 3: Deploy
netlify deploy --prod --dir=frontend

# Or drag and drop frontend folder on Netlify dashboard
```

---

---

## 🎯 PRODUCTION CHECKLIST

### Before Deployment
- [ ] Update API_BASE_URL to Render backend
- [ ] Update WhatsApp number
- [ ] Add all SEO meta tags
- [ ] Create sitemap.xml
- [ ] Create robots.txt
- [ ] Add JSON-LD structured data
- [ ] Test contact form with backend
- [ ] Test all links work
- [ ] Test responsive design on mobile
- [ ] Test performance (< 3s load time)

### After Deployment
- [ ] Website accessible at Vercel URL
- [ ] All CSS loads correctly
- [ ] Images display without issues
- [ ] Contact form works
- [ ] No console errors
- [ ] Mobile menu works
- [ ] Forms submit successfully
- [ ] API calls reach backend

---

---

## 📊 PERFORMANCE METRICS TO TRACK

```javascript
// Check Google PageSpeed Insights
// https://pagespeed.web.dev/

// Metrics:
// - First Contentful Paint (FCP): < 1.8s
// - Largest Contentful Paint (LCP): < 2.5s
// - Cumulative Layout Shift (CLS): < 0.1
// - Time to Interactive (TTI): < 3.8s
```

---

---

## 🚀 DEPLOYMENT SUMMARY

✅ SEO optimized
✅ Production-ready
✅ Performance optimized
✅ Security hardened
✅ Mobile responsive
✅ API integrated
✅ Ready to deploy

**Your Vercel URL**: https://ashnex.vercel.app
