from django.shortcuts import render, redirect
from .models import Problem, Profile, Submission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from cloudinary import uploader, api

@login_required
def editprofile(request):
    if request.method == "GET":
        user = request.user
        profile = Profile.objects.get(user=user)

        return render(request, "userPanel/editprofile.html", {"profile": profile})

    else:
        user = request.user
        profile = Profile.objects.get(user=user)

        name = request.POST.get("name")
        email = request.POST.get("email")
        department = request.POST.get("department")
        varsity_id = request.POST.get("varsity_id")
        uri_link = request.POST.get("uri_link")
        contact = request.POST.get("contact")
        image = request.FILES.get("image")
        show_email = request.POST.get("showemail")
        show_contact = request.POST.get("showcontact")

        if show_email == "on":
            show_email = True
        else:
            show_email = False

        if show_contact == "on":
            show_contact = True
        else:
            show_contact = False

        print(varsity_id)

        if image:
            uploaded = uploader.upload(image)
            link = uploaded["url"]
            profile.image = link

        user.email = email
        user.username = varsity_id
        
        user.save()

        profile.name = name
        profile.department = department
        profile.varsity_id = varsity_id
        profile.uri_link = uri_link
        profile.contact = contact
        profile.show_email = show_email
        profile.show_number = show_contact

        profile.save()

        return redirect("public:profile", id=user.id)