# Why Your Cache Issue Happened & How It's Fixed

## The Ultra-Deep Analysis

### **Layer 1: HTTP vs Meta Tags (The Fundamental Misunderstanding)**

You added these meta tags to `index.html`:
```html
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
```

**This does NOTHING on GitHub Pages.** Here's why:

1. **HTTP Response Headers** (set by the server - GitHub Pages):
   - `Cache-Control: public, max-age=3600`
   - Tells CDNs, proxies, and browsers how long to cache
   - **Cannot be overridden by HTML meta tags**

2. **HTML Meta Tags** (parsed by browsers):
   - Only work if HTTP headers don't specify caching
   - Are ignored when HTTP `Cache-Control` is present
   - Cannot reach CDN caches (which sit between browser and origin)

**The browser follows this priority:**
```
HTTP Response Headers (ALWAYS WINS)
    ↓ (ignored if HTTP headers present)
HTML Meta Tags
    ↓ (ignored if either above present)
Browser defaults
```

### **Layer 2: CloudFlare CDN (GitHub Pages' Hidden Caching Layer)**

GitHub Pages uses **CloudFlare as a CDN**, which:
- Caches **entire responses** including HTML (not just static assets)
- Respects `max-age=3600` aggressively
- Has **edge nodes worldwide** all serving stale copies

Even if your browser didn't cache it, CloudFlare caches it for the full hour.

### **Layer 3: TRMNL's 24/7 Persistence (Your Specific Problem)**

A TRMNL device:
- Runs **continuously** (never restarted)
- Keeps browser tabs **permanently open**
- Your old cache check used `sessionStorage`:
  ```javascript
  sessionStorage.getItem('pageVersion')
  ```
- `sessionStorage` is cleared **only when tab closes**
- Your device never closes the tab → cache check never runs

**Result:** After first deployment, the device fetches the page once, caches it, and keeps serving that cached version forever.

### **Layer 4: Cascading Cache Failures**

Once HTML is cached, the embedded data is also stale:

```html
<script>
    window.trainsData = {"updated": "2025-11-12T08:26:24...", ...};
    window.calendarData = {"updated": "2025-11-12T07:26:21...", ...};
</script>
```

And the `setInterval` refreshes fetch from stale cached JSON:

```javascript
// Every 2 minutes
setInterval(async () => {
    const response = await fetch('calendar.json');  // ← CACHED, gets old data
}, 2 * 60 * 1000);
```

---

## How The Fix Works

### **Fix #1: Force Reload Every 30 Minutes**

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

**Why this works:**

1. **Uses `localStorage`** (not `sessionStorage`)
   - Persists even when tab never closes
   - Survives device restarts
   - On TRMNL's 24/7 running, this tracks time across days

2. **Adds `?t=<timestamp>` Query Parameter**
   - `?t=1234567890` tells browsers: "This is a new URL, don't use cache"
   - Different URL = different cache entry
   - CloudFlare's cache also sees new URL = fetches fresh

3. **Enforces 30-Minute Maximum Staleness**
   ```
   Device starts → sets pageLoadTime
   ↓ (30 min later)
   Forces reload with ?t=<new-timestamp>
   ↓
   Browser: "URL changed, fetch fresh from server"
   ↓
   CloudFlare: "URL changed, fetch fresh from origin"
   ↓
   Gets fresh HTML
   ```

### **Fix #2: Cache-Bust All AJAX Calls**

```javascript
// Before: Fetches cached file
const response = await fetch('calendar.json');

// After: Forces fresh fetch every time
const response = await fetch('calendar.json?t=' + Date.now());
```

Each `setInterval` cycle now gets:
- `calendar.json?t=1234567891` (first call)
- `calendar.json?t=1234567892` (second call)
- `calendar.json?t=1234567893` (third call)

Different URL = unique cache entry = never cached.

### **Fix #3: Meta Refresh as Safety Net**

```html
<meta http-equiv="refresh" content="1800">
```

If JavaScript fails (simple browser, TRMNL error, etc.), the browser automatically refreshes every 30 minutes (1800 seconds).

---

## What Now Happens After Deployment

### **Before Fix (Broken):**
```
Deploy new index.html (v2)
    ↓
User loads page → Gets v2 HTML
    ↓
Browser caches: "index.html = v2, expiry in 1 hour"
    ↓
Deploy update to calendar.json
    ↓
User refreshes page → Still gets v2 HTML (from cache!)
    ↓
setInterval fetches calendar.json → Still cached
    ↓
Device shows old data forever (until 1 hour elapses)
```

### **After Fix (Works):**
```
Deploy new index.html (v2)
    ↓
User loads page → Gets v2 HTML
    ↓
JavaScript: sets localStorage.pageLoadTime = now
    ↓
Deploy update to calendar.json
    ↓
30 min later:
    ↓
localStorage check: "30 min passed!" → Force reload with ?t=1234567890
    ↓
Browser: "New URL (with ?t param), fetch fresh"
    ↓
Gets v2 HTML with new embedded data
    ↓
setInterval fetches: calendar.json?t=<unique-time>
    ↓
Each fetch gets fresh data (no caching)
    ↓
Device always shows latest data
```

---

## Edge Cases & Limitations

### ✅ What This Fixes
- HTML staying stale on 24/7 TRMNL devices
- Stale embedded data (train/calendar)
- Stale AJAX responses
- CloudFlare CDN caching

### ⚠️ What This Doesn't Fully Fix
- **GitHub Pages still caches for others** for up to 1 hour
  - But your device bypasses it via query params
  - Others will see old data for up to 1 hour
  
- **Font CDN caching** (Google Fonts)
  - `fonts.googleapis.com` has its own cache
  - Doesn't matter (styles/fonts rarely change)

### 🎯 For Perfect Control: Migrate to Netlify

If you want:
- Zero caching delays for ALL users
- Per-file cache control
- HTTP/2 push optimization

Use **Netlify** with a `_headers` file:
```
[[headers]]
for = "index.html"

[headers.values]
Cache-Control = "public, max-age=0, must-revalidate"

[[headers]]
for = "/*.json"

[headers.values]
Cache-Control = "public, max-age=0, must-revalidate"
```

GitHub Pages simply cannot do this.

---

## Testing Your Fix

1. **Deploy these changes**
2. **Visit your page** → Note the timestamp in localStorage:
   ```javascript
   localStorage.getItem('pageLoadTime')  // Should show current time
   ```
3. **Wait 30 minutes** → Page auto-reloads
4. **Check Network tab** in DevTools → URLs should have `?t=` parameters
5. **Update calendar.json** → Changes appear within 30 min max

---

## Key Takeaway

**The core issue:** GitHub Pages + CloudFlare caching + stale `sessionStorage` check = permanent staleness on 24/7 TRMNL devices.

**The solution:** Force full-page refresh every 30 minutes with persistent `localStorage` tracking + cache-bust ALL resource fetches with timestamps.

This is the **only reliable way** to do this on GitHub Pages without migrating to a hosting platform that allows HTTP header control.
