---
name: brownfield-analysis
description: "Use this skill for this scope: permitted Brownfield Review or preparation before non-trivial existing-system changes. Boundary: clarifies reuse, owners, risks and Mode/Slice; never bypasses control or grants implementation. The requested effect, not discovery, decides AGDF activation."
---

# brownfield-analysis

## Purpose
Ensure delivery in an existing system is Brownfield-oriented, not Greenfield-style.

The skill answers:

- which existing artefacts matter
- what already exists fully or partially
- what can be reused, extended, or refactored
- whether new artefacts are really needed
- architecture, compatibility, migration, and regression impact
- the minimal clean next step
- whether Context Graph impact exists without automatically creating a node

## Runtime Contract
Use `continuation.runtime_contracts` after `skill_continuation`. If absent: listed MCP `agdf_inspect` (`operation: contract`, `module: <name>`); else supplied schema-2 executable/argv_prefix[0] `contract --module <name>`; else bundled files below. MCP reads need no hook or shell. Missing module: stop; never infer/search for runtime.

- `../../meta/contracts/gate-transition.md`
- `../../meta/contracts/modes.md`
- `../../meta/contracts/context-graph.md`
- `../../meta/contracts/quality.md`

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

Use listed MCP `agdf_dispatch` (load deferred; host prefix allowed): `skill_id` `brownfield-analysis`, `presentation_language`, `working_directory`, and only bound `target_source`/`primary_target` and `run_id`. Never search unlisted tools.
If absent/failing: supplied schema-2 executable, child-only environment, immutable argv_prefix, declared arguments; `--skill brownfield-analysis`, language and working directory.
For `--language`: Required presentation language for the latest natural-language user request as one well-formed BCP 47 tag. If the request explicitly asks for a response language, use that tag; otherwise use the dominant request language. Use en when mixed or ambiguous. A valid unsupported tag renders through the complete English pack. Missing or invalid input fails before governance evaluation.
`target_source`: `explicit_target` if request names `primary_target`; `continued_target` if it unambiguously continues confirmed target; `current_repository` if request names this/current repo with one matching repo active. Otherwise omit the pair; cwd has no target authority.
Quote shell values as data.
For a result with `terminal: true`, the entire assistant response must consist only of host_action.text, copied verbatim. Add no question, explanation, heading, citation, link or other surrounding text; do not translate or reformat it; invoke no later tool and stop.
On skill_continuation use only its target/control. Without that tool and a valid binding: `dispatcher_unavailable`; no runtime search, environment repair
or help retries. Dispatch never authorizes.

Brownfield-specific output must make evidence, missing existing-system view, parallel-structure risk, reuse strategy, and the minimal next step visible.
When `.agdf/control/` is present, persist or link `post_ur_review` output under `.agdf/control/artefacts/<key>/BROWNFIELD_REVIEW.md`,
then record the Mode/Slice Decision with the validator's `run-step --step route --route <mode> --reason --evidence`.

## Modes

- `post_ur_review`: use after approved durable UR to size and route the work. Output must decide `quick_task`, `verified_change`, `structured_slice`, `structured_delivery`, or `block` with scope reason and evidence.
- `pre_implementation_analysis`: use after approved durable TP to verify the implementation path before `CD+Tests`. Output must focus on reuse path, owners, regression risk, test impact and minimal clean implementation.

Do not mix both modes silently. Name the active mode in the output.

In `post_ur_review`, also record `delivery_context`, `ui_ux_impact`, `ui_ux_impact_reason` and
`ux_intent_definition_required` using the single classification and routing contract in
`../../meta/contracts/gate-transition.md`. Greenfield records make existing-system evidence explicitly
not applicable; Brownfield records cite repository evidence. Do not create a second Greenfield router.

In the same `post_ur_review`, record architecture relevance before the existing Mode/Slice
Decision. Check only boundaries the proposed change could affect: module or owner, externally
consumed interface, data or source-of-truth ownership, compatibility or migration, runtime or
host contract, and security or policy authority. An unresolved effect on one of these boundaries
is relevant until its evidence owner resolves it. Cite the affected repository paths, contracts
or observed behavior; do not infer relevance from file or owner counts.

