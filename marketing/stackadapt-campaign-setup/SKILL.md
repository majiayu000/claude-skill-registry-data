---
name: stackadapt-campaign-setup
description: Build a StackAdapt campaign and its ad groups end to end. Use when the user wants to set up a StackAdapt campaign, create a StackAdapt ad group, launch a native campaign on StackAdapt, or asks for the StackAdapt campaign setup flow and the decision at each step (channel, objective, budget, flight, pacing, bid, targeting, creatives).
---

# StackAdapt campaign setup

Take a media plan and turn it into a live StackAdapt campaign with correctly configured ad
groups. StackAdapt is a self-serve multi-channel demand-side platform, strongest in native and
also running display, video, connected TV, audio, in-app, and digital out-of-home. This skill
is the build flow and the decision at each step. It assumes the structure is already decided.

If you are not yet sure how many campaigns and ad groups you need, or what the hierarchy is,
start with `stackadapt-account-structure`. For KPI definitions and shared math, see the
`programmatic-foundations` skill.

## When to use this skill

- "Set up a StackAdapt campaign for me." / "Walk me through StackAdapt campaign setup."
- "Create a StackAdapt ad group."
- "Launch a native campaign on StackAdapt."
- "What do I pick at each step when building a campaign?"

Boundaries with sibling skills. Each step below points to the sibling that owns the deep
decision, so this skill stays the spine and does not duplicate them:
- Hierarchy, campaign-vs-ad-group, and where settings live: `stackadapt-account-structure`.
- Targeting and audience construction: `stackadapt-targeting-and-audiences`.
- Bid approach, budget sizing, and pacing detail: `stackadapt-bidding-and-budgets`.
- Inventory selection and brand-safety controls: `stackadapt-inventory-and-brand-safety`.
- Reporting setup and attribution windows: `stackadapt-reporting-and-attribution`.
- In-flight optimization and fixing under-delivery: `stackadapt-optimization-and-troubleshooting`.
- Building many campaigns or ad groups in bulk by API: `stackadapt-api-and-automation`.

## Quick reference

The build order, and the one decision each step turns on:

| Step | Set at | The decision |
| --- | --- | --- |
| 1. Channel | Campaign | Which channel matches the goal: native, display, video, CTV, audio, in-app, DOOH |
| 2. Objective | Campaign | What outcome the buy optimizes toward: awareness, traffic/engagement, or conversions |
| 3. Create ad group(s) | Ad group | One ad group per axis you will budget, pace, bid, target, or report independently |
| 4. Budget | Ad group | Total or daily budget for that ad group; the ad group is the budget container |
| 5. Flight | Ad group | Start and end dates for that ad group |
| 6. Pacing | Ad group | Even (spread spend) vs accelerated (spend as fast as auctions allow) |
| 7. Bid approach | Ad group | Fixed CPM/CPC/CPE vs automated/target CPA, matched to the objective |
| 8. Targeting | Ad group | Geo, audience, contextual, device, schedule; the audience this ad group buys |
| 9. Inventory + brand safety | Ad group | Inventory lists, supply, and safety controls the ad group runs against |
| 10. Creatives | Ad / Creative | Assets in the channel's format, assigned to the ad group |
| 11. Pre-launch review | All | Verify budgets, dates, pixel, targeting, creatives, then submit |

Remember the structural fact from `stackadapt-account-structure`: the **ad group is the line
item**. Steps 4 through 10 all happen at the ad group, repeated for each ad group in the
campaign.

## Core process

1. Pick the channel (campaign level). Choose the channel that matches the goal and the
   creative you have. Native suits content-led prospecting and in-feed engagement; CTV and
   video suit awareness and reach; display suits broad retargeting and ABM; audio suits
   screen-free reach; DOOH suits location-based presence. The channel constrains the formats,
   inventory, and bid units available downstream, so it is the first commitment.
2. Pick the objective (campaign level). Set what the campaign optimizes toward: awareness and
   reach, traffic or engagement, or conversions. The objective shapes which bid approaches make
   sense at step 7 and which metrics matter in reporting. A conversion objective only works if
   the pixel and its events are live (see `stackadapt-account-structure`).
