---
name: calendar-create
description: Create a Google Calendar event with 3-route fallback. Use whenever a calendar event needs to be created for Priscila. Do not use for listing/reading (use gcal_list_events directly).
---

# Calendar Create — 3-Route Fallback

## When to use
- User drops a URL → create task event with full instructions
- Scheduling a meeting, reminder, or content shoot
- Automated agent creating a follow-up event

## When NOT to use
- Reading events → use `mcp__claude_ai_Google_Calendar__gcal_list_events`
- Updating an existing event → use `gcal_update_event`

## Required content in every event
- Full source URL(s)
- Numbered action steps
- Tools to use (skills, scripts)
- Drive links to relevant docs/folders

## 3 Routes — never give up, always try all 3

### Route A — Calendar MCP (preferred)
1. Load schemas: `ToolSearch("select:mcp__claude_ai_Google_Calendar__gcal_create_event")`
2. Call the tool with {calendarId, summary, description, start, end}
3. Deferred tool — schema MUST be loaded first or it fails

### Route B — Composio
```
GOOGLECALENDAR_CREATE_EVENT
  session_id: "cook"
  calendar_id: "primary"
  summary, description, start_time, end_time
```

### Route C — Python OAuth
```python
from googleapiclient.discovery import build
creds = Credentials.from_authorized_user_file('~/ClaudeWorkspace/Credentials/sheets_token.json')
cal = build('calendar','v3',credentials=creds)
cal.events().insert(calendarId='primary', body={
    'summary': title,
    'description': description_with_urls_and_steps,
    'start': {'dateTime': start_iso, 'timeZone': 'America/New_York'},
    'end': {'dateTime': end_iso, 'timeZone': 'America/New_York'},
}).execute()
```
- `sheets_token.json` HAS calendar scope (confirmed 2026-04-12)
- GitHub workflow (phone-triggerable, ROUTE C fallback): `.github/workflows/gcal_event.yml`

## Known wrong reports to prevent
- ❌ "Calendar MCP doesn't load in VSCode" — WRONG. It's deferred. ToolSearch first.
- ❌ "OAuth has no calendar scope" — WRONG. sheets_token.json has calendar scope.

## Never tell Priscila to create the event herself unless all 3 routes fail.
