---
model_tier: high
name: dcf-modeling
description: "Wing-4 valuation cognition for a CFO / finance-partner. Use when a deal, internal investment, or board ask names DCF, intrinsic value, WACC, terminal value, or 'what's it worth on a 5-year hold'."
status: active
tier: senior
domain: product
recommended_for_user_types: [finance]
workspaces:
  - finance
packs:
  - finance-advanced
install:
  default: false
  removable: true
---

# dcf-modeling

## When to use

- A buy-build-or-partner decision needs an intrinsic-value anchor, not just a multiple.
- A board pack asks for sensitivity to discount rate or terminal-growth assumptions.
- An acquisition target's seller-deck IRR claims need a counter-model.

Do NOT use for revenue forecasting alone, market-sizing, or comp-multiple-only screens — those route elsewhere (see Related Skills).

## Procedure

### Step 0: Inspect

1. Confirm the target has ≥3 years of audited or reviewed financials, or a clearly-labelled forecast that names every assumption.
2. Note the cognition cluster: this is **intrinsic-value cognition**, not multiple-arbitrage.

### Step 1: Lock the assumption table

1. Pull or estimate the five drivers — revenue growth (per year, declining to terminal), EBIT margin path, tax rate, capex/sales, change in net working capital/sales.
2. Decompose WACC: cost of equity (CAPM — risk-free + β × ERP), cost of debt (after-tax), capital structure target weights.
3. Pick a terminal-value method **once** — either Gordon-growth (`FCFF_t+1 / (WACC − g)`) or exit-multiple. Naming both inflates spurious precision.

### Step 2: Project free cash flow

1. Build a 5-year FCFF row: `EBIT × (1 − t) + D&A − Capex − ΔNWC`.
2. Discount each year by `1 / (1 + WACC)^t`.
3. Compute terminal value at year 5, discount back.
4. Sum PV(FCFF) + PV(TV) = enterprise value. Subtract net debt → equity value.

### Step 3: Sensitivity grid

1. Build a 5×5 grid: WACC ±200 bps × terminal growth ±100 bps (or exit multiple ±2 turns).
2. Flag the corner cells where equity value flips sign or moves >25% from base — those are the load-bearing assumptions.

### Step 4: Validate

1. Cross-check implied EV/EBITDA against trading comps. If your DCF prints 22× and the sector trades at 11×, **the assumptions are wrong**, not the market.
2. State the two assumptions that drive >50% of the valuation. If you can't name them, the model is undisciplined.

## Gotcha

- Terminal value usually carries 60–80% of total PV. Treating TV as a footnote is the most common DCF malpractice.
- WACC sensitivity is non-linear near `WACC ≈ g`; the Gordon formula explodes. Cap displayed cells; don't pretend the corner is a real number.
- Forecasted FCFF that grows faster than revenue forever implies infinite margin expansion — the model will silently smuggle it in unless you bound EBIT margin at a stated ceiling.
- Synergies in an M&A DCF belong in a separate column. Comingling them with standalone FCFF is how acquirers overpay.

## Do NOT

- Do NOT use a DCF as the sole valuation when the business is < 3 years old or has negative operating cash flow — uncertainty bands swamp the signal.
- Do NOT discount levered cash flow by WACC. Use FCFF↔WACC or FCFE↔Ke; never cross.
- Do NOT report a point estimate without the sensitivity grid. A single number is a prediction, not a valuation.

## Related Skills

**WHEN to use this**

- The decision needs intrinsic value, not relative value.
- The asset has a multi-year cash-flow profile worth modelling explicitly.
- The board wants an answer to "what assumption breaks the deal?"

**WHEN NOT to use this**

- Pure unit-economics question (CAC/LTV/payback) — route to [`unit-economics-modeling`](../unit-economics-modeling/SKILL.md).
- Prioritization of competing internal bets, not valuation — route to [`rice-prioritization`](../rice-prioritization/SKILL.md).
- Strategic-objective decomposition, not value — route to [`okr-tree-modeling`](../okr-tree-modeling/SKILL.md).

## When the agent should load this

- "What's this acquisition worth on a 5-year hold?"
- "Build me a DCF on these financials."
- "How sensitive is the valuation to WACC?"
- "What discount rate does the seller's IRR imply?"
- "Counter-model this seller deck."

## Output

1. **`assumptions.md`** — table with five drivers per year + WACC decomposition + terminal-value method. One row per assumption, one column per year.
2. **`fcff-projection.md`** — 5-year FCFF + discount factors + PV column + terminal-value PV + bridge to equity value.
3. **`sensitivity-grid.md`** — 5×5 markdown table (WACC × terminal growth or exit multiple). Bold the cells where equity value flips sign or moves >25% from base.
4. **`valuation-narrative.md`** — three paragraphs: (a) point estimate + range, (b) the two load-bearing assumptions, (c) cross-check against trading comps with named delta.