3. Create the ad group(s). Add one ad group per axis you decided to separate in
   `stackadapt-account-structure`: prospecting vs retargeting, distinct audiences, distinct
   inventory, distinct budgets or flights. Everything from here is per ad group.
4. Set the budget (ad group). Give each ad group its own total or daily budget. The ad group is
   the budget container, so this is where money is controlled, not the campaign. For sizing
   relative to the bid and the learning needs of automated bidding, see
   `stackadapt-bidding-and-budgets`.
5. Set the flight (ad group). Set start and end dates per ad group. Ad groups in one campaign do
   not have to share dates.
6. Set pacing (ad group). Choose even pacing to spread budget across the flight (the default for
   most always-on and brand work) or accelerated to capture volume as fast as auctions allow
   (use for short bursts or time-sensitive pushes, and watch for early budget exhaustion). Deep
   guidance lives in `stackadapt-bidding-and-budgets`.
7. Choose the bid approach (ad group). Match the bid to the objective. Use a fixed bid
   (CPM, CPC, or cost per engagement) when you want hard control over price, when volume is too
   low for automation to learn, or at launch before there is conversion signal. Use an automated
   or target-CPA approach when the objective is conversions and the pixel is feeding enough
   events for the model to learn. The full decision and target-setting live in
   `stackadapt-bidding-and-budgets`; hand off there rather than guessing a target.
8. Set targeting (ad group). Layer geo, audience (retargeting, lookalike, first-party,
   third-party segments), contextual, device, and dayparting. On native, contextual and
   first-party audiences are the workhorses; for retargeting, use audiences built from the
   universal pixel. Construction detail and the order to layer signals live in
   `stackadapt-targeting-and-audiences`. Do not over-narrow, which starves delivery.
9. Set inventory and brand safety (ad group). Attach inventory lists, choose supply and
   exchanges, and apply brand-safety and viewability controls appropriate to the channel and
   the client's risk tolerance. This is owned by `stackadapt-inventory-and-brand-safety`; apply
   it per ad group so different audiences can run against different supply.
10. Add creatives (ad / creative). Upload or build assets in the channel's format and assign
    them to the ad group. Native needs headline, body, image or video, and a call to action;
    display needs the banner set; video and CTV need the video file and companion where used;
    audio needs the audio file and optional companion display; DOOH needs screen-appropriate
    creative. Assign at least two creatives per ad group where possible so rotation has
    something to optimize. Confirm each creative carries the right click and tracking setup.
11. Review before launch. Walk the pre-launch checklist below, then submit. New campaigns and
    creatives typically pass through a review before they serve, so submit with enough lead time
    before the flight start.

## Decision rules and thresholds

- One channel per campaign. The channel is a campaign-level setting and drives formats and
  inventory, so do not try to mix channels in one campaign. Split by channel.
- One ad group per independently managed slice. Budget, flight, bid, audience, and inventory all
  live on the ad group, so any of those differing means a new ad group. If two slices would get
  the same budget, bid, audience, and inventory, merge them.
- Match the bid to the objective and the signal. Conversions objective plus enough pixel events
  to learn means an automated or target-CPA bid is on the table. Awareness, low volume, or a
  cold launch means start with a fixed bid and revisit once data accrues.
- Pacing follows the goal. Even pacing for always-on, brand, and steady delivery. Accelerated
  only for short, time-boxed pushes, and monitor for early exhaustion.
- Targeting wide enough to deliver. Each added targeting layer shrinks the addressable pool.
  Confirm the combination can still spend the budget across the flight before launch; if not,
  loosen a layer or lower the budget.
- At least two creatives per ad group where the format allows, so rotation and optimization have
  options. A single creative cannot be optimized against anything.
- Pixel before a conversion objective. A conversion-optimized campaign with no live pixel events
  has nothing to learn from. Verify the pixel and events first.

## Pre-launch checklist

Walk this before submitting. Catching a problem here is free; catching it after spend is not.

