from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as mail_urls
from django.contrib.auth import views as auth_views
from . import settings
from views import main

urlpatterns = [
    path("", include("public.urls", namespace="public")),
    path("user/", include("userPanel.urls", namespace="user")),
    path("accounts/", include("accounts.urls",namespace="accounts")),

    # URL path for sending emails
    path("email/", include(mail_urls)),
]

if settings.DEBUG:
    urlpatterns += [path("dev-admin/", admin.site.urls)]
