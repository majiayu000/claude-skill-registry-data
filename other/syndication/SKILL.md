---
name: syndication
description: Builds a plan to spread a financing across multiple providers, defining roles, allocations, underwriting basis, and flex. Use when a financing is too large or risky for one provider.
---

# Syndication Agent

## When to use
Use this agent when a financing is too large or too risky for a single provider to hold and it must be spread across several. The trigger is a deal where the lead cannot or will not retain the full amount and you need a plan for who leads, who participates, and how the paper is allocated and de-risked.

## What it does
It produces a syndication plan with roles and allocations: the lead and participant structure, allocation sizing, the underwriting basis, flex terms, and the timeline to close.

## Method
This agent runs a structured syndication strategy.

1. Define the syndication need. State the total facility size, the lead's target final hold, and the amount that must be placed with others.
   - Establish the driver: sheer size, single-name risk concentration, or a desire to diversify relationships.

2. Set roles. Designate the lead or arranger, any co-leads, and the participant tier.
   - Define responsibilities: the lead runs the process, sets terms, and holds the pen; participants take allocation on those terms with limited input.
   - Decide title economics up front; co-leads expect a larger fee share and league-table credit in exchange for a bigger commitment.

3. Choose the underwriting basis. Decide between a firm underwrite, where the lead commits the full amount and then sells down, and a best-efforts basis, where the lead commits only its own hold and markets the rest.
   - Trade-off: a firm underwrite earns a higher fee and gives the borrower certainty but leaves the lead holding unsold paper if the market softens; best-efforts is lower risk and lower fee.

4. Size allocations. Build the allocation stack: lead final hold, co-lead holds, and participant tickets.
   - Ensure the stack sums to the facility, no single participant creates undue concentration, and there is room to scale back if the book is oversubscribed.

5. Set flex terms. For an underwrite, define pricing flex, structure flex, and any market-flex provisions that let the lead adjust terms to clear the market.
   - State the flex caps explicitly; uncapped flex transfers all market risk to the borrower and is rarely accepted.

6. Build the timeline. Sequence launch, the commitment or syndication period, allocation and scaling, and close and funding.
   - Identify go/no-go checkpoints, typically at the end of the commitment period when the book is assessed.

7. Plan risk management. Address the sell-down plan, a market backstop if demand is soft, and contingency if the book is undersubscribed.
   - What good looks like: the lead knows its worst-case hold and has priced the flex to reach clearing terms without breaching it.

8. Summarize. Present the plan with roles, allocations, basis, flex, and timeline in one view.

## Inputs
- Total facility size and instrument type
- The lead's target final hold and maximum acceptable hold
- Underwriting appetite (firm versus best-efforts)
- Candidate participants and their likely appetite
- Timeline constraints and the funding date
- Market conditions and recent comparable syndications
- The borrower's tolerance for pricing and structure flex

## Output format
Claude returns:
- A statement of the underwriting basis and the rationale for it.
- The role structure naming the lead, any co-leads, and the participant tier with responsibilities.
- The allocation stack described as a list of holders with their ticket sizes summing to the facility (in prose, not a table).
- The flex terms with their caps.
- The timeline with its go/no-go checkpoints.
- The risk-management and contingency plan, including the lead's worst-case hold.

## Example
Northwind Logistics is raising a 500 million dollar term loan, and a bulge-bracket bank leads on a firm underwrite basis targeting a 150 million dollar final hold. The allocation stack places the lead at a 150 million dollar final hold, two co-leads at 100 million dollars each, and four participants at 37.5 million dollars each, which sums to the full 500 million dollars. Flex is set at up to 50 basis points of pricing and one leverage-covenant notch, both capped, so the lead can reach clearing terms without unlimited exposure. The timeline runs launch in week 1, a commitment period through week 3, allocation and scaling in week 4, and close and funding in week 5, with a go/no-go checkpoint at the end of the commitment period; if the book is soft, the contingency is for the lead to retain up to 225 million dollars and re-price within the flex.
