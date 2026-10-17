---
name: ttd-campaign-structure
description: Understand how a buy is organized on The Trade Desk and what each level controls. Use when the user asks about Trade Desk campaign structure, the TTD hierarchy, "TTD advertiser campaign ad group", "how is a TTD campaign organized", what a campaign vs an ad group holds on The Trade Desk, where budget and flight and goal live versus targeting and bidding and creatives, or how to lay out a TTD buy so reporting and pacing hold up. Covers the publicly supportable structure and concepts a trader should know; in-platform setup steps live in the partner platform.
---

# The Trade Desk campaign structure

Map how The Trade Desk (TTD) organizes a buy so budget, pacing, targeting, and reporting line up
before anything goes live. At a high level the hierarchy is advertiser, then campaign, then ad
group. The campaign carries the budget, the flight, and the goal; the ad group carries the
targeting, the bidding, and the creatives. Getting this split right up front is the cheapest
lever you have, because reworking structure after a campaign is delivering costs spend and resets
optimization.

This skill stays at the level public sources support: the structure and the concepts a trader
should know. The detailed, click-by-click setup (exact menu paths, field names, every toggle, and
default values) lives in The Trade Desk platform and its partner help center, which sit behind a
login. Where a specific step needs the platform, this skill says so rather than inventing a screen
name. For DSP-agnostic definitions (flight, pacing, line item, deal ID, frequency) and KPI math,
see the `programmatic-foundations` skill. For what The Trade Desk is and how Kokai and Koa fit,
see the `ttd-platform-overview` skill.

## When to use this skill

- "What is the structure of a Trade Desk campaign?" or "what is the TTD hierarchy?"
- "Advertiser, campaign, ad group: what does each one do on The Trade Desk?"
- "What does a campaign hold versus what an ad group holds on TTD?"
- "Where do budget and flight and the goal live on The Trade Desk?"
- "Where do targeting, bidding, and creatives live?"
- "How should I lay out a TTD buy so reporting and pacing work?"

Boundaries with sibling skills:
- Targeting and audience construction: hand off to `ttd-targeting-and-audiences`.
- Bid approach and optimization: hand off to `ttd-bidding-and-optimization`.
- Inventory, PMP, and programmatic guaranteed deals: hand off to `ttd-inventory-and-deals`.
- Identity, UID2, and cookieless setup: hand off to `ttd-identity-and-uid2`.
- Reporting, attribution, and measurement windows: hand off to `ttd-measurement-and-reporting`.
- API and bulk automation: hand off to `ttd-api-and-automation`.
- What TTD is, Kokai, Koa, channels, service models: hand off to `ttd-platform-overview`.

## Quick reference

The hierarchy, top to bottom:

```
Advertiser   the brand boundary; holds the seat-level context, data, and reporting roll-up
  Campaign   the budget + flight + goal container; the strategic unit of the buy
    Ad Group the execution unit; holds targeting, bidding, and the creatives that serve
      Creative the asset that renders; assigned to and rotates within the ad group
```

The single fact that drives every structural decision: on The Trade Desk the **campaign owns the
money, the dates, and the objective, and the ad group owns how you go get it**. Budget, flight,
and the goal are set on the campaign. Targeting, the bid, and the creatives are set on the ad
group. So anything that needs its own budget envelope, schedule, or goal is a campaign decision,
and anything that needs its own audience, bid, or creative set is an ad-group decision.

What each level decides:

| Level | Owns (publicly supportable) | You split here when |
| --- | --- | --- |
| Advertiser | The brand entity, seat-level data and audiences, and the reporting roll-up across its campaigns | A genuinely separate brand or billing entity is in play |
| Campaign | Budget, flight dates, and the campaign goal / objective the buy is optimized toward | The money, the schedule, or the objective differs |
| Ad group | Targeting and audiences, the bid and optimization settings, inventory selection, and the assigned creatives | The audience, the bid approach, the inventory, or the creative set differs |
| Creative | The served asset and its tracking | The message, offer, format, or size differs |

## Core process

1. Start from the media plan, not the user interface. Write down every distinct combination of
   objective, budget, flight, audience, channel, and inventory the plan calls for. That list maps
   directly onto campaigns and ad groups.
2. Open one campaign per distinct budget, flight, and goal. Because the campaign is the level that
   holds the budget and the objective, a different objective or a separately paced budget is a
   different campaign. Keep one clear goal per campaign so optimization has a single target.
3. Break out ad groups under each campaign by any axis you need to target, bid, or report on
   independently: audience, channel or format, inventory or deal set, or geo. The ad group is the
   execution unit, so that is where those splits belong.
4. Attach creatives to each ad group in the format the channel requires, and let them rotate
   within the ad group. Creative selection sits at the ad group, beneath the campaign goal.
5. Set targeting and audiences on the ad group via `ttd-targeting-and-audiences`, the bid and
   optimization via `ttd-bidding-and-optimization`, and any deals or inventory lists via
   `ttd-inventory-and-deals`.
6. Name every object with a consistent, structured convention before you build, so reporting,
   filtering, and bulk edits work from the start (see Naming convention below).
7. Confirm the exact setup steps in the platform. The order of fields, the precise goal options,
   pacing controls, and frequency settings are in-platform and can change between releases; this
   skill gives the structure, the platform gives the clicks.

## Why budget and goal sit on the campaign

Putting budget, flight, and goal at the campaign level means the campaign is the unit you pace and
the unit Koa-assisted optimization steers toward a single objective. If you scatter conflicting
objectives across ad groups inside one campaign, you blur the target the campaign optimizes for.
Keep the objective coherent at the campaign level, then express the tactical variety (audiences,
channels, creatives) as ad groups underneath. This is the same logic as any DSP where the
budget-bearing level and the optimization goal are one and the same: the thing that holds the
money is the thing the system optimizes.

