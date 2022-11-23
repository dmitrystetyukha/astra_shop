from django.contrib.auth import logout, login
from django.contrib.auth.views import *
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *

from main_app.utils import menu
from user_cabinet.forms import *

from main_app.models import *


class RegisterUser(CreateView):
    """
    Встроенное отображение формы регистрации пользователя
    """

    form_class = RegisterUserForm
    template_name = "user_cabinet/user_cabinet.html"
    success_url = reverse_lazy("login")
    extra_context = {
        "title": "Кабинет пользователя | Регистрация",
        "head_title": "Интернет-магазин фурнитуры АСТРА | Регистрация",
        "button_text": "Зарегистрироваться",
        "menu": menu,
    }

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("main_page")

    class Meta:
        model = User


class Login(LoginView):
    """
    Встроенное отображение формы авторизации
    """

    form_class = LoginUserForm
    template_name = "user_cabinet/user_cabinet.html"
    success_url = "main_page"
    extra_context = {
        "title": "Кабинет пользователя | Авторизация",
        "head_title": "Интернет-магазин фурнитуры АСТРА | Авторизация",
        "button_text": "Авторизоваться",
        "button2_text": "Я хочу создать аккаунт",
        "menu": menu,
    }


class ResetPassword(PasswordResetView):
    """
    Встроенное отображение формы восстановления пароля
    """

    form_class = PasswordResetForm
    template_name = "user_cabinet/user_cabinet.html"
    success_url = "main_page"
    extra_context = {
        "title": "Кабинет пользователя | Сброс пароля",
        "head_title": "Интернет-магазин фурнитуры АСТРА | Сброс пароля",
        "button_text": "Сбросить пароль",
        "menu": menu,
    }


class UserCabinet(ListView):
    """
    Отображение личного кабинета пользователя со списком его заказов.
    """

    model = Order
    template_name = "user_cabinet/user_cabinet.html"
    extra_context = {
        "title": "Кабинет пользователя | Заказы",
        "head_title": "Интернет-магазин фурнитуры АСТРА | Личный кабинет",
        "menu": menu,
        "products_in_order": 0,
    }

    def get_queryset(self):
        orders_created_by_current_user = Order.objects.filter(
            customer=self.request.user
        )
        self.extra_context["products_in_order"] = ProductsInOrder.objects.filter(
            order__in=orders_created_by_current_user
        )
        return orders_created_by_current_user


def logout_user(request):
    logout(request)
    return redirect("main_page")
