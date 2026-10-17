---
name: amazon-dsp-campaign-setup
description: Build an Amazon DSP order and its line items end to end. Use when the user asks how to set up an Amazon DSP campaign, create an order and line items, configure DSP line item settings, choose supply, budget and pacing, flight, the optimization goal, frequency, dayparting, or how to layer targeting on an Amazon DSP line item.
---

# Amazon DSP campaign setup

Build an Amazon DSP order and the line items under it: pick the supply, set budget and pacing, set
the flight, choose the optimization goal, set frequency and dayparting, and layer targeting. This is
the execution playbook; it assumes the structure is already decided. Each setting has a default that
is usually wrong for a specific buy, so the value is in the decision at each step, not the click path.

Amazon DSP is Amazon's programmatic demand-side platform for display, video, audio, and streaming TV
across Amazon properties and third-party exchanges. It is distinct from Amazon Ads sponsored ads
(Sponsored Products, Sponsored Brands, Sponsored Display), which are retail-search self-service ads
with no order or line item model. "Campaign" in everyday speech maps to an order in the DSP.

This skill assumes you know what a CPM, a flight, frequency, and pacing are. For KPI math and shared
definitions, see the `programmatic-foundations` skill.

## When to use this skill

- "Set up an Amazon DSP campaign." / "Walk me through building a DSP order."
- "Create an order and line items." / "What goes in an order vs a line item?"
- "What DSP line item settings do I configure, and in what order?"
- "How do I pick supply / budget / pacing / flight / goal / frequency / dayparting on a line item?"
- "How do I layer targeting onto a line item?"

Boundaries with sibling skills:
- The hierarchy itself, advertiser vs order vs line item, seats, pixels, product types: hand off to
  `amazon-dsp-account-structure`.
- Audience segments and how to build them: hand off to `amazon-dsp-audiences`.
- Choosing exchanges, deals, PMP and programmatic guaranteed, supply quality: hand off to
  `amazon-dsp-inventory-and-supply`.
- Bid mechanics, optimization-goal behavior, learning, and why a line item underdelivers: hand off
  to `amazon-dsp-bidding-and-optimization`.
- Creative specs and assignment: hand off to `amazon-dsp-creative-and-formats`.
- What to measure and report by objective: hand off to `amazon-dsp-measurement-and-reporting` and the
  `reporting-by-campaign-goal` skill.

## Quick reference

Setup order (top down, because each step constrains the next):

```
1. Order      objective -> total budget -> flight -> overall optimization goal -> order frequency
2. Line item  product type -> supply -> targeting -> budget within order -> pacing
                 -> bid / optimization -> frequency -> dayparting -> creative
3. Pre-launch QA, then activate
```

Per-line-item decision table:

| Setting | Decide by | Common default to override |
| --- | --- | --- |
| Product type | Inventory and creative you have (display, OLV, STV, audio) | Set deliberately; drives every later option |
| Supply | Reach and quality target; deal vs open exchange | Do not leave wide open for performance buys |
| Targeting | Order goal plus the audience for this slice | Avoid stacking so many layers that scale dies |
| Budget | Share of order budget for this slice | Even split is rarely the right split |
| Pacing | Even for steady delivery, ahead for fast learning or short flights | Even pacing |
| Bid / goal | The KPI the order optimizes toward | Default bid usually too high or too low |
| Frequency | Channel norms (STV tighter, display looser) | Uncapped or order default |
| Dayparting | When the audience converts | All hours |
| Creative | Matches product type and supply specs | None assigned blocks delivery |

## Core process

### Build the order first

1. Confirm objective and seat. State the single objective for this order (awareness, consideration,
   or performance); it drives the goal and the metrics you will report. Confirm whether you are on a
   self-service or managed-service seat, because that decides who executes. If structure is unclear,
   resolve it with `amazon-dsp-account-structure` before building.
2. Set the total budget and budget cap. The order holds the money the line items spend against, so
   set the pool here and decide whether to cap daily spend to smooth delivery.
