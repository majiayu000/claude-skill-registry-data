---
name: execution
description: Use to execute tracked multi-step work, a standalone plan, or a roadmap phase. Clear bounded implementation can proceed directly under AGENTS.md.
---

# Execution

Execute authorized work through acceptance, verification and recovery. Beads owns
durable task state; a plan document is not a prerequisite for a clear task.

## Scope selector

| Request | Scope |
|---|---|
| Explicit run-all-remaining-phases request or `/run-phases` | Workstream; read `references/workstream-mode.md` |
| Execute a named roadmap phase | Phase |
| Task, standalone plan, or single-phase epic | Task |
| Clear bounded implementation without a plan | Task; use the request and acceptance as the packet |
| Material scope/behavior unresolved | Resolve that gap through planning or brainstorming |

Carry authorization through necessary fixes; a review finding cannot authorize
scope expansion. Follow the delegation policy in `AGENTS.md`.
Risk labels: `small` is bounded, low-risk work; `standard` is a bounded behavior
change; `deep` is cross-cutting, high-risk, or materially unresolved work.
Small work stays inline. Standard work may stay inline or use one bounded worker
when beneficial. Deep work needs risk-appropriate independent review; separate
spec and quality reviewers only when the task requires them or the risks justify
both. Use configured models/effort; if dispatch is unavailable, continue useful
local work and state any required review that remains unperformed.

For delegated units or multi-round review, read `references/task-engine.md`.
Workspace: `scratchpad/execution/<slug>/`, with a slug that distinguishes full
plan/workstream paths. Capture the starting revision and dirty-file baseline;
pre-existing edits are not automatically part of the task.

## Task loop

1. Read the request, existing plan if any, and Beads description/acceptance.
   Claim the exact task with `--actor "<coding-agent>:<unique-id>"`.
2. Implement in dependency order, within owned paths. Use test-first or
   characterization when risk calls for it; apply security to material boundary
   changes. When a failure's cause is unclear, use `systematic-debugging` and fix
   only a cause it confirms: prove the fix with a regression check when one is
   feasible, rerun the original failing scenario, log each attempt (hypothesis,
   change, result), and after two failed fixes stop and return the log to the
   task owner. Hardening other boundaries the defect exposes is the bug-fix
   playbook's step, and so is a top-level request to fix a bug: at top level
   return to `mvp-mode`; inside a delegated task, report that route to the parent.
3. Validate findings as they arrive. Fix confirmed in-scope defects, answer
   incorrect findings with evidence, and record unresolved decisions. Do not
   spend fix rounds implementing unverified feedback.
4. Run applicable project/plan checks and inspect the scoped final diff. Reuse
   valid evidence while its code, inputs and environment remain applicable.
   Small work needs no mandatory reviewer pair. Independent review is driven by
   explicit requirements or unresolved risk, not the act of closing a task.
5. Close with evidence and material limitations in `--reason`; report the result.
   Create durable follow-up work for discoveries outside scope, linked to origin.

For a task epic, map plan tasks to its stage IDs and use the phase close gate.

## Phase loop

1. Resolve the supplied or unambiguous roadmap and read this phase's deliverables,
   spec references, acceptance, risk and exit criterion. Query
   `bd list -t epic --all --spec docs/workstreams/<name>/ --json`: exactly one
   epic title must start with `[<phase-id>]`. The roadmap anchor (`spec_id`) is
   authoritative.
   Zero/duplicate matches are a tracking defect; do not silently re-seed.
2. Confirm the epic is not already closed, check blockers and claim the phase.
   Elaborate a deep phase when its packet
   needs a plan; reuse approval covering this work rather than pausing again.
3. Select a ready direct child from `bd ready --parent <epic> --json`, keeping
   only beads whose `parent` is the epic (the query returns every descendant),
   then call the
   contractor: `uv run python -m workflow_interpreter.foreman --config <foreman-config.toml> contract <epic_id> <stage_id>`.
   The contractor claims atomically and owns execution through closure; do not
   claim or close the stage separately. Match deep-phase `Stage:` plan tasks to
   stage IDs and dependency order before the call. Correct missing or unmatched
   mappings first.
4. Read the contractor's one JSON result. `phase-exhausted` means proceed to
   the close gate; `blocked` names work to clear or bypass with another ready
   stage; `result` means the stage landed and closed, so render tracking with
   the beads skill's `scripts/bd-render-tracking.sh` where available and
   authorized, then select the next stage. `refused` (exit 2) names an invalid
   request: fix its reason before retrying; exit 1 is a crash to report. Use
   `--trace` for read-only evidence, and `--retry` only to mint an eligible new
   attempt. Never edit generated tracking by hand.
5. **Close gate:** query `bd list --parent <epic> --all --json`; require at least
   one stage and every stage closed. Name unclosed stages on failure. Then run
   the roadmap exit criterion. Close the epic only after both conditions hold,
   recording the actual exit evidence.

If the governing plan changes or code invalidates the chosen approach, reconcile
before dependent work continues. Preserve completed work on failure. An unresolved
stage or failed phase exit blocks phase completion and any dependent phase.
Commits, publication and broader work retain their existing authorization gates.

## Independent child workflows

For parallel independent graphs, the orchestrator chooses inputs, models and
an admitted coordination owner; the foreman makes one declared decision per
tick, the inspector contains activations, and the crew runs its vendor CLI.
Follow `docs/usage/children.md` for bounded `admit`,
`drive`, `status` and `collect`. Collection is evidence, not stage closure.
Select receipts with `integration prepare`, then use the contractor's `contract`
command for combined review, checks and landing (`docs/usage/contractor.md`).
Replace a changed graph/model through trusted `children replace`; ordinary
decisions retain admitted pins and human gates. Do not invent child dependencies
or automatic result binding.
