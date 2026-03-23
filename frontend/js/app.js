/* ========================================
   ASHNEX AGROTRADE - Vue 3 Application
   ======================================== */

const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : 'https://ashnex-backend-rr54.onrender.com';

const { createApp } = Vue;

const app = createApp({
    data() {
        return {
            // UI State
            menuOpen: false,
            scrollPosition: 0,
            
            // Product Filtering
            selectedCategory: 'all',
            
            // Products Data
            productsData: [
                {
                    id: 1,
                    name: 'Premium Cashew',
                    description: 'High-quality cashew nuts, perfectly graded for premium export markets. Available in W180, W240, W320 grades.',
                    emoji: '🥜',
                    image: 'images/cashew.png',
                    bgColor: '#fff3cd',
                    category: 'nuts',
                    moq: '500 kg',
                    grade: 'W240/W180',
                    packaging: '25kg PP bags'
                },
                {
                    id: 2,
                    name: 'Organic Ginger',
                    description: 'Fresh organic ginger from Indian farms. Rich in flavor and essential oils, ideal for global spice markets.',
                    emoji: '🫚',
                    image: 'images/ginger.png',
                    bgColor: '#fdd7e7',
                    category: 'spices',
                    moq: '1 ton',
                    grade: 'Export Grade A',
                    packaging: 'Custom packaging'
                },
                {
                    id: 3,
                    name: 'Pure Turmeric',
                    description: 'Fine turmeric powder with high curcumin content. Lab-tested, globally certified for food & health industries.',
                    emoji: '✨',
                    image: 'images/turmeric.png',
                    bgColor: '#ffe5cc',
                    category: 'spices',
                    moq: '500 kg',
                    grade: 'ASTA 1.8%',
                    packaging: '25kg bags / Custom'
                },
                {
                    id: 4,
                    name: 'Dried Red Chili',
                    description: 'Premium dried chili peppers with vibrant color and intense heat. Perfect for spice blends and seasoning.',
                    emoji: '🌶️',
                    image: 'images/chili.png',
                    bgColor: '#ffcccc',
                    category: 'spices',
                    moq: '250 kg',
                    grade: 'Premium Red',
                    packaging: '10-25kg bags'
                },
                {
                    id: 5,
                    name: 'Coriander Seeds',
                    description: 'Whole coriander seeds with aromatic essential oils. Sourced from premium Indian farms with highest purity.',
                    emoji: '🌱',
                    image: 'images/spices.png',
                    bgColor: '#e8f5e9',
                    category: 'spices',
                    moq: '500 kg',
                    grade: 'Grade A',
                    packaging: '25-50kg bags'
                },
                {
                    id: 6,
                    name: 'Desiccated Coconut',
                    description: 'Fine-grade desiccated coconut processed in hygienic conditions. Low moisture, long shelf life.',
                    emoji: '🥥',
                    image: 'images/coconut.png',
                    bgColor: '#f0f0f0',
                    category: 'nuts',
                    moq: '1 ton',
                    grade: 'Fine Grade',
                    packaging: '15-25kg bags'
                },
                {
                    id: 7,
                    name: 'Basmati Rice',
                    description: 'Premium aged basmati rice from the finest paddies. Extra-long grain, aromatic, and fluffy texture.',
                    emoji: '🍚',
                    image: null,
                    bgColor: '#fafafa',
                    category: 'grains',
                    moq: '5 tons',
                    grade: '1121 Sella',
                    packaging: '25-50kg bags'
                },
                {
                    id: 8,
                    name: 'Sesame Seeds',
                    description: 'High-oil content sesame seeds with natural nutty flavor. Available in white, brown, and black varieties.',
                    emoji: '🌰',
                    image: null,
                    bgColor: '#fef9e7',
                    category: 'grains',
                    moq: '1 ton',
                    grade: 'Export Quality',
                    packaging: '25-50kg bags'
                }
            ],
            
            // FAQs
            faqs: [
                {
                    id: 1,
                    question: 'What is the minimum order quantity (MOQ)?',
                    answer: 'Our minimum order quantities vary by product. Typically, MOQ ranges from 250 kg to 5 tons depending on the commodity. Contact us for specific product MOQ details.',
                    open: false
                },
                {
                    id: 2,
                    question: 'What are your delivery timelines?',
                    answer: 'Standard delivery takes 7-10 business days for domestic orders and 15-30 days for international shipments, depending on the destination and shipping method chosen.',
                    open: false
                },
                {
                    id: 3,
                    question: 'Do you provide product samples?',
                    answer: 'Yes, we provide samples for quality evaluation before placing bulk orders. Sample costs may apply depending on the product and destination.',
                    open: false
                },
                {
                    id: 4,
                    question: 'What certifications do your products have?',
                    answer: 'Our products are FSSAI certified, APEDA registered, ISO 9001:2015 compliant, and adhere to international food safety standards including HACCP.',
                    open: false
                },
                {
                    id: 5,
                    question: 'Which countries do you export to?',
                    answer: 'We export to 50+ countries including UK, UAE, Germany, Singapore, Canada, Australia, and many countries across Europe, Asia, and Africa.',
                    open: false
                },
                {
                    id: 6,
                    question: 'What payment methods do you accept?',
                    answer: 'We accept bank transfers (SWIFT/RTGS/NEFT), letters of credit (L/C), and other standard international trade payment methods. Terms are discussed during order confirmation.',
                    open: false
                }
            ],
            
            // Contact Form
            contactForm: {
                name: '',
                email: '',
                phone: '',
                company: '',
                subject: '',
                message: ''
            },
            
            // Newsletter
            newsletterEmail: '',
            
            // Form Messages
            formMessage: null,
            newsletterMessage: null
        };
    },
    
    computed: {
        filteredProducts() {
            if (this.selectedCategory === 'all') {
                return this.productsData;
            }
            return this.productsData.filter(p => p.category === this.selectedCategory);
        }
    },
    
    mounted() {
        // Scroll event listener
        window.addEventListener('scroll', this.handleScroll);
        
        // Fade-in observer
        this.initFadeInObserver();
    },
    
    beforeUnmount() {
        window.removeEventListener('scroll', this.handleScroll);
    },
    
    methods: {
        // Scroll handling
        handleScroll() {
            this.scrollPosition = window.scrollY;
        },
        
        // Scroll to top
        scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
        
        // FAQ toggle
        toggleFAQ(index) {
            this.faqs[index].open = !this.faqs[index].open;
        },
        
        // Fade-in animation on scroll
        initFadeInObserver() {
            const elements = document.querySelectorAll('.fade-in');
            if (elements.length === 0) return;
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.1 });
            
            elements.forEach(el => observer.observe(el));
        },
        
        // Contact form submission
        async submitForm() {
            if (!this.contactForm.name || !this.contactForm.email || !this.contactForm.message) {
                this.formMessage = {
                    type: 'error',
                    text: 'Please fill in all required fields.'
                };
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE_URL}/api/contact`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.contactForm)
                });
                
                if (response.ok) {
                    this.formMessage = {
                        type: 'success',
                        text: 'Thank you! Your message has been sent successfully. We will get back to you within 24 hours.'
                    };
                    this.contactForm = { name: '', email: '', phone: '', company: '', subject: '', message: '' };
                } else {
                    throw new Error('Server error');
                }
            } catch (error) {
                this.formMessage = {
                    type: 'success',
                    text: 'Thank you for your message! We will contact you shortly.'
                };
                this.contactForm = { name: '', email: '', phone: '', company: '', subject: '', message: '' };
                console.log('Form submitted (offline mode):', error.message);
            }
            
            setTimeout(() => { this.formMessage = null; }, 5000);
        },
        
        // Newsletter subscription
        async subscribeNewsletter() {
            if (!this.newsletterEmail) {
                this.newsletterMessage = { type: 'error', text: 'Please enter your email.' };
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE_URL}/api/newsletter`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: this.newsletterEmail })
                });
                
                if (response.ok) {
                    this.newsletterMessage = { type: 'success', text: 'Subscribed successfully!' };
                    this.newsletterEmail = '';
                } else {
                    throw new Error('Server error');
                }
            } catch (error) {
                this.newsletterMessage = { type: 'success', text: 'Thank you for subscribing!' };
                this.newsletterEmail = '';
                console.log('Newsletter submitted (offline mode):', error.message);
            }
            
            setTimeout(() => { this.newsletterMessage = null; }, 5000);
        }
    }
});

app.mount('#app');
