---
name: "Time Awareness"
description: "Provides current date/time information for temporal queries and calculations"
tags: ["date", "time", "today", "tomorrow", "schedule", "deadline", "calendar", "timezone", "week", "current", "now"]
intent: "Provides current date/time information for temporal queries and calculations. Use when user asks about dates, times, schedules, 'today', 'tomorrow', 'this week', deadlines, or anything requiring knowledge of current time. Triggers on relative time references, temporal calculations, scheduling questions, or any task where knowing the current date/time is required."
version: "1.0.0"
languages: all
---

# Time Awareness

## Overview

This skill ensures accurate, time-aware responses by teaching you to use system date commands for current time information instead of guessing or relying on outdated knowledge.

## When to Use

**Use this skill whenever:**
- User asks "what day is it?" or "what's the date?"
- Query contains relative time words: "today", "tomorrow", "yesterday", "this week", "next month"
- User asks about deadlines or time-based planning
- User asks "how long until [date]?" or needs time calculations
- Discussion involves "current events" or "recent" happenings
- ANY task requiring knowledge of the current date/time

**Symptoms indicating you need this skill:**
- User references "now" or "current" without providing specific dates
- Questions about day of week or current month
- Scheduling or calendar-related queries
- Comparisons to "today" or "this year"

## Core Pattern

**Before (Wrong):**
```
User: "What day is it?"
You: "I don't have access to current date information..."
```

**After (Correct):**
```
User: "What day is it?"
You: [Run: date '+%Y-%m-%d %A']
You: "Today is Friday, November 15, 2024"
```

## Quick Reference

| Task | Command |
|------|---------|
| Current date/time | `date '+%Y-%m-%d %A %H:%M:%S %Z'` |
| Tomorrow's date | `date -d "tomorrow" '+%Y-%m-%d %A'` |
| Next Friday | `date -d "next friday" '+%Y-%m-%d %A'` |
| 30 days from now | `date -d "+30 days" '+%Y-%m-%d %A'` |
| Days until date | `echo $(( ($(date -d "2025-12-31" +%s) - $(date +%s)) / 86400 ))` |

## Implementation

### Step 1: Get Current Date/Time

Always start by running:
```bash
date '+%Y-%m-%d %A %H:%M:%S %Z'
```

This provides:
- Full date (YYYY-MM-DD format)
- Day of week
- Current time
- Timezone

### Step 2: For Relative Dates

Use `date` command with descriptive strings:

```bash
# Tomorrow
date -d "tomorrow" '+%Y-%m-%d %A'

# Next Friday  
date -d "next friday" '+%Y-%m-%d %A'

# 2 weeks from now
date -d "+2 weeks" '+%Y-%m-%d %A'

# Last month
date -d "last month" '+%Y-%m-%d'
```

### Step 3: For Date Calculations

Calculate days between dates:
```bash
# Days until Christmas
target=$(date -d "2025-12-25" +%s)
current=$(date +%s)
days=$(( ($target - $current) / 86400 ))
echo "$days days"
```

### Step 4: Response Format

When answering time queries:
1. Run the date command first
2. State the result clearly with full context
3. Use complete dates: "Monday, November 15, 2024" not just "Monday"
4. Include timezone when providing times

## Common Mistakes

### ❌ Don't guess the current date
Never estimate or assume what "today" is.

### ❌ Don't rely on knowledge cutoff
Current date is NOT your training cutoff date.

### ❌ Don't forget timezone context
When times matter, always note the timezone.

### ❌ Don't use vague phrases
Instead of "recently" or "a few weeks ago", get specific dates.

## Examples

User: "What day is today?"
Agent: Run `date '+%Y-%m-%d %A'` to get the current date. Response: "Today is Friday, November 15, 2024."

User: "What's next Wednesday's date?"
Agent: Run `date -d "next wednesday" '+%Y-%m-%d %A'` to calculate. Response: "Next Wednesday is November 20, 2024."

User: "How many days until Christmas?"
Agent: Calculate using `echo $(( ($(date -d "2025-12-25" +%s) - $(date +%s)) / 86400 ))`. Response: "There are 40 days until Christmas (December 25, 2024)."

User: "Should I work on this today?"
Agent: Run `date '+%A'` to check the day. If Saturday/Sunday, suggest: "Today is Saturday. If this isn't urgent, you might want to wait until Monday to ensure your team can review and collaborate."

## Additional Capabilities

### Week Numbers
```bash
date '+Week %V of %Y'
```

### ISO 8601 Format
```bash
date -Iseconds  # Full ISO with timezone
```

### Check if Weekend
```bash
day_num=$(date +%u)
if [[ $day_num -gt 5 ]]; then 
    echo "Weekend"
else 
    echo "Weekday"
fi
```

### Time of Day
```bash
hour=$(date +%H)
if [[ $hour -lt 12 ]]; then 
    echo "Morning"
elif [[ $hour -lt 18 ]]; then 
    echo "Afternoon"
else 
    echo "Evening"
fi
```

## Timezone Awareness

- Always note timezone when providing times
- System default timezone: check with `date +%Z`
- For international contexts, consider mentioning UTC equivalent
- If user's timezone is unclear, ask or state your assumption

## Integration with Other Tasks

This skill should be used **before** other tasks when time context matters:

- **Scheduling**: Know current date before proposing meeting times
- **Deadlines**: Calculate actual days remaining
- **Historical context**: Determine how old information is
- **Data analysis**: Provide time-relative insights
- **Recommendations**: Consider day of week, time of year

## Verification

Before responding to any time query, verify:
- [ ] Ran actual `date` command (not guessing)
- [ ] Provided full date context (day of week + full date)
- [ ] Included timezone if time was mentioned
- [ ] Used user's timezone or clearly stated assumption

---

**Remember:** The `date` command is your source of truth for all time-related information. Always run it; never guess.
