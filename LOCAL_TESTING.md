# Local Calendar Testing Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Set Your Key File Path
```bash
export GOOGLE_CALENDAR_KEY_FILE="/path/to/your/key.json"
```

Replace `/path/to/your/key.json` with the actual path to your service account JSON file.

### 3. Run the Test Script
```bash
python scripts/test_calendar_local.py
```

### What to Expect

#### If it works ✓
```
✓ Loaded key file
  Service account email: xxx@xxx.iam.gserviceaccount.com
  Project ID: my-project
✓ Connected to Google Calendar API

=== Checking calendar access ===
✓ Found 1 calendar(s):
  1. Calendar Name (PRIMARY)
     ID: xxx@group.calendar.google.com

✓ Using calendar: Calendar Name

=== Fetching events ===
✓ Found 5 event(s)

Upcoming events:
  • Team Meeting
    Start: 2025-11-12T14:00:00Z
  • Project Review
    Start: 2025-11-13T10:00:00Z

✓ Saved to public/calendar.json

=== SUCCESS ===
```

#### If it fails with "No calendars found"
```
❌ ERROR: No calendars found!

ACTION REQUIRED:
  1. Open Google Calendar: https://calendar.google.com/calendar/
  2. Find your calendar in the left sidebar
  3. Click the 3 dots next to it → Settings
  4. Go to 'Share with specific people'
  5. Add this email: xxx@xxx.iam.gserviceaccount.com
  6. Give it 'See all event details' permission
```

**Solution**: Share your calendar with the service account email shown above.

#### If it fails with other errors
Check these common issues:
- Wrong key.json file path
- Service account doesn't have Calendar API enabled in Google Cloud
- Missing dependencies (run pip install again)

### 4. Once It Works

If the test script succeeds:
1. `public/calendar.json` will be created with your events
2. Your local page can load it and display events
3. Push to GitHub and the Actions workflow will do the same automatically

### Troubleshooting

**Q: "Import could not be resolved"**
A: You need to install dependencies:
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Q: "Key file not found"**
A: Make sure the path is correct:
```bash
# Find your key.json file
find ~ -name "key.json" 2>/dev/null
# Then set it
export GOOGLE_CALENDAR_KEY_FILE="/full/path/to/key.json"
```

**Q: "No calendars found"**
A: You need to share your Google Calendar with the service account.
The script will show you the email to use.

**Q: Still getting 0 events after sharing?**
A: Wait a few minutes for Google to sync permissions, then try again.

