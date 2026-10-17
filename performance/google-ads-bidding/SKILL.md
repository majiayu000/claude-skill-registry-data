---
name: google-ads-bidding
description: Choose and configure the right Google Ads bid strategy. Use when the user asks about Google Ads bidding, Smart Bidding, which bid strategy to use, Target CPA or Target ROAS, Maximize conversions or conversion value, Maximize clicks, Target impression share, manual CPC, portfolio bid strategies, bid adjustments, seasonality adjustments, data exclusions, the learning period, or why a strategy is not delivering.
---

# Google Ads bidding

Pick the Google Ads bid strategy that matches the goal and the conversion data you actually have,
then set it so it can deliver. The bid strategy decides how every auction bid is computed: by hand,
toward clicks, toward visibility, or toward conversions and value with Smart Bidding. Choosing one
your conversion volume cannot support, or setting a target the auction cannot clear, is the most
common reason a campaign starves or misses goal.

Google Ads is Google's self-service auction platform across Search, YouTube, the Display Network,
Discover, Gmail, and Maps. It is a different platform from DV360; do not carry DV360 bid-strategy
names or line-item concepts into Google Ads. For KPI definitions and goal math (CPA, ROAS, CPC,
CPM), see the `programmatic-foundations` skill. The conversion tracking these strategies depend on
lives in `google-ads-conversion-tracking-and-attribution`; budget and pacing live in
`google-ads-budgets-and-pacing`.

## When to use this skill

- "Which bid strategy should I use?" / "Target CPA or Target ROAS?"
- "Set up Maximize conversions / Maximize conversion value / Target CPA / Target ROAS."
- "When should I use Maximize clicks or Target impression share?"
- "Should I bid manually? What about enhanced CPC?"
- "What is a portfolio bid strategy and when do I need one?"
- "How do bid adjustments work under Smart Bidding?"
- "How do seasonality adjustments and data exclusions work?"
- "How long is the learning period?" / "Why did performance drop after I changed the bid strategy?"

Boundaries with sibling skills:
- Conversion tracking and attribution setup that Smart Bidding depends on:
  `google-ads-conversion-tracking-and-attribution`.
- Budget setting, shared budgets, and pacing across campaigns: `google-ads-budgets-and-pacing`.
- Which campaign type to run at all: `google-ads-campaign-types`.
- Performance Max setup (PMax uses Smart Bidding but its own setup): `google-ads-performance-max`.
- Reading results against the goal: `reporting-by-campaign-goal`.

## Quick reference

Goal to bid strategy:

| Goal | Strategy | Family | Needs conversion data |
| --- | --- | --- | --- |
| Most conversions for the budget | Maximize conversions | Smart Bidding | Yes, builds as it runs |
| Conversions at a cost target | Target CPA (Maximize conversions with a target CPA) | Smart Bidding | Yes, target needs history |
| Most conversion value for the budget | Maximize conversion value | Smart Bidding | Yes, with values |
| Value at a return target | Target ROAS (Maximize conversion value with a target ROAS) | Smart Bidding | Yes, value history |
| Most site visits for the budget | Maximize clicks | Automated, not Smart Bidding | No |
| Visibility at a chosen position | Target impression share | Automated, not Smart Bidding | No |
| Full manual control of the bid | Manual CPC | Manual | No |

Two things the table encodes:
- Smart Bidding means auction-time bidding that optimizes for conversions or conversion value using
  Google AI in every auction. Maximize conversions, Maximize conversion value, Target CPA, and
  Target ROAS are the Smart Bidding strategies.
- Maximize clicks and Target impression share are automated but not Smart Bidding; they optimize for
  clicks or position, not conversions, so they need no conversion data.

## Core process

1. Name the goal precisely. Volume of conversions, conversions at a cost, conversion value, value at
   a return, traffic, or visibility. The goal picks the strategy; do not start from a strategy name.
2. Check the conversion data you have. Conversion-based Smart Bidding needs conversion tracking live
   and enough volume to learn. If you have almost none, start with Maximize conversions (which builds
   history) or, for pure traffic or visibility goals, Maximize clicks or Target impression share,
   which need no conversions.
3. Decide volume versus target. Want the most the budget can buy, start with Maximize conversions or
   Maximize conversion value (they spend the full budget). Want efficiency at a number, add a Target
   CPA or Target ROAS once you have enough history to set a realistic one.
4. Set the strategy at the campaign, or as a portfolio strategy across campaigns that share a goal
   (see Portfolio below). Avoid a target tighter than the auction clears at launch; it starves
   delivery.
