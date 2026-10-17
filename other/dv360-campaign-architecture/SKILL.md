---
name: dv360-campaign-architecture
description: Structure a Display & Video 360 account the right way. Use when the user asks how to structure a campaign, insertion order vs line item, when to split insertion orders or line items, the DV360 hierarchy (partner, advertiser, campaign, insertion order, line item), naming conventions, or how to lay out a media plan in DV360.
---

# DV360 campaign architecture

Decide how to map a media plan onto the Display & Video 360 hierarchy: how many insertion
orders, where to split line items, and how to name everything so reporting and automation
hold up. Good structure is the single biggest lever on whether bidding, pacing, and reporting
behave later. Bad structure is expensive to unwind once a campaign is live.

This skill assumes you know what a CPM, a flight, and a funnel stage are. For KPI definitions
and shared math, see the `programmatic-foundations` skill.

## When to use this skill

- "How should I structure this campaign in DV360?"
- "Insertion order or line item for this?" / "Should this be one IO or several?"
- "When do I split line items?" / "Should video and display live in the same line item?"
- "What is the DV360 hierarchy?" / "Where does Floodlight sit?"
- "What naming convention should I use?"

Boundaries with sibling skills:
- Bid strategy choice per line item: hand off to `dv360-bid-strategy`.
- Targeting and audience construction: hand off to `dv360-targeting-and-audiences`.
- Deal and PG/PMP setup: hand off to `dv360-deals-and-inventory`.
- Budget pacing and in-flight optimization: hand off to `dv360-pacing-and-optimization`.
- Account-level governance, partner/advertiser provisioning, taxonomy ownership: hand off to
  `dv360-account-setup-and-taxonomy`.
- Pre-launch verification: hand off to `dv360-launch-qa`.

## Quick reference

The hierarchy, top to bottom:

```
Partner            agency / trading desk; partner-level settings inherit down
  Advertiser       one real business; owns creatives, audiences, Floodlight, deals
    Campaign       optional planning container; overall objective and total budget
      Insertion Order   the budget + flight + pacing + KPI container
        Line Item       the targeting + bidding + creative-assignment unit
          Ad / Creative assigned at the line item
```

Floodlight (conversion tracking) lives at the advertiser level and is shared from Campaign
Manager 360 across Google Marketing Platform, not inside an individual IO or line item.

What each level decides:

| Level | Owns | You change it when |
| --- | --- | --- |
| Insertion order | Budget, flight dates, pacing, frequency caps, KPI/performance goal | The money, the dates, or the goal differ |
| Line item | Targeting, bid strategy, creative assignment, format | The audience, bid, format, or creative set differ |

## Core process

1. Start from the media plan, not the UI. List every distinct combination of objective,
   market, channel, buying type, budget, and flight. Each distinct budget-and-flight cell is
   a candidate insertion order, because the IO is the only level that holds a budget and dates.
2. Group those cells into insertion orders using the IO split rules below. One IO carries one
   budget, one flight, one pacing setting, and one KPI, so anything that needs its own budget,
   schedule, or success metric needs its own IO.
3. Inside each IO, break out line items using the line item split rules. The line item is the
   bidding and targeting unit, so any axis you want to bid, target, optimize, or report on
   independently becomes its own line item.
4. Pick the line item type per line item (display, video, audio, and YouTube handled
   separately). Type drives available formats, bidding, and inventory.
5. Name every object with the structured convention below before you build, so reporting,
   filtering, and Structured Data File (SDF) automation work from day one.
6. Hand off bidding to `dv360-bid-strategy`, targeting to `dv360-targeting-and-audiences`, and
   run `dv360-launch-qa` before going live.

## Decision rules and thresholds

### Split INSERTION ORDERS by

Each of these forces a separate budget, flight, pacing, or KPI, which only an IO can hold.

- Funnel stage. Awareness, consideration, and conversion carry different KPIs and budgets,
  so keep them in separate IOs. This also keeps frequency management and reporting clean.
- Market or geo. Separate IOs per country or major region when budgets, flights, currency
  pacing, or reporting are managed independently.
- Channel or format. Display, video, CTV, and audio behave differently on pacing, viewability,
  and benchmarks. Separate IOs keep budget control and reporting honest per channel.
- Buying type. Open auction versus programmatic guaranteed or PMP. Guaranteed and reserved
  deals have fixed commitments and fixed pricing, so isolate them from biddable open auction.
- Bid strategy. If two sets of line items need different optimization goals at the IO level,
  separate the IOs so one goal does not constrain the other.
- Verification vendor. Separate IOs when a third-party measurement or brand-safety vendor
  differs, so the cost and reporting attach cleanly.
- Distinct budgets or flights. Any line items that must not share a budget pool or start/end
  date belong in different IOs. Line items inside one IO share its budget and dates.
- Reporting needs. If finance or the client needs a clean budget line for a slice of the buy,
  give that slice its own IO.

### Split LINE ITEMS by

Each of these is an axis you want to target, bid, optimize, or report on independently.

- Audience strategy. Prospecting versus retargeting, or distinct audience segments, so bids
  and budgets do not bleed across intent levels.