3. Set the flight. Start and end dates define the campaign window; line items can run the full window
   or a sub-window, never outside it. Leave a few days of runway before a hard end date so pacing and
   optimization can finish rather than rushing spend at the close.
4. Choose the overall optimization goal and KPI. Pick the goal that matches the objective (reach or
   video completion for awareness, consideration or page-view signals mid-funnel, a conversion or
   ROAS goal for performance). Line items optimize within this. For goal mechanics, see
   `amazon-dsp-bidding-and-optimization`.
5. Set a default frequency cap at the order if one cap fits the whole buy; tighten per line item where
   needed.

### Build each line item

6. Choose the product type: standard display, online video, streaming TV, or audio, matched to the
   inventory and creative you have. Type drives supply, creative specs, and bidding options. Standard
   display now covers desktop, mobile web, and mobile app in one line item.
7. Select supply. Choose Amazon-owned supply, third-party exchanges, and any deals (PMP or
   programmatic guaranteed) for this line item. Keep a deal in its own line item so delivery and
   pricing stay visible. For supply selection and quality, hand off to
   `amazon-dsp-inventory-and-supply`.
8. Layer targeting. Add the audience for this slice plus contextual, geo, device, and other layers on
   top of the order's defaults. Add only the layers the goal needs; every additional layer shrinks
   addressable supply. Build audiences in `amazon-dsp-audiences`.
9. Set the line item budget within the order. Decide this slice's share of the order budget; an even
   split across line items is rarely optimal, so weight toward the supply and audience that serve the
   goal.
10. Set pacing. Even pacing for steady delivery across the flight; front-load (spend ahead) only for a
    short flight or to gather optimization signal fast, then watch for early budget exhaustion.
11. Set the bid and optimization within the order goal. Start from a bid grounded in the channel's CPM
    range, not the default. For how bidding learns and why a line item may not win, hand off to
    `amazon-dsp-bidding-and-optimization`.
12. Set frequency. Tighten the cap for this line item by channel: STV and online video tolerate far
    fewer exposures than display before wear-out. Set caps per the period that matches the buy
    (per day and per week are both common).
13. Set dayparting. Restrict to the hours and days the audience actually converts when the data
    supports it; otherwise run all hours and let optimization find the pattern.
14. Assign creatives. Attach creatives that match the product type and pass the supply's specs; a line
    item with no eligible creative will not deliver. For specs, see `amazon-dsp-creative-and-formats`.

### Before launch

15. QA every line item: product type matches creative, supply is not accidentally wide open or
    empty, targeting layers are not so stacked that scale is near zero, budget and flight sit inside
    the order, a frequency cap is set, and creatives are assigned and approved. Confirm the pixel and
    conversion events exist at the advertiser (set in `amazon-dsp-account-structure`) so optimization
    has signal from the first impression. Then activate.

## Decision rules and thresholds

- One objective per order. If a slice needs a different budget, flight, or goal, it belongs in its
  own order, not a line item (see `amazon-dsp-account-structure`).
- Budget split follows the goal, not fairness. Put budget where the supply and audience most likely
  hit the KPI; rebalance as data comes in rather than locking an even split.
- Pacing: even by default. Use front-loaded pacing only for short flights or to seed optimization,
  and then monitor for the budget exhausting before the flight ends.
- Frequency by channel. Streaming TV and online video wear out fast, so cap exposures tightly; display
  tolerates more. An uncapped video line item burns budget on the same households.
- Targeting depth vs scale. Each added layer (audience and contextual and geo and device) multiplies
  down addressable supply. For performance, prefer a tight audience with light contextual; for reach,
  keep layers minimal so the goal can scale.
- Flight runway. End the buy a few days before any hard deadline so pacing and optimization land
  smoothly instead of dumping spend at the close.
- Deals get their own line item. Never blend a guaranteed or PMP deal with open exchange in one line
  item; you lose delivery and pricing visibility.

Several specific defaults (exact frequency-cap presets, minimum bids, pacing options, available goal
types) vary by product type, country, and console version, and some sit on login-gated console pages.
Confirm the current option for your market in the Amazon DSP console rather than relying on a fixed
number here.

## Templates and examples

