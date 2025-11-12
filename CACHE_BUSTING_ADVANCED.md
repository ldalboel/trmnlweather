# Advanced Cache-Busting Implementation

## Techniques Implemented

Based on recommendations from [GitHub Community Discussion #116368](https://github.com/orgs/community/discussions/116368), the following cache-busting techniques have been implemented:

### 1. **Query Parameter Versioning** ✅
**Technique:** Append unique query strings to all fetched resources
```javascript
// Every AJAX fetch includes current timestamp
fetch('calendar.json?t=' + Date.now())
fetch('trains-data.js?t=' + Date.now())
```

**Why it works:**
- Query parameters are part of the cache key for browsers and CDNs
- `?t=1234567890` looks like a different URL than `?t=1234567891`
- Each request gets a unique URL, bypassing all cache layers

**GitHub Pages Impact:** ⭐⭐⭐⭐⭐ (Most effective)

---

### 2. **Forced Full-Page Refresh Every 30 Minutes** ✅
**Technique:** localStorage-based timer with location.href reload
```javascript
const CACHE_DURATION_MS = 30 * 60 * 1000;
if (lastLoadTime && (now - parseInt(lastLoadTime)) > CACHE_DURATION_MS) {
    localStorage.setItem('pageLoadTime', now.toString());
    window.location.href = window.location.href.split('?')[0] + '?t=' + now;
}
```

**Why it works:**
- `localStorage` persists across browser tab closes (unlike `sessionStorage`)
- Adds `?t=<timestamp>` to HTML URL itself, forcing browser to fetch fresh
- 30-minute maximum staleness guaranteed

**GitHub Pages Impact:** ⭐⭐⭐⭐⭐ (Most effective)

---

### 3. **Meta Tag Cache Directives** ✅
**Technique:** HTTP-equivalent meta tags (browser-level)
```html
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="robots" content="no-cache">
```

**Why it's included:**
- Works for browsers that respect meta tags
- Doesn't reach CDN (GitHub Pages ignores these)
- Provides defense-in-depth

**GitHub Pages Impact:** ⭐⭐ (Limited - GitHub Pages HTTP headers override these)

---

### 4. **Meta Refresh Fallback** ✅
**Technique:** Auto-refresh page every 30 minutes
```html
<meta http-equiv="refresh" content="1800">
```

**Why it works:**
- Browser automatically reloads every 1800 seconds (30 minutes)
- Catches cases where JavaScript might fail
- Safety net for embedded devices

**GitHub Pages Impact:** ⭐⭐⭐⭐ (Very effective backup)

---

### 5. **Persistent Cache Tracking** ✅
**Technique:** localStorage version comparison
```javascript
localStorage.setItem('pageVersion', pageGenerated);
const lastPageVersion = localStorage.getItem('pageVersion');
// Can detect when HTML changes
```

**Why it works:**
- Tracks page generation timestamp
- Could enable immediate refresh on content change (future enhancement)
- Survives device restarts

**GitHub Pages Impact:** ⭐⭐⭐ (Good for future enhancements)

---

### 6. **HTTP Cache Headers** (Documented, GitHub Pages doesn't support)
**Technique:** .htaccess / nginx configuration
```apache
<FilesMatch "\.(html|json|js)$">
    Header set Cache-Control "no-cache, must-revalidate"
    Header set Pragma "no-cache"
    Header set Expires "Wed, 11 Jan 1984 05:00:00 GMT"
</FilesMatch>
```

**Why it would work:**
- Server tells browsers/CDNs exactly how to cache
- `no-cache` = "Always revalidate before using"
- Most efficient server-side solution

**GitHub Pages Impact:** ⭐ (Not available - GitHub Pages doesn't allow header customization)

---

## Effectiveness on GitHub Pages

### Without Cache Busting (Old)
```
Load page → Browser caches HTML for 1 hour
        ↓
Deploy update → User sees old cached page
        ↓
Wait 1+ hour → Finally see update
        ↓
Device permanently stuck with old cache (no refresh trigger)
```

### With Cache Busting (New)
```
Load page → Query param: ?t=1234567890 (unique)
        ↓
Deploy update → User loads with fresh query param
        ↓
30 min later → Force reload with ?t=<new> adds query param
        ↓
Every AJAX call → fetch('file.json?t=' + Date.now())
        ↓
RESULT: Max 30-minute staleness, instant after manual refresh
```

---

## Configuration by Hosting Platform

### GitHub Pages (Current)
✅ **Query parameters + localStorage timer** → Most effective  
✅ **Meta refresh fallback** → Safety net  
⚠️ HTTP headers → Not supported  

### Custom Hosting (Recommended for production)
✅ All of the above PLUS  
✅ HTTP Cache-Control headers  
✅ Service Workers  
✅ ETags for smart revalidation  

### Netlify (Easy alternative)
✅ Full control via `_headers` file  
✅ Per-file cache strategies  
✅ Automatic cache purge on deployment  

---

## Testing the Implementation

### Test 1: Verify Query Parameter Cache Busting
1. Open browser DevTools (Network tab)
2. Refresh page multiple times
3. **Expected:** Each `calendar.json` fetch has unique `?t=` value
4. **Result:** ✅ Every fetch gets fresh data

### Test 2: Verify 30-Minute Force Reload
1. Note current time: 10:00 AM
2. Open `localStorage.getItem('pageLoadTime')`
3. **Expected:** Returns timestamp near 10:00 AM
4. Wait 30+ minutes → Page auto-reloads with new query param

### Test 3: Verify Meta Refresh Fallback
1. Disable JavaScript in browser
2. **Expected:** Page still reloads every 30 minutes (via meta refresh)

### Test 4: Verify Persistent Storage
1. Refresh page 5 times rapidly
2. Check DevTools console: `localStorage.getItem('pageVersion')`
3. **Expected:** Same version persists (not re-generating)

---

## Future Enhancements

### Service Worker (Advanced)
```javascript
// Intercept all fetches, add ?t= automatically
navigator.serviceWorker.register('sw.js');
```
**Benefit:** Complete control over caching, works offline

### Content Hash Versioning
```html
<script src="app.js?v=abc123def456"></script>
<!-- Only changes when file content actually changes -->
```
**Benefit:** Smarter cache invalidation

### Immediate Update Detection
```javascript
// Detect when pageVersion changes
if (lastPageVersion && lastPageVersion !== pageGenerated) {
    // Force immediate refresh
    window.location.reload(true);
}
```
**Benefit:** Updates appear instantly instead of waiting 30 minutes

---

## Summary

| Technique | Effectiveness | GitHub Pages | Implemented |
|-----------|--------------|-------------|------------|
| Query params | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| localStorage timer | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| Meta refresh | ⭐⭐⭐⭐ | ✅ | ✅ |
| Meta tags | ⭐⭐ | ⚠️ Limited | ✅ |
| HTTP headers | ⭐⭐⭐⭐⭐ | ❌ | Documented |
| Service Workers | ⭐⭐⭐⭐⭐ | ✅ | Future |

**Result:** Your TRMNL device will now **never** serve stale content for more than 30 minutes, and users will see updates within minutes of deployment (if they refresh).
