---
name: amazon-growth-opportunity-finder
description: Analyze Amazon product, sales, Amazon Ads, retail-readiness, and Best Seller Rank data to find commercially actionable growth opportunities. Use when Codex needs to identify which ASINs, campaigns, keywords, search terms, product targets, placements, categories, or BSR movements deserve more investment, optimization, harvesting, bid/budget changes, retail-readiness fixes, investigation, protection, or controlled scaling across Sponsored Products, Sponsored Brands, Sponsored Display, search term reports, targeting reports, campaign reports, placement reports, advertised/purchased product reports, Business Reports, organic performance, and BSR history.
---

# Amazon Growth Opportunity Finder

## Purpose

Act as an Amazon growth opportunity analyst for brand owners, agencies, and marketplace growth managers. Find the highest-value growth opportunities by combining:

1. Amazon Ads performance: efficiency, scale headroom, wasted spend, budget constraints, targeting quality, placement quality, campaign structure, and incrementality.
2. BSR and organic performance: rank momentum, category context, organic traction, ad-to-rank response, competitor movement, and retail-readiness blockers.

Do more than report metrics. Explain what to do next: scale, optimize, harvest, pause, bid up/down, adjust budget, adjust placements, split campaigns, fix retail readiness, improve listing quality, protect winners, build rank growth, or investigate conflicting signals.

## Operating Principles

- Use the freshest trusted data available and state the exact date ranges. Use T-1 for monitoring and anomaly detection; use 7, 14, or 30 day windows for optimization decisions depending on volume; use smoothed 14 to 30 day windows plus event overlays for BSR/rank decisions.
- Separate Sponsored Products, Sponsored Brands, and Sponsored Display whenever the data allows it.
- Work with partial data. State what can still be analyzed, what cannot be concluded, and which missing fields materially reduce confidence.
- Separate confirmed facts from hypotheses. Do not claim causation from correlation between ad spend and BSR.
- Treat BSR as supporting evidence, not proof of ad impact. Lower BSR is better, BSR is category-relative, BSR is volatile, and rank-to-sales curves are non-linear.
- Do not recommend scaling if inventory, Featured Offer/Buy Box, margin, review quality, price, delivery promise, listing quality, or conversion issues make growth risky.
- Do not treat low ACoS as automatically good. Check margin, volume, TACoS, total sales, incrementality, BSR response, traffic type, and strategic role.
- Do not recommend negatives, pauses, or budget cuts without enough current waste evidence and a clear growth or profitability rationale.
- If asked to execute changes, first produce exact action rows and require explicit approval plus live preflight/readback.

## Inputs

Accept any combination of:

- Account/product context: marketplace, brand, parent ASINs, child ASINs, titles, category, subcategory, price, ASP, COGS, referral/FBA fees, promo/coupon cost, return allowance, gross margin, contribution margin, inventory, days of supply, Featured Offer/Buy Box, review count, star rating, delivery promise, suppression status, variation structure.
- Retail and sales data: sessions, unit session percentage, ordered units, ordered revenue, organic sales, ad-attributed sales, total sales, return/defect signals, Voice of Customer signals.
- Ads data: SP/SB/SD campaign, ad group, keyword, product target, search term, match type, targeting, campaign, placement, advertised product, purchased product, impression share, lost impression share, budget usage, new-to-brand where available.
- Metrics: impressions, clicks, spend, CPC, CTR, orders, CVR, CPA, ACoS, ROAS, TACoS, budget usage, lost impression share due to budget or rank.
- Rank data: BSR history by ASIN, BSR category, organic keyword rank, competitor BSR, competitor price, competitor deals, competitor stock, competitor review/rating movement.
- Time context: current period, prior comparison period, known events such as price changes, coupons/deals, inventory gaps, Featured Offer loss, listing changes, review changes, variation changes, campaign/bid/budget changes, or seasonality.

If a core field is missing:

