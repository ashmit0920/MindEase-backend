import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("EXPO_PUBLIC_GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You are a helpful academic assistant that helps students make efficient study schedules. To do this, you need to generate Google Calendar events for the students in JSON format. Include study breaks whenever required.\nDO NOT write any explanations or suggestions, only generate the json objects divided across the time duration asked by the user. Keep the timezone unchanged in the sample below.\n\nUse this sample JSON schema for each event:\n\nEvent = {\n    'summary': 'Summary of the study session',\n    'location': 'location of the event',\n    'description': 'Describe the study session',\n    'start': {'dateTime': '2025-02-15T10:00:00+05:30', 'timeZone': 'Asia/Kolkata'},\n    'end': {'dateTime': '2025-02-15T11:00:00+05:30', 'timeZone': 'Asia/Kolkata'},\n    'attendees': [{'email': 'client@example.com'}],\n    'reminders': {'useDefault': True},\n}\nReturn: list[Event]",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "make a study schedule to help me finish my Maths and Science syllabus, from 5 PM to 8 PM.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "```json\n[\n  {\n    \"summary\": \"Math Study Session\",\n    \"location\": \"Home\",\n    \"description\": \"Focus on Chapter 1 - Algebra\",\n    \"start\": {\n      \"dateTime\": \"2024-07-26T17:00:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"end\": {\n      \"dateTime\": \"2024-07-26T17:50:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"attendees\": [\n      {\n        \"email\": \"client@example.com\"\n      }\n    ],\n    \"reminders\": {\n      \"useDefault\": true\n    }\n  },\n  {\n    \"summary\": \"Break\",\n    \"location\": \"Home\",\n    \"description\": \"Take a 10-minute break to relax.\",\n    \"start\": {\n      \"dateTime\": \"2024-07-26T17:50:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"end\": {\n      \"dateTime\": \"2024-07-26T18:00:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"attendees\": [\n      {\n        \"email\": \"client@example.com\"\n      }\n    ],\n    \"reminders\": {\n      \"useDefault\": true\n    }\n  },\n  {\n    \"summary\": \"Science Study Session\",\n    \"location\": \"Home\",\n    \"description\": \"Focus on Chapter 3 - Physics\",\n    \"start\": {\n      \"dateTime\": \"2024-07-26T18:00:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"end\": {\n      \"dateTime\": \"2024-07-26T18:50:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"attendees\": [\n      {\n        \"email\": \"client@example.com\"\n      }\n    ],\n    \"reminders\": {\n      \"useDefault\": true\n    }\n  },\n  {\n    \"summary\": \"Break\",\n    \"location\": \"Home\",\n    \"description\": \"Take a 10-minute break to relax.\",\n    \"start\": {\n      \"dateTime\": \"2024-07-26T18:50:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"end\": {\n      \"dateTime\": \"2024-07-26T19:00:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"attendees\": [\n      {\n        \"email\": \"client@example.com\"\n      }\n    ],\n    \"reminders\": {\n      \"useDefault\": true\n    }\n  },\n  {\n    \"summary\": \"Maths - Practice Problems\",\n    \"location\": \"Home\",\n    \"description\": \"Solve practice problems for Algebra\",\n    \"start\": {\n      \"dateTime\": \"2024-07-26T19:00:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"end\": {\n      \"dateTime\": \"2024-07-26T20:00:00+05:30\",\n      \"timeZone\": \"Asia/Kolkata\"\n    },\n    \"attendees\": [\n      {\n        \"email\": \"client@example.com\"\n      }\n    ],\n    \"reminders\": {\n      \"useDefault\": true\n    }\n  }\n]\n```",
            ],
        },
    ]
)

response = chat_session.send_message(
    "make the schedule for 4 hours instead, giving me 2 hours for each subject")

print(response.text)
