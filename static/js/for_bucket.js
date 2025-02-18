
function decreaseQuantity(productId, cost) {
    updateQuantity(productId, -1, cost);
}

function increaseQuantity(productId, cost) {
    updateQuantity(productId, 1, cost);
}

function updateButtonState(productId, newQuantity, cost) {
    // Обновляем состояние кнопки в зависимости от значения newQuantity
    if (newQuantity <= 1) {
        $('#quantity-button-minus-' + productId).prop('disabled', true);
        $('#quantity-' + productId).text('1');
        $('#total-cost-' + productId).text('Общая стоимость: ' + cost);
    } else {
        $('#quantity-button-minus-' + productId).prop('disabled', false);
    }
}


function updateQuantity(productId, change, cost) {
    $.ajax({
        type: 'POST',
        url: '/update_quantity',  // Замените на ваш реальный маршрут на сервере
        data: { 'product_id': productId, 'change': change, 'cost': cost},
        success: function(response) {
            // Обработка успешного ответа от сервера
            console.log(response);
            $('#quantity-' + productId).text(response.new_quantity);

            var totalCost = response.new_quantity * cost;
            $('#total-cost-' + productId).text('Общая стоимость: ' + totalCost);

            var newQuantity = parseInt(response.new_quantity);
                updateButtonState(productId, newQuantity, cost);

            $('#total').text(response.new_total)
        },
        error: function(error) {
            // Обработка ошибки
            console.error(error);
        }
    });
}


function deleteProduct(pid) {
    $.ajax({
        url: '/delete-product/' + pid,
        type: 'DELETE',
        success: function(response) {
            // Обновление корзины или других элементов страницы
            console.log('Товар успешно удален');
            // Пример: Удаление соответствующего блока товара из DOM
            $('#product-' + pid).remove();
            if ($('.product-block').length === 0) {
                // Если все блоки удалены, обновляем страницу
                window.location.reload();
            }
        },
        error: function(error) {
            console.error('Ошибка при удалении товара:', error);
        }
    });
}


