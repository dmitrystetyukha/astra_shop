from django.contrib.auth.forms import *
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    first_name = forms.CharField(label="Имя", widget=forms.TextInput())
    email = forms.CharField(label="Email", widget=forms.EmailInput())
    phone_number = forms.CharField(
        label="Номер телефона (необязательно)", widget=forms.TextInput(), required=False
    )
    password1 = forms.CharField(label="Придумайте пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(
        label="Повторите придуманный пароль", widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )


class ResetPasswordForm(PasswordResetForm):
    pass