- Creative set. A line item serves its assigned creatives, so a different message, offer, or
  campaign concept needs its own line item to keep reporting and rotation clean.
- Format or size. Separate display sizes, or static versus rich media, when you want to read
  performance or pace them differently.
- Device. Split mobile, desktop, CTV, and tablet when bids, creatives, or performance differ
  by device.
- Frequency rule. A distinct frequency cap or exposure goal for a slice of the audience.
- Optimization axis. Any dimension you want the bid strategy to optimize or that you want to
  isolate in reporting (for example, a test cell).
- Deal versus open auction. Keep a specific deal in its own line item, separate from open
  auction, so deal delivery and pricing are visible and controllable.

Do not over-split. Every extra line item fragments conversion volume, which starves automated
bidding (see `dv360-bid-strategy` on learning periods). Split only where you will act on the
distinction. If two cells would always get the same bid, targeting, and creative, merge them.

### Line item types

Pick the type that matches the buy: display (image, HTML5, native), video, and audio.
YouTube and Demand Gen line items are a separate family with their own formats and bidding;
treat them apart from standard display/video/audio line items.

## Naming convention

Consistent, structured names are what make reporting, filtering, and SDF automation work,
because DV360 reporting and bulk edits key off the name string. Use a delimited template and
keep it identical across every object.

Recommended fields, in order: client, market, channel, objective, funnel stage, flight.

Rules:
- Use a single, consistent delimiter (an underscore works well). Pick one and never mix.
- Avoid special characters, leading/trailing spaces, and commas, which break CSV-based SDF
  workflows and report filters.
- Encode the same fields in the same order on every IO and line item so a wildcard filter
  isolates exactly the slice you want.
- Keep values from a controlled vocabulary (fixed market codes, channel codes, stage codes)
  so filters match. Free-text values defeat the purpose.

Example IO name:
`ACME_US_CTV_Awareness_UpperFunnel_2026Q3`

Example line item names under it:
`ACME_US_CTV_Awareness_UpperFunnel_Prospecting_15s_2026Q3`
`ACME_US_CTV_Awareness_UpperFunnel_Retargeting_30s_2026Q3`

For the controlled vocabulary, governance, and who owns the taxonomy, see
`dv360-account-setup-and-taxonomy`.

## Reference material

- `references/structure-decision-tables.md`: the full IO-split and line-item-split checklists,
  a worked multi-market plan mapped to IOs and line items, and a naming-field cheat sheet.
  Read this when you are laying out a real plan and want a checklist to work through.

## Templates and examples

A two-market, two-funnel-stage prospecting-plus-retargeting video plan:

```
Advertiser: ACME (Floodlight shared from CM360 at this level)
  Campaign: ACME_2026Q3_Brand
    IO: ACME_US_OLV_Consideration_MidFunnel_2026Q3      (budget, flight, even pacing, CPV KPI)
      LI: ..._Prospecting_InStream_2026Q3
      LI: ..._Retargeting_InStream_2026Q3
    IO: ACME_US_OLV_Conversion_LowerFunnel_2026Q3        (separate budget, tCPA KPI)
      LI: ..._Retargeting_InStream_2026Q3
    IO: ACME_CA_OLV_Consideration_MidFunnel_2026Q3       (separate market = separate IO)
      LI: ..._Prospecting_InStream_2026Q3
```

Why it splits this way: US and CA are separate IOs because their budgets, flights, and
reporting are managed independently. Consideration and conversion are separate IOs because
they carry different KPIs and budgets. Prospecting and retargeting are separate line items
because they need different audiences, bids, and creative, and you want to read them apart.

## Common pitfalls

- Putting display and video in one line item. They cannot share a creative format cleanly and
  the blended reporting hides what is working. Split by channel/format.
- One mega-IO for the whole plan. You lose independent budget control, pacing, and per-goal
  KPI reporting. Split by funnel stage and market first.
- Splitting line items so finely that no single line item gets enough conversions for
  automated bidding to learn. Consolidate test cells you will not act on.
- Free-text or special characters in names. They break SDF round-trips and report filters.
  Lock a delimited template and a controlled vocabulary before building.
- Expecting Floodlight to live inside an IO. It is configured at the advertiser level and
  shared from Campaign Manager 360; conversions then attribute to line items.

## Sources

- [Partners in Display & Video 360](https://support.google.com/displayvideo/answer/7622449?hl=en) (as of June 2026)
- [Advertisers in Display & Video 360](https://support.google.com/displayvideo/answer/2696883?hl=en) (as of June 2026)
- [Create an insertion order](https://support.google.com/displayvideo/answer/2696705?hl=en) (as of June 2026)
- [Create a line item](https://support.google.com/displayvideo/answer/2891312?hl=en) (as of June 2026)
- [About Floodlight and Floodlight activities (DV360)](https://support.google.com/displayvideo/answer/3027419?hl=en) (as of June 2026)
- [Create a Floodlight activity](https://support.google.com/displayvideo/answer/2697097?hl=en) (as of June 2026)
