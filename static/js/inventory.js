// Inventory management functionality
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const productTable = document.getElementById('productTable');
    const searchInput = document.getElementById('productSearch');
    const categoryFilter = document.getElementById('categoryFilter');
    const stockFilter = document.getElementById('stockFilter');
    const addProductButton = document.getElementById('addProductButton');
    const productModal = document.getElementById('productModal');
    const productForm = document.getElementById('productForm');

    // Product search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = productTable.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const productName = row.querySelector('.product-name').textContent.toLowerCase();
                const productSku = row.querySelector('.product-sku').textContent.toLowerCase();
                
                if (productName.includes(searchTerm) || productSku.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Category filter functionality
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const selectedCategory = this.value;
            const rows = productTable.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const productCategory = row.getAttribute('data-category');
                
                if (selectedCategory === 'all' || productCategory === selectedCategory) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Stock filter functionality
    if (stockFilter) {
        stockFilter.addEventListener('change', function() {
            const selectedStock = this.value;
            const rows = productTable.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const stockLevel = parseInt(row.querySelector('.stock-level').textContent);
                
                if (selectedStock === 'all') {
                    row.style.display = '';
                } else if (selectedStock === 'low' && stockLevel <= 10) {
                    row.style.display = '';
                } else if (selectedStock === 'out' && stockLevel === 0) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Add product functionality
    if (addProductButton && productModal) {
        addProductButton.addEventListener('click', function() {
            const modal = new bootstrap.Modal(productModal);
            modal.show();
        });
    }

    // Handle product form submission
    if (productForm) {
        productForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const productData = {
                name: formData.get('name'),
                sku: formData.get('sku'),
                category: formData.get('category'),
                price: parseFloat(formData.get('price')),
                quantity: parseInt(formData.get('quantity')),
                alert_threshold: parseInt(formData.get('alert_threshold')),
                description: formData.get('description')
            };

            // Send product data to server
            fetch('/api/products/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(productData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(productModal);
                    modal.hide();
                    
                    // Show success message
                    showAlert('Product added successfully!', 'success');
                    
                    // Reset form
                    productForm.reset();
                    
                    // Refresh product table
                    location.reload();
                } else {
                    showAlert('Error adding product: ' + data.message, 'danger');
                }
            })
            .catch(error => {
                showAlert('Error adding product: ' + error.message, 'danger');
            });
        });
    }

    // Update stock functionality
    window.updateStock = function(productId) {
        const newStock = prompt('Enter new stock quantity:');
        if (newStock === null) return;
        
        const quantity = parseInt(newStock);
        if (isNaN(quantity) || quantity < 0) {
            showAlert('Please enter a valid quantity', 'danger');
            return;
        }

        fetch(`/api/products/${productId}/update-stock/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update stock display
                const stockElement = document.querySelector(`[data-product-id="${productId}"] .stock-level`);
                if (stockElement) {
                    stockElement.textContent = quantity;
                    
                    // Update row class based on stock level
                    const row = stockElement.closest('tr');
                    row.classList.remove('table-warning', 'table-danger');
                    
                    if (quantity <= 10) {
                        row.classList.add('table-warning');
                    }
                    if (quantity === 0) {
                        row.classList.add('table-danger');
                    }
                }
                
                showAlert('Stock updated successfully!', 'success');
            } else {
                showAlert('Error updating stock: ' + data.message, 'danger');
            }
        })
        .catch(error => {
            showAlert('Error updating stock: ' + error.message, 'danger');
        });
    };

    // Delete product functionality
    window.deleteProduct = function(productId) {
        if (!confirm('Are you sure you want to delete this product?')) return;

        fetch(`/api/products/${productId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove product row
                const row = document.querySelector(`[data-product-id="${productId}"]`);
                if (row) {
                    row.remove();
                }
                
                showAlert('Product deleted successfully!', 'success');
            } else {
                showAlert('Error deleting product: ' + data.message, 'danger');
            }
        })
        .catch(error => {
            showAlert('Error deleting product: ' + error.message, 'danger');
        });
    };

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