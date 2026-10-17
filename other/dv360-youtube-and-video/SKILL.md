---
name: dv360-youtube-and-video
description: Buy YouTube and video in Display & Video 360. Use when the user asks about YouTube on DV360, DV360 video, TrueView, skippable vs non-skippable, bumper ads, in-feed or Shorts ads, CPV and what counts as a view, target CPV, a video reach campaign, efficient reach, target frequency, non-skippable reach, ad sequencing, video action, YouTube on connected TV, YouTube Select lineups, Google video partners, or how to buy YouTube programmatically.
---

# DV360 YouTube and video

Set up and bid the YouTube and partners line item family in Display & Video 360: pick the
objective and subtype, choose the right format, and bid it the way YouTube bills instead of
the way display bills. This is the line item family that other DV360 skills hand off to. It
buys YouTube, Google video partners, and YouTube on connected TV, and it behaves differently
from standard display, video, and audio line items in structure, formats, bidding, and
targeting.

This skill assumes you know CPM, CPV, CPA, reach, and frequency. For KPI math see the
`programmatic-foundations` skill. For where the line item sits in the account hierarchy see
`dv360-campaign-architecture`.

## When to use this skill

- "How do I buy YouTube on DV360?" / "Buy YouTube programmatically."
- "Skippable vs non-skippable?" / "When do I use bumper ads / in-feed / Shorts?"
- "What is CPV / TrueView?" / "What counts as a view?"
- "Set up a video reach campaign." / "Efficient reach, target frequency, or non-skippable reach?"
- "How does target frequency work?" / "What frequency can I target?"
- "Set up ad sequencing." / "YouTube video action / drive conversions on YouTube."
- "Buy YouTube on connected TV." / "YouTube Select lineups." / "Google video partners."

Boundaries with sibling skills:
- The bid strategy decision in general (fixed vs automated, learning periods): `dv360-bid-strategy`.
  This skill covers the YouTube-specific strategies (target CPV, target CPM on reach products).
- Audience construction and the full targeting taxonomy: `dv360-targeting-and-audiences`.
  This skill covers how targeting behaves on the three-tier YouTube line item.
- Reach and frequency goal-setting and media-mix planning across channels:
  `reach-and-frequency-planning`. This skill covers the YouTube buying products that deliver
  against those goals.
- Conversion tracking, view-through, and attribution windows: `dv360-measurement-and-attribution`.
- Where the line item lives and how many to create: `dv360-campaign-architecture`.
- Deal-based YouTube buys (instant deals, programmatic guaranteed): `dv360-deals-and-inventory`.

## Quick reference

YouTube and partners line items carry an extra layer that standard line items do not: the ad
group. One line item holds one or more ad groups, and each ad group holds one or more YouTube
ads. Targeting is set at three levels (advertiser, line item, ad group), and line item
targeting flows down to every ad group and cannot be overridden lower.

Pick the line item by objective, then subtype:

| Objective | Subtype | What it buys you | Bidding |
| --- | --- | --- | --- |
| Brand awareness and reach | Efficient reach | Most unique reach for budget; bumper + skippable in-stream + Shorts | Target CPM |
| Brand awareness and reach | Target frequency | Same people a set number of times per week or month | Target CPM |
| Brand awareness and reach | Non-skippable reach | Full message delivered; 5 to 30s, longer skews to CTV | Target CPM |
| Brand awareness and reach | Ad sequence | A defined series of videos in order | Target CPM |
| Product and brand consideration | Video views | Views at efficient cost; skippable in-stream + in-feed + Shorts | Target CPV |
| Action / drive conversions | Video action | Conversions on YouTube (being retired, see below) | Maximize conversions, tCPA, tROAS |

Action note: YouTube video action line items are being phased out in favor of Demand Gen line
items. Treat new action-objective YouTube work as a Demand Gen build, and migrate existing
video action line items rather than creating more. Confirm the current cutover date on the
help page in Sources before you plan around it.

Format to billing map (this is the part that differs from display):

