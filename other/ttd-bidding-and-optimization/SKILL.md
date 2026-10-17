---
name: ttd-bidding-and-optimization
description: How buying and optimization work on The Trade Desk at a conceptual level. Use when the user asks about Trade Desk bidding, Koa optimization, Kokai AI, TTD bid strategy, how to optimize a TTD campaign, predictive clearing, KPI prediction, bid factors, seeds, TTD forecasting, or TTD pacing. Covers the publicly documented model of impression valuation and AI-assisted optimization, and flags which exact bidding controls live in the partner platform.
---

# The Trade Desk bidding and optimization

How The Trade Desk turns budget into won impressions against a KPI: the platform AI scores
each impression for its value to your campaign, you steer that AI with a goal, a seed, and
bid factors, and the system optimizes price, allocation, and pacing across the flight. This
skill explains the publicly documented model so an agent can reason about a TTD campaign and
give sound advice. The exact menu of bid controls, the optimization settings, and the numbers
live in the partner platform behind a login, so this skill states the concept and flags where
the operator has to confirm specifics in the product.

This skill assumes you know CPM, CPA, CPC, ROAS, win rate, and pacing. For those definitions
and the KPI math, see the `programmatic-foundations` skill. For deciding what report proves a
goal was met, see the `reporting-by-campaign-goal` skill. For where a campaign sits in the
account, see the `ttd-campaign-structure` skill (sibling). For audiences and data that feed
the bid, see the `ttd-targeting-and-audiences` skill (sibling).

## When to use this skill

- "How does bidding work on The Trade Desk?" / "What is a TTD bid strategy?"
- "What is Koa?" / "What does Kokai's AI actually do?" / "How does Koa optimize my campaign?"
- "How do I optimize a TTD campaign?" / "Performance mode vs doing it by hand."
- "What are bid factors / seeds / KPI prediction / predictive clearing?"
- "How does TTD forecasting work?" / "Will this change help before I make it?"
- "How does pacing work on The Trade Desk?"

Boundaries with sibling skills:
- Audience definition, first- and third-party data, the data marketplace, contextual, and the
  seed's data side: `ttd-targeting-and-audiences`.
- Campaign and ad group structure, where bidding settings live in the hierarchy:
  `ttd-campaign-structure`.
- Inventory, deals, and supply paths such as OpenPath: `ttd-inventory-and-deals`.
- Identity (Unified ID 2.0, EUID) that underpins addressability: `ttd-identity-and-uid2`.
- Programming changes through the API: `ttd-api-and-automation`.
- Reading results and attribution: `ttd-measurement-and-reporting`.

## Quick reference

| The user wants | Concept that answers it | Where the specifics live |
| --- | --- | --- |
| To understand how TTD bids | AI scores each impression by value to the campaign | Partner platform |
| To pick a goal for the AI | Set the KPI the optimization steers toward | Partner platform |
| To tell the AI what they value | Seed plus bid factors on chosen dimensions | Partner platform |
| To avoid overpaying | Predictive clearing against first-price clearing prices | Automatic, tune in platform |
| To hand execution to the AI | Performance mode runs Koa features within your guardrails | Partner platform |
| To test a change before committing | Forecasting shows projected impact first | Partner platform |
| To control delivery over the flight | Budget, flight dates, and pacing settings | Partner platform |

The recurring pattern: the AI proposes value per impression and price, you constrain it with a
goal, a seed, bid factors, and budget. The names and toggles for those constraints are in the
product, so confirm exact labels there rather than guessing.

## Core process

Use this to reason about or advise on a TTD campaign's buying and optimization.

1. Anchor on the objective and KPI first. The optimization is only meaningful relative to the
   goal it serves, so name the KPI (reach, CPC, CPA, ROAS, completed views) before touching
   bids. The `reporting-by-campaign-goal` skill maps objective to KPI set.
2. Confirm there is signal. AI-assisted optimization toward a conversion KPI needs conversion
   volume to learn from, the same constraint as any DSP. With thin signal, lean on a
   higher-funnel KPI or more manual control until data accrues.
3. Define what "valuable" means to the AI. The platform AI calculates the value of each
   impression to your specific campaign; you shape that by creating a seed (your ideal
   customer) and adding bid factors on the dimensions that matter to the brand. Hand the
   audience and data side of the seed to `ttd-targeting-and-audiences`.
4. Let predictive clearing set the price. The AI analyzes historical clearing prices across
   first-price auction environments so you win at efficient prices and cut wasted spend.
   Treat this as price discipline, not a separate KPI.
5. Decide how much to automate. Performance mode lets the AI handle execution (Koa
   Optimizations, audience expansion, predictive clearing, identity features) within the
   goals, KPI, seed, and targeting you set. You can refine inputs or override at any point.
   Choose more automation when you have signal and a clear KPI, less when you need tight,
   absolute control.
6. Forecast before you change. The forecasting engine projects the impact of an edit before
   you commit it, so model a change first instead of learning from spend. Confirm the exact
   forecasting surface in the platform.
7. Set budget and pacing to match the strategy. Even, goal-aware delivery gives the
   optimization room to learn and spread across the flight. The exact pacing options and their
   labels are in the platform; confirm them there.
8. Hold changes stable long enough to read. Frequent resets restart learning, so let an edit
   run before judging it, then verify against the KPI with `ttd-measurement-and-reporting`.

## Decision rules and thresholds

The Trade Desk does not publish fixed numeric learning thresholds or bid-cap formulas on its
public pages, and the live controls sit in the partner platform. Apply these public,
concept-level rules and confirm the exact settings in the product.