For a local change with no material boundary effect or unresolved architecture question, record
`architecture-not-applicable` and the affected code/owner evidence supporting that reason. Do
not require a full architecture checklist or diagram for this route. For a relevant change,
record the boundary, impact, evidence, missing facts and existing owner of the next action in
the same Brownfield Review. Classify each architecture finding in its existing Reuse And
Parallel-Structure Risk row as `problem`, `trade-off` or `unresolved`. A proposed trade-off that
knowingly retains or adds debt is not accepted merely because it is documented: the same finding
must have a rationale, accountable owner, mitigation and finite review date or exit condition.
Until all four are present, leave it unresolved and route the missing decision to its owner.
The Brownfield Review itself must then be at least `revise`; use `block` when the missing
decision prevents a safe Mode/Slice route. Do not report `pass` while claiming that the debt
acceptance is still open.
Use a focused diagram only when it answers a named ownership or dependency question that the
textual evidence cannot settle; link it from the same review.

Architecture evidence informs the sole Structured Depth Decision in `modes.md`; it does not
select a mode independently. If a decisive route fact is missing or conflicting, use the
existing `block` and `depth_facts_missing | depth_facts_conflicting` recovery. Route later gaps
through the normalized owners in `quality.md`; this review grants no downstream approval.

## Rules
1. Brownfield first: understand the existing codebase before PRD/SD decisions when existing-system impact is possible, and again before implementation.
2. Brownfield Review after `Approval: UR`, or before it while the UR card is ready so that card can name the route, is a sizing and routing step. It must visibly decide `quick_task`, `verified_change`, `structured_slice`, `structured_delivery`, or `block` before PRD depth or implementation is chosen. Persist the completed review and its decision, scope reason, evidence and required next gate in the same internal operation; mark the review `done` only after both the artefact and canonical run projection are complete. An interrupted, incomplete or legacy record stays at fail-closed `Mode/Slice Decision` recovery without another user approval.
3. Reuse-before-create: prefer existing modules, services, components, tables, endpoints, tests, and configuration.
4. Minimal clean slice: choose the smallest durable intervention, not merely the smallest technical diff.
5. No silent parallel structures.
6. Existing architecture, naming, error handling, logging, security, and test conventions are binding unless deviation is justified.
7. What is not visibly evidenced does not count as existing.
8. Async execute paths must not become a second product-policy decision point.
9. Visible state ownership must be checked for chat, rendering, scrolling, recovery, and status problems.
10. SoT/runtime/product-semantics drift must be named; if official behaviour must be decided first, recommend UR or equivalent product direction.
11. Large UI surfaces and state hooks must be checked for mixed render, view-model, derived state, orchestration, persistence, and recovery ownership.
12. Context Graph impact must be curated; it is not a review log or version index.
13. Specification archive migrations must follow the archive index if present.
14. In `post_ur_review`, evaluate unchanged compact paths first. For a structured candidate, apply
    only the `Structured Depth Decision` in `modes.md`; do not recreate its trigger/check matrix in
    this skill.
15. A positive structured decision requires `depth_policy_version: 1`,
    `depth_facts_status: complete`, complete evidence for all seven bounded-slice checks, a primary
    reason code, rejected alternative and evidence references. A decisive full-depth trigger may
    support `structured_delivery`; `structured_slice` requires every bounded-slice check to pass.
16. Missing or conflicting decisive facts without an already-evidenced full-depth trigger persist
    the existing `block` decision with `depth_facts_missing | depth_facts_conflicting`, named facts,
    their evidence owner where known, a Brownfield Review link and a precise next action for evidence
    completion and Brownfield/Mode-Slice re-evaluation.
17. Owner, file, consumer, task or derived-path counts must never select a structured depth by
    themselves.
18. In `post_ur_review`, apply the architecture-relevance rules above before the Mode/Slice Decision.

## When To Use
- after `gate-check` permits `Brownfield Review` or the selected canonical run record names Brownfield Review as the next allowed action
- after `gate-check` permits implementation preparation or the selected canonical run record already names Brownfield Analysis as the next allowed action
- after `Approval: UR` when existing owners, SoT, contracts, policies, persistence, runtime paths, tests, UI, UX or architecture may affect PRD/SD scope
- before `CD+Tests`
- before changes to an existing repository
- bug fixes in existing modules
- feature extensions in existing architecture
- refactorings
- unclear existing coverage
- risk of new parallel structures
- a TP is clear but its connection to the existing system is not

