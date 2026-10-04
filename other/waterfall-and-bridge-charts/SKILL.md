---
name: waterfall-and-bridge-charts
description: Builds waterfall (bridge) charts that explain how a starting value became an ending value through a sequence of additions and subtractions.
---

# Waterfall and Bridge Charts

## When to use
Use this when the message is "how did we get from A to B." A waterfall, also called a bridge, decomposes a change into its drivers: opening value, a sequence of positive and negative moves, and the closing value. It is the standard chart for profit bridges, variance analysis, headcount changes, and price-volume-mix.

## What it does
It returns a fully specified waterfall: the bar sequence, which bars are totals versus deltas, the floating-bar construction, color rule for increases and decreases, connector lines, and labeling. It makes the drivers of a change legible at a glance.

## Method
Step 1. Define the start, the end, and the drivers.
List the opening value, each driver that moves it (with sign and size), and the closing value. The drivers must sum from opening to closing exactly. If they do not, there is a missing bridge item; surface it as an explicit "other" or "unexplained" bar rather than hiding the gap.

Step 2. Order the drivers deliberately.
Order tells a story. Common orders are largest driver first, or a logical sequence (volume, then price, then mix, then cost). Group all increases then all decreases only if that aids the narrative. Keep the order stable if you show the same bridge across periods.

Step 3. Construct the floating bars.
A waterfall is built from a stacked column chart where an invisible base bar lifts each delta to its correct floating height. The opening and closing bars rest on the zero baseline. Each delta bar floats: its base equals the running cumulative total before the move. Set the base series fill to no fill so only the delta bars show.

Step 4. Color by direction.
Use one color for increases, a second for decreases, and a third neutral color for the opening and closing total bars. Keep the increase and decrease colors consistent with the rest of the deck. The accent color is best reserved for the single most important driver or the closing value.

Step 5. Add connector lines.
Thin horizontal connectors link the top of one bar to the base of the next. They guide the eye along the cumulative path and make the bridge read as one flow rather than disconnected bars. Keep them light gray.

Step 6. Label every bar with its value and sign.
Show the value on each delta bar with an explicit plus or minus. Label the opening and closing totals clearly. The signed labels let the reader verify the arithmetic.

Step 7. Validate the math.
Confirm opening plus the signed deltas equals closing. A waterfall that does not reconcile is worse than no chart. State the reconciliation in one line.

Step 8. Build native in PowerPoint.
Insert a stacked column chart, structure the worksheet with a base series and a delta series (or separate increase and decrease columns), set the base fill to none, add connectors, and label. Everything stays editable.

## Inputs
- Opening value, closing value, and each driver with sign and magnitude.
- The intended order of drivers.
- The single driver or total to emphasize, if any.
- The deck's increase and decrease colors.

## Output format
- The ordered bar sequence (opening, deltas, closing).
- Which bars are totals versus floating deltas.
- The base-series construction note.
- Color rule for increases, decreases, totals, and the accent bar.
- Connector and label plan.
- The reconciliation check (opening plus deltas equals closing).

## Example
Input: operating profit bridge, opening 100, volume plus 18, price plus 9, cost minus 22, mix minus 5, closing 100.

Output:
- Sequence: Opening 100, Volume +18, Price +9, Cost -22, Mix -5, Closing 100.
- Totals: Opening and Closing rest on zero; the four drivers float.
- Base series: invisible base equals the running cumulative before each delta.
- Color: increases blue, decreases gray-blue, totals neutral; Cost in accent color as the largest decrease.
- Connectors: light gray lines linking each bar to the next.
- Reconciliation: 100 + 18 + 9 - 22 - 5 = 100, confirmed.
