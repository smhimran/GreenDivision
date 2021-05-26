from django.core.management.base import BaseCommand
from userPanel.models import Problem, Profile
from userPanel.scraper import scrape_data

from googleapiclient.discovery import build
from google.oauth2 import service_account


class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Problem.objects.all().delete()

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # The ID of spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1gB4VeIGeGqDx1--vE5eor0fJUkbMWxj737YZbPxh-4I'

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="Sheet1!A2:D226").execute()

        values = result.get('values', [])

        for rows in values:
            problem_id = int(rows[2])
            name = rows[3]
            serial = rows[1]
            url = "https://www.urionlinejudge.com.br/judge/en/problems/view/" + rows[2]
            category = rows[0]

            models = Problem(problem_id=problem_id, name=name, serial=serial, url=url, category=category)
            models.save()
            print("saved " + name)

        print("\nUpdated Problems Successfully!\n")

        print("\nUpdating Profiles....\n")

        profiles = Profile.objects.all()

        for profile in profiles:
            profile.solve_count = 0
            profile.last_submission_time = None
            profile.total_scrapped = 0
            profile.status = "Active"

            profile.save()

        print("\nUpdated Profiles Successfully!\n")


        print("\nRunning Scrapper...\n")

        scrape_data()

        print("\nScrapper ran successfully!\n")

