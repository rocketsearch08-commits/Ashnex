/* ========================================
   ASHNEX AGROTRADE - MAIN VUE.JS APPLICATION
   Frontend Logic using Vue 3
   ======================================== */

const { createApp } = Vue;

// ===== API CONFIGURATION =====
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'
    : 'https://ashnex-backend-rr54.onrender.com';

// ===== MAIN APPLICATION =====
const app = createApp({
    data() {
        return {
            // UI State
            menuOpen: false,

            // Products
            selectedCategory: 'All',
            categories: ['All', 'Cashew', 'Ginger', 'Turmeric', 'Other'],
            
            // Sample Products Data (from MongoDB in production)
            productsData: [
                {
                    id: 1,
                    name: 'Premium Cashew',
                    category: 'Cashew',
                    description: 'High-quality cashew nuts, perfectly roasted and graded for premium export',
                    bgColor: '#fff3cd',
                    emoji: '🥜',
                    minOrder: '500 kg',
                    grade: 'W240/W180',
                    packaging: '20kg/25kg bags'
                },
                {
                    id: 2,
                    name: 'Organic Ginger',
                    category: 'Ginger',
                    description: 'Fresh, organic ginger from Indian farms, ideal for spice markets worldwide',
                    bgColor: '#fdd7e7',
                    emoji: '🌱',
                    minOrder: '1 ton',
                    grade: 'Export Grade A',
                    packaging: 'Bulk cartons, 100kg bags'
                },
                {
                    id: 3,
                    name: 'Pure Turmeric Powder',
                    category: 'Turmeric',
                    description: 'Fine turmeric powder with high curcumin content, globally certified',
                    bgColor: '#ffe5cc',
                    emoji: '✨',
                    minOrder: '500 kg',
                    grade: 'ASTA Grade 1.8%',
                    packaging: '25kg/50kg bags'
                },
                {
                    id: 4,
                    name: 'Dried Chili',
                    category: 'Other',
                    description: 'Premium dried chili peppers, perfect for spice blends and seasoning',
                    bgColor: '#ffcccc',
                    emoji: '🌶️',
                    minOrder: '250 kg',
                    grade: 'Premium Red',
                    packaging: '20kg boxes'
                },
                {
                    id: 5,
                    name: 'Coriander Seeds',
                    category: 'Other',
                    description: 'Aromatic coriander seeds, essential for Indian and international cuisines',
                    bgColor: '#d1f2eb',
                    emoji: '⭐',
                    minOrder: '300 kg',
                    grade: 'Export Grade',
                    packaging: '25kg/50kg bags'
                },
                {
                    id: 6,
                    name: 'Cashew Kernels',
                    category: 'Cashew',
                    description: 'Premium cashew kernels, W180 and W240 grades available',
                    bgColor: '#fff3cd',
                    emoji: '🎁',
                    minOrder: '1 ton',
                    grade: 'W180/W240/W210',
                    packaging: '10kg/25kg/50kg'
                },
                {
                    id: 7,
                    name: 'Fenugreek Seeds',
                    category: 'Other',
                    description: 'High-quality fenugreek seeds for pharmaceutical and food industries',
                    bgColor: '#e8f5e9',
                    emoji: '🌾',
                    minOrder: '200 kg',
                    grade: 'Premium Grade',
                    packaging: '20kg/25kg bags'
                },
                {
                    id: 8,
                    name: 'Coconut Products',
                    category: 'Other',
                    description: 'Coconut oil, copra, and desiccated coconut for global markets',
                    bgColor: '#f0f4c3',
                    emoji: '🥥',
                    minOrder: '500 kg',
                    grade: 'Food Grade',
                    packaging: '30kg/50kg buckets'
                }
            ],

            // Featured Products (first 3)
            featuredProducts: [],

            // FAQ Data
            faqs: [
                {
                    id: 1,
                    question: 'What are your minimum order quantities?',
                    answer: 'Minimum order quantities vary by product, typically ranging from 250kg to 1 ton. We also offer flexible arrangements for larger bulk orders. Please contact our sales team for specific product requirements.',
                    open: false
                },
                {
                    id: 2,
                    question: 'Which countries do you export to?',
                    answer: 'We export to 50+ countries across 6 continents including UK, UAE, Europe, Asia Pacific, North America, and Australia. We handle all customs clearance, documentation, and logistics arrangements.',
                    open: false
                },
                {
                    id: 3,
                    question: 'What certifications do you have?',
                    answer: 'We are FSSAI certified, APEDA registered, ISO 9001:2015 compliant, and have HACCP certification. All products meet international food safety standards and are regularly audited by third-party laboratories.',
                    open: false
                },
                {
                    id: 4,
                    question: 'What is your typical delivery timeline?',
                    answer: 'Average delivery time is 7-10 days with 99.9% on-time delivery guarantee. We provide real-time shipment tracking and handle all logistics through trusted international carriers.',
                    open: false
                },
                {
                    id: 5,
                    question: 'Do you offer customized packaging?',
                    answer: 'Yes! We offer custom packaging solutions to meet your specific requirements including branded packaging, bulk containers, and food-grade materials. Our packaging team works closely with you to ensure your needs are met.',
                    open: false
                },
                {
                    id: 6,
                    question: 'How do I request a quote?',
                    answer: 'You can request a quote using our contact form, sending an email to info@ashnexagrotrade.com, or calling us at +91 9999 999 999. Our sales team will respond within 24 hours with a detailed quotation.',
                    open: false
                }
            ],

            // Contact Form
            form: {
                name: '',
                email: '',
                product: '',
                quantity: '',
                message: ''
            },

            // Newsletter
            newsletterEmail: '',

            // Form submission state
            isSubmitting: false,
            submitMessage: '',
            submitMessageType: '' // 'success' or 'error'
        };
    },

    computed: {
        // Filter products based on selected category
        filteredProducts() {
            if (this.selectedCategory === 'All') {
                return this.productsData;
            }
            return this.productsData.filter(product => product.category === this.selectedCategory);
        }
    },

    methods: {
        /**
         * Initialize featured products
         */
        initFeaturedProducts() {
            this.featuredProducts = this.productsData.slice(0, 3);
        },

        /**
         * Smooth scroll to section
         * @param {string} sectionId - ID of the section to scroll to
         */
        scrollTo(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        },

        /**
         * Submit contact form
         * In production, this would send data to Flask backend
         */
        async submitForm() {
            // Validate form
            if (!this.form.name || !this.form.email || !this.form.product || !this.form.quantity || !this.form.message) {
                this.submitMessage = 'Please fill in all fields';
                this.submitMessageType = 'error';
                return;
            }

            // Validate email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.form.email)) {
                this.submitMessage = 'Please enter a valid email address';
                this.submitMessageType = 'error';
                return;
            }

            this.isSubmitting = true;
            this.submitMessage = '';

            try {
                // ===== API ENDPOINT =====
                // In production, replace 'http://localhost:5000' with your Flask backend URL
                const response = await fetch('http://localhost:5000/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: this.form.name,
                        email: this.form.email,
                        product: this.form.product,
                        quantity: this.form.quantity,
                        message: this.form.message
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Success: Clear form and show success message
                    this.submitMessage = 'Message sent successfully! We will contact you soon.';
                    this.submitMessageType = 'success';
                    
                    // Reset form
                    this.form = {
                        name: '',
                        email: '',
                        product: '',
                        quantity: '',
                        message: ''
                    };

                    // Clear message after 5 seconds
                    setTimeout(() => {
                        this.submitMessage = '';
                    }, 5000);
                } else {
                    // Error response from server
                    this.submitMessage = data.message || 'Failed to send message. Please try again.';
                    this.submitMessageType = 'error';
                }
            } catch (error) {
                // Network error or parsing error
                console.error('Form submission error:', error);
                
                // For development: Show a helpful message
                if (error.message.includes('Failed to fetch')) {
                    this.submitMessage = 'Backend server is not running. Please start Flask backend on http://localhost:5000';
                } else {
                    this.submitMessage = 'Error sending message. Please check your connection and try again.';
                }
                this.submitMessageType = 'error';
            } finally {
                this.isSubmitting = false;
            }
        },

        /**
         * Close mobile menu when clicking outside
         */
        handleClickOutside(event) {
            const navbar = document.querySelector('.nav-container');
            if (navbar && !navbar.contains(event.target) && this.menuOpen) {
                this.menuOpen = false;
            }
        },

        /**
         * Subscribe to newsletter
         */
        async subscribeNewsletter() {
            // Validate email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(this.newsletterEmail)) {
                this.submitMessage = 'Please enter a valid email address';
                this.submitMessageType = 'error';
                return;
            }

            this.isSubmitting = true;

            try {
                const response = await fetch(`${API_BASE_URL}/api/newsletter`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: this.newsletterEmail
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    this.submitMessage = '✅ Subscribed successfully! Check your email for exclusive offers.';
                    this.submitMessageType = 'success';
                    this.newsletterEmail = '';

                    setTimeout(() => {
                        this.submitMessage = '';
                    }, 5000);
                } else {
                    this.submitMessage = data.message || 'Subscription failed. Please try again.';
                    this.submitMessageType = 'error';
                }
            } catch (error) {
                console.error('Newsletter subscription error:', error);
                this.submitMessage = 'Error subscribing. Please try again later.';
                this.submitMessageType = 'error';
            } finally {
                this.isSubmitting = false;
            }
        },

        /**
         * Toggle FAQ item open/closed
         */
        toggleFAQ(index) {
            this.faqs[index].open = !this.faqs[index].open;
        }
    },

    mounted() {
        // Initialize featured products
        this.initFeaturedProducts();

        // Add click outside listener for menu
        document.addEventListener('click', this.handleClickOutside);

        console.log('✅ Ashnex Agrotrade - Frontend Initialized');
        console.log('📱 Total Products:', this.productsData.length);
        console.log('🌐 Backend API: http://localhost:5000');
    },

    beforeUnmount() {
        // Cleanup event listener
        document.removeEventListener('click', this.handleClickOutside);
    }
});

// Mount the Vue app to the #app element
app.mount('#app');

// ===== DEVELOPMENT HELPERS =====
// Uncomment these in development to test the app

// window.debugApp = {
//     // Test form submission locally (without backend)
//     testForm: function() {
//         const testData = {
//             name: 'John Doe',
//             email: 'john@example.com',
//             product: 'cashew',
//             quantity: 500,
//             message: 'Testing the form submission'
//         };
//         console.log('📨 Test data ready:', testData);
//         // Manually set form and submit
//         app.config.globalProperties.$options.methods.submitForm.call(app);
//     },
//     
//     // Check product data
//     checkProducts: function() {
//         console.log('🛍️ Available Products:', app.config.globalProperties.$data.productsData);
//     }
// };

