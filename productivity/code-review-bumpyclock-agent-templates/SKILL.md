---
name: code-review
description: Review a PR, branch, commit, or local diff for actionable defects and regressions.
disable-model-invocation: true
---

# Code review

Review the requested changes against their requirements and repository contracts.
Use this workflow for a distinct review task or a concrete concern that warrants review during authorized work.
Routine implementation checks do not require a separate review workflow.

## Scope

Honor the requested focus and comparison endpoints.
Infer omitted scope from the conversation, PR metadata, or local changes when the evidence is clear.
Ask only when plausible choices would materially change the review.
For Git comparison details, read [Diff scope](references/diff-scope.md).

Treat a review-only request as read-only.
For a combined review-and-fix request, complete authorized corrections and affected checks before the final report.
Do not treat review as permission to publish comments, commit, push, or merge.

Use supplied requirements first, then relevant issue or repository context.
If no spec is available, continue with code and contract checks and state the limit.
Do not require tracker setup or a new spec to review a diff.

## Assess

Inspect changed code and the callers, contracts, or tests needed to establish its effects.
Search for repository standards, including `CODING_STANDARDS.md` and `CONTRIBUTING.md` when present.
Prioritize concrete defects, requirement gaps, and consequential maintainability regressions.
Distinguish new or worsened problems from unrelated pre-existing defects.

### Default maintainability bar

Apply the strict maintainability bar by default, even when behavior is correct and tests pass.
Use a requested focus to allocate depth, not to waive this bar for the reviewed code.
Honor explicit user exclusions and report the resulting coverage limit.

Block approval for high-confidence, unjustified structural costs in the diff, including missed clear simplifications.
Examples include misplaced ownership, scattered feature checks, duplicate canonical helpers, tangled branches, and unnecessary wrapper, cast, or optionality churn.
Require decomposition when changed code exposes mixed responsibilities with a clear separation that reduces complexity.
State the concrete cost and a safe correction that preserves required behavior and useful boundaries.

Treat explicit repository requirements as authoritative when they justify a pattern.
Keep preferences, speculative redesigns, and lower-confidence concerns advisory.
Do not require a runtime defect to establish a structural blocker.

For a maintainability-focused review or a concrete structural concern, read [Standards baseline](references/standards-baseline.md).

Use targeted checks to resolve material uncertainty.
Reuse applicable evidence instead of rerunning checks solely because review began.

Delegate independent concerns when separate context or expertise will improve the review.
Give each reviewer a fresh context with the actual scope and relevant evidence when the harness supports it.
Wait for delegated review results and aggregate them before delivering the review.
Reconcile duplicate or conflicting claims before delivery.

## Report

Lead with actionable findings, ordered by impact.
For each finding, cite the location, trigger or violated contract, consequence, and smallest useful correction.
Separate supported defects from unresolved questions and optional suggestions.
Identify blockers explicitly.
Withhold approval while a supported blocker remains.
Use the requested report format when specified.

If no actionable findings remain, say so.
State the reviewed scope, material coverage limits, and checks performed.
Finish when the requested scope is assessed and material claims have evidence or an explicit unresolved limit.
