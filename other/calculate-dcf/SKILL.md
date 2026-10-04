---
name: calculate-dcf
description: Use when valuing a company, project, or asset using discounted cash flow analysis
source: CFA Institute Level II curriculum; Damodaran's "Investment Valuation" (3rd ed.); McKinsey "Valuation" (7th ed.)
tags: [finance, investing, valuation, dcf, wacc, modeling]
verified: true
---

# Calculate DCF

Build a discounted cash flow valuation to estimate the intrinsic value of an asset.

## Why This Is Best Practice

**Adopted by:** CFA Institute, investment banks (Goldman Sachs, Morgan Stanley), private equity firms globally
**Impact:** DCF remains the dominant valuation methodology for intrinsic value; Damodaran's NYU research shows it outperforms multiples-based methods for long-horizon investments.

**Why best:** DCF forces explicit assumptions about growth, margins, and risk, making them auditable. Unlike comparable-company analysis, DCF anchors value to fundamental cash generation rather than market sentiment. Proper WACC construction links capital structure to the discount rate, keeping the model internally consistent.

## Steps

1. **Project free cash flow** — Forecast FCFF (EBIT × (1 − tax rate) + D&A − CapEx − ΔNWC) for 5–10 years; use three scenarios (base, bull, bear).
2. **Determine the discount rate (WACC)** — WACC = (E/V) × Re + (D/V) × Rd × (1 − T); use CAPM for cost of equity (Re = Rf + β × ERP); source beta from comparable public firms if private.
3. **Estimate terminal value** — Apply Gordon Growth Model (TV = FCFFn+1 / (WACC − g)) or exit-multiple method; g should not exceed long-run nominal GDP growth (~3–4%).
4. **Discount all cash flows** — PV = Σ [FCFFt / (1 + WACC)^t] + TV / (1 + WACC)^n.
5. **Calculate equity value** — Enterprise Value = PV of FCFFs + TV; Equity Value = EV − Net Debt − Minority Interest + Cash.
6. **Run sensitivity analysis** — Build a two-way table varying WACC (±100 bps) and terminal growth rate (±50 bps); this is mandatory, not optional.
7. **Sanity-check against comps** — Validate implied EV/EBITDA and P/E multiples against industry peers; large deviations demand explanation.
8. **State assumptions explicitly** — Document every key assumption with its rationale; a DCF is only as trustworthy as its inputs.

## Rules

- Never use a terminal growth rate above the long-run nominal GDP growth rate.
- Always discount terminal value at the same WACC as interim cash flows.
- Use unlevered free cash flow (FCFF) when computing enterprise value; switch to FCFE only for equity value directly.
- Perform sensitivity analysis on at minimum WACC and terminal growth rate before presenting results.
- Cross-check equity value per share against current market price; document the implied premium or discount.

## Examples

**SaaS company, 5-year horizon:** Revenue $50M growing 30% YoY, EBIT margin expanding from 10% to 25%, WACC = 12%, terminal growth = 3%. Base-case equity value = $420M vs. market cap of $380M → 10.5% upside; bear case = $290M, bull case = $610M. Sensitivity table shows value crosses market price at WACC > 13.8%.

## Common Mistakes

- **Using book-value weights for WACC** — WACC must use market-value weights; book values systematically understate equity.
- **Ignoring working-capital changes** — Failing to include ΔNWC overstates FCF for high-growth businesses.
- **Single-point estimate without sensitivity** — A DCF without sensitivity analysis is false precision; ranges are the real output.
- **Terminal value dominating EV (>80%)** — Signals projection period is too short or growth assumptions are too aggressive.

---

> **Finance disclaimer:** This skill encodes professional best practices for educational purposes. It is not financial advice. Consult a licensed financial advisor before making investment decisions.
