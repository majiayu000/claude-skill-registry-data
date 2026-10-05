---
name: goal-lifecycle
description: "Enforce the FlowGoal state machine: every `lifecycle.status` transition (draft → active → {waiting_for_user, waiting_for_ci, blocked, achieved, failed, cancelled}) writes the new lifecycle block through `bin/flow-goal-record.sh` AND a `goal-created` or `goal-evaluation` artifact to the decision journal. Use when any code path mutates `lifecycle.status`: /flow:goal pause/resume/clear, the draft → active step after goal-contract-capture, the evaluator's verdict, or the Stop hook's stuck detection. A goal in `failed` with no artifact explaining why is worse than no state machine."
allowed-tools: Bash, Read, Edit
agent: general-purpose
---

# Goal Lifecycle

## Contract

Iron law: no `lifecycle.status` transition without an audit-trail entry — the goal file changes only through `bin/flow-goal-record.sh --update-lifecycle`, and every transition writes a `goal-created` (draft → active) or `goal-evaluation` journal artifact. Invoked by `/flow:goal create`, `/flow:start` Phase 1, and `/flow:debug` for draft → active after `goal-contract-capture`; by `/flow:goal pause | resume | clear`; after `/flow:goal evaluate` confirms a terminal verdict; and by `goal-evaluator` for non-terminal updates. Inputs: goal id, from-state, to-state, reason, trigger (`evaluator | command | hook | user`). Returns the new status once the write and the artifact both succeed. Permitted skips: the run event when `scope.run_id` is unset; the journal artifact for the Stop hook's own `failed` writes (stuck, budget), audited by their run event. Nothing else.

## State machine

Non-terminal: `draft`, `active`, and the resumable `waiting_for_user`, `waiting_for_ci`, `blocked`. Terminal and immutable: `achieved`, `failed`, `cancelled` — new work needs a new goal id. The allowed-transition table with triggers, the disallowed transitions, and the `last_evaluation.result` mapping live in `references/goal-lifecycle-transitions.md`; `bin/flow-goal-record.sh` enforces the same table and refuses anything outside it (including `terminal → any`, `active → draft`, and `blocked → achieved` without passing through `active`).

## Outputs

1. Goal file: `lifecycle.status`, `lifecycle.last_evaluation`, optional `current_phase` / `current_activity`, `turns_evaluated` incremented when leaving `active` for a non-terminal state.
2. Journal artifact: `goal-created` for draft → active, `goal-evaluation` for every other transition.
3. One `lifecycle_transition` event in `.flow/runs/<run-id>/events.jsonl` when `run_id` is set.

## Workflow

1. **Validate** — read the goal. If its status differs from the caller's from-state, another process transitioned it: stop and raise the six-field escalation (`references/escalation-format.md`). Reject a transition outside the table with a stderr explanation and exit 1.
2. **Compose** the lifecycle fragment:
   ```yaml
   lifecycle:
     status: <to>
     current_phase: <preserved or caller-updated>
     current_activity: <preserved or caller-updated>
     turns_evaluated: <incremented when from=active and to is non-terminal>
     last_evaluation:
       result: <pass | incomplete | fail | needs_human_review | blocked>
       reason: <caller-provided; under 200 chars; comma-safe>
       at: <ISO-8601 UTC now>
   ```
3. **Write** — `bin/flow-goal-record.sh --update-lifecycle --goal-id <id> --lifecycle-file <fragment> --from-status <from>`. The helper takes an O_NOFOLLOW lock, replaces only the `lifecycle` block, validates against `schemas/v1/goal.schema.json` when `jsonschema` is installed, and writes tempfile + rename + fsync. Surface any non-zero exit with its stderr; do not retry blindly — a race means re-reading the state.
4. **Journal** — draft → active: `bin/journal-record.sh --issue {N} --type goal-created --metadata goal_id=<id> --metadata source=<src>`. Otherwise: `bin/journal-record.sh --issue {N} --type goal-evaluation --metadata goal_id=<id> --metadata result=<to> --metadata reason=<short>`. Ad-hoc goals with no issue write to the session journal `.decisions/session-{YYYY-MM-DD}.md`.
5. **Run event** — when `run_id` is set, append `{"at","type":"lifecycle_transition","goal_id","from","to"}` to `.flow/runs/<run-id>/events.jsonl`; `bin/flow-record-activity.sh` appends it as part of the FlowActivity the caller records for the phase boundary.

## Rules

- Never edit `.flow/goals/<id>.goal.yaml` directly; never bypass the from-state check.
- Never resurrect a terminal goal.
- Never skip the journal artifact because "the lifecycle block records it" — the goal file is local state, the journal is the cross-PR audit trail.
- Keep `last_evaluation.reason` short; the reasoning lives in the journal artifact body.

## References

- `plugins/flow/references/goal-lifecycle-transitions.md` — transition table, disallowed transitions, result mapping.
- `plugins/flow/references/decision-journal-schema.md` — `goal-created` and `goal-evaluation` artifact rows.
