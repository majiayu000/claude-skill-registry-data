---
name: dv360-bid-strategy
description: Choose and configure the right Display & Video 360 bid strategy. Use when the user asks which bid strategy to use, fixed vs automated bidding, Target CPA, Target CPM, Target ROAS, maximize conversions or value, minimize CPA or CPC, target viewable CPM, custom bidding, learning periods, bid caps, or why a line item is not winning auctions.
---

# DV360 bid strategy

Pick the bid strategy for a line item and set it so it actually delivers: fixed when you need
control, automated when you have signal and a clear goal, custom when standard goals cannot
express the value you care about. The bid strategy is set on the line item and is the lever
that turns budget into won impressions against your KPI.

This skill assumes you know CPM, CPA, CPC, ROAS, and viewability. For those definitions and
the KPI math, see the `programmatic-foundations` skill. For where the line item sits in the
account, see `dv360-campaign-architecture`.

## When to use this skill

- "Which bid strategy should I use?" / "Fixed or automated bidding?"
- "Set up Target CPA / Target CPM / Target ROAS / maximize conversions / maximize value."
- "Should I use minimize CPA, target viewable CPM, optimized reach?"
- "What is custom bidding and when do I need it?"
- "How long is the learning period?" / "Why did performance drop after I changed the bid?"
- "Why is my line item not winning / not spending?"

Boundaries with sibling skills:
- Where to put the line item and how many to create: `dv360-campaign-architecture`.
- Budget pacing and in-flight optimization: `dv360-pacing-and-optimization`.
- Building a custom bidding algorithm (rules or script) in depth: `dv360-custom-bidding`.
- Deal and inventory setup that fixes the price: `dv360-deals-and-inventory`.
- Full delivery troubleshooting tree: `dv360-troubleshooting`.

## Quick reference

| Situation | Use | Why |
| --- | --- | --- |
| Little or no conversion data | Fixed bid | Automation has nothing to learn from |
| Reserved / programmatic guaranteed fixed-rate deal | Fixed bid | Price is already fixed by the deal |
| Tight, absolute CPM ceiling you cannot exceed | Fixed bid | Targets are averages, not hard caps |
| Small scale or pure reach/brand goal | Fixed bid | Not enough signal for goal-based automation |
| Want max conversions/value and have signal | Maximize (spend full budget) | Algorithm optimizes per impression |
| Want efficiency at a target | Target CPA / CPC / viewable CPM / ROAS | Optimizes toward the named goal |
| Value differs by impression beyond standard goals | Custom bidding | Score impressions on your own logic |

Two families of automated bidding:
- Maximize a KPI while spending the full budget (volume-first).
- Maximize a KPI while prioritizing a target (efficiency-first), for example a target CPA or
  target viewable CPM that the algorithm tries to meet or beat.

## Core process

1. Check conversion data. If the line item (or comparable history) lacks meaningful conversion
   volume, start fixed or with a non-conversion automated goal (viewable CPM, completed views).
   Conversion-based automation (tCPA, tROAS, maximize conversions/value) needs conversions to
   learn from.
2. Name the goal. Volume (more conversions/value), efficiency (hit a cost target), or value
   (ROAS). The goal picks the family: maximize-spend for volume, performance-goal for
   efficiency, value-based for ROAS.
3. Check inventory type. Programmatic guaranteed and reserved fixed-rate deals set the price,
   so use fixed bidding there. Biddable open auction and non-guaranteed PMP can take automated
   bidding.
4. Set the strategy on the line item. Automated bidding can be set at the line item, or set at
   the insertion order to apply to all its line items. Add a bid cap only if you must, knowing
   it can throttle the algorithm.
5. Pair with even pacing. Automated strategies optimize across the flight, so even pacing lets
   them learn and spread delivery. Do not use ASAP with automated bidding (see Decision rules).
6. Hold the strategy stable through the learning period (below). If it is starving or missing
   goal, diagnose with the pitfalls table before changing anything.

## Decision rules and thresholds

### When fixed bid wins

- Limited conversion data, so automation has nothing to optimize against.
- Reserved or programmatic guaranteed fixed-rate deals, where the price is set by the deal.
- You need tight CPM control. Note that automated targets are averages the system tries to
  hold, not absolute ceilings, so when you must stay under a hard CPM at all times, fix the bid.
- Small scale or brand/reach goals where there is not enough signal for goal-based automation.

DV360 applies optimized fixed bidding by default to avoid overpaying on a fixed-bid line item;
you can opt out if you need the exact bid every time.

### When automated bidding wins

