---
name: pk-team-review
description: "Command: pk-team-review"
---

# Command: pk-team-review

Read-only health-check. Compares current team assignments against the
latest landscape snapshot and surfaces tier-drift, unavailable models,
and new outperformers. No entities are written.

## Syntax

```
pk-team-review
  [--landscape-artifact <ART-id>]  # explicit landscape override; skips discovery
  [--landscape <artifact-id>]      # alias for --landscape-artifact
  [--threshold <float>]            # flag if tier-score drifted > N pts, default 0.15
  [--budget-scope <SCOPE-id>]      # filter budget drift query to a specific scope
  [--budget-drift-threshold <float>]
                                   # override the projection's drift_threshold_pct
```

## Process (sequential, read-only)

### Step 1 — Load current team

1. Read `context/team/roster.md` to get the active role → model mapping.
2. Resolve the governing DecisionRecord (the most recent `pk-team-create`
   DecisionRecord) via `decision-record.get_decision`.
3. Extract stored formula weights and tier scores from
   `spec.inputs_snapshot`. These are the baseline scores for the diff.
4. Extract `landscape_artifact` ID and date from `inputs_snapshot`.

### Step 2 — Load landscape snapshot

Landscape resolution follows the same three-level precedence as
`pk-team-create` (see `references/landscape-resolution.md`):

1. If `--landscape-artifact <ART-id>` (or alias `--landscape`) is
   supplied, load that artifact directly.
2. Otherwise use the artifact ID stored in the governing DecisionRecord
   `inputs_snapshot.landscape_artifact`. If neither is available,
   apply the three-level discovery: project-tagged artifact first,
   then kit default `landscape-summary`.
3. If the artifact is older than 90 days, include a staleness warning
   in the output. Do not block.

### Step 3 — Re-score current assignments

For each currently-assigned model:
```
model-recommender.get_pricing(<model-id>)
model-recommender.get_profile(<model-id>)
```

Recompute `TierScore` using the weights from `inputs_snapshot`
(not from `--weight-overrides` — the baseline uses stored weights).
Apply the same normalisation across the current accessible candidate set.

### Step 4 — Query for new candidates

```
model-recommender.query_models(
  G_floor=<stored_governance_floor>,
  apply_user_filter=true
)
```

Score all accessible candidates with the stored weights. Identify any
model that:
- Would out-score the current assignment for its role by more than
  `--threshold` (default 0.15).
- Appeared in the landscape since the last `pk-team-create` run.

### Step 5 — Detect unavailable models

```
model-recommender.check_availability()
```

Flag any currently-assigned model whose availability is `degraded`
or `major_outage`.

### Step 5b — Check consultant engagement windows

Call `team-manager.query_consultant_findings()`.

This returns findings with code `team.consultant.expired_but_active`
(severity: warning) for every active TeamMember where `type=consultant`
AND `engagement_window.ends_at < now`. Include the findings in the diff
report (see CONSULTANT WARNINGS section below). This step is read-only.

### Step 5c — Check budget drift

Call `team-manager.query_budget_drift(scope_id?, threshold_pct?)`.

