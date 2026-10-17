---
name: stackadapt-account-structure
description: Understand how a StackAdapt account is organized and where every setting lives. Use when the user asks about StackAdapt account structure, the StackAdapt hierarchy, StackAdapt campaign vs ad group, what an ad group is on StackAdapt, the StackAdapt conversion pixel, which channels StackAdapt runs (native, display, video, connected TV, audio, in-app, digital out-of-home), or where account-level settings and conversions sit.
---

# StackAdapt account structure

Map how StackAdapt organizes a buy so campaigns, ad groups, ads, and conversion tracking are
laid out in a way that reporting, pacing, and optimization hold up later. StackAdapt is a
self-serve multi-channel demand-side platform best known for native advertising, and it also
runs display, video, connected TV, audio, in-app, and digital out-of-home from the same
account. Getting the structure right up front is the cheapest lever you have. Reworking it
after a campaign is live costs spend and learning.

This skill assumes you know what a CPM, a flight, and a funnel stage are. For KPI definitions
and shared math, see the `programmatic-foundations` skill.

## When to use this skill

- "What is the StackAdapt hierarchy?" / "How is a StackAdapt account organized?"
- "What is the difference between a campaign and an ad group on StackAdapt?"
- "What does an ad group control on StackAdapt?"
- "Which channels can I run on StackAdapt?"
- "What is the StackAdapt pixel and where does it live?" / "How does conversion tracking work?"
- "Where do account-level settings sit?"

Boundaries with sibling skills:
- Building a campaign and ad groups step by step: hand off to `stackadapt-campaign-setup`.
- Targeting and audience construction: hand off to `stackadapt-targeting-and-audiences`.
- Bid approach, budget, and pacing choices: hand off to `stackadapt-bidding-and-budgets`.
- Inventory selection and brand safety controls: hand off to `stackadapt-inventory-and-brand-safety`.
- Reporting and attribution windows: hand off to `stackadapt-reporting-and-attribution`.
- Programmatic API and bulk automation: hand off to `stackadapt-api-and-automation`.

## Quick reference

The hierarchy, top to bottom:

```
Account / Workspace   the login boundary; holds users, the pixel, audiences, billing, brands
  Campaign            the channel + objective container; holds the overall intent of the buy
    Ad Group          the line item level; holds budget, flight, pacing, bid, targeting, inventory
      Ad / Creative   the asset that serves; assigned to and rotates within the ad group
```

The single fact that drives every structural decision: on StackAdapt the **ad group is the
line item**. Budget, flight dates, pacing, the bid, targeting, and inventory all live at the
ad group, not the campaign. The campaign above it is mostly a channel-and-objective grouping
and a reporting roll-up. So anything that needs its own budget, schedule, bid, audience, or
inventory list becomes its own ad group.

What each level decides:

| Level | Owns | You change it when |
| --- | --- | --- |
| Account / Workspace | Users and permissions, the conversion pixel, saved audiences, billing, brand entities, account defaults | Rarely. This is governance, not per-campaign work |
| Campaign | Channel, objective/optimization intent, the overall grouping that ad groups inherit | The channel or the objective of the buy differs |
| Ad group | Budget, flight dates, pacing, bid (CPM/CPC/CPE/target CPA), targeting, inventory and brand-safety lists, frequency | The money, dates, bid, audience, format, or inventory differ |
| Ad / Creative | The served asset and its tracking | The message, offer, format, or size differs |

## Core process

1. Start from the media plan, not the user interface. List every distinct combination of
   channel, objective, budget, flight, audience, and inventory. Each distinct budget-and-flight
   cell is a candidate ad group, because the ad group is the only level that holds a budget and
   dates.
2. Group ad groups under campaigns by channel and objective. One campaign carries one channel
   and one optimization intent, so native prospecting and CTV awareness are separate campaigns.
3. Inside each campaign, break out ad groups by any axis you want to budget, pace, bid, target,
   or report on independently. The ad group is the line item, so that is where the split happens.
