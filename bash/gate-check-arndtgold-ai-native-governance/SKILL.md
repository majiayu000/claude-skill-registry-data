---
name: gate-check
description: "Use this skill for this scope: delivery control and gate readiness. Boundary: delegates drafts; never approves or skips gates. The requested effect, not discovery, decides AGDF activation."
---

# gate-check

## Purpose

After Request Activation, dispatch the earliest canonical gate or internal step; non-authorizing.

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

## Route Boundary

Selected operation:

- Active-run lists use `control.doctor` all-active inspection; see the Request Activation contract.
- `skill.gate-check`: dispatch first; changes use `intake`. No prior repository/control inspection.
- `delivery.start`: resolve target once; unresolved: orient and stop. Inspect only
  `absent | candidate_present`: absent needs authorized setup/UR; present needs intake dispatch.
  Stop on mismatch; no legacy live run or proxy.

Unbound changes: intake without `run_id`. Match original scope against candidate URs at
`resolve_delivery_run`: unequivocal match -> resume ID + `expected_revision_id`; independent scope ->
new unused ID. Recency, candidate count, shared files or `AGDF_RUN_ID` cannot bind scope. Ask only
about genuinely overlapping work, never start with Run IDs. Invalid inventory blocks assignment.
Use revisions returned by `run-create`/`run-step`; new scope needs durable UR approval.
After `run-approve` returns `outcome: approved`, redispatch the same target/run immediately with
`continue_delivery: true`. `control.gate_route` identifies the current gate and responsible skills;
Use `continuation.skill_id` per interaction policy; stop at decisions/blockers.

## Executable Dispatch

UR content is delegated through `phase: ur_definition` to `ur-definition`; never draft it here.
PRD content is delegated through `phase: prd_definition` to `prd-definition`; never draft it here.
SD content is delegated through `phase: sd_definition` to `sd-definition`; never draft it here.

Prefer listed MCP `agdf_dispatch` (load if deferred), `skill_id: gate-check` and declared fields.
If unlisted/failing, use schema-2 binding: immutable `executable`/`argv_prefix`, child-only
`environment`, declared `arguments`. Quote shell data; CLI revision uses `--revision`.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Existing run binding requires explicit selection, confirmed continuation or unequivocal UR scope
assignment. Never construct or repair a runtime.

For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
`gate-check` has deterministic-control dispatch. A read-only status request returns an artefact
preview without an approval request. Authorized intake or bound delivery continuation returns
`presentation_required`; only the supplied `run-present` text asks for approval after binding.
`host_action.text` contains the preview or recovery for terminal results.
Dispatch is non-authorizing. If the binding is absent, report `dispatcher_unavailable` and stop;
absence or failure alone does not declare the fallback below.

## Declared `instruction_only` Fallback

Only explicit trusted `instruction_only` runtime evidence enables fallback. Load needed modules:

- `../../meta/contracts/task-target-resolution.md`
- `../../meta/contracts/gate-transition.md`
- `../../meta/contracts/gate-artifact-preparation.md`
- `../../meta/contracts/interaction.md`
- `../../meta/contracts/control-scaffold.md`
- `../../meta/contracts/modes.md`
- `../../meta/contracts/quality.md`

Apply directly; do not duplicate tables or procedures. Fallback grants no authority.

For `prepare_gate_artifact`, follow its runtime contract with the supplied gate and bound paths;
canonical evaluation owns eligibility.