- Match automation to signal. Conversion-goal optimization needs conversion volume. With
  little signal, optimize toward a higher-funnel KPI (reach, viewable, completed views) or
  keep more manual control until data builds. This mirrors the general DSP rule in
  `programmatic-foundations`.
- A goal is a target the AI steers toward, not a guaranteed hard ceiling. When you need an
  absolute price cap that can never be exceeded, you need an explicit control, so verify the
  cap setting in the platform rather than assuming the KPI target enforces it.
- Use a seed plus bid factors to express value, not blunt exclusions. Bid factors let the AI
  keep weighing every impression while leaning toward what you value; hard exclusions throw
  away opportunities the AI could have priced correctly.
- Let predictive clearing manage price in first-price environments. Overriding it with a rigid
  manual bid can forfeit the efficiency it finds across historical clearing prices.
- Change one lever at a time and forecast first. Stacking edits hides which one moved the KPI,
  and the forecasting engine exists precisely so you can predict impact before spending.
- Give every change a stabilization window before judging it. Reading a KPI too early, mid
  learning, leads to false negatives and premature reversals.

When a recommendation depends on an exact toggle, target field, bid-factor dimension, or
numeric threshold, say so plainly: that specific control is set in the partner platform and the
operator should confirm the current label and range there.

## How the AI fits together

A plain-language model of the publicly described pieces, so an agent can explain them.

- Koa is The Trade Desk's AI, introduced in 2018 to help set up and optimize campaigns against
  business objectives. Kokai, launched in 2023, distributes Koa's AI across the buying
  workflow rather than confining it to a single step.
- Impression valuation. The AI considers each impression opportunity individually and
  calculates its value to your specific campaign, prioritizing the most relevant opportunities
  in a fraction of a second, at very high throughput (the public pages cite analysis of up to
  15 million ad opportunities each second). "Value" is the sum of many AI calculations,
  publicly described as including KPI prediction, relevance, bid factors, and inventory
  quality.
- Seeds and bid factors are how you teach the AI. A seed defines your ideal customer; bid
  factors tell the AI which dimensions matter to the brand so it leans toward them when
  scoring. These are operator inputs set in the platform.
- Predictive clearing is price optimization. The AI analyzes historical clearing prices in
  first-price auctions so bids clear at efficient levels and waste less spend.
- Performance mode is the "let the AI execute" posture: you set goals, KPI, seed, and
  targeting, and the AI runs performance features (Koa Optimizations, audience expansion,
  predictive clearing, identity features) that adapt to live signals, with override available.
- Forecasting is the "look before you leap" surface: the forecasting engine projects the
  impact of edits and optimizations so you can understand them before committing.

Koa Audiences and Koa Optimizations are the publicly named optimization features. Their exact
configuration and any newer feature names live in the partner platform; confirm current naming
there.

## Templates and examples

Advice framing, conceptual (confirm exact controls in the platform):

> "Set your KPI to CPA, build a seed from your converter list, and add bid factors on the few
> dimensions you care about (for example device or content category) rather than hard
> exclusions, so Koa keeps pricing every impression. Let predictive clearing handle the bid in
> the first-price auctions. Before you change the goal, run the forecast to see the projected
> impact. The exact toggles and fields are in the platform, so confirm the labels there."

Triage framing when a campaign underdelivers against KPI:

> "First confirm the objective and KPI are set correctly. Then check there is enough conversion
> signal for a conversion goal; if not, optimize to a higher-funnel KPI for now. Confirm budget
> and pacing are not starving delivery. Make one change, forecast it, and let it stabilize
> before reading the result. The specific settings to inspect are in the partner platform."

## Common pitfalls

- Treating a KPI target as a hard price ceiling. It is a goal the AI steers toward; for an
  absolute cap, confirm an explicit control in the platform.
- Pointing conversion-goal optimization at a campaign with almost no conversions, then blaming
  the AI. With thin signal, start higher in the funnel.
- Smothering the AI with hard exclusions instead of bid factors, which removes impressions the
  AI could have priced well.
- Stacking several edits at once, so no single change can be credited or blamed.
- Judging a change before it stabilizes and reverting on noise.
- Inventing bid-factor names, menu labels, or thresholds. When the detail is platform-specific,
  say it is set in the partner platform and have the operator verify it.

## Sources

- The Trade Desk, Our Demand Side Platform (DSP) overview: https://www.thetradedesk.com/our-demand-side-platform (as of June 2026)
- The Trade Desk, AI for Advertising (Koa, bid factors, seeds, predictive clearing, Koa Audiences and Koa Optimizations): https://www.thetradedesk.com/our-demand-side-platform/ai-artificial-intelligence (as of June 2026)
- The Trade Desk press release, "The Trade Desk Launches Kokai" (Koa history, per-impression scoring, KPI prediction, predictive clearing), June 6, 2023: https://www.thetradedesk.com/press-room/the-trade-desk-launches-kokai-a-new-media-buying-platform-that-brings-the-full-power-of-ai-to-digital-marketing (as of June 2026)
- The Trade Desk, Performance mode: AI-powered trading (goals, KPI, seed, automated price and allocation, override): https://www.thetradedesk.com/resources/outcome-driven-optimization-powered-by-ai (as of June 2026)

Note on sourcing: The Trade Desk's detailed product documentation and API reference sit behind
a partner login and are not cited here. The exact bidding controls, optimization settings, and
numeric thresholds require access to the partner platform.