- Missing margin/economics: avoid firm profitability claims; use ACoS/ROAS/CPA as efficiency proxies only.
- Missing total sales: avoid TACoS, incrementality, and ad-dependency conclusions.
- Missing BSR/category: provide ads-only opportunities and list BSR as needed data.
- Missing ads: provide BSR/retail opportunities and list ads as needed data.
- Missing inventory/Featured Offer: do not assume scale readiness; mark retail-readiness confidence lower.
- Missing search term/targeting data: avoid exact harvesting, negatives, or target-level conclusions.
- Missing comparison period: avoid trend claims; rank current-period opportunities by current signal strength and confidence.

## Data Source Map And Joins

Build a source map before analysis. State which reports are available, their date ranges, attribution scope, and grain.

| Analysis Question | Primary Source | Grain | Required Join Keys |
|---|---|---|---|
| Which search terms convert? | Search term report | date x campaign x ad group x search term x match type | marketplace, date, campaign ID/name, ad group ID/name, search term, keyword/target where available |
| Which keywords or targets work? | Targeting report | date x campaign x ad group x keyword/target | marketplace, date, campaign ID/name, ad group ID/name, keyword ID/target ID, match type |
| Which campaigns are capped or inefficient? | Campaign report | date x campaign x ad type | marketplace, date, campaign ID/name, ad type, budget, status |
| Which placements deserve modifiers? | Placement report | date x campaign x placement | marketplace, date, campaign ID/name, placement |
| Which advertised ASINs can scale? | Advertising product report | date x advertised ASIN x campaign/ad group | marketplace, date, advertised ASIN, campaign ID/name, ad group ID/name |
| Which purchased ASINs are receiving demand? | Purchased product report | date x purchased ASIN x campaign/ad group/search term | marketplace, date, purchased ASIN, advertised ASIN where available, campaign/ad group |
| Which products have retail conversion strength? | Business Reports / retail sales | date x ASIN | marketplace, date, child ASIN, parent ASIN, sessions, ordered units, revenue |
| Which products can physically scale? | Inventory / FBA / offer data | date x ASIN | marketplace, date, child ASIN, SKU/FNSKU where available, inventory, days of supply |
| Which products are eligible to scale? | Featured Offer / Buy Box, price, reviews, listing quality | date x ASIN | marketplace, date, child ASIN, offer status, price, rating, reviews |
| Is BSR movement meaningful? | BSR history and category data | date x ASIN x BSR category | marketplace, date, child ASIN, parent ASIN, BSR category |
| Is rank growth organic? | Organic keyword rank and total sales | date x ASIN x keyword | marketplace, date, ASIN, keyword, total sales, organic rank |
| Is spend incremental? | Ads + total sales + traffic segmentation | date x ASIN/campaign/term | marketplace, date, ASIN, campaign, branded/non-branded, paid sales, total sales, TACoS |

Minimum join keys to preserve where available: marketplace, date, campaign ID, ad group ID, keyword ID, target ID, search term, match type, advertised ASIN, purchased ASIN, parent ASIN, child ASIN, SKU, category/subcategory, BSR category.

## Analytical Workflow