4. Assign ads and creatives to each ad group in the format the channel requires (native assets,
   display banners, video, audio, or DOOH creative). Creatives rotate within the ad group.
5. Install the StackAdapt conversion pixel once at the account level before launch, and define
   the conversion events you will optimize toward, so attribution and optimization work from day
   one. See conversion pixel below.
6. Name every object with the structured convention below before you build, so reporting,
   filtering, and bulk edits work from the start.
7. Hand off targeting to `stackadapt-targeting-and-audiences`, bid and budget to
   `stackadapt-bidding-and-budgets`, and inventory and brand safety to
   `stackadapt-inventory-and-brand-safety`.

## Channels available

StackAdapt runs these channels from one account. The channel is chosen at the campaign level
and constrains the formats, inventory, and bid units available to the ad groups beneath it.

- Native. In-feed, in-ad, and content-recommendation placements that match the look of the
  surrounding page. This is the platform's flagship channel and supports native video and
  outstream.
- Display. Static banners, rich media, HTML5, in-banner video, and interactive units across
  web and app.
- Video. In-stream, native video, native outstream, and interstitial across desktop, mobile,
  and app.
- Connected TV (CTV). Streaming inventory with pod-level controls and creative transcoding;
  measured with cross-device attribution.
- Audio. Streaming music, podcasts, and audiobooks with non-skippable formats and optional
  companion display.
- In-app / in-game. Display and video formats inside mobile and PC apps and games.
- Digital out-of-home (DOOH). Programmatic placements on digital screens, planned by location,
  venue type, and timing signals rather than by individual user.

Because all channels share one account, the same audiences and the same conversion pixel work
across them, which is what makes cross-channel retargeting and a single conversion view
possible. Lean on this when planning omnichannel: build the audience and pixel once, then run
ad groups against them on whichever channels fit the goal.

## The StackAdapt conversion pixel

Conversion tracking on StackAdapt runs through a single account-level pixel, sometimes called
the universal pixel. It is the backbone of both measurement and optimization, so treat it as
launch-blocking.

How it works in practice:

- The pixel is created and managed at the account or workspace level, not inside a campaign or
  ad group, so every campaign in the account can attribute to it and every ad group can
  optimize toward its events. Place the base pixel sitewide once.
- On top of the base pixel you define conversion events (for example a page load on a
  thank-you or purchase-confirmation page, or a specific action). Each event carries a
  conversion category so reporting and optimization can tell a lead from a purchase.
- The same pixel powers retargeting and lookalike audiences. Visitors it observes become
  audiences you can target or model from, which is why it must be live before you build
  prospecting-plus-retargeting structures.
- For server-side or cookieless setups, StackAdapt also offers a server-to-server pixel path
  through its Pixel API, so conversions can be reported without a browser-side tag. Reach for
  this when a client requires server-side tagging or a clean-room style integration.

When you then choose a conversion-based bid (for example a target CPA) on an ad group, it
optimizes toward the pixel events you defined here. Define the events first, then build the ad
groups that chase them. For event setup mechanics and step-by-step pixel installation, see the
StackAdapt help center; for the server-side path, see the StackAdapt developer documentation.

## Where account-level settings live

These are set once at the account or workspace level and inherit down. Confirm them before
your first campaign rather than per buy:

- Users, roles, and permissions.
- The conversion pixel and its conversion events.
- Saved and shared audiences (retargeting, lookalike, first-party, third-party data segments).
- Brand entities and any brand-level defaults.
- Billing, currency, and account-level pacing or spend defaults.

Anything that should be reused across many campaigns belongs here. Anything specific to one
slice of the buy belongs on the ad group.

## Naming convention

Consistent, structured names are what make reporting, filtering, and bulk edits work, because
report filters and bulk operations key off the name string. Use a delimited template and keep
it identical across every object.

Recommended fields, in order: client/brand, channel, objective, funnel stage, audience, flight.

