---
description: End of day - sync memory, clear done list, externalize knowledge, prep tomorrow
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(date:*)
  - Agent
---

End-of-day ritual. Externalize knowledge, clean up, prepare for tomorrow.

## Steps

### Step 1: Read current state (parallel)

Read simultaneously:
- `.claude/memory.md`
- `Daily Notes/MMDDYY.md` (today)
- `Scratchpad.md`
- `Task Board.md`

### Step 2: Process remaining scratchpad items

Same as /sync Step 2. Clear everything — scratchpad should be empty at end of day.

### Step 3: Sync memory

Edit `.claude/memory.md`:
- Update "Now" to reflect where things stand
- Resolve completed Open Threads
- Prune stale Recent Decisions (older than 1 week)
- Clear resolved Blockers

### Step 4: Move completed tasks

In `Task Board.md`:
- Move all completed tasks from Today → Done
- Clear Done list if it's Friday
- Move incomplete Today items to This Week or Backlog with a note on why

### Step 5: Knowledge externalization

Review today's work for learnings:
- **User corrections**: Anything the user explicitly corrected → nominate to `.claude/knowledge-nominations.md`
- **Empirical discoveries**: Things proven through testing → nominate
- **Pattern observations**: Recurring patterns noticed → nominate
- **Failure lessons**: Root cause of any resolved failures → nominate

Format: `- [MMDDYY] /wrap-up: [learning] | Evidence: [source]`

### Step 6: Mandatory daily audit

Spawn the auditor agent to review today's work:

```
Agent(auditor): Review today's work in Daily Notes/MMDDYY.md. Check:
1. Were all tasks completed or properly deferred?
2. Were any knowledge-base rules violated?
3. Are there any pending nominations to review?
Tier: T1 (quick scan). Report findings.
```

### Step 7: Review incident log

Read `.claude/logs/incident-log.md`. Summarize any notable events.

### Step 8: Preview tomorrow

Based on Task Board and Open Threads, suggest 1-3 priorities for tomorrow.
Add them to Task Board → Today.

### Step 9: Update daily note

Add to `Daily Notes/MMDDYY.md` → End of Day Summary:
- Key accomplishments
- Decisions made
- Open items carried forward
- Tomorrow's priorities

### Step 10: Sign off

Brief message: what was accomplished today, what's next tomorrow.
