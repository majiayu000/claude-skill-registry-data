---
name: whats-next
description: Use when user asks what to focus on next, what's next, what they should do, or needs help prioritizing their immediate work
---

# What's Next

## Overview

**Core principle:** Query both data sources (OmniFocus + macOS Calendar), integrate the timeline, and give 1-2 directive next actions. Never present options—YOU decide based on context.

## When to Use

- User asks "What's next?", "What should I work on?", "What do I focus on now?"
- User seems overwhelmed or has decision fatigue
- User is context-switching and needs direction

## Quick Reference

1. **Fetch macOS Calendar events** → Find next hard deadline
2. **Query OmniFocus tasks** → Get flagged, due, next, and available items
3. **Analyze time window** → Calculate available time until next deadline
4. **Make context-aware choice** → Consider energy, estimates, flags, defer dates
5. **Give 1-2 directive actions** → Not options. Decide.

## Implementation

### Step 1: Query macOS Calendar

```bash
# Get events from now through end of day
osascript -e 'tell application "Calendar"
  set startDate to current date
  set endDate to startDate + (1 * days)
  set theEvents to {}
  repeat with cal in calendars
    set calEvents to (every event of cal whose start date ≥ startDate and start date ≤ endDate)
    set theEvents to theEvents & calEvents
  end repeat
  repeat with evt in theEvents
    log (summary of evt) & " | " & (start date of evt as string)
  end repeat
end tell'
```

### Step 2: Query OmniFocus

```javascript
// Get tasks in priority order
mcp__OmniFocus__query_omnifocus({
  entity: "tasks",
  filters: {
    status: ["Next", "Available", "DueSoon", "Overdue"]
  },
  includeCompleted: false,
  fields: ["name", "dueDate", "deferDate", "estimatedMinutes", "flagged", "projectName", "taskStatus"]
})
```

### Step 3: Integrate and Decide

**Find next hard deadline:**
- Next calendar event OR next task due date
- Calculate available time window

**Context-aware selection:**
- **If exhausted/EOD** → Quick wins (< 20 min) OR "stop for today"
- **If < 30 min available** → Quick wins only
- **If 1-2 hours** → Flagged items OR next available tasks that fit
- **Defer dates** → Highlight newly-available tasks
- **Overdue flagged** → Address if time permits, else communicate plan

**Output format:**
```
Next: [Specific task name]
Why: [Time available] + [context reason]
```

NOT:
```
You could do A, B, or C. What do you think?
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "What would you like to focus on?" | Query data sources. YOU decide. |
| "Here are 3 options: A, B, C" | Give 1-2 directive recommendations. |
| "Should you continue debugging or switch?" | Make the choice based on data. |
| Recommending 70 min of work when user is exhausted | Consider "stop for today" or < 15 min tasks. |
| Forgetting to query actual data sources | ALWAYS fetch Calendar + OmniFocus data. |
| Ignoring defer dates | Call out newly-available deferred tasks. |

## Red Flags - STOP

These thoughts mean you're avoiding responsibility:
- "Let me ask what you prefer"
- "I could present some options"
- "It depends on what you want"
- "Let me get clarification first" (before querying data)

**All of these mean: Query the data. Make the decision. Give directive guidance.**

## Special Cases

**User is debugging/in middle of work:**
Check if that work is tracked in OmniFocus. If not, ask progress status. If stuck > 2 hours, recommend context switch.

**User says "I'm beat":**
Consider stopping for the day. If work remains, suggest < 15 min tasks or defer to tomorrow.

**Conflicting priorities:**
Time window wins. If meeting in 30 min and boss asked about 1.5 hour task, recommend preparing for meeting + communicating timeline for other task.

**Empty or sparse data:**
- OmniFocus empty → "Add tasks to your OmniFocus for what needs doing today."
- Calendar empty + OmniFocus has tasks → "No meetings today. Focus on: [specific flagged/next task]"
- Both empty → "You're clear. Take the day off." (If user pushes back, THEN suggest adding tasks)

**NEVER** say "either... or..." even with sparse data. Stay directive. Choose ONE recommendation.

**User asks for options:**
Acknowledge but redirect: "Let me give you a clear recommendation instead." Then query data and decide.

**User disagrees with recommendation:**
Defer to their preference. You're directive about initial recommendations, not dogmatic when they have different context.
