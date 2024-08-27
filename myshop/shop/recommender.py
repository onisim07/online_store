import redis
from django.conf import settings
from .models import Product


# Соединить с Redis:
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

class Recommender:
    def get_product_key(self, id):
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            for with_id in products_ids:
                # Получить другие товары, купленные вместе с каждым товаром:
                if product_id != with_id:
                    # Увеличить балл товара, купленного вместе:
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        products_ids = [p.id for p in products]
        if len(products) == 1:
            # только 1 товар:
            suggestions = r.zrange(
                self.get_product_key(products_ids[0]),
                0, -1, desc=True)[:max_results]
        else:
            # Сгенерировать временный ключ:
            flat_ids = ''.join([str(id) for id in products_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Несколько товаров, объединить баллы ысех товаров
            # сохранить полученное сортированное множество
            # во временном ключе
            keys = [self.get_product_key(id) for id in products_ids]
            r.zunionstore(tmp_key, keys)
            # Удалить ID товаров, для которых дается рекомендация:
            r.zrem(tmp_key, *products_ids)
            # Получить ID товаров по их кол-ву, сортировка по убыванию:
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # Удалить временный ключ:
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # Получить предлагаемые товары и
        # отсортировать по порядку их появления:
        suggested_products = list(Product.objects.filter(
            id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))