| Format | Length | Billing | What you pay for |
| --- | --- | --- | --- |
| Skippable in-stream | any; skippable after 5s | CPV (or target CPM) | A view: 30s watched, or full video if shorter, or an interaction |
| Non-skippable in-stream | 15 to 30s | Target CPM or fixed CPM | An impression |
| Bumper | up to 6s, not skippable | Target CPM or fixed CPM | An impression |
| In-feed | any | CPV | A click to watch, or a 10s autoplay view |
| Shorts | any | CPV or target CPM | Impression, TrueView view, or engagement |
| Masthead | reserved placement | CPM (reservation) | An impression |

## Core process

1. Complete advertiser setup before you build. Enable Google and partner inventory and accept
   the YouTube terms, turn on auto-tagging so conversions from YouTube clicks are counted, and
   link any YouTube channel you need. Have everything active at least 24 hours before flight so
   the line item can warm up. The line item cannot run without the terms accepted.
2. Pick the objective from the funnel stage, not the format. Awareness and reach, consideration,
   or action map to the subtypes above. The objective and subtype lock the eligible formats and
   the bid strategy, so choosing the subtype is most of the setup.
3. Pick the subtype. For pure reach efficiency use efficient reach. To control how often the
   same person sees the ad use target frequency. To guarantee the full message lands (and lean
   into connected TV) use non-skippable reach. To tell a story in order use ad sequence. For
   views and consideration use video views. For conversions, build Demand Gen instead of video
   action.
4. Choose formats within the subtype where the subtype allows a mix. Multi-format reach products
   spread delivery across bumper, skippable, in-feed, and Shorts to find the cheapest path to the
   goal; deselecting formats narrows supply and usually raises cost.
5. Set the bid the way the format bills. CPV or target CPV for view-billed formats, target CPM
   for impression-billed reach formats and sequences, fixed CPM only when a deal or a hard ceiling
   demands it. See `dv360-bid-strategy` for the fixed-vs-automated logic and learning periods.
6. Build the ad group and ads. Pick the YouTube video, set the landing page, and apply ad-group
   targeting. Remember line item targeting already flows down and cannot be loosened here.
7. Add connected TV deliberately. To buy YouTube on TV screens, use a connected TV insertion
   order and a YouTube on connected TV line item, which auto-sets the CTV-compatible type, format,
   bid strategy, and device targeting. Note several newer subtypes are not offered on CTV line
   items; build those in a standard insertion order.
8. Hand off. Audience strategy to `dv360-targeting-and-audiences`, reach and frequency goals to
   `reach-and-frequency-planning`, conversion measurement to `dv360-measurement-and-attribution`.

## Decision rules and thresholds

### What counts as a view (CPV and TrueView)

CPV bills a TrueView view, not an impression. The threshold depends on the format:

- Skippable in-stream: a view counts when the viewer watches 30 seconds, or the whole video if
  it is shorter than 30 seconds, or interacts with the ad. The viewer can skip after 5 seconds,
  so a skip before 30s costs nothing.
- In-feed: counts when the viewer clicks the thumbnail to watch, or watches 10 seconds of
  autoplay.
- Shorts: counts on a 10s watch (or completion), a call-to-action click, or an engagement.
- Bumper and non-skippable: TrueView views are not counted, because the viewer cannot skip.
  These are impression-billed, so judge them on CPM, reach, and frequency, not view rate.

Practical consequence: do not compare view rate across CPV and CPM formats, and do not put a
view-rate goal on a bumper or non-skippable line item. Use CPV and view rate for skippable,
in-feed, and Shorts; use CPM, reach, and frequency for bumper, non-skippable, and CTV.

### Target CPV vs maximum CPV

New YouTube video views buying uses target CPV: you set a target average cost per view and the
system optimizes to win as many views as possible around that target, so individual views run
above or below it. This is the successor to the older maximum CPV (mCPV) cap. If you inherit an
mCPV line item, plan to move it to target CPV. Treat the target as an average the algorithm
holds, not a hard ceiling, the same caution that applies to all automated targets in
`dv360-bid-strategy`.

### Choosing the reach product

