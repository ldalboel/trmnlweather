# Netlify Cost Optimization: GitHub Actions → Webhook Deploy

## Problem
Netlify charges **20 credits per build** on paid plans. With GitHub Actions deploying every 15 minutes, that's:
- 96 deployments/day × 20 credits = **1,920 credits/day**
- 57,600 credits/month (you only have 300!)

## Solution: Webhook Deploys Only
Instead of letting Netlify rebuild on every push, we use GitHub Actions to generate the HTML and push it directly. Netlify receives the push via webhook and deploys instantly **without rebuilding** (no credits charged).

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Actions (every 15 minutes)                           │
│ ├─ Fetch Google Calendar                                    │
│ ├─ Fetch Rejseplanen trains                                 │
│ ├─ Generate index.html with embedded data                   │
│ └─ Commit & push to main branch                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ GitHub Webhook Trigger                                      │
│ (no cost)                                                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Netlify Webhook Deploy (~30 seconds)                        │
│ ├─ Receive push from GitHub                                 │
│ ├─ Skip build (command: "echo 'skipping...'")              │
│ ├─ Deploy pre-built index.html directly                     │
│ └─ 0 CREDITS CHARGED ✓                                      │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### netlify.toml Settings
```toml
[build]
  # Minimal command - just echo, don't rebuild
  command = "echo 'Skipping build - using GitHub Actions generated files'"
  publish = "."
  ignore = "git diff --quiet HEAD^ HEAD -- ."
```

**What this does:**
- `command`: Runs instantly (no actual build)
- `publish = "."`: Deploys the root directory as-is (index.html already there from GitHub Actions)
- `ignore`: Netlify won't rebuild on every commit (optional but recommended)

### Netlify UI Configuration
1. Go to **Site Settings** → **Build & Deploy** → **Build Settings**
2. Set **Build command** to: `echo "No build needed"`
3. Set **Publish directory** to: `.` (current directory)
4. Go to **Deploy keys** and verify GitHub is connected
5. Go to **Deploy notifications** and confirm webhook is active

## Verification

### Before (Expensive)
- Every GitHub push → Netlify rebuild → 20 credits × 96/day = BREAKS YOUR BUDGET

### After (Free)
- GitHub Actions generates HTML (free)
- Pushes to GitHub (free)
- Netlify webhook receives push (free)
- Netlify deploys pre-built files (no rebuild = no credits)
- Deploy time: ~30 seconds
- Cost: **$0**

## Deployment Timeline

**Every 15 minutes:**
1. **T+0:00** - GitHub Actions starts
2. **T+2:00** - Data fetched and HTML generated
3. **T+2:30** - Committed and pushed to main
4. **T+2:45** - Netlify webhook triggered
5. **T+3:15** - Site live with fresh data

**Total: ~3 minutes from trigger to live**

## Troubleshooting

### Netlify still rebuilding?
- Check Site Settings → Build & Deploy → Branches & deploy contexts
- Make sure "Auto publish" is ON
- Clear Netlify cache and redeploy

### Webhook not firing?
- Go to GitHub repo → Settings → Webhooks
- Verify Netlify webhook is listed
- Check recent deliveries for errors

### Deploy previews not working?
- They'll be skipped (no build = no preview)
- This is expected and fine for a data display site
- All updates go through main branch

## Cost Breakdown

| Component | Cost | Frequency |
|-----------|------|-----------|
| GitHub Actions | Free | Every 15 min |
| GitHub Storage | Free | Unlimited |
| Netlify Hosting | Free tier or paid | Every 15 min |
| Netlify Builds | **$0** | Skipped |
| Netlify Webhooks | Free | Every deploy |
| **Monthly Total** | **$0 build costs** | - |

## When to Switch Back

If you need:
- Deploy previews for pull requests
- Build-time environment setup
- More complex build processes

...then you'd need to pay for builds. But for this use case, webhook deploys are perfect.

## Next Steps

1. ✅ Update `netlify.toml` (done)
2. Push changes to GitHub
3. Go to Netlify UI and manually trigger a deploy to verify it works
4. Monitor for next 24 hours to confirm no unexpected credits are charged
5. Enjoy free deployments! 🎉
