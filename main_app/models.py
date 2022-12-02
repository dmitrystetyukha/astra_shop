from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from astra_shop.settings import MEDIA_ROOT


class ProductCategory(models.Model):
    """
    Класс, описывающий модель представления сущности "Категория продукта".

    Параметры:
        name -- наименование категории товара
        description -- краткое описание категории
        image -- фотография
    """

    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=MEDIA_ROOT)

    class Meta:
        verbose_name_plural = "Категории товара"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """
    Класс, описывающий модель представления сущности "Продукт".

    Параметры:
        name -- наименование товара
        description -- краткое описание товара
        category -- ссылка на категорию, к которой относится
        товар
        image -- фотография
        price -- стоимость одной единицы товара
    """

    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(
        to="ProductCategory", on_delete=models.CASCADE, blank=False
    )
    image = models.ImageField(upload_to=MEDIA_ROOT)
    price = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return f"{self.name} {self.category.name}"

    class Meta:
        verbose_name_plural = "Товары"


class Order(models.Model):
    """
    Класс, описывающий модель представления сущности "Заказ".

    Параметры:
        timestamp -- дата оформления заказа
        product -- ссылка на товар
        customer -- ссылка на пользователя, которым совершен заказ
    """

    timestamp = models.DateTimeField(
        blank=False,
    )
    customer = models.ForeignKey(
        to="user_cabinet.User", blank=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.timestamp}, order #{self.pk} from {self.customer.first_name}"

    class Meta:
        verbose_name_plural = "Заказы"


class ProductsInOrder(models.Model):
    """
    Класс, описывающий модель представления сущности "Товары в заказах".
    Параметры:
        order -- ссылка на заказ
        product -- ссылка на товар
        quantity -- к-во товара в заказе
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = "Товары в заказах"


class CallBackOrder(models.Model):
    """
    Класс, описывающий модель представления сущности "Заявка на обратный звонок".
    Таблица хранит заявки от анонимных пользователей
    Параметры:
        name, email, phone_number -- контактные данные
        timestamp -- дата оформления заявки, по умолчанию - текущая дата
        comment -- комментарий к заявке
    """

    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(
        blank=False,
    )
    comment = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name_plural = "Заявки на обратный звонок"
