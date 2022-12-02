from django.shortcuts import render
from django.views.generic import ListView, DetailView

from main_app.forms import *
from main_app.models import *
from main_app.utils import *
from shopping_cart.forms import CartAddProductForm

add_to_cart_form = CartAddProductForm()


def main_page(request):
    """Отображает главную страницу"""
    context_data = {"title": "Главная"}
    return render(request, "main_app/main_page.html", context=context_data)


class Catalog(ListView):
    """
    Представление хранимых в БД категорий товара позволяющее при помощи
    встроенного в django шаблонизатора формировать шаблон динамически,
    основываясь на содержимом БД.

    model -- модель из main_app/models.py, на основе которой
    будет изменяться шаблон
    template_name -- предварительно созданный шаблон в templates/main_app
    extra_context -- дополнительные данные, отправляемых шаблонизатору
    """

    model = ProductCategory
    template_name = "main_app/catalog.html"
    extra_context = {"title": "Каталог товаров"}


class Category(ListView):
    """
    Представление хранимых в БД товаров, принадлежащих категории, которая
    будет выбрана на странице для детального ознакомления. Позволяет при помощи
    встроенного в django шаблонизатора формировать шаблон динамически,
    основываясь на содержимом БД.

    model -- модель из main_app/models.py, на основе которой
    будет изменяться шаблон
    template_name -- предварительно созданный шаблон в templates/main_app
    extra_context -- дополнительные данные, отправляемых шаблонизатору
    """

    model = Product
    template_name = "main_app/category_single.html"
    extra_context = {"menu": menu, "title": ""}

    def get_queryset(self):
        title = (
            ProductCategory.objects.filter(id=self.kwargs["category_id"])
            .first()
            .name.capitalize()
        )
        self.extra_context["title"] = title
        return Product.objects.filter(category=self.kwargs["category_id"])


class ProductSingle(DetailView):
    """
    Представление хранимых в БД данных о конкретном товаре. Позволяет
    при помощи встроенного в django шаблонизатора формировать шаблон
    динамически, основываясь на содержимом БД.

    model -- модель из main_app/models.py, на основе которой
    будет изменяться шаблон
    slug_field -- поле, по которому осуществляется перееход к DetailView
    нужной записи в таблице "Product"
    template_name -- предварительно созданный шаблон в templates/main_app
    extra_context -- дополнительные данные, отправляемых шаблонизатору
    """

    model = Product  # используемая таблица в БД
    slug_field = "pk"
    template_name = "main_app/product_single.html"
    extra_context = {"title": "", "add_to_cart_form": add_to_cart_form}

    def get_object(self, queryset=None):
        showed_object = self.model.objects.get(pk=self.kwargs["product_id"])
        self.extra_context["title"] = showed_object.name.capitalize()
        return showed_object


def about(request):
    """
    Отображает страницу с контактной информацией
    """
    user_is_authorized = request.user.is_authenticated
    form = (
        CallBackOrderForAuthorizedUsers(request.POST)
        if user_is_authorized
        else CallBackOrderForUnauthorizedUsers(request.POST)
    )
    if form.is_valid():
        # если данные в форме верны
        form_data: dict = form.cleaned_data
        call_back_order = CallBackOrder()
        if user_is_authorized:
            # Если пользователь авторизован
            phone_number_from_db = (
                request.user.phone_number
            )
            call_back_order.name = request.user.first_name
            call_back_order.email = request.user.email
            call_back_order.phone_number = phone_number_from_db
            call_back_order.comment = (
                form_data["comment"]
                + "\nПредпочитаемый способ связи: "
                + form_data["preferred_communication_method"]
            )
        else:
            call_back_order.name = form_data["name"]
            call_back_order.email = form_data["email"]
            call_back_order.phone_number = form_data["phone_number"]
            call_back_order.comment = (
                form_data["comment"]
                + "\nПредпочитаемый способ связи: "
                + form_data["preferred_communication_method"]
            )
        call_back_order.timestamp = datetime.now()
        call_back_order.save()
        # сохраняется заявка на обратный
        form = (
            CallBackOrderForAuthorizedUsers()
            if user_is_authorized
            else CallBackOrderForUnauthorizedUsers()
        )
    context_data = {
        "form": form,
        "title": "О нас",
    }

    return render(request, "main_app/about.html", context=context_data)
