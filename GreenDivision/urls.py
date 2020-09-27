from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path("", include("userPanel.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("dev-admin/", admin.site.urls)]