A performance display order with a prospecting and a retargeting line item:

```
Order: ACME_Display_Performance_2026Q3
  Objective: performance | Budget: 120,000 USD | Flight: Jul 1 - Sep 28 (runway before Sep 30)
  Goal: optimize to off-Amazon purchase | Order frequency: default cap, tightened per line item

  Line item: ACME_Display_Prospecting_Standard_2026Q3
    Product type: standard display | Supply: Amazon + 3P open exchange
    Targeting: in-market + lifestyle audiences, light contextual, US geo
    Budget: 70% of order | Pacing: even | Bid: grounded in display CPM range
    Frequency: per-day cap | Dayparting: all hours | Creative: responsive e-commerce set

  Line item: ACME_Display_Retargeting_Standard_2026Q3
    Product type: standard display | Supply: Amazon + 3P open exchange
    Targeting: site-visitor + cart-abandoner audiences, no extra contextual, US geo
    Budget: 30% of order | Pacing: even | Bid: higher than prospecting (higher intent)
    Frequency: tighter per-day cap | Dayparting: all hours | Creative: offer-led set
```

Why it is built this way: one objective (performance) means one order. Prospecting and retargeting are
separate line items so their bids, budgets, audiences, and creative differ and read independently.
Retargeting gets a higher bid and tighter frequency because intent is higher and the audience is
smaller. Budget weights toward prospecting because it carries the reach, and the flight ends two days
early so optimization lands cleanly.

A short-flight streaming TV awareness order:

```
Order: ACME_STV_Launch_Awareness  | Goal: reach + video completion | Flight: 2 weeks
  Line item: ACME_STV_Prospecting_PremiumVideo
    Product type: streaming TV | Supply: Amazon premium video + select 3P apps
    Targeting: broad demo + lifestyle audience, minimal extra layers (protect scale)
    Pacing: front-loaded (short flight, seed optimization early)
    Frequency: tight weekly cap (video wears out fast) | Creative: non-skippable video
```

## Common pitfalls

- Building it bottom-up. The order's budget, flight, and goal constrain every line item, so set the
  order first or you will rework the line items.
- Leaving supply wide open on a performance line item. Open, unfiltered supply wastes budget; scope
  supply to quality inventory and the relevant deals.
- Over-stacking targeting. Audience plus contextual plus geo plus device plus daypart can shrink
  addressable supply to near zero. Add only the layers the goal needs.
- Uncapped frequency on video or STV. The same households absorb the budget. Cap video tightly.
- Even budget splits by habit. Weight budget toward the supply and audience that serve the goal, and
  rebalance from data.
- Front-loading by default. Front-loaded pacing on a long flight exhausts budget early; reserve it for
  short flights or deliberate optimization seeding.
- Launching without creatives assigned or the pixel live. A line item with no eligible creative does
  not deliver, and a missing conversion event makes the early flight optimize blind.
- Treating this as sponsored ads. There are no keywords or ASIN bids here; if the request is about
  search-result ads, it is Sponsored Products / Brands / Display, not the DSP.

## Sources

- [Amazon DSP: Advertise with a demand-side platform](https://advertising.amazon.com/solutions/products/amazon-dsp) (as of June 2026)
- [What is a demand-side platform? A complete guide](https://advertising.amazon.com/library/guides/demand-side-platform) (as of June 2026)
- [Amazon DSP APIs developer guide](https://advertising.amazon.com/API/docs/en-us/guides/dsp/developer-guide) (as of June 2026)
- [How to create and update a line item (DSP API tutorial)](https://advertising.amazon.com/API/docs/en-us/guides/dsp/tutorials/create-and-update-line-item) (as of June 2026)
- [Simplified display line items (single standard display line item)](https://advertising.amazon.com/resources/whats-new/display-line-item-consolidation) (as of June 2026)

Exact in-console setup steps, available pacing and goal options, and frequency presets live on
login-gated console help such as the "Create an Amazon DSP campaign" page in the Amazon Ads Support
Center. Where a specific option or number is not on a public page, the steps above describe standard
Amazon DSP practice; confirm the current option in the Amazon DSP console for your market.
