// ===================================
// Green Haven Nursery - Cart JavaScript
// Shopping cart functionality
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'auth.html?redirect=cart.html';
        return;
    }
    
    loadCart();
});

async function loadCart() {
    const container = document.getElementById('cart-container');
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load cart');
        }
        
        const data = await response.json();
        
        if (!data.items || data.items.length === 0) {
            container.innerHTML = `
                <div class="text-center py-20">
                    <svg class="w-24 h-24 text-stone-300 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/>
                    </svg>
                    <h3 class="text-2xl font-serif text-stone-700 mb-4">Your cart is empty</h3>
                    <p class="text-stone-600 mb-8">Add some beautiful plants to get started!</p>
                    <a href="plants.html" class="bg-emerald-700 text-white px-8 py-3 rounded-full hover:bg-emerald-800 transition inline-block">
                        Shop Plants
                    </a>
                </div>
            `;
            return;
        }
        
        container.innerHTML = `
            <div class="grid lg:grid-cols-3 gap-8">
                <!-- Cart Items -->
                <div class="lg:col-span-2 space-y-4">
                    <h2 class="text-2xl font-serif text-emerald-950 mb-6">Cart Items (${data.items.length})</h2>
                    ${data.items.map(item => `
                        <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg transition" id="cart-item-${item.product.id}">
                            <div class="flex items-center gap-6">
                                <!-- Product Image -->
                                <div class="w-24 h-24 bg-gradient-to-br from-emerald-100 to-emerald-50 rounded-xl flex items-center justify-center flex-shrink-0">
                                    ${item.product.image_url ? 
                                        `<img src="${item.product.image_url}" alt="${item.product.name}" class="w-full h-full object-cover rounded-xl">` :
                                        `<svg class="w-12 h-12 text-emerald-300" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M12 22c4.97 0 9-4.03 9-9-4.97 0-9 4.03-9 9zM5.6 10.25c0 1.38 1.12 2.5 2.5 2.5.53 0 1.01-.16 1.42-.44l-.02.19c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5l-.02-.19c.4.28.89.44 1.42.44 1.38 0 2.5-1.12 2.5-2.5 0-1-.59-1.85-1.43-2.25.84-.4 1.43-1.25 1.43-2.25 0-1.38-1.12-2.5-2.5-2.5-.53 0-1.01.16-1.42.44l.02-.19C14.5 2.12 13.38 1 12 1S9.5 2.12 9.5 3.5l.02.19c-.4-.28-.89-.44-1.42-.44-1.38 0-2.5 1.12-2.5 2.5 0 1 .59 1.85 1.43 2.25-.84.4-1.43 1.25-1.43 2.25zM12 5.5c1.38 0 2.5 1.12 2.5 2.5s-1.12 2.5-2.5 2.5S9.5 9.38 9.5 8s1.12-2.5 2.5-2.5zM3 13c0 4.97 4.03 9 9 9 0-4.97-4.03-9-9-9z"/>
                                        </svg>`
                                    }
                                </div>
                                
                                <!-- Product Details -->
                                <div class="flex-grow">
                                    <h3 class="text-lg font-serif text-emerald-900 mb-1">${item.product.name}</h3>
                                    <p class="text-stone-600 text-sm mb-3">${item.product.description.substring(0, 80)}...</p>
                                    <div class="flex items-center justify-between">
                                        <span class="text-xl font-serif text-emerald-700">$${item.product.price.toFixed(2)}</span>
                                        
                                        <!-- Quantity Controls -->
                                        <div class="flex items-center gap-3">
                                            <div class="quantity-selector">
                                                <button onclick="updateQuantity(${item.product.id}, ${item.quantity - 1})" class="px-3 py-1">−</button>
                                                <input type="number" value="${item.quantity}" min="1" max="${item.product.stock}" readonly class="w-12 text-center border-none">
                                                <button onclick="updateQuantity(${item.product.id}, ${item.quantity + 1})" class="px-3 py-1">+</button>
                                            </div>
                                            
                                            <button onclick="removeFromCart(${item.product.id})" class="text-red-600 hover:text-red-700 transition">
                                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <!-- Order Summary -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-2xl p-6 shadow-lg sticky top-24">
                        <h3 class="text-xl font-serif text-emerald-950 mb-6">Order Summary</h3>
                        
                        <div class="space-y-4 mb-6">
                            <div class="flex justify-between text-stone-700">
                                <span>Subtotal</span>
                                <span>$${data.total.toFixed(2)}</span>
                            </div>
                            <div class="flex justify-between text-stone-700">
                                <span>Shipping</span>
                                <span class="text-emerald-600">FREE</span>
                            </div>
                            <div class="border-t border-stone-200 pt-4">
                                <div class="flex justify-between text-xl font-serif text-emerald-900">
                                    <span>Total</span>
                                    <span>$${data.total.toFixed(2)}</span>
                                </div>
                            </div>
                        </div>
                        
                        <a href="checkout.html" class="block w-full bg-emerald-700 text-white text-center py-3 rounded-full hover:bg-emerald-800 transition shadow-lg hover:shadow-xl mb-3">
                            Proceed to Checkout
                        </a>
                        
                        <a href="plants.html" class="block w-full text-center text-emerald-700 hover:text-emerald-800 transition py-2">
                            Continue Shopping
                        </a>
                    </div>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading cart:', error);
        container.innerHTML = `
            <div class="text-center py-20">
                <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <h3 class="text-2xl font-serif text-stone-700 mb-4">Unable to load cart</h3>
                <p class="text-stone-600 mb-8">Please try again later</p>
                <button onclick="loadCart()" class="bg-emerald-700 text-white px-8 py-3 rounded-full hover:bg-emerald-800 transition">
                    Retry
                </button>
            </div>
        `;
    }
}

async function updateQuantity(productId, newQuantity) {
    const token = localStorage.getItem('token');
    
    if (newQuantity < 1) {
        removeFromCart(productId);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart/update`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: newQuantity
            })
        });
        
        if (response.ok) {
            loadCart();
            updateCartCount();
        } else {
            const data = await response.json();
            showToast(data.message || 'Failed to update quantity', 'error');
        }
    } catch (error) {
        console.error('Error updating quantity:', error);
        showToast('Failed to update quantity', 'error');
    }
}

async function removeFromCart(productId) {
    const token = localStorage.getItem('token');
    
    if (!confirm('Remove this item from cart?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart/remove`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ product_id: productId })
        });
        
        if (response.ok) {
            showToast('Item removed from cart', 'success');
            loadCart();
            updateCartCount();
        } else {
            const data = await response.json();
            showToast(data.message || 'Failed to remove item', 'error');
        }
    } catch (error) {
        console.error('Error removing item:', error);
        showToast('Failed to remove item', 'error');
    }
}
