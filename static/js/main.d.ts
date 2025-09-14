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
declare class PortfolioApp {
    private navMenu;
    private hamburger;
    private contactForm;
    private formMessage;
    private themeToggle;
    private currentTheme;
    constructor();
    private init;
    private setupEventListeners;
    private toggleMobileMenu;
    private closeMobileMenu;
    private toggleTheme;
    private loadTheme;
    private setupSmoothScrolling;
    private handleNavbarScroll;
    private handleContactForm;
    private validateForm;
    private submitContactForm;
    private getCSRFToken;
    private showFormMessage;
    private initializeParticles;
    private setupScrollAnimations;
    private setupActiveNavigation;
    scrollToSection(sectionId: string): void;
    downloadResume(): void;
}
declare const app: PortfolioApp;
