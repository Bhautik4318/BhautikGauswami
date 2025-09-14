"use strict";
// TypeScript Main Application File
// Handles particles animation, smooth scrolling, contact form, and UI interactions
class PortfolioApp {
    constructor() {
        this.currentTheme = 'dark';
        this.navMenu = document.getElementById('nav-menu');
        this.hamburger = document.getElementById('mobile-menu');
        this.contactForm = document.getElementById('contact-form');
        this.formMessage = document.getElementById('form-message');
        this.themeToggle = document.getElementById('theme-toggle');
        this.init();
    }
    init() {
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupEventListeners();
                this.initializeParticles();
                this.setupScrollAnimations();
            });
        }
        else {
            this.setupEventListeners();
            this.initializeParticles();
            this.setupScrollAnimations();
        }
    }
    setupEventListeners() {
        // Mobile menu toggle
        if (this.hamburger && this.navMenu) {
            this.hamburger.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }
        // Theme toggle
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
        // Navigation links smooth scroll
        this.setupSmoothScrolling();
        // Contact form submission
        if (this.contactForm) {
            this.contactForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleContactForm();
            });
        }
        // Navbar background on scroll
        window.addEventListener('scroll', () => {
            this.handleNavbarScroll();
        });
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (this.navMenu && this.hamburger &&
                !this.navMenu.contains(e.target) &&
                !this.hamburger.contains(e.target)) {
                this.closeMobileMenu();
            }
        });
        // Load saved theme
        this.loadTheme();
        // Window resize handler for particles
        window.addEventListener('resize', () => {
            setTimeout(() => {
                this.initializeParticles();
            }, 100);
        });
        // Content change observer for dynamic particles resizing
        const resizeObserver = new ResizeObserver(() => {
            setTimeout(() => {
                this.initializeParticles();
            }, 100);
        });
        resizeObserver.observe(document.body);
    }
    toggleMobileMenu() {
        if (this.navMenu && this.hamburger) {
            this.navMenu.classList.toggle('active');
            this.hamburger.classList.toggle('active');
        }
    }
    closeMobileMenu() {
        if (this.navMenu && this.hamburger) {
            this.navMenu.classList.remove('active');
            this.hamburger.classList.remove('active');
        }
    }
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        // Update theme button icon
        if (this.themeToggle) {
            const icon = this.themeToggle.querySelector('i');
            if (icon) {
                icon.className = this.currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
        // Save theme preference
        localStorage.setItem('theme', this.currentTheme);
        // Reinitialize particles with new theme
        this.initializeParticles();
    }
    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        this.currentTheme = savedTheme;
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        // Update theme button icon
        if (this.themeToggle) {
            const icon = this.themeToggle.querySelector('i');
            if (icon) {
                icon.className = this.currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }
    setupSmoothScrolling() {
        const navLinks = document.querySelectorAll('.nav-link, .scroll-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                if (href && href.startsWith('#')) {
                    const targetId = href.substring(1);
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        const offsetTop = targetElement.offsetTop - 70; // Account for fixed navbar
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                        // Close mobile menu after clicking link
                        this.closeMobileMenu();
                    }
                }
            });
        });
    }
    handleNavbarScroll() {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(0, 0, 0, 0.98)';
            }
            else {
                navbar.style.background = 'rgba(0, 0, 0, 0.95)';
            }
        }
    }
    async handleContactForm() {
        if (!this.contactForm || !this.formMessage)
            return;
        const formData = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            subject: document.getElementById('subject').value.trim(),
            message: document.getElementById('message').value.trim()
        };
        // Basic validation
        if (!this.validateForm(formData)) {
            this.showFormMessage('Please fill in all fields correctly.', 'error');
            return;
        }
        // Show loading state
        const submitBtn = this.contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
        try {
            const response = await this.submitContactForm(formData);
            if (response.status === 'success') {
                this.showFormMessage(response.message, 'success');
                this.contactForm.reset();
            }
            else {
                this.showFormMessage(response.message, 'error');
            }
        }
        catch (error) {
            console.error('Contact form error:', error);
            this.showFormMessage('An error occurred. Please try again later.', 'error');
        }
        finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }
    validateForm(data) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        // More lenient validation - message only needs to be longer than 3 characters
        return data.name.length > 0 &&
            emailRegex.test(data.email) &&
            data.subject.length > 0 &&
            data.message.length > 3;
    }
    async submitContactForm(data) {
        const csrfToken = this.getCSRFToken();
        const response = await fetch('/contact/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }
    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
    showFormMessage(message, type) {
        if (!this.formMessage)
            return;
        this.formMessage.textContent = message;
        this.formMessage.className = `form-message ${type}`;
        this.formMessage.style.display = 'block';
        // Hide message after 5 seconds
        setTimeout(() => {
            if (this.formMessage) {
                this.formMessage.style.display = 'none';
            }
        }, 5000);
    }
    initializeParticles() {
        // Set particles container to cover entire document
        const particlesContainer = document.getElementById('particles-js');
        if (particlesContainer) {
            // Make sure particles cover the entire document height
            const documentHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);
            particlesContainer.style.height = documentHeight + 'px';
            particlesContainer.parentElement.style.height = documentHeight + 'px';
        }
        // Get current theme colors
        const isDark = this.currentTheme === 'dark';
        const particleColor = isDark ? '#ffffff' : '#000000';
        // Initialize particles.js with enhanced configuration for better visibility
        if (typeof particlesJS !== 'undefined') {
            particlesJS('particles-js', {
                particles: {
                    number: {
                        value: 150, // Reduced from 200 to 150
                        density: {
                            enable: true,
                            value_area: 800 // Reduced area for more density
                        }
                    },
                    color: {
                        value: particleColor
                    },
                    shape: {
                        type: 'circle',
                        stroke: {
                            width: 0,
                            color: particleColor
                        }
                    },
                    opacity: {
                        value: 0.6, // Increased from 0.3 to 0.6 for better visibility
                        random: true,
                        anim: {
                            enable: true,
                            speed: 1.5, // Slightly faster animation
                            opacity_min: 0.2, // Increased minimum opacity
                            sync: false
                        }
                    },
                    size: {
                        value: 3, // Increased from 2 to 3
                        random: true,
                        anim: {
                            enable: true,
                            speed: 2,
                            size_min: 0.5, // Increased minimum size
                            sync: false
                        }
                    },
                    line_linked: {
                        enable: true,
                        distance: 150, // Increased connection distance
                        color: particleColor,
                        opacity: 0.4, // Increased line opacity for better visibility
                        width: 1.5 // Increased line width
                    },
                    move: {
                        enable: true,
                        speed: 5, // Optimal speed for smooth visible movement
                        direction: 'none',
                        random: true,
                        straight: false,
                        out_mode: 'bounce', // Particles bounce off edges
                        bounce: true,
                        attract: {
                            enable: false,
                            rotateX: 600,
                            rotateY: 1200
                        }
                    }
                },
                interactivity: {
                    detect_on: 'canvas',
                    events: {
                        onhover: {
                            enable: false // Disabled hover interactions
                        },
                        onclick: {
                            enable: true, // Enable click interactions
                            mode: 'push' // Add particles on click
                        },
                        resize: true
                    },
                    modes: {
                        push: {
                            particles_nb: 8 // Increased from 4 to 8 particles on click
                        }
                    }
                },
                retina_detect: true
            });
        }
    }
    setupScrollAnimations() {
        // Intersection Observer for reveal animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, observerOptions);
        // Add reveal class to elements and observe them
        const revealElements = document.querySelectorAll('.skill-category, .project-card, .certificate-card, .timeline-item');
        revealElements.forEach(el => {
            el.classList.add('reveal');
            observer.observe(el);
        });
        // Navbar active link highlighting
        this.setupActiveNavigation();
    }
    setupActiveNavigation() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        const observerOptions = {
            threshold: 0.3,
            rootMargin: '-70px 0px -70px 0px'
        };
        const navObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.id;
                    // Remove active class from all nav links
                    navLinks.forEach(link => {
                        link.classList.remove('active');
                    });
                    // Add active class to current section's nav link
                    const activeLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
                    if (activeLink) {
                        activeLink.classList.add('active');
                    }
                }
            });
        }, observerOptions);
        sections.forEach(section => {
            navObserver.observe(section);
        });
    }
    // Public methods for external access
    scrollToSection(sectionId) {
        const element = document.getElementById(sectionId);
        if (element) {
            const offsetTop = element.offsetTop - 70;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }
    downloadResume() {
        // Handle resume download
        const link = document.createElement('a');
        link.href = '/static/media/resume.pdf';
        link.download = 'Bhautik_Gauswami_Resume.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}
// Initialize the application
const app = new PortfolioApp();
// Export for global access if needed
window.portfolioApp = app;
//# sourceMappingURL=main.js.map