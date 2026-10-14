---
name: apple-calendar
description: Read and create Apple Calendar events (macOS). Use when the user asks about today's schedule, upcoming events, or wants to create a calendar event.
---

# Apple Calendar (GenosOS)

Manage calendar events via the dedicated `calendar` tool. Secure — no exec or osascript exposed.

## Actions

```
calendar({ action: 'today' })                                          → today's events
calendar({ action: 'upcoming', days: 7 })                              → next 7 days
calendar({ action: 'create', title: 'Meeting', date: '2026-03-25', time: '10:00', duration: 60 })
```

## Notes

- macOS only — reads from Apple Calendar app
- Creates events in the first calendar by default
- Duration in minutes (default: 60)
- Date format: YYYY-MM-DD, time format: HH:MM
