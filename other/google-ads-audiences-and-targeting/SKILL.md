---
name: google-ads-audiences-and-targeting
description: Decide who to reach in Google Ads and how to attach them to a campaign. Use when the user asks about Google Ads audiences, audience segments, your data or remarketing, Customer Match, in-market or affinity, detailed demographics or life events, custom segments, targeting vs observation, optimized targeting, content targeting for Display and Video (topics, placements, content keywords), demographic targeting and exclusions, or audience signals for Performance Max and Demand Gen. This is Google Ads, not DV360.
---

# Google Ads audiences and targeting

Pick the right audience segments and content signals, attach them in the right mode, and let
automation expand reach without losing control. This skill is the people-and-context brain for
Google Ads. Google Ads is a different platform from Display & Video 360; its audience model,
naming, and the targeting-vs-observation control are Google Ads concepts, so do not import DV360
combined-audience or assigned-targeting logic here. For the keyword layer of Search, see
`google-ads-keywords-and-match-types`. For reach, frequency, and funnel-stage definitions, see
`programmatic-foundations`. For goal-specific reporting, see `reporting-by-campaign-goal`.

## When to use this skill

Use this when the task is about WHO a Google Ads campaign reaches and IN WHAT CONTENT, including:

- Choosing among your data (remarketing), Customer Match, in-market, affinity, detailed
  demographics, life events, and custom segments.
- Deciding Targeting vs Observation when you attach a segment.
- Turning optimized targeting on or off and knowing what it does to reach.
- Content targeting for Display and Video: topics, placements, and content (Display/Video)
  keywords, and how they combine.
- Demographic targeting as a narrowing layer and audience exclusions.
- Audience signals for Performance Max and audiences for Demand Gen.

Boundaries with sibling skills:
- Search keyword match types, negatives, and the search terms report live in
  `google-ads-keywords-and-match-types`. Keywords as Display content signals are covered here;
  keywords as Search query matching are covered there.
- Bid strategy (Target CPA, Target ROAS, Maximize conversions) lives in `google-ads-bidding`.
  Optimized targeting and audience signals lean on Smart Bidding but the strategy is chosen there.
- Performance Max as a campaign type lives in `google-ads-performance-max`. This skill covers the
  audience-signal input; that skill covers asset groups and channels.
- The remarketing tag, Customer Match list upload mechanics, and conversion setup live in
  `google-ads-conversion-tracking-and-attribution`. This skill decides which segment to use; that
  skill wires up the data that feeds it.

## Quick reference

Audience segment taxonomy and when to reach for each:

| Segment type | What it is | Reach for it when |
| --- | --- | --- |
| Your data (remarketing) | People who already interacted: site and app visitors, video viewers, converters | Re-engagement and seeding automation with proven signal |
| Customer Match | Your first-party CRM data (email, phone) matched to Google accounts | Reach and re-engage known customers across Search, Shopping, YouTube, Gmail, Display |
| In-market | Active purchase intent for a category | Lower funnel, people about to buy |
| Affinity | Durable interests, habits, lifestyle | Upper funnel awareness and consideration at scale |
| Detailed demographics | Long-term life facts (e.g. parental status, education, homeownership) | Coarse qualification of who, usually layered |
| Life events | Time-bound milestones (moving, graduating, marrying) | Short relevance windows around a life change |
| Custom segments | You define by keywords, URLs, and apps | No off-the-shelf segment fits the niche |

Two controls decide how a segment behaves:

- **Targeting vs Observation.** Targeting narrows reach to that segment. Observation does not
  change reach at all; it only lets you watch and bid-adjust how that segment performs. Targeting
  is for narrowing; observation is for measuring.
- **Optimized targeting.** Looks beyond the segments you picked to find new people likely to meet
  the campaign goal, using your segments and the landing page as a starting signal. It expands
  reach and respects your brand-safety and content exclusions.

Content targeting (Display and Video) is a separate axis from audiences and answers WHERE the ad
runs by page content: topics, placements, and content keywords. Combined in one ad group they
match ANY of them, which widens reach.

## Core process

