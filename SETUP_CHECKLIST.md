# Quick Checklist: Complete the OAuth 2.0 Setup

## What I've Done ✅
- [x] Reviewed official Google Calendar API documentation
- [x] Identified root cause: service accounts can't access personal calendars
- [x] Designed solution: OAuth 2.0 with user credentials
- [x] Updated `scripts/update_calendar.py` for OAuth 2.0
- [x] Created `scripts/get_oauth_token.py` for setup
- [x] Updated `.github/workflows/update-calendar.yml`
- [x] Created 6 comprehensive documentation files
- [x] Verified no syntax errors
- [x] Ready for deployment

## What You Need to Do 📋

### Phase 1: Local Setup (15 minutes)

- [ ] **1.1** Go to https://console.cloud.google.com/apis/credentials
- [ ] **1.2** Create OAuth 2.0 Client ID (Desktop application)
- [ ] **1.3** Download JSON and save as `credentials.json` in project root
- [ ] **1.4** Verify file exists: `ls -la credentials.json`
- [ ] **1.5** Run: `python3 scripts/get_oauth_token.py`
- [ ] **1.6** Copy the refresh token (long string)
- [ ] **1.7** Test locally:
  ```bash
  export GOOGLE_CALENDAR_REFRESH_TOKEN="your-token-here"
  python3 scripts/update_calendar.py
  ```
- [ ] **1.8** Verify output shows your calendar events

### Phase 2: GitHub Setup (5 minutes)

- [ ] **2.1** Go to https://github.com/ldalboel/trmnlweather/settings/secrets/actions
- [ ] **2.2** Add secret: `GOOGLE_CALENDAR_REFRESH_TOKEN` = [your token]
- [ ] **2.3** Add secret: `GOOGLE_CLIENT_ID` = [from credentials.json]
- [ ] **2.4** Add secret: `GOOGLE_CLIENT_SECRET` = [from credentials.json]
- [ ] **2.5** Verify all 3 secrets are listed

### Phase 3: Deployment (2 minutes)

- [ ] **3.1** Add updated files to git:
  ```bash
  git add scripts/update_calendar.py
  git add scripts/get_oauth_token.py
  git add .github/workflows/update-calendar.yml
  git add .gitignore
  ```
- [ ] **3.2** Commit: `git commit -m "Update Google Calendar integration to use OAuth 2.0"`
- [ ] **3.3** Push: `git push origin main`
- [ ] **3.4** Go to GitHub Actions tab
- [ ] **3.5** Watch "Update Calendar" workflow run
- [ ] **3.6** Verify it completes successfully ✓

### Phase 4: Verification (5 minutes)

- [ ] **4.1** Check GitHub: https://github.com/ldalboel/trmnlweather
- [ ] **4.2** View `public/calendar.json` in browser
- [ ] **4.3** Verify it contains your upcoming events
- [ ] **4.4** Test calendar display on TRMNL device (if available)
- [ ] **4.5** Celebrate! 🎉

---

## Estimated Time
- Phase 1: 15 minutes
- Phase 2: 5 minutes
- Phase 3: 2 minutes
- Phase 4: 5 minutes
- **Total: ~27 minutes**

---

## Troubleshooting Quick Fixes

**If local test fails:**
```bash
# Check environment variable is set
echo $GOOGLE_CALENDAR_REFRESH_TOKEN

# Re-run token generation
python3 scripts/get_oauth_token.py

# Check credentials.json exists
cat credentials.json | head -5
```

**If GitHub Actions fails:**
- Check workflow logs for specific error
- Verify all 3 secrets are added to GitHub
- Try running locally first to verify setup works
- Check that secrets don't have extra spaces/newlines

**If calendar.json is empty:**
- Verify refresh token is still valid
- Re-run local test: `python3 scripts/update_calendar.py`
- Check that you have events in your Google Calendar

---

## Key Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `scripts/get_oauth_token.py` | Generate refresh token | Created ✅ |
| `scripts/update_calendar.py` | Fetch calendar events | Updated ✅ |
| `.github/workflows/update-calendar.yml` | GitHub Actions workflow | Updated ✅ |
| `NEXT_STEPS.md` | Detailed setup guide | Created ✅ |
| `API_REVIEW_SUMMARY.md` | Overview of changes | Created ✅ |
| `credentials.json` | OAuth Client ID (you download) | Pending |
| GitHub Secrets | Refresh token + credentials | Pending |

---

## Important Reminders

⚠️ **Don't commit:**
- `credentials.json` (add to .gitignore ✓)
- `token.json` (add to .gitignore ✓)

✅ **Do commit:**
- `scripts/get_oauth_token.py`
- Updated `scripts/update_calendar.py`
- Updated `.github/workflows/update-calendar.yml`

---

## Next Action

👉 **Start:** Go to Google Cloud Console and download OAuth 2.0 Client ID
   https://console.cloud.google.com/apis/credentials

Questions? Check `NEXT_STEPS.md` or the other documentation files.
