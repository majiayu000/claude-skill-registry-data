---
name: market-intelligence
description: Produces a live market intelligence brief on sector deal drivers and capital flows, for when you need a fast read before a pitch, call, or screen.
---

# Market Intelligence Agent

## When to use
Reach for this agent when you need a live read on deal drivers and capital flows in a sector and cannot wait days for a formal research package. Typical triggers are prepping for a client call, framing a pitch, or sizing whether a sector is heating up or cooling off. It is built for the moment when a banker asks "what is actually moving in this space right now?"

## What it does
It returns a market intelligence brief that names the current catalysts, traces where capital is flowing, and spells out the implications for deal activity and for a specific client or target. The output is decision-grade context, not a data dump.

## Method
The agent runs a structured market and deal-driver scan:

1. Fix the scope: define the sector, the sub-segments in play, the geography, and the time window (typically trailing 6 to 12 months plus a forward look).
   - Name the specific value-chain stage so upstream and downstream signals are not blurred together.
   - Pitfall: a scope drawn too wide averages away the very signal you are hunting for.

2. Map the supply of capital: strategic acquirers with balance-sheet capacity, financial sponsors raising or deploying dry powder, and public-market appetite via recent equity and debt issuance.
   - Note fund closes, recapitalizations, and authorized buybacks, since these signal deployment intent.

3. Map the demand for capital: which companies are seeking growth funding, refinancing walls of maturing debt, or under pressure to divest non-core units.
   - Flag near-term maturity walls and covenant pressure, which often force a transaction on the seller's timetable.

4. Catalog the catalysts: regulatory shifts, technology disruption, input-cost swings, consolidation waves, and rate or credit conditions that change the cost of doing deals.
   - Separate structural catalysts (durable) from cyclical ones (transient), since they carry different weight in a thesis.

5. Read the deal tape: recent M&A, financings, and restructurings in the sector, extracting the multiples paid, the rationale cited, and who was active on each side.
   - Good looks like a handful of genuinely comparable transactions with EV/EBITDA context, not a long undifferentiated list.

6. Score momentum: judge whether activity is accelerating or decelerating, and whether valuations are expanding or compressing versus the prior period.
   - Compare deal count and average multiple against the trailing comparable window rather than an absolute level.

7. Draw implications: translate the scan into what it means for deal flow, for likely buyer and seller behavior, and for the named client or target.
   - Tie each implication back to a specific catalyst or capital-flow observation so the logic is traceable.

8. Flag the watch list: identify the two to four signals that would confirm or reverse the read, so the client knows what to monitor.
   - Make each signal observable and time-bound, not a vague "watch the market."

## Inputs
- The sector or sub-segment to scan, and the geography of interest.
- The time window to cover, and whether a forward look is wanted.
- Any specific client, target, or peer the brief should orient around.
- The decision the brief will feed (pitch, screen, call prep, board update).
- Known recent deals, financings, or house views to fold in.
- Any constraints, such as firm-name restrictions or a required length.

## Output format
Claude returns a brief with these named sections:
- Read: a two-line headline verdict with the single most important takeaway.
- Capital Flows: who is deploying capital and who is raising it, on both the strategic and sponsor sides.
- Catalysts: a ranked list of the forces moving the sector, each with a one-line reason.
- Recent Deal Signal: a short prose rundown of comparable transactions with the multiples and rationale, written in sentences rather than a grid.
- Implications: what the scan means for the named client or target.
- Watch List: the confirming or reversing signals to monitor.
- Confidence Note: an explicit confidence level and any gaps where data was thin.

## Example
Scope: mid-market cold-chain logistics, North America, trailing 12 months plus forward look. Read: consolidation is accelerating as sponsors chase pharma-driven demand for temperature-controlled capacity, and windows for sub-scale operators to sell are opening. Capital Flows: two large sponsors are actively rolling up regional operators, while public carriers issue debt to fund fleet expansion. Catalysts, ranked: pharma volume growth, tightening emissions rules raising the cost of older fleets, and elevated financing costs squeezing sub-scale players. Recent Deal Signal: a regional operator similar to fictional Northwind Cold Chain changed hands at roughly a high-single-digit EV/EBITDA multiple, with the buyer citing route density as the rationale. Implication for Northwind: it is a credible roll-up target now, and a sale process would likely draw competitive sponsor interest at a premium to the last comparable. Watch List: any new platform entrant, a shift in pharma outsourcing patterns, and any move in credit spreads that would raise financing cost.
