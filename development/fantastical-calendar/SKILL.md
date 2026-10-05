---
name: fantastical-calendar
description: Create Fantastical calendar events and reminders from Codex on macOS. Use when the user asks Codex to add, schedule, parse, preview, or send a meeting, appointment, task, reminder, time block, daily plan item, 行事曆, 日曆, 會議, 待辦, or 提醒 into Fantastical.
---

# Fantastical Calendar

## Overview

Use this skill to turn a user's natural-language scheduling request into a Fantastical event or reminder through the local macOS Fantastical app.

Prefer the bundled script over ad hoc AppleScript:

```bash
python3 scripts/fantastical_parse.py "Project review on 2026-06-19 at 10:00" --notes "Prep deck before the call"
```

The script defaults to preview mode: it opens Fantastical with the parsed item but does not add it immediately.

## Workflow

1. Clarify only when a calendar detail is genuinely ambiguous: date, time, duration, title, attendee context, calendar, or whether it is an event vs reminder.
2. Convert relative dates into explicit dates before sending to Fantastical whenever possible. Use the user's current timezone from the thread context or check the system date if needed.
3. Build one concise Fantastical sentence containing the title, exact date, start time, and duration or end time.
4. Put extra context, links, preparation notes, or source text in `--notes` instead of overloading the event title.
5. Run `scripts/fantastical_parse.py` from this skill folder.
6. Tell the user whether Fantastical was opened for review or the item was added immediately.

## Add Policy

Use preview mode unless the user explicitly asks to add/create/schedule it now or has confirmed the parsed result.

Preview:

```bash
python3 scripts/fantastical_parse.py "Deep work on 2026-06-19 from 09:00 to 11:00"
```

Add immediately:

```bash
python3 scripts/fantastical_parse.py "Deep work on 2026-06-19 from 09:00 to 11:00" --add-immediately
```

Dry run for validation:

```bash
python3 scripts/fantastical_parse.py "Deep work on 2026-06-19 from 09:00 to 11:00" --dry-run
```

## Sentence Patterns

Use explicit, Fantastical-friendly wording:

- `Team sync on 2026-06-19 from 10:00 to 10:30`
- `Call Alice on 2026-06-20 at 15:00 for 45 minutes`
- `Remind me to submit expenses on 2026-06-21 at 09:00`
- `Focus block on 2026-06-18 from 14:00 to 16:00`

For Chinese user requests, keep the user-facing reply in Chinese, but send Fantastical an explicit mixed or English sentence if it reduces parsing risk.

## Local Integration Details

Read `references/fantastical-macos.md` only when debugging the app integration, updating the script, or adapting it to another Fantastical version.

The current script uses AppleScript `parse sentence` first and can fall back to the Fantastical URL scheme when needed.
