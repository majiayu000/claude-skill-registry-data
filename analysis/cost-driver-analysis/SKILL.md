---
name: cost-driver-analysis
description: Decomposes cost changes into volume, rate, and mix effects to identify the true root cause of cost escalation or decline.
---

# Cost Driver Analysis

## When to use

Use this skill when total cost has moved materially and the team needs to distinguish between what was driven by volume (more units), rate (higher price per unit), and mix (a shift toward higher-cost products or channels). Without this decomposition, cost reduction actions are often aimed at the wrong lever.

## What it does

Produces a three-factor decomposition of cost change: volume effect, rate effect, and mix effect, with a plain-English explanation of which factor is dominant and what that implies for cost reduction strategy.

## Method

This skill applies a Price-Volume-Mix (PVM) variance analysis, which is standard practice in management consulting cost diagnostics.

**Step 1: Define the cost elements**
- Identify the cost pool being analyzed (e.g., total COGS, a specific sub-category, or a single line item such as packaging materials).
- Confirm the unit of measurement for volume (units produced, transactions, headcount, etc.).
- Confirm the rate basis (cost per unit, cost per transaction, cost per FTE, etc.).

**Step 2: Calculate volume effect**
- Volume effect = (current period volume - prior period volume) x prior period rate
- This isolates how much of the cost change is explained purely by doing more or less of the same activity at the same cost per unit.

**Step 3: Calculate rate effect**
- Rate effect = (current period rate - prior period rate) x prior period volume
- This isolates how much of the cost change comes from paying more (or less) per unit, holding volume constant at the prior period level.

**Step 4: Calculate mix effect**
- Mix effect = total cost change - volume effect - rate effect
- The mix effect captures the residual: the cost impact of a shift in the composition of activity (e.g., more premium-grade materials, a higher share of expensive SKUs, or a greater proportion of overtime hours).

**Step 5: Interpret and prioritize**
- Rank the three effects by absolute dollar value.
- For the dominant effect, identify the specific sub-driver: which product, channel, vendor, or cost center accounts for most of that effect.
- Map each effect to a potential intervention:
  - Volume effect: demand management, capacity optimization, or make-vs-buy review.
  - Rate effect: renegotiation, competitive sourcing, or contract discipline.
  - Mix effect: product/channel rationalization, specification review, or demand channel shift.

**Step 6: Sensitivity check**
- Run a simple sensitivity: if the dominant rate driver were reduced to prior-period levels, what would the annual saving be in dollars and as a percentage of total cost?
- State any assumptions explicitly (e.g., "this assumes no volume change and no mix shift").

## Inputs

- Current-period total cost, volume, and implied rate for the cost pool.
- Prior-period equivalents.
- If multiple cost elements (SKUs, categories) contribute, a breakdown by element for both periods.

## Output format

A structured analysis with:
1. Summary finding (one paragraph: which effect dominates and what it means)
2. PVM decomposition as a prose table (prior cost, current cost, volume effect $, rate effect $, mix effect $, total change $)
3. Sub-driver analysis for the dominant effect (top 3 sub-drivers by contribution)
4. Intervention map (bullet list: each effect, its implication, and the recommended next action)
5. Sensitivity statement (one sentence with the saving estimate and stated assumptions)

## Example

**User input:**
"Our direct material cost rose from $22M to $27M. Volume grew 8%. Average input price rose 12%. The rest is mix."

**Claude output (abbreviated):**
> **Summary**
> The $5M cost increase is driven primarily by rate (higher input prices), which accounts for $2.6M of the rise. Volume growth adds $1.8M and the shift toward higher-specification materials adds approximately $0.6M as a mix effect.
>
> **PVM decomposition**
> - Volume effect: $22M x 8% = +$1.76M
> - Rate effect: $22M x 12% = +$2.64M (dominates)
> - Mix effect: $5M - $1.76M - $2.64M = +$0.60M
>
> **Intervention map**
> - Rate effect ($2.6M): Run a competitive RFP for the top 3 input materials. Benchmark current rates against market index prices. Estimate: 8-15% rate reduction possible if contracts are out of cycle.
> - Volume effect ($1.8M): Review whether the volume growth is in plan; if demand is below forecast, identify over-purchasing and adjust safety stock parameters.
> - Mix effect ($0.6M): Review specification creep. Check whether upgraded materials are required or have been added without formal sign-off.
>
> **Sensitivity**
> If input prices were held to prior-year levels, annual direct material cost would be $24.4M rather than $27M, a saving of $2.6M (10% of current spend), assuming no change in volume or mix.
