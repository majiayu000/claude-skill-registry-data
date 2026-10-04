---
name: dynamic-routing
description: >
  Select alternative execution paths when a plan step fails — branch on
  outcomes instead of blind retry. Load when a structured plan step fails,
  an unexpected observation arrives, or the user asks what to try next
  after an error. Also triggers on "try another approach", "route around
  this failure", "replan on failure", "if X fails try Y", or outcome-based
  branching during multi-step work. Pairs with structured-planning and
  debug-and-fix. Does not replace root-cause debugging — adds plan-level
  path selection.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: DyFlow NeurIPS 2025, GAP arXiv 2510.25320, NaviAgent arXiv 2506.19500, model-selection tier escalation (agent-loom upgrade Phase 2)
  resources:
    references:
      - ROUTE-PATTERNS.md
      - examples.md
---
# Dynamic Routing

When a step fails or observation ≠ expected, you **reflect, branch, and revise the plan** — never blind-retry the same action. Output is an updated plan delta + chosen alternate path.

## Hard Rules

Ground reflection in step evidence — cite tool output, error message, or test failure.
Blind retry of the identical action is forbidden unless the reflection identifies a transient cause (network, rate limit) with a documented backoff.
Every route decision appends to the plan's **Plan delta log** in `.agent-loom/plans/<task-id>.md`.
Prefer **path recombination** (insert/replace remaining steps) over full replan when <50% of steps remain.
If failure is a bug in existing code, route to `debug-and-fix` before resuming the plan.

---

## Workflow

### Step 1 — Capture failure context

From the failed step: `step_id`, expected vs actual, error text, layer (tool/env/code/plan).

### Step 2 — Structured reflection (3 lines max)

```markdown
Hypothesis: [cause grounded in evidence]
Layer: [plan | tooling | code | environment]
Actionability: [plan revision | debug-and-fix | escalate user]
```

### Step 3 — Select route

Read `references/ROUTE-PATTERNS.md`. Pick one:

| Route | When |
|-------|------|
| **Alternate tool** | Same goal, different tool/path |
| **Decompose** | Step too large — split into Sx.1, Sx.2 |
| **Rollback + revise** | Prior step assumption wrong — mark prior `revised`, insert fix step |
| **Escalate model tier** | Executing model tripped a `model-selection` tripwire (same test failed 2x, 3 attempts at one fix, unscoped design question) — announce the tier switch; the HUMAN changes models (advisory, per model-selection) |
| **Abort** | Goal infeasible with current constraints — mark `aborted`, stop |
| **Debug handoff** | Root cause unclear — `debug-and-fix`, resume plan after fix |

### Step 4 — Update plan

1. Mark failed step `failed` or `revised`.
2. Insert/replace pending steps.
3. Append delta log row.
4. Run `structured-planning` lint via `plan_lint.py`.

### Step 5 — Resume

Return control to `structured-planning` at the new first pending step.

---

## Gotchas

- Retrying without changing inputs is not routing — it's a loop.
- Full replan discards useful done steps — patch the remainder.
- Environment flakes need explicit transient tag + max 1 retry with backoff.
- Tier escalation is advisory: announce `switch to [tier/model]` and WAIT — never assume the harness can switch models itself. Tier escalation (who executes) and path revision (what to do) are separate decisions; they can combine.

---

## Output Format

```markdown
## Dynamic route — [task_id] / [step_id]

Reflection:
- Hypothesis: [...]
- Layer: [...]

Route chosen: [alternate tool | decompose | rollback+revise | abort | debug handoff]

Plan delta:
| at | step_id | from | to | reason |
|----|---------|------|-----|--------|
| [...] |

Resume at: **Sx** | Handoff: debug-and-fix | Aborted
```

---

## Examples

Teaser: S2 migration fails (table exists) → route decompose → S2.1 check schema, S2.2 apply delta only.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Retry might work" | Same inputs → same failure. Change the path. |
| "Replan from scratch is faster" | Loses done-step evidence and trace links. |
| "Error is obvious" | Write the hypothesis anyway — audit trail. |
| "Skip delta log" | Next agent won't know why the plan changed. |
| "Debug later" | If layer=code, debug now before continuing plan. |

## Verification

- [ ] Reflection cites step evidence
- [ ] Plan delta log updated
- [ ] No identical blind retry
- [ ] plan_lint.py passes after revision

## Red Flags

- Same action repeated after failure
- Plan revised without delta log entry
- Code bug worked around in plan without debug-and-fix

## Prune Log
Last pruned: 2026-07-08
- Added Escalate-model-tier route wired to model-selection tripwires (agent-loom upgrade Phase 2)

## Impact Report

```
Route: [task_id]/[step_id] | Decision: [route type] | Resume: [step or handoff]
```
