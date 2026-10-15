---
name: pruning-view
description: "Produce a prune report: stale candidates, stale promoted learnings, and suspected regressions. Use weekly or when startup context feels noisy. Read-only — writes a report but never removes anything on its own."
---

# pruning-view

## When to use
- Weekly hygiene pass.
- After a noticeable increase in friction records.
- When `stable/global.md` approaches the configured budget.

## Protocol
1. Run: `bash ~/.claude/evolution/bin/evolve-prune.sh`
2. Run: `bash ~/.claude/evolution/bin/evolve-regression.sh`
3. Read the resulting `reports/YYYY-MM-DD-prune.md` and `reports/YYYY-MM-DD-regression.md`.
4. Summarize to the user: `N stale candidates, M stale promotions, K suspected regressions.`
5. For each finding, propose the safest action:
   - Stale candidate → move to `rejected/` (operator decides).
   - Stale stable learning → suggest `/evolution demote <id>`.
   - Suspected regression → suggest `/evolution demote <id>` with the contradicting record IDs as evidence.
6. Do not execute any mutation. The operator confirms each action.

## Staleness definition
From `config.yaml: stale_after_days` (default 90). A candidate or promoted learning is stale if `last_confirmed` is older than that cutoff.

## Regression definition
`config.yaml: regression_failure_count` (default 3). A promoted learning is suspected-regression if ≥ N records since its `promoted_at` share token overlap with its text and are of type `correction` or `friction`.

## Output
Summary of the two reports inline + the paths to the full files. No writes to `stable/`.
