# Google Calendar Integration Setup

## Summary
This setup fetches your private Google Calendar events and displays them on your weather page using GitHub Actions and a service account.

## Files Created
- `.github/workflows/update-calendar.yml` - GitHub Actions workflow that runs every 6 hours
- `scripts/update_calendar.py` - Python script to fetch calendar events
- `public/calendar.json` - Generated file with calendar events (auto-updated)

## Setup Instructions

### 1. Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or use existing
3. Enable Google Calendar API
4. Create Service Account:
   - Credentials → Create Credentials → Service Account
   - Name: `trmnlweather-calendar`
   - Create and skip optional steps
5. Generate JSON key:
   - Click service account
   - Keys → Add Key → Create new key (JSON format)
   - Save the `key.json` file

### 2. Share Calendar with Service Account
1. From the JSON key file, copy the `client_email`
2. Open Google Calendar settings
3. Go to your calendar's sharing settings
4. Share with the service account email
5. Give "See all event details" permission

### 3. GitHub Secrets
1. Go to your repo → Settings → Secrets and variables → Actions
2. New repository secret:
   - Name: `GOOGLE_CALENDAR_KEY`
   - Value: Paste entire contents of `key.json`

### 4. Test It
1. Go to your repo's Actions tab
2. Find "Update Calendar" workflow
3. Click "Run workflow"
4. Wait for it to complete
5. Check `public/calendar.json` was created with your events

### 5. Deploy
Push all changes to GitHub and enable GitHub Pages if not already enabled.

## How It Works
- **Trigger**: Every 6 hours (configurable in `.github/workflows/update-calendar.yml`)
- **Process**: GitHub Actions runs the Python script with your service account credentials
- **Output**: Generates `public/calendar.json` with the next 30 days of events
- **Display**: Your page loads and displays the next 5 upcoming events

## Customization

### Change Update Frequency
Edit `.github/workflows/update-calendar.yml` and change the cron schedule:
```yaml
- cron: '0 */6 * * *'  # Every 6 hours
- cron: '0 * * * *'    # Every hour
- cron: '0 0 * * *'    # Daily at midnight
```

### Change Calendar
Edit `scripts/update_calendar.py` and change:
```python
calendar_id = 'primary'  # Your calendar ID
```

### Show More/Fewer Events
Edit `index.html` in the `displayCalendarEvents` function:
```javascript
for (let i = 0; i < Math.min(5, events.length); i++) {
    // Change 5 to show more or fewer events
}
```

## Troubleshooting

**Calendar not showing?**
- Check Actions tab for workflow errors
- Verify service account has calendar access
- Check that calendar.json was created in `public/`

**"Calendar file not found"?**
- Run the workflow manually from Actions tab
- Wait for it to complete

**Events not updating?**
- The workflow runs every 6 hours
- Manually trigger from Actions tab for immediate update

