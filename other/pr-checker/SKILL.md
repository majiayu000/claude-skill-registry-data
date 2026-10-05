---
name: pr-checker
description: Review a change set for correctness, regressions, security risks, and test coverage gaps.
---

# Goal

Produce a practical, high-signal review of a branch, diff, or PR.

# Review checklist

- Correctness
- Behavior regressions
- Security implications
- Missing validation or tests
- Migration or rollout risk
- Maintainability issues that could hide bugs

# Output format

For each finding:
- Severity
- What is wrong
- Why it matters
- Evidence
- Suggested fix
