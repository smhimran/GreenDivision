from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from userPanel.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_email_verification import sendConfirm
from cloudinary import uploader, api

def user_login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)

            if user.is_active == False:
                msg = "Account is not active, you need to activate your account before login. An account activation link has been sent to your mailbox."
                return render(request, "accounts/login.html", {"msg": msg})

            user = authenticate(username=user.username, password=password)

            if user:
                login(request, user)
                return redirect("public:index")
            else:
                msg = "Incorrect Password!"
                return render(request, "accounts/login.html", {"msg": msg})
        
        except User.DoesNotExist:
            msg = "No such user!"
            return render(request, "accounts/login.html", {"msg": msg})


def sign_up(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        department = request.POST.get("department")
        varsity_id = request.POST.get("id")
        image = request.FILES.get("image")
        username = varsity_id
        url = request.POST.get("url")
        contact = request.POST.get("contact")
        password = request.POST.get("password")
        conPassword = request.POST.get("conPassword")

        print(image)

        if password != conPassword:
            msg = "Passwords didn't match!"

            return render(request, "accounts/register.html", {"msg": msg})

        try:
            user = User.objects.create(
                username=username, password=password, email=email, is_active=False
            )
            user.set_password(password)
            user.save()

            if image:
                uploaded = uploader.upload(image)
                link = uploaded["url"]

                Profile.objects.create(
                    user=user, name=name, image=link, department=department, contact=contact, varsity_id=varsity_id, uri_link=url
                )

            else:
                Profile.objects.create(
                    user=user, name=name, department=department, varsity_id=varsity_id, uri_link=url
                )

            sendConfirm(user)

        except Exception as e:
            return render(request, "accounts/register.html", {"msg": "A user with the email or id already exists!"})

        return redirect("accounts:login")


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:login")