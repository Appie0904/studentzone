// StudentZone - Modern JavaScript Enhancements

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 StudentZone JavaScript loaded');
    
    // Initialize all components
    initNavbar();
    initSearch();
    initAnimations();
    initTooltips();
    initDropdowns();
    initScrollEffects();
    initLoadingStates();
    
    // Debug dropdown functionality
    debugDropdowns();
    
    // Add global test function
    window.testDropdown = testDropdownManually;
});

// Global test function for dropdown
function testDropdownManually() {
    console.log('🧪 Manual dropdown test started...');
    
    // Check Bootstrap
    if (typeof bootstrap === 'undefined') {
        console.error('❌ Bootstrap not loaded');
        return false;
    }
    
    console.log('✅ Bootstrap loaded:', bootstrap.VERSION);
    
    // Check for dropdown elements
    const dropdowns = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    console.log(`Found ${dropdowns.length} dropdown elements`);
    
    if (dropdowns.length === 0) {
        console.error('❌ No dropdown elements found');
        return false;
    }
    
    // Test first dropdown
    const firstDropdown = dropdowns[0];
    console.log('Testing dropdown:', firstDropdown);
    
    try {
        const dropdownInstance = new bootstrap.Dropdown(firstDropdown);
        console.log('✅ Dropdown instance created');
        
        // Try to show it
        dropdownInstance.show();
        console.log('✅ Dropdown shown');
        
        // Hide after 2 seconds
        setTimeout(() => {
            dropdownInstance.hide();
            console.log('✅ Dropdown hidden');
        }, 2000);
        
        return true;
    } catch (error) {
        console.error('❌ Error with dropdown:', error);
        return false;
    }
}

// Debug dropdown functionality
function debugDropdowns() {
    console.log('🔍 Debugging dropdowns...');
    
    // Check if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        console.log('✅ Bootstrap is loaded');
        console.log('Bootstrap version:', bootstrap.VERSION);
        
        // Check for dropdown elements
        const dropdownElements = document.querySelectorAll('[data-bs-toggle="dropdown"]');
        console.log('Found dropdown elements:', dropdownElements.length);
        
        dropdownElements.forEach((element, index) => {
            console.log(`Dropdown ${index + 1}:`, element);
            
            // Try to initialize dropdown manually
            try {
                const dropdown = new bootstrap.Dropdown(element);
                console.log(`✅ Dropdown ${index + 1} initialized successfully`);
            } catch (error) {
                console.error(`❌ Error initializing dropdown ${index + 1}:`, error);
            }
        });
    } else {
        console.error('❌ Bootstrap is not loaded!');
    }
}

// Navbar functionality (hide/show on scroll, background change)
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add background when scrolled
        if (scrollTop > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
        
        // Hide/show navbar on scroll
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}

// Search functionality (debounced input, focus/blur effects, loading state)
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(this.value);
        }, 300);
    });
    
    searchInput.addEventListener('focus', function() {
        this.parentElement.classList.add('search-focused');
    });
    
    searchInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('search-focused');
    });
}

function performSearch(query) {
    if (query.length < 2) return;
    
    console.log('Searching for:', query);
    // TODO: Implement actual search functionality
}

// Initialize animations (Intersection Observer for scroll-triggered animations)
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.content-card, .stat-card, .hero-graphic').forEach(el => {
        observer.observe(el);
    });
}

// Initialize tooltips (Bootstrap Tooltip)
function initTooltips() {
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Initialize dropdowns (custom logic for user profile dropdown)
function initDropdowns() {
    console.log('Initializing dropdowns...');
    
    // Wait a bit for Bootstrap to load
    setTimeout(() => {
        if (typeof bootstrap !== 'undefined' && bootstrap.Dropdown) {
            console.log('✅ Bootstrap Dropdown class available');
            
            // Initialize all dropdowns manually
            const dropdownElementList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
            console.log(`Found ${dropdownElementList.length} dropdown elements`);
            
            dropdownElementList.forEach(function (dropdownToggleEl, index) {
                console.log(`Initializing dropdown ${index + 1}:`, dropdownToggleEl);
                try {
                    const dropdown = new bootstrap.Dropdown(dropdownToggleEl);
                    console.log(`✅ Dropdown ${index + 1} initialized successfully`);
                } catch (error) {
                    console.error(`❌ Error initializing dropdown ${index + 1}:`, error);
                }
            });
        } else {
            console.error('❌ Bootstrap Dropdown not available');
            console.log('Bootstrap object:', typeof bootstrap);
            if (typeof bootstrap !== 'undefined') {
                console.log('Bootstrap keys:', Object.keys(bootstrap));
            }
            
            // Fallback: Manual dropdown implementation
            initManualDropdowns();
        }
    }, 100);
}

// Fallback manual dropdown implementation
function initManualDropdowns() {
    console.log('Using manual dropdown implementation');
    
    const dropdownToggles = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                const isOpen = dropdownMenu.classList.contains('show');
                
                // Close all other dropdowns
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
                
                // Toggle current dropdown
                if (!isOpen) {
                    dropdownMenu.classList.add('show');
                }
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

// Scroll effects (parallax for hero, smooth scroll for anchor links)
function initScrollEffects() {
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Loading states (add loading class to buttons)
function initLoadingStates() {
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        // Skip authentication forms (login, register, etc.)
        const form = button.closest('form');
        if (form && (form.action.includes('/login/') || form.action.includes('/register/') || form.action.includes('/logout/'))) {
            return;
        }
        
        button.addEventListener('click', function() {
            this.classList.add('loading');
            this.disabled = true;
            
            // Remove loading state after form submission
            setTimeout(() => {
                this.classList.remove('loading');
                this.disabled = false;
            }, 2000);
        });
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// API helper functions
const API = {
    async get(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                }
            });
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },
    
    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    }
};

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}

// Theme management
const Theme = {
    current: localStorage.getItem('theme') || 'light',
    
    init() {
        this.apply(this.current);
        this.addToggleListener();
    },
    
    apply(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.current = theme;
    },
    
    toggle() {
        const newTheme = this.current === 'light' ? 'dark' : 'light';
        this.apply(newTheme);
    },
    
    addToggleListener() {
        const themeToggle = document.querySelector('[data-theme-toggle]');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggle());
        }
    }
};

// Initialize theme
Theme.init();

// Export for global use
window.StudentZone = {
    showNotification,
    validateForm,
    API,
    Theme
}; 