What requires platform access: the specific list of selectable campaign goals, the exact pacing
modes and their math, and the frequency-cap controls and the levels they can be set at are
in-platform behaviors. State the concept (a campaign carries a single goal and a paced budget over
a flight) and route the precise options to the platform and to `ttd-bidding-and-optimization`.

## Why targeting, bidding, and creatives sit on the ad group

The ad group is where the buy actually executes, so it is where the decisions that vary by tactic
live: who you are reaching (targeting and audiences), how much you will pay and how the bid
adapts (bidding and optimization), where the ads can run (inventory and deals), and what serves
(creatives). Splitting ad groups along these axes is what gives you independent control and a
clean read in reporting. Two audiences you want to budget the same but read and optimize
separately are two ad groups. Two creative concepts you want to compare are, at minimum,
separable within or across ad groups so the report can tell them apart.

What requires platform access: the exact targeting dimensions and how audiences are attached, the
specific bid strategies and optimization settings, and how creatives are uploaded, approved, and
assigned. Those are owned by the sibling skills and, ultimately, the platform UI. This skill only
fixes which level they belong to.

## Naming convention

Consistent, structured names are what make reporting, filtering, and bulk edits work, because
report filters and bulk operations key off the name string. Use a delimited template and keep it
identical across every object.

Recommended fields, in order: client or brand, channel, objective, funnel stage, audience,
flight.

Rules:
- Use a single, consistent delimiter (an underscore works well). Pick one and never mix.
- Avoid special characters, leading or trailing spaces, and commas, which break CSV-based bulk
  workflows and report filters.
- Encode the same fields in the same order on every campaign and ad group so a wildcard filter
  isolates exactly the slice you want.
- Keep values from a controlled vocabulary (fixed channel codes, stage codes, audience codes) so
  filters match. Free-text values defeat the purpose.

Example campaign name:
`ACME_CTV_Awareness_UpperFunnel_2026Q3`

Example ad group names under it:
`ACME_CTV_Awareness_UpperFunnel_Demo_Geo_2026Q3`
`ACME_CTV_Awareness_UpperFunnel_PixelAud_Retarget_2026Q3`

## Templates and examples

A two-objective omnichannel plan mapped onto the hierarchy:

```
Advertiser: ACME (seat-level data and audiences live here, reporting rolls up here)
  Campaign: ACME_CTV_Awareness_2026Q3            (goal = awareness, its own budget + flight)
    Ad group: ..._Demo_Geo_2026Q3                 (demo + geo targeting, CPM-style bid, CTV creative)
    Ad group: ..._PixelAud_Retarget_2026Q3        (retargeting audience, its own bid, CTV creative)
  Campaign: ACME_Display_Conversion_2026Q3        (goal = conversion, separate budget + flight)
    Ad group: ..._Prospecting_Contextual_2026Q3   (contextual targeting, performance bid, display creative)
    Ad group: ..._Retarget_SiteVisitors_2026Q3    (site-visitor audience, performance bid, display creative)
```

Why it splits this way: awareness and conversion are separate campaigns because the objective and
the paced budget differ, and the campaign is the level that holds both. Inside each campaign the
ad groups split by audience and tactic because that is the execution level where targeting, bid,
and creative vary and where you want an independent read. The advertiser-level audiences (for
example the site-visitor pool) are defined once and reused by the ad groups that need them.

## Common pitfalls

- **Treating the ad group as the budget container.** On The Trade Desk the budget, flight, and
  goal sit on the campaign. Plan the money and the objective at the campaign level, then express
  tactics as ad groups.
- **Mixing conflicting goals inside one campaign.** A campaign carries one objective and the
  optimization steers toward it. Splitting awareness and conversion into the same campaign blurs
  the target. Use one campaign per goal.
- **Over-splitting ad groups so finely that none gathers enough signal.** Conversion-based
  optimization needs volume to learn. Split ad groups only where you will actually act on the
  distinction; otherwise consolidate. The learning mechanics live in
  `ttd-bidding-and-optimization`.
- **Free-text or special characters in names.** They break bulk round-trips and report filters.
  Lock a delimited template and a controlled vocabulary before building.
- **Asserting exact in-platform steps from memory.** The precise goal options, pacing modes,
  frequency controls, and field names are in-platform and change across releases. Give the
  structure, then confirm the clicks in the platform and its partner help center.

## Sources

- Our platform, The Trade Desk (omnichannel platform to plan, execute, and measure media buying
  across channels; self-serve): https://www.thetradedesk.com/us/our-platform (as of June 2026)
- Our Demand Side Platform (DSP), The Trade Desk (independent DSP; advanced data-driven tools to
  plan, execute, and measure; unify media buying across channels in a single platform):
  https://www.thetradedesk.com/us/our-platform/dsp-demand-side-platform (as of June 2026)
- The Trade Desk, Wikipedia (omnichannel platform for brands and advertisers; largest independent
  demand-side platform): https://en.wikipedia.org/wiki/The_Trade_Desk (as of June 2026)

The advertiser, campaign, and ad group hierarchy and the level each setting belongs to are
described here at the publicly supportable level. The step-by-step build (exact menu paths, the
full list of campaign goal options, pacing and frequency controls, and how targeting, bids, and
creatives are configured and assigned) lives in The Trade Desk platform and its partner help
center, which require a logged-in seat and so are not cited above. Use the platform and its
in-platform help for those specifics, and the sibling TTD skills for each subsystem.
