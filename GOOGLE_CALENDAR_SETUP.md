# Google Calendar Integration - Correct Setup

## The Problem with Service Accounts

After reviewing the official Google Calendar API documentation, I discovered that **service accounts cannot directly access shared personal calendars**. The service account approach only works with:

1. **Domain-Wide Delegation** (requires Google Workspace admin setup)
2. **Calendars owned by the service account** itself

Simply sharing a personal calendar with a service account email doesn't grant API access.

## The Solution: OAuth 2.0 User Credentials

Instead, we use **your own Google account credentials** with OAuth 2.0:

1. You authorize once locally (generates a refresh token)
2. Store the refresh token securely in GitHub Secrets
3. GitHub Actions uses the refresh token to fetch your calendar

**This is simpler and actually works!**

## Setup Steps

### Step 1: Create an OAuth 2.0 Client ID

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth 2.0 Client ID**
5. Choose **Desktop application**
6. Name it (e.g., "TRMNL Weather Calendar")
7. Click **Create**
8. Download the JSON file and save it as `credentials.json` in your project root

### Step 2: Generate Refresh Token Locally

```bash
# Make sure you have the packages installed
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Run the token generation script
python3 scripts/get_oauth_token.py
```

This will:
1. Open your browser to Google login
2. Ask for permission to access your calendar
3. Display your refresh token in the terminal

### Step 3: Add Refresh Token to GitHub Secrets

1. Go to your GitHub repo: https://github.com/ldalboel/trmnlweather/settings/secrets/actions
2. Click **New repository secret**
3. Name: `GOOGLE_CALENDAR_REFRESH_TOKEN`
4. Value: Paste the refresh token from Step 2
5. Click **Add secret**

### Step 4: Update GitHub Actions Workflow

In `.github/workflows/update-calendar.yml`, replace the old service account secret with the refresh token:

```yaml
env:
  GOOGLE_CALENDAR_REFRESH_TOKEN: ${{ secrets.GOOGLE_CALENDAR_REFRESH_TOKEN }}
```

### Step 5: Deploy

Push your changes to GitHub. The workflow will now:
1. Use your refresh token to authenticate
2. Access your personal calendar
3. Fetch events for the next 30 days
4. Save to `public/calendar.json`

## Testing Locally

Before deploying to GitHub:

```bash
export GOOGLE_CALENDAR_REFRESH_TOKEN="your-refresh-token-here"
python3 scripts/update_calendar.py
```

You should see your calendar events printed and saved to `public/calendar.json`.

## Troubleshooting

### "Error: credentials.json not found"
- Download the OAuth 2.0 Client ID JSON from Google Cloud Console
- Save it as `credentials.json` in your project root

### "No calendars found" in GitHub Actions
- Make sure the refresh token was generated with the correct Google account
- Verify the token is correctly set in GitHub Secrets
- Run locally to test: `GOOGLE_CALENDAR_REFRESH_TOKEN=<token> python3 scripts/update_calendar.py`

### Token expired
- Refresh tokens expire after 6 months of inactivity
- Run the script at least every 6 months to refresh, or regenerate: `python3 scripts/get_oauth_token.py`

## Security Notes

- **Never commit `credentials.json`** to Git - add it to `.gitignore`
- Keep your refresh token secret (only in GitHub Secrets)
- The token only grants calendar.readonly access

## References

- [Google Calendar API Python Quickstart](https://developers.google.com/calendar/api/quickstart/python)
- [OAuth 2.0 for Server-to-Server Applications](https://developers.google.com/identity/protocols/oauth2/service-account)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
