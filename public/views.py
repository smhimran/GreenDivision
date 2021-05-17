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

    condition = list(Problem.objects.filter(category="Condition"))
    condition_count = len(condition)

    geo = list(Problem.objects.filter(category="Geometry"))
    geo_count = len(geo)

    math = list(Problem.objects.filter(category="Simple Math"))
    math_count = len(math)

    loop = list(Problem.objects.filter(category="Loop"))
    loop_count = len(loop)

    array = list(Problem.objects.filter(category="Array/Simple DS"))
    array_count = len(array)

    string = list(Problem.objects.filter(category="String"))
    string_count = len(string)

    adhoc = list(Problem.objects.filter(category="Ad-hoc"))
    adhoc_count = len(adhoc)


    for problem in beginner:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in condition:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in math:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in loop:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in array:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in string:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%Y-%m-%d %H:%M')
            problem.solved = True
        else:
            problem.time = '-'
            problem.solved = False

    for problem in adhoc:
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

    return render(request, 'public/profile.html', {'profile': profile, "beginner": beginner, "condition": condition, "geo": geo, 
                                                    "math": math, "loop": loop, 'array': array, "string": string, "adhoc": adhoc,
                                                    "beginner_count": beginner_count, 
                                                    "condition_count": condition_count, 
                                                    "geo_count": geo_count,
                                                    "math_count": math_count,
                                                    "loop_count": loop_count,
                                                    "array_count": array_count,
                                                    "string_count": string_count,
                                                    "adhoc_count": adhoc_count,
                                                    })


def eligibility(request, id):
    return render(request, 'public/eligibility.html')


def about(request):
    return render(request, 'public/about.html')