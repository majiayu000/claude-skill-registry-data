---
name: amazon-dsp-inventory-and-supply
description: Choose where Amazon DSP impressions come from and wire the supply to a goal. Use when the user asks about Amazon DSP inventory, Amazon supply, owned-and-operated inventory, Prime Video ads, Fire TV or Twitch or IMDb inventory, streaming TV on Amazon, Amazon Publisher Direct, third-party exchange supply on Amazon DSP, Amazon DSP deals, private marketplace, private auction, or programmatic guaranteed on Amazon.
---

# Amazon DSP inventory and supply

Decide where Amazon DSP impressions come from and wire the supply so a line item delivers against
its goal. Amazon DSP is Amazon's programmatic demand-side platform for audience-first display, video,
and streaming buys, distinct from Amazon's sponsored ads that run on Amazon search and detail pages.
Its supply edge is exclusive owned-and-operated inventory (Amazon.com, Fire TV, Twitch, IMDb, Prime
Video) reachable with first-party shopping and streaming signal, extended by third-party supply.

This skill covers supply sourcing and deal mechanics. For who to reach inside that supply, hand off
to `amazon-dsp-audiences`. For CPM, floor price, auction mechanics, and reach math, see
`programmatic-foundations`. For reading delivery against the goal, see `reporting-by-campaign-goal`.

## When to use this skill

Use this when the task is about WHERE Amazon DSP inventory comes from and how a deal is plumbed,
including:

- Amazon owned-and-operated supply: Amazon.com, Fire TV, Twitch, IMDb and the ad-supported streaming
  service, Prime Video ads, Alexa, and Kindle.
- Amazon Publisher Direct and third-party exchange supply beyond Amazon's own properties.
- Streaming TV and Prime Video ads as a distinct premium supply tier.
- Deals: Preferred Deal, Private Auction (private marketplace), and Programmatic Guaranteed, plus
  open real-time bidding.
- Choosing a supply source for a brand vs performance goal and blending tiers.

Boundaries with sibling skills:
- Audience selection, retargeting, and exclusions live in `amazon-dsp-audiences`. This skill picks
  the supply; that skill picks the people.
- KPI, CPM, and auction-mechanic definitions live in `programmatic-foundations`.

## Quick reference

Supply sources, from most exclusive to most scaled:

| Supply source | What it is | Reach for it when |
| --- | --- | --- |
| Amazon owned-and-operated | Amazon.com, Fire TV, Twitch, IMDb, Prime Video, Alexa, Kindle | You want Amazon's exclusive context plus first-party signal |
| Streaming TV (a premium subset of O&O plus APD) | Full-screen non-skippable video on Prime Video, Twitch, Fire TV, live sports, and APD streaming apps | The goal is premium video reach and co-viewed TV impact |
| Amazon Publisher Direct (APD) | Direct premium streaming, display, and audio from third-party publishers | You want premium third-party supply with direct relationships |
| Third-party exchanges | Open and curated exchange supply across the web and apps | You need scale beyond Amazon and APD |

Deal types on Amazon DSP, from most scaled to most committed:

| Deal type | Commitment | Price | Typical use |
| --- | --- | --- | --- |
| Open real-time bidding | None | Auction, clears at market | Scaled reach and performance |
| Private Auction (PMP) | None | Auction with a floor | Curated inventory, competitive |
| Preferred Deal | None (not obligated to buy) | Fixed | First look at a fixed CPM |
| Programmatic Guaranteed | Reserved volume | Fixed | Premium, reserved, must-deliver |

Deal discovery in one line: find and activate deals through the deals widget and inventory tooling in
Amazon DSP, where Preferred Deal, Private Auction, and Programmatic Guaranteed live alongside your
owned-and-operated, Amazon Publisher Direct, and third-party exchange supply selections on the line
item.

## Core process

1. **Match the supply tier to the goal.** Brand and high-impact goals that want premium context and
   guaranteed delivery map to streaming TV, owned-and-operated, and Programmatic Guaranteed. Reach and
   performance goals that want scale and efficiency map to open RTB plus selective PMP and APD. Most
   plans blend tiers.
2. **Lead with owned-and-operated where the context fits.** Amazon.com, Fire TV, Twitch, IMDb, and
   Prime Video are exclusive to Amazon DSP and pair the placement with first-party shopping and
   streaming signal. This is the supply other DSPs cannot buy, so use it where that context is the
   point. Pair it with the audience strategy in `amazon-dsp-audiences`.
3. **Treat streaming TV and Prime Video ads as a distinct premium tier.** These are full-screen,
   non-skippable video impressions on premium and live content (including live sports). Plan them for
   co-viewed reach and brand impact, with their own creative specs and frequency discipline, not as
   interchangeable with display.
4. **Extend with Amazon Publisher Direct for premium third-party supply.** APD gives direct access to
   premium third-party streaming TV, display, and audio inventory, a quality step between owned-and-
   operated and the open exchanges.
5. **Add third-party exchanges for scale.** Open and curated exchange supply across the web and apps
   backstops the premium tiers and carries the bulk of scaled reach when the goal needs it.
6. **Use deals where you need price, priority, or guarantee.** Negotiate a Programmatic Guaranteed
   deal when delivery is non-negotiable, a Preferred Deal to lock a fixed price with a first look and
   no obligation, and a Private Auction for curated competitive inventory. Activate them through the
   deals widget and assign them to the line item.
7. **Match line item type and creative specs to the supply.** Streaming TV video, display, and audio
   each have their own specs. A video deal will not serve display creatives, and a placement the
   supply does not support will not render. Match before launch.