Rules:
- Use a single, consistent delimiter (an underscore works well). Pick one and never mix.
- Avoid special characters, leading or trailing spaces, and commas, which break CSV-based bulk
  workflows and report filters.
- Encode the same fields in the same order on every campaign and ad group so a wildcard filter
  isolates exactly the slice you want.
- Keep values from a controlled vocabulary (fixed channel codes, stage codes, audience codes)
  so filters match. Free-text values defeat the purpose.

Example campaign name:
`ACME_Native_Consideration_MidFunnel_2026Q3`

Example ad group names under it:
`ACME_Native_Consideration_MidFunnel_Prospecting_Contextual_2026Q3`
`ACME_Native_Consideration_MidFunnel_Retargeting_PixelAud_2026Q3`

## Templates and examples

A native-plus-CTV omnichannel plan, prospecting and retargeting, mapped onto the hierarchy:

```
Account: ACME (one universal pixel, shared audiences live here)
  Campaign: ACME_Native_Consideration_2026Q3        (channel = native, objective = consideration)
    Ad group: ..._Prospecting_Contextual_2026Q3      (own budget, flight, CPC bid, contextual targeting)
    Ad group: ..._Retargeting_PixelAud_2026Q3        (separate budget, target CPA, pixel-built audience)
  Campaign: ACME_CTV_Awareness_2026Q3                (channel = CTV, objective = awareness)
    Ad group: ..._Prospecting_Demo_2026Q3            (separate budget, CPM bid, demo + geo targeting)
```

Why it splits this way: native and CTV are separate campaigns because the channel and objective
differ and each channel constrains its own formats and inventory. Prospecting and retargeting
are separate ad groups because they need different budgets, bids, audiences, and you want to
read them apart. The retargeting audience and the universal pixel are defined once at the
account level and reused across both campaigns.

## Common pitfalls

- Treating the campaign as the budget container. On StackAdapt the budget, flight, and bid live
  on the ad group. Setting up one fat campaign and expecting to pace it as a unit does not match
  the model. Split into ad groups.
- Mixing channels under one campaign. The channel is set at the campaign level and drives
  available formats and inventory, so a campaign is single-channel by design. Use separate
  campaigns per channel.
- Launching before the pixel is live. Conversion-based bidding has nothing to optimize toward
  and retargeting pools start empty. Place the universal pixel and define events first.
- Over-splitting ad groups so finely that no single ad group gets enough conversions for a
  conversion-based bid to learn (see `stackadapt-bidding-and-budgets` on learning). Split only
  where you will act on the distinction.
- Free-text or special characters in names. They break bulk round-trips and report filters.
  Lock a delimited template and a controlled vocabulary before building.

## Sources

- [StackAdapt Developer Documentation (REST, GraphQL, Pixel API, Data Taxonomy, MCP Server)](https://docs.stackadapt.com) (as of June 2026)
- [Native Advertising | StackAdapt](https://www.stackadapt.com/native-advertising) (as of June 2026)
- [Display Advertising | StackAdapt](https://www.stackadapt.com/display-advertising) (as of June 2026)
- [Video Advertising | StackAdapt](https://www.stackadapt.com/video-advertising) (as of June 2026)
- [Connected TV Advertising | StackAdapt](https://www.stackadapt.com/connected-tv) (as of June 2026)
- [Programmatic Audio Advertising | StackAdapt](https://www.stackadapt.com/programmatic-audio) (as of June 2026)
- [In-Game Advertising | StackAdapt](https://www.stackadapt.com/in-game-advertising) (as of June 2026)
- [Digital Out-of-Home Advertising | StackAdapt](https://www.stackadapt.com/digital-out-of-home-advertising) (as of June 2026)

For step-by-step pixel installation, conversion-event setup, and account administration screens,
see the StackAdapt help center at support.stackadapt.com. Some help center articles require a
logged-in account, so they are not cited above; the developer documentation covers the
server-side Pixel API path publicly.