- Efficient reach when the goal is the most unique people for the budget and you do not need to
  control frequency. Bumper plus skippable plus Shorts, target CPM.
- Target frequency when repetition drives the outcome and you want a set number of exposures per
  person. Supported ranges: with a single in-stream format, weekly 2 to 4 and monthly 4 to 8;
  with multi-format ads enabled, weekly 2 to 7 and monthly 4 to 12. Pick a target inside these
  bands; asking for more frequency than the band allows will not deliver.
- Non-skippable reach when the entire message must land. Videos run 5 to 30 seconds; up to 6
  seconds report as bumpers and 7 to 30 seconds as non-skippable. Ads 16 to 30 seconds serve
  primarily on connected TV, so use this subtype when you want longer creative on the big screen.
- Ad sequence when order matters: introduce then reinforce, prompt then inspire, attract then
  direct, or tell a multi-part story. Sequences bill on target CPM and optimize to deliver the
  whole sequence to a person. Target frequency is the simpler tool when you only need repetition
  and the order does not matter; reserve sequencing for a deliberate narrative.

### Connected TV

YouTube on connected TV is bought through a connected TV insertion order and a YouTube on
connected TV line item. The line item type is set to connected TV reach and consideration and
the platform auto-configures the CTV-compatible format, bid strategy, and device targeting.
Longer non-skippable creative (16 to 30s) naturally concentrates here. Several newer YouTube
subtypes are not available on CTV line items, so when you need one of those, build it in a
standard insertion order and let device targeting reach TV inventory.

## Audiences and inventory on YouTube

- Audience targeting on YouTube ad groups spans demographics (age, gender, household income,
  parental status), first-party YouTube audiences and Customer Match, Google audiences
  (Affinity, In-market, Life events, Detailed demographics), plus lookalike, combined, and
  custom audiences with optional audience expansion. Content targeting (placements, keywords,
  categories) is treated as one contextual dimension. For building and combining these segments,
  hand off to `dv360-targeting-and-audiences`; this skill is about which line item carries them.
- Line item targeting applies to all ad groups under it and cannot be overridden at the ad group
  level. Set the broad guardrails (geo, language, device, brand-safety exclusions) on the line
  item and use the ad group for the audience and content specifics.
- YouTube Select lineups package the top tier of popular YouTube channels in a market for brand
  buys. They are bought through deals (instant deals, guaranteed and non-guaranteed), not open
  auction, and include formats like in-stream, Shorts, and Pause; 30-second non-skippable is
  available against Select lineups. For deal mechanics, hand off to `dv360-deals-and-inventory`.
- Google video partners extend video beyond YouTube to vetted publisher sites and apps across
  devices, and can add meaningful incremental reach for a budget. Opt in when the goal is reach;
  keep it off when you need YouTube-only placement. It is a setting on the YouTube line item, not
  a separate buy.

## Reference material

This skill is self-contained. For adjacent depth, see the cross-linked skills named above
(`dv360-bid-strategy`, `dv360-targeting-and-audiences`, `reach-and-frequency-planning`,
`dv360-measurement-and-attribution`, `dv360-deals-and-inventory`, `dv360-campaign-architecture`)
and the verified help pages in Sources.

## Templates and examples

Upper-funnel awareness, broad reach, no frequency control:
```
Objective:  Brand awareness and reach
Subtype:    Efficient reach
Formats:    bumper + skippable in-stream + Shorts
Bidding:    target CPM
Judge on:   CPM, unique reach. Not view rate (mixed CPV/CPM formats).
```

Awareness where repetition is the lever:
```
Objective:  Brand awareness and reach
Subtype:    Target frequency
Target:     3x per week (inside the 2 to 7 multi-format weekly band)
Formats:    multi-format (bumper, skippable, in-feed, Shorts)
Bidding:    target CPM
```

Longer storytelling on the big screen:
```
Insertion order: Connected TV
Line item:  YouTube on connected TV (connected TV reach and consideration)
Creative:   20 to 30s non-skippable (serves primarily on CTV)
Bidding:    target CPM (auto-configured)
```

