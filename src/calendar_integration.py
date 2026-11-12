import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_calendar_service():
    ''' Returns an authorized Google Calendar API service instance. '''
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_study_event(action, duration_hours, exam_date):
    ''' Creates a study event in the user's Google Calendar. '''
    if action == "Rest":
        print("\nRest day selected. No study session was scheduled.")
        return

    service = get_calendar_service()

    start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(hours=duration_hours)

    event = {
        "summary": f"Study Plan: {action}",
        "description": (
            f"Recommended action: {action}\n"
            f"Study duration: {duration_hours} hour(s)\n"
            f"Exam date: {exam_date.isoformat()}"
        ),
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Vancouver"
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/Vancouver"
        }
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()

    print("\nCalendar event created successfully!")
    print(created_event.get("htmlLink"))