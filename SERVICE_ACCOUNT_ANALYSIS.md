# Quick Reference: Service Accounts vs OAuth 2.0 for Calendar

## Key Insight from Official Docs

**Service Accounts** = For apps with their own data
**OAuth 2.0 + User Credentials** = For apps accessing user data

## Service Account Limitations

❌ Cannot access personal calendars via `calendarList().list()`
❌ Cannot impersonate users without domain-wide delegation
❌ Requires Google Workspace admin setup
❌ Returns empty items: `"items": []`

## OAuth 2.0 User Credentials

✅ Direct access to all your personal calendars
✅ Works immediately, no admin setup needed
✅ Recommended by Google's own quickstart
✅ Returns your calendars in `calendarList().list()`
✅ Only requires one-time authorization

## Code Comparison

### Old Approach (Doesn't Work)
```python
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_info(
    key_dict,
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)
# Result: calendarList().list() returns []
```

### New Approach (Works!)
```python
from google.oauth2.credentials import Credentials

creds = Credentials(
    token=None,
    refresh_token=REFRESH_TOKEN,  # From get_oauth_token.py
    token_uri='https://oauth2.googleapis.com/token',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
creds.refresh(Request())
# Result: calendarList().list() returns your calendars
```

## Official Sources

1. **Service Account Docs**: https://developers.google.com/identity/protocols/oauth2/service-account
   - Quote: "service accounts... use Google APIs to work with its own data"

2. **Calendar API Quickstart**: https://developers.google.com/calendar/api/quickstart/python
   - Uses OAuth 2.0 with `Credentials`, not service accounts

3. **Domain-Wide Delegation**: https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority
   - Explicitly says this requires "super administrator of the Google Workspace domain"

## Implementation Status

✅ Updated `scripts/update_calendar.py` to use OAuth 2.0
✅ Created `scripts/get_oauth_token.py` for setup
✅ Updated `.github/workflows/update-calendar.yml`
✅ Created comprehensive setup documentation
✅ Ready for local testing and GitHub deployment
