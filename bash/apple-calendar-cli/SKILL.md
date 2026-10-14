---
name: apple-calendar-cli
description: Manage Apple Calendar events — list, create, update, delete via EventKit CLI. macOS 14+ required.
metadata: { "nyxclaw": { "emoji": "📅", "requires": { "bins": ["apple-calendar-cli"] } } }
---

# Apple Calendar CLI — Agent Skill

You have access to `apple-calendar-cli`, a command-line tool for managing Apple Calendar events via EventKit on macOS.

## Prerequisites

- macOS 14+ required
- Install: `brew install sichengchen/tap/apple-calendar-cli`
- Calendar access permission must be granted (System Settings > Privacy & Security > Calendars)

## Date Format

All dates use ISO 8601 format:

- Date only: `YYYY-MM-DD` (interpreted as start of day in local timezone)
- Date and time: `YYYY-MM-DDTHH:MM:SS` (local timezone)
- Full ISO 8601: `YYYY-MM-DDTHH:MM:SSZ` or with offset

## Global Options

- `--json` — Output results as structured JSON (available on all commands)
- `--version` — Show version
- `--help` / `-h` — Show help

**Always use `--json` when calling from an agent** for reliable parsing.

## Commands

### list-calendars

List all available calendars.

```bash
apple-calendar-cli list-calendars --json
```

**JSON output** — array of objects:

```json
[
  {
    "identifier": "CALENDAR-ID",
    "title": "Work",
    "type": "calDAV",
    "source": "iCloud",
    "color": "#1BADF8",
    "isImmutable": false
  }
]
```

Use `identifier` to filter events or target a specific calendar when creating events.

### list-events

List events within a date range.

```bash
apple-calendar-cli list-events --json
apple-calendar-cli list-events --from 2026-02-22 --to 2026-02-28 --json
apple-calendar-cli list-events --from 2026-02-22 --to 2026-02-28 --calendar CALENDAR-ID --json
```

**Options:**

- `--from` — Start date (default: today)
- `--to` — End date (default: 7 days from start)
- `--calendar` — Filter by calendar identifier

**JSON output** — array of event objects:

```json
[
  {
    "identifier": "EVENT-ID",
    "title": "Team standup",
    "startDate": "2026-02-22T10:00:00-08:00",
    "endDate": "2026-02-22T10:30:00-08:00",
    "isAllDay": false,
    "location": "Conference Room A",
    "notes": null,
    "calendarTitle": "Work",
    "calendarIdentifier": "CALENDAR-ID",
    "url": null,
    "hasRecurrenceRules": true
  }
]
```

### get-event

Get full details of a single event.

```bash
apple-calendar-cli get-event EVENT-ID --json
```

**JSON output** — single event object (same schema as list-events items).

### create-event

Create a new calendar event.

```bash
apple-calendar-cli create-event \
  --title "Meeting with Alice" \
  --start "2026-02-23T14:00:00" \
  --end "2026-02-23T15:00:00" \
  --json

apple-calendar-cli create-event \
  --title "All-day conference" \
  --start "2026-03-01" \
  --end "2026-03-02" \
  --all-day \
  --calendar CALENDAR-ID \
  --location "Convention Center" \
  --notes "Bring laptop" \
  --url "https://example.com/conf" \
  --json
```

**Required options:**

- `--title` — Event title
- `--start` — Start date/time
- `--end` — End date/time (must be after start)

**Optional options:**

- `--calendar` — Calendar identifier (default: system default calendar)
- `--notes` — Event notes
- `--location` — Event location
- `--all-day` — Mark as all-day event
- `--url` — Event URL
- `--recurrence` — Recurrence rule: `daily`, `weekly`, `monthly`, `yearly`
- `--recurrence-end` — End date for recurrence
- `--recurrence-count` — Number of occurrences
- `--attendees` — Comma-separated email addresses
- `--alert` — Alert offset (e.g., `15m`, `1h`, `1d`)

**JSON output** — the created event object with its new identifier.

### update-event

Update an existing event (partial update — only specified fields change).

```bash
apple-calendar-cli update-event EVENT-ID --title "New title" --json
apple-calendar-cli update-event EVENT-ID \
  --start "2026-02-23T15:00:00" \
  --end "2026-02-23T16:00:00" \
  --location "Room B" \
  --json
```

**Required argument:**

- `<id>` — Event identifier

**Optional options:**

- `--title` — New title
- `--start` — New start date/time
- `--end` — New end date/time
- `--calendar` — Move to different calendar (by identifier)
- `--notes` — New notes
- `--location` — New location
- `--url` — New URL

**JSON output** — the updated event object.

### delete-event

Delete a calendar event.

```bash
apple-calendar-cli delete-event EVENT-ID --json
```

**JSON output:**

```json
{
  "deleted": true,
  "event": { ... }
}
```

## Common Agent Workflows

### Find and reschedule an event

```bash
# 1. List events to find the one to reschedule
apple-calendar-cli list-events --from 2026-02-22 --to 2026-02-28 --json

# 2. Get full details
apple-calendar-cli get-event EVENT-ID --json

# 3. Update the time
apple-calendar-cli update-event EVENT-ID \
  --start "2026-02-24T14:00:00" \
  --end "2026-02-24T15:00:00" \
  --json
```

### Create an event on a specific calendar

```bash
# 1. List calendars to find the right one
apple-calendar-cli list-calendars --json

# 2. Create the event on that calendar
apple-calendar-cli create-event \
  --title "Dentist" \
  --start "2026-02-25T09:00:00" \
  --end "2026-02-25T10:00:00" \
  --calendar CALENDAR-ID \
  --json
```

### Check today's schedule

Date-only values resolve to midnight (`00:00:00`), so `--to` must be the **next day** to cover the full day:

```bash
# Correct: covers 2026-02-22 00:00 to 2026-02-23 00:00
apple-calendar-cli list-events --from 2026-02-22 --to 2026-02-23 --json
```

## Error Handling

- **Calendar access denied**: User needs to grant access in System Settings > Privacy & Security > Calendars
- **Event not found**: The event ID may be stale — list events again to get current IDs
- **Invalid date format**: Use ISO 8601 (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`)
- **End before start**: Ensure the end date/time is after the start date/time