5. Let Smart Bidding own the auction signals. Under Smart Bidding most manual bid adjustments are
   ignored because the system already adjusts per auction (see Bid adjustments below). Do not try to
   hand-tune what the algorithm is optimizing.
6. Hold the strategy through the learning period (below). Use seasonality adjustments only for short,
   known conversion-rate swings and data exclusions only for short tracking outages; both are
   surgical tools, not routine levers.
7. Judge against the goal, not the mechanism (hand off to `reporting-by-campaign-goal`).

## The strategies in detail

### Smart Bidding (conversion and value strategies)

- Maximize conversions: sets bids to get the most conversions while spending the budget.
  Volume-first. The on-ramp when you want conversions and do not yet have the history for a reliable
  target. Add a Target CPA when you want to hold a cost.
- Target CPA: Maximize conversions with a target cost per action. Sets bids to get as many
  conversions as possible at the average CPA you choose. For evaluation, measure over the last 30
  days including at least 30 conversions; you can start with little history, but the target gets
  reliable as volume builds.
- Maximize conversion value: sets bids to get the most conversion value while spending the budget,
  for advertisers whose conversions carry different values. Add a Target ROAS when you want to hold a
  return.
- Target ROAS: Maximize conversion value with a target return on ad spend. Sets bids to get as much
  conversion value as possible at the ROAS you choose. It wants a value history before it qualifies
  (roughly at least 15 conversions in the past 30 days at the conversion-tracking level for Search
  and Shopping, more is better), and reporting values across campaigns for several weeks before you
  fix a target.

All four require conversion tracking. Value strategies additionally require accurate conversion
values, not just counts. For tracking and values, hand off to
`google-ads-conversion-tracking-and-attribution`.

### Automated, not Smart Bidding

- Maximize clicks: adjusts CPC to get as many clicks as possible within the budget. Optional max CPC
  cap. Use it for traffic goals or when you have no conversion signal yet. It does not optimize for
  conversions or position.
- Target impression share: sets bids to show your ad at a chosen position (absolute top, top, or
  anywhere) for a chosen share of auctions. Use it for brand defense and visibility goals, not for
  efficiency. Note impression-share metrics track Google Search, not Search Partners.

### Manual CPC and enhanced CPC

Manual CPC lets you set the maximum CPC yourself per ad group or keyword, for full control when you
deliberately do not want automation, for example a small or highly atypical account. Note that
enhanced CPC (the old setting that nudged manual bids up or down toward conversions) is no longer
available for Search and Display campaigns as of the week of March 31, 2025. So the practical choice
today is plain manual CPC for control, or a Smart Bidding strategy for conversion optimization;
there is no enhanced-CPC middle option on Search and Display anymore. Prefer Smart Bidding once you
have conversion tracking and any reasonable volume, because per-auction optimization beats a static
manual bid.

## Portfolio bid strategies

A portfolio bid strategy is a goal-driven strategy applied across multiple campaigns (and where
applicable ad groups and keywords) so they optimize toward a shared goal from one place.

- Available for Maximize clicks, Target impression share, Target CPA, Target ROAS, Maximize
  conversions, and Maximize conversion value, stored in the Shared library.
- Not available for Performance Max campaigns (PMax bidding is set on the campaign; see
  `google-ads-performance-max`).
- Use one when several campaigns share a single goal and budget logic and you want bids set and
  changed for the group together, often paired with a shared budget (see
  `google-ads-budgets-and-pacing`). Use a standard (single-campaign) strategy when a campaign's goal
  or economics differ from its neighbors.

## Bid adjustments under Smart Bidding

A bid adjustment is a percentage increase or decrease that shows ads more or less often by device,
location, ad schedule, audience, or demographic.

- Manual-bidding ranges: device roughly -100% to +900%; location, ad schedule, audience, and
  demographic roughly -90% to +900%. Multiple adjustments multiply, with some same-dimension
  exceptions.
- Under Smart Bidding, most manual bid adjustments are ignored, because the strategy already sets a
  bespoke bid per auction using these same signals. The practical exception is a device adjustment
  of -100% to fully exclude a device. Do not expect a +20% mobile adjustment to do anything under
  Target CPA; the algorithm has already priced mobile.
- The takeaway: on Smart Bidding, express intent through the goal, the target, targeting, and budget,
  not through layered manual adjustments.

## Seasonality adjustments and data exclusions

Both tell Smart Bidding about a temporary change so it does not over- or under-react. Use sparingly.