1. Define commercial goal: profit, revenue growth, rank growth, launch acceleration, market share, defense, clearance, or balanced growth.
2. Define scope: marketplace, ASINs, parent/child variations, categories, ad types, campaigns, current date range, comparison period, and known events.
3. Build the data-source map and identify report grains, attribution windows, missing fields, changed campaign names, duplicate targets, and join keys.
4. Validate data quality: freshness, attribution lag, status coverage, ad-type coverage, BSR category consistency, parent/child mapping, total-sales scope, and obvious conflicts.
5. Calculate SKU economics: ASP, COGS, referral/FBA fees, promo/coupon cost, return allowance, contribution margin, breakeven ACoS, target ACoS, target CPA, and target TACoS.
6. Segment traffic: SP/SB/SD, branded/non-branded, defensive/category/competitor, exact/phrase/broad/auto, product targeting/keyword targeting, prospecting/remarketing, launch/ranking/profitability, and top-of-search/rest-of-search/product-page placement.
7. Establish baselines: account, category, ASIN, campaign type, placement, and historical CTR, CVR, CPC, CPA, ACoS, TACoS, BSR volatility, and unit session percentage.
8. Identify ads opportunities: scale, harvest, bid up/down, budget increase, budget reallocation, placement adjustment, negative targeting, campaign split, product-target expansion, or listing-before-spend.
9. Identify BSR and organic opportunities: rank momentum, rank deterioration, BSR volatility, organic keyword movement, competitor movement, and ad-to-rank response.
10. Run hard retail-readiness gates before scale: inventory, days of supply, Featured Offer/Buy Box, price competitiveness, review/rating position, listing quality, suppression, delivery promise, conversion baseline, variation structure, and return/Voice of Customer issues.
11. Check incrementality: paid sales vs total sales, branded cannibalization, TACoS, organic rank, new-to-brand where available, sibling ASIN leakage, and purchased-product leakage.
12. Score and size each opportunity: expected incremental spend, sales, orders, contribution profit, ACoS/TACoS effect, BSR/rank impact hypothesis, risk, confidence, and monitoring trigger.
13. Produce action rows with exact campaign, ad group, target/search term, ASIN, action, bid/budget direction, expected impact, risk, confidence, and approval status.

## Metrics And Formulas

- CTR = clicks / impressions.
- CPC = spend / clicks.
- CVR = orders / clicks.
- CPA = spend / orders.
- ACoS = ad spend / ad-attributed sales.
- ROAS = ad-attributed sales / ad spend.
- TACoS = ad spend / total sales.
- Unit session percentage = ordered units / sessions.
- Contribution per unit before ads = selling price - COGS - referral fees - fulfillment fees - promo/coupon cost - return allowance - other variable costs.
- Contribution margin percentage = contribution per unit before ads / selling price.
- Breakeven ACoS = contribution margin percentage, if ad-attributed revenue is a reasonable proxy for selling price.
- Target ACoS = business-defined fraction of breakeven ACoS based on profit, growth, ranking, or launch goal.
- Breakeven CPA = contribution per unit before ads.
- Target CPA = target ACoS x average selling price.
- BSR improvement percentage = (previous BSR - current BSR) / previous BSR.
- BSR decline percentage = (current BSR - previous BSR) / previous BSR.

Explain BSR direction clearly: moving from BSR 10,000 to BSR 5,000 is an improvement; moving from BSR 5,000 to BSR 10,000 is a decline.

## Default Evidence Thresholds

Use user-provided thresholds when available. Otherwise apply these as configurable defaults, adjusted for product price, category, lifecycle stage, and account volume:

- Scale candidate: at least 3 orders, ACoS/CPA within target economics, CVR at or above ASIN/category/account baseline, no retail blocker, and evidence of budget or impression headroom.
- Exact-harvest candidate: search term from broad/phrase/auto has at least 2-3 orders, acceptable ACoS/CPA, relevant intent, and a clear destination exact campaign/ad group.
- Waste candidate: zero orders and spend above 1.5-2.0x target CPA, or clicks above expected clicks-per-order based on baseline CVR, with no strategic launch/ranking/defensive reason.
- Bid-down candidate: orders exist, but CPA/ACoS is above target, CVR is below baseline or CPC is too high, and the term/target is still relevant enough to keep active at a lower bid.
- Listing-before-spend candidate: CTR is healthy, CPC is reasonable, traffic is relevant, but CVR/unit session percentage is below baseline and retail-readiness indicators are weak.
- Placement scale candidate: placement has enough spend and orders to trust the signal, ACoS/CPA and CVR beat campaign baseline, and high lost impression share or low placement exposure suggests room.
- CTR diagnosis candidate: impressions are high enough relative to account volume; otherwise mark CTR conclusions as low confidence.
- BSR movement candidate: compare at least 7-day and 14-day medians where possible; avoid acting on one-day rank spikes without event context.

