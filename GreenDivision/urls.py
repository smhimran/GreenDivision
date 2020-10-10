from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as mail_urls
from django.contrib.auth import views as auth_views
from . import settings
from views import main

urlpatterns = [
    path("", include("userPanel.urls", namespace="user")),
    path("accounts/login/", main.user_login, name="login"),
    path("accounts/logout/", main.user_logout, name="logout"),
    path("register/", main.sign_up, name="register"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("email/", include(mail_urls)),
]

if settings.DEBUG:
    urlpatterns += [path("dev-admin/", admin.site.urls)]
