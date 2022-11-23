import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main_app.models import *
from main_app.utils import menu
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    Добавляет товар в корзину и перенаправляет на детальное отображение корзины
    :param product_id: ссылка на товар
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], update_quantity=cd["update"])
    return redirect("cart:cart_detail")


def cart_remove(request, product_id):
    """
    Удаляет товар из корзины и перенаправляет на детальное отображение корзины
    :param product_id: ссылка на товар
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """
    Отображает шаблон с детальным отображением содержимого корзины
    :param request:
    """
    cart = Cart(request)
    context_data = {"menu": menu, "title": "Корзина", "cart": cart}
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "update": True}
        )
    return render(request, "cart/cart_detail.html", context=context_data)


@require_POST
def create_order(request):
    """
    Создает и сохраняет заказ, основываясь на содержимом корзины, перенаправляет на детольное отображение корзины
    """
    cart = Cart(request)
    order = Order(customer=request.user, timestamp=datetime.now())
    order.save_base()
    for item in cart:
        ProductsInOrder(
            order=order, product=item["product"], quantity=item["quantity"]
        ).save()
    cart.clear()
    return redirect("cart:cart_detail")
