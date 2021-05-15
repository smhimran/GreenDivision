from django.shortcuts import render
from django.contrib.auth.models import User
from userPanel.models import Problem, Profile, Submission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def standings(request):
    
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

    return render(request, "public/index.html", {"profiles": profiles})


def user_profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    submissions = Submission.objects.filter(user=profile).order_by('problem')
    # problems = Problem.objects.all()

    beginner = list(Problem.objects.filter(category="Input/Output"))
    beginner_count = len(beginner)

    ifelse = list(Problem.objects.filter(category="If-else"))
    ifelse_count = len(ifelse)

    geo = list(Problem.objects.filter(category="Geometry"))
    geo_count = len(geo)


    for problem in beginner:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in ifelse:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in geo:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    return render(request, 'public/profile.html', {'profile': profile, "beginner": beginner, "ifelse": ifelse, "geo": geo, 
                                                    "beginner_count": beginner_count, 
                                                    "ifelse_count": ifelse_count, 
                                                    "geo_count": geo_count})


def eligibility(request, id):
    return render(request, 'public/eligibility.html')


def about(request):
    return render(request, 'public/about.html')