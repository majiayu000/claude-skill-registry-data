---
description: Mid-day sync - review daily note, update memory, process notes
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(date:*)
---

Mid-day context refresh. Process captured notes, update memory, health check.

## Steps

### Step 1: Read current state (parallel)

Read simultaneously:
- `.claude/memory.md`
- `Daily Notes/MMDDYY.md` (today's date)
- `Scratchpad.md`

### Step 2: Process scratchpad

For each item in Scratchpad:
- Is it a task? → Move to Task Board
- Is it a decision? → Add to Daily Note → Decisions
- Is it a learning? → Nominate to `.claude/knowledge-nominations.md`
- Is it a note? → Add to Daily Note → Notes
- Is it stale? → Delete

Clear processed items from Scratchpad.

### Step 3: Scan task board

Read `Task Board.md`:
- Move completed tasks from Today → Done
- Flag any tasks that are blocked
- Check if priorities have shifted

### Step 4: Context health check

Self-assess:
- Am I still oriented on the right problem?
- Have I been going in circles on anything?
- Is my context getting heavy? (If yes, consider `/clear` after sync)

### Step 5: Orientation check (Boyd's Law)

Ask yourself:
- What has changed since this morning?
- What assumptions am I making that might be wrong?
- What's the simplest next action?

### Step 6: Update memory

Edit `.claude/memory.md`:
- Update "Now" with current focus
- Add/resolve items in "Open Threads"
- Record any new decisions in "Recent Decisions"
- Update "Blockers" if anything changed

### Step 7: Review incident log

Read `.claude/logs/incident-log.md` (if it exists). Look for:
- Repeated failures (same error 3+ times)
- Blocked commands that should be allowed (or vice versa)
- Any CRITICAL severity events

Report anything noteworthy to the user.

### Step 8: Status report

Brief summary:
- What was accomplished this morning
- Current focus
- Any blockers or changes in priority
- Suggested next action
