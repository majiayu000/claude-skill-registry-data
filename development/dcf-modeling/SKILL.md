---
name: dcf-modeling
description: Builds a discounted cash flow model with WACC, dual terminal value, and sensitivities when you need an intrinsic value from cash flows.
---

# DCF Modeling Agent

## When to use
Use this when you need an intrinsic value based on cash flows rather than a market read. Typical triggers: the peer set is thin or noisy, the business is undergoing a transition the multiples miss, or you want a fundamentals-anchored cross-check on comps. Reach for it when value should be driven by what the business generates, not what the market currently pays.

## What it does
It produces a DCF: projected unlevered free cash flows discounted at WACC to an enterprise value, a terminal value computed two ways, an EV-to-equity bridge, and a sensitivity grid on WACC and growth.

## Method
1. Project unlevered free cash flow. Build FCF independent of financing.
   - Start from EBIT, tax it at the marginal rate to get NOPAT, add back D&A, subtract capex, and subtract the increase in net working capital, for each explicit year (usually 5 to 10).

2. Build the cost of equity via CAPM. Price the equity risk.
   - Cost of equity equals the risk-free rate plus beta times the equity risk premium; relever beta to the subject capital structure if it was drawn from peers.

3. Build the after-tax cost of debt. Reflect the tax shield.
   - After-tax cost of debt equals the pre-tax cost of debt times one minus the marginal tax rate.

4. Compute WACC. Blend the two at target weights.
   - Weight cost of equity by the equity share of capital and after-tax cost of debt by the debt share, using target or market weights rather than book values.

5. Compute terminal value two ways. Cross-check the tail.
   - Gordon growth: final-year FCF times one plus g, divided by (WACC minus g). Exit multiple: a terminal EV/EBITDA on final-year EBITDA.
   - Reconcile the two: note the implied growth the exit multiple embeds and the implied multiple the growth assumption embeds.

6. Discount to present. Bring cash flows and terminal value back.
   - Discount each explicit FCF and the terminal value at WACC, applying the mid-year convention where appropriate, and sum to enterprise value.

7. Bridge EV to equity. Get to per-share value.
   - Subtract net debt, minority interest, and preferred, add non-operating assets, then divide by diluted shares.
   - Use diluted shares on a treasury-method basis so in-the-money options and convertibles are captured.

8. Sensitize and stress. Show the range, not one number.
   - Flex WACC across a band and perpetuity growth (or the exit multiple) across a band; check terminal value as a share of total EV and flag it if it dominates.

## Inputs
- An operating forecast or three-statement model to draw FCF from
- The marginal tax rate and the D&A and capex outlook
- Working-capital assumptions driving the change in net working capital
- CAPM inputs: risk-free rate, beta, and equity risk premium
- Capital-structure weights and the pre-tax cost of debt
- Net debt, diluted shares, and non-operating items for the bridge
- Terminal assumptions: perpetuity growth and the terminal exit multiple

## Output format
- An assumptions block showing the WACC build component by component
- The unlevered free-cash-flow projection listed by year
- Both terminal value calculations with their implied cross-checks
- The discounting to enterprise value, with the mid-year convention noted if used
- The EV-to-equity bridge down to per-share value
- A sensitivity section describing the per-share range across the WACC and growth bands in prose
- Describe the sensitivity grid in prose, never as a markdown table

## Example
For Cobalt Software (fictional, illustrative): unlevered FCF runs 60, 68, 77, 85, 92 over five years. CAPM gives cost of equity of 11 percent (risk-free 4, beta 1.2, ERP 5.8); after-tax cost of debt is 3.6 percent at a 25 percent tax rate; WACC lands at 9.8 percent. Gordon growth at 3 percent gives a terminal value near 1,300, while a 12x exit multiple gives 1,260, a close cross-check that implies about 3.2 percent embedded growth. Discounted with mid-year convention, EV is about 1,180; less net debt of 150, equity is 1,030, or 20.60 per share on 50 shares. Terminal value is roughly 68 percent of EV, within a normal range. Flexing WACC of 9 to 11 percent and growth of 2 to 4 percent spans roughly 17.50 to 24.00 per share.
