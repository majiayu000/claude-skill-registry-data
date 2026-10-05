---
name: review-gate
description: Run an independent semantic review gate before merging non-trivial work, alongside CI and any configured automated code review tool.
---

# Review Gate

Use this after implementation and before merge.

## Division of Labor

- **Mechanical checks — owned by automated review (e.g. Alibaba Code Review) and CI**: linting, formatting, conventional style, and straightforward static-analysis findings. When automated review tools like Alibaba Code Review are configured, their output is recorded via `ai-agent-pr-metadata`.
- **Semantic review — owned by this gate**: requirements compliance, correctness, regressions, security/authorization, contract/integration risk, and acceptance-test adequacy — everything mechanical tooling can't judge.

## Workflow

1. Confirm linked issue and acceptance criteria.
2. Confirm verification commands and results.
3. Read Alibaba Code Review's findings and the GitHub CI/check results on the PR before starting the independent review — don't re-derive what's already there. If no automated code review tool is configured on the repository, rely on CI check results and proceed directly with independent semantic review.
4. Review spec compliance before code style.
5. Check business logic and edge cases, regressions and compatibility, security and authorization, API/database/queue/integration contracts, and test adequacy including missing acceptance tests (see [canonical reviewer scope checklist](references/reviewer-scope-checklist.md), which already covers backwards-compatibility explicitly).
6. Revisit an Alibaba Code Review or CI finding only when it indicates an unresolved correctness, security, data-loss, configuration, or acceptance-criteria issue — not to relitigate style or formatting.
7. Post concrete findings or explicitly state no blocking issues. Do not repeat resolved lint, formatting, conventional-style, or straightforward static-analysis findings already covered by CI or automated review.
8. Apply review findings before merge.

## Two-Axis Review Structure

Review along two independent axes and report findings under separate headers:

1. **Spec Compliance Axis**: Does the diff satisfy every acceptance criterion and expected behavior without scope creep or missed edge cases?
2. **Standards & Code Quality Axis**: Does the code adhere to this repository's conventions, architecture patterns, and semantic quality standards?

**Rule**: Never cross-rerank findings across the two axes. A change can cleanly follow conventions yet fail the spec, or satisfy the spec while violating architectural standards. Evaluate both independently.

## Semantic Smell Baseline (12 Fowler Smells)

Use these 12 smells as semantic heuristics during review. Documented repository standards always override these heuristics, and mechanical checks owned by CI/OCR must be skipped:

1. **Mysterious Name**: Unclear variable, function, or class name → rename to reflect intent and domain concepts.
2. **Duplicated Code**: Identical or near-identical logic in multiple places → extract helper or shared abstraction.
3. **Feature Envy**: Function queries another object's data more than its own → move behavior closer to data.
4. **Data Clumps**: Same group of primitives repeatedly passed together → group into a value object or struct.
5. **Primitive Obsession**: Raw strings/ints used for rich domain concepts → encapsulate in small value objects.
6. **Repeated Switches**: Same `switch` or `match` on type codes scattered across files → use polymorphism or strategy pattern.
7. **Shotgun Surgery**: One change forces many small edits across multiple files → consolidate related responsibilities.
8. **Divergent Change**: One class changes for multiple unrelated reasons → split into cohesive classes with single responsibilities.
9. **Speculative Generality**: Hooks, parameters, or abstractions built for hypothetical future needs → delete unused generic machinery.
10. **Message Chains**: Client navigates long chains (`a.b().c().d()`) → hide delegation or extract query.
11. **Middle Man**: Class merely delegates without adding value → remove delegate and call target directly.
12. **Refused Bequest**: Subclass rejects inherited methods/data → replace inheritance with composition.

## Reviewer Contract

The reviewer should read the issue, acceptance criteria, automated review output (if present), CI results, and the PR diff first. Pull more context only when needed.

## Proportional Performance & Reliability Checks

Scale the depth of performance review to the PR's Risk Level (do not prematurely optimize; do not ignore an obvious regression):

- **Low Risk**: Skip dedicated performance checks unless the diff introduces an obvious infinite loop or severe memory leak.
- **Medium Risk**: Check for obvious algorithmic regressions (e.g. $O(N^2)$ loops where $O(N)$ was standard), N+1 queries in modified routes/queries, missing caching where an existing project pattern supplies it, and resource cleanup.
- **High Risk**: Check concurrency limits, network timeouts and retries on external calls, queue payload sizes, lock contention/slow migrations, and deterministic failure-path resource cleanup.

## Merge Rule

CI remains a hard merge gate; this review does not replace it and is not the place to rerun or restate lint/static-analysis automation. Do not merge non-trivial work without a review record. If an automated or subagent reviewer stalls, post a manual expert review that states residual risk.
