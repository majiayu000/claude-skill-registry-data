---
name: review-feedback-promoter
description: Convert repeated review findings into durable harness checks. Use when code review catches recurring agent mistakes that should become docs, tests, lint rules, boundary checks, validation scripts, or quality policy.
---

# Review Feedback Promoter

## Purpose

Turn recurring human or agent review feedback into reusable harness defenses instead of repeating the same comment.

## Inspect First

- recent review findings, `agent-reviewer` output, quality docs, lint/boundary/test scripts, architecture docs, dependency/security policies, and known repeated defects

## Procedure

1. Classify each finding.
   - Documentation rule for knowledge gaps.
   - Test for behavior gaps.
   - Boundary or lint check for mechanical architecture gaps.
   - Security/dependency/migration check for governance gaps.
   - Entropy/golden-pattern update for consistency gaps.

2. Record promotions.
   - Create or update `docs/quality/review-feedback-promotions.md`.
   - Include source finding, promoted defense, validation command, owner, and status.

3. Add the lightest durable defense.
   - Prefer existing project-native checks.
   - Add scripts only when deterministic and repeatable.
   - Avoid broad rules that create false positives.

4. Route specialized fixes.
   - Use `architecture-boundary-enforcer` for import/layer issues.
   - Use `testing-strategy-builder` or `tdd-playwright-workflow` for behavior gaps.
   - Use `documentation-sync-enforcer`, `security-baseline`, or `dependency-governance` for specialized policy gaps.

## Validation

- Confirm each promotion maps to a real repeated finding.
- Confirm each new rule has a command, doc location, or test path.
- Confirm the defense is specific enough to avoid noisy failures.

## Completion Criteria

- Repeated review feedback has a durable follow-up path.
- The harness grows stronger without bloating root instructions or adding unnecessary tools.
