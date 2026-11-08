---
name: gcal
description: Read or write your Google Calendar over the REST API (or the google-calendar MCP), and prove it by reading it back. Use when you say "put this on my calendar", "add it to my calendar", "schedule this", "what's on my calendar", "add a reminder", "block time for X", "checkpoint", or ask to turn a plan into dated commitments. Covers the one-time OAuth setup, the traps (API keys can't write, Testing-mode tokens die weekly, Tasks are invisible in the month view), and the rules for events that actually get seen.
---

# Google Calendar

**Goal:** dated commitments land on the real calendar, and you *prove* it by reading them
back. Done = a read-back listing that shows what you claim you wrote.

## Setup (once)

1. In a Google Cloud project: enable the **Calendar API** (and the **Tasks API** if you want
   to read tasks). Create an **OAuth client, type Desktop**, download it to
   `~/.config/gcal/oauth-client.json`.
2. **OAuth consent screen -> Publish app -> In production** (click through the
   unverified-app warning for your own account). Left in "Testing", the refresh token
   expires every 7 days.
3. `python3 scripts/auth.py` — loopback flow on :3517 with `prompt=consent` so a refresh
   token is actually returned; writes `~/.config/gcal/tokens-calendar-tasks.json`.

Refresh + call, no libraries needed:

```python
import json, os, urllib.parse, urllib.request
cli = json.load(open(os.path.expanduser('~/.config/gcal/oauth-client.json')))['installed']
tok = json.load(open(os.path.expanduser('~/.config/gcal/tokens-calendar-tasks.json')))
d = urllib.parse.urlencode({'client_id': cli['client_id'], 'client_secret': cli['client_secret'],
                            'refresh_token': tok['refresh_token'], 'grant_type': 'refresh_token'}).encode()
at = json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', d))['access_token']
```

- Events: `https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events` (`primary`
  works) — always send `start/end` as `{"dateTime": "...", "timeZone": "<IANA zone>"}`.
- If the `google-calendar` MCP (`npx -y @cocal/google-calendar-mcp`) is loaded, prefer its
  tools; fall back to raw REST.

## Prefer EVENTS over Google Tasks

Tasks live behind a **"Tasks" layer in the Calendar sidebar that is often OFF**, so a task
you write can be invisible in the month view the person actually opens. The API returns
200, the read-back passes, and both of you believe a dated commitment exists while nothing
is visible. Unless the person explicitly lives in Tasks, **make everything an event** —
even when they say "task". A task also can't carry a time (the Tasks API silently drops it).

**Converting an overdue task:** an event in the past will never be seen. Reschedule it to the
next actionable slot (later today, else tomorrow) and say you re-dated it. Delete the
original task in the same pass.

## Traps

1. **An API key can NEVER write to a private calendar.** API keys carry no identity, and
   every personal-data write needs one. Say this immediately when someone offers an API key —
   before they paste a secret into the chat.
2. **A "Testing" consent screen expires the refresh token every 7 days** (project property;
   hits service accounts and OAuth clients alike). If auth breaks about a week after setup,
   this is why.
3. **An MCP server can't be called in the session that installs it** (servers load at
   session start), but its OAuth flow writes a token file immediately, usable over raw REST
   right away.
4. **Google Tasks is a separate API with separate enablement AND a separate scope.** The 403
   body carries the exact activation URL — read the error body, not just the status.
5. **Don't clobber an MCP's own token file** when re-authing for extra scopes; write yours
   somewhere else.
6. **A service account can't add attendees** to events on a personal Gmail calendar (needs
   Workspace domain-wide delegation) and sees nothing until the calendar is shared with its
   `client_email`. The OAuth path is strictly better for a personal calendar.

## Rules

- **Don't set reminders unless asked.** Pass `reminders: {useDefault: false, overrides: []}`
  on every insert — `useDefault: true` silently inherits the calendar's popups. Many people
  read their calendar and don't want it buzzing.
- **Always read back what you wrote, from the EVENTS endpoint, with the neighbouring days**
  in the listing. A read-back of only the row you wrote proves it exists, not that it is
  where the person looks.
- **Never re-import an .ics after writing via API.** It duplicates every event.
- **Put the actionable link and logistics in the event body**, not only in chat, so tapping
  the notification on a phone is sufficient.
- **Never write a bare local time without its timezone.**
- **The calendar is for a person's life, not an agent's work queue.** Appointments, travel,
  people, deadlines someone else set, and irreversible actions only the person can take go
  on the calendar. "Re-run a script", "chase a request", "read a data release" belong in a
  file the next agent session reads (see the `pending-queue` hook). The tell: if the event's
  body has to say "no action needed", it isn't a calendar item.
- Decide yourself: dates, times, wording, re-dating overdue items. Ask before deleting or
  moving entries the person didn't put in scope.
