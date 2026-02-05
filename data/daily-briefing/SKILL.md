---
name: daily-briefing
description: Generate a comprehensive daily briefing combining calendar events, email inbox status, and reminders. Use when the user asks to plan their day, get a morning briefing, or wants an overview of their schedule and tasks. This orchestrates multiple skills together.
allowed-tools: Bash
---

# Daily Briefing

Comprehensive morning briefing that combines your schedule, emails, and tasks into an actionable daily plan.

## When to Use

- "Plan my day"
- "Give me my morning briefing"
- "What's my day look like?"
- "Help me organize my day"
- "What should I focus on today?"

## Requirements

This skill requires `icalBuddy` for accurate calendar data with recurring events:
```bash
brew install ical-buddy
```

## Instructions

### Step 1: Gather Data

Run all three data-gathering commands in parallel:

1. **Check Calendar** (using icalBuddy for recurring events):
```bash
TODAY=$(date +%Y-%m-%d)
icalBuddy -n -iep "title,datetime,location" -df "%Y-%m-%d" -tf "%H:%M" eventsFrom:"$TODAY" to:"$TODAY"
```

2. **Check Email**:
```bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false
```

3. **Check Reminders**:
```bash
osascript .claude/skills/list-reminders/scripts/list_tasks.scpt
```

### Step 2: Analyze and Synthesize

Cross-reference the data:
- Match calendar events with related tasks
- Identify time blocks for task completion
- Highlight urgent items from email
- Flag scheduling conflicts

### Step 3: Generate Briefing

Present in this format:

```
🌅 Good Morning! Here's Your Day (October 26, 2025)

📅 CALENDAR (0 events)
• No meetings scheduled
• Full day available for focused work

📬 INBOX (38 unread, 24h)
• 0 urgent/actionable items
• Newsletters can be batch-processed later

✅ TASKS (X incomplete)
• Overdue: X items - PRIORITY
• Today: X items
• Total pending: X items

⏰ RECOMMENDED SCHEDULE
• 9:00-12:00: Deep work on [high-priority task]
• 12:00-13:00: Lunch + email triage
• 13:00-16:00: [Task completion]
• 16:00-17:00: Tomorrow prep + inbox zero

💡 FOCUS FOR TODAY
1. [Most important task]
2. [Second priority]
3. [Third priority]

🎯 You have a clear day - make it count!
```

### Step 4: Offer Follow-up

Ask if the user wants to:
- Block time for specific tasks
- Dive deeper into any category
- Create reminders from emails
- Reschedule anything

For examples, see [examples.md](examples.md).
