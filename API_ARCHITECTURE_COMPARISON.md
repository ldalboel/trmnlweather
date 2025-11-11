# Visual Comparison: Why OAuth 2.0 Works, Service Accounts Don't

## ❌ Service Account Architecture (Doesn't Work)

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Google Account                      │
│                   (you@gmail.com)                          │
│                                                              │
│  Calendar: "My Calendar"                                   │
│  └─ Shared with: trmnlweather-calendar@...iam.gserviceaccount.com
└─────────────────────────────────────────────────────────────┘
                           ↓
                    [Manual UI Sharing]
                           ↓
┌─────────────────────────────────────────────────────────────┐
│               Service Account Identity                      │
│        (trmnlweather-calendar@...iam.gserviceaccount.com)  │
│                                                              │
│  API Call: service.calendarList().list()                  │
│  └─ What calendars do I own? → []                         │
│  └─ What calendars are delegated to me? → [] (no admin)  │
│  └─ Result: EMPTY!                                         │
└─────────────────────────────────────────────────────────────┘
```

**Problem:** Sharing via Google Calendar UI doesn't grant API access.

---

## ✅ OAuth 2.0 Architecture (Works!)

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Google Account                      │
│                   (you@gmail.com)                          │
│                                                              │
│  Calendar: "My Calendar" → ACCESSIBLE                      │
│  Shared Calendars → ACCESSIBLE                             │
│  Everything → ACCESSIBLE (because it's YOUR account)       │
└─────────────────────────────────────────────────────────────┘
                           ↓
            [OAuth 2.0 Authorization Flow]
            (One-time, happens locally)
                           ↓
            Generates Refresh Token
                           ↓
        Stored in GitHub as GOOGLE_CALENDAR_REFRESH_TOKEN
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions (Every 6 hours)                 │
│                                                              │
│  Authenticates using refresh token                         │
│  Becomes: you@gmail.com (authenticated user)              │
│                                                              │
│  API Call: service.calendarList().list()                  │
│  └─ I am you@gmail.com                                    │
│  └─ What calendars can I see? → [Your Calendar]          │
│  └─ What events are there? → [Event 1, Event 2, ...]    │
│  └─ Result: SUCCESS! ✓                                    │
│                                                              │
│  Saves to: public/calendar.json                            │
└─────────────────────────────────────────────────────────────┘
                           ↓
                 Web Browser fetches JSON
                           ↓
                Calendar events display
```

**Solution:** OAuth 2.0 makes the API call **as you**, not as a service account.

---

## The Key Difference

| Aspect | Service Account | OAuth 2.0 User |
|--------|-----------------|----------------|
| **Identity** | Robot account (no real person) | Your Google account |
| **Calendar Access** | Only calendars it owns | All calendars you can access |
| **Shared Calendars** | ❌ Not accessible | ✅ Accessible |
| **Admin Required** | ✅ Yes (domain-wide delegation) | ❌ No |
| **Setup Time** | Days (requires admin) | Minutes (just authorize once) |
| **API Response** | `{"items": []}` | `{"items": [{calendar 1}, {calendar 2}]}` |

---

## API Responses Side-by-Side

### Service Account (Wrong)
```json
{
  "kind": "calendar#calendarList",
  "etag": "p32hc3l0aet8og==",
  "nextSyncToken": "CDQKDg1FbEQDKbDSdAiBQBxE",
  "items": []  ← EMPTY!
}
```

### OAuth 2.0 User (Correct)
```json
{
  "kind": "calendar#calendarList",
  "etag": "p32hc3l0aet8og==",
  "nextSyncToken": "CDQKDg1FbEQDKbDSdAiBQBxE",
  "items": [
    {
      "kind": "calendar#calendarListEntry",
      "etag": "1234567890",
      "id": "your-email@gmail.com",
      "summary": "Your Calendar",
      "primary": true
    }
  ]  ← YOUR CALENDARS!
}
```

---

## Google's Official Recommendation

From [Google Calendar API Quickstart](https://developers.google.com/calendar/api/quickstart/python):

```python
# Google's own example uses OAuth 2.0, not service accounts
creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("calendar", "v3", credentials=creds)
```

**Translation:** "To access a user's calendar, authenticate AS that user using OAuth 2.0."

---

## Why This Matters

**Your situation:**
- You want to display your personal calendar on your TRMNL device
- GitHub Actions needs to fetch the events
- The calendar is yours, not a shared organizational calendar

**Correct authentication for your situation:**
- Use OAuth 2.0 with your Google account credentials
- Not service accounts (those are for backend systems)

This is exactly what Google's own documentation recommends for personal calendar access.
