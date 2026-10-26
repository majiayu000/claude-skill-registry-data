---
name: qa-testing
description: Use when planning or writing tests, defining coverage, or gating on unit/integration/e2e/regression checks, including golden-fixture verification for tax logic.
---

# QA & Testing

## 7-stage QA process

1. Requirements review — understand what's being tested and why.
2. Test planning — scope, risk areas, what's in/out.
3. Test design — concrete test cases (including edge/boundary cases).
4. Execution — run the tests.
5. Defect logging — log failures with a clear repro.
6. Regression — re-run affected areas after fixes.
7. Reporting & continuous improvement — capture what should be tested going
   forward.

## Test pyramid & tooling

- Favor many fast unit tests, fewer integration tests, and a thin layer of e2e
  tests at the top.
- This repo: **Vitest** for unit/integration, **Playwright** for e2e.

## Quality gates

- A failed unit test blocks the commit/push.
- A failed integration test blocks deploy.
- These gates are deterministic — no "it's probably fine."

## Golden-fixture discipline (tax logic)

- Any change under `src/lib/tax` (or anything computing Anlage KAP/KAP-INV/SO
  values) **must** be verified against golden fixtures — known-correct,
  ELSTER-verified inputs/outputs — not just unit-tested against arbitrary
  expectations.

## Coverage

- Prioritize coverage of critical paths (tax computation, auth, money-handling)
  and edge/boundary cases over raw line-coverage percentage.

---
Source: virtuosoqa.com/post/software-qa-process
