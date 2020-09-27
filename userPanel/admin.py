from django.contrib import admin
from .models import Problem, Profile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Problem)