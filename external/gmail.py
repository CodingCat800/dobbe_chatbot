import base64
import os.path
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]

def get_gmail_service():
    creds = None

    if os.path.exists("integrations/token.json"):
        creds = Credentials.from_authorized_user_file(
            "external/token.json", SCOPES
        )

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "external/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=8080)

        with open("external/token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email_gmail_api(
    to_email: str,
    subject: str,
    body: str,
):
    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()
