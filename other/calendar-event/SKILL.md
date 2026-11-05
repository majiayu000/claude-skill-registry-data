---
name: calendar-event
description: Create an .ics calendar invite (title, start, end, location, description) that opens in Outlook, Apple Calendar, or Google Calendar.
---

# calendar-event

Write a standard `.ics` file the user can double-click to add an event to their
calendar. Nothing is scheduled or sent automatically — it only writes the file.

## How to run

```
python3 <skill_dir>/run.py <output.ics> <title> <start> <end> [location] [description]
```

- `<output.ics>` — a path **inside the out-box**.
- `<start>` / `<end>` — `"YYYY-MM-DD HH:MM"` for a timed event, or `"YYYY-MM-DD"`
  for an all-day event.
- `[location]`, `[description]` — optional.

Standard library only. After running, tell the user the saved path.
