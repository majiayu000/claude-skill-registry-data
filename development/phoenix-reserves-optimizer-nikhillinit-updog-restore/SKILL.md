---
name: phoenix-reserves-optimizer
description:
  'Reserve allocation and follow-on optimization for the Phoenix fund model. Use
  when working on deterministic reserve engine logic and optimal reserves
  ranking.'
---

# Phoenix Reserves Optimizer

You handle reserve sizing and follow-on allocation logic, especially around the
deterministic reserve engine and "next dollar" optimization.

## When to Use

- When implementing or refactoring:
  - `DeterministicReserveEngine.calculateReserves(...)`
  - Any code that computes or displays optimal reserves or "next dollar" metrics
- When linking reserve logic to:
  - `state.forecastResult.portfolio`
  - `state.graduationMatrix`
  - `state.stageStrategies`

## Core Concepts

- **Inputs:**
  - Total fund size
  - Portfolio companies and their staged investments
  - Graduation matrix and stage strategies
  - Available reserve pool (e.g., 40% of total capital)

- **Outputs:**
  - Per-company reserve recommendations
  - Fund-level reserves usage
  - Metrics that can underpin:
    - "Exit MOIC on planned reserves"
    - Opportunity cost of deploying reserves into each company

## Workflow

1. Compute:
   - `totalCapital = fundSize * 1_000_000`
   - `initialCapital` from initial checks
   - `availableReserves` from user-defined ratio (e.g., 40%)

2. Call the reserve engine with:
   - Portfolio
   - Graduation matrix
   - Stage strategies
   - Available reserves

3. Verify:
   - Sum of allocated reserves ≤ availableReserves
   - No negative or NaN allocations
   - Edge cases when reserves are insufficient are handled gracefully (e.g.,
     proportional scaling).

4. Document:
   - Any assumptions about prioritization (e.g., later-stage vs earlier-stage
     deals).
   - How reserves are scored/ranked.

## Validation Patterns

### Edge Cases to Test

- **Zero reserves available**: Ensure graceful handling (no allocations, not
  errors)
- **Insufficient reserves**: Proportional scaling across portfolio
- **Single company**: All reserves allocated to one deal
- **Negative values**: Detect and reject invalid inputs

### Example Validation

```typescript
// Reserve allocation constraints
expect(totalAllocated).toBeLessThanOrEqual(availableReserves);
expect(allocations.every((a) => a >= 0)).toBe(true);
expect(allocations.some(isNaN)).toBe(false);
```

## Invariants

- Total reserved capital must never exceed the configured reserves pool.
- Changes to the reserve engine must not break existing reserve analytics or
  dashboards.
