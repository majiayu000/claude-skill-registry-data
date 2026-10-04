---
name: sensitivity-analysis
description: Builds two-variable data tables around a base case to show which drivers move value the most, expressed as swing in value, IRR, or EPS.
---

# Sensitivity Analysis Agent

## When to use
Use this agent when you need to see what moves value the most: after a base-case model is built and you want to know which assumptions to defend hardest, or before a committee that will ask how robust the number is. Unlike scenario analysis, this isolates variables one or two at a time rather than telling coherent stories. Reach for it once the base case is stable enough to flex.

## What it does
Produces sensitivity ranges across the key value drivers, typically as a two-variable data table around the base case, showing the swing in the output metric and identifying the highest-leverage driver.

## Method
1. Fix the base case and the single output metric that matters.
   - Common metrics are enterprise value, IRR, MOIC, or accretion/dilution EPS.
   - Lock the base case first so every flex is measured against one clean reference point.

2. List the candidate drivers and rank them by expected leverage.
   - Typical candidates: growth rate, margin, exit multiple, entry multiple, WACC or discount rate, leverage, and financing cost.
   - Rank by how much each plausibly moves the output, not just how uncertain it is.

3. Pick the two most material drivers for the primary two-variable data table.
   - Everything else can be shown as one-way sensitivities.
   - Pitfall: pairing two drivers that are really the same bet, which wastes a dimension.

4. Set a sensible step range around the base for each.
   - For example plus or minus fifty and one hundred basis points, or half a turn and a full turn of multiple.
   - Keep steps symmetric so the swing is easy to read.

5. Build the two-variable data table.
   - One driver across the columns, the other down the rows, with the output metric at each intersection and the base case in the center cell.

6. Read the swing.
   - Compare the corners and the center to see how far the metric moves for a given move in each driver.
   - The wider the spread along an axis, the more that driver matters.

7. Identify the highest-leverage driver and any threshold.
   - Name the driver whose range produces the widest swing, and flag where the deal stops clearing its hurdle.

8. Add one-way sensitivities for secondary drivers.
   - Summarize which assumptions the recommendation is most exposed to and which barely move the answer.

## Inputs
- The base-case model or its key outputs and assumptions
- The output metric to sensitize (enterprise value, IRR, MOIC, EPS)
- The candidate drivers and a reasonable range for each
- The step size to flex each driver by
- Any hurdle rate or threshold the output must clear
- Any drivers that are contractually fixed and should not be flexed

## Output format
Claude returns:
- The base-case output value as the reference point.
- A prose description of the two-variable data table: which driver is on each axis, the range and step of each, and the output value at the base case, at the corners, and at any threshold crossing.
- A swing read: the change in the output across each driver's range, and the named highest-leverage driver.
- One-way sensitivities for the secondary drivers, ranked by materiality.
The data table is described in words, never rendered as a markdown table.

## Example
For a sponsor's LBO of Northwind Logistics, the base case gives a five-year IRR of twenty-two percent. The two-variable data table sensitizes exit EV/EBITDA multiple across the columns, from 7.0x to 9.0x in half-turn steps, and revenue CAGR down the rows, from four percent to eight percent in one-point steps, with the base case at 8.0x and six percent in the center. IRR ranges from about fourteen percent in the bottom-left corner (7.0x exit, four percent growth) to about thirty percent in the top-right (9.0x exit, eight percent growth). The exit multiple is the highest-leverage driver: a full turn moves IRR by roughly six points, versus about four points for two points of CAGR. IRR drops below the twenty percent hurdle once the exit multiple falls under 7.5x at base-case growth, which is the number to defend hardest in committee. One-way sensitivities show entry leverage and financing cost as the next most material drivers, while working-capital timing barely moves the return.
