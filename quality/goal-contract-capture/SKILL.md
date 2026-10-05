---
name: goal-contract-capture
description: "Capture a FlowGoal contract as `.flow/goals/<id>.goal.yaml` — outcome, acceptance criteria with verification commands, specification (non-goals, failure modes, interface contracts, risk map), constraints, evaluator binding, continuation policy, lifecycle. Use when /flow:start passes the Spec Validation Gate, when /flow:goal create runs, or when /flow:debug confirms a hypothesis. Acceptance criteria alone are not a contract: without an evaluator binding and boundaries the Stop hook cannot enforce evidence and goals cannot resume."
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
agent: general-purpose
---

# Goal Contract Capture

## Contract

Iron law: no `.flow/goals/<id>.goal.yaml` without an evaluator binding, and no contract element invented: every specification element is lifted from the journal or escalated. Invoked by `/flow:start` (Phase 1, after the Spec Validation Gate), `/flow:goal create`, and `/flow:debug` (after the confirmed hypothesis) with a goal id, scope, source, and invocation reason (`start | goal-create | review | address | debug`). Returns the written goal path plus a `goal-created` journal artifact; the caller then invokes `goal-lifecycle`. Permitted skips: `review` and `address` invocations skip the specification block (they inherit the issue's capture); `goal-create` with no linked issue skips the journal artifact. Nothing else may be skipped.

## Inputs

1. **Goal id**: `issue-{N}`, `pr-{N}-review`, `pr-{N}-address`, or an ad-hoc slug matching `^[a-z0-9][a-z0-9-]{0,63}$`.
2. **Scope**: `repo`, `branch`, optional `issue`/`pr`, optional `journal` path (`<journal dir>/issue-{N}.md`, the journal dir being what `bin/journal-dir.sh` prints).
3. **Source**: issue body, PR description, or user-supplied outcome.
4. **Invocation reason**: selects the outcome template and `evaluator.type`.

## Outputs

`.flow/goals/<id>.goal.yaml` conforming to `plugins/flow/schemas/v1/goal.schema.json`, written only through `bin/flow-goal-record.sh --create --goal-file <composed.yaml>` (atomic, O_NOFOLLOW-defended, schema-validated), plus `bin/journal-record.sh --issue {N} --type goal-created --metadata goal_id=<id> --metadata source=<src>`.

## Workflow

1. **Pre-flight**: if the goal file exists with `lifecycle.status` outside `{cancelled, failed}`, stop and raise the six-field escalation (`references/escalation-format.md`). Never overwrite an active goal.
2. **`metadata`**: `id`, `created_at` (ISO-8601 UTC), `created_by` (invoking command), `owner` (git `user.email` or `@me`).
3. **`scope`**: from inputs; leave `run_id` unset (run-state-management fills it).
4. **`objective`**: `outcome` by reason: `start`: "Issue #{N} is implemented and verified."; `review`: "PR #{N} review completed with findings posted or no-finding evidence recorded."; `address`: "All unresolved findings on PR #{N} are resolved, commented, or escalated."; `goal-create`: AskUserQuestion; `debug`: the caller's template. Each AC comes from `criterion-verification-map` output with `status: pending`, `evidence_ref: null`, and its `verification_command` when one exists.
5. **`specification`**: lift from the journal's `## Specification` section written by `specification-capture`: `non_goals` from `### Non-goals`, `failure_modes` from `### Failure modes`, `interface_contracts` from `### Interface contracts`, and `risk_map` from the `### Risk map` table, where each row `Area | Plausible wrong version | Discriminating check` becomes `{area, plausible_wrong_version, discriminating_check}`. When the journal has no `### Risk map`, omit the `risk_map` key. Never invent rows or fill an empty block with placeholders; an empty non-goals, failure-modes, or interface-contracts block is a six-field escalation.
6. **`constraints`**: `tdd_required`, `require_all_pass`, `no_calendar_estimates`, `no_tier3_without_confirmation` all `true`; `denied_paths` from `flow.goals.denied_paths`; `allowed_paths` only when the goal narrows scope.
7. **`evaluator`**: `type: flow_verdict_judge` (`hybrid` when fuzzy criteria exist, `deterministic` when every AC has a command), `command: /flow:goal evaluate`, `judge_agent: goal-evaluator-judge`, `evidence_bundle_format: plugins/flow/references/evidence-bundle-format.md`, `denied_context: [implementation_rationale, self_review_findings]`.
8. **`continuation`**: `mode: flow_managed`, `on_incomplete: continue_next_activity`, `on_blocked: six_field_escalation`, `on_complete: mark_achieved`, `max_iterations` from settings (default 20).
9. **`lifecycle`**: `status: active`, `current_phase` by reason (`start`: explore, `review`: fan-out, `address`: categorize, `debug`: fix), `current_activity`, `turns_evaluated: 0`, `last_evaluation: {result: incomplete, reason: "Goal created; evidence not yet collected.", at: <now>}`. Never `achieved` at creation.
10. **Write, record, verify**: run the helper, surface any non-zero exit with its stderr, append the journal artifact, then read the file back and confirm it parses and matches the schema.

## Trust

`bin/flow-goal-record.sh --create` also records the goal in the per-user trust ledger (`goal-trust.jsonl` in the per-user state directory `bin/cascade-resolve.sh --state-dir` names, via `bin/flow-goal-trust.sh record`). The Stop hook executes a goal's verification commands only when the goal is trusted or `flow.goals.executeVerificationCommands` is true. A goal is trusted only when it was created through flow in this user's environment; a goal that arrived with a checkout is not. Editing a `verification_command` by hand changes the hash and untrusts the goal until you run `bin/flow-goal-trust.sh record --goal-file .flow/goals/<id>.goal.yaml`.

## References

- `plugins/flow/skills/specification-capture/SKILL.md`: the journal headings lifted in step 5.
- `plugins/flow/skills/criterion-verification-map/SKILL.md`: AC verification-command shape.
- `plugins/flow/references/flow-goals.md`: full YAML example and settings.