1. **Start from the goal and funnel stage.** Performance leans on your data, Customer Match, and
   in-market, with optimized targeting on. Awareness leans on affinity, detailed demographics, and
   topics or placements. Picking the segment class from the goal stops you from layering segments
   that fight each other.
2. **Spend owned signal first.** Use your data and Customer Match on the people most likely to
   convert, then extend with Google in-market and affinity segments. First-party signal is the
   durable base as third-party signals decline; route the list mechanics to
   `google-ads-conversion-tracking-and-attribution`.
3. **Choose Targeting or Observation on purpose.** On Search and Shopping, default to Observation
   so you keep keyword-driven reach and only layer bid adjustments and insight from the segment.
   Use Targeting when you genuinely want to restrict an ad group to a segment (common on Display
   and Video). Observation never shrinks reach; Targeting does.
4. **Layer demographics and exclusions as narrowing, not reach.** Demographic targeting only
   prevents people outside your selected groups from seeing the ad; it does not add reach. Exclude
   converters, existing customers, and irrelevant segments before adding more includes, because
   exclusion is the cheapest precision you have.
5. **Add content targeting for Display and Video.** Set topics for content categories, placements
   for specific sites, apps, channels, or pages, and content keywords for contextual reach.
   Remember they combine as ANY within an ad group, so stacking them widens rather than narrows;
   to narrow content, use a tightly themed ad group instead.
6. **Decide optimized targeting last.** If you need scale on Display, Demand Gen, or Video action,
   turn it on knowing it will look beyond your chosen segments to find converters and may move
   delivery away from your hand-picked lists. Keep exclusions and brand-safety on as hard limits.
7. **For Performance Max and Demand Gen, supply signals, not hard targets.** In Performance Max,
   add an audience signal (your data, custom segments, interests, demographics) to teach the model
   who converts; it guides optimization but does not cap reach. In Demand Gen, build audience
   segments and lookalike segments off a seed list. Hand Performance Max setup to
   `google-ads-performance-max`.

## Decision rules and thresholds

- **Observation by default on Search; Targeting when you mean to restrict.** Adding a segment as
  Observation on a Search campaign costs you nothing in reach and gives you a performance read and
  a bid-adjustment lever. Reserve Targeting for when narrowing is the actual intent.
- **First-party first.** Your data and Customer Match carry the strongest signal and are the most
  durable as cookies and cross-site identifiers decline. Build the strategy so it survives
  third-party signal loss; do not depend on segment types that lean on third-party data.
- **Affinity is upper funnel, in-market is lower funnel.** If the KPI is a conversion, lead with
  in-market, custom segments, and your data. If the KPI is reach or consideration, lead with
  affinity and detailed demographics. Matching segment intent to the KPI is the core call.
- **Demographics narrow; they do not prospect.** Treat demographic targeting and detailed
  demographics as qualification layers on top of an audience or content base, not as a standalone
  reach source.
- **Optimized targeting trades control for scale.** It can pull delivery off your best segment when
  it finds equal-goal traffic elsewhere. That is fine for performance scale, wrong when you needed
  those specific people reached. Decide per campaign, and keep exclusions hard.
- **Content targeting combines as ANY; narrow with structure.** Adding more topics, placements, and
  content keywords to one ad group widens reach because the ad matches any of them. To tighten,
  split into purpose-built ad groups rather than expecting the layers to intersect.
- **Audience signals are guidance, not targeting.** In Performance Max, the audience signal speeds
  learning but does not limit who the campaign can reach; the model may serve outside it. Set that
  expectation and give it strong first-party signal to learn from.
- **Similar audiences are gone.** Google Ads removed similar audiences (also called similar
  segments) and the replacement path is your first-party segments plus optimized targeting or
  audience expansion, and Smart Bidding on Search and Shopping. Do not write a plan that depends on
  similar audiences; use optimized targeting and lookalike segments (Demand Gen) instead.

## Reference material

- See `programmatic-foundations` for reach, frequency, funnel-stage, and conversion definitions.
  This skill does not redefine them.
