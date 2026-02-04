import os.path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    if os.path.exists("external/token.json"):
        creds = Credentials.from_authorized_user_file(
            "external/token.json", SCOPES
        )

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "external/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("external/token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def create_calendar_event(
    summary: str,
    description: str,
    start_dt: datetime,
    end_dt: datetime,
):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    created_event = (
        service.events()
        .insert(calendarId="primary", body=event)
        .execute()
    )

    return created_event.get("htmlLink")
