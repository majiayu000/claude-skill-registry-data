---
description: Sprint retrospective - review what worked, what didn't, improve process
argument-hint: "[time period]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Agent
  - Bash(date:*)
---

Retrospective analysis. Review a time period, extract patterns, improve the system.

## Steps

### Step 1: Determine scope

If user specified a time period, use that. Otherwise default to "this week."

### Step 2: Gather data (parallel reads)

Read simultaneously:
- Recent daily notes (last 5-7 days)
- `.claude/logs/verdicts.jsonl` (session quality trends)
- `.claude/logs/incident-log.md` (issues and blocks)
- `.claude/logs/failure-log.md` (tool failures)
- `.claude/knowledge-nominations.md` (pending learnings)
- `Task Board.md` (completion rate)

### Step 3: Analyze patterns

**What went well?**
- Tasks completed on time
- Smooth workflows (no blocks)
- Learnings successfully captured
- Quality verdicts trending positive

**What didn't go well?**
- Repeated failures (same error type)
- Blocked commands that should have been allowed
- Tasks that took much longer than expected
- Context flushes (/clear) needed frequently
- Quality verdict blocks

**What to change?**
- Are there process bottlenecks?
- Are hooks too strict or too lenient?
- Are agents missing capabilities?
- Are commands missing or underused?

### Step 4: Extract improvements

For each identified improvement:
1. Is it a **knowledge-base rule**? → Promote directly
2. Is it a **process change**? → Add to Scratchpad for user review
3. Is it a **tool/config change**? → Create task on Task Board
4. Is it a **pattern to watch**? → Nominate to knowledge-nominations

### Step 5: Write retro report

Add to daily note:

```markdown
## Retrospective — [period]

### Went Well
- [bullets]

### Didn't Go Well
- [bullets]

### Action Items
- [ ] [specific improvement with owner]

### Metrics
- Tasks completed: [X]
- Quality verdict pass rate: [X]%
- Incidents: [X] (CRITICAL: [X], HIGH: [X])
- Context flushes: [X]
```

### Step 6: Create action items

Add any actionable improvements to `Task Board.md` → This Week.
