# Deploying to Netlify

## Quick Setup (5 minutes)

### Step 1: Commit Configuration Files
```bash
cd /Users/lucasdalboel/Documents/GitHub/trmnlweather
git add _headers netlify.toml HOSTING_OPTIONS.md
git commit -m "Add Netlify deployment configuration

- _headers: Set Cache-Control headers to prevent caching
- netlify.toml: Configure build and redirect settings
- Eliminates need for client-side cache-busting workarounds"
git push origin main
```

### Step 2: Connect to Netlify
1. Go to https://app.netlify.com
2. Sign up (free) with GitHub
3. Click "Add new site" → "Import an existing project"
4. Select GitHub provider
5. Authorize GitHub
6. Select your repository: `ldalboel/trmnlweather`
7. Configure build:
   - **Build command:** Leave blank (or `echo 'Static site'`)
   - **Publish directory:** `.` (root)
8. Click "Deploy site"

That's it! 🎉

### Step 3: Access Your Site
Your site will be available at:
```
https://<random-name>.netlify.app
```

Or set a custom subdomain:
1. Go to Site settings → General → Site details
2. Change site name to something like `trmnlweather`
3. New URL: `https://trmnlweather.netlify.app`

### Step 4: Custom Domain (Optional)
1. Go to Site settings → Domain management
2. Click "Add domain"
3. Enter your domain name
4. Update DNS records (Netlify will show you exactly what to do)

---

## What Happens Now

### Auto-Deployment
Every time you push to GitHub:
```bash
git push origin main
```

Netlify automatically:
1. Pulls your latest code
2. Deploys it to their CDN
3. Site updates live in ~30 seconds

### Cache Headers
Netlify now serves these headers:

**index.html:**
```
Cache-Control: public, max-age=0, must-revalidate
```
→ Browser must revalidate every request (instant updates!)

**\*.json files:**
```
Cache-Control: public, max-age=0, must-revalidate
```
→ No caching of calendar/train data (always fresh!)

**scripts/\*:**
```
Cache-Control: public, max-age=3600
```
→ Scripts cached for 1 hour (good balance)

---

## Benefits Over GitHub Pages

| Feature | GitHub Pages | Netlify |
|---------|-------------|---------|
| Cache Control Headers | ❌ Not allowed | ✅ Full control |
| Auto-deploy on push | ✅ | ✅ |
| Max staleness time | 1 hour | 0 seconds |
| Client-side workarounds needed | ✅ Yes | ❌ No |
| HTTPS | ✅ | ✅ |
| Custom domain | ✅ | ✅ |
| Automatic HTTPS | ✅ | ✅ |
| Free tier | ✅ | ✅ |

---

## Verification

### Test 1: Check Headers
```bash
curl -I https://trmnlweather.netlify.app/index.html
```

Should show:
```
Cache-Control: public, max-age=0, must-revalidate
```

### Test 2: Verify Instant Updates
1. Deploy a change to GitHub
2. Visit your Netlify URL
3. See the update within 30 seconds (not 1 hour!)

### Test 3: Check JSON caching
```bash
curl -I https://trmnlweather.netlify.app/calendar.json
```

Should show:
```
Cache-Control: public, max-age=0, must-revalidate
```

---

## You Can Now Remove Client-Side Cache Busting (Optional)

Since Netlify handles caching server-side, you can simplify index.html by removing:

❌ localStorage cache-busting logic (no longer needed)
❌ Meta refresh fallback (no longer needed)
✅ Keep column alternation (it's fun!)

**But** keeping the client-side cache-busting doesn't hurt - it's an extra layer of protection.

---

## Troubleshooting

### Site not updating after push
1. Check Netlify dashboard for deploy status
2. Wait 30-60 seconds for deployment
3. Hard refresh browser (Cmd+Shift+R on Mac)

### Headers not showing correctly
1. Go to Netlify Site Settings → Build & Deploy
2. Verify `_headers` file is in publish directory
3. Redeploy site manually

### Wrong files deploying
1. Check `.gitignore` - make sure no important files are ignored
2. Verify `_headers` and `netlify.toml` are committed to GitHub
3. Redeploy manually from Netlify dashboard

---

## Next Steps

1. ✅ Commit these configuration files
2. ✅ Sign up for Netlify
3. ✅ Connect your GitHub repo
4. ✅ Get your Netlify URL
5. ✅ Update TRMNL device to point to new URL
6. ✅ Enjoy instant updates with zero caching delays!

---

## Important Notes

- Netlify free tier includes **unlimited deployments**
- Your site is static, so it uses minimal resources
- No build process needed (everything's already built)
- All files in your repo root get deployed (except .gitignore)

**You're ready to deploy!** 🚀
