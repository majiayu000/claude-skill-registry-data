---
name: phoenix-precision-guard
description:
  'Precision and type-safety hardening for Phoenix calculation paths. Use when
  configuring ESLint/TypeScript, replacing parseFloat in P0 files, or validating
  Decimal.js precision.'
---

# Phoenix Precision Guard

You enforce numeric precision and type safety for all P0 calculation paths in
the Phoenix VC fund model.

## When to Use

Invoke this skill when:

- Removing or triaging `parseFloat` in calculation code
- Tightening ESLint or TypeScript strictness for analytics modules
- Configuring or validating Decimal.js usage
- Adding or updating precision tests
- Investigating numeric drift or rounding errors in calculations

Do **not** use this skill for:

- Waterfall semantic changes (use `phoenix-waterfall-ledger-semantics`)
- Truth-case orchestration (use `phoenix-truth-case-orchestrator`)
- XIRR or fee logic bugs (use `phoenix-xirr-fees-validator`)
- Probabilistic/Monte Carlo work (use `phoenix-advanced-forecasting`)

## Scope

P0 calculation files include (non-exhaustive):

- `server/analytics/xirr.ts`
- `server/analytics/waterfall-*.ts`
- `server/analytics/fees.ts`
- `server/analytics/capital-allocation.ts`
- `server/analytics/exit-recycling.ts`
- `server/utils/financial.ts`
- `client/src/core/engines/*.ts`

## ESLint & TS Rules

### ESLint

- Ban `parseFloat` in P0 paths.
- Require explicit radix for `parseInt`.
- Disallow implicit type coercion in calculation code (except `!!` as needed).

Run:

```bash
/fix-auto
# or
npm run lint
```

### TypeScript Strictness

Incrementally enable:

- `noImplicitAny`
- `strictNullChecks`
- `strictFunctionTypes`
- `noImplicitReturns`

For each flag:

1. Enable in `tsconfig.json`.
2. Run `npm run check`.
3. Fix errors in P0 calculation files first.
4. Baseline non-P0 issues with `@ts-expect-error` and a comment referencing the
   phase.

## parseFloat Triage

1. Find all occurrences:

   ```bash
   rg "parseFloat" server/analytics/ client/src/core/engines/
   ```

2. Classify each usage:
   - Calculation → replace with Decimal.js (`new Decimal(value)` or
     `Decimal(value)`).
   - Config/ENV integer → `parseInt(value, 10)`.
   - Non-critical/test → deprioritize.

3. After each batch of replacements:
   - Run the truth-case suite.
   - Confirm no regression in pass rate.

## Decimal.js Precision

- Ensure a single central configuration (e.g., in a shared utility) sets
  precision, e.g.:

  ```typescript
  Decimal.set({ precision: 20 });
  ```

- Add a dedicated precision test file (e.g., `tests/unit/precision.test.ts`)
  asserting behavior like:
  - `0.1 + 0.2 = 0.3`
  - Long chains of operations remain stable.

## Invariants

- Truth-case pass rates must remain ≥ baseline after precision refactors.
- No new P0 calculation path should use native `number` math where precision
  matters.
- TypeScript and ESLint errors in P0 files must be fixed, not silenced.
