---
name: assistant-review
description: "Review code, fix actionable findings, and run one fresh re-review. Use for explicit code review or the workflow Review phase; QA runs only when required."
---

# Autonomous Review And QA Evaluation

## Contracts

Canonical schemas are authoritative at enforcement points. Read
`contracts/index.yaml` first; do not load every contract at entry.
- `entry`: load `contracts/input.yaml` review-entry fields selected by `review-entry-fields` in `contracts/index.yaml`.
- Triggered `change_impact` and `architecture_pack_input`: resolve before planning or dispatch; keep change-impact guidance out of Reviewer bundles.
- `current_round`: load the active `contracts/phase-gates.yaml` round at each transition; `selected_handoff`: resolve the compact `contracts/handoffs.yaml` dispatch pointer before Reviewer or QAEvaluator dispatch.
- `reviewer_context`: resolve at pass start; `return_validation`: resolve after its result; `completion`: load `contracts/output.yaml` before final exit.

Migration note: assistant-review contracts are v7.2. Persisted 6.0/7.0/7.1 batch packets are invalidated and rebuilt; they never reach CLEAN. A triggered Pack validates recoverable selected design, rationale, and viable alternatives/dispositions plus `architecture_decision_pack_checks`.
Applicable instructions set `subagent_trigger_scope`; opt-out, unavailability,
or policy blocks use direct fallback. Reviewer returns and final summaries have
non-empty `reviewed_scope` so workflow consumers can use the producer packet.

Selectors resolve canonical fields. Entry loads no review guidance. A missing or
invalid selector uses `load_full_authoritative_file`: validate that full
canonical file and record recovery.

## Goal

Find evidence-backed defects, regressions, and test gaps; fix authorized
findings; and return one policy-safe result without claiming proof. Required QA
independently evaluates acceptance, evidence, quality, progression, and readiness.

## Success Criteria

- Resolve scope, mode, and material before the loop; rank findings by severity,
  evidence, and confidence.
- Each frozen-snapshot batch plans and attempts at least two independent passes.
  All expected passes reach terminal accounting before aggregation, fix, or exit.
  `CLEAN`/`ISSUES_FIXED` require complete coverage. Audit exits after one started
  batch with non-empty `reviewed_scope`; incomplete coverage, including failed,
  timed-out, or blocked passes, returns `HAS_REMAINING_ITEMS`.
- Every review applies SOLID, KISS, DRY, YAGNI, and readability from
  `references/review-principles.md`. An applicable Pack checks freshness,
  ownership/dependency, semantic types, falsifiable quality, compatibility or
  extension, and verification handoff.
- Review-fix addresses or explicitly defers must-fix and should-fix findings,
  then validates and performs a fresh review.
- QA evaluation runs after code-review/build evidence when `qa_evaluation_mode=required`, returns score progression and a final acceptance verdict, and does not replace code-reviewer.
- QA required positive triggers: explicit QA/acceptance evaluation request, accepted Done Contract, harness-capable acceptance scope, domain-scored scope, or scoped UI/visual/product/UX/docs/DX acceptance.
- QA non-triggers: template labels/placeholders, generic acceptance criteria labels, optional/not_required reasons, delegation/source-changing work alone, and ordinary medium+ code-review-only/source-changing work.
- QA evaluation loads `references/domain-rubrics.md` only when acceptance criteria, Done Contract, `domain_context`, or explicit `rubric_refs` scope domain quality; selected_domain_rubrics/domain_quality_scores when scoped.

## Constraints

- Infer authority from semantic modification authority: report-only is audit;
  clear source authorization is review-fix; a carried approved workflow allows
  only bounded in-scope fixes. If editing versus audit is materially unresolved,
  ask: "Should I only report findings, or also implement and verify fixes?" Do
  not review or mutate until answered.
- Present no intermediate review summaries. Frame refactor findings with a
  concrete risk, and use clean-code principles as evidence lenses.
- Keep QA evaluation separate from code review: QA owns acceptance, Done
  Contract, verification, scoped quality, progression, and final result; Code Reviewer continues to own code defects, security, architecture, and test-coverage review.

## Entry

Prefer explicit material, then uncommitted changes, task journal/packet, then
current-file audit. Ask only when no review material is available.

A standalone `review this` without carried workflow evidence runs Spec Review against user scope. Review-fix
repairs an authorized mismatch and repeats to a PASS pointer before Reviewer
dispatch; audit retains the Spec Review mismatch as an aggregate finding and continues a frozen read-only multi-pass batch. Standalone does not require a task journal;
`task_journal_path` is optional. A workflow-composed review consumes carried
Spec Review PASS and current build/test evidence. After any source fix, every
subsequent Reviewer dispatch requires real current passed build/test evidence;
not-applicable is invalid.

## Review Modes

Select the applicable spec, regression, test, maintainability, bugfix evidence,
semantic contract, behavioral contract, agentic-loop safety, and security modes.
The three entry flags enable contract/loop modes; security-sensitive surfaces
route to `assistant-security`. `risk_selected_specialist` uses Code Reviewer
with the assistant-security checklist/perspective while keeping the canonical Reviewer
schema.

