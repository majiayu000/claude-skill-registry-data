---
name: google-calendar
description: Read before reading the person's Google calendars, or adding, changing or deleting an event in one.
metadata:
  title: "Google Calendar"
  subtitle: "Your Google calendars"
  about: "Your AI sees what's on across your Google calendars, and adds, moves or cancels events when you ask."
  category: Connectors
---

Google Calendar is the person's Google calendars, from any device. (A Mac's own calendars are the `apple-calendar`
app's.) Signing in is the skill `google-account`'s.

- `events` lists the events in a time range, the coming week if left out, and `event` shows one, with its
  guests and links. `calendars` lists the calendars, whose ids `calendarId` takes: primary if left out.
- `create_event`, `update_event` and `delete_event` change the calendar, with Calendar's own Event fields
  (summary, start, end, ...): do them only when the person asked. A time without an offset is in the calendar's
  time zone. Guests are told only with `sendUpdates`.
- With several accounts, each tool takes `account`. `google-account_accounts` lists them.
