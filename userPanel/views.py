from django.shortcuts import render, redirect
from .models import Problem, Profile, Submission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.contrib.sites.models import Site
from cloudinary import uploader, api
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import pytz
from GreenDivision import settings

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

@login_required
def applyforblue(request):
    if request.method == "GET":
        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.status != 'Eligible':
            return redirect("public:eligiblilty", id=user.id)
        
        return render(request, "userPanel/apply_for_blue.html", {"profile": profile})
    else:
        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.status != 'Eligible':
            return redirect("public:eligiblilty", id=user.id)

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = settings.BASE_DIR / 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        SAMPLE_SPREADSHEET_ID = '1rVBv0BMY7e_Vs-QcdawwMR8yRnl0TcdH9t8aE94xBu4'

        service = build('sheets', 'v4', credentials=creds)

        #create the row to insert as lists of list
        current_time = datetime.now(pytz.timezone("Asia/Dhaka")).strftime('%d/%m/%Y %I:%M:%S %p')

        name = profile.name
        email = user.email
        department = profile.department
        varsity_id = profile.varsity_id
        uri_link = profile.uri_link

        green_profile = reverse('public:profile', args=(request.user.id,))
        domain = request.META['HTTP_HOST']
        green_profile = "http://" + domain + green_profile

        solve_count = profile.solve_count

        semester = request.POST.get("semester")
        contact = request.POST.get("contact")
        campus = request.POST.get("campus")
        takeoff = request.POST.get("takeoff")
        contest = request.POST.get("contest")
        rank = request.POST.get("rank")
        coding_hour = request.POST.get("coding-hour")
        why = request.POST.get("why")
        view = request.POST.get("view")
        view_cp = request.POST.get("cp-view")

        user_data = [[  current_time, name, email, department, varsity_id, uri_link, green_profile, solve_count, semester, contact, campus, takeoff, contest, rank, coding_hour, why, view, view_cp ]]

        # Call the Sheets API
        sheet = service.spreadsheets()

        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A2", valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":user_data})
        response = request.execute()

        print(response)

        return redirect("public:profile", id=user.id)