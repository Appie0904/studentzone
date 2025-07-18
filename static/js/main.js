// StudentZone Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Smooth scrolling for anchor links
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

    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Processing...';
                submitBtn.disabled = true;
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });

    // Vote button functionality
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!this.dataset.url) return;
            
            const voteType = this.dataset.voteType;
            const url = this.dataset.url;
            
            // Add loading state
            const originalHTML = this.innerHTML;
            this.innerHTML = '<span class="loading-spinner"></span>';
            this.disabled = true;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update vote count
                    const voteCount = this.closest('.vote-section').querySelector('.vote-count');
                    if (voteCount) {
                        voteCount.textContent = data.vote_count;
                    }
                    
                    // Update button state
                    this.classList.remove('voted', 'downvoted');
                    if (data.user_vote === 'upvote') {
                        this.classList.add('voted');
                    } else if (data.user_vote === 'downvote') {
                        this.classList.add('downvoted');
                    }
                    
                    // Show success message
                    showToast('Vote recorded successfully!', 'success');
                } else {
                    showToast(data.message || 'Error recording vote', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error recording vote', 'error');
            })
            .finally(() => {
                this.innerHTML = originalHTML;
                this.disabled = false;
            });
        });
    });

    // Bookmark functionality
    document.querySelectorAll('.bookmark-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!this.dataset.url) return;
            
            const url = this.dataset.url;
            const originalHTML = this.innerHTML;
            
            this.innerHTML = '<span class="loading-spinner"></span>';
            this.disabled = true;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle bookmark icon
                    const icon = this.querySelector('i');
                    if (data.bookmarked) {
                        icon.className = 'fas fa-bookmark text-primary';
                        showToast('Added to bookmarks!', 'success');
                    } else {
                        icon.className = 'far fa-bookmark';
                        showToast('Removed from bookmarks', 'info');
                    }
                } else {
                    showToast(data.message || 'Error updating bookmark', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error updating bookmark', 'error');
            })
            .finally(() => {
                this.innerHTML = originalHTML;
                this.disabled = false;
            });
        });
    });

    // Search functionality with debouncing
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2) {
                    performSearch(this.value);
                }
            }, 300);
        });
    }

    // Add fade-in animation to cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
});

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function performSearch(query) {
    // This would typically make an AJAX request to search endpoint
    // For now, we'll just log the query
    console.log('Searching for:', query);
}

// Export functions for use in other scripts
window.StudentZone = {
    showToast,
    getCookie,
    performSearch
}; 