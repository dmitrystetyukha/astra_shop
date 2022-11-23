from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


@admin.register(ProductsInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(CallBackOrder)
class CallBackOrderAdmin(admin.ModelAdmin):
    list_display = ["timestamp"]