## Inputs
Use what is available:

- approved UR, Task Plan, `task_id`, `story_id`
- project structure
- affected files, modules, services, APIs, data models
- existing tests
- architecture notes from PRD or SD
- repository conventions

If inputs are missing, work only from observable evidence and mark gaps explicitly.
If gate status, approval, scope or next allowed action is unclear, stop and route to `gate-check` instead of recommending PRD/SD detail or starting implementation.
When used as Brownfield Review after `Approval: UR`, do not recommend PRD, SD, TP, or implementation until the Mode/Slice Decision is explicit, evidenced and recorded.

## Workflow
1. Identify affected tasks and scope.
2. Find relevant existing artefacts.
3. Assess current coverage before new implementation:
   - `fully_done`
   - `partially_done`
   - `not_done`
4. Choose reuse strategy:
   - `extend`
   - `refactor`
   - `replace`
   - `new`
5. Assess change impact:
   - files/modules
   - interfaces
   - data model/migrations
   - backwards compatibility
   - regression tests
   - side effects
6. Check parallel-structure risk.
7. Check SoT/runtime/product-semantics drift.
8. Check primary visible ownership for UI/status/recovery paths.
9. Check UI monolith risk for large surfaces or central hooks.
10. Check Context Graph impact according to `../../meta/contracts/context-graph.md`.
11. Recommend the minimal clean implementation path.
12. In `post_ur_review`, record the conditional Architecture Impact described above in the same Brownfield Review.
13. In `post_ur_review`, record `depth_policy_version`, `depth_facts_status`,
    `primary_reason_code`, `decisive_full_depth_triggers`, `rejected_alternative`,
    `missing_or_conflicting_facts`, `depth_evidence_refs` and evidence for all seven bounded-slice
    check IDs in the Brownfield Review. Then persist the completed review and the existing
    Mode/Slice Decision atomically.

## Output
Use a concise structure:

```text
## Brownfield Analysis
- mode: post_ur_review | pre_implementation_analysis
- decision: pass | revise | block | not_applicable
- mode_slice_decision: quick_task | verified_change | structured_slice | structured_delivery | block
- required_next_gate: none | PRD | SD | TP | Brownfield Analysis
- artefact: .agdf/control/artefacts/<key>/BROWNFIELD_REVIEW.md | none
- scope:
- evidence:
- transparency: why later artefacts are skipped, shortened or required
- missing_evidence:
- current_coverage:
- reuse_strategy:
- risks:
- context_graph_impact:
- required_next_step:
```

For `post_ur_review`, include the four UI/UX routing fields immediately after `scope`. If UX intent
definition is required, its `ready | blocked | not_applicable` result must be visible before PRD
readiness. A required `blocked` result is at least `revise` for this routing step.

For a structured `post_ur_review` candidate, also include the complete `Structured Depth Evidence`
section from `BROWNFIELD_REVIEW.md`. The decision projection must show the primary reason, decisive
dimensions, bounded-slice result, rejected alternative, evidence and required next gate. For
missing/conflicting facts, show product-language `depth_unresolved` while persisting `block`; name
the gap and exact recovery action. Structural instruction checks can detect missing contract
elements but do not prove semantic model compliance or live-host behavior.

## Pass / Revise / Block Guidance
- `pass`: existing owners are understood, reuse path is clear, and no blocking drift or parallel structure risk remains.
- `revise`: relevant evidence, tests, ownership, or reuse path is incomplete.
- `block`: implementation would create a second SoT, second owner, unresolved product semantics, or hard unmitigated risk.

## Forbidden
This skill must not:

- propose a Greenfield replacement without evidence
- silently accept overlapping ownership
- convert product-semantics drift into a mere refactor
- create Context Graph nodes automatically
- treat archive links as active current specification signals
- recommend broad PRD/SD/TP or implementation by reflex before Mode/Slice Decision is recorded