8. **Confirm the bid clears the floor.** For auction supply and floored deals, the bid or bid-strategy
   ceiling must meet or beat the floor or fixed price, or the impression is filtered before the
   auction. See `programmatic-foundations` for floor and auction mechanics.

## Decision rules and thresholds

- **Tier the mix to the goal.** Owned-and-operated, streaming TV, and Programmatic Guaranteed buy
  exclusive context and delivery certainty at a higher CPM. APD and third-party exchanges buy scale
  and efficiency. Brand-led plans weight toward O&O, streaming, and guaranteed; performance-led plans
  weight toward open RTB and PMP with O&O for quality pockets.
- **Owned-and-operated is the differentiator, so use it on purpose.** It is the supply no other DSP
  can access and the only place the shopping and streaming signal sits next to the placement. If a
  plan ignores it and runs only exchange supply, it has thrown away the reason to be on Amazon DSP.
- **Streaming TV is premium video, price and pace it that way.** Full-screen non-skippable inventory
  on Prime Video, Twitch, Fire TV, and live sports commands premium CPMs and rewards tight frequency
  control. Do not lump it into a display line item or judge it on click metrics.
- **Commit only what guaranteed delivery requires.** Programmatic Guaranteed reserves a fixed volume
  at a fixed price and is an obligation. Size it to the reserved need and let auction and open supply
  flex around it.
- **A floor is a hard gate.** If the bid cannot clear the floor or fixed price, the deal cannot win,
  full stop. Check this before blaming targeting or audience size.
- **Choose APD vs open exchange on quality vs scale.** Reach for Amazon Publisher Direct when you want
  premium third-party supply with direct relationships and tighter quality. Reach for open exchanges
  when you need maximum scale and accept more variability.

## Reference material

- See `programmatic-foundations` for CPM, floor price, real-time bidding, private marketplace, and
  win-rate definitions. This skill does not redefine them.
- See `amazon-dsp-audiences` for the audience layered on top of this supply, and
  `reporting-by-campaign-goal` for reading supply and deal delivery against the goal.

## Templates and examples

Brand campaign, premium video reach, must deliver:

- Supply: Programmatic Guaranteed on Prime Video streaming TV for the flagship flight, plus owned-
  and-operated Fire TV and Twitch for additional co-viewed reach.
- Tiering: guaranteed Prime Video reserves the must-deliver volume; O&O streaming and select APD
  streaming apps extend reach around it.
- Setup check: deal accepted and active, streaming TV creative specs matched, frequency caps set for
  full-screen video, bid equals the fixed price.

Performance campaign, blended supply:

- Supply: open real-time bidding across third-party exchanges for scaled reach, plus a Private
  Auction PMP on two premium retail-context publishers, plus owned-and-operated Amazon.com placements
  for in-market shoppers.
- Tiering: open RTB carries the bulk of the budget; PMP and O&O capture the higher-intent pockets.
- Setup check: PMP floors are clearable by the bid strategy, creative specs match each supply type,
  and deals are assigned to the line item through the deals widget.

## Common pitfalls

- **Running Amazon DSP as a generic exchange buy.** Ignoring owned-and-operated and streaming supply
  wastes the one thing Amazon DSP has that others do not. Lead with the exclusive supply where the
  context fits the goal.
- **Treating streaming TV like display.** Full-screen non-skippable video on Prime Video and Twitch
  is a premium tier with its own specs, CPMs, and frequency needs. Do not judge it on clicks or lump
  it into a display line item.
- **Bidding below the floor.** The most common reason a freshly assigned deal shows zero spend. The
  bid is filtered before the auction, so no impression serves. Check the floor first.
- **Creative or line item type mismatch.** A video deal will not serve display creatives, and a size
  or format the supply does not support will never render. Match specs to the supply.
- **Over-committing guaranteed volume.** Programmatic Guaranteed is an obligation. Reserving more than
  the plan needs locks budget you cannot redeploy. Size it to the reserved need.
- **Blaming targeting before checking supply and floor.** Deal status, dates, floor, and creative
  specs are faster to verify and more often the cause than audience or geography restriction. Check
  the supply plumbing before the audience.

## Sources

Official Amazon Ads pages, all verified as of June 2026. Amazon's public documentation is thinner
than some DSPs and several deep-dive and console pages require an advertiser login. Where a detail
(exact deal-widget steps, supply availability by marketplace, spend minimums) is not fully covered on
a public page, confirm it in the Amazon DSP console or the Amazon Ads help center for your account,
since availability and minimums change and vary by region and service tier.

- Amazon DSP product overview (owned-and-operated supply: Prime Video, Twitch, Thursday Night
  Football, Amazon.com, Fire TV, Kindle, Alexa; APD and third-party exchanges; RTB, PMP, private
  auction, and programmatic guaranteed): https://advertising.amazon.com/solutions/products/amazon-dsp
- Demand-side platform guide (DSP definition, Amazon-exclusive properties, third-party apps and
  sites): https://advertising.amazon.com/library/guides/demand-side-platform
- Streaming TV ads (full-screen non-skippable video on Prime Video, Twitch, Fire TV, live sports;
  Amazon Publisher Direct): https://advertising.amazon.com/solutions/products/streaming-tv-ads
- Activate programmatic deals with the deals widget (Preferred Deal, Private Auction, Programmatic
  Guaranteed alongside owned-and-operated, Amazon Publisher Direct, and third-party exchange supply
  on the line item): https://advertising.amazon.com/resources/whats-new/activate-programmatic-deals-fasterusing-new-deals-widget
- Ad exchange guide (ad exchange and real-time bidding definition):
  https://advertising.amazon.com/library/guides/ad-exchange
