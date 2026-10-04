---
name: LBO Structuring
description: Builds the sponsor base case -- sources and uses that tie, leverage in turns, the cash sweep, a flat-multiple exit, and returns as both IRR and MOIC with a value-creation bridge -- when you need to know what a structure pays and where the return comes from.
---

# LBO Structuring

## When to use

Use this skill when the entry price is live and you need to know what the structure returns, not what the seller says the business is worth. It fixes one base case -- one entry multiple, one capital structure, one exit -- for sensitivity work to flex against, and belongs before an indicative bid, not after.

## What it does

Produces the sponsor base case: sources and uses that tie to the dollar, leverage in turns of QoE-adjusted EBITDA, an annual cash sweep, a flat-multiple exit, and returns as both IRR and MOIC with a bridge splitting the equity gain into EBITDA growth, multiple change and debt paydown.

## Method

### Step 1 -- Fix the entry and tie sources to uses

Entry EV is the entry multiple times QoE-adjusted EBITDA -- never management-adjusted, because the haircut is the argument. Uses are purchase price, refinanced debt, fees and closing adjustments; sources are debt in turns of that same EBITDA, rollover, and sponsor equity as the plug. Sources must equal uses to the dollar before any return is computed, and fees are real equity: they sit in uses and never appear at exit. State leverage in turns, and equity as a percentage of EV.

### Step 2 -- Build the cash available, then sweep it

EBITDA less capex, less the movement in net working capital, less cash taxes, less cash interest is what sweeps. Cash taxes rise as the interest shield shrinks, so a flat tax line flatters late-year deleveraging, where most of the sweep sits. Model the step-downs the credit agreement contains -- typically 75% below 4.0x, 50% below 3.0x -- not a full sweep for five years, and resolve the interest circularity with iteration or a circuit breaker.

### Step 3 -- Exit at a flat multiple

Exit EV is the exit multiple times exit-year EBITDA; exit equity is exit EV less net debt at exit. The base case exits at the entry multiple. Assuming expansion is aggressive and must be defended, not assumed: name the cause -- a re-rating the comparable set already shows, scale that moves the asset into a different buyer universe -- and quantify it separately, so the IC can strip it out and still see a deal.

### Step 4 -- Report IRR and MOIC, then bridge them

MOIC is exit equity over total equity invested; IRR is the annualised return over the hold. Report both: a strong MOIC on a seven-year hold can miss the hurdle, a fast flip can clear IRR on an immaterial gain. Bridge the gain into EBITDA growth at the constant entry multiple, multiple change on exit-year EBITDA, debt paydown equal to the cumulative sweep, and the fee drag at entry.

## Inputs

- QoE-adjusted LTM EBITDA and the entry multiple range from process terms
- Capital structure: tranches, quantum, rates, amortisation
- Five-year plan with capex, working capital and cash taxes
- Fee estimate, management rollover, fund hurdle and hold period

## Output format

1. Sources and uses, tied, with the equity plug shown
2. Entry: EV, multiple, turns of leverage, equity as % of EV
3. Cash sweep by year: cash available, sweep, closing debt
4. Exit: hold, multiple, exit EBITDA, net debt at exit
5. Returns: MOIC and IRR, both stated
6. Value-creation bridge: EBITDA, multiple, debt paydown, fees

Total length: 700-1,000 words, for an IC that re-adds the numbers.

## Example

**Worked base case (fictional -- Meridian Flow Controls, industrial valve aftermarket):**

Entry at 10.0x QoE EBITDA of $40.0M gives EV of $400.0M; with $14.0M of fees, uses are $414.0M, funded by $220.0M of debt (5.5x), $12.0M of rollover and $182.0M of sponsor equity -- tied. Equity at risk is $194.0M, 48.5% of EV. In year 1, EBITDA of $44.0M less cash interest of $22.0M (10.0% on $220.0M), capex of $8.0M, working capital of $1.0M and cash taxes of $2.0M leaves $11.0M swept; the sweep builds to $23.0M by year 5 as interest falls faster than taxes rise, so cumulative paydown is $85.0M and net debt at exit is $135.0M. Year-5 EBITDA of $62.0M at a flat 10.0x gives EV of $620.0M and exit equity of $485.0M -- 2.50x MOIC and 20.1% IRR over five years.

The bridge: entry equity value of $180.0M (EV less debt), plus $220.0M of EBITDA growth ($22.0M at 10.0x), plus nothing from multiple, plus $85.0M of debt paydown, equals $485.0M. Seventy-two per cent of the gain is EBITDA; the $14.0M of fees costs 0.19x of MOIC. Exiting at 11.0x would add $62.0M, 0.32x and 2.9 points of IRR, while the base case clears a 20% hurdle by a tenth of a point -- one assumed turn supplying almost all the comfort, from the variable the sponsor does not control.
