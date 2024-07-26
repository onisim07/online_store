from .cart import Cart
# ПРОЦЕССОР КОНТЕКСТА!
# ЗДЕСЬ СОЗДАЕТСЯ ЭКЗЕМПЛЯР КЛАССА Cart И ОБЕСПЕЧИВАЕТСЯ ЕГО
# ДОСТУПНОСТЬ ВО ВСЕХ ШАБЛОНАХ В ВИДЕ ПЕРЕМЕННОЙ cart

# Нужно редактировать настойки еще, в TEMPLATES += cart.context_processors.cart

def cart(request):
    count = len(Cart(request))
    if count % 10 == 1 and count % 100 != 11:
        string = 'товар'
    elif count % 10 >= 2 and count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        string = 'товара'
    else:
        string = 'товаров'

    return {'cart': Cart(request),
            'string': string}