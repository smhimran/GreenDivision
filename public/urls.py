from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.standings, name="index"),
    path("standings/", views.standings, name="standings"),
    path('profile/<int:id>/', views.user_profile, name="profile"),
    path('eligibility/<int:id>/', views.eligibility, name="eligiblilty"),
    path("about/", views.about, name="about")
]
