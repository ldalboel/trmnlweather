#!/usr/bin/env python3
"""
Simplified debug script to check calendar access step by step.
"""

import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

key_file = "./trmnlweather-2d51705b25ee.json"

print("Step 1: Loading key file...")
with open(key_file) as f:
    key_dict = json.load(f)
print(f"✓ Service account: {key_dict.get('client_email')}")

print("\nStep 2: Creating credentials...")
credentials = service_account.Credentials.from_service_account_info(
    key_dict,
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)
print("✓ Credentials created")

print("\nStep 3: Building Calendar API client...")
service = build('calendar', 'v3', credentials=credentials)
print("✓ Calendar API client built")

print("\nStep 4: Listing calendars...")
try:
    result = service.calendarList().list().execute()
    print(f"✓ API call successful")
    print(f"  Response: {json.dumps(result, indent=2)}")
    
    items = result.get('items', [])
    print(f"\n  Found {len(items)} calendars")
    
    if len(items) == 0:
        print("\n❌ PROBLEM: Service account has no calendars!")
        print("\nPossible causes:")
        print("  1. Calendar not shared with service account")
        print("  2. Shared with wrong email address")
        print("  3. Permissions haven't synced yet (wait 5-10 min)")
        print("  4. Shared as 'Free/busy' instead of 'See all event details'")
        
        print(f"\n📝 Make sure you shared your calendar with:")
        print(f"   {key_dict.get('client_email')}")
        print("\n   And gave it 'See all event details' permission")
    else:
        print("\n✓ SUCCESS! Service account has access to calendars:")
        for item in items:
            print(f"  - {item.get('summary')} ({item['id']})")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
