from django.shortcuts import render
from django.contrib.auth.models import User
from userPanel.models import Problem, Profile, Submission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def standings(request):
    beginner = Problem.objects.filter(category="Input/Output")
    beginner_count = len(beginner)

    ifelse = Problem.objects.filter(category="If-else")
    ifelse_count = len(ifelse)

    maths = Problem.objects.filter(category="Geometry")
    maths_count = len(maths)

    profiles_list = Profile.objects.order_by(
        '-solve_count', 'last_submission_time')

    n = 1
    if request.user.is_authenticated:
        try:
            user = request.user
            user = Profile.objects.get(user=user)

            for i, item in enumerate(profiles_list):
                if item == user:
                    n = i+1
                    break

        except Exception as e:
            print(e)

    n = (n // 10) + 1

    paginator = Paginator(profiles_list, 10)

    page = request.GET.get('page', 1)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(n)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return render(request, "public/index.html", {
        "beginners": beginner, "ifelse": ifelse, "maths": maths,
        "beginner_count": beginner_count, "ifelse_count": ifelse_count,
        "maths_count": maths_count, "profiles": profiles
    })


def user_profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    submissions = Submission.objects.filter(user=profile).order_by('dateTime')

    return render(request, 'public/profile.html', {'profile': profile, "submissions": submissions})


def eligibility(request, id):
    return render(request, 'public/eligibility.html')


def about(request):
    return render(request, 'public/about.html')