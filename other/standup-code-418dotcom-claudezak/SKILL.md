---
description: Quick daily standup - yesterday, today, blockers from git and tasks
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Glob
  - Bash(git log:*, date:*)
---

Automated daily standup. Pulls from git history and task board to generate yesterday/today/blockers in 30 seconds.

## Steps

### Step 1: Get the date context

```bash
date +"%m%d%y %A"
```

Determine yesterday (skip weekends if today is Monday → use Friday).

### Step 2: Gather data (parallel)

**Git activity (yesterday):**
```bash
git log --after="yesterday 00:00" --before="today 00:00" --oneline --no-merges
```

If no commits yesterday, try the last 2 days.

**Task Board:**
Read `Task Board.md`:
- Items marked done recently
- Items currently in progress
- Items marked blocked

**Daily note (yesterday):**
Read yesterday's daily note if it exists — scan for decisions, notes, and end-of-day summary.

**Memory:**
Read `.claude/memory.md` → Now section for current focus.

### Step 3: Generate the standup

Format:

```markdown
## Standup — [Day, Date]

### Yesterday
- [What was accomplished — from git commits and task board]
- [Each item as a bullet, combining related commits]

### Today
- [Priority tasks from task board and memory]
- [Ordered by importance]

### Blockers
- [Anything marked blocked or flagged as waiting]
- [Or "None" if clear]
```

### Step 4: Append to daily note

Add the standup to today's daily note under a `## Standup` section.

If no daily note exists for today, create one first (follow the format from `/start`).

### Step 5: Output

Print the standup concisely. Keep it under 10 lines — standups should be fast.

If there are blockers, highlight them. If everything is clear, say so.
