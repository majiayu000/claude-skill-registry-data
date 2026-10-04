---
name: covenant-package-analysis
description: Rebuilds covenant EBITDA, maps the debt and restricted-payment baskets, and tests headroom under a downside case, when you need to know what a credit agreement actually permits.
---

# Covenant Package Analysis Agent

## When to use
Use this when the question is not what a borrower has done but what the documents let it do next. Typical triggers: sizing incremental debt for an acquisition, testing whether a dividend or sponsor recap fits the baskets, underwriting a credit whose leverage looks fine on the marketed number, or working out how far EBITDA can fall before a lender gets a seat at the table. Reach for it whenever a leverage ratio is quoted without saying whose definition of EBITDA it uses.

## What it does
It produces a covenant analysis: the credit perimeter, the maintenance and incurrence tests and when each is live, a rebuilt Consolidated EBITDA with every addback identified, capacity in each debt and restricted-payment basket, and a headroom schedule naming the first breach under a downside case.

## Method
1. Draw the perimeter. Know who is actually on the hook.
   - Identify the borrower, guarantors, restricted subsidiaries, and any unrestricted or excluded entities, and note what share of EBITDA sits outside the guarantee.
   - EBITDA at non-guarantors flatters every ratio while being structurally unavailable to the lenders testing it.

2. Classify the regime. Maintenance and incurrence are different animals.
   - Maintenance covenants test every quarter whatever the borrower does; incurrence covenants bite only on an action, the cov-lite norm for institutional term loans and bonds.
   - A springing revolver covenant tested only above a drawn threshold is the trap worth naming: it goes live in exactly the stress that causes the breach.

3. Rebuild Consolidated EBITDA from the definitions. Do not take the marketing number.
   - Work the addbacks line by line: restructuring, stock compensation, non-recurring items, pro forma effect of acquisitions, and run-rate cost synergies.
   - The tells are an uncapped synergy addback, a long realization window, and no requirement that the actions be identified; an aggregate cap as a percentage of EBITDA is the only real discipline.

4. Rebuild the debt definition. Establish which ratio the covenant runs on.
   - Confirm whether the test is first-lien, secured or total, gross or net, whether cash netting is capped, and whether letters of credit and receivables facilities count.

5. Map the debt baskets. Add them, because they stack.
   - Free-and-clear incremental capacity, ratio incremental, general debt baskets, and the non-guarantor cap; note MFN pricing protection and whether it sunsets.
   - Grower baskets set at the greater of a fixed amount and a percentage of EBITDA ratchet on the same inflated EBITDA the addbacks produced, so one aggressive definition buys capacity twice.

6. Map restricted payments and permitted investments. This is where value leaves.
   - Size the builder or available-amount basket and its starter, the general restricted-payment basket, and the ratio prong unlocking unlimited payments below a leverage level.
   - Check for a J.Crew blocker on moving material intellectual property to unrestricted subsidiaries, and read the investment baskets for the drop-down and uptier routes recent restructurings made routine.

7. Run the downside case. Headroom is a forecast, not a fact.
   - Rebuild the ratio quarter by quarter on stressed EBITDA, with any addback resting on an unrealized plan removed, and name the first breach quarter and the EBITDA decline causing it.

8. Test the cure. Know what the borrower can do about it.
   - Read the equity cure: how many over what period, whether proceeds count as EBITDA or must repay debt, and whether the amount is capped at the shortfall.

## Inputs
- The credit agreement and any indentures, with definitions and negative covenants
- Reported financials and management's adjusted EBITDA with its addback bridge
- Debt schedule by tranche, with cash balances and revolver utilization
- The downside case to run, or the stress parameters to build one
- Any pending action to test: an acquisition, dividend, recap, or asset sale
- Prior compliance certificates, showing how the borrower computes the ratio

## Output format
- The credit perimeter, with the share of EBITDA sitting at non-guarantors
- A bridge from reported EBITDA to Consolidated EBITDA, each addback named and sized
- The covenant regime: each test, its level, its trigger, and its testing date
- Basket capacity item by item, with grower baskets stated on both prongs
- A headroom schedule by quarter under base and downside, naming the first breach
- The cure analysis and what remains available after it is used
- Present all schedules in prose, never as markdown tables

## Example
For Dunmore Packaging (fictional, illustrative): reported LTM EBITDA of 180 becomes Consolidated EBITDA of 225 after 14 of restructuring, 22 of run-rate synergies, 6 of stock compensation, and 3 of legal costs, an aggregate 45 sitting at 20 percent of the adjusted figure, inside the 25 percent cap. Against first-lien debt of 1,150 and second-lien of 250, with cash netting capped at 50, first-lien net leverage reads 4.89x on the covenant number and 6.11x on reported EBITDA: the addbacks are worth 1.2 turns. The 6.50x maintenance test springs only above 35 percent utilization of the 100 revolver, so headroom on the marketed number looks like a 25 percent EBITDA decline. In the downside, EBITDA falls to 153 and the synergy addback rolls off unearned, leaving 176; drawing 50 on the revolver both springs the test and lifts first-lien net debt to 1,150, giving 6.53x against 6.50x. The breach is 0.9 of EBITDA wide and one equity cure closes it, which is the point for a committee: the covenant does not stop the damage, it only dates it.