Automated bidding calculates a per-impression bid to make the most of the budget. Pick the
goal that matches intent:

- Maximize (spend full budget): get the most conversions, value, completed in-view and audible
  impressions, or viewable impressions for the budget. Volume-first.
- Goal-constrained: maximize clicks or conversions while prioritizing a target KPI, target
  viewable CPM, target CPA, or Target ROAS. Efficiency-first.

The full list of strategies and the goal each one optimizes is in
`references/bid-strategy-map.md`.

### Custom bidding

When the value of an impression is not captured by a standard goal, use custom bidding: it
scores each impression by importance to your objective and bids accordingly. Build the
algorithm with rules (weighted conversions, no code) or a script (optimize toward
non-conversion signals such as brand lift). For building and validating the algorithm, hand
off to `dv360-custom-bidding`.

Custom bidding needs enough scored-impression volume to train. As a rule of thumb DV360 looks
for meaningful positive-signal volume per advertiser and per line item before it can calibrate,
so do not point custom bidding at a brand-new, low-volume line item.

### Learning period

Automated and custom strategies need conversion volume and a stabilization window before their
performance should be judged. The bidding algorithm can take up to four weeks to learn and
calibrate. Value-based strategies (Target ROAS, maximize conversion value) additionally want a
minimum conversion history before they qualify, and a no-change window after you switch.
Practical rule: change the strategy or its target as little as possible during learning, because
edits reset calibration and waste the window.

### Interaction with pacing

Pair automated bidding with even pacing so the algorithm can optimize across the whole flight.
ASAP pacing front-loads spend and can overspend early, which fights the optimization and burns
budget before the algorithm has learned. See `dv360-pacing-and-optimization` for pacing setup.

## Reference material

- `references/bid-strategy-map.md`: every fixed, maximize, goal-constrained, value-based, and
  custom strategy mapped to its goal, the line-item types it applies to, and the matching DV360
  API v4 field. Read this when picking a specific strategy or setting it through the API/SDF.

## Templates and examples

- Lower-funnel conversion line item, healthy conversion history: Target CPA at the line item,
  even pacing, no bid cap. Hold it for the full learning window before reading performance.
- Upper-funnel CTV awareness line item, no conversions: maximize completed in-view and audible
  impressions, or target viewable CPM, even pacing. Conversion goals would have nothing to learn.
- Premium programmatic guaranteed CTV deal at a fixed rate: fixed bid at the deal rate. The
  price is set, so automation adds nothing.
- Retail line item where a sale's value varies widely: custom bidding scoring impressions by
  predicted value, built in `dv360-custom-bidding`, then assigned here.

## Common pitfalls

- Target set too tight. A tCPA, tROAS, or target viewable CPM below what the inventory clears
  at starves delivery, because the algorithm cannot find impressions at that price. Loosen the
  target or widen targeting, then let it relearn.
- Too few conversions for tCPA or tROAS. Without conversion volume the algorithm cannot learn;
  switch to a maximize or non-conversion goal until volume builds, or consolidate line items.
- Bid cap throttling automated bidding. A cap that is too low blocks the algorithm from
  bidding to win valuable impressions. Remove or raise the cap if delivery or performance
  suffers.
- Changing strategy mid-flight. Switching strategy or moving the target resets the learning
  period and discards calibration. Decide up front and hold it.
- ASAP pacing with automated bidding. Front-loads spend and overspends before the algorithm
  has learned. Use even pacing.
- "Line item not winning." Before touching the strategy, check the usual causes: bid or target
  below the clearing price, targeting too narrow, creative not approved, budget or pacing
  capping delivery, or deal eligibility. The full tree is in `dv360-troubleshooting`.

## Sources

- [Automated bid strategies](https://support.google.com/displayvideo/answer/2997422?hl=en) (as of June 2026)
- [Value based bidding strategies](https://support.google.com/displayvideo/answer/14161766?hl=en) (as of June 2026)
- [Custom bidding overview](https://support.google.com/displayvideo/answer/9723477?hl=en) (as of June 2026)
- [Set a fixed CPM bid for a line item](https://support.google.com/displayvideo/answer/2696858?hl=en) (as of June 2026)
- [Troubleshoot your deals and line items](https://support.google.com/displayvideo/answer/6292894?hl=en) (as of June 2026)
- [BiddingStrategy, DV360 API v4 reference](https://developers.google.com/display-video/api/reference/rest/v4/BiddingStrategy) (as of June 2026)
- [advertisers.lineItems, DV360 API v4 reference](https://developers.google.com/display-video/api/reference/rest/v4/advertisers.lineItems) (as of June 2026)
