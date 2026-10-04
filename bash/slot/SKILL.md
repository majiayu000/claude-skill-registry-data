---
name: "Slot — Time Slot & Schedule Block Manager"
description: "Use when managing time slots, creating schedule blocks, detecting booking conflicts, exporting calendars, or applying scheduling templates for appointments."
version: "2.0.3"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["slot", "schedule", "calendar", "time-management", "booking", "planner"]
---

# Slot — Time Slot & Schedule Block Manager

Create, query, and manage time slots and schedule blocks. Detect conflicts, export to standard calendar formats, and apply reusable templates.

## Commands

### create
Create a new time slot with date, start/end time, and label.
```bash
bash scripts/script.sh create "2024-03-15" "09:00" "10:30" "Team Standup"
```

### list
List all scheduled slots, optionally filtered by date range.
```bash
bash scripts/script.sh list
bash scripts/script.sh list "2024-03-15" "2024-03-22"
```

### check-conflict
Check if a proposed time slot conflicts with existing bookings.
```bash
bash scripts/script.sh check-conflict "2024-03-15" "09:30" "10:00"
```

### export
Export slots to iCal (.ics) or CSV format.
```bash
bash scripts/script.sh export ics
bash scripts/script.sh export csv
```

### templates
Show or apply common scheduling templates (work day, pomodoro, etc.).
```bash
bash scripts/script.sh templates
bash scripts/script.sh templates pomodoro
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Output
- Slot listings with conflict indicators
- iCal and CSV exports
- Template-based batch slot creation

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
