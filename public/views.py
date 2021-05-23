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
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in condition:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in math:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in loop:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in array:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in string:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in adhoc:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

    for problem in geo:
        time = submissions.filter(problem=problem)

        if time.exists():
            problem.time = time[0].dateTime.strftime('%B %d, %Y at %H:%M %p')
            problem.solved = True
            problem.language = time[0].language
        else:
            problem.time = '-'
            problem.solved = False
            problem.language = '-'

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

    beginner_solved = 0
    condition_solved = 0
    math_solved = 0
    loop_solved = 0
    geo_solved = 0
    array_solved = 0
    string_solved = 0
    adhoc_solved = 0

    for problem in beginner:
        time = submissions.filter(problem=problem)

        if time.exists():
            beginner_solved += 1

    for problem in condition:
        time = submissions.filter(problem=problem)

        if time.exists():
            condition_solved += 1

    for problem in math:
        time = submissions.filter(problem=problem)

        if time.exists():
            math_solved += 1

    for problem in loop:
        time = submissions.filter(problem=problem)

        if time.exists():
            loop_solved += 1

    for problem in array:
        time = submissions.filter(problem=problem)

        if time.exists():
            array_solved += 1

    for problem in string:
        time = submissions.filter(problem=problem)

        if time.exists():
            string_solved += 1

    for problem in adhoc:
        time = submissions.filter(problem=problem)

        if time.exists():
            adhoc_solved += 1

    for problem in geo:
        time = submissions.filter(problem=problem)

        if time.exists():
            geo_solved += 1

    beginner_percentage = (beginner_solved / beginner_count) * 100
    math_percentage = (math_solved / math_count) * 100
    condition_percentage = (condition_solved / condition_count) * 100
    loop_percentage = (loop_solved / loop_count) * 100
    geo_percentage = (geo_solved / geo_count) * 100
    array_percentage = (array_solved / array_count) * 100
    string_percentage = (string_solved / string_count) * 100
    adhoc_percentage = (adhoc_solved / adhoc_count) * 100

    return render(request, 'public/eligibility.html', {'profile': profile, 
                                                    "beginner_count": beginner_count, "condition_count": condition_count, 
                                                    "geo_count": geo_count, "math_count": math_count,
                                                    "loop_count": loop_count, "array_count": array_count,
                                                    "string_count": string_count, "adhoc_count": adhoc_count,
                                                    "beginner_solved": beginner_solved, "condition_solved": condition_solved, 
                                                    "geo_solved": geo_solved, "math_solved": math_solved,
                                                    "loop_solved": loop_solved, "array_solved": array_solved,
                                                    "string_solved": string_solved, "adhoc_solved": adhoc_solved,
                                                    "beginner_percentage": beginner_percentage, "condition_percentage": condition_percentage, 
                                                    "geo_percentage": geo_percentage, "math_percentage": math_percentage,
                                                    "loop_percentage": loop_percentage, "array_percentage": array_percentage,
                                                    "string_percentage": string_percentage, "adhoc_percentage": adhoc_percentage,
                                                    })


def about(request):
    return render(request, 'public/about.html')