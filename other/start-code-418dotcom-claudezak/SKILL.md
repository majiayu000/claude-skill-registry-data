---
description: Start the day - load memory, open task board, ready to work
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(date:*)
---

Begin a working session. Load context, create today's daily note, review tasks.

## Steps

### Step 1: Get today's date

```bash
date +"%m%d%y %H:%M %A"
```

### Step 2: Load memory (parallel reads)

Read simultaneously:
- `.claude/memory.md`
- `.claude/knowledge-base.md`

These are your working context. Knowledge-base entries are mandatory constraints.

### Step 3: Create daily note

Create `Daily Notes/MMDDYY.md` (if it doesn't exist):

```markdown
# MMDDYY - Daily Work Log

## Decisions
-

## Meetings & Conversations
-

## Notes
-

## End of Day Summary
-
```

### Step 4: Open task board

Read `Task Board.md`. Scan for:
- Overdue items (anything from previous days still open)
- Today's priorities
- Blocked items

### Step 5: Task review

For each task in Today:
1. Is it still relevant?
2. Do I have what I need to start?
3. Are there dependencies?

Move stale tasks to Backlog. Flag blocked items.

### Step 6: Ready to work

Output a brief orientation:
- What day it is
- Top 1-3 priorities for today
- Any blockers or open threads from memory.md
- "Ready to work. What's first?"

Keep it short. The user wants to start working, not read a report.
