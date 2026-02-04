---
name: calendar
description: Read and write macOS Calendar events using natural language
---

# Calendar Skill

Interact with your macOS Calendar through natural language commands.

## What You Can Do

- **Read events**: "What's on my calendar today?" or "Show me next Friday's schedule"
- **Create events**: "Add team meeting tomorrow at 2pm" or "Create dentist appointment next Tuesday at 10am"
- **Delete events**: "Remove the standup from tomorrow"
- **List calendars**: "What calendars do I have?"

## Implementation Reference

Use AppleScript via subprocess to interact with Calendar.app:

```python
import subprocess
from datetime import datetime, timedelta
import re

def create_event(title, when, duration_min=60, location=None, notes=None):
    """Create a calendar event"""
    start = parse_datetime(when)
    end = start + timedelta(minutes=duration_min)

    offset_start = int((start - datetime.now()).total_seconds())
    offset_end = int((end - datetime.now()).total_seconds())

    script = f'''
tell application "Calendar"
    tell calendar "Calendar"
        set startDate to (current date) + {offset_start}
        set endDate to (current date) + {offset_end}
        set evt to make new event with properties {{summary:"{title}", start date:startDate, end date:endDate}}
'''
    if location:
        script += f'        set location of evt to "{location}"\n'
    if notes:
        script += f'        set description of evt to "{notes}"\n'

    script += '''    end tell
end tell
'''
    subprocess.run(['osascript', '-e', script], check=True)

def read_events(date_str="today"):
    """Read events for a date"""
    target = parse_date(date_str)

    script = f'''
tell application "Calendar"
    set output to {{}}
    set target to date "{target.strftime('%A, %B %d, %Y')}"

    repeat with cal in calendars
        repeat with evt in (events of cal whose start date ≥ target and start date < (target + 1 * days))
            set end of output to (summary of evt) & " at " & (time string of start date of evt)
        end repeat
    end repeat

    return output
end tell
'''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def list_calendars():
    """List all calendars"""
    script = '''
tell application "Calendar"
    return name of every calendar
end tell
'''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
    return result.stdout.strip().split(", ")

def delete_event(title, date_str="today"):
    """Delete an event by title"""
    target = parse_date(date_str)
    next_day = target + timedelta(days=1)

    script = f'''
tell application "Calendar"
    tell calendar "Calendar"
        delete (every event whose summary is "{title}" and start date ≥ date "{target.strftime('%A, %B %d, %Y 00:00:00')}" and start date < date "{next_day.strftime('%A, %B %d, %Y 00:00:00')}")
    end tell
end tell
'''
    subprocess.run(['osascript', '-e', script], check=True)

def parse_date(s):
    """Parse natural language date"""
    s = s.lower().strip()
    now = datetime.now()

    if s == "today": return now
    if s == "tomorrow": return now + timedelta(days=1)
    if s == "yesterday": return now - timedelta(days=1)

    days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6}

    for day, num in days.items():
        if s.startswith("next " + day):
            days_ahead = (num - now.weekday() + 7) % 7 or 7
            return now + timedelta(days=days_ahead)

    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except:
        return now

def parse_datetime(s):
    """Parse natural language date with time"""
    s = s.lower().strip()

    # Match: "tomorrow at 2pm", "today at 10:30am", etc.
    m = re.match(r"(tomorrow|today|next \w+|yesterday).*?(\d{1,2}):?(\d{0,2})\s*(am|pm)?", s)
    if m:
        date_part, hour, minute, meridiem = m.groups()
        hour = int(hour)
        minute = int(minute) if minute else 0

        if meridiem == "pm" and hour != 12: hour += 12
        if meridiem == "am" and hour == 12: hour = 0

        base = parse_date(date_part)
        return base.replace(hour=hour, minute=minute, second=0, microsecond=0)

    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except:
        return datetime.now()
```

## Usage Examples

```python
# Read today's events
events = read_events("today")
print(events)

# Create a meeting
create_event("Team Sync", "tomorrow at 2pm", location="Zoom", duration_min=30)

# Delete an event
delete_event("Team Sync", "tomorrow")

# List all calendars
cals = list_calendars()
print(cals)
```

When you ask Claude Code to interact with your calendar, it generates and runs the appropriate code.
