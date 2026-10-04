---
name: assistant-workflow
description: "Prepare, plan, build, or resume persisted task state. Use for repository-grounded feature/epic/story technical preparation, implementation, fixes, migrations, refactors, and project artifacts."
requires:
  - assistant-review
---

# Development Workflow

Public routing contract; mechanics live in references and contracts.

## Goal

Move work to verified outcome through right-sized phases, gates, tests, review, and safe execution.

## Success Criteria

- Scale phases to risk; Decompose, Design, and durable state run only when triggered.
- Before resume, reconcile the newest user request and repository evidence.
- On stale, superseded, or completed resume state, update `{agent_state_dir}/task.md` before acting; record classification, reason, task identity, and exact next action.
- `plan_mode`: bounded small uses no-wait `inline`; For `execution_intent != prepare_only`, `approval_required` applies to medium+, risk, destructive, scope changes. `prepare_only`: `inline` only for explicitly requested readiness planning; otherwise `none`.
- `references/workflow-controller.md` is the canonical source for controller intensity, workflow state, manual verification, harness/QA routing, and review-role separation.
- Ordinary medium+ workflow tasks stay standard, non-harness, and non-QA unless explicit controller criteria apply.
- Harness-capable execution carries required artifacts; preparation records requests as typed future obligations with capability inactive.
- Candidate Search is reserved for explicit alternatives, open-ended architecture/design, optimization, high uncertainty, repeated failures, unclear/flaky bugs, or reviewer-requested pivots.
- Triggered Architecture Decision Packs are source-backed and fresh. `prepare_only` retains Discover-only Pack context through Preparation Completion; `execution_intent != prepare_only` continues through Plan binding, task packets, Build, handoff, and Review.
- Behavior changes default tests-first or carry explicit validation in the same Build step.
- Existing-system prep inspects sources, code, and tests. `prepare_only` ends without implementation claims; optional readiness planning is inline. Carry the exact approved typed preparation result into `implement_only`; existing-system evidence or a `not_applicable` basis and inactive future harness/QA obligations remain part of that result before their gates activate. Product questions require evidence.
- A behavior-bearing change records compact change-impact applicability evidence. Only shared, materially unresolved, or explicitly carried expanded impact assessments use the common checker and carry an artifact identity through planning, Build, and assistant-review; the checker is resolved from the active installation, never the repository cwd.
- Review, QA, and security routing apply when triggered.
- Medium+ final handoff binds canonical review/QA state and exact snapshot;
  remaining items, incomplete coverage, or rejected/blocked QA forbid completion.
- Medium+ output follows `references/final-handoff.md`; prepare_only returns readiness and next implementation state.

## Constraints

- Explicit user or repository artifact schemas override workflow-internal shapes; preserve exact paths, keys, types, ids, and supplied literals.
- Run phases. `prepare_only`: Discover -> Preparation Completion; readiness optional, implementation gates inapplicable. Other work skips Plan only when eligible.
- Do not ask ritual questions when code/context makes the next safe action clear.
- Ask material clarifications only when an undiscoverable implementation-shaping unknown lacks a safe default and affects correctness, scope, behavior, data, public contract, security, migration safety, or verification; group by topic.
- assistant-clarify owns prompt-level ambiguity when its routing matches; clear prompts do not invoke it. Existing workflow clarification owns precise, answerable questions and safe defaults.
- Load `references/progressive-discovery.md` when `uncertainty_shape=progressive`, `progressive_route_clear_consumption_state in [pending, consumed]`, `progressive_sequence_readiness_state in [active, closed]`, or `progressive_artifact_retention_state=terminally_archived`. The durable markers load validation regardless of whether progressive_artifact_retention_state is missing, not_applicable, or retained, so invalid carried state fails closed instead of releasing artifacts. Retained state keeps active/resumable progressive artifacts available after `uncertainty_shape=bounded`. `terminally_archived` is allowed only with a typed `progressive_terminal_archival` tombstone binding the current task, final decision map, archival/termination basis, and resolvable evidence proving continuation and reference resolution are impossible; `Task state: completed` does not qualify by itself, and terminally archived state cannot revert. Fully specified tasks with `not_applicable` markers stay bounded, and size alone is not a trigger.
- Progressive Discover is a no-execution boundary; any mutating prerequisite uses a separate approved workflow that returns evidence before normal workflow gates continue.
- Keep scope changes explicit and tied to correctness, security, safety, or verification.
- Do not install tools, upload code, call external services, or paste proprietary content into third-party systems unless the user explicitly approved that path.
- Prefer repo-native commands over new tooling.
- When external services, installs, or sensitive-data handling are in scope, load `references/ai-usage-policy.md` for company-safe detail. It is not an entry dependency.

## Contracts

Canonical contracts are authoritative. Read `contracts/index.yaml` first, validate at enforcement, and load only the contract selector applicable to the current boundary:

- `entry`: load entry fields declared by `contracts/index.yaml` from `contracts/input.yaml`; `references/triage-rubric.md` is the only declared entry reference.
- `architecture_design`: load `references/architecture-decision-pack.md` when `architecture_design_mode != not_applicable`; use its typed artifact before Decompose or Plan and retain its reference through Review.
- `feature_preparation`: for repository-grounded preparation, existing behavior, any `implement_only` workflow, or any carried `approved_feature_preparation_harness_obligation` or `approved_feature_preparation_qa_acceptance_obligation` (including `feature_preparation_scope=not_applicable`), load `references/feature-preparation-evidence.md`; resolve and retain `approved_feature_preparation_result` unchanged plus the applicable evidence ref or typed `not_applicable` source binding before Decompose, Plan, or Build. A carried QA obligation uses only the existing post-Build, post-Code-Reviewer QA Evaluator lane.
- `change_impact`: load `references/change-impact.md` when behavior, cosmetic, or local/shared/unresolved impact affects verification. Record compact applicability; only shared, unresolved, or explicitly carried expanded work requires common pre-Build/completion.
- `progressive_discovery`: load `references/progressive-discovery.md` when `uncertainty_shape=progressive`, either durable marker is pending/consumed or active/closed, or `progressive_artifact_retention_state=terminally_archived`; durable markers route even when the retention state is missing or invalid. `terminally_archived` releases the durable artifacts only with the typed `progressive_terminal_archival` tombstone and explicit final archival/termination evidence, never merely `Task state: completed`, and cannot revert.
- `delegation`: load role and trigger fields when roles may be required and before any subagent dispatch.
- `current_phase`: active `contracts/phase-gates.yaml` at transition.
- `selected_handoff`: `contracts/handoffs.yaml` before dispatch and return validation.
- `completion`: `contracts/output.yaml` at completion before final exit.

Selectors resolve by unique id plus canonical path, section, key, and explicit names. Runtime selectors resolve `name_from` only through their declared `allowed_names`.

Missing or invalid selector: `load_full_authoritative_file`; validate the full named canonical file and record recovery.

Migration note: assistant-workflow contracts are v11.1. v11.0 packets lacking a triggered `change_impact_evidence` envelope are not completion-compatible when a behavior/locality gate applies; recapture and rebuild current evidence rather than inventing historical execution or review. v10: `prepare_only` uses `feature_preparation_result`, records execution not started, omits Build/test/review/final-handoff claims, and retains `handoff_binding_state=discover_only` through Preparation Completion even for optional readiness planning. v9: `execution_intent`; existing-system preparation produces or carries `feature_preparation_evidence`. Bash/provider review runners are removed; native task packets retain scope and verification. v8: consumed all-excluded route-clear maps may keep `entries=[]` only with complete exclusion lineage; Pack alternatives use stable `selected_alternative_id` bindings and verified `quality_scenario_id` scenarios use resolvable verification identity. Pack `review_result` retains canonical refs. v6: `semantic_type_inspection`, `contributor_evidence`. v4 consumers use `handoff_binding_state=discover_only`
with Discover context/journal.
For `execution_intent != prepare_only`, Plan atomically binds task/review refs
as `downstream_bound` before Build when `plan_mode!=none`; plan_mode=none binds
inline task/review refs at the pre-Build boundary.
Material invalidation clears stale downstream refs through refresh, re-plan,
and reapproval. Direct-user, applicable
`AGENTS.md`, or active-skill instructions trigger delegation; record
`subagent_trigger_scope` and dispatch without
separate permission question. Explicit opt-out, unavailability, or
exact policy block uses evidenced fallback. `verification_command` is non-empty
argv `string[]`; assistant-review owns Reviewer/QAEvaluator handoffs and returns
`final_summary` / `qa_evaluation_result`. Persisted wrappers record current
`skills/assistant-review/contracts/index.yaml#schema_version`; mismatch
invalidates their refs and reruns the required current-contract lane without
guessing packet shape. Workflow validates exact current-batch alias/identity;
`reviewed_scope` is non-empty.

## Visible Checkpoints

Phase markers are required only for `controller_intensity=strict`, explicit
project policy, or a user request. Light and standard work still follows every
logical phase and gate, but reports progress with concise natural updates
without exact marker ceremony.

When exact markers are required, use this instruction: `Use this exact format:`

```
--- PHASE: [name] ---
```

For steps within a phase:

```
>> [step description]
```

For completion:

```
--- PHASE: [name] COMPLETE ---
```

## Refactor Guidance

- Justify it with a concrete risk only: correctness, security, unsafe change surface, ownership, brittle testing, or poor extension seam.
- Tie incidental or scope-expanding refactors to concrete risk instead of vague framing such as generic convention language, style, cleanliness, or generic improvement.
- Choose the smallest useful, durable fix that removes the identified risk. Keep cleanup scoped unless the user explicitly requested cleanup, reorganization, or refactor work.

## Triage

Start Triage with a concise update; strict markers use `--- PHASE: TRIAGE ---`.

Load `references/triage-rubric.md`, perform a quick read-only Candidate scope
scan, then assess task type, risk, size, gates, agents, controller intensity,
plan mode, subagent state, and search mode. Ideas need binary criteria.

