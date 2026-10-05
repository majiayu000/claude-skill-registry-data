---
name: customer-rfp-response-process
description: |
  Use when a carrier (asset-based, brokerage, or 3PL) asks how to respond to a shipper RFP / RFQ — bid
  packaging, lane analysis, rate strategy, SOPs/SOWs, qualifications response, insurance compliance,
  EDI requirements, and how to win competitive bids without leaving margin on the table.
---

# Customer RFP Response Process

A Request For Proposal (RFP) or Request For Quote (RFQ) is how mid-to-large shippers select carriers for annual or multi-year freight contracts. Winning RFPs at the right rates is how carriers grow their book of business without spending on sales reps.

## Types of bids

| Type | Length | Detail |
|---|---|---|
| Spot quote | Minutes to hours | Single load, current rate |
| Mini-bid | 1–2 weeks | 5–20 lanes, 3–6 month duration |
| Annual RFP | 4–8 weeks | 100+ lanes, full 12-month contract |
| Multi-year contract | 8–12 weeks | Strategic award, often top 5 carriers per shipper |

Annual RFPs and multi-year contracts are the prize — predictable freight, dedicated capacity, sometimes guaranteed lanes.

## What a shipper sends

Typical RFP package:

1. **Cover letter** — introduction, contact, timeline, decision criteria
2. **Bid file (Excel)** — lanes, volumes, equipment, modes, accessorials
3. **Standard Operating Procedures (SOP)** — pickup/delivery process, scheduling, claims
4. **Master Transportation Agreement (MTA)** — contract terms
5. **Insurance requirements** — limits, endorsements (e.g., $2M auto liability, $1M cargo)
6. **EDI requirements** — 204/210/214/990 transactions, technology compatibility
7. **Qualifications questionnaire** — DOT #, safety scores, fleet size, ELD provider, references
8. **Sustainability questionnaire (growing)** — emissions, SmartWay membership

## RFP response workflow (4–8 weeks typical)

### Week 1 — Triage and qualify

- Read full RFP (every page)
- Identify lanes you can serve (match equipment, geography, capacity)
- Check insurance compliance (can we get the limits? at what cost?)
- Check EDI capability (do we have it or need to invest?)
- Decide go/no-go: pursue only if 30%+ of lanes are winnable

### Week 2 — Lane analysis

For each lane:
- Origin / destination ZIP
- Volume (loads/week, loads/year)
- Equipment type
- Tender pattern (M-F daytime? night? weekend?)
- Current rate (often disclosed by shipper) or market rate (DAT, Truckstop, internal data)
- Cost-to-serve estimate
- Margin target

Build a pricing model per lane.

### Week 3 — Pricing strategy

| Strategy | When to use |
|---|---|
| Match market rate exactly | Most lanes, you'll have margin from operational efficiency |
| Aggressive below-market | "Strategic lane" — buy market share, willing to lose money short-term |
| Above-market premium | Specialty service (temp-controlled, hazmat, white-glove) |
| Reject | Lanes you can't profitably serve |

Aggressive bids should be a small fraction (5–15%) of total volume to manage risk.

### Week 4 — Qualifications and proposal