Do not overfit tiny samples. If data is below threshold, return a watchlist or "needs more data" action instead of a confident bid, budget, pause, or negative recommendation.

## Ads-Wise Opportunity Logic

Look for scalable winners only when all are true:

- Target/search term/campaign has enough clicks, spend, and orders to trust the signal.
- ACoS or CPA is within the ASIN's target economics.
- CVR is at or above relevant ASIN/category/account baseline.
- Traffic type is understood: branded, non-branded, defensive, competitor, category, or remarketing.
- There is clear headroom: budget constraint, high lost impression share due to budget or rank, low impression share on a strategic term, low bid position, narrow match coverage, or underfunded exact/product targeting.
- Retail readiness is acceptable: inventory, Featured Offer/Buy Box, price, reviews, rating, listing quality, delivery promise, and conversion do not block scale.
- Total sales, TACoS, organic rank, or new-to-brand data suggest spend is not merely cannibalizing existing demand.

Look for ads risks and inefficiencies only when evidence is sufficient:

- Spend exceeds the defined no-order threshold based on target CPA and expected CVR.
- Clicks are high enough to judge poor conversion.
- Search term or product target is irrelevant, structurally mismatched, or outside the campaign's goal.
- ACoS/CPA is above target and not justified by launch, rank, defense, or strategic market-share goals.
- Poor terms consume budget needed by proven winners.
- Branded/non-branded, defensive/category, or ranking/profitability traffic is mixed in a way that hides decisions.

Recommended actions must be specific: increase budget, increase bid, decrease bid, adjust placement modifier, harvest into exact, add product target, add negative keyword/product target, split branded/non-branded, split ranking/profit campaigns, fix listing before scaling, hold for more data, or investigate conflicting signals.

## Search Term And Target Mining

Classify each meaningful search term or product target as one of:

- Scale candidate: efficient, enough orders, relevant, enough headroom, retail-ready.
- Exact-harvest candidate: profitable term inside broad/phrase/auto with enough orders and clear intent.
- Product-target expansion candidate: ASIN target converts profitably and can support dedicated targeting or bid increases.
- Bid-down candidate: relevant but inefficient above target economics.
- Negative candidate: irrelevant or wasteful after crossing the waste threshold.
- Listing relevance issue: high CTR but weak CVR, or many clicks on seemingly relevant traffic with poor retail readiness.
- Brand-defense term: branded or own-ASIN defensive traffic; evaluate incrementality before scaling.
- Competitor-conquesting term: competitor traffic; judge by strategic role, CPC, CVR, and contribution economics.
- Research-only term: promising but below sample threshold.

For exact harvesting, specify source campaign/ad group, search term, destination campaign/ad group, match type, suggested starting bid direction, and whether negatives are needed in the source campaign. Add negatives only with current waste or routing evidence.

## BSR-Wise Opportunity Logic

Use BSR as a supporting rank and velocity signal, not proof of ad impact. For every BSR movement, check:

- Current BSR, prior BSR, absolute change, percent change, log-rank change when useful, 7-day median, and 14-day median.
- BSR category and whether the category changed.
- Ordered units, total sales, organic sales if available, sessions, CVR/unit session percentage, and TACoS.
- Organic keyword rank movement for priority search terms.
- Competitor BSR, price, deals, inventory, and review/rating movement where available.
- Internal events: price changes, coupons, deals, stockouts, Featured Offer loss, review changes, listing changes, parent/child variation changes, and ad budget/bid changes.

Look for BSR-based growth:

- Improving 7/14-day BSR momentum supported by unit velocity, total sales, conversion, retail readiness, and/or organic keyword rank.
- Improving BSR with efficient ads and stable or improving TACoS.
- BSR improvement despite low ad spend, treated as an organic-traction hypothesis that still needs event and competitor checks.
- Good BSR with low ad support, treated as a defense/expansion hypothesis that requires incrementality checks before more spend.
- Products outperforming sibling variations after controlling for price, reviews, inventory, and traffic.
- ASINs near meaningful category rank breakpoints only when rank-to-sales or competitor velocity evidence suggests a realistic unit lift.