| Size | Phases |
|---|---|
| **Prepare-only** | Discover -> [readiness] -> Preparation Completion; no implementation |
| **Small** | Discover quick -> [Plan] -> Build -> Review -> Document; `plan_mode=none` only for trivial safe work, otherwise inline or approval-required |
| **Medium** | Discover -> Decompose -> Plan -> [Design] -> Build -> Review -> Document |
| **Large** | Discover -> Decompose -> Plan -> Design -> Build -> Review -> Document |
| **Mega** | Discover -> Decompose -> Plan -> Design -> Build -> Review -> Document |

[Design] = UI only.

Print: `>> Triaged as: [SIZE] — phases: [list]`
Print: `>> Triage metadata: type=[TASK_TYPE] | risk=[RISK_TIER] | intensity=[controller_intensity] | architecture=[architecture_design_mode] | plan=[plan_mode] | gates=[count] | agents=[count] | search=[search_mode] | scope_confidence=[low|medium|high]`

If scope exceeds initial triage during any phase, stop and re-triage. Use `references/candidate-search.md` only when `search_mode: candidate_search` is selected.

## Phase Routing

Load the generated `references/phases/<current-phase>.md` view for the active phase (lowercase; Preparation Completion is `preparation-completion`). Missing or unknown view: load authoritative `references/phases.md`. Load `references/workflow-controller.md` only when resolving shared routing/default, movement, harness, review, QA, or subagent-separation decisions. Load `references/architecture-decision-pack.md` only when `architecture_design_mode != not_applicable`. Use `references/context-budget-and-pattern-retrieval.md` for large material or framework patterns, `references/artifact-first-output-contract.md` before Plan only when `execution_intent != prepare_only`, `references/decomposition-plan-review.md` before medium+ Decompose exits, `references/plans/<size>.md` during Plan (`mega` uses `large`; `prepare_only` uses `prepare-only`); missing or unknown view loads authoritative `references/plan-template.md`, and `references/context-handoff-templates.md` applies to non-standard continuations. Optional `prepare_only` readiness Plans omit Artifact Contracts and executable slices.

| Phase | When | Key Actions |
|---|---|---|
| Discover | All | Inspect request/repo and unknowns; create a source map only when the current file/boundary cannot be resolved directly; unknown-cause bugfixes: load `assistant-debugging`. |
| Decompose | Medium+ implementation work | Smallest slices with acceptance and verification. |
| Plan | `plan_mode != none`; optional prepare_only readiness | Inline/approval routing. |
| Design | UI only; `execution_intent != prepare_only` | Direction, checklist, approval. |
| Build | `execution_intent != prepare_only` | Light direct; ordinary medium one edit/test executor; separation only for high-risk or broad/noisy/environment-heavy verification. Tests/validation travel with code. |
| Review | `execution_intent != prepare_only` | Light self-review; expanded impact uses canonical `assistant-review`; standard/strict use independent `assistant-review`; QA when required. |
| Document | `execution_intent != prepare_only` | Apply state/manual-verification modes; metrics optional and non-blocking. |
| Preparation Completion | `prepare_only` | Return readiness; approval is next. |

For subagent rules, load `references/subagent-dispatch.md` and resolve
`subagent_policy_state`, `subagent_execution_mode`, `subagent_trigger_scope`,
and conditional `policy_blocking_source` before spawning. Light small low-risk
work uses `not_required` and `not_applicable`. For standard/strict work, a
direct user request or applicable `AGENTS.md` or active-skill instruction triggers `delegation_triggered`: infer scope and dispatch the configured role agents without a separate permission question. Direct fallback needs explicit
opt-out, an exact active policy block, or real unavailability; do not infer unavailability merely because no visible tool is named `Task`, `delegate`, or `subagent`. Delegation retains parent sandbox, tool/action approvals,
external-write, install, destructive-operation, and secrets safeguards.

Load `references/harness-controller.md` only for `execution_intent != prepare_only` with `harness_capable=true`.
Load `assistant-security` when touching auth, user input, secrets, persistence, network calls, shell commands, dependency/config changes, or external integrations.

## Output

Return:
- Status: complete, partially complete, blocked, or plan ready.
- Changed files: paths and purpose.
- Verification: commands, pass/fail, skipped checks with reasons.
- Review result: spec, quality, QA, and security when applicable.
- Residual risk: blockers, assumptions, policy constraints, or follow-up.
- Next step: one practical recommendation.

Do not use phrases like "should work", "probably fixed", or "looks good" unless immediately qualified with evidence or uncertainty.

## Stop Rules

- Stop and ask when an implementation-shaping field is material, undiscoverable, and has no safe default.
- Stop before Build when `plan_mode=approval_required` until plan approval.
- Stop before response if required output-contract evidence is missing; implementation also requires build, tests, and review evidence.
- Stop when a plan deviation changes approved scope, files, behavior, risk, verification, or acceptance criteria; record the deviation and get approval before continuing.