Compile:
- Company profile (years in business, fleet size, equipment mix)
- Safety profile (DOT #, MCS-150, CSA scores, accident history)
- Financial information (D&B rating, references)
- Technology (TMS, ELD, EDI, GPS tracking)
- Sustainability (SmartWay, EV pilot, biodiesel)
- Customer references (3–5 references with permission)

Write executive summary that highlights:
- Specific lanes / volumes you're bidding
- Your differentiated value (reliability score, on-time %, tracking visibility)
- Why you can serve at your rate (operational scale, dedicated trucks, regional terminal)

### Week 5–6 — Submission and Q&A

- Submit by deadline (often through TMS bid portal or transportation procurement system like JDA, Coupa, MercuryGate, etc.)
- Respond to follow-up questions promptly (usually 48 hours)
- Sometimes oral interviews / "best and final" rounds

### Week 7–8 — Award

- Shipper announces awards (lane-by-lane allocation)
- Negotiate edge cases on award (you may get a lane you didn't bid; you may not get a lane you did bid)
- Sign contract / MSA
- Implementation: EDI testing, SOP review, account-manager assignment

## Pricing levers in your favor

| Lever | Notes |
|---|---|
| Multi-year commitment | Lock 12–24 mo at a slight premium for steady freight |
| Backhaul opportunity | If shipper has 2-way freight, price together |
| Equipment dedication | Dedicate 5–10 trucks at a slight premium for guaranteed capacity |
| Drop-and-hook trailers | More efficient, justify $0.10–$0.20/mi premium |
| Tracking visibility (real-time GPS) | Modern shippers pay for this |
| On-time guarantee | Premium for service-level commitment |
| Surge capacity option | Shipper pays a retainer for guaranteed capacity in peak |

## Pitfalls to avoid

- Bidding without modeling cost-to-serve (you win the lane, lose money)
- Skipping the SOP review — you signed for a process you can't operationally perform
- Missing the insurance limit ($2M auto liability standard now — many smaller carriers default $1M)
- No EDI capability — disqualified from large shipper bids
- Failing to negotiate accessorial rates (detention, layover, fuel surcharge, lumper) — eats margin
- Bidding all lanes equally aggressive — concentration risk if 30% of bids hit and you can't cover
- Not having a strong safety profile — shipper procurement is risk-averse

## Insurance requirements (shipper baseline 2025)

| Coverage | Common requirement |
|---|---|
| Auto liability | $1M–$2M ($5M for hazmat, heavy haul) |
| General liability | $1M |
| Cargo | $100K (some shippers require $250K) |
| Workers' comp | Statutory |
| Umbrella | $5M–$10M for tier-1 shippers |

Annual premium for a 50-truck fleet at standard limits: $200K–$500K depending on safety profile. CSA scores directly affect rate.

## EDI requirements

| Transaction | Function |
|---|---|
| 204 | Shipment Tender (shipper offers load) |
| 990 | Response to Tender (accept/reject) |
| 214 | Shipment Status (in-transit updates) |
| 210 | Invoice |
| 820 | Payment Order |

Modern alternatives: API integrations, MercuryGate, MacroPoint, project44 visibility platforms.

Without EDI/API capability, carrier is locked out of ~70% of shipper RFPs.

## Sustainability / SmartWay

EPA SmartWay Transport Partnership is increasingly required:
- Free, voluntary
- Measure fuel/emissions data
- Annual report submission
- Many Fortune 500 shippers require Partner status to bid

Becoming a Partner: ~6–8 hours of data prep + annual reporting. Low effort, high access.

## Award rate / contract management

Once awarded:
- Set up shipper in TMS with rate schedule
- Configure EDI partner
- Train operations team on shipper SOP
- Monitor early-load performance (on-time %, tender acceptance %)
- Quarterly business review with shipper
- Renew or rebid annually

## Common mistakes

- Bidding without lane-cost modeling — you're guessing
- Ignoring tender-acceptance metric in shipper's scorecard — gets you "off-loaded" mid-contract
- No follow-up on submitted bids — losing visibility / relationship
- Bid + win + can't cover (over-commit) — destroys shipper relationship for years
- Treating RFP as one-shot — RFP cycles repeat annually, build relationship for next year
- Aggressive rate on day 1 of contract — leaves you no room when fuel spikes or driver pay raises

## Where this fits in X3

X3 captures lane-level cost data (driver pay, fuel, equipment, overhead) so carriers can model bid rates against actuals. The dashboard rolls up tender-acceptance and on-time performance per shipper so quarterly business reviews are data-driven.

Bidding well is the difference between a fleet that grows and a fleet that gets squeezed. Most small carriers leave significant margin in their bids — modeling the math closes that gap.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=customer-rfp-response-process

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
