---
name: lbo-modeling
description: Builds an LBO model with sources and uses, a debt schedule, and returns when you need to test a sponsor buyout and its economics.
---

# LBO Modeling Agent

## When to use
Use this when you need to test a sponsor buyout and its returns rather than a strategic or intrinsic value. Typical triggers: assessing whether a financial buyer can pay a given price, setting a floor in a valuation range, or stress-testing leverage and returns. Reach for it when the question is what a sponsor can pay and still hit its return hurdle.

## What it does
It produces an LBO model: a sources-and-uses table, an entry with leverage, a debt schedule with a cash sweep, an exit, and returns (IRR and MOIC) decomposed into a value-creation bridge across EBITDA growth, multiple change, and debt paydown.

## Method
1. Set the entry. Fix price and hold.
   - Set entry EV as a multiple of LTM EBITDA, and establish the transaction date and hold period (commonly 5 years).

2. Build sources and uses. Make them tie.
   - Uses: purchase equity value, refinanced debt, and transaction fees. Sources: new debt tranches sized to a leverage target in turns of EBITDA, with sponsor equity as the plug; total sources must equal total uses.

3. Project the operating case. Get to cash for debt service.
   - Grow revenue and EBITDA off drivers, then subtract capex, the change in working capital, and cash taxes to reach free cash flow available for debt paydown, kept consistent with any three-statement model.

4. Build the debt schedule. Track each tranche.
   - For each tranche roll opening balance, mandatory amortization, cash interest, and the closing balance; apply an optional cash sweep of excess free cash flow to prepay debt in priority order.

5. Resolve the interest circularity. Keep the model stable.
   - Interest depends on the debt balance, which depends on the sweep, which depends on cash after interest; resolve with iterative calculation or a circuit-breaker toggle.

6. Set the exit. Value the equity at sale.
   - Apply an exit EV/EBITDA multiple (often the entry multiple held flat in the base case) to exit-year EBITDA for exit EV, then subtract net debt at exit for exit equity value to the sponsor.
   - Assuming exit above entry is aggressive; keep the base case flat and treat any expansion as upside to be defended.

7. Compute returns. Measure the outcome.
   - MOIC equals exit equity divided by entry equity; IRR is the annualized return over the hold, reflecting the timing of any interim distributions or dividend recap.
   - Watch the split: a high MOIC on a long hold can still miss the IRR hurdle, so report both rather than one alone.

8. Build the value-creation bridge. Explain where returns came from.
   - Decompose the equity gain into EBITDA growth (at constant entry multiple), multiple expansion or contraction, and debt paydown, then sensitize returns on entry multiple, leverage, and exit multiple.

## Inputs
- Entry EBITDA and the entry EV multiple
- An operating forecast or three-statement model for the hold period
- Debt terms: tranche sizes or a leverage target, rates, and amortization
- Cash-sweep rules and repayment priority across tranches
- Transaction fees and any financing fees
- The hold period and the exit-multiple assumption
- The sponsor return hurdle to test against

## Output format
- A sources-and-uses section with the tie shown
- The operating case by year, down to free cash flow available for debt paydown
- The debt schedule by tranche and year, with the cash sweep applied
- The exit calculation from exit EBITDA and exit multiple to exit equity value
- A returns section stating IRR and MOIC
- A value-creation bridge splitting the equity gain into EBITDA growth, multiple change, and debt paydown, plus a sensitivity on the key levers
- Present all schedules in prose, never as markdown tables

## Example
For Cobalt Software (fictional, illustrative): entry at 10.0x LTM EBITDA of 100 sets EV at 1,000; with 5.0x leverage (500 of debt) and 30 of fees, sponsor equity is 530. EBITDA grows to 150 by year 5 while the cash sweep pays debt down from 500 to 250. At a flat 10.0x exit, exit EV is 1,500, and less 250 of net debt gives 1,250 of equity: MOIC of 2.4x and IRR near 19 percent, above a 15 percent hurdle. The value-creation bridge attributes the roughly 720 of equity gain about 500 to EBITDA growth, 0 to multiple change (held flat), and 250 to debt paydown, less fee drag. Cutting the exit multiple to 9.0x drops MOIC to about 2.1x, showing the return leans on operating growth, not multiple expansion.
