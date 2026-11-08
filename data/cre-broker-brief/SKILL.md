---
name: cre-broker-brief
description: Build a commercial-real-estate brief for an income property (apartments, retail centre, office, industrial) that a broker hands a seller or markets to buyers — NOI-over-cap valuation benchmarked to local caps, a cap-rate football field, county-record facts, levered return math (DSCR, cash-on-cash, value-add equity), a named buyer pool, and charts drawn only from real numbers. Use when a broker asks for a listing pitch or buyer-marketing brief on an income property, or when someone asks "what is this building worth and why".
compatibility: >-
  Network access to county assessor sites, grounded web search and Google Maps Platform with the user's own key.
metadata:
  network-hosts: "maps.googleapis.com generativelanguage.googleapis.com"
  network-purpose: "property facts, market research and property imagery"
---

# CRE broker brief (income property)

Value is `NOI ÷ cap rate`, not revenue × multiple, and there are usually no reviews worth
mining. Write for the **broker's** chair (win the listing, or market it to buyers), never as
advice to the owner. Pair with `flip-deal-feed` for the underwriting scripts and
`broker-prospecting-dossier` for the pre-listing cold approach.

## Read the request first: intent drives the deliverable

- "Help me win the listing" -> a valuation / why-now pitch to the seller.
- "Already signed, show buyer upside and comps" -> a buyer-marketing brief.
- A "revenue" figure on a CRE request is usually **NOI**. Compute `ask ÷ NOI` = going-in cap
  and lead with it.

There is no fixed template. The sections below are ingredients; the brief is the best answer to
what was asked.

## Data-gathering playbook (the repeatable value)

1. **County property records: the spine.** Most counties run a public assessor app: verified
   units, year built, class, land and building size, the county's income-approach value, owner
   entity and mailing address, and assessed-value history. Find the county's portal; recipes do
   not port between counties.
   - **Assessed-value history is a trade detector:** a 2-3x jump in one year usually means a
     sale and reassessment. A rename or "new management" dates it.
2. **Grounded web research** (`gemini-web-search` or equivalent) for what records lack:
   - the **last trade** (trade press, sold listings). Often paywalled; record it as a diligence
     lead, never print an unverified buyer name as fact.
   - the **buyer pool**: active local and regional investors in this asset class, named, sourced.
   - **peer asking rents** by unit type: the mark-to-market check.
   - **submarket cap rates, occupancy, rent growth, supply pipeline** from brokerage research.
3. **Imagery**: Street View and Static Maps (Google Maps Platform key). Check that the Street
   View frame actually shows the building.

### The walls: be honest, never fake

- **Non-disclosure states** (e.g. Kansas, Texas, Utah and others) do not publish sale prices.
  Use the county's income-approach value as a conservative anchor and point the broker at their
  own CoStar for trades.
- Many county apps are address-only, so an owner's portfolio can't be enumerated free. The owner
  mailing address is the clustering key (see `broker-prospecting-dossier`).
- **Surface the downside.** If asking rents already sit above the submarket, say so: the upside
  is a renovation premium, not blanket increases. Buyers trust the honest read.

## The analysis

- **Cap-rate football field.** Value at a range of *local* market caps (e.g. 6.0 / 6.5 / 7.0 /
  7.5%) against the ask. If the ask's cap is wider than where the submarket trades, the ask is
  below market value: often the headline.
- **Use the right cap for the class and vintage.** Older Class-C walk-ups trade well above
  institutional Class-B caps; using the low figure can double the apparent value created.
- **Levered return**: state your own assumptions (LTV, rate, amortisation), compute DSCR,
  cash-on-cash and the value-add equity created. When caps sit below the debt rate, leverage
  hurts at ask; show the buy-below-ask + cheaper-debt scenario and say plainly that the money is
  made on price.
- **Pre-empt the county value.** The buyer will pull the assessed value; explain it (tax-basis
  floor, non-disclosure, peers assessed lower).
- **Value-add leverage**: every $1 of NOI growth = $1 ÷ cap of value. Who pays which utility is
  often a bigger lever than rent (sub-metering / bill-back). Label scenarios illustrative.
- **What to request next**: rent roll (in-place vs market), trailing-12 operating statement,
  sold comps from the broker's own data.

## The deliverable: hand-authored HTML -> PDF with real charts

| Chart | Type | Carries |
|---|---|---|
| Price per door | horizontal bars | ask vs live value-add comps |
| Cap-rate football field | horizontal bars | value at local caps vs the ask |
| Assessed-value history | line | the trade-detection step-up |
| Valuation anchors | horizontal bars | county floor -> ask -> value-add target |
| Submarket | donut + stat tiles | occupancy (true part-of-whole only), rent growth, pipeline |
| NOI -> value | line | leverage at the cap |
| Levered return | table | going-in vs stabilised (DSCR, CoC, equity) |
| Buyer pool | cards | named active investors, sourced |

Bars, lines and tables for comparisons; a donut only for a true part-of-whole; never a pie for
comps. **Charts render only real, stated numbers.** Embed images as data URIs so the HTML is
self-contained for the PDF renderer (WeasyPrint or headless Chrome). Version every revision
(`v1`, `v2`); never overwrite.

## Done when

- It answers the stated intent directly.
- It reads as a broker document: no "you should fix" anywhere.
- Every figure is public data or the broker's own; sources footnoted; nothing invented.
- Valuation is NOI ÷ cap at **local** caps; levered assumptions labelled as yours.
- Charts match the prose; the property photo verifiably shows the building.
- The honest downside is in it.
- Optional: run it past a broker reader-persona (see `simulate-campaign`) before sending.
