---
name: amazon-dsp-account-structure
description: Understand and lay out the Amazon DSP entity hierarchy. Use when the user asks about Amazon DSP account structure, the Amazon DSP hierarchy, advertiser vs order vs line item, order vs line item, managed vs self-service DSP, DSP seats, line item or product types (display, video, streaming TV, audio), the Amazon Ads pixel, conversion events, or where budget, flight, and goals live in Amazon DSP.
---

# Amazon DSP account structure

Map a programmatic media plan onto the Amazon DSP hierarchy: advertiser, then order, then line
item. Getting the hierarchy right up front decides whether budget control, pacing, optimization,
and reporting behave once the buy is live, because each level owns a fixed set of settings that
the levels below inherit. Restructuring a live order is expensive, so structure deliberately.

Amazon DSP is Amazon's programmatic demand-side platform for display, video, audio, and streaming
TV across Amazon properties (Prime Video, Twitch, Fire TV, Amazon.com, Freevee) and third-party
exchanges. It is distinct from Amazon Ads sponsored ads (Sponsored Products, Sponsored Brands,
Sponsored Display), which are self-service retail-search ads keyed to keywords and ASINs and are
not part of the DSP. This skill covers the DSP only. When someone says "Amazon DSP campaign," they
mean an order; "campaign" is the colloquial word, "order" is the entity.

This skill assumes you know what a CPM, a flight, frequency, and a funnel stage are. For KPI
definitions and shared programmatic math, see the `programmatic-foundations` skill.

## When to use this skill

- "What is the Amazon DSP account structure / hierarchy?"
- "Order vs line item, what is the difference?" / "Is an order the campaign?"
- "Managed service or self-service DSP, which do I need?"
- "What line item or product types does Amazon DSP have?" / "display vs video vs STV vs audio"
- "What is the Amazon Ads pixel?" / "Where do conversion events get defined?"
- "Where do budget, flight dates, and the optimization goal live?"

Boundaries with sibling skills:
- Step-by-step build of an order and its line items: hand off to `amazon-dsp-campaign-setup`.
- Audience construction and segments: hand off to `amazon-dsp-audiences`.
- Supply, exchanges, deals, PMP/PG: hand off to `amazon-dsp-inventory-and-supply`.
- Bid and optimization-goal mechanics: hand off to `amazon-dsp-bidding-and-optimization`.
- Creative specs and ad formats: hand off to `amazon-dsp-creative-and-formats`.
- Pixel-based and Amazon-conversion reporting, attribution windows: hand off to
  `amazon-dsp-measurement-and-reporting`, and see the `reporting-by-campaign-goal` skill for which
  metrics to report against which objective.
- API and bulk management of the same objects: hand off to `amazon-dsp-api-and-automation`.

## Quick reference

The hierarchy, top to bottom:

```
Seat / account     your DSP access; managed-service or self-service; one or more advertisers
  Advertiser       one real brand; owns creatives, audiences, pixels, conversion events, brand
    Order          the campaign-level container: budget, flight, overall goal, default settings
      Line item    the buy: supply + targeting + bid + creative; budget and flight within the order
        Creative   the ad served, assigned at the line item
```

Pixels and conversion events are configured at the advertiser level and shared down to every order
and line item under that advertiser, the same way Floodlight sits at the advertiser level in DV360.

What each level owns:

| Level | Owns | You create a new one when |
| --- | --- | --- |
| Advertiser | Brand identity, creatives, audiences, pixels, conversion events, billing entity | A separate brand or legal billing entity is involved |
| Order | Total budget, flight dates, budget caps, overall optimization goal, default frequency, order-level supply and audience defaults | The money, the dates, or the campaign objective differ |
| Line item | Supply (inventory and deals), targeting layered on the order, bid and pacing, optimization within the order goal, creative assignment, line-item budget and flight | The supply, audience, bid, format, or creative set differ |

## Core process

1. Confirm you are in the DSP, not sponsored ads. If the work is keyword or ASIN bidding inside
   search results, it is Sponsored Products / Brands / Display and a different toolset, not this.
2. Pick the seat model. Managed-service if you want Amazon to operate the buy or you cannot meet
   self-service onboarding; self-service if your team operates the console directly. This decides
   who builds and who has console access, not the hierarchy itself. See the rules below.
3. Set up or identify the advertiser for the brand. The advertiser is where creatives, audiences,
   the pixel, and conversion events live, so everything reusable attaches here once.
