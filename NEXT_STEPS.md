# Next Steps: Complete the Google Calendar Integration

## What's Changed

I've reviewed the official Google API documentation and discovered the root cause of your calendar access issues. **Service accounts fundamentally cannot access personal shared calendars.** The solution is to use OAuth 2.0 with your own Google credentials instead.

### Files Updated

✅ **`scripts/update_calendar.py`** - Now uses OAuth 2.0 instead of service accounts
✅ **`scripts/get_oauth_token.py`** - NEW: One-time setup to generate refresh token
✅ **`.github/workflows/update-calendar.yml`** - Updated to use refresh token secret
✅ **`GOOGLE_CALENDAR_SETUP.md`** - NEW: Complete setup guide
✅ **`API_DOCUMENTATION_REVIEW.md`** - NEW: Explains the API findings
✅ **`SERVICE_ACCOUNT_ANALYSIS.md`** - NEW: Quick reference
✅ **`.gitignore`** - Added credentials and sensitive files

## Action Items (In Order)

### 1. Download OAuth 2.0 Client ID
- Go to https://console.cloud.google.com/apis/credentials
- Create a new **Desktop application** OAuth 2.0 Client ID
- Download the JSON
- Save as `credentials.json` in your project root folder

### 2. Generate Refresh Token (Local)
```bash
# Make sure dependencies are installed
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Run the token generation script
python3 scripts/get_oauth_token.py
```

This will:
1. Open your browser to Google login
2. Request permission to access your calendar
3. Display a refresh token in your terminal

### 3. Test Locally
```bash
export GOOGLE_CALENDAR_REFRESH_TOKEN="paste-your-token-here"
python3 scripts/update_calendar.py
```

You should see:
```
✓ Successfully authenticated with Google Calendar

=== Available calendars ===
1. Your Calendar Name (your-calendar-id@google.com)
   Primary: True

=== Using calendar: your-calendar-id@google.com ===

=== Fetching events ===
Time range: 2025-11-11T... to 2025-12-11T...
Found 5 events
  - Event 1 (2025-11-15T14:00:00+00:00)
  - Event 2 (2025-11-20T09:00:00+00:00)
  ...

✓ Successfully saved 5 events to public/calendar.json
```

### 4. Add Secrets to GitHub
1. Go to https://github.com/ldalboel/trmnlweather/settings/secrets/actions
2. Add three new secrets:
   - **Name:** `GOOGLE_CALENDAR_REFRESH_TOKEN` | **Value:** [paste your token]
   - **Name:** `GOOGLE_CLIENT_ID` | **Value:** [from credentials.json, field: client_id]
   - **Name:** `GOOGLE_CLIENT_SECRET` | **Value:** [from credentials.json, field: client_secret]

### 5. Test on GitHub
Push any change to trigger the workflow:
```bash
git add .
git commit -m "Update Google Calendar integration to use OAuth 2.0"
git push
```

Check the GitHub Actions tab to see if the workflow succeeds. You should see `public/calendar.json` updated with your events.

## Verification Checklist

- [ ] Downloaded OAuth 2.0 Client ID as `credentials.json`
- [ ] Ran `get_oauth_token.py` and got a refresh token
- [ ] Tested locally with `GOOGLE_CALENDAR_REFRESH_TOKEN` env var
- [ ] Saw your calendar events printed successfully
- [ ] Added three secrets to GitHub
- [ ] Pushed changes to GitHub
- [ ] GitHub Actions workflow ran successfully
- [ ] `public/calendar.json` was updated with your events
- [ ] Calendar events display on your weather page

## Troubleshooting

If something doesn't work:

1. **"No calendars found" error locally**
   - Make sure you logged in with the correct Google account
   - Re-run `python3 scripts/get_oauth_token.py`
   - Verify `credentials.json` is in the project root

2. **GitHub Actions fails**
   - Check that all three secrets are added correctly
   - View the workflow run logs for detailed error messages
   - Try running locally first to verify the setup works

3. **Token expired in GitHub Actions**
   - Refresh tokens are valid for 6 months of inactivity
   - Re-run `python3 scripts/get_oauth_token.py` to get a new token
   - Update the secret in GitHub

## Why This Works Now

✅ OAuth 2.0 credentials authenticate **as you**, not a service account
✅ Google Calendar API returns all your calendars (including shared ones)
✅ No Google Workspace admin setup needed
✅ Follows Google's official API documentation and quickstart examples
✅ More secure than service accounts for personal use

---

**Ready to proceed?** Start with step 1: Download the OAuth 2.0 Client ID from Google Cloud Console.
