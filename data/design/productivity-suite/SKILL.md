---
name: Productivity Suite
description: Manage calendar events, spreadsheets, and recurring schedules.
---

# Productivity Skill

## Capabilities
- **Calendar**: List upcoming events and create new meetings (`productivity.calendar_list`, `productivity.calendar_create`).
- **Sheets**: Read data from and append rows to Google Sheets (`productivity.sheets_read`, `productivity.sheets_append`, `productivity.sheets_create`).
- **Scheduling**: Set up recurring tasks for the agent (`productivity.schedule_task`).

## Usage
- Use `calendar` tools for "schedule a meeting" or "what's on my agenda?".
- Use `sheets` tools for "save this to a spreadsheet" or "read the budget file".
- Use `schedule_task` when the user wants something done *periodically* (e.g. "check this every day").

## Constraints
- Requires user authentication via `requireUser`.
- Requires Google Calendar/Sheets to be connected in Settings.
