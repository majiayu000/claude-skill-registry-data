---
name: assistant-review
description: "Reviews code and diffs (the current uncommitted changes, named files, a branch or a pull request), specs, plans, tests, documents, Jira tickets, and refinement material, fixes actionable findings, and runs one fresh re-review, or reports only in audit mode. Use for code review, C# pull requests, readiness checks on such material, and the workflow Review phase; QA runs only when required. Assessing a skill itself belongs to assistant-skill-creator; formal review of a delivered diff stays here."
---

# Review

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md).


Find scoped defects/regressions in diff and connected callers/contracts/tests/
configuration, including outside-diff consumers. Findings need real situations,
file/line evidence, impact, calibrated confidence and smallest useful fixes.
Style/speculation stays non-blocking. Preserve carried reduced-testing boundary/source through criteria,
verification evidence and material snapshot refs. Additional tests require a
distinct important uncovered failure and inadequate-existing-evidence rationale;
scores/generic coverage advice cannot expand scope. Return material expansion
to selection/approval.

## Authority and scope

For "review this", resolve explicit scope, uncommitted work, carried state and
current files. Missing required material blocks. Report-only selects audit; clear
edit authority permits scoped review-fix. Ask on ambiguity before inspection or
mutation. Ownership grants no edits. Standalone review runs without a task journal.

Use local company-safe checks. External operations retain approval. Redact secrets
and private data; preserve dirty work; return out-of-scope findings to workflow.

## Review process

At structured boundaries load `contracts/index.yaml`. For behavior or cosmetic
changes, an impact artifact, or locality/shared/unresolved claims, load
`change_impact` and [change-impact.md](references/change-impact.md) before planning or dispatch;
keep caller-only guidance outside Reviewer bundles.

Structured batches load [review-loop.md](references/review-loop.md) before the first batch; v10 rules:

- Formal review uses newly created independent actors and self-contained context
  (Codex `fork_turns=none`), bound to retained native creation/handoff/source
  authority. Missing isolation stays incomplete; no author fallback.
- Each frozen batch attempts every expected pass: trivial/small light review
  (controller_intensity light) uses one newly created reviewer covering both concerns
  (another after a fix); light review records the compact result unless admission, a Pack
  or expanded impact requires structure (plan review: persisted/executable admission only); medium+ keeps at least two
  sibling-blind passes. Resolve `reviewer_context` for each pass, or `lifecycle_reviewer_context`
  only when assigned_scope or coverage_obligations affect lifecycle boundaries;
  synchronous/cosmetic scope alone uses ordinary context. Load the selected handoff before
  dispatch/return, and `return_validation` before aggregation. Account for every
  expected pass; incomplete coverage returns `HAS_REMAINING_ITEMS`.
- Standalone review checks the user's specification. Audit retains mismatches
  as findings and finishes one read-only batch. Review-fix repairs authorized
  mismatches and requires Spec PASS before quality review. Workflow-composed
  review consumes current due-check evidence; acceptance review owns spec checks.
- Review relevant spec, regression, testing, maintainability, bugfix,
  semantic/behavioral contract, loop-safety and security concerns. For every
  review of code, unless explicit instructions say otherwise, load
  [principles](references/review-principles.md) and apply its SOLID and
  "Behaviour selection and machinery" sections to the changed code. Apply matching
  [checklists](references/review-checklists.md) and other principle sections;
  exclude unrelated sections. Medium+ retains its Design Coherence Pass. For a
  changed function with nested branches or loops, use the advisory
  [cognitive-complexity estimate](references/cognitive-complexity.md); it never
  blocks by itself.
- Review carried Architecture Decision Packs, including invalid ones, using the
  matching checklist. Preserve freshness, types/lifecycle/compatibility/quality
  evidence and `review_intensive` independent challenge.
