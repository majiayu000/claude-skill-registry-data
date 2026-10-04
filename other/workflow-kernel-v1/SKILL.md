---
name: assistant-workflow
description: "prepare/technical preparation; plan/build; implement/fix; migrate/refactor; resume persisted task state."
---

# Development Workflow

- On stale, superseded, or completed state, update `{agent_state_dir}/task.md`
  before acting: classification, reason, task identity, exact next action.
- RED -> GREEN -> verification. Build repair owns failures; Review
  review-fix/re-review; Document is the sole owner of `final_handoff`.

- Explicit user or repository artifact schemas override workflow-internal shapes; preserve exact paths, keys, types, ids, and supplied literals.
## Contract Loading

Read `contracts/index.yaml`: `entry`, `current_phase`, `selected_handoff`, and
`completion`. `feature_preparation`:
repository-grounded existing behavior: inspect requirements, design, current implementation, and behavioral tests before classifications/questions.
`architecture_design` runs on Pack trigger; pending quality scenarios keep verification_ref absent. Invalid selectors: `load_full_authoritative_file`; record recovery.
Phase: `references/phases.md`; routing:
`references/workflow-controller.md`; `progressive_discovery`:
`references/progressive-discovery.md`.

- `delegation` before dispatch for indexed role/trigger fields.
v4 uses `subagent_trigger_scope`; `verification_command` is non-empty argv
`string[]`; persisted Reviewer/QA wrappers bind current
`producer_schema_version` and rebuild on mismatch.

## Execution

1. Triage size/risk/gates/state/lane/QA/delegation. `plan_mode`:
   `none` skips Plan, `inline` is concise, and
   `approval_required` waits for approval before Build.
2. Preparation-only: typed result, no execution evidence. Build verifies
   slices; QA needs trigger; document handoff.

## Output

Small work returns status, changed areas, compact acceptance/verification.
