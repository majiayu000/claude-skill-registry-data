---
name: qa-gate
description: "Use this skill for this scope: sole final Quality Readiness decision. Boundary: only instance for `pass | revise | block`. The requested effect, not discovery, decides AGDF activation."
---

# qa-gate

## Purpose
Make the formal QA gate decision.

This skill is the only final QA decision point for `pass | revise | block`.

It answers:

- whether `QA pass` is allowed
- whether the implementation must be revised
- whether a hard blocker remains
- whether relevant TP tasks are sufficiently verified
- whether P0/P1 tasks are complete
- whether Brownfield fit is sufficient
- whether solution integrity is sufficient
- whether blockers, critical risks, or missing evidence remain

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

Use listed MCP `agdf_dispatch` (load deferred; host prefix allowed): `skill_id` `qa-gate`, `presentation_language`, `working_directory`, and only bound `target_source`/`primary_target` and `run_id`. Never search unlisted tools.
If absent/failing: supplied schema-2 executable, child-only environment, immutable argv_prefix, declared arguments; `--skill qa-gate`, language and working directory.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Quote shell values as data.
For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
On skill_continuation use only its target/control. Without that tool and a valid binding: `dispatcher_unavailable`; no runtime search, environment repair
or help retries. Dispatch never authorizes.
For a qa-gate skill_continuation, control.candidate_runs is the complete canonical active-run inventory when run selection is unresolved, otherwise an empty array. Use its run_id, objective, normalized current_gate, decision and revision_id fields as data; filter by current_gate: QA and do not rescan run files, invent candidates or omit returned QA candidates.

QA-specific `decision` is exactly `pass | revise | block`.
`pass` is allowed only when TP coverage, Brownfield fit, solution integrity, and relevant documentation/Context Graph impact are sufficiently evidenced.
`sot_drift` must not pass silently as a warning.
Consume applicable findings through `../../meta/contracts/quality.md` §Normalized Review Gaps.
QA must not maintain a second mapping or reclassify review findings.

When post-CD+Tests review evidence exists, present the Runtime Contract's derived Quality
Readiness projection before the detailed QA report: Plan coverage, Solution integrity, Code
quality and QA decision in that order. Name `qa-gate` as the sole decision owner, show one
decisive reason and one permissible next action, and keep detailed reports as evidence links or
on-demand detail. The projection is non-authorizing and must not replace the Run Status Card,
Gate Transition Card or the durable QA report.

## Resolved Target Run And Evidence Discovery

After the Direct Skill Invocation Preflight resolves one governance target, discover QA context from
that target instead of asking the user to reconstruct repository evidence:

1. Prefer an explicit run identifier only when it belongs to the resolved governance target and
   matches the requested QA scope. Otherwise use the returned canonical candidate inventory.
2. Select exactly one run whose objective matches the request and whose canonical gate state permits
   QA. Validate the selected state through gate-check or the equivalent agent-native control
   inspection.
3. If no eligible run exists, report the current earlier gate or internal step and stop before a QA
   decision. If several runs remain plausible, list only their identifiers and objectives, request
   one run selection and stop before a QA decision. Run clarification is a pre-decision outcome, not
   a fabricated `block` result.
4. From the selected run and its Artefacts/Artefact Chain, resolve and read the approved TP,
   Brownfield Analysis, CD+Tests evidence, Task Plan Review, Clean Implementation Review, Code
   Review, normalized findings, test results and Context Graph state that are present and readable.
5. Treat inaccessible external evidence and missing mandatory artefacts as explicit evidence gaps.
   Do not ask the user to paste or relink repository files that the skill can read itself.
6. Once one eligible QA run is established, evaluate the discovered evidence and emit exactly one
   `pass | revise | block` decision with one permissible next step.

QA owns the Quality Readiness and QA decision only. It must not reconstruct or promise a Run Status
Card, Gate Transition Card, native QA card or interactive QA card. Operational run status and gate
approval orientation remain owned by gate-check and the Interaction Contract.

## Rules
1. No QA pass without strong evidence.
2. TP is the reference, not merely working code.
3. P0/P1 gaps block `pass`.
4. Brownfield fit is mandatory.
5. UI surface integrity is mandatory for UI-impacting changes.
6. Solution integrity is mandatory.
7. After one eligible QA run is selected, always output exactly one decision: `pass`, `revise`, or `block`.
8. Open risks, missing tests, partial TP coverage, or side effects must be visible.
9. Applicable UX Intent Fidelity rows must all be `fulfilled` with suitable visible evidence before `pass`.
10. A `requirements_gap` routes to PRD revision; QA must not invent or accept the missing criterion.
11. Any applicable normalized finding that is `open`, missing, unknown, contradictory or supported by
    insufficient evidence prevents `pass`.
12. A `resolved` finding counts only when its durable review evidence proves the routed correction or decision.

## When To Use
- after `CD+Tests`
- after `code-review`
- after `task-plan-review`
- after `clean-implementation-review`
- before UAT
- before any claim that implementation is done, releasable, or QA-ready
- when evidence from Brownfield, TP, or clean-review skills exists

Important:

- `CD+Tests` is implementation and test status only.
- Without review evidence and TP coverage, `QA pass` is not allowed.

## Inputs
Use what is available:

- approved TP and TP Review
- Brownfield Analysis
- Clean Implementation Review
- `code-review` or Code Review Report
- test/build results
- documentation impact review
- runtime or UI evidence
- known blockers and risks

If evidence is missing, lower the decision accordingly.

## Workflow
1. Resolve the target, select exactly one eligible run and discover its durable evidence.
2. Confirm the relevant gate context and verify TP coverage.
3. Verify P0/P1 completion.
4. Verify Brownfield fit.
5. Verify UX Intent Fidelity when applicable, including visible evidence for visible-behavior claims.
6. Consume normalized findings without reclassification; fail closed on every open or invalid row.
7. Verify solution integrity.
8. Verify tests and evidence strength.
9. Verify documentation and Context Graph impact if relevant.
10. Decide:
   - `pass`
   - `revise`
   - `block`
11. State the single required next step.

## Output
Use this shape:

```text
## QA Gate
- decision: pass | revise | block
- evidence:
- missing_evidence:
- risks:
- required_next_step:
- impact_codes:
```

If Context Graph impact is relevant, include the fields from `../../meta/contracts/context-graph.md`.

### Compact Chat Output

At `pass`: one line — `QA: pass — <one-line summary>`. Reference the durable QA report
path. Do not show the Quality Readiness projection or evidence inventory in chat.
At `revise`/`block`: show the decisive dimension, reason and next action.

## Decision Guidance
- `pass`: required TP tasks are done, evidence is strong, no blocking Brownfield or solution-integrity risk remains.
- `revise`: implementation is plausible but missing evidence, partial tasks, UX gaps, or fixable integrity issues remain.
- `block`: hard prerequisite, approval, product semantics, security/compliance, SoT drift, or critical behaviour is unresolved.

## Forbidden
This skill must not:

- grant QA pass from a green build alone
- hide partial task completion
- replace UAT
- treat missing reviews as completed
- downgrade SoT drift to harmless warning
- silently repair, normalize or reroute a review finding

Apply interaction.md Bounded internal recovery and prepared observation for eligible bound follow-up. It adds no gate or approval authority.
