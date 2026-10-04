---
name: structured-planning
description: >
  Decompose multi-step work into a revisable subgoal plan with stable step IDs,
  checkpointing, and plan-ahead execution. Load when a task needs explicit
  planning before action, subgoal decomposition, plan checkpointing, or
  ReCAP-style plan-ahead execution. Also triggers on "structured plan",
  "plan with steps", "subgoal graph", "revise the plan", "checkpoint plan",
  or multi-step tasks where naive one-shot execution would be fragile. Skips
  trivial single-step tasks. Pairs with dynamic-routing on failure. Distinct
  from process-decomposer (registry/triage) and problem-to-plan (doc deliverables).
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: Anthropic Building Effective Agents, ReCAP NeurIPS 2025, DyFlow, GAP, NaviAgent
  resources:
    references:
      - PATTERNS.md
      - PLAN-SCHEMA.md
      - examples.md
    scripts:
      - plan_lint.py
---
# Structured Planning

You plan before you act: emit a subgoal checklist with stable ids (`S1`, `S1.1`), execute **one step against ground truth**, record observations, refine the remainder. On failure, hand off to `dynamic-routing` — do not blind-retry.

## Hard Rules

Trivial tasks (single step, obvious outcome) → skip formal plan; state "trivial — plan skipped."
Non-trivial tasks → write plan to `.agent-loom/plans/<task-id>.md` per `references/PLAN-SCHEMA.md`.
Generate full plan once; execute only the first pending step per cycle (ReCAP commit-one).
Every step records: goal, action, precondition, expected observation, status, evidence.
Run `scripts/plan_lint.py` after each plan write.
Append plan changes to **Plan delta log** with reason — never silent edits.

---

## Workflow

### Step 1 — Triage complexity

| Signal | Route |
|--------|-------|
| Single tool call / one file / clear outcome | Skip plan — execute directly |
| Multi-step, failure-prone, or user asked to plan | Continue |

### Step 2 — Draft full plan

1. Assign `task_id` slug and stable step ids.
2. Fill all fields per PLAN-SCHEMA.
3. Write file; run `plan_lint.py`.

### Step 3 — Execute one step

1. Mark step `in-progress`.
2. Run the action; capture **actual** observation in `evidence:`.
3. Mark `done` or `failed`.

### Step 4 — Refine remainder

Before the next step: update preconditions/expected fields for pending steps using new evidence. Log deltas.

### Step 5 — On failure

Invoke `dynamic-routing` with failed step id + evidence. Apply revised plan; lint again.

### Step 6 — Complete

All steps `done` or explicit `aborted`. Emit final plan path.

---

## Gotchas

- Executing the whole plan without observation updates recreates one-shot fragility.
- Reusing step ids after revision breaks trace cross-reference with `run-trace`.
- Plans in chat only — not auditable; always persist to `.agent-loom/plans/`.

---

## Output Format

```markdown
## Structured plan — [task_id]

Plan file: `.agent-loom/plans/[task_id].md`
Steps: N total | done: N | pending: N | failed: N

Current step: **Sx** — [goal]
Observation: [actual vs expected]

Delta (if any): [step] [from→to] — [reason]

Next: execute **Sy** | invoke dynamic-routing | complete
```

---

## Examples

Teaser: 4-step API feature → full plan written → S1 done (migration applied) → S2 preconditions updated after observing schema conflict.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Planning is overhead" | Rework from a failed one-shot costs more. |
| "I'll keep the plan in my head" | Not handoff-safe; write the file. |
| "Execute all steps then fix" | Violates commit-one; observations won't flow. |
| "process-decomposer already planned" | That produces process entries; this is runtime execution state. |
| "problem-to-plan wrote a plan doc" | docs/plans/ is spec; this is live execution tracking. |

## Verification

- [ ] Plan file exists at `.agent-loom/plans/<task-id>.md`
- [ ] plan_lint.py passes
- [ ] Only one step executed per cycle
- [ ] Delta log updated on revision

## Red Flags

- Multi-step work with no plan file
- Failed step without delta log entry
- Blind retry of same action after failure

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 1 family)

## Impact Report

```
Plan: [task_id] | Steps: N/M done | Lint: [pass/fail] | Current: [step id]
```
