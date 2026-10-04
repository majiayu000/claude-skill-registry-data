---
name: precedent-transactions
description: Builds a precedent deal set with paid multiples and control premia when you need what buyers have actually paid in past transactions.
---

# Precedent Transactions Agent

## When to use
Use this when you need what buyers actually paid in past deals rather than where public peers trade today. Typical triggers: setting an offer or defense range in an M&A process, or grounding a control-value view that trading comps miss. Reach for it when the relevant benchmark is the price a real acquirer paid, including the control premium.

## What it does
It produces a precedent deal set: comparable historical transactions with paid EV/EBITDA (and EV/revenue where relevant), computed control premia, adjusted for cycle and synergy, and applied to the subject to imply a value range.

## Method
1. Define the screen. Target deals that resemble the subject situation.
   - Screen for transactions involving similar targets by sector, size, geography, and deal type over a relevant lookback window, often 3 to 5 years to stay cycle-relevant.

2. Assemble deal facts. Capture what each multiple and premium needs.
   - For each deal record the announcement date, target and acquirer type (strategic or sponsor), deal value, target LTM EBITDA and revenue at announcement, and the consideration mix.

3. Compute paid multiples. Use metrics as of announcement.
   - Transaction EV equals offer equity value plus target net debt; compute EV/EBITDA and EV/revenue on the target's LTM figures at the time of the deal.
   - Pitfall: using today's EBITDA against a historical price inflates the multiple; always pair the price and the metric from the same date.

4. Compute control premia. Measure what control cost.
   - For public targets, compare the offer price per share to the unaffected price one day and one month prior to derive the premium paid.
   - Pick the unaffected date carefully: rumor-driven run-ups before announcement can understate the true premium if you anchor to the leaked price.

5. Adjust for context. Do not blend incomparable deals silently.
   - Flag deals struck at a cycle peak or trough, and separate strategic buyers (who may pay for synergies) from sponsors (who underwrite to a return), annotating rather than averaging across them blindly.

6. Establish the benchmark. Summarize the paid set.
   - Take the median and mean paid multiple and the median premium, noting the range and the strategic-versus-sponsor split.

7. Apply to the subject. Convert paid multiples into value.
   - Multiply the subject's LTM EBITDA by the low, median, and high paid multiples for an implied EV range, and sanity-check the implied premium against those observed.
   - Bridge the implied EV back to an offer price per share so the result is comparable to a live bid.

8. Interpret. Land where the subject belongs.
   - State where it should sit given deal type, likely synergies, and cycle position, and call out any precedent to down-weight and why.
   - Note the buyer universe: if only sponsors are realistic bidders, weight the sponsor deals more heavily than the strategic ones.

## Inputs
- Subject LTM EBITDA and revenue, and net debt
- A candidate list of precedent transactions, or permission to propose one
- The relevant lookback window for the screen
- Whether strategic, sponsor, or both buyer types are in scope
- Target unaffected trading prices, for premium work
- Any known synergy or cycle context to adjust for

## Output format
- A deal-set section describing each transaction, its paid EV/EBITDA, and the premium paid
- A benchmark section with the median and mean paid multiple and the median premium
- The strategic-versus-sponsor split and the observed premium range
- The implied value range from applying the low, median, and high multiples to the subject
- A short interpretation of where the subject belongs and which deals were down-weighted
- Present the deal set in prose, never as a markdown table

## Example
For Meridian Foods (fictional, illustrative): six deals over four years show paid EV/EBITDA of 9.0x to 11.5x, a median of 10.2x, with control premia of 22 to 38 percent, a median of 29 percent. Two strategic deals sit at the top on synergy value, while one sponsor deal at 9.0x anchors the low. Applied to the subject's LTM EBITDA of 120, the median 10.2x implies EV of about 1,225, with a band of 1,080 to 1,380. The implied premium over the subject's standalone comps value of about 1,010 is roughly 21 percent, at the low end of the observed range and reasonable for a non-synergistic buyer. A cycle-peak deal is down-weighted, placing the subject nearer 10.0x, or about 1,200.
