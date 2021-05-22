from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('edit/', views.editprofile, name="editprofile"),
    path('applyforblue/', views.applyforblue, name="applyforblue"),
]
