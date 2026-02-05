---
name: read-calendar
description: Read macOS Calendar events for a specified date range. Use this when the user asks about their schedule, upcoming meetings, today's agenda, or wants to know what's on their calendar. Returns events with times, locations, and attendees.
allowed-tools: Bash
---

# Read Calendar

Retrieves calendar events from macOS Calendar for analysis, planning, and scheduling.

## When to Use

- "What's on my calendar today?"
- "Show me my schedule for this week"
- "Do I have any meetings tomorrow?"
- "What's my next meeting?"

## Requirements

This skill requires `icalBuddy` to properly handle recurring events:
\`\`\`bash
brew install ical-buddy
\`\`\`

## Instructions

### Execute Calendar Read

Use icalBuddy to retrieve events including recurring ones:

\`\`\`bash
icalBuddy -n -iep "title,datetime,location" -df "%Y-%m-%d" -tf "%H:%M" eventsFrom:<start_date> to:<end_date>
\`\`\`

Example:
\`\`\`bash
icalBuddy -n -iep "title,datetime,location" -df "%Y-%m-%d" -tf "%H:%M" eventsFrom:2025-10-26 to:2025-10-27
\`\`\`

**Note:** icalBuddy properly handles recurring events (unlike AppleScript which doesn't pre-generate future instances).

### Present Results

Format events clearly:
- Group by day
- Show time, title, location, calendar name
- Highlight conflicts if any
- Identify gaps for focus time
- Mark recurring events clearly
