from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Function to store auth token, dont need to login everytime


def get_credentials():
    creds = None
    # Load credentials from token.json if available
    if os.path.exists('MindEase/utils/token.json'):
        creds = Credentials.from_authorized_user_file(
            'MindEase/utils/token.json', SCOPES)

    # If credentials are not valid, authenticate again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh token automatically
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'MindEase/utils/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new credentials
        with open('MindEase/utils/token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return creds


creds = get_credentials()
service = build('calendar', 'v3', credentials=creds)

# Get Calendar List
calendar_list = service.calendarList().list().execute()
print(calendar_list, end="\n")

event = {
    'summary': 'Meeting with Capstone Team',
    'location': 'Google Meet',
    'description': 'Discuss project updates.',
    'start': {'dateTime': '2025-02-15T10:00:00+05:30', 'timeZone': 'Asia/Kolkata'},
    'end': {'dateTime': '2025-02-15T11:00:00+05:30', 'timeZone': 'Asia/Kolkata'},
    'attendees': [{'email': 'client@example.com'}],
    'reminders': {'useDefault': True},
}

event_result = service.events().insert(
    calendarId='primary', body=event).execute()
print(f"Event created: {event_result.get('htmlLink')}")

events_result = service.events().list(calendarId='primary', maxResults=20,
                                      singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items')

for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(f"{start} - {event['summary']}")
