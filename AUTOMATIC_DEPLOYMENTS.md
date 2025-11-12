# Automatic Deployment Pipeline with Netlify

## How It Works

You already have a complete automated pipeline set up! Here's the flow:

### The Pipeline:

```
GitHub Actions (Every 15 minutes)
    ↓
Fetch calendar.json from Google Calendar
    ↓
Fetch trains-data.js from Rejseplanen
    ↓
Generate updated index.html
    ↓
If data changed:
  - Commit changes
  - Push to GitHub main branch
    ↓
Netlify GitHub webhook triggered
    ↓
Deploy new version (~30 seconds)
    ↓
Live on https://trmnlweather.netlify.app ✅
```

---

## Update Frequency

### Current Schedule (from `.github/workflows/update-calendar.yml`):
```
Runs every 15 minutes at: :00, :15, :30, :45 (every hour)
```

### What updates:
- ✅ **Calendar events** (from Google Calendar)
- ✅ **Train/bus departures** (from Rejseplanen)
- ✅ **index.html** (with embedded latest data)

### What triggers Netlify deployment:
Only if data actually **changed** (smart commit logic):
```bash
git diff --quiet && git diff --staged --quiet || \
  (git commit -m "Update..." && git push)
```

This means:
- **No push** = No unnecessary deploy
- **Data changed** = Automatic commit + push → Netlify deploys

---

## Timeline Example

**11:00** - GitHub Action runs
- Fetches latest calendar & trains
- No changes detected
- No commit, no deploy ✅ (efficient)

**11:15** - GitHub Action runs
- Fetches latest calendar & trains
- New train departure added!
- Commits to GitHub
- Pushes to main
- Netlify detects push
- Deploys new version in ~30 seconds
- Your TRMNL sees update! ✅

---

## Configuration

### Current Settings:

**File:** `.github/workflows/update-calendar.yml`

```yaml
on:
  schedule:
    # Every 15 minutes
    - cron: '0,15,30,45 * * * *'
  workflow_dispatch:  # Can also trigger manually
```

### Change Update Frequency (if desired):

Edit the cron expression:

```yaml
# Every 15 minutes (current)
cron: '0,15,30,45 * * * *'

# Every 5 minutes (more frequent)
cron: '*/5 * * * *'

# Every 30 minutes (less frequent)
cron: '0,30 * * * *'

# Every hour at :00
cron: '0 * * * *'

# Every 2 hours
cron: '0 */2 * * *'
```

---

## Netlify Integration Steps

When you connect to Netlify:

1. **Netlify watches your GitHub repo**
2. **Any push to main triggers auto-deploy**
3. **Your GitHub Actions pushes data updates**
4. **Netlify automatically deploys updated data**

### No extra configuration needed!

Netlify automatically:
- Detects GitHub pushes
- Builds (runs `echo 'Static site'`)
- Deploys to CDN
- Serves with cache headers (`max-age=0`)

---

## What You Get

### Update Frequency:
- Calendar events: Every 15 minutes (automatic)
- Train departures: Every 15 minutes (automatic)
- TRMNL sees updates: ~5-10 minutes after data changes
  - 5 min = GitHub Action detection + fetch
  - 2 min = Deploy delay (only if data changed)

### No Manual Action Required:
- ✅ No manual git commits
- ✅ No manual pushes
- ✅ No manual Netlify redeploys
- ✅ Everything is automatic!

### Efficiency:
- ✅ Commits only when data actually changes
- ✅ No pointless deployments
- ✅ Smart detection of what changed

---

## Monitoring

### View GitHub Actions Runs:
1. Go to your GitHub repo
2. Click "Actions" tab
3. See all runs: calendar updates, deployments, etc.
4. Click any run to see logs

### View Netlify Deployments:
1. Go to https://app.netlify.app
2. Select your site
3. Click "Deploys" tab
4. See deployment history and logs

### Current Status:
The two workflows you have:
- `update-calendar.yml` - Set A (every 15 min at :00, :15, :30, :45)
- `update-calendar-b.yml` - Set B (probably staggered)
- `deploy.yml` - Manual deploy trigger

---

## Testing

### Manually Trigger Update:
```bash
# Or just go to GitHub Actions and click "Run workflow"
# This will force an immediate run without waiting for schedule
```

Steps:
1. Go to GitHub repo
2. Click "Actions" tab
3. Select "Update Calendar and Trains (Set A)"
4. Click "Run workflow"
5. Wait ~5 minutes
6. Check Netlify for deployment

---

## What Happens Every 15 Minutes

```python
# 1. Fetch latest from Google Calendar
calendar_events = fetch_google_calendar()

# 2. Fetch latest from Rejseplanen
train_departures = fetch_rejseplanen()

# 3. Embed in HTML
html = generate_static_html(calendar_events, train_departures)

# 4. Save files
save(calendar.json, calendar_events)
save(trains-data.js, train_departures)
save(index.html, html)

# 5. Detect changes
if files_changed():
    git_commit("Update calendar events and train departures")
    git_push()  # → Triggers Netlify deploy!
else:
    # No changes, skip deployment (efficient!)
    pass
```

---

## Summary

🎯 **You already have everything set up!**

- ✅ GitHub Actions runs every 15 minutes
- ✅ Fetches calendar and train data
- ✅ Commits if data changed
- ✅ Pushes to GitHub
- ✅ Netlify auto-deploys on push
- ✅ Your site updates automatically

**Just connect to Netlify and you're done!**

No additional configuration needed - it all works together seamlessly.

---

## Next Steps

1. Sign up for Netlify: https://app.netlify.app
2. Connect your GitHub repo
3. Set Netlify site name: `trmnlweather`
4. Update TRMNL device URL to: `https://trmnlweather.netlify.app`
5. Watch your data update every 15 minutes automatically! 🚀
