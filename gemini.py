from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, TypeAdapter

load_dotenv()
GEMINI_KEY = os.getenv("EXPO_PUBLIC_GEMINI_KEY")


# class CalendarEvent(BaseModel):
#     summary: str
#     location: str
#     description: str
#     start: dict
#     end: dict
#     attendees: list[dict]
#     reminders: dict


prompt = """I want to make an efficient study schedule spread across 3 hours, from 5 PM to 8 PM. Generate a Google Calendar event for it in JSON format.
DO NOT write any explanations or suggestions, only generate the json objects divided across these 3 hours. Keep the timezone unchanged in the sample below.

Use this sample JSON schema for each event:

Event = {
    'summary': 'Summary of the study session',
    'location': 'location of the event',
    'description': 'Describe the study session',
    'start': {'dateTime': '2025-02-15T10:00:00+05:30', 'timeZone': 'Asia/Kolkata'},
    'end': {'dateTime': '2025-02-15T11:00:00+05:30', 'timeZone': 'Asia/Kolkata'},
    'attendees': [{'email': 'client@example.com'}],
    'reminders': {'useDefault': True},
}
Return: list[Event]"""

client = genai.Client(api_key=GEMINI_KEY)
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
)

event = response.text
print(event)
