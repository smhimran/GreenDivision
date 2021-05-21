from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Problem(models.Model):
    Category_choices = (
        ('Input/Output', 'Input/Output'),
        ('Simple Math', 'Simple Math'),
        ('Condition', 'Condition'),
        ('Loop', 'Loop'),
        ('Geometry', 'Geometry'),
        ('Array/Simple DS', 'Array/Simple DS'),
        ('String', 'String'),
        ('Ad-hoc', 'Ad-hoc'),
    )
    problem_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=300)
    url = models.URLField(max_length=100, unique=True)
    category = models.CharField(max_length=100, choices=Category_choices, blank=True, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    Department_choices = (
        ('Computer Science and Engineering', 'Computer Science and Engineering'),
        ('Softwear Engineering', 'Softwear Engineering'),
        ('Other', 'Other'),
    )

    Status_choices = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Eligible', 'Eligible'),
        ('Blue', 'Blue'),
        ('Requested', 'Requested'),
        ('Request from Blue', 'Request from Blue'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    image = models.URLField(blank=True, null=True)
    varsity_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(
        max_length=500, choices=Department_choices, null=True)
    uri_link = models.URLField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    show_email = models.BooleanField(default=False)
    show_number = models.BooleanField(default=False)
    total_scrapped = models.IntegerField(default=0)
    solve_count = models.IntegerField(default=0)
    last_submission_time = models.DateTimeField(blank=True, null=True)
    solved_problems = models.ManyToManyField(Problem, through='Submission')
    status = models.CharField(
        max_length=150, choices=Status_choices, default='Active')

    def __str__(self):
        return self.varsity_id


class Submission(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    dateTime = models.DateTimeField()
