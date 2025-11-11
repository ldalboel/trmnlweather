#!/usr/bin/env python3
"""
Fetch Google Calendar events and save to JSON file.
Uses OAuth 2.0 user credentials instead of service accounts.
"""

import json
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Get the refresh token from environment
REFRESH_TOKEN = os.environ.get('GOOGLE_CALENDAR_REFRESH_TOKEN')
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

if not REFRESH_TOKEN:
    print("Error: GOOGLE_CALENDAR_REFRESH_TOKEN environment variable not set")
    print("Run: python3 scripts/get_oauth_token.py")
    exit(1)

if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables not set")
    print("These should be set as GitHub Secrets or environment variables")
    exit(1)

try:
    # Create credentials from refresh token
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    
    # Refresh to get a valid access token
    creds.refresh(Request())
    print(f"✓ Successfully authenticated with Google Calendar")
    
except Exception as e:
    print(f"Error authenticating: {e}")
    print("Make sure GOOGLE_CALENDAR_REFRESH_TOKEN is set correctly")
    exit(1)

# Create the Calendar API client
service = build('calendar', 'v3', credentials=creds)

# Try to get calendar list to see what calendars are accessible
print("\n=== Available calendars ===")
try:
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])
    
    if not calendars:
        print("ERROR: No calendars found!")
        print("This usually means the GOOGLE_CALENDAR_REFRESH_TOKEN is invalid or expired.")
        print("Run: python3 scripts/get_oauth_token.py")
        # Create empty calendar.json and exit
        os.makedirs('public', exist_ok=True)
        with open('public/calendar.json', 'w') as f:
            json.dump({'updated': datetime.utcnow().isoformat(), 'events': []}, f)
        exit(1)
    else:
        for i, cal in enumerate(calendars):
            print(f"{i+1}. {cal.get('summary', 'Unnamed')} ({cal['id']})")
            print(f"   Primary: {cal.get('primary', False)}")
    
    # Use the primary calendar (your main calendar)
    primary_cal = None
    for cal in calendars:
        if cal.get('primary', False):
            primary_cal = cal
            break
    
    if primary_cal:
        calendar_id = primary_cal['id']
        print(f"\n=== Using primary calendar: {primary_cal.get('summary', 'Unnamed')} ({calendar_id}) ===")
    else:
        # Fallback to first calendar if no primary found
        calendar_id = calendars[0]['id']
        print(f"\n=== Using calendar: {calendars[0].get('summary', 'Unnamed')} ({calendar_id}) ===")
    
except Exception as e:
    print(f"Error listing calendars: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Time range: today to 30 days from now
now = datetime.utcnow()
time_min = now.isoformat() + 'Z'
time_max = (now + timedelta(days=30)).isoformat() + 'Z'

print(f"\n=== Fetching events ===")
print(f"Time range: {time_min} to {time_max}")

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
        print(f"  - {event_obj['title']} ({start})")
    
    # Ensure output directory exists
    os.makedirs('public', exist_ok=True)
    
    # Write to JSON file
    with open('public/calendar.json', 'w') as f:
        json.dump(calendar_data, f, indent=2)
    
    print(f"\n✓ Successfully saved {len(events)} events to public/calendar.json")
    
except Exception as e:
    print(f"\n✗ Error fetching calendar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)


