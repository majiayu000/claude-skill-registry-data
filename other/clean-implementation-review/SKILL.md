---
name: clean-implementation-review
description: "Use this skill for this scope: evidence dimension: inspect whether the solution is structurally clean. Boundary: supports Quality Readiness; not a TP or QA substitute. The requested effect, not discovery, decides AGDF activation."
---

# clean-implementation-review

## Purpose
Evaluate implementation integrity.

This skill answers:

- was the task solved with a clean primary solution
- was the root cause fixed or only masked
- were unnecessary fallbacks, workarounds, guards, defaults, or shims introduced
- were unnecessary parallel structures introduced
- does the solution fit the existing architecture
- is it maintainable or workaround-heavy

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

Use listed MCP `agdf_dispatch` (load deferred; host prefix allowed): `skill_id` `clean-implementation-review`, `presentation_language`, `working_directory`, and only bound `target_source`/`primary_target` and `run_id`. Never search unlisted tools.
If absent/failing: supplied schema-2 executable, child-only environment, immutable argv_prefix, declared arguments; `--skill clean-implementation-review`, language and working directory.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Quote shell values as data.
For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
On skill_continuation use only its target/control. Without that tool and a valid binding: `dispatcher_unavailable`; no runtime search, environment repair
or help retries. Dispatch never authorizes.

Clean-review-specific output must make the primary solution, fallbacks, workarounds, parallel structures, exit criteria, and next cleanup/review step visible.
Applicable findings must use `../../meta/contracts/quality.md` §Normalized Review Gaps. This skill
must distinguish a missing upstream decision from implementation that violates an approved decision.

## Rules
1. Clean primary solution before fallback.
2. Root cause before symptom masking.
3. Fallbacks are exceptions, not target architecture.
4. Every retained fallback needs rationale, target state, and exit condition.
5. No silent parallel structures.
6. Brownfield fit is mandatory.
7. Maintainability matters; "works somehow" is not enough.
8. Async execute paths must not decide product rules again.
9. Shared finalization or merge rules belong in one owner.
10. Missing canonical ownership, fallback policy, exit criteria or parallel-structure decisions are
    upstream gaps; do not invent those decisions during review.
11. Actual code that violates an approved design or plan is an implementation gap.
12. Missing, unknown or contradictory classifications fail closed and stay open.

## When To Use
- after `CD+Tests`
- before QA
- when a solution contains many guards, defaults, or special paths
- when wrappers or helper layers were introduced
- when symptom treatment is suspected
- when fallback, retry, or compatibility-shim logic was added
- when code works but the architecture looks questionable

## Inputs
Use what is available:

- Task Plan
- Code Deliverables
- changed files
- tests and test results
- `code-review` or Code Review Report
- QA Report
- Brownfield Analysis findings
- PRD or SD architecture notes

If evidence is missing, mark it explicitly.

## Workflow
1. Understand the intended change.
2. Identify the primary implementation path.
3. Identify fallbacks, guards, defaults, shims, retries, wrappers, and catch-all branches.
4. Decide whether each is justified.
5. Check for parallel ownership.
6. Check Brownfield fit.
7. Assess whether the implementation fixes the root cause.
8. Assign a decision:
   - `pass`
   - `revise`
   - `block`
   - `not_applicable`

## Output
Use this compact structure:

```text
## Clean Implementation Review
- decision:
- primary_solution:
- evidence:
- fallbacks_retained:
- workaround_or_shim_risk:
- parallel_structure_risk:
- brownfield_fit:
- missing_evidence:
- required_next_step:
```

When findings exist, append:

```text
## Normalized Findings
| finding_id | gap_type | routing_target | gap_status | evidence | required_next_step |
|---|---|---|---|---|---|
```

Use the shared Quality Contract for meanings and routes; do not copy its complete mapping here.

## Pass / Revise / Block Guidance
- `pass`: primary solution is clean, tested, and integrated with existing owners.
- `revise`: solution works but contains avoidable fallback, unclear ownership, or missing evidence.
- `block`: solution creates a second SoT, a second owner, unbounded fallback, or masks unresolved product semantics.

### Compact Chat Output

At `pass`: one line — `Clean Review: pass — <one-line summary>`.
At `revise`/`block`: show the specific fallback/workaround/parallel-structure risk with file references.

## Forbidden
This skill must not:

- accept fallback-heavy logic as target architecture
- hide unjustified workarounds
- treat green tests as proof of solution integrity
- decide final QA
- create a missing design, plan or product decision during review
- silently repair or reclassify an invalid normalized finding
