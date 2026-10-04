---
name: capital-structure
description: Reads and reshapes the mix of debt and equity with leverage and cost-of-capital metrics, use it when you need to analyze or optimize a capital structure.
---

# Capital Structure Agent

## When to use
Use this when you need to read a company's existing mix of debt and equity or reshape it toward a target. This comes up when assessing debt capacity for an acquisition, evaluating a refinancing, or advising on whether a balance sheet is under or over-levered. This agent builds the current structure, the key ratios, and a comparison to a target.

## What it does
It produces a capital structure view: the current debt and equity mix built out by instrument, net debt and leverage metrics, interest coverage, a weighted average cost of capital estimate, and a side-by-side comparison to a proposed target structure.

## Method
1. Build the current structure by instrument.
   - List each debt tranche (revolver, term loans, senior notes, subordinated debt) with balance, coupon, maturity, and security, then equity by class.
   - This priority-ordered picture is the base for every ratio that follows.

2. Compute net debt.
   - Net debt equals total debt less cash and cash equivalents.
   - Show gross and net separately so the cash position stays visible.

3. Calculate leverage.
   - Compute net debt to EBITDA, and where relevant gross debt to EBITDA and net debt to (EBITDA less capex).
   - Use a normalized EBITDA and note any add-backs, since aggressive adjustments flatter leverage.

4. Compute interest coverage.
   - Compute EBITDA divided by cash interest, and optionally (EBITDA less capex) divided by interest.
   - This tests how comfortably the company services debt through a downturn.

5. Estimate the cost of each capital component.
   - After-tax cost of debt per tranche uses the coupon and the tax shield; cost of equity uses CAPM with the risk-free rate, beta, and equity risk premium.
   - Common pitfall: using book weights; use market values.

6. Compute WACC.
   - Weight each component by market value and blend the after-tax costs.
   - State the weights and inputs so the number is auditable rather than a black box.

7. Define the target structure.
   - Set the desired leverage and instrument mix, informed by debt capacity, covenant headroom, and where comparable companies sit.
   - Good looks like: a target the company can actually reach from current cash flow.

8. Compare current to target.
   - State the change in leverage, coverage, and WACC, the incremental debt capacity or paydown implied, and the practical steps to get there (refinance, raise, or repay).

## Inputs
- The current debt schedule: tranches, balances, coupons, maturities, security
- Cash balance and normalized EBITDA, with capex if available
- Equity value or share count and price, plus beta
- Market inputs: risk-free rate, equity risk premium, tax rate
- Comparable-company leverage levels for benchmarking
- The target leverage or structure you are testing
- Any near-term maturities or covenant tests

## Output format
- Current structure: each instrument with balance and terms, in priority order.
- Metrics block: gross and net debt, leverage ratios, interest coverage, and WACC with the component costs and market-value weights shown.
- Target structure: the desired leverage and mix.
- Comparison: changes in leverage, coverage, and WACC, the implied debt capacity or paydown, and the financing action to get there.
- Describe any table as structured text, never a rendered markdown table.

## Example
Meridian Foods, current structure. Debt in priority order: revolver drawn 20m, term loan 180m at 6.5% due 2029 (secured), senior notes 100m at 7.25% due 2031. Cash 40m, so gross debt 300m and net debt 260m. On normalized EBITDA of 65m with add-backs disclosed, net leverage is 4.0x and interest coverage is 3.1x. After-tax cost of debt roughly 5.2%, cost of equity via CAPM roughly 11% on a beta of 1.1, and blended WACC roughly 8.4% at market weights of 55% equity and 45% debt. Target: bring net leverage to 3.0x, implying about 65m of paydown from free cash flow over two years, which lifts coverage toward 3.9x and lowers WACC modestly as the equity weight rises.