- Before workflow-composed mutation, preserve or refresh the canonical verification
  selection under `F_REVIEW_VERIFICATION_SELECTION`. An active TDD finding goes
  back to the Build owner with its identities, oracle, scope, IDs, and bindings;
  the review fixer cannot bypass RED. Standalone review-fix retains build/tests.
- After fixes, verify due selected/binding checks, freeze the source and run a
  fresh complete batch. No-build admission requires no required/completed fix or
  due selected/executable binding check.

Change-impact projection cannot replace snapshot/coverage closure. Review 11.0
replaced the change-impact checker receipt with a checklist result; 10.0 packets
stay current-readable ([change-impact.md](references/change-impact.md)). At entry, load
`legacy_history` and [legacy-compatibility.md](references/legacy-compatibility.md)
only for persisted pre-10.0 packets or v9 records;
historical evidence cannot certify a current clean batch.

## QA and stopping

QA stays separate from code review and runs after Build and Code Reviewer evidence
only when explicit QA/acceptance, accepted Done Contract, harness acceptance,
domain-scored scope, or scoped UI/visual/product/UX/docs/DX acceptance requires it.
Size, delegation, source changes, and generic acceptance labels do not trigger QA.
Carry approved preparation QA obligations and exact result/source bindings.
Load [qa-evaluation-loop.md](references/qa-evaluation-loop.md) when required and
[domain-rubrics.md](references/domain-rubrics.md) only for scoped domain quality.
Required independent acceptance judgment uses a newly created fresh-context actor;
unavailable isolation remains incomplete. Pure check execution stays discretionary.

Audit stops after its first started batch, without fixes. Review-fix runs round 1,
authorized fixes and validation, then fresh round 2. Round 3+ requires changed
files, unresolved findings, validation failure, regression/drift, or changed
hypothesis; score alone is insufficient.
Load [score-tracking.md](references/score-tracking.md) only at a structured
boundary for score bookkeeping, where Review contracts load the `current_round`
EXIT gate or the `completion` `rubric_summary` artifact: workflow-composed
review, a task journal or persisted result, a QA consumer, or a requested
serialized result. A standalone review returned only to the user is not a
structured boundary for score bookkeeping: it still loads its handoff and
`return_validation` selectors, and reports findings, coverage and limits, with
reviewer rubric dimensions as returned and no score progression or drift labels.
Require a recorded pivot/restart decision before another pass only for evidenced
shared semantic guard stagnation or an applicable material change. Scores alone
never require a decision, evaluator reset or pause.

## Request and plan coverage

For review_subject plan or acceptance, load request_plan (`request_plan_reconciliation`).
One fresh `plan_coverage_and_feasibility` plan-review pass checks original requirements, decisions,
feasibility/order, oracles, completion allocation and avoidable work. Corrections receive fresh closure review before
approval; already-running approved plans retain authority. Final acceptance review solely owns request/plan/delivery reconciliation, including task-wide
work and spec obligations: missing criteria, extra scope, changed-files or verification mismatch.
It uses the common guide's [coverage check](references/operating-guidance.md#request-alignment).
Missing work/findings remains `HAS_REMAINING_ITEMS`.

## Result

Report scope, findings/fixes, verification and limits. No findings means
"No material findings within the reviewed scope and available evidence";
`CLEAN` is an enum, not proof. Retain
`contracts/output.yaml`, canonical reviewed scope, batch/round evidence, required
checks and QA. A standalone review returned only to the user retains no
`rubric_summary` score progression. `CLEAN`/`ISSUES_FIXED` require complete current coverage and no
remaining must-fix/should-fix items; failed/blocked passes never qualify.
Omit empty checklists and internal protocol from human summaries.

Load [review-finding-permanent-rule.md](references/review-finding-permanent-rule.md)
only for evidence of recurring process gaps or high-impact repeatable failures.
Findings require no automatic permanent rule/framework. Retain classification
envelopes for existing mapped all-ID distillation fixtures; omit them from
ordinary human summaries.
