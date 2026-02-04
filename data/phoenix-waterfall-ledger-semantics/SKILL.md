---
name: phoenix-waterfall-ledger-semantics
description:
  'Waterfall ledger semantics and clawback behavior for the Phoenix VC fund
  model. Use when working on tier or ledger waterfall code, clawback behavior,
  or waterfall truth cases.'
---

# Phoenix Waterfall Ledger Semantics

You own GP/LP waterfall semantics for both the tier-based and ledger-based
engines, including shortfall-based partial clawback and cross-validation rules.

## When to Use

Invoke this skill when:

- Editing `server/analytics/waterfall-tier.ts` or
  `server/analytics/waterfall-ledger.ts`
- Working on clawback behavior or validating scenario L08 and related cases
- Expanding or debugging waterfall truth-case JSONs
- Syncing waterfall docs/JSDoc with actual behavior

## Files You Own

- Implementation:
  - `server/analytics/waterfall-tier.ts`
  - `server/analytics/waterfall-ledger.ts`
- Types / config:
  - `shared/types/waterfall.ts` (or equivalent config types)
- Truth cases:
  - `docs/waterfall-tier.truth-cases.json`
  - `docs/waterfall-ledger.truth-cases.json`
- Documentation:
  - Waterfall section in `docs/calculations.md`
  - Clawback JSDoc in the waterfall config types

## Core Concepts

### Tier vs. Ledger

- **Tier engine**:
  - Simple tiers (return of capital, preferred, carry splits)
  - No ledger-level clawback

- **Ledger engine**:
  - Full ledger of contributions and distributions
  - Applies **shortfall-based partial clawback**:
    - GP carry is limited by fund-level profit above the LP shortfall
    - If LPs haven't achieved capital + preferred return, GP carry is reduced
      proportionally
    - Not a binary all-or-nothing clawback
    - Not time-based; uses cumulative fund performance at liquidation

Only for simple, no-clawback, no-recycling cases may tier and ledger results be
expected to match.

### Clawback Semantics

Ensure implementation and docs agree:

- Use a shortfall-based formula:
  - `LP shortfall = (required capital + pref) – actual LP distributions`
  - GP clawback = min(GP carry, LP shortfall)
- JSDoc must clearly state:
  - "Shortfall-based partial clawback (NOT hard floor, NOT time-based)"
  - Include a concrete example referencing the relevant truth case (e.g., L08)

## Truth-Case Workflow

1. Identify failing scenario(s) in tier/ledger truth-cases JSON.
2. Run targeted tests:

   ```bash
   npm test -- tests/truth-cases/runner.test.ts -t "<scenario-id>"
   ```

3. Compare:
   - Expected vs actual totals (LP distributions, GP carry, clawback)
   - Row-level distributions for ledger scenarios (e.g., quarterly rows)

4. Decide:
   - JSON wrong → fix truth case and re-run
   - Implementation wrong → adjust code, keep semantics aligned with docs and
     plan

## Documentation Sync

Whenever you change behavior:

- Update:
  - `docs/calculations.md` waterfall section
  - JSDoc for waterfall config and key functions
- Include:
  - Plain-English description of clawback behavior
  - Example using a real truth-case ID

## Invariants

- Clawback must never cause LPs to receive less than capital + pref while GP
  receives carry.
- Ledger engine must respect the LPA semantics described in the plan and JSDoc.
- Tier engine is not used to validate clawback scenarios.
