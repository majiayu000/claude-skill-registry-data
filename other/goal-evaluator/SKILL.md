---
name: goal-evaluator
description: "Evaluate a FlowGoal against its evidence ledger: run every deterministic verification command first, dispatch the goal-evaluator-judge only for fuzzy criteria, then return a structured verdict and write non-terminal lifecycle updates. Use when /flow:goal evaluate runs, when the Stop hook fires in evaluator-loop mode, or when /flow:start Phase 4 or /flow:debug converts AC evidence into a verdict. A lifecycle transition without deterministic evidence is silent premature completion."
allowed-tools: Bash, Read, Edit, Agent
agent: general-purpose
---

# Goal Evaluator

## Contract

Iron law: deterministic checks beat LLM judgment: run every `verification_command` first and never substitute judge output for a runnable command's exit code. Invoked by `/flow:goal evaluate <id>` and `/flow:debug` step 6 (`trigger=command`), and by `hooks/scripts/flow-goal-evaluator.sh` in evaluator-loop mode (`trigger=stop-hook`), with goal id, run id, and trigger. Returns `{verdict, confidence, delta, reason, next_step_hint, criterion_results}` plus, for terminal outcomes, a `proposed_transition`; writes evidence sidecars and non-terminal lifecycle updates, never `last-verdict.json` and never a terminal status. Permitted skips: the judge when no fuzzy criteria remain; the path-boundary check when `constraints.allowed_paths` is unset.

## Inputs

1. **Goal id**: `.flow/goals/<id>.goal.yaml` with status `active` (or resumable `waiting_for_user`, `waiting_for_ci`, `blocked`). Never read through a symlink: when `bin/flow-mkdir.sh --check .flow/goals` refuses, or the goal file is a symlink, there is no goal to evaluate — it belongs to the link's target.
2. **Run id**: for `.flow/runs/<run-id>/evidence/`; defaults to the goal's `scope.run_id`.
3. **Trigger**: `manual | stop-hook | command`.

## Outputs

1. Updated goal: AC `status` (`pending → evidence_collected → pass | fail`), `evidence_ref`, `last_evaluated_at`, `last_result`; `lifecycle.last_evaluation`; non-terminal `lifecycle.status`.
2. `*.evidence.yaml` sidecars via `bin/flow-record-evidence.sh` (the `goal-evidence-ledger` skill).
3. A `goal-evaluation` journal artifact.
4. The structured verdict, returned to the caller.

## Workflow

### Step 1: Load

Read the goal, confirm it matches `schemas/v1/goal.schema.json`, and read existing sidecars for ACs that already carry `evidence_ref`.

### Step 2: Deterministic checks

For each AC with a `verification_command`: run `bash -c "<command>"`, capture stdout/stderr and the exit code, write a `command_result` FlowEvidence with `proves: [<AC.id>]` and `limitations` (criterion-verification-map's "Does NOT promise" field when present), then update the AC entry (`status: evidence_collected`, `evidence_ref`, `last_evaluated_at`, `last_result`).

### Step 3: Deterministic verdict

All `must_pass` ACs exit 0 → `pass`; any `must_pass` AC non-zero → `fail`; any AC without a command → `incomplete` (judge required).

### Step 4: Path boundary

When `constraints.allowed_paths` is set, run `git diff --name-only`; any file outside the globs → write a `path_boundary_check` sidecar (`proves: []`, violating filenames) and set the candidate to `blocked` with reason `path_boundary_violation`.

### Step 5: Judge (conditional)

Dispatch `Agent(goal-evaluator-judge)` only when `evaluator.type == hybrid` and fuzzy criteria remain, or when `evaluator.type == flow_verdict_judge` and the user invoked `/flow:goal evaluate`. Pass the outcome + AC table, sidecar paths, the evidence bundle (`references/evidence-bundle-format.md`), and `denied_context` verbatim. The judge returns verdict, confidence, delta, next_step_hint.

### Step 6: Lifecycle update

Map the candidate and judge verdict to a status with the table in `references/goal-lifecycle-transitions.md`.

**Non-terminal transitions** (`active`, `blocked`, `waiting_for_user`, `waiting_for_ci`): set `lifecycle.status`, increment `turns_evaluated`, set `last_evaluation = {result, reason, at}`, and write immediately via `bin/flow-goal-record.sh --update-lifecycle`.

**Terminal transitions** (`achieved`, `failed`, `cancelled`): the skill does NOT write them. Return `proposed_transition: {to, reason, turns_evaluated}` and leave the persisted status non-terminal; the caller is responsible for invoking AskUserQuestion and, on confirmation, calling `bin/flow-goal-record.sh --update-lifecycle`. The Stop-hook evaluator-loop cannot ask: it records the verdict and approves the stop with a hint to run `/flow:goal evaluate <id>`. It writes one terminal status itself, `failed`, on stuck detection and when the turn budget is used up on a turn that would block again (`references/goal-lifecycle-transitions.md`).

### Step 7: Journal

`bin/journal-record.sh --issue {N} --type goal-evaluation --metadata goal_id=<id> --metadata result=<status> --metadata evidence_bundle=<run-dir> --metadata failures=<comma-list or none>`.

### Step 8: Return the verdict (the skill does NOT write `last-verdict.json`)

Return verdict, confidence, delta, reason, and next_step_hint. The caller, `commands/goal.md` (`source: "command"`) or `flow-goal-evaluator.sh` (`source: "evaluator-loop"`), invokes `bin/flow-record-verdict.sh` and treats a helper failure as non-fatal. One owner per write; two writers race and the last one wins.

### Step 9: Stuck detection (stop-hook only)

When `trigger == stop-hook` and the pass-set is unchanged for `flow.goals.failAfterStuckTurns` consecutive turns (default 3), propose `failed` with reason `stuck_no_progress`.

## Rules

- No AC reaches `pass` without an `evidence_ref`.
- No lifecycle write without a `goal-evaluation` artifact.
- Never run the judge when deterministic checks suffice; never skip the path-boundary check when `allowed_paths` is set.

## References

- `plugins/flow/agents/goal-evaluator-judge.md`: the judge; inherits verdict-judge's Independence Protocol.
- `plugins/flow/references/goal-lifecycle-transitions.md`: verdict-to-status table.
- `plugins/flow/bin/flow-record-verdict.sh`: the caller-owned `last-verdict.json` writer.
