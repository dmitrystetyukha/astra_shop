from django.contrib.auth import logout, login
from django.contrib.auth.views import *
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *

from user_cabinet.forms import *

from main_app.models import *
from user_cabinet.models import *


class RegisterUser(CreateView):
    """
    Встроенное отображение формы регистрации пользователя
    """

    form_class = RegisterUserForm
    template_name = "user_cabinet/user_cabinet.html"
    success_url = reverse_lazy("login")
    extra_context = {
        "title": "Регистрация",
        "button_text": "Зарегистрироваться",
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
        "title": "Авторизация",
        "button_text": "Авторизоваться",
        "button2_text": "Я хочу создать аккаунт",
    }


class ResetPassword(PasswordResetView):
    """
    Встроенное отображение формы восстановления пароля
    """

    form_class = PasswordResetForm
    template_name = "user_cabinet/user_cabinet.html"
    success_url = "main_page"
    extra_context = {
        "title": "Сброс пароля",
        "button_text": "Сбросить пароль",
    }


class UserCabinet(ListView):
    """
    Отображение личного кабинета пользователя со списком его заказов.
    """

    model = Order
    template_name = "user_cabinet/user_cabinet.html"
    extra_context = {
        "title": "Заказы",
        "products_in_order": 0,
    }

    def get_queryset(self):
        """Возвращает список заказов для пользователя"""
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
