from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as mail_urls
from . import settings
from views import main

urlpatterns = [
    path("", include("userPanel.urls", namespace="user")),
    path("login/", main.user_login, name="login"),
    path("logout/", main.user_logout, name="logout"),
    path("register/", main.sign_up, name="register"),
    path("email/", include(mail_urls)),
]

if settings.DEBUG:
    urlpatterns += [path("dev-admin/", admin.site.urls)]