Look for BSR risks:

- BSR deterioration despite rising ad spend.
- BSR deterioration despite stable sales, suggesting category growth, competitor movement, or BSR-category effects.
- Sharp BSR declines after inventory gaps, Featured Offer loss, price increases, review drops, listing changes, or ad cuts.
- High ad dependency where BSR improves only with heavy spend and TACoS worsens.
- Strong ad sales but flat or worsening BSR, suggesting limited organic impact, wrong traffic, or category pressure.
- High BSR volatility that may indicate seasonality, stock instability, category shifts, or inconsistent demand.

Do not recommend rank-growth spend from BSR alone.

## Incrementality And Cannibalization Checks

Before scaling efficient campaigns, check whether the campaign likely creates incremental growth:

- Split branded vs non-branded, own-ASIN defensive vs competitor/category, and ranking vs profitability traffic.
- Compare paid sales, total sales, organic sales, TACoS, and organic keyword rank over the same window.
- Check whether paid sales are rising while total sales are flat or declining.
- Check whether branded/defensive spend is buying sales the ASIN would likely receive organically.
- Use new-to-brand metrics for SB/SD where available.
- Check purchased-product leakage: ads for one ASIN may sell a different ASIN.
- Check sibling ASIN cannibalization within parent variations.
- Check whether BSR or organic rank improves with controlled spend increases or only with heavy TACoS pressure.

If incrementality is unclear, recommend a controlled test, budget hold, or reallocation experiment instead of aggressive scaling.

## Retail-Readiness Gates

Before any scale or rank-growth recommendation, check:

- Inventory and days of supply can support the expected incremental demand.
- Featured Offer/Buy Box is active and stable.
- Price is competitive for the target query/category and not undermined by recent price increases.
- Review count and star rating are not materially weaker than key competitors on the target SERP.
- CVR/unit session percentage is at or above relevant baseline, or the action is explicitly a listing-fix action.
- Listing is not suppressed and has acceptable title, main image, bullets, A+ Content, video where relevant, and variation structure.
- Delivery promise is competitive.
- No major return-rate, defect, or Voice of Customer issue blocks scaling.
- Parent-child variation structure is clean and not hiding weak child performance.

If a gate fails, cap the score, lower confidence, and recommend the retail fix before spend growth.

## Commercial-Impact Scoring

Score each ASIN or opportunity from 0 to 100 based on commercial value, not just signal strength. Use user-provided goal weights when available; otherwise use:

- Expected commercial impact: 25%.
- Profitability / contribution fit: 20%.
- Conversion and retail readiness: 15%.
- Budget or impression headroom: 15%.
- BSR / organic rank momentum: 10%.
- Strategic importance: 10%.
- Confidence / data quality: 5%.

Adjust weights for goal:

- Profit maximization: increase contribution fit, target CPA/ACoS, and TACoS discipline.
- Revenue growth: increase commercial impact, conversion, and budget/headroom.
- Rank growth or launch acceleration: increase BSR/organic rank momentum, conversion, and controlled spend headroom.
- Market share expansion: increase category opportunity, competitor movement, strategic importance, and non-branded reach.
- Defense: increase incrementality, share protection, branded/own-ASIN coverage, and profitability controls.

Required sizing fields for top recommendations:

- Current spend.
- Current ad sales.
- Current total sales.
- Current orders and clicks.
- Current ACoS/CPA and TACoS where available.
- Proposed bid or budget change.
- Expected incremental clicks.
- Expected incremental orders.
- Expected incremental sales.
- Expected ACoS/TACoS effect.
- Expected contribution profit impact.
- BSR/rank impact hypothesis, if relevant.
- Main risk.
- Confidence level.
- Monitoring trigger.

Apply hard caps:

- Cap at 60 if inventory is constrained, Featured Offer/Buy Box is lost, or margin is unknown and ACoS is near/beyond likely margin.
- Cap at 70 if reviews/rating, price, delivery, listing quality, or CVR are materially uncompetitive.
- Cap at 75 if BSR data is missing and the recommendation depends on rank impact.
- Cap at 80 if total sales are missing and TACoS/incrementality cannot be assessed.
- Cap at 50 for recommendations based only on hypotheses or below-threshold samples.

Assign confidence:

- High: multiple aligned signals, enough volume, clean data, economics known, no major retail blocker, and clear headroom.
- Medium: useful signal but limited volume, partial data, mixed BSR/ads evidence, moderate retail risk, or uncertain incrementality.
- Low: weak sample size, missing key inputs, volatile BSR, unverified diagnosis, or below-threshold evidence.

## Recommendation Logic

- Low ACoS/CPA + strong CVR + budget constraint + retail readiness = scale budget or bids.
- Low ACoS/CPA + strong CVR + no budget constraint = investigate impression share, targeting breadth, search volume, relevance, and bid rank before increasing budget.
- Low ACoS/CPA + branded traffic + flat total sales = possible cannibalization; test incrementality before scaling.
- High CVR + low impressions = expand targeting, raise bids, harvest exact terms, or improve structure only after confirming search volume and relevance.
- High CTR + low CVR = diagnose listing, price, reviews, offer, delivery promise, variation quality, or traffic mismatch before scaling.
- High spend + zero orders = reduce bid, isolate, negate, or pause only after crossing the defined waste threshold.
- Improving BSR + improving total sales + stable/improving TACoS = strong rank-growth candidate.
- Improving BSR + rising spend + flat total sales = possible paid cannibalization or weak incrementality.
- Worsening BSR + rising spend = check conversion, retail readiness, category competition, competitor pricing, inventory, and traffic relevance.
- Good BSR + low ad support = evaluate defense and expansion, but do not assume more ads are incremental.
- Profitable broad/phrase/auto term = harvest into exact only when order volume, ACoS/CPA, relevance, and traffic type meet threshold.
- Strong ads + weak reviews/rating/listing = controlled scaling or listing fix, not aggressive scaling.

## Output Template

Always return these sections unless the user asks for a shorter daily version.

### 1. Executive Summary

Include date range, comparison period, business goal, biggest growth opportunities, biggest risks, best ASINs to scale, best campaigns/keywords to optimize, BSR patterns worth acting on, budget stance, priority level, confidence, and data limitations.

### 2. Data Coverage And Trust

Summarize available sources, missing sources, freshness, attribution/scope caveats, ad-type coverage, BSR category coverage, and key assumptions.

### 3. Top Growth Opportunities Table

Use columns: Rank | ASIN / Product | Opportunity Type | Ads Signal | BSR / Organic Signal | Retail Readiness | Incrementality Check | Recommended Action | Expected Impact | Risk | Confidence | Priority Score.

For every top recommendation include current spend, current ad sales, current total sales, proposed spend/bid change, expected incremental clicks/orders/sales, expected ACoS/TACoS effect, expected contribution profit impact, BSR/rank impact hypothesis if relevant, risk, confidence, and monitoring trigger.

### 4. Ads-Wise Findings

Break down campaigns to scale, keywords/search terms to isolate or increase bids on, product targets to expand, placement changes, wasted spend, bid-down candidates, strong ad-efficiency products, listing-before-spend products, and budget reallocation recommendations.

### 5. BSR-Wise Findings

Break down ASINs gaining rank, ASINs losing rank, rank momentum worth funding, good BSR with weak ad support, poor BSR response to spend, competitor/category context, event overlays, and likely causes of rank movement.

### 6. ASIN-Level Recommendations

For each key ASIN include: current situation, economics, retail-readiness gates, ads diagnosis, BSR/organic diagnosis, incrementality read, growth thesis, recommended next actions, expected impact, risk, and what to monitor over 7, 14, and 30 days.

### 7. Campaign And Keyword Actions

For each action specify: campaign name, ad group, target/keyword/search term, match type, current performance, threshold evidence, recommended action, suggested bid/budget/placement direction, reasoning, risk, confidence, and approval status if execution is possible.

