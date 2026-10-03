---
name: morning-briefing
description: "Generates a daily priorities briefing across all active matters. Use when Mandy says 'morning briefing', 'what's on today', 'daily update', 'priorities', 'what needs attention', or starts a new work day. Shows overdue deadlines, limitation alerts, proactive stage expectations, unanalysed documents, and a prioritised task list."
---

# Morning Briefing — Daily Priorities

## Important
- This is READ-ONLY. Do not commit to git.
- Read `matters/index.jsonl` first — NOT every matter.json.
- Only read full matter.json for flagged matters.
- Limitation alerts ALWAYS come first.

## Instructions

### Step 1: Read Index
Read `matters/index.jsonl`. Filter to `status: "active"` only.
If empty: show welcome message, suggest `/new-matter` or `/help`. STOP.

### Step 2: Categorise Deadlines
From index fields `next_deadline` and `next_deadline_type`:
- **OVERDUE** — past due date
- **CRITICAL** — within 7 days
- **UPCOMING** — within 30 days

### Step 3: Categorise Limitation Periods
From index field `limitation_expiry`:
- **LIMITATION EXPIRED** — past date
- **LIMITATION CRITICAL** — within 6 months
- **LIMITATION APPROACHING** — within 12 months

### Step 4: Deep Read Flagged Matters
Read full `matter.json` ONLY for matters with: overdue deadlines, limitation alerts, `unanalysed_docs > 0`, `open_flags > 0`, or no activity in 30+ days.

### Step 5: Stage Expectations
Read `rules/stage-expectations.json`. Check each active matter against expected actions for their current stage and claim type.

### Step 6: Unanalysed Documents
For flagged matters, check `documents/` for `*.pdf` without `.extract.json` sibling.

### Step 7: Present
```
LIMITATION ALERTS (always first, if any)
→ OVERDUE DEADLINES
→ THIS WEEK (critical 7 days)
→ PROACTIVE ALERTS (stage expectations overdue)
→ UNANALYSED DOCUMENTS
→ OPEN FLAGS
→ STALE MATTERS (no activity 30+ days)
→ DRAFT LETTERS (unsent)
→ PRIORITISED TASK LIST
```

Suggest `/weekly-review` if no weekly review found in `feedback/weekly-reviews/` within 7 days.

## Error Handling
- **index.jsonl malformed:** "Index file appears corrupted. Run `/validate-matters` to repair."
- **No active matters:** Show welcome message and suggest next steps.
