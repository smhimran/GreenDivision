from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.index, name="index"),
    path("standings/", views.standings, name="standings"),
    path('profile/', views.user_profile, name="profile"),
]