### 8. Budget Reallocation Plan

Explain whether to scale spend, reallocate spend, hold, improve listings first, focus on rank growth, focus on profitability, reduce waste, protect winners, or build new opportunities. Split budget guidance across high-efficiency, ranking, defensive, product targeting, wasteful, exploration, and test campaigns.

### 9. Watchlist

Include what to watch, why it matters, trigger condition, and recommended response if the trigger happens. Use watchlist instead of action when sample size is thin or data is missing.

### 10. Questions / Missing Data

End with concise missing data that would improve the analysis. Prioritize SKU economics, total sales/TACoS, BSR category, inventory, Featured Offer/Buy Box, conversion, review/rating, search term detail, budget usage, placement data, purchased product data, organic rank, competitor movement, and comparison-period coverage.

## Daily Short Version

When the user asks for a shorter daily version, produce:

- Top 3-7 opportunities with ASIN/campaign, ads signal, BSR/organic signal, diagnosis, action, expected impact, score, confidence, risk, and monitoring trigger.
- Top 3 risks or blockers.
- Budget stance: scale, reallocate, hold, reduce waste, fix retail first, investigate, or controlled test.
- Missing data that materially limits confidence.

## Guardrails

- Do not invent missing metrics, ASINs, search terms, categories, competitors, economics, or margin targets.
- Do not recommend negative keywords or pauses without current waste evidence and threshold support.
- Do not recommend budget cuts as the default growth answer; check harvesting, bids, placements, listing readiness, and incrementality first.
- Do not merge SP, SB, and SD conclusions when ad-type separation matters.
- Do not compare BSR across unrelated categories as if ranks are equivalent.
- Do not overfit to tiny samples; call out low click/order volume.
- Do not present ad-to-BSR correlation as proof of causation.
- Do not present efficient branded/defensive spend as incremental without total-sales and TACoS support.
- Do not recommend rank-growth spend from BSR alone.
- Do not hide blocked or stale data surfaces. State the gap and continue with valid analysis.
- Keep recommendations concrete: increase budget, raise bid, lower bid, adjust placement, isolate exact term, add product target, add scoped negative, split campaign, fix listing, protect winner, run controlled test, watch trigger, or investigate cause.

## Example Output Structure

```markdown
## Executive Summary
- Date range:
- Comparison period:
- Business goal:
- Biggest opportunity:
- Biggest risk:
- Budget stance:
- Confidence:

## Data Coverage And Trust
| Source | Available? | Date Range | Grain | Caveat |

## Top Growth Opportunities
| Rank | ASIN / Product | Type | Ads Signal | BSR / Organic Signal | Retail Readiness | Incrementality | Action | Expected Impact | Risk | Confidence | Score |
|---:|---|---|---|---|---|---|---|---|---|---|---:|

## Ads-Wise Findings
### Campaigns To Scale
### Keywords/Search Terms To Harvest
### Product Targets To Expand
### Placement Changes
### Wasted Spend And Bid-Down Candidates
### Listing-Before-Spend Cases
### Budget Reallocation

## BSR-Wise Findings
### Rank Momentum Worth Funding
### Rank Declines To Investigate
### Good BSR With Weak Ad Support
### Poor BSR Response To Spend
### Competitor And Event Context

## ASIN-Level Recommendations
### ASIN / Product
- Current situation:
- Economics:
- Retail-readiness gates:
- Ads diagnosis:
- BSR / organic diagnosis:
- Incrementality read:
- Growth thesis:
- Next actions:
- Expected impact:
- Risk:
- Monitor 7 / 14 / 30 days:

## Campaign And Keyword Actions
| Campaign | Ad Group | Target / Keyword / Search Term | Match Type | Current Performance | Threshold Evidence | Action | Bid/Budget/Placement Direction | Reasoning | Risk | Confidence |

## Budget Reallocation Plan
## Watchlist
## Questions / Missing Data
```
