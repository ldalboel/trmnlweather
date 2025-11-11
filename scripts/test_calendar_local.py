#!/usr/bin/env python3
"""
Local test script for Google Calendar integration.
Run this locally to test before deploying to GitHub Actions.

Usage:
  1. Set your Google service account JSON path:
     export GOOGLE_CALENDAR_KEY_FILE="/path/to/your/key.json"
  
  2. Run this script:
     python scripts/test_calendar_local.py
"""

import json
import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    # Get the service account key file path
    key_file = os.environ.get('GOOGLE_CALENDAR_KEY_FILE')
    
    if not key_file:
        print("ERROR: GOOGLE_CALENDAR_KEY_FILE environment variable not set")
        print("\nUsage:")
        print('  export GOOGLE_CALENDAR_KEY_FILE="/path/to/your/key.json"')
        print("  python scripts/test_calendar_local.py")
        exit(1)
    
    if not os.path.exists(key_file):
        print(f"ERROR: Key file not found: {key_file}")
        exit(1)
    
    print(f"Reading key file: {key_file}")
    
    try:
        with open(key_file) as f:
            key_dict = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read key file: {e}")
        exit(1)
    
    print(f"✓ Loaded key file")
    print(f"  Service account email: {key_dict.get('client_email')}")
    print(f"  Project ID: {key_dict.get('project_id')}")
    
    # Set up authentication
    try:
        credentials = service_account.Credentials.from_service_account_info(
            key_dict,
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        print(f"✓ Created credentials")
    except Exception as e:
        print(f"ERROR: Failed to create credentials: {e}")
        exit(1)
    
    # Create the Calendar API client
    try:
        service = build('calendar', 'v3', credentials=credentials)
        print(f"✓ Connected to Google Calendar API")
    except Exception as e:
        print(f"ERROR: Failed to connect to Calendar API: {e}")
        exit(1)
    
    # Try to get calendar list
    print(f"\n=== Checking calendar access ===")
    try:
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        print(f"DEBUG: Raw response: {json.dumps(calendar_list, indent=2, default=str)}")
        
        if not calendars:
            print("\n❌ ERROR: No calendars found!")
            print("\nDEBUG INFO:")
            print(f"  Service account: {key_dict.get('client_email')}")
            print(f"  Response keys: {calendar_list.keys()}")
            print(f"  Items: {calendar_list.get('items')}")
            print("\nACTION REQUIRED:")
            print(f"  1. Open Google Calendar: https://calendar.google.com/calendar/")
            print(f"  2. Find your calendar in the left sidebar")
            print(f"  3. Click the 3 dots next to it → Settings")
            print(f"  4. Go to 'Share with specific people'")
            print(f"  5. Add this email: {key_dict.get('client_email')}")
            print(f"  6. Give it 'See all event details' permission")
            print(f"\nWait 5-10 minutes for permissions to sync, then try again.")
            exit(1)
            exit(1)
        
        print(f"\n✓ Found {len(calendars)} calendar(s):")
        for i, cal in enumerate(calendars):
            primary = " (PRIMARY)" if cal.get('primary') else ""
            print(f"  {i+1}. {cal.get('summary', 'Unnamed')}{primary}")
            print(f"     ID: {cal['id']}")
        
        calendar_id = calendars[0]['id']
        print(f"\n✓ Using calendar: {cal.get('summary', 'Unnamed')}")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to list calendars: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    
    # Try to fetch events
    print(f"\n=== Fetching events ===")
    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + timedelta(days=30)).isoformat() + 'Z'
    
    print(f"Time range: {time_min} to {time_max}")
    
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            maxResults=50
        ).execute()
        
        events = events_result.get('items', [])
        print(f"\n✓ Found {len(events)} event(s)")
        
        if events:
            print("\nUpcoming events:")
            for event in events[:5]:  # Show first 5
                start = event['start'].get('dateTime') or event['start'].get('date')
                title = event.get('summary', 'Untitled')
                print(f"  • {title}")
                print(f"    Start: {start}")
        else:
            print("\n(No events in the next 30 days)")
        
        # Create the calendar data structure
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
        
        # Save to local file
        os.makedirs('public', exist_ok=True)
        with open('public/calendar.json', 'w') as f:
            json.dump(calendar_data, f, indent=2)
        
        print(f"\n✓ Saved to public/calendar.json")
        print(f"\n=== SUCCESS ===")
        print(f"Your calendar is working! 🎉")
        print(f"\nNext steps:")
        print(f"  1. Commit these changes: git add . && git commit -m 'Add calendar'")
        print(f"  2. Push to GitHub: git push")
        print(f"  3. GitHub Actions will run automatically every 6 hours")
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to fetch events: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()