- See `google-ads-conversion-tracking-and-attribution` for the remarketing tag, Customer Match
  upload and matching, and the conversion data that feeds your data segments.
- See `google-ads-bidding` for the Smart Bidding strategy that optimized targeting and audience
  signals depend on.
- See `google-ads-performance-max` for asset groups, channels, and when Performance Max is right;
  this skill only covers its audience-signal input.

## Templates and examples

Display prospecting ad group, premium cookware brand, performance goal:

- Base segment (Targeting, because Display narrows by audience): in-market for "Cookware &
  Bakeware" plus a custom segment from competitor and recipe-site URLs.
- Exclude: your-data converters and a Customer Match list of existing buyers.
- Content layer: topics "Food & Drink" and a curated placement list of cooking sites; expect this
  to widen reach since content combines as ANY, so keep the ad group tightly themed.
- Optimized targeting: on, seeded by the segments above, to find new converters; exclusions stay
  hard.

Search non-brand campaign, observation overlay:

- Keywords carry reach (see `google-ads-keywords-and-match-types`).
- Segments added as Observation: in-market for the category and a your-data "all visitors" list,
  so you can read performance and apply bid adjustments without shrinking reach.
- Demographics: exclude age bands outside the buying profile only if data supports it; demographic
  targeting narrows, it does not add reach.

Performance Max audience signal, B2B software:

- Signal inputs: your-data list of trial signups and converters, a custom segment from competitor
  and category search terms, plus relevant in-market and detailed-demographic segments.
- Expectation: this guides the model and speeds learning; it does not cap reach, and the campaign
  may serve beyond the signal. Allow about two weeks for the model to integrate new signal.

## Common pitfalls

- **Setting a segment to Targeting on Search by accident.** That silently restricts the ad group
  to the segment and can collapse reach. On Search and Shopping, default to Observation.
- **Expecting demographics to prospect.** Demographic targeting only filters out people outside the
  selected groups; it adds no reach. Use it as a layer, not an audience.
- **Treating optimized targeting as free scale.** It can quietly redirect spend away from your best
  first-party segment. Fine for performance, bad when you needed those exact users. Decide on
  purpose and keep exclusions on.
- **Stacking content targeting and expecting it to narrow.** Topics, placements, and content
  keywords combine as ANY within an ad group, so adding more widens reach. Narrow with separate ad
  groups, not more layers in one.
- **Forgetting exclusions.** Without converter and customer exclusions you pay to re-serve people
  who already acted and you let overlapping includes double-count. Exclusions are mandatory hygiene.
- **Planning around similar audiences.** They were removed. A plan that still relies on them will
  not run; move to first-party segments with optimized targeting or audience expansion, and
  lookalike segments in Demand Gen.

## Sources

Official Google Ads Help, all pages opened and verified as of June 2026.

- About audience segments (your data, Customer Match, in-market, affinity, detailed demographics, life events, custom segments; "remarketing" is now "your data"): https://support.google.com/google-ads/answer/2497941
- Add audience targeting to an ad group or campaign: https://support.google.com/google-ads/answer/2497940
- About "Targeting" and "Observation" settings: https://support.google.com/google-ads/answer/7365594
- About Customer Match: https://support.google.com/google-ads/answer/6379332
- About custom segments (keywords, URLs, apps): https://support.google.com/google-ads/answer/9805516
- About optimized targeting (finds new converters beyond your segments; respects content exclusions): https://support.google.com/google-ads/answer/10537509
- About demographic targeting (narrowing only): https://support.google.com/google-ads/answer/2580383
- About combining content targeting types (topics, placements, Display/Video keywords match ANY): https://support.google.com/google-ads/answer/2580292
- About topic targeting: https://support.google.com/google-ads/answer/2497832
- About placement targeting: https://support.google.com/google-ads/answer/2470108
- Choose keywords for Display Network campaigns (content keywords): https://support.google.com/google-ads/answer/2453986
- About audience signals for Performance Max campaigns (optional, guides AI, does not cap reach): https://support.google.com/google-ads/answer/14530785
- Demand Gen audiences overview (segments and lookalike segments): https://support.google.com/google-ads/answer/15594567
