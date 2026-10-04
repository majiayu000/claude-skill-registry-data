---
name: merger-analysis
description: Tests whether a proposed combination creates value by running accretion and dilution analysis on pro-forma EPS.
---

# Merger Analysis Agent

## When to use
Use this when a client or deal team is weighing an acquisition and needs to know whether the combination lifts or hurts earnings per share. It is the first quantitative screen before a board discussion or a pitch. Reach for it whenever someone asks "is this deal accretive or dilutive" or wants to test a price, mix, or synergy assumption.

## What it does
It produces an accretion and dilution read with pro-forma effects: standalone versus combined EPS, the accretion or dilution percentage in year one, the breakeven premium, and the synergy level required to make the deal neutral.

## Method
Accretion and dilution analysis, worked step by step.

1. Collect standalone figures for acquirer and target: net income, diluted shares, and current EPS. Confirm the tax rate and the target purchase price.
   - Purchase price is offer per share times fully diluted shares (include options via the treasury method), plus the assumed control premium over the unaffected price.
   - Pitfall: use forward net income where available, since deals are marketed on next-twelve-months earnings, not trailing.

2. Set the consideration mix: percent cash, percent new debt, and percent stock.
   - Cash and debt carry a financing cost; stock creates new shares at the acquirer's exchange ratio.
   - Good practice: check the mix against leverage capacity so pro-forma net debt to EBITDA stays inside covenant.

3. Layer financing effects.
   - For debt and cash used, subtract after-tax incremental interest (rate times amount, times one minus tax rate). Foregone interest on cash spent is treated the same way.
   - Use the marginal borrowing rate, not the blended historical rate, or the drag will be understated.

4. Layer synergies.
   - Add expected pre-tax cost synergies, apply the tax rate, to get the after-tax synergy contribution; phase them in if they ramp over years one to three.
   - Net out one-time costs to achieve synergies (severance, systems) in the year they hit.

5. Compute new share count.
   - For the stock portion, divide stock consideration by the acquirer share price to get newly issued shares; add to existing diluted shares.
   - Sanity-check the implied exchange ratio against the target's own share price.

6. Build pro-forma net income.
   - Acquirer net income plus target net income, plus after-tax synergies, minus after-tax financing costs, adjusted for incremental deal amortization of intangibles.
   - Keep a clean bridge so each adjustment is visible and defensible to a board.

7. Compute pro-forma EPS and compare to standalone.
   - Pro-forma net income divided by combined shares gives pro-forma EPS; the difference over standalone EPS is the accretion or dilution percent.

8. Solve for breakeven.
   - Hold the deal neutral and back out the maximum premium payable, or the minimum synergies needed, so pro-forma EPS equals standalone EPS.
   - The synergy-to-neutral figure is often the most persuasive number in a board discussion.

9. Sensitize the result.
   - Flex premium, synergy level, and mix so the team sees exactly where the deal flips from accretive to dilutive.

## Inputs
- Acquirer and target net income (forward where available) and diluted share counts
- Acquirer and target share prices and the offer price per share
- Assumed control premium over the unaffected price
- Consideration mix (cash, debt, stock) and the marginal financing rate
- Expected cost and revenue synergies with phasing and cost to achieve
- Blended and marginal tax rates
- Any incremental deal amortization of acquired intangibles

## Output format
- A one-line verdict: accretive or dilutive and by how much in year one
- A sources-and-uses summary in prose (what funds the deal and where it goes)
- A pro-forma bridge in prose from combined net income to pro-forma EPS, adjustment by adjustment
- The accretion or dilution percentage against standalone EPS
- The breakeven premium and the synergy-to-neutral figure
- A two-variable sensitivity described in prose (premium versus synergies), never a literal table

## Example
Northwind Logistics (acquirer) earns 200 million on 100 million shares, so EPS is 2.00. It acquires Coastal Freight, which earns 40 million, in an all-stock deal priced at 600 million. At Northwind's 30 share price that issues 20 million new shares, lifting the total to 120 million. Combined net income of 240 million, plus 15 million after-tax synergies, gives 255 million, so pro-forma EPS is 2.13, roughly 6.4 percent accretive. Breakeven analysis shows Northwind could raise the offer to about 700 million before the deal turns dilutive at the current synergy level, and the deal stays accretive even if synergies come in a third light.
