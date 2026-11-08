---
name: mac-calendar
description: List and search your Calendar.app events on a Mac straight from the local calendar database, read-only, with recurring events expanded. Use when asked "what's on my calendar this week", "when is the dentist", "what did I have on March 3rd", "list everything on the Work calendar next month", or "who was in that meeting". Covers every account Calendar.app syncs (iCloud, Google, Exchange, subscribed holidays).
compatibility: macOS; reads local files only; needs Full Disk Access
---

# Mac Calendar (local, read-only)

`scripts/calendar_read.py`, Python 3 stdlib only.

```bash
python3 scripts/calendar_read.py today
python3 scripts/calendar_read.py week --detail          # location, call link, attendees, notes
python3 scripts/calendar_read.py events --since 2026-12-01 --until 2026-12-31 --calendar Work
python3 scripts/calendar_read.py events --days 30 --search dentist
python3 scripts/calendar_read.py search "board meeting"  # all time, any calendar
python3 scripts/calendar_read.py calendars
```

```
Wed 2026-11-04 11:00-12:00         Design review  [Work]
                                    where: Room 4 | 100 Main St
                                    with:  dana@example.com
Fri 2026-11-06  all day (3 days)   Lake trip  [Home]
```

## Where the data is

`~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb` (SQLite, WAL; opened `mode=ro`).

- `CalendarItem`: one row per event (the master for a recurring series). `entity_type = 2` is an event.
  `start_date`/`end_date` are seconds since 2001-01-01. `calendar_id` -> `Calendar.title`;
  `Calendar.store_id` -> `Store.name` (the account). `location_id` -> `Location(title, address)`.
- `OccurrenceCache(event_id, occurrence_date, occurrence_start_date, occurrence_end_date)`: every
  occurrence of every event, recurrences expanded, for a rolling window of about one year back to
  a few years ahead.
- `Participant(owner_id = event, entity_type 7 = attendee, 8 = organizer)` -> `Identity.display_name`; `email`.

## Traps

- **Querying `CalendarItem.start_date` alone misses every repeat** of a recurring event. Use
  `OccurrenceCache` for ranges; the script falls back to master rows outside its window.
- **`occurrence_start_date` is often NULL**; use `COALESCE(occurrence_start_date, occurrence_date)`.
- **All-day dates are stored two ways.** Master rows are "floating" UTC midnight (`start_tz = '_float'`),
  so reading them in local time puts New Year's Day on Dec 31. OccurrenceCache uses local midnight.
- Cancelled events stay in the table with `status = 3`; shown as CANCELLED.

## Permission (TCC) and the EventKit route

The SQLite read needs **Full Disk Access** for the app running the agent (System Settings > Privacy
& Security > Full Disk Access, then restart that app).

EventKit (`osascript -l JavaScript` with `ObjC.import('EventKit')`, or a small Swift script) is the
supported API, but it needs the separate **Calendars** permission, and a command-line process
usually cannot raise the prompt: `EKEventStore.authorizationStatusForEntityType(0)` stays 0 (not
determined) and the store returns zero calendars without an error. Use it only if the host app is
already listed under Privacy & Security > Calendars. The file read above needs neither.

## Limits

Read-only; to create events use Calendar.app, AppleScript or a calendar API skill. Only calendars
synced to this Mac are visible.
