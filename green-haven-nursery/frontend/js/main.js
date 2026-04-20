// ===================================
// Green Haven Nursery - Main JavaScript
// Core functionality and utilities
// ===================================

// API Configuration
const API_BASE_URL = 'https://green-haven-nursery.onrender.com/';

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Update cart count on page load
    updateCartCount();
    
    // Update auth link
    updateAuthLink();
});

// Update Cart Count
async function updateCartCount() {
    const token = localStorage.getItem('token');
    const cartCountElement = document.getElementById('cart-count');
    
    if (!cartCountElement) return;
    
    if (!token) {
        cartCountElement.textContent = '0';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            const totalItems = data.items ? data.items.reduce((sum, item) => sum + item.quantity, 0) : 0;
            cartCountElement.textContent = totalItems;
        } else {
            cartCountElement.textContent = '0';
        }
    } catch (error) {
        console.error('Error updating cart count:', error);
        cartCountElement.textContent = '0';
    }
}

// Update Auth Link
function updateAuthLink() {
    const token = localStorage.getItem('token');
    const authLink = document.getElementById('auth-link');
    
    if (!authLink) return;
    
    if (token) {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        authLink.textContent = user.name || 'Account';
        authLink.href = '#';
        authLink.addEventListener('click', function(e) {
            e.preventDefault();
            showAccountMenu();
        });
    } else {
        authLink.textContent = 'Login';
        authLink.href = 'pages/auth.html';
    }
}

// Show Account Menu
function showAccountMenu() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    const menu = document.createElement('div');
    menu.className = 'fixed inset-0 z-50 flex items-start justify-end p-4';
    menu.innerHTML = `
        <div class="fixed inset-0 bg-black bg-opacity-50" onclick="this.parentElement.remove()"></div>
        <div class="relative bg-white rounded-lg shadow-xl p-6 w-64 mt-16 mr-4 space-y-4">
            <div class="border-b border-stone-200 pb-4">
                <p class="text-sm text-stone-600">Signed in as</p>
                <p class="font-semibold text-emerald-900">${user.name}</p>
                <p class="text-xs text-stone-500">${user.email}</p>
            </div>
            <a href="orders.html" class="block text-stone-700 hover:text-emerald-700 transition">My Orders</a>
            <button onclick="logout()" class="w-full text-left text-red-600 hover:text-red-700 transition">
                Logout
            </button>
        </div>
    `;
    
    document.body.appendChild(menu);
}

// Logout Function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '../index.html';
}

// Format Price
function formatPrice(price) {
    return `$${parseFloat(price).toFixed(2)}`;
}

// Format Date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Validate Email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate Phone
function isValidPhone(phone) {
    const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
    return phoneRegex.test(phone);
}

// Show Loading Spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'flex justify-center items-center py-12';
    spinner.innerHTML = `
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-700"></div>
    `;
    element.innerHTML = '';
    element.appendChild(spinner);
}

// Show Error Message
function showError(element, message) {
    element.innerHTML = `
        <div class="text-center py-12">
            <svg class="w-16 h-16 text-stone-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="text-stone-600">${message}</p>
        </div>
    `;
}

// Debounce Function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Local Storage Helper
const storage = {
    get: (key) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error(`Error getting ${key} from localStorage:`, error);
            return null;
        }
    },
    
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error(`Error setting ${key} in localStorage:`, error);
            return false;
        }
    },
    
    remove: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error(`Error removing ${key} from localStorage:`, error);
            return false;
        }
    }
};

// Toast Notification System
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;
    
    const colors = {
        success: 'bg-emerald-600 text-white',
        error: 'bg-red-600 text-white',
        info: 'bg-blue-600 text-white',
        warning: 'bg-amber-600 text-white'
    };
    
    const icons = {
        success: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>`,
        error: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>`,
        info: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>`,
        warning: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>`
    };
    
    toast.className += ` ${colors[type]}`;
    toast.innerHTML = `
        <div class="flex items-center space-x-3">
            ${icons[type]}
            <span class="font-medium">${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    // Remove toast
    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
}

// Copy to Clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success', 2000);
    } catch (error) {
        console.error('Failed to copy:', error);
        showToast('Failed to copy', 'error', 2000);
    }
}

// Generate Delivery Code (Helper for frontend simulation)
function generateDeliveryCode() {
    return 'GH-' + Math.random().toString(36).substr(2, 9).toUpperCase();
}

// Check Authentication Status
function requireAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'auth.html';
        return false;
    }
    return true;
}

// Handle API Errors
function handleApiError(error, defaultMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    if (error.message === 'Failed to fetch') {
        showToast('Unable to connect to server. Please try again later.', 'error');
    } else if (error.status === 401) {
        showToast('Session expired. Please login again.', 'error');
        setTimeout(() => {
            logout();
        }, 2000);
    } else if (error.status === 403) {
        showToast('Access denied.', 'error');
    } else if (error.status === 404) {
        showToast('Resource not found.', 'error');
    } else if (error.status === 500) {
        showToast('Server error. Please try again later.', 'error');
    } else {
        showToast(error.message || defaultMessage, 'error');
    }
}

// Export utilities for other modules
window.GreenHaven = {
    API_BASE_URL,
    updateCartCount,
    updateAuthLink,
    logout,
    formatPrice,
    formatDate,
    isValidEmail,
    isValidPhone,
    showLoading,
    showError,
    showToast,
    copyToClipboard,
    generateDeliveryCode,
    requireAuth,
    handleApiError,
    storage
};