- Channel and objective on the campaign match the brief.
- Every ad group has a budget, a start and end date, and a pacing setting.
- The bid approach on each ad group matches the objective, and any target is sane for the goal.
- Targeting on each ad group is correct and wide enough to deliver the budget across the flight.
- Inventory and brand-safety controls are attached per ad group.
- Each ad group has its creatives assigned, in the right format, with working click and tracking
  setup, ideally two or more for rotation.
- For a conversion objective, the universal pixel is live and the conversion events exist (see
  `stackadapt-account-structure`).
- Names follow the controlled convention so reporting and bulk edits work.
- Submitted with enough lead time for creative and campaign review before the flight start.

## Templates and examples

A native consideration campaign with prospecting and retargeting ad groups, filled in:

```
Campaign: ACME_Native_Consideration_2026Q3
  Channel:   Native
  Objective: Traffic / engagement

  Ad group: ACME_Native_Consideration_Prospecting_Contextual_2026Q3
    Budget:    $12,000 total over the flight
    Flight:    2026-07-01 to 2026-09-30
    Pacing:    Even
    Bid:       Fixed CPC, hand off target to stackadapt-bidding-and-budgets
    Targeting: US, contextual categories + first-party segment, all devices
    Inventory: standard native supply + brand-safety list (see inventory skill)
    Creatives: 3 native units (headline + body + image + CTA), rotating

  Ad group: ACME_Native_Consideration_Retargeting_PixelAud_2026Q3
    Budget:    $5,000 total over the flight
    Flight:    2026-07-01 to 2026-09-30
    Pacing:    Even
    Bid:       Target CPA (pixel events live), set target with bidding skill
    Targeting: US, site-visitor audience built from the universal pixel, 30-day window
    Inventory: same native supply + brand-safety list
    Creatives: 2 native units with a returning-visitor offer, rotating
```

Why it is built this way: native and a traffic objective at the campaign level; two ad groups
because prospecting and retargeting need different budgets, bids, audiences, and you want to
read them apart; the retargeting ad group can run a target CPA because the pixel is already
feeding events, while prospecting starts on a fixed CPC until there is signal.

## Common pitfalls

- Setting budget or flight on the campaign and expecting it to control spend. Those live on the
  ad group on StackAdapt. Configure them per ad group.
- Picking a conversion objective or a target-CPA bid before the pixel is live or before there
  are enough events to learn. Start fixed, switch once signal exists.
- Stacking so many targeting layers that the ad group cannot spend its budget. Verify
  deliverability against the flight, then loosen if needed.
- One creative per ad group, leaving rotation and optimization nothing to work with. Load two or
  more where the format allows.
- Submitting at the flight start with no buffer for review. Build and submit ahead so review
  clears before go-live.
- Reinventing targeting, bidding, inventory, or reporting choices here. Those are owned by the
  sibling skills named above. This skill is the order of operations; hand off for the depth.

## Sources

- [StackAdapt Developer Documentation (REST, GraphQL, Pixel API, Data Taxonomy, MCP Server)](https://docs.stackadapt.com) (as of June 2026)
- [Native Advertising | StackAdapt](https://www.stackadapt.com/native-advertising) (as of June 2026)
- [Display Advertising | StackAdapt](https://www.stackadapt.com/display-advertising) (as of June 2026)
- [Video Advertising | StackAdapt](https://www.stackadapt.com/video-advertising) (as of June 2026)
- [Connected TV Advertising | StackAdapt](https://www.stackadapt.com/connected-tv) (as of June 2026)
- [Programmatic Audio Advertising | StackAdapt](https://www.stackadapt.com/programmatic-audio) (as of June 2026)
- [Digital Out-of-Home Advertising | StackAdapt](https://www.stackadapt.com/digital-out-of-home-advertising) (as of June 2026)

The exact in-product setup screens, the campaign and creative review timing, and field-level
defaults are documented in the StackAdapt help center at support.stackadapt.com. Some help
center articles require a logged-in account, so they are not cited as sources here; the
step-level pacing, bid, targeting, and inventory decisions are covered by the sibling skills
named throughout, and where a specific in-product default is not publicly documented the
guidance above states the operational best practice rather than a fabricated citation.
