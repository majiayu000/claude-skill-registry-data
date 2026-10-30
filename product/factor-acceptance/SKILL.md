---
name: factor-acceptance
description: TrueAlpha Factor Acceptance Protocol. Enforces the strict quantitative rules for factor computation, PIT semantics, composite confidence bounds, and anti-fraud gating.
---

# TrueAlpha Factor Acceptance Protocol

> **Core Axiom (AGENTS.md & init.md)**:
> *"A constant never stands in for a measurement. Never overwrite a point-in-time record. Never put computation logic outside `common/factors`. Factor inputs are provenance-neutral typed records. Composite confidence cannot exceed the minimum consumed confidence."*

## 1. When to Activate This Skill
- When designing, reviewing, or modifying any factor module in `common/factors`.
- When adding or reviewing composite factor definitions (such as three-tier valuation, strategy evaluators).
- When validating factor outputs against ground-truth datasets.

## 2. Mandatory Verification Checklist

### 1. Point-in-Time & Measurement Integrity
- [ ] **Dual Timestamps**: Distinguish `valid_time` from `transaction_time` (knowable-at).
- [ ] **No Clock Defaults**: `transaction_time` must come from an explicit source property, never an insertion-clock default (`now()`).
- [ ] **No Hardcoded Constants**: Universe size, obligation count, denominator cells (never hardcode 84 cells!), growth window, freshness, and confidence scores (never stamp `0.85`, `0.92`, or `1.00`) must be derived from the run and the continuous `0-100` confidence model (`source prior x agreement x freshness x lineage`), not hardcoded.
- [ ] **Decimal Monetary Arithmetic**: Use `Decimal` with explicit rounding context (`ROUND_HALF_EVEN`) for monetary values; binary floating point (`float`) is strictly prohibited.

### 2. Degenerate & Missing Data Gating
- [ ] **Explicit Gaps Beat Silent Drops**: If data is missing or unsourced, return `value=None` with an explicit reason code (e.g. `growth_convention_unsourced:analyst_consensus`), never substitute 0, a sentinel, or a silent default.
- [ ] **Corporate Action Awareness**: Per-share metrics (like EPS) must not be compared across stock splits without split adjustment. When corporate actions are unadjusted, net income must anchor growth rates.

### 3. Composite Factor Rules (Module 7)
- [ ] **Confidence Bounding**: Composite factor confidence must satisfy:
  $$\text{confidence}_{\text{composite}} \le \min_{i}(\text{confidence}_{\text{input}_i})$$
- [ ] **Availability & Score Propagation**: Every computed value is served (`available`) alongside its continuous `0-100` confidence score (`High` $\ge 80$, `Medium` $60\text{–}79$, `Low` $< 60$). Low confidence lowers the composite score; it never silently drops or blocks the row.
- [ ] **Materialized Inputs Only**: Composite factors reload materialized upstream factor results from `mart`; they never branch on raw source vendors or bypass the mart layer.

### 4. Standing Checks (skills `smoke` and `close`)
- [ ] **Whole Scope Covered**: Every deliverable in the issue scope has a standing check.
- [ ] **Reproducible Red**: Confirm the check goes RED against the unfixed code before declaring victory.
- [ ] **Fail Where Production Calls**: Test passes data through the exact deployed call signature.
