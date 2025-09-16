// TypeScript Main Application File
// Handles particles animation, smooth scrolling, contact form, and UI interactions

import { getParticlesConfig } from './lib/particlesConfig.js';

declare var particlesJS: any;

interface ContactFormData {
    name: string;
    email: string;
    subject: string;
    message: string;
}

interface ContactResponse {
    status: 'success' | 'error';
    message: string;
}

class PortfolioApp {
    private navMenu: HTMLElement | null;
    private hamburger: HTMLElement | null;
    private contactForm: HTMLFormElement | null;
    private formMessage: HTMLElement | null;
    private themeToggle: HTMLElement | null;
    private currentTheme: string = 'dark';

    constructor() {
        this.navMenu = document.getElementById('nav-menu');
        this.hamburger = document.getElementById('mobile-menu');
        this.contactForm = document.getElementById('contact-form') as HTMLFormElement;
        this.formMessage = document.getElementById('form-message');
        this.themeToggle = document.getElementById('theme-toggle');
        
        this.init();
    }

    private init(): void {
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupEventListeners();
                this.initializeParticles();
                this.setupScrollAnimations();
            });
        } else {
            this.setupEventListeners();
            this.initializeParticles();
            this.setupScrollAnimations();
        }
    }

    private setupEventListeners(): void {
        // Mobile menu toggle
        if (this.hamburger && this.navMenu) {
            this.hamburger.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }

        // Theme toggle with keyboard support
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
            
            // Keyboard support for accessibility
            this.themeToggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleTheme();
                }
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
                !this.navMenu.contains(e.target as Node) && 
                !this.hamburger.contains(e.target as Node)) {
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

    private toggleMobileMenu(): void {
        if (this.navMenu && this.hamburger) {
            this.navMenu.classList.toggle('active');
            this.hamburger.classList.toggle('active');
        }
    }

    private closeMobileMenu(): void {
        if (this.navMenu && this.hamburger) {
            this.navMenu.classList.remove('active');
            this.hamburger.classList.remove('active');
        }
    }

    private toggleTheme(): void {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        
        // Update TumbleButton aria-checked state
        if (this.themeToggle) {
            this.themeToggle.setAttribute('aria-checked', this.currentTheme === 'light' ? 'true' : 'false');
        }
        
        // Save theme preference
        localStorage.setItem('theme', this.currentTheme);
        
        // Reinitialize particles with new theme using optimized config
        this.initializeParticles();
    }

    private loadTheme(): void {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        this.currentTheme = savedTheme;
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        
        // Update TumbleButton aria-checked state
        if (this.themeToggle) {
            this.themeToggle.setAttribute('aria-checked', this.currentTheme === 'light' ? 'true' : 'false');
        }
    }

    private setupSmoothScrolling(): void {
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

    private handleNavbarScroll(): void {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(0, 0, 0, 0.98)';
            } else {
                navbar.style.background = 'rgba(0, 0, 0, 0.95)';
            }
        }
    }

    private async handleContactForm(): Promise<void> {
        if (!this.contactForm || !this.formMessage) return;

        const formData: ContactFormData = {
            name: (document.getElementById('name') as HTMLInputElement).value.trim(),
            email: (document.getElementById('email') as HTMLInputElement).value.trim(),
            subject: (document.getElementById('subject') as HTMLInputElement).value.trim(),
            message: (document.getElementById('message') as HTMLTextAreaElement).value.trim()
        };

        // Basic validation
        if (!this.validateForm(formData)) {
            this.showFormMessage('Please fill in all fields correctly.', 'error');
            return;
        }

        // Show loading state
        const submitBtn = this.contactForm.querySelector('button[type="submit"]') as HTMLButtonElement;
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;

        try {
            const response = await this.submitContactForm(formData);
            
            if (response.status === 'success') {
                this.showFormMessage(response.message, 'success');
                this.contactForm.reset();
            } else {
                this.showFormMessage(response.message, 'error');
            }
        } catch (error) {
            console.error('Contact form error:', error);
            this.showFormMessage('An error occurred. Please try again later.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    private validateForm(data: ContactFormData): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        // More lenient validation - message only needs to be longer than 3 characters
        return data.name.length > 0 &&
               emailRegex.test(data.email) &&
               data.subject.length > 0 &&
               data.message.length > 3;
    }

    private async submitContactForm(data: ContactFormData): Promise<ContactResponse> {
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

    private getCSRFToken(): string {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        return cookieValue || '';
    }

    private showFormMessage(message: string, type: 'success' | 'error'): void {
        if (!this.formMessage) return;

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

    private initializeParticles(): void {
        // Set particles container to cover entire document
        const particlesContainer = document.getElementById('particles-js');
        if (particlesContainer) {
            // Make sure particles cover the entire document height
            const documentHeight = Math.max(
                document.body.scrollHeight,
                document.body.offsetHeight,
                document.documentElement.clientHeight,
                document.documentElement.scrollHeight,
                document.documentElement.offsetHeight
            );
            
            particlesContainer.style.height = documentHeight + 'px';
            particlesContainer.parentElement!.style.height = documentHeight + 'px';
        }
        
        // Use optimized particles configuration
        if (typeof particlesJS !== 'undefined') {
            const config = getParticlesConfig(this.currentTheme as 'dark' | 'light');
            particlesJS('particles-js', config);
        }
    }

    private setupScrollAnimations(): void {
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

    private setupActiveNavigation(): void {
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
    public scrollToSection(sectionId: string): void {
        const element = document.getElementById(sectionId);
        if (element) {
            const offsetTop = element.offsetTop - 70;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    }

    public downloadResume(): void {
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
(window as any).portfolioApp = app;
