---
name: outlook-calendar
description: "Read Outlook calendar events via ICS subscription. Use when user asks about meetings, schedule, calendar, appointments, or availability."
---

# Outlook Calendar Reader

## Overview

This skill reads calendar events from Outlook via ICS subscription URL.

## When to Use

- User asks about today's meetings or schedule
- User asks about upcoming events
- User wants to check availability
- User asks "What's on my calendar?"

## ICS URL Configuration

**ICS URL**: `<YOUR_ICS_URL_HERE>`

> ⚠️ **Setup Required**: Replace `<YOUR_ICS_URL_HERE>` above with your actual ICS URL.
>
> **How to get your ICS URL:**
> 1. Open [Outlook Web](https://outlook.office365.com)
> 2. Go to Calendar → Settings (gear icon) → View all Outlook settings
> 3. Calendar → Shared calendars → Publish a calendar
> 4. Select calendar and permissions → Publish → Copy ICS link

## Execution Steps

### Method 1: Use ics_parser.py (Recommended)

The skill includes `ics_parser.py` that handles all parsing and RRULE expansion.

**Prerequisite**: [uv](https://docs.astral.sh/uv/) must be installed.

```bash
# Get today's date
TODAY=$(date +%Y-%m-%d)

# Parse events for today
uv run ~/.claude/skills/outlook-calendar/ics_parser.py \
  --url "ICS_URL_HERE" \
  --start "$TODAY" \
  --end "$TODAY"

# Parse events for a date range
uv run ~/.claude/skills/outlook-calendar/ics_parser.py \
  --url "ICS_URL_HERE" \
  --start 2025-12-01 \
  --end 2025-12-31

# Output as JSON
uv run ~/.claude/skills/outlook-calendar/ics_parser.py \
  --url "ICS_URL_HERE" \
  --start 2025-12-01 \
  --end 2025-12-31 \
  --format json

# Debug mode (shows event counts)
uv run ~/.claude/skills/outlook-calendar/ics_parser.py \
  --url "ICS_URL_HERE" \
  --start 2025-12-01 \
  --end 2025-12-31 \
  --debug
```

### Method 2: Manual Parsing with WebFetch

If the script is not available, use WebFetch and parse manually:

1. **Fetch ICS**: Use WebFetch to retrieve the ICS URL
2. **Parse Events**: Extract VEVENT blocks
3. **Handle RRULE**: Expand recurring events (see RRULE Reference below)
4. **Filter & Format**: Filter by date range and output as table

## Script Features

The `ics_parser.py` script handles:

- ✅ All 3 DTSTART formats (UTC, TZID, all-day)
- ✅ RRULE expansion (WEEKLY, DAILY with BYDAY, INTERVAL, UNTIL, COUNT)
- ✅ Automatic timezone conversion (UTC → Taipei UTC+8)
- ✅ Dependencies auto-installed by uv
- ✅ Table or JSON output format
- ✅ Debug mode for troubleshooting

## Output Format

The script outputs a markdown table:

| Date | Time | Event | Location |
|------|------|-------|----------|
| 2025-12-02 (Tue) | 10:30-11:00 | 🔄 Standup Meeting | Microsoft Teams |
| 2025-12-02 (Tue) | 14:00-15:00 | 🔄 Weekly Meeting | Conference Room |
| 2025-12-03 (Wed) | 09:00-10:00 | Project Review | Zoom |

- 🔄 indicates a recurring event

## RRULE Reference

### Identify Recurring Events

A VEVENT with `RRULE` is a recurring event:

```
BEGIN:VEVENT
DTSTART;TZID=Taipei Standard Time:20250424T103000
RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR
SUMMARY:Standup Meeting
END:VEVENT
```

### Common RRULE Parameters

| Parameter | Meaning | Example |
|-----------|---------|---------|
| `FREQ` | Frequency | DAILY, WEEKLY, MONTHLY, YEARLY |
| `INTERVAL` | Every N periods | 2 = every 2 weeks |
| `BYDAY` | Day of week | MO, TU, WE, TH, FR, SA, SU |
| `UNTIL` | End date | 20251231T235959Z |
| `COUNT` | Total occurrences | 10 |

### DTSTART Formats

Outlook ICS uses 3 different formats:

| Format | Example | Timezone |
|--------|---------|----------|
| UTC | `DTSTART:20251211T060000Z` | UTC (convert +8) |
| With TZID | `DTSTART;TZID=Taipei Standard Time:20250424T103000` | Local time |
| All-day | `DTSTART;VALUE=DATE:20251225` | Date only |

## Example Queries

- "What meetings do I have today?"
- "Show my calendar for this week"
- "Am I free tomorrow afternoon?"
- "What's on my schedule for 12/5?"

## Troubleshooting

### Quick Debug

```bash
# Run with debug flag
uv run ics_parser.py --url "..." --start 2025-12-01 --end 2025-12-31 --debug
```

Output shows:
- Total VEVENTs in ICS
- Number of recurring events
- Whether dateutil is available
- Events found in range

### Common Issues

| Issue | Solution |
|-------|----------|
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| No events found | Check date range matches your query |
| Script not found | Run install.sh to install skill |
| ICS URL placeholder | Edit SKILL.md and configure your ICS URL |

## Error Handling

- If ICS URL shows placeholder: Guide user to edit this file and configure their ICS URL
- If uv not found: Install uv first (see README)
- If no events found: Confirm the date range and calendar permissions
- If parsing fails: Use `--debug` flag to see event counts
