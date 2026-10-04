---
name: ib-pitch-deck
version: 1.0.0
description: Populate an investment-banking pitch template from source data — situation, market, valuation, buyer landscape, and process recommendation — to win or advise on a mandate.
author: matrixx0070
tags: [investment-banking, pitchbook, mandate, valuation, deal-marketing]
capabilities: []
---

## When to use
Use this when you have the underlying analysis and need to assemble it into a coherent pitchbook — the deck a bank presents to win a mandate or advise a client on a transaction. The pitch tells a story: here is your situation, here is what the market and comparable deals say you are worth, here are the buyers, and here is how we would run the process and why we should run it.

**Not for:** the disclosed sell-side book to buyers (use ib-cim-builder), individual company one-pagers (use ib-strip-profile), or the accretion model (use ib-merger-model). This assembles the argument to a client, not the marketing to buyers.

## Method
1. Nail the objective and audience: is this a sell-side mandate pitch, a buy-side advisory pitch, or a strategic-options review? The recommendation section changes accordingly.
2. Open with the situation and the "why us / why now": your read of the client's position and the market window.
3. Build the market and industry section: size, growth, trends, and recent transaction activity that frames the opportunity.
4. Present valuation using multiple methods — trading comparables, precedent transactions, and DCF — and triangulate to a defensible range shown as a football-field chart.
   **Decision point:** if the methods diverge widely, explain why (cycle, growth premium, control premium in precedents vs. trading comps) rather than averaging them into a false midpoint.
5. Lay out the buyer landscape or strategic options: who would transact and why, tied to the buyer-list thesis.
6. Recommend the process: structure, timeline, and the value the bank adds — with credentials/tombstones that prove relevant experience.
7. Ensure every number ties to its source analysis; assemble on the firm template and review before the client meeting.

## Example
> Sell-side mandate pitch to a founder considering an exit. Deck opened with the founder's situation and a favorable M&A window in the sector, then a market section citing three recent comparable deals. Valuation triangulated trading comps (8-10x EBITDA), precedents (10-12x, control premium), and a DCF, presented as a football field with an $180-220M range. Buyer landscape leaned on a tiered acquirer thesis. Process recommendation proposed a targeted two-round auction over five months, backed by three relevant tombstones. Every multiple tied to the comps workbook.

## Pitfalls
- A "kitchen-sink" deck with no narrative thread — a pitch is an argument, not a data dump.
- Averaging divergent valuation methods into a single number instead of explaining the spread and showing a range.
- Valuation figures that do not tie to the underlying comps/DCF workbooks.
- Overpromising a valuation to win the mandate that the market cannot deliver, setting up a disappointed client later.

## Output format
```
PITCHBOOK — <Client> — <Sell-side / Buy-side / Strategic options> — <date>

1. EXECUTIVE SUMMARY        <situation + recommendation in brief>
2. SITUATION & WHY NOW      <client position, market window, why us>
3. MARKET & INDUSTRY        <size, growth, trends, recent deal activity>
4. VALUATION                Trading comps: <x-x EBITDA>
                            Precedent transactions: <x-x EBITDA>
                            DCF: <range>
                            -> FOOTBALL FIELD: implied range <low>-<high>
5. BUYER LANDSCAPE / OPTIONS  <tiered acquirers or strategic alternatives>
6. PROCESS RECOMMENDATION    <structure, timeline, milestones, our value-add>
7. CREDENTIALS / TOMBSTONES  <relevant prior mandates>
APPENDIX                     <detailed comps, DCF, assumptions>

All figures tie to: <comps workbook / DCF model>
```

## Reference
- The three core valuation methods triangulated in a pitch: comparable companies (trading multiples), precedent transactions (deal multiples, which embed a control premium), and discounted cash flow (intrinsic value); results are shown as a "football field" range, not a single point.
- Precedent-transaction multiples typically exceed trading comps because acquirers pay a control premium; DCF depends heavily on WACC and terminal assumptions — divergence is explained, not averaged away.
- A pitchbook is a persuasive narrative: situation -> market -> value -> buyers/options -> process -> credentials; each section builds toward the recommendation and the "why us."
- Winning a mandate on an inflated valuation is a short-term win and a long-term liability; the credible range that survives the process is the right one to present.
