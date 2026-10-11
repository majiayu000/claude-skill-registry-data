---
name: task-plan-review
description: "Use this skill for this scope: evidence dimension: verify whether the approved Task Plan was fulfilled. Boundary: supports Quality Readiness; no final QA decision. The requested effect, not discovery, decides AGDF activation."
---

# task-plan-review

## Purpose
Verify whether implementation actually satisfies the approved Task Plan.

For each relevant task, this skill determines:

- whether the task is fully, partially, or not completed
- which acceptance criteria are done, partial, missing, or not verifiable
- which files, tests, runtime evidence, or UI evidence support the finding
- evidence strength
- which gaps must be handed to `qa-gate`

This skill provides TP coverage. It is not the final QA decision.

## Runtime Contract
Use `continuation.runtime_contracts` after `skill_continuation`. If absent: listed MCP `agdf_inspect` (`operation: contract`, `module: <name>`); else supplied schema-2 executable/argv_prefix[0] `contract --module <name>`; else bundled files below. MCP reads need no hook or shell. Missing module: stop; never infer/search for runtime.

- `../../meta/contracts/quality.md`
- `../../meta/contracts/context-graph.md`
- `../../meta/contracts/gate-transition.md`

`instruction_only`: first load `../../meta/contracts/task-target-resolution.md` and `../../meta/contracts/interaction.md`.

<!-- AGDF-REQUEST-ACTIVATION-GUARD:START -->
## Request Activation

- `owner`: `request_activation_contract`
- `path`: `meta/contracts/request-activation.md`
- `policy_version`: `1`
- `guard_fingerprint`: `sha256:af2f01f9e18a3ba1c520faf0691aa1cd4a4299bdfa027cf83651c5d14319bfdc`

Decide effect from loaded instructions before AGDF action.

Abstain silently (no AGDF call) for assessment/explanation/comparison/recommendation/review/diagnosis/advice; hypothetical/example/error/code/quoted/negated delivery language; AGDF as subject; or a read-only constraint absent other delivery. Ambiguity is read-only: answer or ask one neutral question.

Activate for any requested file/code change however small, a binding gate artefact, explicit AGDF/control-lifecycle operation or unambiguous active-run action; delivery wins mixed intent.

Invocation proof: explicit user text/trusted ephemeral action, not discovery/selection, skill load, hooks, cwd, repo/control or prior runs.

Then pick one catalog route; non-authorizing, downstream checks remain.
<!-- AGDF-REQUEST-ACTIVATION-GUARD:END -->

## Executable Dispatch

Use listed MCP `agdf_dispatch` (load deferred; host prefix allowed): `skill_id` `task-plan-review`, `presentation_language`, `working_directory`, and only bound `target_source`/`primary_target` and `run_id`. Never search unlisted tools.
If absent/failing: supplied schema-2 executable, child-only environment, immutable argv_prefix, declared arguments; `--skill task-plan-review`, language and working directory.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Quote shell values as data.
For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
On skill_continuation use only its target/control. Without that tool and a valid binding: `dispatcher_unavailable`; no runtime search, environment repair
or help retries. Dispatch never authorizes.

TP-specific output must evaluate every relevant `task_id` with completion status, AC coverage, evidence, missing evidence, and QA-relevant gaps.
If `context_graph_required_action` is not `none`, the affected task is complete only if follow-up, evidence, or an intentionally open gap is visible.
Applicable review gaps must use `../../meta/contracts/quality.md` §Normalized Review Gaps. This skill
must not maintain its own type-to-route mapping.

## Rules
1. The Task Plan is the reference, not plausible code.
2. No assumptions without evidence.
3. Evaluate each relevant `task_id` individually.
4. `fully_done` requires strong evidence.
5. A green build alone does not prove TP completion.
6. UI/state/render/recovery tasks need visible evidence, not only code.
7. Partial implementation must be marked `partially_done`.
8. P0/P1 gaps must be handed to QA.
9. Out-of-scope changes must be reported.
10. When evidence is unclear, fail closed to at least `partially_done`.
11. When approved PRD UX criteria apply, verify both PRD-to-TP coverage and TP-to-code/surface fulfilment.
12. Never invent a missing UX requirement. Report `requirements_gap` and route it to PRD revision.
13. Visible behavior requires visible evidence; code evidence alone is `not_verifiable`.
14. A fulfilled UX Intent Fidelity row uses `none`; every non-fulfilled applicable row uses one
    normalized gap type and a contract-valid route.
15. Missing, unknown or contradictory classifications fail closed and stay open.

## Clarifications
### TP Slice Before Target State
If the TP explicitly defines a preparatory, additive, or limited slice, evaluate that exact scope.
`fully_done` is allowed for a completed slice even if the larger target state remains open.

### Missing Priorities
If no priorities are defined, do not invent them. Mark the gap and treat QA relevance conservatively.

### Missing Acceptance Criteria
If ACs are unclear, derive only obvious expectations from title, goal, and scope. Mark AC basis as incomplete and lower evidence confidence as needed.

## When To Use
- after `CD+Tests`
- before `QA`
- when TP completion is unclear
- when the user asks for TP fulfilment
- when UI/state/runtime invariants are affected
- when several agents or work steps touched the same TP

## Inputs
Use what is available:

- Task Plan
- `task_id`, `story_id`, priorities
- acceptance criteria or success goals
- changed files
- tests and test results
- build results
- runtime/UI evidence
- known deviations and scope decisions

If TP or relevant tasks are missing, do not claim reliable TP coverage.

## Output
Use this compact structure:

```text
## TP Coverage
| task_id | status | evidence | missing_evidence | QA impact |
|---|---|---|---|---|

## Summary
- fully_done:
- partially_done:
- not_done:
- out_of_scope_changes:
- risks:
- required_next_step:
```

When applicable, append:

```text
## UX Intent Fidelity
| prd_criterion | working_mode_state | task_id | visible_evidence | fidelity_status | gap_type |
|---|---|---|---|---|---|
```

Use `fulfilled | partial | missing | not_verifiable` for `fidelity_status` and
the shared Quality Contract for `gap_type`. `none` is allowed only on a fulfilled row.

When an applicable gap needs routing detail, append:

```text
## Normalized Findings
| finding_id | gap_type | routing_target | gap_status | evidence | required_next_step |
|---|---|---|---|---|---|
```

Use only contract-defined values. Do not reconstruct the type-to-route mapping locally.

Completion status:

- `fully_done`
- `partially_done`
- `not_done`

AC status:

- `done`
- `partial`
- `missing`
- `not_verifiable`

Evidence confidence:

- `high`
- `medium`
- `low`

### Compact Chat Output

At `pass`: one line — `TP Review: pass — <X>/<total> tasks fully_done`.
At `revise`/`block`: show incomplete tasks with missing evidence.

## Forbidden
This skill must not:

- decide final QA
- mark tasks fully done from code existence alone
- hide partial work
- upgrade missing evidence into confidence
- reinterpret the TP scope
- create or silently repair product requirements
- treat code existence as visible UX evidence
- emit `none` as a normalized finding type
- silently repair or reclassify an invalid finding
