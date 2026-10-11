---
name: code-review
description: "Use this skill for this scope: evidence dimension: review the actual diff for defects, regression and security findings. Boundary: supports Quality Readiness; does not replace QA. The requested effect, not discovery, decides AGDF activation."
---

# code-review

## Purpose
Produce the mandatory Code Review Report (CR) for a relevant run.

It answers:

- whether the changed code shows functional defects, security issues, regression risks, or maintainability problems that matter
- whether findings are blocking, revisable, or advisory
- which concrete evidence in files, diffs, tests, or runtime observations supports each finding
- which issues must be fixed before QA
- whether Brownfield, TP, or clean-review follow-up remains open

## Runtime Contract
Use `continuation.runtime_contracts` after `skill_continuation`. If absent: listed MCP `agdf_inspect` (`operation: contract`, `module: <name>`); else supplied schema-2 executable/argv_prefix[0] `contract --module <name>`; else bundled files below. MCP reads need no hook or shell. Missing module: stop; never infer/search for runtime.

- `../../meta/contracts/quality.md`
- `../../meta/contracts/context-graph.md`

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

Use listed MCP `agdf_dispatch` (load deferred; host prefix allowed): `skill_id` `code-review`, `presentation_language`, `working_directory`, and only bound `target_source`/`primary_target` and `run_id`. Never search unlisted tools.
If absent/failing: supplied schema-2 executable, child-only environment, immutable argv_prefix, declared arguments; `--skill code-review`, language and working directory.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Quote shell values as data.
For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
On skill_continuation use only its target/control. Without that tool and a valid binding: `dispatcher_unavailable`; no runtime search, environment repair
or help retries. Dispatch never authorizes.

Code-review-specific output must make actual findings, missing review scope, evidence strength, and the next required step visible.
Applicable findings must use `../../meta/contracts/quality.md` §Normalized Review Gaps. Concrete diff
defects remain Code Review findings; missing upstream constraints route to their authoritative owner.

## Rules
1. Review the actual diff and impacted code, not intent alone.
2. Findings require concrete evidence.
3. Prioritize correctness, safety, data integrity, compatibility, and maintainability over style.
4. Do not generate style-only noise.
5. Missing review scope or evidence must stay visible.
6. Brownfield owners and existing conventions are binding unless deviation is justified.
7. Distinguish blocking defects from fixable review findings.
8. CR does not grant QA pass.
9. Do not turn Code Review into a static requirements checklist or invent missing upstream constraints.
10. A genuinely new implementation risk uses `emergent_risk` with an explicit earliest-owner assessment.
11. Missing, unknown or contradictory classifications fail closed and stay open.

## When To Use
- after `CD+Tests`
- before `QA`
- when code changes exist
- when multiple agents or contributors touched the same area
- when a commit-near change needs explicit review evidence

## Inputs
Use what is available:

- changed files and diff
- affected neighbouring code
- test/build results
- Brownfield Analysis
- Task Plan and TP Review
- Clean Implementation Review
- runtime or UI evidence
- known risks or follow-up decisions

If no code changes are present, do not invent a CR result.

## Workflow
1. Inspect the changed files and directly impacted neighbours.
2. Check correctness, edge cases, and error paths.
3. Check security, data handling, and state ownership risks.
4. Check regression and compatibility risks.
5. Check maintainability only where it creates real defect or change-risk exposure.
6. Classify the overall result:
   - `pass`
   - `revise`
   - `block`
   - `not_applicable`
7. Set exactly one required next step.

## Output
Use this compact structure:

```text
## Code Review
Record the decision with the validator's `run-step --step review --decision <pass|revise|block> --evidence`.

- decision: pass | revise | block | not_applicable
- findings:
  - [severity] file/path - issue - evidence
- missing_evidence:
- risks:
- required_next_step:
```

When findings exist, append:

```text
## Normalized Findings
| finding_id | gap_type | routing_target | gap_status | evidence | required_next_step |
|---|---|---|---|---|---|
```

Use the shared Quality Contract for meanings and routes; do not copy its complete mapping here.

## Decision Guidance
- `pass`: no meaningful review finding remains evident in reviewed scope.
- `revise`: fixable correctness, regression, or maintainability issues remain.
- `block`: a hard defect, security risk, data-integrity risk, or unresolved critical uncertainty remains.
- `not_applicable`: no code changes were present for review.

### Compact Chat Output

At `pass`: one line — `Code Review: pass — <one-line summary>`.
At `revise`/`block`: show blocking findings with file references. Full report remains in durable file or inline evidence as specified.

## Forbidden
This skill must not:

- decide final QA
- accept a green build as sufficient review evidence
- hide missing review scope
- generate style-only findings
- duplicate TP Review or QA as if they were the same step
- invent a requirement, design decision or plan obligation to justify a finding
- silently repair or reclassify an invalid normalized finding