- Seasonality adjustments inform Smart Bidding of an expected conversion-rate change for a short,
  known event (a 1 to 7 day promotion or sale). They are ideal for short events and work poorly over
  long stretches (more than 14 days at a time). Smart Bidding already handles ordinary seasonality,
  so reserve these for genuine, sharp, planned swings. Available for Search, Shopping, and Display on
  Target CPA and Target ROAS, and for Performance Max on all its bid strategies.
- Data exclusions tell Smart Bidding to ignore conversion data from a window when tracking was
  broken (a tagging outage or site downtime), so the bad data does not poison learning. Apply them
  quickly after catching the issue and only for short windows; do not use them to paper over
  problems that ran for weeks. Available for Search, Display, Shopping, and Performance Max.

## Learning period

When you set or change a Smart Bidding strategy or its target, the system needs time to calibrate
before its performance should be judged. Expect a learning period of roughly one to two weeks, and
treat value strategies (Target ROAS, Maximize conversion value) as needing more conversion history
and a longer settle than count-based ones. The operative rule: change the strategy and its target as
little as possible during learning, because every edit restarts calibration and wastes the window.
If it is missing goal during learning, diagnose with the pitfalls below before touching the strategy.

## Templates and examples

- New lead-gen Search campaign, little conversion history: start Maximize conversions to build
  volume, then move to Target CPA once you can read at least ~30 conversions over 30 days and set a
  realistic target. Even budget, no manual bid adjustments.
- Retail Shopping with revenue values: Maximize conversion value, then Target ROAS once you have a
  value history (around 15+ conversions in 30 days and a few weeks of reported values), with the
  target set to a return the auction can actually clear.
- Brand-term defense: Target impression share at absolute top with a high share target, accepting
  that this is a visibility goal, not an efficiency one.
- Pure traffic push to a new content hub with no conversion goal yet: Maximize clicks with a sensible
  max CPC cap until conversion tracking and volume exist, then reassess.
- Several campaigns sharing one CPA goal and budget: a portfolio Target CPA across them with a shared
  budget (see `google-ads-budgets-and-pacing`).

## Common pitfalls

- Target set too tight. A Target CPA or Target ROAS the inventory cannot clear starves delivery,
  because the algorithm cannot find auctions at that price. Loosen the target or widen targeting,
  then let it relearn.
- Too few conversions for a target strategy. Without volume, Target CPA and Target ROAS cannot learn.
  Start with Maximize conversions or Maximize conversion value (or Maximize clicks for traffic) until
  volume builds, then add a target.
- Using a value strategy without accurate values. Target ROAS and Maximize conversion value optimize
  to conversion value; if values are missing or wrong, the optimization is wrong. Fix values first
  (`google-ads-conversion-tracking-and-attribution`).
- Layering manual bid adjustments on Smart Bidding. They are mostly ignored, so they create a false
  sense of control. Use the goal and target instead; reserve device -100% for true exclusions.
- Changing strategy or target mid-flight. Each change resets the learning period and discards
  calibration. Decide up front and hold.
- Overusing seasonality adjustments or data exclusions. They are surgical tools for short, known
  events and short tracking outages, not routine levers. Misusing them fights the algorithm.
- Reaching for manual CPC by default, or expecting enhanced CPC on Search or Display. Manual CPC
  forgoes per-auction optimization, and enhanced CPC is no longer offered on Search and Display.
  Prefer Smart Bidding once tracking and any volume exist.

## Sources

- [About Smart Bidding](https://support.google.com/google-ads/answer/7065882) (as of June 2026)
- [About automated bidding](https://support.google.com/google-ads/answer/2979071) (as of June 2026)
- [About Target CPA bidding](https://support.google.com/google-ads/answer/6268632) (as of June 2026)
- [About Target ROAS bidding](https://support.google.com/google-ads/answer/6268637) (as of June 2026)
- [About Maximize conversions bidding](https://support.google.com/google-ads/answer/7381968) (as of June 2026)
- [About Maximize conversion value bidding](https://support.google.com/google-ads/answer/7684216) (as of June 2026)
- [About Maximize clicks bidding](https://support.google.com/google-ads/answer/6268626) (as of June 2026)
- [About Target impression share bidding](https://support.google.com/google-ads/answer/9121108) (as of June 2026)
- [Portfolio bid strategy: Definition](https://support.google.com/google-ads/answer/6263072) (as of June 2026)
- [About bid adjustments](https://support.google.com/google-ads/answer/2732132) (as of June 2026)
- [About seasonality adjustments](https://support.google.com/google-ads/answer/10369906) (as of June 2026)
