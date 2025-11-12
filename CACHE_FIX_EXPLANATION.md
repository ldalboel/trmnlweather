# GitHub Pages Cache Issue - Complete Analysis & Fix

## The Core Problem

GitHub Pages serves files with `Cache-Control: public, max-age=3600` (1 hour). Your HTML's `<meta http-equiv="Cache-Control">` tags **don't override HTTP headers** — they're browser-only directives that GitHub Pages ignores.

After the first deployment, browsers and CDNs cache the file for up to 1 hour, so changes appear static until the cache expires.

## Root Causes

### 1. **HTTP Headers Override Meta Tags**
- `<meta http-equiv="...">` is parsed by browsers only
- HTTP response headers (set by GitHub Pages) take precedence
- GitHub Pages doesn't allow custom header configuration

### 2. **Weak Client-Side Cache Detection**
- Your old version check used `sessionStorage` (cleared on tab close)
- TRMNL devices never close tabs, so it never resets
- It checked script content, not actual data freshness

### 3. **Cached JSON Files**
- `calendar.json` and `trains-data.js` fetches had no cache busting
- Even if HTML reloaded, these were still cached
- `setInterval` refreshes were fetching cached versions

### 4. **Missing Persistent Cache Tracking**
- No mechanism to force refresh after time period on long-running devices
- TRMNL runs 24/7, so stale cache persists indefinitely

## The Complete Fix

### Part 1: Force Refresh Every 30 Minutes
```javascript
(function() {
    const CACHE_DURATION_MS = 30 * 60 * 1000;
    const lastLoadTime = localStorage.getItem('pageLoadTime');
    const now = Date.now();
    
    if (lastLoadTime && (now - parseInt(lastLoadTime)) > CACHE_DURATION_MS) {
        localStorage.setItem('pageLoadTime', now.toString());
        window.location.href = window.location.href.split('?')[0] + '?t=' + now;
        return;
    }
    localStorage.setItem('pageLoadTime', now.toString());
})();
```

**Why it works:**
- `localStorage` persists across tab closes (unlike `sessionStorage`)
- Adds `?t=<timestamp>` query parameter, bypassing HTTP cache
- Forces hard refresh after 30 minutes

### Part 2: Cache-Bust All Fetches
```javascript
// Before
const response = await fetch('calendar.json');

// After
const response = await fetch('calendar.json?t=' + Date.now());
```

**Why it works:**
- Query parameters are unique per request
- CDN/browser cache keys include query string
- Each fetch gets fresh data

### Part 3: Set Explicit HTTP Cache Headers (if using custom domain)
If you migrate from `github.io` to a custom domain with proper hosting:

```
Cache-Control: public, max-age=300
# or for no caching
Cache-Control: public, max-age=0, must-revalidate
```

### Part 4: Meta Refresh (Safety Net)
```html
<meta http-equiv="refresh" content="1800">
```
Automatically refreshes the page every 30 minutes as a fallback.

## What Changed in This Fix

1. ✅ `index.html` now has forced refresh logic with `localStorage`
2. ✅ `calendar.json` fetch now includes `?t=` timestamp
3. ✅ `meta http-equiv="refresh"` added as secondary safety net
4. ✅ `_config.yml` added to document intent
5. ✅ Improved refresh interval (30 min) for better data freshness

## Expected Behavior After Fix

- **First visit**: Loads normally, sets `pageLoadTime` in localStorage
- **30 minutes later**: Forces `?t=<timestamp>` reload, gets fresh HTML
- **Every 2-30 min**: `setInterval` fetches get `?t=Date.now()`, always fresh
- **Browser cache**: Completely bypassed via query parameters
- **GitHub Pages CDN**: Can't serve stale content due to unique URLs

## Testing the Fix

1. Visit your page
2. Wait 30 minutes OR manually clear localStorage: `localStorage.clear()`
3. Page should reload automatically with fresh data
4. Check Network tab in DevTools — URLs should have `?t=` parameters

## If This Still Doesn't Work

**Option A: Use Netlify (Recommended)**
- Netlify allows custom cache headers via `_headers` file
- Much more control over caching behavior
- Free tier supports your use case

**Option B: Add Service Worker**
```javascript
navigator.serviceWorker.register('sw.js');
```
Creates a service worker that intercepts all fetches and adds cache busting.

**Option C: Use API Gateway Rewrite**
Point TRMNL to a server you control (AWS Lambda, Vercel, Netlify) that:
- Always serves fresh index.html with `max-age=0`
- Proxies to your GitHub Pages for other assets

## Why This Is Hard on GitHub Pages

GitHub Pages is a **static file host**, not an app server. It:
- Cannot run custom server code
- Cannot set per-file HTTP headers
- Cannot intercept requests
- Uses CloudFlare as CDN (caches aggressively)

That's why client-side cache busting (query parameters + localStorage) is the solution.
