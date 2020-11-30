from django.shortcuts import render
from .models import Problem, Profile


def index(request):
    return render(request, "userPanel/index.html")


def standings(request):
    beginner = Problem.objects.filter(category="Beginner")
    beginner_count = len(beginner)

    ifelse = Problem.objects.filter(category="If-else")
    ifelse_count = len(ifelse)

    maths = Problem.objects.filter(category="Math")
    maths_count = len(maths)

    profiles = Profile.objects.order_by(
        '-solve_count', 'last_submission_time')

    return render(request, "userPanel/standings.html", {
        "beginners": beginner, "ifelse": ifelse, "maths": maths,
        "beginner_count": beginner_count, "ifelse_count": ifelse_count,
        "maths_count": maths_count, "profiles": profiles
    })