Where:
- `scope_id` = `--budget-scope` flag value (or omitted to auto-detect
  from the governing DecisionRecord's `chartering_scope`).
- `threshold_pct` = `--budget-drift-threshold` flag value (or omitted to
  use the projection's stored `drift_threshold_pct`, default 20).

**Logic inside `query_budget_drift`:**

1. Read the most-recent chartering DecisionRecord that contains a
   `budget_projection` block in its `inputs_snapshot`.
2. If no `budget_projection` block is found: return `status=no_projection_on_file`
   and emit an informational note in the diff report:
   > "no budget projection on file — drift check skipped"
3. Query event-log for invocation events within the chartering Scope's window
   bound to the projection's RoleSlots.  Sum actual cost
   (token counts × unit_cost_usd from the projection snapshot).
4. Compute `drift_pct = (actual - projected) / projected × 100`.
5. If `|drift_pct| > drift_threshold_pct`:
   - Over-spend: emit finding `team.budget.drift`, severity **warning**
     (actionable — consider rebalance or scope reduction).
   - Under-spend: emit finding `team.budget.drift`, severity **info**
     (capacity planning signal — model may be cheaper than expected or
     invocation volume is lower than chartered).
6. Include per-slot drift table in the BUDGET DRIFT section below.

This step is fully read-only.

### Step 6 — Emit diff report

Output format (stdout only — no files written). Each row is keyed by
**archetype name** (resolved through the
`assets/archetype-catalog-mapping.yaml` mapping, layered with the
project override) so the operator sees the same names accepted by
`pk-team-rebalance --roles`. The underlying `(SLOT-id, ROLE-id,
seniority)` tuple is shown in parentheses for traceability.

```
=== pk-team-review — <date> ===
Baseline: DecisionRecord <DEC-id> (<pk-team-create date>)
Chartering Scope: <SCOPE-id>
Landscape: <artifact-id> (<artifact date>) [STALE: >90 days if applicable]
Weights used: C=<C> K=<K> L=<K> G=<G>
Threshold: <threshold>
Mapping source: kit-default | project | cli   (overrides: <count>)

TIER-DRIFT (score delta > threshold):
  developer (SLOT-q2-2026-software-engineer-1, ROLE-software-engineer/senior):
    <old-model-id> (baseline 0.62) → new score 0.44  ▼0.18
    → Best alternative: <new-model-id> (score 0.71, heavy)
    → Recommendation: rebalance this archetype

UNAVAILABLE:
  junior-developer (SLOT-q2-2026-software-engineer-2,
                    ROLE-software-engineer/junior):
    <model-id> — status: major_outage
    → Best fallback: <model-id> (score 0.38, light)

NEW OUTPERFORMERS:
  assistant (SLOT-q2-2026-assistant-1, ROLE-assistant/specialist):
    <new-model-id> (score 0.52) outperforms current
    <model-id> (score 0.31) by 0.21 — within light tier, no tier-shift

CONSULTANT WARNINGS [team.consultant.expired_but_active]:
  <TEAMMEMBER-slug> (<name>, engaged_for: <SCOPE-id>):
    engagement_window ended <ends_at> — still active
    → deactivate or extend engagement_window via update_team_member

BUDGET DRIFT [team.budget.drift | WARNING/INFO]:
  Projected: $<projected_total>   Actual: $<actual_total>
  Drift: <drift_pct>%  (threshold: ±<threshold_pct>%)
  Direction: over-spend (WARNING — actionable) | under-spend (INFO)

  Per-slot drift:
    <SLOT-id> (<role>/<seniority>):
      projected $<projected_total_usd>  actual $<actual_cost_usd>
      drift <slot_drift_pct>% (<direction>)
    ...

  → over-spend: consider pk-team-rebalance or scope reduction
  → under-spend: volume or price lower than chartered (no action required)

  [If no budget_projection block in chartering DEC]:
  BUDGET DRIFT: no budget projection on file — drift check skipped

STABLE (no action needed):
  project-manager, senior-architect, senior-researcher,
  junior-architect, junior-researcher

SUMMARY:
  2 archetypes recommended for rebalance
  1 archetype urgently needs replacement (major_outage)
  1 consultant with expired engagement window (see CONSULTANT WARNINGS)
  1 budget drift finding: over-spend +32% (see BUDGET DRIFT)
  Run: pk-team-rebalance --roles developer,junior-developer --confirm \
       --reason "<reason>"
=============================
```

Omit empty sections. Always emit the SUMMARY even if no issues found.
Include a count of consultant warnings in the SUMMARY line even when
no other issues are detected.

## State side-effects

None. This command is fully read-only.

## Distinction from pk-team-create

`pk-team-review` reads and diffs; `pk-team-create` writes. Running
`pk-team-review` is always safe and reversible. Only run `pk-team-create`
or `pk-team-rebalance` when you have reviewed the diff and confirmed
the recommended changes.
