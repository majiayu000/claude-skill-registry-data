---
name: strategy-add
description: Add or integrate a strategy within the current trading-bot architecture without breaking scorer flow, WAIT explainability, reporting, paper position handling, or hard risk ordering. Use when introducing a new strategy module or changing how strategy outputs feed the existing analysis stack.
---

# Strategy Add

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — strategies sit in **L2–L4** signal/scoring space; outputs must remain explainable for **L5** and observability.
- **`AGENTS.md`** — signals flow through risk (**L7**) and paper execution; **no black-box** metadata.

## Purpose

Use this skill when strategy work must fit the current end-to-end pipeline:
- regime-aware scoring
- WAIT explainability metadata
- non-bypassable risk and execution-quality gates
- paper position lifecycle and portfolio reporting
- shadow analytics and operator panel summaries

## Use When

Use this skill when:
- introducing a new strategy module under `app/strategies`
- wiring a strategy into scorer, reporting, or manual-review analytics
- extending signal metadata needed by explainability or shadow summaries

## Do Not Use When

Do not use this skill for:
- isolated parameter tuning in an existing strategy
- scorer-confidence experiments that do not change raw strategy outputs
- portfolio sizing or risk-only changes

## Required Checks

- Keep the strategy in its own small module.
- Return a structured signal object with action, confidence, reason, and any required explainability metadata.
- Integrate cleanly with scorer inputs and current reporting paths.
- Preserve WAIT explainability and journal readability.
- Confirm new signals still flow through existing risk, quality gate, and paper-only execution order.
- Update README only if the workflow or operator-visible behavior changed.

## Expected Output

- `Strategy:` name and thesis.
- `Integration Points:` scorer, reporting, journal, or panel surfaces touched.
- `Safety Check:` paper-only and risk-order impact.
- `Validation:` exact checks run.
