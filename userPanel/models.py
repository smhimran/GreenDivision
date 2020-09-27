from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    varsity_id = models.CharField(max_length=100, unique=True)
    uri_link = models.URLField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    show_email = models.BooleanField(default=False)
    show_number = models.BooleanField(default=False)

    def __str__(self):
        return self.varsity_id


class Problem(models.Model):
    problem_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=300)
    url = models.URLField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name