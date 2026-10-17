---
name: testing-strategy
description: Test at the right level for each risk — unit, integration, end-to-end — plus regression per defect and flake control.
version: 1
triggers: testing strategy, test pyramid, unit tests, integration tests, e2e, regression
category: Engineering & code
blurb: Test at the right level for each risk — unit, integration, end-to-end — with regression per defect.
archetype: knowledge
example: Give me a testing strategy for this system, level by level.
---

# Testing Strategy — the QA seat

Tests are the team's immune system: fast where they can be, real where they must be. Coverage is a signal, not a goal — every P0 has a test.

## When to use
- Any feature build or refactor.
- Bug fixes: write the regression test **first**.
- Before any release or handoff.

## Method
1. **Pyramid**: many unit tests (logic), fewer integration tests (boundaries, DB/API), few e2e tests (critical journeys).
2. **Risk-first**: test what breaks expensively; P0 flows get e2e; tricky edge cases get unit tests.
3. **Deterministic fixtures**: no shared mutable state; explicit seed data; time and randomness controlled.
4. **Bug → test**: every confirmed defect gets a failing test before the fix — and keeps it forever.
5. **Flake policy**: quarantine immediately, fix within a week, or delete consciously (a flaky test is worse than none).
6. **Negative testing**: invalid input, timeouts, partial failures, retries — assert sane failure, not just "no crash".
7. **Report honestly**: what ran, what passed, what is NOT covered.

## Artifacts
- Test suites per level, fixtures, a short `TEST-PLAN.md` for non-trivial work (stating what's excluded).

## Quality gates
- [ ] Full suite green before handoff (no skipped/quarantined without a tracked ticket).
- [ ] Critical journeys covered end-to-end.
- [ ] Every fixed bug has a regression test.
- [ ] Coverage gaps stated explicitly in the report.

## Red lines
- Tests must not depend on production systems or live data.
- Never "fix" a test by weakening its assertion — fix the code or delete the test deliberately.

## Related
`code-review-practice` (gates) · `ci-cd-pipeline` (automation) · `backend-engineering` (failure modes).
