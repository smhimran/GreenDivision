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

    # Auth urls (Important for default password reset)

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # URL path for sending emails
    path("email/", include(mail_urls)),
]

if settings.DEBUG:
    urlpatterns += [path("dev-admin/", admin.site.urls)]
