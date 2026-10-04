---
name: ib-buyer-list
version: 1.0.0
description: Build and prioritize the acquirer universe for a sell-side M&A process — strategic and financial buyers scored on strategic fit, ability to pay, and likelihood to transact.
author: matrixx0070
tags: [investment-banking, m&a, sell-side, buyer-list, deal-origination]
capabilities: []
---

## When to use
Use this when you are preparing a sell-side outreach and need a defensible, prioritized list of who to approach. The buyer list drives the whole process: too narrow and you leave value on the table, too wide and you leak confidentiality and burn team capacity. You segment strategics from financial sponsors, assess fit and ability to pay, and tier them so the client can approve who gets contacted.

**Not for:** the material you send buyers (use ib-teaser / ib-cim-builder), the bid instructions (use ib-process-letter), or the model that tests what a specific buyer can pay (use ib-merger-model). Do not contact anyone before the client approves the list.

## Method
1. Define the ideal-acquirer thesis with the deal team: what does this asset let a buyer do that they could not do alone (adjacency, geography, capability, scale)?
2. Build the strategic universe — competitors, adjacent players, up/downstream integrators, and companies that have stated the target's space as a priority.
3. Build the financial universe — private-equity sponsors with a relevant thesis, portfolio company add-on fits, and family offices; note dry powder and fund vintage.
4. Score each name on three axes: strategic fit, ability to pay (balance sheet / fund size / financing), and likelihood to transact (mandate, deal history, current appetite).
   **Decision point:** flag any competitor whose diligence access poses a strategic risk if the deal fails — client may want them excluded or staged to a later round.
5. Tier the list: Tier 1 (approach first, highest conviction), Tier 2 (approach in first round), Tier 3 (reserve / hold).
6. Note relationship coverage — who at the firm owns each relationship — and any conflicts to clear.
7. Present the list to the client for approval; the approved list, not the banker, decides who is contacted.

## Example
> Sell-side of a mid-market industrial-automation firm. Strategic universe: three larger automation OEMs and two adjacent robotics players (high fit, strong balance sheets). Financial universe: four sponsors with existing automation platforms for an add-on, plus two generalist funds with dry powder. Scored fit/ability/likelihood 1-5. A direct competitor scored high on fit but was staged to round two over diligence-leak risk. Client approved 18 names across three tiers before any outreach.

## Pitfalls
- Padding the list with low-fit names, which dilutes focus and multiplies confidentiality exposure.
- Giving a strategic competitor deep diligence access early when a failed deal would hand them your client's playbook.
- Scoring "ability to pay" on size alone — a large buyer with no financing appetite or an integration backlog is not a real bidder.
- Contacting names before the client signs off on the list.

## Output format
```
BUYER LIST — PROJECT <codename> (for client approval)

STRATEGIC BUYERS
# | Buyer | Fit(1-5) | Ability(1-5) | Likelihood(1-5) | Tier | Rationale | Relationship | Notes/conflicts
1 | ...   | ...      | ...          | ...             | 1    | ...       | ...          | ...

FINANCIAL BUYERS (sponsors / family offices)
# | Buyer | Fit | Ability (fund/dry powder) | Likelihood | Tier | Platform fit | Relationship | Notes
1 | ...   | ... | ...                        | ...        | 1    | add-on to X  | ...          | ...

TIER SUMMARY:  T1 (approach first): <n>   T2 (round 1): <n>   T3 (reserve): <n>
EXCLUSIONS / STAGED: <name — reason (e.g., competitor diligence risk)>
Client approval: [ ] approved  [ ] revise   Date: <>
```

## Reference
- Two buyer classes: strategics (synergies, can often pay more, but slower and riskier on diligence leakage) and financial sponsors (return-driven, disciplined on price, faster process, add-on fit matters).
- Three-axis screen: strategic fit, ability to pay (balance sheet / fund size / financing certainty), likelihood to transact (mandate, deal cadence, current appetite).
- Broad ("blast") vs. targeted process is a client decision balancing price maximization against confidentiality and disruption; the tiered list supports either.
- The client approves the outreach list; competitors are frequently staged to later rounds to limit competitively sensitive diligence access.
