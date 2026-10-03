---
name: code-review
description: Review a code change independently for correctness, regression risk, maintainability, compatibility, tests, and unsafe assumptions.
---
# Code Review

Use when implementation exists and needs independent technical review.

## Procedure
1. Read the stated goal and acceptance criteria before inspecting the diff.
2. Understand the changed behavior, boundaries, and affected callers or data paths.
3. Look for correctness bugs, missing edge cases, state inconsistencies, error-handling gaps, compatibility breaks, unsafe concurrency, and hidden assumptions.
4. Evaluate whether tests exercise the changed behavior and meaningful failure modes.
5. Separate blocking findings from suggestions. Give each finding a precise location, consequence, and rationale.
6. Verify suspicious claims by reading adjacent code or running targeted checks when practical.
7. Re-review fixes to blocking findings.

## Quality gate
A review should maximize signal. Do not bury important defects in style commentary or demand rewrites without a concrete engineering reason.