document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.añadir_al_carrito');
    const cartItemsContainer = document.querySelector('.cart-items tbody');
    const cartTotalPrice = document.getElementById('cart-total-price');
    const cartToggleButton = document.querySelector('.carrito');
    const cartContainer = document.querySelector('.cart-items-container');
    const cartCloseButton = document.querySelector('.cart-close-button');
    const buyButton = document.getElementById('cart-button-buy');
    const clearButton = document.getElementById('cart-button-clear');

    function saveCart() {
        const cartItems = [];
        cartItemsContainer.querySelectorAll('tr').forEach(row => {
            const id = row.dataset.productId;
            const nombre = row.querySelector('td:nth-child(2)').textContent;
            const precio = parseFloat(row.querySelector('td:nth-child(3)').textContent.replace('$', '').replace(',', ''));
            const cantidad = parseInt(row.querySelector('.item-quantity').value);
            const imagen = row.querySelector('td:nth-child(1) img').src;

            cartItems.push({ id, nombre, precio, cantidad, imagen });
        });
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
    }

    function loadCart() {
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        cartItems.forEach(producto => {
            const row = createCartItemRow(producto);
            row.querySelector('.item-quantity').value = producto.cantidad;
            cartItemsContainer.appendChild(row);
        });
        updateTotalPrice();
    }

    function addToCart(producto) {
        let existingCartItem = findCartItem(producto.id);

        if (existingCartItem) {
            const quantityElement = existingCartItem.querySelector('.item-quantity');
            quantityElement.value = parseInt(quantityElement.value) + 1;
        } else {
            const row = createCartItemRow(producto);
            cartItemsContainer.appendChild(row);
        }

        updateTotalPrice();
        saveCart();
        cartContainer.classList.add('show');
    }

    function findCartItem(productId) {
        return cartItemsContainer.querySelector(`tr[data-product-id="${productId}"]`);
    }

    function createCartItemRow(producto) {
        const row = document.createElement('tr');
        row.dataset.productId = producto.id;
        row.innerHTML = `
            <td><img src="${producto.imagen}" alt="${producto.nombre}" style="width: 50px;"></td>
            <td>${producto.nombre}</td>
            <td>${producto.precio.toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })}</td>
            <td><input type="number" class="item-quantity" value="1" min="1"></td>
            <td><button class="delete-button"><i class="fa-solid fa-times"></i></button></td>
        `;
        return row;
    }

    function updateTotalPrice() {
        let totalPrice = 0;
        cartItemsContainer.querySelectorAll('tr').forEach(row => {
            const priceText = row.querySelector('td:nth-child(3)').textContent;
            const price = parseFloat(priceText.replace('$', '').replace(',', ''));
            const quantity = parseInt(row.querySelector('.item-quantity').value);
            totalPrice += price * quantity;
        });
        cartTotalPrice.textContent = `Precio total: ${totalPrice.toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })}`;
    }

    function toggleCart() {
        console.log('Haciendo clic en el botón del carrito...');
        cartContainer.classList.toggle('show');
    }

    cartToggleButton.addEventListener('click', toggleCart);
    cartCloseButton.addEventListener('click', toggleCart);

    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const productId = event.currentTarget.dataset.productId;
            const productPrice = parseFloat(event.currentTarget.dataset.productPrice);
            const productName = event.currentTarget.closest('.section__instrumentos-cards-card').querySelector('.productos__titulo').textContent;
            const productImage = event.currentTarget.closest('.section__instrumentos-cards-card').querySelector('.productos__img').src;

            const producto = {
                id: productId,
                nombre: productName,
                precio: productPrice,
                imagen: productImage
            };

            addToCart(producto);
        });
    });

    buyButton.addEventListener('click', () => {
        const cartItems = cartItemsContainer.getElementsByTagName('tr');
        if (cartItems.length === 0) {
            swal({
                title: 'Carrito vacío',
                text: 'El carrito de compras está vacío. Agrega productos antes de realizar la compra.',
                icon: "error",
                button: "Aceptar"
            });
            return;
        }
    
        const productIds = [];
        const productPrices = [];
        const productQuantities = [];
        for (let i = 0; i < cartItems.length; i++) {
            const productId = cartItems[i].dataset.productId;
            const productQuantity = cartItems[i].querySelector('.item-quantity').value;
            const productPrice = parseFloat(cartItems[i].getElementsByTagName('td')[2].textContent.replace('$', '').replace(',', ''));
            productIds.push(productId);
            productQuantities.push(productQuantity);
            productPrices.push(productPrice);
        }
    
        const url = `/confirmar_compra/?productos=${productIds.join(',')}&cantidades=${productQuantities.join(',')}&precio_final=${calculateTotalPrice(productPrices)}`;
    
        swal({
            title: '¿Estás seguro de realizar la compra?',
            text: `Resumen del pedido:\n\n${productIds.map((id, index) => `${id} (Cantidad: ${productQuantities[index]}) - Precio: ${productPrices[index].toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })}`).join('\n')}\nTotal: ${calculateTotalPrice(productPrices).toLocaleString('es-MX', { style: 'currency', currency: 'MXN' })}\n\nUna vez confirmada la compra, los productos serán enviados y no podrás deshacer esta acción.`,
            icon: 'warning',
            buttons: {
                cancel: 'Cancelar',
                confirm: 'Comprar'
            },
            dangerMode: true
        }).then((confirmed) => {
            if (confirmed) {
                window.location.href = url;
            }
        });
    });

    function calculateTotalPrice(prices) {
        return prices.reduce((total, price) => total + price, 0);
    }

    clearButton.addEventListener('click', () => {
        cartItemsContainer.innerHTML = '';
        updateTotalPrice();
        saveCart();
    });

    cartItemsContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-button')) {
            const row = event.target.closest('tr');
            row.remove();
            updateTotalPrice();
            saveCart();
        }
    });

    cartItemsContainer.addEventListener('change', () => {
        updateTotalPrice();
        saveCart();
    });

    loadCart();
});