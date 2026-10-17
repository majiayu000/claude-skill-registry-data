---
name: amazon-dsp-audiences
description: Build and layer audiences in Amazon DSP from shopping and streaming signals. Use when the user asks about Amazon DSP audiences, Amazon in-market or lifestyle or interest or life-event audiences, retargeting on Amazon, ASIN retargeting, views or purchases remarketing, advertiser audiences (pixel, event, hashed CRM), audiences built in Amazon Marketing Cloud, lookalike or similar audiences, or how to sequence and exclude audiences across the funnel.
---

# Amazon DSP audiences

Pick and layer the right Amazon DSP audiences so a line item reaches in-the-aisle shoppers and
streamers at enough scale to spend. Amazon DSP is Amazon's programmatic demand-side platform for
audience-first display, video, and streaming buys. It is distinct from Amazon's sponsored ads,
which are keyword-and-product placements that run on Amazon search and detail pages. The Amazon DSP
differentiator is its first-party shopping and streaming signal, so the audience strategy is the
core of the buy.

This skill is the targeting brain for Amazon DSP. For where the impressions come from (owned-and-
operated, streaming, deals, third-party exchanges) hand off to `amazon-dsp-inventory-and-supply`.
For audiences you build by querying signals in a clean room, cross-link to `amazon-marketing-cloud`.
For CPM, reach, frequency, and funnel definitions, see `programmatic-foundations`. For how to read
results against the goal, see `reporting-by-campaign-goal`.

## When to use this skill

Use this when the task is about WHO an Amazon DSP line item should reach, including:

- Choosing among Amazon audiences: in-market, lifestyle, interest, and life-event segments.
- Advertiser (your data) audiences: pixel and event based, hashed CRM uploads, and audiences built
  in Amazon Marketing Cloud and activated into Amazon DSP.
- Third-party audiences for broader reach beyond Amazon and your own data.
- Lookalike or similar audiences seeded from a high-value source.
- Retargeting on views, purchases, and ASIN-level signals with a chosen lookback window.
- Layering, sequencing, and excluding audiences across the funnel.
- The privacy posture of each audience type and when first-party signal is the honest advantage.

Boundaries with sibling skills:
- Inventory, supply sources, streaming TV, and deals live in `amazon-dsp-inventory-and-supply`.
- Clean-room audience construction, SQL-style queries, and cross-source analysis live in
  `amazon-marketing-cloud`. This skill covers selecting and activating an AMC-built audience; that
  skill covers building it.
- KPI and reach math live in `programmatic-foundations`. This skill does not redefine them.

## Quick reference

Audience taxonomy and when to reach for each. The first two columns are the Amazon DSP grouping;
the third is the funnel position an expert assumes.

