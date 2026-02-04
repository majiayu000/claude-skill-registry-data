---
name: phoenix-xirr-fees-validator
description:
  'Validation for XIRR and fee calculations. Use when working on
  server/analytics/xirr.ts, server/analytics/fees.ts, or their truth cases.'
---

# Phoenix XIRR & Fees Validator

You ensure XIRR and fee calculations match their intended behavior and, where
applicable, Excel parity.

## When to Use

- Debugging or refactoring:
  - `server/analytics/xirr.ts`
  - `server/analytics/fees.ts`
- Editing:
  - `docs/xirr.truth-cases.json`
  - `docs/fees.truth-cases.json`
- Cross-checking against Excel/Sheets XIRR or simple fee math.

## XIRR

- Use irregular cash-flow IRR with proper date handling.
- Align sign conventions with truth cases:
  - Investments → negative
  - Distributions → positive
- Where feasible, cross-check a subset of scenarios against Excel's `XIRR()`
  using the `excelFormula` field in JSON.

## Fees

- Confirm:
  - Management fee = % of the correct base (committed or called, depending on
    config).
  - Fee timing matches the fund life / fee schedule.
- Truth cases should include:
  - Simple "2% of commitment" scenarios.
  - Step-down and alternative-fee-basis examples if implemented.

## Tests & Truth Cases

- For any change:
  - Re-run only XIRR and fees sections of the truth-case suite first.
  - Then run the full suite.
- If you update expectations:
  - Fix the JSON.
  - Document in `docs/phase0-validation-report.md` what changed and why.
