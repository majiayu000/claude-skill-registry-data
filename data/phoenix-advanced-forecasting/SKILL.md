---
name: phoenix-advanced-forecasting
description:
  "Architecture for the 'living model': graduation rates, multi-MOIC analysis,
  reserves ranking, scenarios, and Monte Carlo. Always sits on top of the
  deterministic core."
---

# Phoenix Advanced Forecasting

You are the architectural and implementation guide for Phoenix's probabilistic
"living model" layer, built on top of a validated deterministic fund engine.

The deterministic core (Phase 1) handles:

- Fees / XIRR / Waterfalls / Capital allocation / Recycling
- 6-decimal precision and JSON truth-case validation

The probabilistic layer (Phase 2) adds:

- Graduation & exit models
- Multi-MOIC analysis
- Reserves ranking and optimization
- Scenario management
- Monte Carlo simulation

## 1. When to Use

Use this skill when:

- Designing or modifying:
  - Graduation rate / exit / failure rate models
  - MOIC variants (current, exit, initial vs follow-on, MOIC on reserves,
    opportunity cost)
  - Portfolio ranking and reserve optimization
  - Construction vs Current scenarios
  - Monte Carlo simulations over the deterministic engine
- Adding "living model" features that ingest deterministic outputs and produce
  distributions or optimized decisions.

Do **not** use this skill:

- For fixing deterministic math bugs (hand off to the relevant deterministic
  skill).
- For precision or type-safety work (hand off to `phoenix-precision-guard`).

## 2. Architecture Overview

```text
User Inputs
  └─► Deterministic Engine (Phase 1)
        • Fees / XIRR / Waterfall / Capital Allocation / Recycling
        • 6-decimal precision / JSON truth cases / Excel parity
          ↓
  Probabilistic Layer (Phase 2)
        • Graduation & exit engines
        • MOIC calculation suite (multiple types)
        • Portfolio ranking & reserves optimization
        • Scenario builder (Construction vs Current)
        • Monte Carlo orchestrator
          ↓
  Outputs
        • Distributions (TVPI, DPI, MOIC, IRR)
        • Optimal reserves ranking ("next dollar" decisions)
        • Scenario comparisons & dashboards
```

Principles:

- Never inject randomness into Phase 1 modules.
- Treat Phase 1 outputs as pure building blocks.
- Allow deterministic "Expectation Mode" for every probabilistic component.

## 3. Graduation Rate Engine

For each stage:

- Inputs:
  - `graduationRate`, `exitRate`, `failureRate`
  - `avgMonthsToEvent`
- Constraint:
  - `graduationRate + exitRate + failureRate = 1.0`
- Provide:
  - `expectedTransition(params)` – deterministic expectation for testing
  - `sampleTransition(params, rng)` – stochastic draws for Monte Carlo

Expected use:

- Drive:
  - Stage counts over time
  - Follow-on demand based on graduations
  - Exit timing distributions

## 4. MOIC Calculation Suite

Implement MOIC variants as **pure deterministic functions**:

Recommended variants:

1. Current MOIC (mark-to-market on total invested capital)
2. Exit MOIC (projected)
3. Initial-only MOIC
4. Follow-on-only MOIC
5. Blended MOIC (initial + follow-on)
6. Exit MOIC on planned reserves (core "next dollar" metric)
7. Opportunity cost MOIC (this dollar vs alternatives)

These should:

- Decompose performance between initial and follow-on checks.
- Handle partial exits and convertibles where applicable.
- Use the same decimal precision conventions as Phase 1.

## 5. Portfolio Ranking & Reserves Optimization

Design ranking as:

- Inputs:
  - MOIC breakdowns
  - Planned reserves per company
  - Graduation/exit expectations
- Outputs:
  - Ranked list of companies by "Exit MOIC on planned reserves" (or chosen
    metric)
  - Suggested reserve allocation subject to a total reserves constraint

Guidelines:

- Avoid mutating core capital allocation; treat this as a "decision support"
  layer.
- Make ranking criteria explicit and user-configurable.

## 6. Scenario Management & Monte Carlo

Scenario types:

- Construction forecast – original plan
- Current forecast – plan + actuals/remaining capital

Scenario management should:

- Allow toggling individual deals/assumptions on/off
- Compare multiple scenarios side-by-side
- Export/import scenario configs to/from JSON or CSV

Monte Carlo:

- Wrap deterministic forecast calls in a loop.
- Use configurable:
  - `iterations`
  - `seed`
  - scenario set
- Aggregate results into:
  - Distributions (means, percentiles) for TVPI, DPI, MOIC, IRR

## 7. Validation

For every probabilistic feature:

- Provide a deterministic "Expectation Mode":
  - No randomness, just expectations.
- Validate expectation mode against:
  - Analytical calculations
  - Excel/Sheets model where applicable
- Add tests for:
  - Distribution means ≈ expectations
  - Valid ranges and normalization of probabilities
  - No negative or impossible metrics

## 8. Invariants

- Phase 2 must never degrade Phase 1 truth-case pass rates.
- All probabilistic modules must be seedable and testable.
- Scenario and Monte Carlo outputs must be explainable to LPs in plain language.
