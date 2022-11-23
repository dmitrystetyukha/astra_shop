from django.urls import path
from .views import *


urlpatterns = [
    path(
        "",
        UserCabinet.as_view(),
        name="user_cabinet",
    ),
    path(
        "register/",
        RegisterUser.as_view(),
        name="register",
    ),
    path(
        "login/",
        Login.as_view(),
        name="login",
    ),
    path(
        "logout/",
        logout_user,
        name="logout",
    ),
    path(
        "reset_password/",
        ResetPassword.as_view(),
        name="reset",
    ),
]