Mid-funnel consideration, optimizing for views:
```
Objective:  Product and brand consideration
Subtype:    Video views
Formats:    skippable in-stream + in-feed + Shorts
Bidding:    target CPV
Judge on:   CPV, view rate.
```

Lower-funnel conversions on YouTube:
```
Build a Demand Gen line item, not a video action line item.
Video action is being retired; migrate existing ones. See Sources for the cutover date.
```

## Common pitfalls

- Treating YouTube like a display line item. It has an extra ad group layer, objective-and-subtype
  selection, three-level targeting, and CPV billing. Build it as its own family.
- Putting a view-rate or CPV goal on a bumper or non-skippable line item. Those bill on impressions
  and never count TrueView views; measure them on CPM, reach, and frequency.
- Reading view rate across mixed formats. A multi-format reach line item blends CPV and CPM
  formats, so a single view-rate number is misleading. Split the read by format.
- Asking for more frequency than the band supports. Target frequency only delivers inside its
  weekly and monthly ranges; a target above the band will underdeliver. Check the band for your
  format mix first.
- Deselecting formats to "stay on brand" and then paying more. Narrowing a multi-format reach
  product shrinks supply and usually raises CPM or CPV. Narrow only when placement control is
  worth the premium.
- Building new video action line items. They are being paused and archived in favor of Demand Gen.
  Start action-objective work as Demand Gen and migrate the rest before the cutover.
- Forgetting advertiser prerequisites. Without accepting the YouTube terms, enabling Google and
  partner inventory, and turning on auto-tagging, the line item will not run or will not attribute
  conversions. Set these up at least 24 hours before flight.
- Expecting line item targeting to be loosened at the ad group. It flows down and cannot be
  overridden lower, so set the floor correctly on the line item.

## Sources

- [YouTube & partners ad formats (DV360)](https://support.google.com/displayvideo/answer/6274216?hl=en) (as of June 2026)
- [Create YouTube & partners line items (DV360)](https://support.google.com/displayvideo/answer/6274679?hl=en) (as of June 2026)
- [Initial setup for running YouTube & partners and Demand Gen line items (DV360)](https://support.google.com/displayvideo/answer/6274611?hl=en) (as of June 2026)
- [Create YouTube efficient reach line items (DV360)](https://support.google.com/displayvideo/answer/9173684?hl=en) (as of June 2026)
- [Create YouTube target frequency line items (DV360)](https://support.google.com/displayvideo/answer/13002456?hl=en) (as of June 2026)
- [Non-skippable reach line items (DV360)](https://support.google.com/displayvideo/answer/9224914?hl=en) (as of June 2026)
- [YouTube ad sequence campaigns (DV360)](https://support.google.com/displayvideo/answer/9322949?hl=en) (as of June 2026)
- [Create YouTube video views line items (DV360)](https://support.google.com/displayvideo/answer/14113197?hl=en) (as of June 2026)
- [About YouTube video action line items (DV360)](https://support.google.com/displayvideo/answer/9065351?hl=en) (as of June 2026)
- [Create YouTube & partners on Connected TV line items (DV360)](https://support.google.com/displayvideo/answer/12168640?hl=en) (as of June 2026)
- [Targeting for YouTube & partners and Demand Gen line items (DV360)](https://support.google.com/displayvideo/answer/6260055?hl=en) (as of June 2026)
- [Optimize your YouTube campaign (DV360)](https://support.google.com/displayvideo/answer/6277135?hl=en) (as of June 2026)
- [About video ad formats (Google Ads)](https://support.google.com/google-ads/answer/2375464?hl=en) (as of June 2026)
- [About YouTube ads and view metrics (Google Ads)](https://support.google.com/google-ads/answer/2375431?hl=en) (as of June 2026)
- [Video reach campaigns (Google Ads)](https://support.google.com/google-ads/answer/10581234?hl=en) (as of June 2026)
- [About Target frequency (Google Ads)](https://support.google.com/google-ads/answer/12400225?hl=en) (as of June 2026)
- [About Google video partners (Google Ads)](https://support.google.com/google-ads/answer/7166933?hl=en) (as of June 2026)
