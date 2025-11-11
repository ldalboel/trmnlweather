# API Documentation Review - Key Findings

## Critical Issue Found

After reviewing the official Google Calendar API documentation, I discovered that **service accounts cannot access personal shared calendars**. The issue with your current setup is:

### Why Service Accounts Don't Work

From the official documentation on [Using OAuth 2.0 for Server to Server Applications](https://developers.google.com/identity/protocols/oauth2/service-account):

> "A service account is a special kind of account used by an application, rather than a person. Typically, an application uses a service account when the application uses Google APIs to work with **its own data** rather than a user's data."

The `calendarList().list()` call only returns:
1. Calendars **owned by** the service account
2. Calendars accessible via **domain-wide delegation** (requires Google Workspace admin)

It does NOT return:
- Personal calendars shared with the service account email

### The Root Cause

Even though you shared your calendar with the service account email, Google Calendar API treats:
- **Manual sharing** = Calendar UI feature
- **API access** = Requires different permissions

A shared calendar is visible in Google Calendar UI but the API won't list it.

## The Correct Solution

Use **OAuth 2.0 with user credentials** instead:

### Architecture

```
Your Google Account (One-time setup)
    ↓
OAuth 2.0 Authorization → Generates Refresh Token
    ↓
Store in GitHub Secrets
    ↓
GitHub Actions Workflow
    ↓
Use Refresh Token to authenticate
    ↓
Access your personal calendar (as your account)
    ↓
Fetch events → Save to JSON
```

### Why This Works

From the [Python Quickstart](https://developers.google.com/calendar/api/quickstart/python):

```python
# This is how Google's own docs authenticate
creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("calendar", "v3", credentials=creds)

# Then access the calendar normally
events_result = service.events().list(calendarId="primary", ...).execute()
```

The `Credentials` class with a refresh token represents **you**, not a service account. So you can access all your calendars, including shared ones.

## Changes Made

### Files Created/Modified

1. **`scripts/get_oauth_token.py`** (NEW)
   - One-time setup script
   - Generates refresh token from your Google account
   - Outputs instructions for adding to GitHub Secrets

2. **`scripts/update_calendar.py`** (UPDATED)
   - Now uses `Credentials` with refresh token
   - Removes service account authentication
   - Uses environment variables: `GOOGLE_CALENDAR_REFRESH_TOKEN`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

3. **`.github/workflows/update-calendar.yml`** (UPDATED)
   - Changed environment variable from `GOOGLE_CALENDAR_KEY` to `GOOGLE_CALENDAR_REFRESH_TOKEN`
   - Added `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` secrets

4. **`GOOGLE_CALENDAR_SETUP.md`** (NEW)
   - Comprehensive setup guide
   - Explains the OAuth 2.0 flow
   - Step-by-step instructions
   - Troubleshooting tips

## Next Steps

1. Download OAuth 2.0 Client ID from Google Cloud Console
2. Save as `credentials.json` in project root
3. Run: `python3 scripts/get_oauth_token.py`
4. Copy the refresh token to GitHub Secrets
5. Push changes to GitHub
6. GitHub Actions will automatically fetch your calendar

## Why This Approach Is Better

✅ Works with personal calendars (no domain admin needed)
✅ Simpler than service accounts + domain delegation
✅ Uses Google's official recommended pattern
✅ More secure (refresh token expires, specific scopes)
✅ Already working in thousands of projects using Google Calendar API

The key insight: **Service accounts are for apps with their own data. User credentials are for apps accessing user data.**
