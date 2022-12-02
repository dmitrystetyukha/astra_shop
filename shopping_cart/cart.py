from decimal import Decimal
from django.conf import settings
from main_app.models import Product


class Cart(object):
    """Класс, описывающий поведение корзины товаров"""

    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняется ПУСТАЯ корзина в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """Перебирает товары в корзине и находит их в базе данных."""
        product_ids = self.cart.keys()
        # получаем товары и добавляем их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Возвращает количество товаров в корзине."""
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """Добавляет товар в корзину или обновляет его количество."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """Сохраняет товар"""
        self.session.modified = True

    def remove(self, product):
        """Удаляет товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Возвращает общую стоимость товаров в корзине"""
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_total_quantities(self):
        """
        Возвращает общее количество предметов в корзине
        :return:
        """
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        """Очищает корзину в сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
