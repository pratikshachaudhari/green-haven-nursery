// ===================================
// Green Haven Nursery - Home Page JavaScript
// Loads featured products on the home page
// ===================================

document.addEventListener('DOMContentLoaded', async function() {
    await loadFeaturedProducts();
});

async function loadFeaturedProducts() {
    const featuredContainer = document.getElementById('featured-plants');
    
    if (!featuredContainer) return;
    
    try {
        // Fetch products from API
        const response = await fetch(`${API_BASE_URL}/products`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        
        const products = await response.json();
        
        // Take first 3 products as featured
        const featuredProducts = products.slice(0, 3);
        
        // Clear loading placeholders
        featuredContainer.innerHTML = '';
        
        // Create product cards
        featuredProducts.forEach(product => {
            const card = createProductCard(product);
            featuredContainer.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading featured products:', error);
        featuredContainer.innerHTML = `
            <div class="col-span-3 text-center py-12">
                <p class="text-stone-600">Unable to load featured products.</p>
                <a href="pages/plants.html" class="text-emerald-700 hover:text-emerald-800 underline mt-4 inline-block">
                    View all plants
                </a>
            </div>
        `;
    }
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 group';
    
    card.innerHTML = `
        <div class="relative h-80 overflow-hidden bg-stone-100">
            <img 
                src="${product.image_url}" 
                alt="${product.name}"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                onerror="this.src='https://via.placeholder.com/400x400/10b981/ffffff?text=${encodeURIComponent(product.name)}'"
            >
        </div>
        <div class="p-6">
            <h3 class="text-xl font-serif text-emerald-900 mb-2">${product.name}</h3>
            <p class="text-stone-600 text-sm mb-4 line-clamp-2">${product.description}</p>
            <div class="flex items-center justify-between">
                <span class="text-2xl font-semibold text-emerald-800">$${product.price.toFixed(2)}</span>
                <button 
                    onclick="addToCartFromHome(${product.id})"
                    class="bg-emerald-700 text-white px-6 py-2 rounded-full hover:bg-emerald-800 transition-colors duration-200 text-sm font-medium"
                >
                    Add to Cart
                </button>
            </div>
        </div>
    `;
    
    return card;
}

async function addToCartFromHome(productId) {
    const token = localStorage.getItem('token');
    
    if (!token) {
        // Redirect to login if not authenticated
        window.location.href = 'pages/auth.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });
        
        if (response.ok) {
            showToast('Added to cart!', 'success');
            updateCartCount();
        } else {
            const data = await response.json();
            showToast(data.message || 'Failed to add to cart', 'error');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('Failed to add to cart', 'error');
    }
}
