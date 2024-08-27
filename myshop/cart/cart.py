from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        '''Инициализировать корзину'''
        self.session = request.session
        # Получаем корзину из текущего сеанса:
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохранить пустую корзину в сеансе:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Сохранить текущий применённый купон:
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        ''' Добавить товар в козину либо обновить его кол-во.
            quantity=1 - кол-во товара.
            override_quantity - нужно ли заменить кол-во переданным кол-вом (True) /
            прибавить новое кол-во (False).
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        '''Пометить сеанс как изменённый, чтобы обеспечить его сохранение'''
        self.session.modified = True

    def remove(self, product):
        '''Удалить товар из корзины'''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных
        '''
        product_ids = self.cart.keys()
        # Получить объекты Product и добавить из в корзину:
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''Подсчитывать все товарные позиции в корзине.'''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''Общая стоимость товаров:'''
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        '''Удалить корзмну из сеанса'''
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
