---
name: pr-review
description: Review guidance for pull requests with emphasis on correctness, regressions, validation gaps, and operational risk.
compatibility: opencode
metadata:
  audience: reviewers
  purpose: review-guidance
---
# Pull request review guidance

## Core approach

- Focus on bugs, regressions, risky assumptions, and missing tests.
- Review the full change scope, not just the latest diff hunk.
- Consider runtime behavior, rollout behavior, and maintenance impact.
- Prefer concrete findings over broad style commentary.

## Review priorities

- behavioral correctness
- edge cases and failure paths
- test coverage and validation quality
- security, migration, and operational risk where relevant
- consistency with existing architecture and conventions

## Guardrails

- findings first, summary later
- prioritize by severity
- cite evidence where possible
- explicitly say when no meaningful findings were discovered
