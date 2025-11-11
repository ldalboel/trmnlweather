#!/usr/bin/env python3
"""
Fetch Google Calendar events and save to JSON file.
"""

import json
import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Get the service account key from environment
KEY_JSON = os.environ.get('GOOGLE_CALENDAR_KEY')

if not KEY_JSON:
    print("Error: GOOGLE_CALENDAR_KEY environment variable not set")
    exit(1)

# Parse the key
key_dict = json.loads(KEY_JSON)

# Set up authentication
credentials = service_account.Credentials.from_service_account_info(
    key_dict,
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)

# Create the Calendar API client
service = build('calendar', 'v3', credentials=credentials)

# Try to get calendar list to see what calendars are accessible
print("Available calendars:")
try:
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])
    for cal in calendars:
        print(f"  - {cal['summary']} ({cal['id']})")
    
    if not calendars:
        print("  No calendars found! Make sure you shared your calendar with the service account.")
        exit(1)
    
    # Use the first calendar found (usually the primary one)
    calendar_id = calendars[0]['id']
    print(f"\nUsing calendar: {calendar_id}")
except Exception as e:
    print(f"Error listing calendars: {e}")
    exit(1)

# Time range: today to 30 days from now
now = datetime.utcnow()
time_min = now.isoformat() + 'Z'
time_max = (now + timedelta(days=30)).isoformat() + 'Z'

print(f"Fetching events from {time_min} to {time_max}")

try:
    # Fetch events
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime',
        maxResults=50
    ).execute()
    
    events = events_result.get('items', [])
    
    print(f"Found {len(events)} events")
    
    # Process events into a simpler format
    calendar_data = {
        'updated': now.isoformat(),
        'events': []
    }
    
    for event in events:
        start = event['start'].get('dateTime') or event['start'].get('date')
        end = event['end'].get('dateTime') or event['end'].get('date')
        
        event_obj = {
            'title': event.get('summary', 'Untitled'),
            'start': start,
            'end': end,
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'all_day': 'dateTime' not in event['start']
        }
        
        calendar_data['events'].append(event_obj)
    
    # Ensure output directory exists
    os.makedirs('public', exist_ok=True)
    
    # Write to JSON file
    with open('public/calendar.json', 'w') as f:
        json.dump(calendar_data, f, indent=2)
    
    print(f"Successfully saved {len(events)} events to public/calendar.json")
    
except Exception as e:
    print(f"Error fetching calendar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

