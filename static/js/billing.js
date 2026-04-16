// Billing functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const cart = [];
    let subtotal = 0;
    const taxRate = 0.10; // 10% tax

    // DOM Elements
    const productGrid = document.getElementById('productGrid');
    const cartItems = document.getElementById('cartItems');
    const subtotalElement = document.getElementById('subtotal');
    const taxElement = document.getElementById('tax');
    const totalElement = document.getElementById('total');
    const customerSelect = document.getElementById('customerSelect');
    const paymentMethod = document.getElementById('paymentMethod');
    const checkoutButton = document.getElementById('checkoutButton');

    // Product search functionality
    const searchInput = document.getElementById('productSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const products = productGrid.querySelectorAll('.product-card');
            
            products.forEach(product => {
                const productName = product.querySelector('.product-name').textContent.toLowerCase();
                const productSku = product.querySelector('.product-sku').textContent.toLowerCase();
                
                if (productName.includes(searchTerm) || productSku.includes(searchTerm)) {
                    product.style.display = '';
                } else {
                    product.style.display = 'none';
                }
            });
        });
    }

    // Category filter functionality
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const selectedCategory = this.value;
            const products = productGrid.querySelectorAll('.product-card');
            
            products.forEach(product => {
                const productCategory = product.getAttribute('data-category');
                
                if (selectedCategory === 'all' || productCategory === selectedCategory) {
                    product.style.display = '';
                } else {
                    product.style.display = 'none';
                }
            });
        });
    }

    // Add to cart functionality
    function addToCart(productId, quantity = 1) {
        const product = document.querySelector(`[data-product-id="${productId}"]`);
        if (!product) return;

        const productName = product.querySelector('.product-name').textContent;
        const productPrice = parseFloat(product.querySelector('.product-price').textContent.replace('$', ''));
        
        // Check if product is already in cart
        const existingItem = cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({
                id: productId,
                name: productName,
                price: productPrice,
                quantity: quantity
            });
        }
        
        updateCart();
    }

    // Update cart display
    function updateCart() {
        if (!cartItems) return;

        cartItems.innerHTML = '';
        subtotal = 0;

        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            subtotal += itemTotal;

            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-0">${item.name}</h6>
                        <small class="text-muted">$${item.price.toFixed(2)} x ${item.quantity}</small>
                    </div>
                    <div class="d-flex align-items-center">
                        <span class="me-2">$${itemTotal.toFixed(2)}</span>
                        <button class="btn btn-sm btn-danger" onclick="removeFromCart(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;

            cartItems.appendChild(cartItem);
        });

        const tax = subtotal * taxRate;
        const total = subtotal + tax;

        if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        if (taxElement) taxElement.textContent = `$${tax.toFixed(2)}`;
        if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;

        // Enable/disable checkout button
        if (checkoutButton) {
            checkoutButton.disabled = cart.length === 0 || !customerSelect.value;
        }
    }

    // Remove from cart functionality
    window.removeFromCart = function(productId) {
        const index = cart.findIndex(item => item.id === productId);
        if (index !== -1) {
            cart.splice(index, 1);
            updateCart();
        }
    };

    // Update quantity functionality
    window.updateQuantity = function(productId, change) {
        const item = cart.find(item => item.id === productId);
        if (item) {
            item.quantity += change;
            if (item.quantity < 1) item.quantity = 1;
            updateCart();
        }
    };

    // Customer selection change
    if (customerSelect) {
        customerSelect.addEventListener('change', function() {
            if (checkoutButton) {
                checkoutButton.disabled = cart.length === 0 || !this.value;
            }
        });
    }

    // Checkout functionality
    if (checkoutButton) {
        checkoutButton.addEventListener('click', function() {
            if (cart.length === 0 || !customerSelect.value) return;

            const orderData = {
                customer: customerSelect.value,
                items: cart,
                paymentMethod: paymentMethod.value,
                subtotal: subtotal,
                tax: subtotal * taxRate,
                total: subtotal + (subtotal * taxRate)
            };

            // Send order data to server
            fetch('/api/orders/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(orderData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Clear cart
                    cart.length = 0;
                    updateCart();
                    
                    // Show success message
                    showAlert('Order placed successfully!', 'success');
                    
                    // Reset form
                    customerSelect.value = '';
                    paymentMethod.value = 'cash';
                } else {
                    showAlert('Error placing order: ' + data.message, 'danger');
                }
            })
            .catch(error => {
                showAlert('Error placing order: ' + error.message, 'danger');
            });
        });
    }

    // Helper function to get CSRF token
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
}); 