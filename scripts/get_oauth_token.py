#!/usr/bin/env python3
"""
Generate an OAuth 2.0 refresh token for Google Calendar.
Run this ONCE locally to generate a token, then save the refresh_token to GitHub secrets.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# You need to download a "Desktop app" OAuth client ID from Google Cloud Console
# https://console.cloud.google.com/apis/credentials
# Then save it as credentials.json in this directory

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_oauth_token():
    """Get OAuth 2.0 refresh token for Calendar access."""
    
    if not os.path.exists('credentials.json'):
        print("ERROR: credentials.json not found!")
        print("\nTo fix this:")
        print("1. Go to https://console.cloud.google.com/apis/credentials")
        print("2. Create a new 'Desktop application' OAuth 2.0 Client ID")
        print("3. Download the JSON and save it as 'credentials.json' in this directory")
        return None
    
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )
    
    creds = flow.run_local_server(port=0)
    
    # Extract the refresh token
    refresh_token = creds.refresh_token
    
    print("\n" + "="*60)
    print("SUCCESS! Here is your refresh token:")
    print("="*60)
    print(refresh_token)
    print("="*60)
    print("\nNow add this to GitHub Secrets:")
    print("1. Go to https://github.com/ldalboel/trmnlweather/settings/secrets/actions")
    print("2. Create a new secret named: GOOGLE_CALENDAR_REFRESH_TOKEN")
    print("3. Paste the token above as the value")
    print("4. Save")
    print("\nThen the GitHub Actions workflow will use it automatically!")
    
    return refresh_token

if __name__ == '__main__':
    get_oauth_token()
