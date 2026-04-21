// ===================================
// Green Haven Nursery - Authentication
// Login and Registration functionality
// ===================================

// Handle Registration
async function handleRegister(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    
    // Get form data
    const formData = {
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        password: form.password.value,
        confirm_password: form.confirm_password.value,
        phone: form.phone.value.trim(),
        address: form.address.value.trim()
    };
    
    // Validation
    if (!formData.name || !formData.email || !formData.password || !formData.phone || !formData.address) {
        showToast('Please fill in all fields', 'error');
        return;
    }
    
    if (!isValidEmail(formData.email)) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    if (formData.password.length < 6) {
        showToast('Password must be at least 6 characters long', 'error');
        return;
    }
    
    if (formData.password !== formData.confirm_password) {
        showToast('Passwords do not match', 'error');
        return;
    }
    
    if (!isValidPhone(formData.phone)) {
        showToast('Please enter a valid phone number', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating account...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: formData.name,
                email: formData.email,
                password: formData.password,
                phone: formData.phone,
                address: formData.address
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Account created successfully! Please login.', 'success');
            form.reset();
            
            // Switch to login tab after short delay
            setTimeout(() => {
                document.getElementById('login-tab').click();
            }, 1500);
        } else {
            showToast(data.message || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showToast('Unable to connect to server. Please try again later.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
    }
}

// Handle Login
async function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    
    // Get form data
    const email = form.email.value.trim();
    const password = form.password.value;
    
    // Validation
    if (!email || !password) {
        showToast('Please enter email and password', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token and user data
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showToast('Login successful!', 'success');
            
            // Redirect after short delay
            setTimeout(() => {
                const redirect = new URLSearchParams(window.location.search).get('redirect');
                window.location.href = redirect || '../index.html';
            }, 1000);
        } else {
            showToast(data.message || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Unable to connect to server. Please try again later.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
    }
}

// Check if user is already logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    if (token) {
        // Redirect to home if already logged in
        const redirect = new URLSearchParams(window.location.search).get('redirect');
        window.location.href = redirect || '../index.html';
    }
}

// Toggle Password Visibility
function togglePasswordVisibility(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.innerHTML = `
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
        `;
    } else {
        input.type = 'password';
        icon.innerHTML = `
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        `;
    }
}

// Initialize auth page
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    
    // Tab switching
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form-container');
    const registerForm = document.getElementById('register-form-container');
    
    if (loginTab && registerTab) {
        loginTab.addEventListener('click', function() {
            loginTab.classList.add('border-emerald-700', 'text-emerald-700');
            loginTab.classList.remove('border-transparent', 'text-stone-600');
            registerTab.classList.remove('border-emerald-700', 'text-emerald-700');
            registerTab.classList.add('border-transparent', 'text-stone-600');
            
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
        });
        
        registerTab.addEventListener('click', function() {
            registerTab.classList.add('border-emerald-700', 'text-emerald-700');
            registerTab.classList.remove('border-transparent', 'text-stone-600');
            loginTab.classList.remove('border-emerald-700', 'text-emerald-700');
            loginTab.classList.add('border-transparent', 'text-stone-600');
            
            registerForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
        });
    }
});

// Export functions
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.togglePasswordVisibility = togglePasswordVisibility;
