---
name: code-review
description: Reviews Laravel 12 + Blade + MySQL code as a senior engineer for correctness, architecture, security, performance, maintainability, accessibility, tests, and regressions. Use for code review, refactoring review, or pre-release review.
---

# Senior Code Review

## Review order
1. Correctness and requirement coverage.
2. Security and authorization.
3. Data integrity and migrations.
4. Bugs and edge cases.
5. Performance and query behavior.
6. Architecture and maintainability.
7. Tests and regression protection.
8. Blade accessibility and UX.
9. Style and consistency.

## Review method
- Inspect the diff and surrounding code.
- Understand existing conventions before criticizing deviations.
- Trace affected request/data flows.
- Check failure paths, permissions, validation, transactions, and concurrency-sensitive behavior.
- Check for N+1 and unbounded queries.
- Check whether tests actually prove the behavior.

## Findings
Classify findings as:
- BLOCKER: security, data-loss, broken core behavior, or release-blocking defect.
- HIGH: significant bug, authorization flaw, migration risk, or severe performance issue.
- MEDIUM: correctness/maintainability issue likely to cause future problems.
- LOW: minor improvement.

Do not manufacture findings. If code is correct, say so and identify residual risk rather than inventing issues.

## Refactoring
Recommend the smallest change that materially improves the code. Avoid style-only rewrites unless explicitly requested.

## Output
Summarize:
- what was reviewed
- findings ordered by severity
- exact files/areas involved
- why each issue matters
- concrete fix
- tests/checks performed
- residual risks
