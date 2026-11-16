---
name: code-review
description: Review a proposed diff for correctness, regressions, security, and maintainability without editing it. Use before merging or when asked for an independent review.
---

# Code Review

Review the actual diff against the intended behavior, not just style preferences.

1. Read the request/spec, changed files, surrounding implementation, and relevant tests.
2. Trace changed paths through callers, data boundaries, error handling, and compatibility surfaces.
3. Look for correctness defects, regressions, security/privacy risks, data loss, concurrency errors, and missing tests.
4. Check whether tests prove the claimed behavior and whether important failure paths are covered.
5. Report findings first, ordered by severity. Each finding includes location, concrete failure scenario, impact, and a focused remedy.
6. Separate confirmed defects from questions, risks, and optional improvements.

Do not report purely stylistic preferences as blockers. Do not make edits during a review-only task. If no actionable findings exist, state the areas reviewed and the limits of the review; do not imply exhaustive proof or a security certification.
