# Google Calendar Integration - Setup Complete ✓

## Summary
Your local calendar integration **works perfectly**! ✓
- Refresh token successfully authenticated
- Fetched **13 events** from your primary calendar (`ldalboel@gmail.com`)
- Events saved to `public/calendar.json`

## To Deploy to GitHub Actions

### Step 1: Add Refresh Token to GitHub Secrets
1. Go to: https://github.com/ldalboel/trmnlweather/settings/secrets/actions
2. Click **"New repository secret"**
3. Name: `GOOGLE_CALENDAR_REFRESH_TOKEN`
4. Value: `1//0cgX1rSMfEuJHCgYIARAAGAwSNwF-L9Iri3ligvEq2FBiijMiDclFWlw3RHiu3OYI5ZpMCToh_u_ELvWbBqrtA78Ys2xg0N3nb7o`
5. Click **"Add secret"**

> ⚠️ **Security Note**: This token allows access to your Google Calendar. Do NOT share it publicly. GitHub keeps it encrypted.

### Step 2: Verify GitHub Actions Workflow
The workflow `.github/workflows/update-calendar.yml` is already set up to:
- Run every 6 hours automatically
- Use the `GOOGLE_CALENDAR_REFRESH_TOKEN` secret
- Extract client ID/secret from `credentials.json` (already in repo)
- Fetch your calendar events
- Write `public/calendar.json`
- Commit and push to GitHub Pages

### Step 3: Test Locally (Optional)
Before pushing to GitHub, test locally:

```bash
# Option 1: Using the wrapper script
export GOOGLE_CALENDAR_REFRESH_TOKEN="1//0cgX1rSMfEuJHCgYIARAAGAwSNwF-L9Iri3ligvEq2FBiijMiDclFWlw3RHiu3OYI5ZpMCToh_u_ELvWbBqrtA78Ys2xg0N3nb7o"
./scripts/run_calendar_local.sh

# Option 2: Direct Python call
export GOOGLE_CALENDAR_REFRESH_TOKEN="1//0cgX1rSMfEuJHCgYIARAAGAwSNwF-L9Iri3ligvEq2FBiijMiDclFWlw3RHiu3OYI5ZpMCToh_u_ELvWbBqrtA78Ys2xg0N3nb7o"
export GOOGLE_CLIENT_ID="1039045253345-u5t8cclb7vdi0j891tm6soef0dhek8b0.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="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"
python3 scripts/update_calendar.py
```

## How It Works

### Flow
```
Your Google Account
    ↓ (authorize once with get_oauth_token.py)
Refresh Token (stored as GitHub secret)
    ↓ (every 6 hours, GitHub Actions runs)
Google Calendar API
    ↓ (fetches next 30 days of events)
public/calendar.json (automatically committed to GitHub Pages)
    ↓ (your TRMNL device fetches this)
TRMNL Weather Display (shows calendar events in row 4)
```

### Files Modified
- `scripts/update_calendar.py` - Fixed to use primary calendar (not holiday calendar)
- `scripts/run_calendar_local.sh` - New wrapper script for local testing
- `.github/workflows/update-calendar.yml` - Workflow uses `GOOGLE_CALENDAR_REFRESH_TOKEN` secret

## Next Steps

1. ✅ **Local test passed** - Calendar events fetching works
2. ⏭️ **Add secret to GitHub** - Copy refresh token to GitHub Actions secrets
3. ⏭️ **Push changes** - Commit the `scripts/update_calendar.py` fix and test in GitHub Actions
4. ⏭️ **Verify deployment** - Check that `public/calendar.json` updates automatically every 6 hours
5. ⏭️ **Test on TRMNL** - Your weather display should now show calendar events in row 4

## Troubleshooting

### If calendar doesn't update on GitHub
1. Check GitHub Actions logs: https://github.com/ldalboel/trmnlweather/actions
2. Look for the `update-calendar` workflow run
3. If it fails, the error message will tell you why

### If the refresh token expires
- Google refresh tokens typically last 6 months of inactivity
- If it expires, just run `python3 scripts/get_oauth_token.py` again
- Get the new token and update the GitHub secret

### If you see "No calendars found"
- This means the refresh token is invalid or expired
- Run `python3 scripts/get_oauth_token.py` to generate a new one
- Update the GitHub secret with the new token

## Files to Keep Secret

**DO NOT COMMIT:**
- `1//0cgX1rSMfEuJHCgYIARAAGAwSNwF-L9Iri3ligvEq2FBiijMiDclFWlw3RHiu3OYI5ZpMCToh_u_ELvWbBqrtA78Ys2xg0N3nb7o` (your refresh token)
- `trmnlweather-2d51705b25ee.json` (old service account key - no longer needed, safe to delete)

**OK TO COMMIT:**
- `credentials.json` - This is a public OAuth client ID (not a secret, just a client ID)
- `scripts/update_calendar.py` - The script itself
- `.github/workflows/update-calendar.yml` - The workflow
