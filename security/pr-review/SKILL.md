---
name: pr-review
description: Review pull requests and code changes for correctness, risk, tests, security, performance, and maintainability. Use when Codex is asked for a PR review, code review, diff review, change review, risk review, or pre-merge feedback.
license: MIT
---

# PR Review

## Core Workflow

1. Understand the change intent, affected surface, user impact, and stated test
   plan before judging the diff.
2. Review for correctness, edge cases, regressions, security, data handling,
   performance, compatibility, and maintainability.
3. Prioritize findings that could cause wrong behavior, user harm, production
   risk, or future maintenance cost.
4. Tie each finding to concrete evidence from code, tests, logs, or behavior.
5. Separate blocking findings from non-blocking suggestions and style nits.
6. Call out missing tests or validation when risk remains.

## Safety Rules

- Do not approve, merge, or dismiss review feedback automatically.
- Do not invent test results. State when tests were not run.
- Do not flood the review with preferences when there are no material risks.
- Escalate security, privacy, auth, billing, migration, data-loss, and rollout
  concerns.

## Deliverable Shape

For PR reviews, provide:

- Findings ordered by severity
- File or area references where available
- Missing tests or validation gaps
- Residual risk
- Brief change summary only after findings
- Open questions that affect review confidence

## References

- Read `references/pr-review-checklist.md` when reviewing pull requests,
  patches, diffs, or pre-merge code changes.
