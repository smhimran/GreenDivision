from django.contrib import admin
from .models import Problem, Profile, Submission

# Register your models here.

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('serial', 'problem_id', 'name', 'category')
    list_filter = ('category', )
    search_fields = ("serial", 'problem_id', 'name',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('varsity_id', 'name', 'department', 'status')
    list_filter = ('department', 'status')
    search_fields = ('varsity_id', 'name')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'dateTime')
    list_filter = ('problem', 'language')
    search_fields = ('user__user__username',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission, SubmissionAdmin)
