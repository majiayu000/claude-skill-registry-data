---
name: progress
description: One-shot build queue dashboard. Shows counts by status, burndown, what moved recently, blockers. Use when user says /progress, "how are we doing", "queue status", "what's done", "burndown", or wants a quick pulse on build progress.
---

# PROGRESS (Build Queue Dashboard)

## Purpose

Instant snapshot of build queue health without reading the full 500-line file.

## Procedure

### Phase 1: Parse Queue

Read `docs/UNIFIED-BUILD-QUEUE.md` and extract:

1. Total items per status: DONE, PARTIAL, SPEC-READY, DRAFT, UNSPECCED, BLOCKED, IN-FLIGHT
2. Total items per category (section headers)
3. Items with dependencies that are now met (unblocked)

### Phase 2: Compute Metrics

```
## Build Progress [date]

### Status Breakdown
| Status     | Count | % of Total |
|------------|-------|------------|
| DONE       | X     | X%         |
| PARTIAL    | X     | X%         |
| SPEC-READY | X     | X%         |
| BLOCKED    | X     | X%         |
| IN-FLIGHT  | X     | X%         |
| DRAFT      | X     | X%         |
| TOTAL      | X     | 100%       |

### Progress Bar
[##########----------] 48% complete (DONE + verified PARTIAL)

### By Category
| Category | Done | Partial | Ready | Blocked |
|----------|------|---------|-------|---------|
```

### Phase 3: Movement Since Last Check

Compare with git history of `docs/UNIFIED-BUILD-QUEUE.md`:

- Items that moved to DONE in last 7 days
- Items that moved to PARTIAL in last 7 days
- New items added
- Items newly blocked

### Phase 4: Actionable Insights

- "X items are PARTIAL needing verification (run /sweep)"
- "Y items are BLOCKED - here's what blocks them: [list]"
- "Z items have all dependencies met, ready to build"
- "Highest-priority unbuild item: [name]"

## Output Format

Terse. One screen. No fluff. Numbers and actionable next steps only.

## Constraints

- Read-only. Never modify the queue file.
- If queue file doesn't exist, say so.
- Always show the progress bar visualization.
