---
name: reminders-and-time
description: Interpret reminder and timer requests correctly, and only claim scheduling when an authorized scheduler confirms it.
---

# Reminders And Time

1. Distinguish time questions/calculations, schedule planning, calendar changes, timers, reminders, and recurring checks.
2. Ground relative dates such as 'tomorrow' in an authoritative local timestamp and timezone. Do not fabricate the current time or interpret DST ambiguities as certainty.
3. Resolve only missing material fields: task, date, local time, recurrence. Do not demand known timezone details twice.
4. If a real authorized scheduler is available, confirm meaningful parameters, schedule once, and verify returned state and ID. If absent, say **'No reminder was set'** and offer a concise reminder the user can enter manually.
5. A recorded schedule is not proof a notification was delivered to the watch or heard. Treat schedule existence, delivery, display and acknowledgment as different states.
6. Before retrying after a timeout, look for the existing reminder if possible; use exact ID to edit or cancel.
7. Do not promise to proactively follow up from chat alone. This profile ships with cron jobs and notification integrations disabled.