4. Define the pixel and conversion events at the advertiser level before building orders, so line
   items can optimize toward and report on those events from day one (off-Amazon conversions need
   a pixel or an approved measurement integration; on-Amazon conversions use Amazon signals).
5. Create one order per distinct budget, flight, and objective. The order is the only level that
   holds a total budget and flight and a single overall goal, so each of those that must stand
   alone needs its own order.
6. Inside each order, create line items by supply and targeting and creative. The line item is the
   buy unit, so any axis you want to bid, pace, target, or report independently becomes a line item.
7. Choose each line item's product type (standard display, online video, streaming TV, audio) to
   match the inventory and creative. Type drives available supply, creative specs, and bidding.
8. Hand off the detailed build to `amazon-dsp-campaign-setup`, audiences to `amazon-dsp-audiences`,
   and supply to `amazon-dsp-inventory-and-supply`.

## Decision rules and thresholds

### Managed-service vs self-service

- Choose self-service when your team will operate the console, you want no separate management fee
  on media, and you can complete self-service onboarding. You build and control everything directly.
- Choose managed-service when you want Amazon's team to plan and run the buy consultatively, or your
  team lacks programmatic operating capacity. Managed-service carries a spend minimum (commonly cited
  at 50,000 USD, and the minimum varies by country), so confirm the current threshold for your market
  in the Amazon Ads console or with your Amazon representative before committing.
- The hierarchy (advertiser, order, line item) is identical either way. The difference is who has the
  console seat and who executes, not the object model. A self-service seat can still get consultative
  support; the spend minimum is the practical dividing line.

### When to split ORDERS

Each of these forces a separate budget, flight, or overall goal, which only an order can hold.

- Objective. Awareness, consideration, and performance carry different goals and budgets. Keep them
  in separate orders so one goal does not constrain the other and reporting stays clean.
- Distinct budget or flight. Any line items that must not share a budget pool or start and end date
  belong in separate orders. Line items inside one order draw on the order's budget and flight.
- Channel mix when budgets are managed separately. If streaming TV and display each need their own
  committed budget and pacing, separate orders make that control explicit.
- Market or region when budgets, currency, or reporting are managed independently.
- Reporting or billing line. If finance or the client needs a clean budget line for a slice of the
  buy, give that slice its own order.

### When to split LINE ITEMS

Each of these is an axis you want to target, bid, optimize, or report on independently within the
order's budget and goal.

- Supply or deal. A specific deal (PMP or programmatic guaranteed) belongs in its own line item,
  separate from open-exchange supply, so delivery and pricing are visible and controllable.
- Product type. Display, online video, streaming TV, and audio are different line item types with
  different creatives and bidding; they cannot share one line item.
- Audience strategy. Prospecting versus retargeting, or distinct segments, so bids and budgets do
  not bleed across intent levels.
- Creative set. A line item serves its assigned creatives, so a different message, offer, or format
  needs its own line item for clean rotation and reporting.
- Bid or pacing rule. A different bid, optimization emphasis, or frequency goal for a slice.

Do not over-split. Every extra line item fragments conversion volume, which slows optimization (see
`amazon-dsp-bidding-and-optimization`). Split only where you will act on the distinction; if two
slices would always get the same supply, bid, targeting, and creative, merge them.

### Line item / product types

- Standard display. Image and responsive e-commerce creative across Amazon and third-party display
  supply. Amazon consolidated desktop, mobile web, and mobile app display into one standard display
  line item, so you no longer build three separate line items to cover those display channels.
- Online video (OLV). In-stream and out-stream video across web and app supply.
- Streaming TV (STV). Video on connected TV and premium streaming supply (Prime Video, Freevee,
  Twitch, Fire TV, and partner apps). Non-skippable, full-screen, measured on video completion.
- Audio. Audio ads across streaming audio supply, including Amazon Music's ad-supported tier.

Match the type to the inventory and creative you actually have. Type determines available supply,
creative specs, and which bidding and optimization goals apply.

## Where budget, flight, and goals live

- Total budget and budget caps: the order. The order's budget is the pool the line items spend
  against; line item budgets, if set, partition that pool.
- Flight (start and end dates): the order sets the campaign window; line items can run for the full
  order flight or a sub-window inside it, never outside it.
- Overall optimization goal and KPI: the order. Line items optimize within that goal and can carry
  their own bid and pacing emphasis.
- Frequency: a default cap can sit at the order and be tightened per line item.
- Targeting and supply: layered. Order-level defaults apply to its line items, and each line item
  adds or narrows supply, audience, and other targeting on top.