Authorship, branch/PR ownership, platform, and connector availability identify
material but never authorize edits. Out-of-scope findings return to the
composing workflow. Findings state severity (`must-fix`, `should-fix`, or
`nit`), file/line evidence, impact, smallest useful fix, and calibrated
confidence; speculative concerns are non-blocking Observations.

Load `references/qa-evaluation-loop.md` after build/test and code-review
evidence only when QA is required. Code Reviewer still owns code defects,
security, architecture, and test coverage.

## Company-Safe Review Rules

Prefer local diffs and repo-native checks; require no external scanner, remote
review, or unapproved install. Redact secrets and proprietary data, and offer
local/manual alternatives when policy blocks a scan.

## Mandatory Review Checklists

The fresh Reviewer context bundle points to `references/review-checklists.md`
and supplies only applicable sections; each yields findings or an explicit "no
concrete risk found" check.

- Agentic loop flag -> Agentic Loop Safety Checklist -> `agentic_loop_safety_checks`.
- Behavioral flag -> Behavioral Contract Review Checklist -> `behavioral_contract_checks`.
- Semantic flag -> Semantic Contract Review Checklist -> `semantic_contract_checks`.
- Architecture Decision Pack flag -> Architecture Decision Pack Review Checklist -> `architecture_decision_pack_checks`.

## Refactor-Related Findings

Allowed risk categories: correctness, security, unsafe change surface,
branching/responsibility growth, hidden dependency/ownership, brittle testing,
poor extension seam, and readability/maintainability drag. Every refactor-related finding MUST state its risk category, affected surface, review evidence, and the smallest durable fix. Use concrete risk framing instead of generic convention, style, cleanliness, or improvement language. Request broad cleanup only when a smaller durable fix cannot remove the risk.

## Architecture Decision Pack Review

Review a Pack only when metadata or material says one applies; its mode equals
canonical `architecture_design_mode`, and `review_intensive` includes
independent challenge evidence. Verify source/revision freshness, invalidating
questions, boundaries, control/early exit, ownership/disposal, resource
envelope, extension registration, representative path, semantic type and
primitive-exception boundaries, falsifiable quality scenarios, compatibility,
extension seam, verification, and rollback. Generic `string`, numeric,
collection, or callback interfaces that erase domain/public/lifecycle semantics
without a local primitive exception and conversion/validation are findings.
Treat unsupported memory, performance, or extensibility claims as unknown or a
verification gap.

## Principle and Readability Lens

For medium+ reviews, run the **Design Coherence Pass** and return
evidence-bound `principle_checks.design_coherence`; findings name surface, risk,
and smallest fix.

## Review Loop Routing

After entry, load `references/review-loop.md` before the first REVIEW step. It
owns batch protocol, loop, barriers, pivots, and the max 10 rounds; principles,
checklists, and rubric guidance belong to fresh pass bundles. Before dispatch,
include `worker_return_schema_selector`: recursive required/triggered shapes,
types, enums, and cardinality only; never sibling/batch state. Impact projection
preserves canonical closure; it cannot make audit or review-fix clean.

Required QA follows build/test and code-review evidence. A carried
`approved_feature_preparation_qa_acceptance_obligation` uses the exact result
and successful-pair conditions in `contracts/handoffs.yaml` and
`contracts/phase-gates.yaml`: echo its scope/prerequisite/source binding with
evidence; otherwise return rejected/`HAS_REMAINING_ITEMS` or blocked/`BLOCKED`.

## Exit: Present Final Result

Use `contracts/output.yaml`. For no findings, say: "No material findings within the reviewed scope and available evidence"; `CLEAN` is an enum, not proof.

## Rules

- Keep round results internal; use fresh sibling-blind bundles, wait for every
  response, and return `HAS_REMAINING_ITEMS` for incomplete coverage.
- Prior fixes require closure verification.

## Output

Return reviewed scope, rounds/result, evidence-backed findings and fixes, verification, applicable bugfix/agentic/behavioral/semantic checks, required QA result, and residual risk. `contracts/output.yaml` owns the exact schema.

## Stop Rules

- Audit mode stops after one review batch. Report terminal findings without edits.
- The normal review-fix path is an initial review batch, fixes and validation, then one fresh re-review batch; mutation requires a new snapshot and complete coverage.
- Before round 3+, require `additional_round_reason` backed by changed files,
  unresolved finding, validation failure, regression/drift, or changed
  hypothesis; score alone is insufficient. round 10 is terminal; never start 11.
- Stop and report a blocker if required review material is unavailable or empty.

### Drift detection (medium+ scope)

Compare rounds with `references/score-tracking.md`. Drift, regression,
stagnation, or pivot evidence returns `pivot_restart_signal`; the orchestrator records `pivot_restart_decision` before another pass.


## Review Finding Rule Distillation

For each blocker or must-fix finding, load
`references/review-finding-permanent-rule.md` and classify `one_off_fix`,
`permanent_rule_candidate`, or `no_action`. Promote only recurring process/eval
gaps, missing contracts/checklists, or high-impact repeatable failures.
