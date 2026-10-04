---
name: carve-out-analysis
description: Builds standalone carve-out EBITDA and the separation economics for a business being sold out of a parent, for use when you must value a divestiture rather than a whole company.
---

# Carve-Out Analysis Agent

## When to use
Use this when what is being sold is a division, a segment, or a set of assets inside a larger group rather than a company that already stands alone. Typical triggers: a corporate divestiture, a sponsor bidding for a non-core unit, or a management buyout of a division. Reach for it the moment someone quotes segment EBITDA as if it were the target's earnings.

## What it does
It produces carve-out economics: a bridge from reported segment EBITDA to defensible standalone EBITDA, a bottom-up cost build, the transitional service and separation costs, the stranded cost left at the parent, and a valuation that carries the separation burden.

## Method
1. Define the perimeter first. Say exactly what is being sold.
   - List the entities, contracts, customers, people, IP, systems, and sites in scope, and name every shared asset that must be split, licensed, or duplicated.
   - A perimeter that moves later invalidates every number below it. Lock it first.

2. Reverse the parent's allocations. Add back the charge, then forget it.
   - Segment reporting is an allocation exercise built for group management, not a standalone P&L; add back the management charge and any cost allocated on a revenue or headcount key to reach true contribution. An allocation is not the cost of a function, and confusing the two is the most common carve-out error.

3. Build standalone costs bottom up. Cost the organization, do not scale the allocation.
   - Price the finance, HR, IT, legal, procurement, insurance, and audit functions the business needs on day one, at market rates and real headcount.
   - Expect a permanent dis-synergy: a smaller unit loses the group's scale in procurement, insurance, and licensing, and that gap never closes.

4. Normalise the intercompany relationships. Both directions.
   - Restate transfer-priced purchases and sales onto market terms, and strip revenue from sister divisions that will not continue, together with the margin it carries.

5. Price the TSA and the separation. One-time and run-rate are different money.
   - Set scope, duration, price per service, and exit rights; a TSA priced at the parent's cost still runs above insourced cost, so model the drag.
   - Add one-time separation capex: ERP stand-up, data migration, rebranding, site separation, legal reorganization.

6. Quantify stranded cost at the parent. The seller's problem, the buyer's leverage.
   - Stranded cost is the group cost the division carried that does not leave with it; name it, because it drives the parent's post-deal dilution and its flexibility on price.

7. Value the standalone business, then charge it for separation.
   - Apply the multiple to carve-out EBITDA, never to segment EBITDA, then deduct one-time separation cost and the TSA drag for net value.

## Inputs
- Divisional P&L for three years as reported, and the parent's allocation methodology
- Organization chart and headcount, split into dedicated and shared
- Intercompany volumes, transfer prices, and shared contracts
- Systems landscape, separability, and the draft TSA scope, pricing, and duration

## Output format
- The perimeter item by item, with shared assets flagged
- A bridge from segment EBITDA to carve-out EBITDA, each step named and quantified
- The standalone cost build by function, and TSA cost by service and term, with run-rate drag separated from one-time cost
- The stranded cost left at the parent, and a valuation on carve-out EBITDA net of separation cost
- Present all schedules in prose, never as markdown tables

## Example
For the Coatings division of Northvale Industrial (fictional, illustrative), the parent reports segment EBITDA of 60 on revenue of 400. Adding back the 10 corporate charge gives contribution of 70; a bottom-up build of finance, HR, IT, legal, and audit costs 16, taking it to 54; restating resin bought from a sister plant onto market terms costs 3; and 20 of revenue sold to another division stops, removing 4 of margin. Carve-out EBITDA is 47, some 22 percent below the reported 60, so at 8.0x the business is worth 376 rather than 480. An eighteen-month TSA at 9 a year against a 7 insourced run-rate adds 2 a year of drag, or 3 over the term, and separation capex is 12, so net value is about 361. Of the 10 the parent charged, only 4 leaves with the division: 6 is stranded at Northvale, which is why the seller will argue the buyer should carry the separation cost.
