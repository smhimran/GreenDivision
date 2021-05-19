from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [

    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.sign_up, name="register"),
]
