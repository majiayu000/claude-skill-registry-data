---
name: carrier-cost-per-mile-modeling
description: |
  Use when a carrier asks how to calculate cost-per-mile (CPM) at the fleet, truck, lane, or driver
  level — separating fixed vs variable costs, allocating overhead, accounting for empty miles, and
  using CPM to negotiate rates, build pricing tiers, or evaluate lane profitability.
---

# Carrier Cost-Per-Mile (CPM) Modeling

CPM is the single most important number in trucking economics. Every rate quoted, every lane evaluated, every truck spec'd should ultimately be tested against CPM. Carriers who don't know their CPM are guessing.

## Definition

**CPM = Total Operating Cost ÷ Total Miles Driven**

Most carriers compute three versions:
- **Loaded CPM** = Total cost / Loaded miles only
- **Total CPM** = Total cost / All miles (loaded + empty)
- **Marginal CPM** = Variable cost only / Miles (used for incremental decisions)

## Cost categories

### Variable costs (per-mile)

These scale directly with miles driven:

| Item | Typical $/mi |
|---|---|
| Driver wages | $0.55–$0.70 |
| Driver benefits & payroll tax | $0.10–$0.15 |
| Fuel (after fuel surcharge offset) | $0.05–$0.15 |
| Maintenance (parts + labor) | $0.10–$0.18 |
| Tires | $0.025–$0.04 |
| Tolls & permits | $0.03–$0.06 |

**Total variable: $0.85–$1.30 per mile**

### Fixed costs (allocated per mile)

These exist whether the truck runs or not — allocated by dividing annual cost by expected annual miles:

| Item | Annual $/truck | $/mi at 120K mi |
|---|---|---|
| Tractor depreciation or lease | $24,000–$36,000 | $0.20–$0.30 |
| Trailer depreciation | $3,500–$5,500 | $0.03–$0.05 |
| Insurance (liability + cargo + physical damage) | $9,000–$18,000 | $0.075–$0.15 |
| Office payroll (allocated) | $10,000–$18,000 | $0.08–$0.15 |
| Office occupancy | $1,500–$3,500 | $0.013–$0.03 |
| Software (TMS, ELD, accounting) | $1,800–$3,500 | $0.015–$0.03 |
| Permits/licenses (IRP, 2290, UCR) | $2,500–$4,500 | $0.02–$0.04 |
| Other G&A | $4,000–$10,000 | $0.03–$0.08 |

**Total fixed: $0.45–$0.65 per mile** at 120K miles/year.

### Full CPM

Variable + Fixed = **$1.30–$1.95 per total mile** for a typical asset-based dry van OTR fleet.

## Three CPM uses

### 1. Rate negotiation floor

When a broker offers $2.10/mile on a 600-mile load:

- Loaded CPM: $1.65 → margin $0.45/mi → $270 contribution
- Account for empty miles back (200 mi @ $0): total trip miles 800, revenue $2.10 × 600 = $1,260
- Total-trip CPM: $1,260 / 800 = $1.575 revenue per mile
- Vs full CPM $1.65 → loss of $0.075/mi × 800 = -$60

Decision: reject. Or only accept if you can find a backhaul covering the deadhead.

### 2. Lane profitability

| Lane | Avg loaded CPM revenue | Empty % | Effective rev/mi | Margin vs CPM $1.65 |
|---|---|---|---|---|
| CHI→ATL→CHI | $2.35 (round trip) | 5% | $2.23 | +$0.58 |
| LA→NYC | $2.80 (1-way) | 50% | $1.40 | -$0.25 |
| DAL→DFW local | $3.10 | 15% | $2.64 | +$0.99 |
| Phoenix dedicated | $2.20 (round trip) | 8% | $2.02 | +$0.37 |

Drop or reprice unprofitable lanes. Bid hard for high-margin lanes at next RFP.

### 3. Truck-level rollup

Per truck per year:
- Miles: 130,000
- Loaded miles: 117,000 (90% loaded)
- Revenue per loaded mile: $2.20 = $257,400
- Total CPM: $1.55 = total cost $201,500
- Operating margin: $55,900 = 21.7%

A second truck operating at 80% loaded ratio at the same loaded rate produces:
- Loaded miles: 104,000 × $2.20 = $228,800
- Total miles: 130,000 × $1.55 = $201,500
- Operating margin: $27,300 = 11.9%

Same equipment, same driver pay rate — but the loaded ratio gap costs $28K/year. Loaded ratio is the highest-leverage operational metric.

## Driver-level CPM

A 50-driver fleet:
- Top quartile drivers: total CPM $1.40 (low fuel idle, low maintenance, high MPG)
- Bottom quartile drivers: total CPM $1.95 (high idle, hard on equipment, low MPG)

Spread = $0.55/mi × 130K miles = $71,500/year per driver difference. Coach or replace bottom quartile — biggest lever in the operation.

## Computing CPM (practical workflow)

### Step 1 — Pull 12 months of expense data

From accounting (QuickBooks, Sage, NetSuite):
- Total driver compensation (W-2 wages + benefits + tax)
- Fuel purchases
- Maintenance (parts + labor)
- Tires
- Insurance (annual / 12)
- Depreciation
- Office payroll
- Office occupancy
- Software
- All G&A

### Step 2 — Pull total miles from ELD or TMS

- Total miles driven (all trucks, all months)
- Total loaded miles (if separated)

### Step 3 — Allocate

- Total cost / total miles = Total CPM
- Total cost / loaded miles = Loaded CPM

### Step 4 — Drill down

- By truck (assign each truck's miles + maintenance + fuel)
- By driver (assign each driver's pay + miles + fuel events)
- By lane (assign trip-level revenue and cost)

Most TMS / fleet management systems do this automatically once data is wired up.

## Common mistakes

- Computing CPM only on loaded miles (and ignoring deadhead) — overstates profitability
- Not allocating fixed cost to per-mile — quotes that look profitable aren't
- Using "industry average" CPM instead of your actual numbers — every fleet is different
- Failing to update CPM quarterly as fuel and driver pay shift
- Treating all trucks as equal — newer trucks cost 30–40% less to maintain
- Bidding rates below CPM "to keep the truck moving" — losing money per mile is worse than parking

## Where this fits in X3

X3 auto-computes total and loaded CPM at the fleet, truck, and driver level using ELD + fuel-card + maintenance + accounting feeds. The negotiation tool overlays current CPM on broker rate offers and flags loss-making loads before acceptance.

CPM is not a one-time calculation — it's a weekly habit. Carriers that watch CPM beat carriers that don't.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=carrier-cost-per-mile-modeling

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
