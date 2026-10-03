---
name: daily-planner
description: >-
  Adaptive daily planning skill that pivots the active weekly plan based on what closed
  yesterday. Directly reuses the core engine and adversarial Northstars from weekly-planner
  (skills/3-weekly/weekly-planner/) to eliminate logic drift and prevent planning contradictions.
  Re-sequences the daily merge queue and highlights the immediate blocker for the operator.
---

# Daily Planner (Adaptive Daily Pivot)

Adapts the active weekly plan based on yesterday's progress, landed PRs, and newly emerged blockers.

**Drift Prevention Contract:** This skill does NOT duplicate planning heuristics or merge algorithms. It directly executes the shared core engine at `${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/weekly-planner/scripts/planner_core.py` (or `skills/3-weekly/weekly-planner/scripts/planner_core.py` when in this repository) to ensure that daily tactical decisions remain 100% coherent with the weekly trajectory.

---

## Daily Workflow

### Step 1: Preflight & Weekly Plan Lookup

1. Locate the latest weekly plan in `temp/planner/` (`weekly-plan-*.json` or `WEEKLY-PLAN-*.md`).
2. If no weekly baseline exists, the daily runner halts with an actionable error prompting the operator to run `/weekly-planner` first to establish the baseline trajectory.

### Step 2: Ingest Yesterday's Closures

Run the shared engine in daily mode:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/weekly-planner/scripts/planner_core.py" --repo-root . --mode daily
# Or when running directly inside XYZ-forge:
python3 skills/3-weekly/weekly-planner/scripts/planner_core.py --repo-root . --mode daily
```

The engine automatically:
- Scans PRs merged in the last 24–36 hours (`gh pr list --state merged` bounded by `mergedAt`).
- Scans issues closed in the last 24–36 hours (`gh issue list --state closed` bounded by `closedAt`).
- Reconciles baseline items from the weekly plan against these closures and marks completed items `[DONE]`.

Before presenting a status change, recheck current sources and the latest explicit owner decisions; a merged PR alone does not prove deployment, backfill, or production acceptance.

### Step 3: Re-Sequence & Promote Unblocked Work

- Open PRs are re-sorted topologically into the 4 phases (Ready to Land, Blockers to Fix, Needs Rebase, In Review) with CI status check validation (`statusCheckRollup`).
- Newly unblocked dependent tasks are promoted to the top of today's operator queue.
- If a task is waiting on a business decision, the **Provisional Decision Protocol** is applied (fallback default + record on canonical tracking issue).

### Step 4: Adversarial Audit on the Daily Pivot

Before presenting the pivoted day plan, the engine executes the 2nd-Pass Adversarial Audit:
- **Duplication:** Checks if today's actions duplicate work in review.
- **Contradiction:** Checks if two developers are scheduled to touch colliding files today.
- **Race Condition:** Ensures long-running migrations/backfills aren't scheduled over concurrent sync jobs.

### Step 5: Output Daily Action Queue

Emits both machine-readable `temp/planner/daily-pivot-<date>.json` and human-readable `temp/planner/DAILY-PIVOT-<date>.md`:
1. **Accomplished Yesterday:** Include only updates evidenced within the stated calendar day and cite their dates/sources; keep older context separate, even when the ingestion window spans 24–36 hours.
2. **Today's Immediate P0 Blocker:** The single item the operator should clear first.
3. **Today's Teammate Action Queues:** Focused tasks for each member.
4. **Active Merge Sequence:** Live status of the PR queue with passing CI requirements.

Apply the weekly planner's Step 5 calibration checks to the daily queue, using fresh per-owner and per-applicable-tenant evidence rather than carrying forward an old success count.
