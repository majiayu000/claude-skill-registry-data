---
name: dcf-valuation-builder
description: "Builds a transparent Discounted Cash Flow (DCF) valuation with a 5-10 year forecast, terminal value, Weighted Average Cost of Capital (WACC) derivation, sensitivity tables, and a football-field summary. Use when valuing a company, business unit, acquisition target, or capital project; pressure-testing an investment thesis; preparing a board valuation memo; or stress-testing assumptions against precedent transactions and trading comparables."
---

# DCF Valuation Builder

> Defensible intrinsic-value modeling that holds up in an Investment Committee (IC), audit committee, or Mergers and Acquisitions (M&A) negotiation.

## What this skill is

A structured, auditable workflow that turns a set of financial assumptions into a Discounted Cash Flow (DCF) model with explicit reasoning at every step. It builds the revenue and operating model bottoms-up, derives the Weighted Average Cost of Capital (WACC) from first principles, reconciles two terminal-value methods, and triangulates the output against trading and transaction comparables on a football field.

## What it solves

- Hand-waved valuations where the discount rate is hardcoded and the terminal value drives everything
- Single-point answers that hide enormous sensitivity to a few inputs
- Force-fitting a number to a target price with no traceability
- Forecasts disconnected from operating drivers (revenue, margin, capital expenditure, working capital)
- Inability to defend assumptions when an Investment Committee (IC) or board pushes back

## When to invoke

- Valuing a company, business unit, or Mergers and Acquisitions (M&A) target for an internal memo
- Building a fairness opinion or board valuation pack
- Stress-testing a sell-side or banker model
- Comparing strategic investment options on an apples-to-apples Net Present Value (NPV) basis
- Re-underwriting an existing investment after material new information

## Phase 1: Scope and inputs

Before modeling, establish:
- Valuation date and fiscal-year convention
- Valuation purpose (M&A, fairness opinion, Internal Rate of Return (IRR) hurdle, restructuring, tax)
- Currency and inflation assumptions
- Forecast horizon (5 years default; 10 years for long-cycle assets like infrastructure, pharmaceuticals, energy)
- Available data: 3-5 years historical financials, management forecast, comparable set, recent transactions

Log every input source with file name, date, and confidence rating (High / Medium / Low).

## Phase 2: Revenue build (bottoms-up)

Pick the right driver tree:
- **Software as a Service (SaaS) or subscription**: net new Annual Recurring Revenue (ARR) = (new logos × Annual Contract Value (ACV)) + (expansion − churn); revenue = beginning ARR + ½ × net new ARR
- **Transactional or marketplace**: Gross Merchandise Value (GMV) × take-rate
- **Volume × price**: units × Average Selling Price (ASP), broken by segment or geography
- **Consumption**: active users × Average Revenue Per User (ARPU) × engagement

Always show three scenarios - Base, Bull (+1 standard deviation), Bear (−1 standard deviation) - with explicit Compound Annual Growth Rate (CAGR) for each.

## Phase 3: Operating model

Forecast each line as **percent of revenue** with a credible glide path to terminal margins:

| Line item | Year 1 | Year 5 | Terminal | Convergence logic |
|-----------|--------|--------|----------|-------------------|
| Gross margin | X% | Y% | Z% | Mature peer benchmark |
| Sales and Marketing (S&M) | X% | Y% | Z% | Lifetime Value to Customer Acquisition Cost (LTV/CAC) discipline |
| Research and Development (R&D) | X% | Y% | Z% | Innovation intensity |
| General and Administrative (G&A) | X% | Y% | Z% | Operating leverage |
| Earnings Before Interest and Taxes (EBIT) margin | X% | Y% | Z% | Industry steady state |

Build to Unlevered Free Cash Flow (UFCF):

```
UFCF = EBIT × (1 − tax rate) + Depreciation and Amortization (D&A) − capital expenditure − Δ Net Working Capital (NWC)
```

Validate that capital expenditure approximately equals D&A at terminal year (steady-state requirement).

## Phase 4: WACC derivation

Show every input - never hardcode WACC.

| Component | Value | Source |
|-----------|-------|--------|
| Risk-free rate (10-year U.S. Treasury) | x.xx% | Federal Reserve / Bloomberg |
| Equity Risk Premium (ERP) | x.xx% | Damodaran / Duff & Phelps |
| Levered beta | x.xx | Comparable companies, re-levered |
| Cost of equity via Capital Asset Pricing Model (CAPM) | x.xx% | Risk-free rate + β × ERP |
| Pre-tax cost of debt | x.xx% | Yield to Maturity (YTM) or synthetic credit rating |
| After-tax cost of debt | x.xx% | × (1 − tax rate) |
| Target debt / (debt + equity) | x.xx% | Industry median capital structure |
| **WACC** | **x.xx%** | Weighted sum |

Add country risk premium and small-company size premium where applicable.

## Phase 5: Terminal value

Use **both** methods and reconcile:

1. **Gordon growth (perpetuity)**: Terminal Value (TV) = Free Cash Flow (FCF) at year n+1 / (WACC − g), with g ≤ long-run nominal Gross Domestic Product (GDP) growth
2. **Exit multiple**: TV = terminal-year Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA) × peer median Enterprise Value / EBITDA (EV/EBITDA)

Show the implied perpetuity growth from the exit multiple, and the implied exit multiple from the perpetuity. Flag unrealistic values (g > 5%, exit multiple > 25×) and explain.

## Phase 6: Discount and bridge to equity

- Use mid-year convention unless cash flows are seasonal
- Discount each year's UFCF plus TV to Present Value (PV) → **Enterprise Value (EV)**
- Bridge: Equity value = EV − debt − preferred equity − minority interest + cash + non-core assets
- Divide by diluted shares (treasury stock method) → implied share price

## Phase 7: Sensitivity and football field

Produce a 2-way sensitivity on the top drivers (typically WACC × g, or WACC × terminal margin):

|         | g = 1.5% | g = 2.0% | g = 2.5% | g = 3.0% |
|---------|---------:|---------:|---------:|---------:|
| WACC 8% | $xx | $xx | $xx | $xx |
| WACC 9% | $xx | $xx | $xx | $xx |
| WACC 10%| $xx | $xx | $xx | $xx |

Triangulate on a football field: trading comparables, precedent transactions, 52-week trading range, Leveraged Buyout (LBO) floor, sum-of-the-parts.

## Output

- One-page valuation memo with value range, midpoint, and recommended point estimate
- WACC build, terminal value reconciliation, and sensitivity table
- Football field with at least 3 cross-check methods
- Top 3 value drivers and top 3 risks (with downside cases quantified)
- Explicit list of "what would change the call"

## Operating rules

**Always**
- Show every formula; no black-box outputs
- Tie every assumption to a source or benchmark
- Reconcile both terminal value methods
- Stress-test with a downside case where IRR < WACC
- Present a range, never a single point

**Never**
- Force-fit a target valuation
- Use a discount rate without showing CAPM derivation
- Assume perpetuity growth above long-run GDP
- Skip the bridge from EV to equity value
- Confuse equity value with enterprise value