| Audience class | Segment types | Reach for it when |
| --- | --- | --- |
| Amazon audiences (Amazon's data) | In-market, lifestyle, interest, life event | You want first-party shopping and streaming signal and have no equivalent of your own |
| Advertiser audiences (your data) | Pixel and event, hashed CRM, AMC-built | You have site, app, conversion, or customer signal to re-engage or seed |
| Lookalike or similar | Modeled from a seed audience | You have a strong seed and need scale beyond it |
| Third-party audiences | Licensed off-platform segments | You need reach in a category neither Amazon nor your data covers |

Amazon audience segments at a glance:

| Segment | What it captures | Funnel |
| --- | --- | --- |
| In-market | Recently shopping a category, "in-the-aisle" | Mid to lower funnel, intent |
| Lifestyle | Aggregated shopping and streaming habits (for example "foodies", "tech enthusiasts") | Upper funnel, awareness |
| Interest | A specific browsing or purchasing interest | Upper to mid funnel |
| Life event | Time-bound moments (for example "traveling soon") | Relevance window |

Combination logic an expert assumes: within an include group, segments combine as OR (any match);
a single exclude group removes users with AND or ALL logic. Build multiple include groups to widen,
add the exclude group to clean up, and keep the segment count per ad group within platform limits.

ASIN retargeting in one line: pick the ASINs (your products or related ones), choose views vs
purchases, and set the lookback window to the buying cycle. Tight lookback raises intent and cuts
reach; long lookback does the reverse.

## Core process

1. **Start from the goal and the funnel, not the segment list.** Awareness leans on lifestyle and
   interest audiences plus broad reach. Consideration leans on in-market and your own event-based
   audiences. Performance and loyalty lean on ASIN purchase retargeting and hashed CRM. Mapping the
   stage first keeps you from stacking segments that fight each other.
2. **Spend your first-party signal first.** If you have pixel, event, conversion, or CRM data, build
   the advertiser audience and use it before renting Amazon or third-party segments. It is the most
   relevant and the most durable as identifiers fade.
3. **Add Amazon audiences for the signal you lack.** This is the honest Amazon DSP edge: in-market
   and lifestyle segments are built from real Amazon shopping plus Prime Video, IMDb, and Twitch
   streaming activity that you cannot replicate from your own site alone. Use them where you have no
   equivalent first-party signal, not as a reflex.
4. **Build retargeting deliberately with the right lookback.** For views or purchases remarketing
   and ASIN-level retargeting, set the lookback window to match the product buying cycle (short for
   fast-moving consumables, long for considered purchases). The window is the intent dial.
5. **Seed lookalikes from your best source.** When a high-value seed (purchasers, high-LTV CRM, an
   AMC-built converter audience) is too small to spend, model a lookalike or similar audience from it
   to extend reach while staying close to the seed's behavior.
6. **Bring in AMC-built audiences for logic the console cannot express.** When you need a rule the
   standard builder cannot state (for example, exposed to channel A but not B, then purchased), build
   the audience in Amazon Marketing Cloud and activate it into Amazon DSP. See `amazon-marketing-cloud`.
7. **Layer with OR to widen, exclude to clean.** Add segments to an include group (OR) to grow the
   pool. Put converters, existing customers, and irrelevant users into the single exclude group.
   Exclusion is the cheapest precision you have.
8. **Sequence across line items, do not over-intersect one.** Amazon DSP grows the pool with OR
   include groups, so deep AND-style intersection is expressed by splitting funnel stages across
   separate line items (prospecting, retargeting, loyalty) rather than choking one line item.
9. **Check scale before launch.** Confirm the audience is large enough to spend the daily budget and
   to give optimization data. If it is too small, widen the include group, loosen the lookback, or
   move to a lookalike.

## Decision rules and thresholds

- **First-party first, Amazon audiences for the gap.** Use your pixel, event, and CRM audiences on
  the people most likely to convert, then extend with Amazon audiences and lookalikes. The shopping-
  signal advantage is real but it is rented data about Amazon behavior, not a substitute for your own
  customer signal. Write the strategy so it survives third-party identifier loss by leaning on first-
  party and Amazon-native signal.
- **In-market vs lifestyle is funnel position.** In-market equals active category intent for mid and
  lower funnel. Lifestyle and interest equal durable habits for the top. If the KPI is a conversion
  or purchase, prefer in-market plus retargeting. If the KPI is reach or new-to-brand, prefer
  lifestyle and interest.
- **Lookback window is the intent dial for retargeting.** A 7 to 14 day window is hot, recent intent
  for fast cycles. A 30 to 90 day or longer window is broader and suits considered purchases. Set it
  to the buying cycle, not a default.
- **OR widens, the exclude group cleans, splitting line items sequences.** Use multiple include
  groups (OR) to grow reach. Use the single exclude group for converters and customers. Express
  funnel sequencing by separate line items, because the platform does not intersect include groups
  the way some DSPs do.
- **Respect per-ad-group segment limits.** There is a ceiling on segments and include groups per ad
  group, so do not pile in dozens of overlapping segments. Curate to the few that matter and let the
  exclude group remove waste.
- **Seed size gates a lookalike.** A lookalike needs a seed large enough to model. If a seed is too
  small even to model, widen the seed (longer lookback, more ASINs) before trying to extend it.
- **Match audience size to budget and flight.** A tight retargeting pool or a narrow AMC audience may
  be too small to spend the plan or to teach optimization. If the audience cannot support the budget,
  widen it or move budget to a line item that can.

## Reference material

- See `programmatic-foundations` for CPM, reach, frequency, lookback, and funnel-stage definitions.
  This skill does not redefine them.
- See `amazon-marketing-cloud` for building rule-based and lookalike audiences in the clean room from
  pseudonymized signals, then activating them into Amazon DSP.
- See `amazon-dsp-inventory-and-supply` for the supply the audience runs against, and
  `reporting-by-campaign-goal` for reading audience performance against the campaign goal.

## Templates and examples

Performance line item, kitchenware brand, drive purchases:

- First-party base (include group A, OR): ASIN purchasers 0 to 365 days excluded later; site-pixel
  cart abandoners 0 to 14 days; hashed CRM lapsed buyers.
- Amazon signal (include group B, OR): in-market for "cookware" and "small kitchen appliances".
- Lookalike: similar audience seeded from high-LTV purchasers to extend reach.
- Exclude group: ASIN purchasers 0 to 30 days (just bought), employees, current subscribers.
- Lookback: views remarketing at 14 days, purchases retargeting tuned to the replacement cycle.
- Scale check: confirm the combined pool can spend the daily budget; if not, loosen the in-market
  lookback or lean harder on the lookalike.

Awareness line item, new beverage brand, new-to-brand reach:

- Amazon audiences (include group, OR): lifestyle "foodies" plus interest "healthy living".
- Life event (separate include group): a relevant moment if one fits the product.
- Exclude group: existing purchasers if a first-party or ASIN audience exists, so spend goes to new
  customers.
- AMC option: if you need "streamed our brand on Prime Video but never purchased", build that
  audience in `amazon-marketing-cloud` and activate it here.
- Scale check: lifestyle and interest are broad by design, so confirm frequency caps and supply, not
  audience size, are the binding constraint.

## Common pitfalls

- **Reaching for Amazon audiences before using your own data.** The shopping signal is attractive,
  but your pixel, event, and CRM audiences convert better and are more durable. Use first-party
  first, then fill gaps with Amazon segments.
- **Wrong lookback window.** A 7 day window on a 6 month replacement cycle starves the pool; a 90 day
  window on a daily consumable serves stale intent. Set the window to the buying cycle.
- **Forgetting the exclude group.** Without converter and customer exclusions you pay to re-serve
  people who already bought and you let overlapping includes double-count. The single exclude group
  is mandatory hygiene.
- **Over-stuffing one ad group with segments.** Piling dozens of overlapping segments into one ad
  group hurts clarity and hits platform limits. Curate, and sequence the funnel across line items.
- **Treating lifestyle as intent.** Lifestyle and interest are durable habits, not active purchase
  intent. If the KPI is a conversion, lead with in-market and retargeting, not lifestyle.
- **Over-claiming the data.** Be honest in the plan: Amazon audiences are Amazon's first-party signal
  about Amazon-ecosystem behavior, powerful for relevance but still rented and aggregated. They do
  not see your full off-Amazon funnel; that is what your pixel, CRM, and AMC audiences add.

## Sources

Official Amazon Ads pages, all verified as of June 2026. Amazon's public documentation is thinner
than some DSPs and several deep-dive pages require an advertiser login. Where a detail (per-ad-group
segment limits, exact lookback options, AMC activation steps) is not fully covered on a public page,
confirm it in the Amazon DSP console or the Amazon Ads help center for your account, since these
limits change and can vary by marketplace.

- Amazon DSP product overview (Amazon audiences, advertiser audiences, third-party audiences; first-
  party buying, browsing, and streaming signals): https://advertising.amazon.com/solutions/products/amazon-dsp
- Demand-side platform guide (DSP definition and Amazon DSP first-party signal differentiator):
  https://advertising.amazon.com/library/guides/demand-side-platform
- Amazon audiences segment categories (in-market, lifestyle, interest, life event, with examples):
  https://advertising.amazon.com/resources/whats-new/sponsored-display-amazon-audiences
- Display ads guide (the four audience categories: interests, life events, lifestyle, in-market):
  https://advertising.amazon.com/library/guides/display-ads-guide
- Views and purchases remarketing and lookback windows (first-party shopping and streaming signals):
  https://advertising.amazon.com/library/guides/display-ads-purchases-remarketing
- Simplified audience targeting (include groups with OR or ANY logic, single exclude group with AND
  or ALL, segment count per ad group): https://advertising.amazon.com/library/news/simplified-audience-targeting
- Amazon Marketing Cloud (clean room; rule-based and lookalike audience creation from pseudonymized
  signals, activation into campaigns): https://advertising.amazon.com/solutions/products/amazon-marketing-cloud
