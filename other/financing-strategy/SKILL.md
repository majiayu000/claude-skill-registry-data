---
name: financing-strategy
description: Builds a financing plan across sources, sizing, and sequence for a deal, use it when a transaction needs a plan for how it gets funded.
---

# Financing Strategy Agent

## When to use
Use this when a transaction needs a concrete plan for how it gets funded, such as an acquisition, a leveraged buyout, a growth raise, or a recapitalization. The question is not just how much money is needed but which sources supply it, in what tranches, at what cost, and in what order. This agent lays that out end to end.

## What it does
It produces a financing plan across sources, sizing, and sequence: a sources-and-uses view, the debt and equity mix with tranching, the cost and covenant profile of each layer, and the sequence in which the financing is arranged and drawn.

## Method
1. Size the need with a sources-and-uses view.
   - Uses: purchase price or enterprise value, refinanced existing debt, transaction fees, and minimum cash.
   - Sources must equal uses exactly; an unbalanced sheet is the first thing a lender rejects.

2. Set the target leverage.
   - Anchor total debt to EBITDA on cash flow stability, sector norms, and lender appetite.
   - This split decides how much debt versus equity the structure requires.

3. Lay out the debt tranches from senior to junior.
   - Revolver for liquidity, senior secured term debt, then any second-lien, unitranche, subordinated, or mezzanine layer.
   - Size each and note its position in the priority stack, since junior capital prices off the cushion below it.

4. Size the equity.
   - The sponsor or acquirer equity check plugs the gap between debt raised and total uses, plus any rollover or co-investment.
   - Good looks like: an equity contribution that clears typical lender minimums, often around a third of the structure.

5. Price each layer.
   - Give expected margin or coupon per tranche, upfront fees, and any payment-in-kind or warrant features on junior capital.
   - Roll up a blended cost of the financing so the total burden is visible.

6. Set the covenant and terms profile.
   - Note maintenance versus incurrence covenants, leverage and coverage tests, call protection, and amortization per tranche.
   - Flag where headroom is tight, since a covenant that trips in year one kills the plan.

7. Test the structure against downside.
   - Stress EBITDA and confirm covenants hold and debt stays serviceable.
   - Common pitfall: a structure that only works in the base case.

8. Define the sequence.
   - Order the commitments: equity certainty first, then the lead debt commitment, then syndication, with a timeline to close and a drawdown schedule.

9. Flag the key risks and alternatives.
   - Call out market windows, rate sensitivity, and a fallback if a tranche prices wide or a lender pulls back.

## Inputs
- The transaction size and uses: purchase price, debt to refinance, fees, minimum cash
- EBITDA and cash flow, plus capex and working capital needs
- Target or maximum leverage and any lender indications
- Available equity: sponsor check, rollover, co-investors
- The current rate environment and pricing indications per layer
- Existing debt terms and any change-of-control or prepayment triggers
- The required timeline to close

## Output format
- Sources and uses: both sides listed and summed to an equal total.
- Structure: each debt tranche with size, pricing, and covenants in priority order, then the equity check, then the blended cost.
- Downside test: the stress applied and whether covenants and serviceability hold.
- Sequence and timeline: the order of commitments, the drawdown schedule, and the key risks with a fallback.
- Describe the sources-and-uses and tranche detail as structured text, never a rendered markdown table.

## Example
Northwind Logistics buyout. Uses: enterprise value 500m, refinance existing debt 60m, fees 20m, minimum cash 10m, total 590m. Sources: revolver undrawn at close (40m committed), senior term loan 300m at a margin around 4.5% with a leverage maintenance covenant, subordinated notes 90m at roughly 9% with incurrence-based terms, and sponsor equity of 200m, total 590m. Opening leverage 5.4x on EBITDA of 72m, equity at 34% of the structure, and blended debt cost roughly 5.5%. Downside test: a 15% EBITDA decline keeps coverage above 1.5x and the leverage covenant intact. Sequence: equity commitment first, senior commitment letter next, subordinated notes placed pre-close, then draw at completion with the revolver reserved for working capital. Key risk: if the notes price wide, the fallback is to upsize the term loan and trim the check modestly.
