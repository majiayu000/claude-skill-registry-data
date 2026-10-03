---
name: all-matters
description: "Shows a pipeline view of all matters grouped by stage. Use when Mandy says 'all matters', 'pipeline', 'caseload', 'show all', 'how many matters', or wants an overview of her entire practice."
---

# All Matters — Pipeline View

## Important
- READ-ONLY. No commit. Reads `matters/index.jsonl` only.

## Instructions
1. Read index. Filter by status (default: active).
2. Group by stage. Sort within stage by deadline urgency.
3. Present: `{id} | {client} | {type} | {next_deadline} | flags: {n} | docs pending: {n}`
4. Symbols: ⚠ overdue, ⏰ this week, ○ OK
5. Summary stats: total active, overdue, unanalysed, flags, stale.
