---
name: calendar
description: The org's events calendar, synced from Notion to Google Calendar.
---

# Calendar

Use it to answer "what's on" and to keep the Google Calendar in step with the Notion events database.

## Flow

1. `calendar.events` for past and upcoming events. Start here for any question about an event.
2. `calendar.settings` to see which Notion database and Google Calendar the org uses and when it last synced.
3. To set up: `calendar.setup` makes the Google Calendar, then `calendar.update_settings` sets the Notion database and turns sync on.
4. `calendar.sync` copies Notion events to Google now. The sync job also runs on its own.

## Watch out

- Notion is the source. An edit made in Google Calendar is overwritten on the next sync.
- An empty id in `calendar.update_settings` clears that setting.