## Pixels and conversion events

- The Amazon Ads pixel (advertiser pixel) is a tag placed on advertiser-owned pages to record
  off-Amazon events (page view, purchase, sign-up, custom events). It is created and managed at the
  advertiser level, so every order and line item under that advertiser can optimize toward and report
  on those events. Pixels must follow Amazon's pixeling policy, and a vendor or ad server must be
  certified to place pixels or drop tags on Amazon pages.
- Conversion events define what counts as a conversion. Off-Amazon conversions come from the pixel
  or an approved measurement integration; on-Amazon conversions (detail page views, purchases,
  add-to-cart, brand-new-to-brand) come from Amazon retail signals and do not need a pixel.
- Amazon renamed the older "Pixel" metric category to "Off-Amazon," because those metrics now include
  conversions from non-pixel interfaces as well. Read column groups as "Off-Amazon" versus on-Amazon
  rather than "pixel versus not."
- For attribution windows, modeled conversions, and which conversion metric to optimize and report
  against, hand off to `amazon-dsp-measurement-and-reporting` and `reporting-by-campaign-goal`.

Set pixels and conversion events at the advertiser level before launching orders, so optimization
has signal from the first impression. Retrofitting conversion tracking after launch loses early data.

## Templates and examples

A brand running an upper-funnel STV push plus a lower-funnel display retargeting buy:

```
Advertiser: ACME (pixel + purchase/sign-up conversion events configured here)
  Order: ACME_STV_Awareness_2026Q3        (own budget, flight, reach/video-completion goal)
    Line item: ACME_STV_Prospecting_PrimeVideo_2026Q3   (STV type, Amazon premium video supply)
    Line item: ACME_STV_Prospecting_3PApps_2026Q3       (STV type, third-party app supply)
  Order: ACME_Display_Performance_2026Q3  (separate budget, flight, conversion goal)
    Line item: ACME_Display_Retargeting_Standard_2026Q3 (standard display, retargeting audience)
    Line item: ACME_Display_Deal_PMP_2026Q3             (standard display, a specific PMP deal)
```

Why it splits this way: awareness and performance are separate orders because they carry different
budgets, flights, and goals. STV and display are different product types, so they are different line
items. Prospecting versus retargeting and open-exchange versus the PMP deal are separate line items
because you want to bid, pace, and read them independently. The pixel and conversion events sit once
at the advertiser and feed both orders.

## Common pitfalls

- Confusing Amazon DSP with sponsored ads. Sponsored Products / Brands / Display are retail-search
  self-service ads and have no order or line item hierarchy. If the request is about keywords or
  ASIN targeting in search results, it is not a DSP task.
- Treating the order as just a folder. The order holds the budget, flight, and overall goal; line
  items cannot exceed its budget or run outside its flight. Plan budget and dates at the order.
- Building separate display line items per device. Standard display now covers desktop, mobile web,
  and mobile app in one line item; splitting by device fragments delivery without benefit.
- Setting up the pixel after launch. Conversion events live at the advertiser and feed optimization;
  add them before the first impression or the early flight optimizes blind.
- Over-splitting line items so no single line item gets enough conversions to optimize. Consolidate
  slices you will not act on separately.
- Assuming managed-service changes the structure. It changes who operates the seat, not the
  advertiser, order, line item model.

## Sources

- [Amazon DSP: Advertise with a demand-side platform](https://advertising.amazon.com/solutions/products/amazon-dsp) (as of June 2026)
- [What is a demand-side platform? A complete guide](https://advertising.amazon.com/library/guides/demand-side-platform) (as of June 2026)
- [Amazon Ads API overview](https://advertising.amazon.com/about-api) (as of June 2026)
- [Amazon DSP APIs developer guide](https://advertising.amazon.com/API/docs/en-us/guides/dsp/developer-guide) (as of June 2026)
- [Simplified display line items (single standard display line item)](https://advertising.amazon.com/resources/whats-new/display-line-item-consolidation) (as of June 2026)
- [Amazon Pixeling Guidelines (ad policy)](https://advertising.amazon.com/resources/ad-policy/pixeling-policy) (as of June 2026)

Some Amazon Ads detail (managed-service spend minimums, exact pixel and conversion-event setup steps,
attribution windows) lives in login-gated console help such as the "Create an Amazon DSP campaign" and
"Conversion tracking" pages in the Amazon Ads Support Center. Where a number or step is not on a public
page, confirm it in the Amazon Ads console or Support Center for your market rather than relying on a
remembered figure.
