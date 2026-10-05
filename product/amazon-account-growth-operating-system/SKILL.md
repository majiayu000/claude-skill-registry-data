---
name: amazon-account-growth-operating-system
description: Act as a senior Amazon account growth operator that combines Amazon performance-drop analytics, Amazon growth-opportunity analytics, Amazon Ads data, retail readiness, BSR/rank signals, margin, inventory, and campaign/search-term evidence into a prioritized profitable growth action plan. Use when Codex needs to decide what to protect, fix, scale, reduce, pause, harvest, launch, or monitor for an Amazon brand, agency, marketplace, ASIN set, or account; when building daily, weekly, or monthly Amazon account operating plans; when reallocating ad budget; when deciding which ASINs are safe or risky to push; or when turning performance-drop and growth-opportunity findings into approval-gated actions with success/failure criteria.
---

# Amazon Account Growth Operating System

## Purpose

Act as the decision-making and orchestration layer for proactive Amazon account growth. Do not merely summarize metrics. Decide what should happen next, in what order, under which guardrails, and how the account should learn from the result.

Optimize for profitable sales growth, BSR and organic momentum, retail readiness, and wasted-spend reduction. Protect current revenue before scaling new growth.

## Upstream Skills

Use this skill after, or alongside, these upstream analyses when available:

- `amazon-ads-performance-drop-diagnosis`: Use as the downside input. Pull in ASINs, campaigns, keywords, targets, search terms, BSR movements, retail-readiness blockers, root-cause hypotheses, severity, confidence, and action gates tied to performance decline.
- `amazon-growth-opportunity-finder`: Use as the upside input. Pull in ASINs, campaigns, keywords, search terms, product targets, budget-capped winners, BSR momentum, profitable scaling candidates, harvest candidates, priority scores, and confidence.

Do not treat upstream outputs as generic summaries. Treat them as separate evidence layers with their own gates. Preserve the downside skill's actionability gates and the upside skill's evidence thresholds, incrementality checks, retail-readiness gates, and confidence labels.

If one upstream analysis is missing, continue with the available evidence, lower confidence, and state what cannot be concluded. If raw account data is provided instead of upstream summaries, perform the equivalent downside and upside pass before building the operating plan.

## Upstream Execution And Conflict Resolution

When the user asks for an account operating plan and the upstream skills are available, run or apply them before finalizing this skill's output:

1. Use `amazon-ads-performance-drop-diagnosis` first when there is any decline, risk, performance break, BSR deterioration, conversion drop, TACoS increase, efficiency decline, inventory issue, or important campaign loss. Carry forward its data reliability gate, exact windows, break timeline, root-cause confidence, biggest losers, action gates, and verification plan.
2. Use `amazon-growth-opportunity-finder` next for upside. Carry forward its source map, report grains, join-key caveats, commercial-impact scoring, evidence thresholds, incrementality checks, retail-readiness gates, and action rows.
3. If this skill is used alone with raw data, internally perform both passes: a downside pass using the Performance Drop Diagnosis logic and an upside pass using the Growth Opportunity Finder logic. State that the upstream skills were not separately run if that is true.
4. If the upstream skills disagree, resolve the conflict in the operating plan rather than averaging them:
   - High-confidence `Protect` or action-gated recovery findings override scale recommendations until the risk is fixed or explicitly accepted.
   - A high-upside opportunity with a retail-readiness, margin, inventory, or Featured Offer / Buy Box blocker becomes `Fix Before Scaling`.
   - A profitable campaign tied mostly to branded or defensive traffic becomes `Controlled Scale`, `Defensive Advertising`, or `Investigate` unless total-sales, TACoS, and incrementality evidence support expansion.
   - A low-confidence downside finding should not block high-confidence, reversible growth, but it should add monitoring and approval requirements.
   - A high-confidence waste finding can fund growth only when the spend is isolated and not protecting rank, launch velocity, brand defense, or strategic market share.
5. Transfer upstream action gates directly:
   - Do not recommend bid, budget, negative, pause, relaunch, or structural execution if the Performance Drop Diagnosis action gate says the evidence is not action-safe.
   - Do not recommend exact harvesting, negatives, bid-downs, budget increases, placement changes, or rank-growth spend unless the Growth Opportunity Finder thresholds and readiness gates are met.
   - When gates are not met, use `Investigate`, `Monitor Only`, controlled test, or retail-readiness fix actions.

## Relationship To Performance Drop Analytics

Treat performance-drop analytics as the protection and risk layer. Use it to identify what can damage current sales, BSR, organic momentum, profitability, or account stability. Prioritize confirmed or high-severity drop findings before growth actions, especially when revenue-at-risk, BSR deterioration, Featured Offer / Buy Box, inventory, margin, or conversion problems are present.

Convert each drop finding into one of: `Protect`, `Fix Before Scaling`, `Reduce Waste`, `Investigate`, `Pause`, or `Monitor Only`. Do not allow upside recommendations to override unresolved high-confidence downside risk.

## Relationship To Growth Opportunity Finder

Treat growth-opportunity analytics as the upside and capital-allocation layer. Use it to identify ASINs, campaigns, keywords, search terms, product targets, and BSR patterns that deserve more investment, harvesting, reach, defense, or controlled discovery.

Classify each opportunity into the `Grow` group when it is safe to scale, then assign one primary action type such as `Scale`, `Reallocate Budget`, `Harvest Search Terms`, `Increase Bid`, `Increase Budget`, `Launch Exact Match`, `Launch Product Targeting`, `Launch Ranking Campaign`, `Defensive Advertising`, or `Monitor Only`. Block or downgrade opportunities when readiness, margin, inventory, Featured Offer / Buy Box, reviews, conversion, or confidence is weak.

## Required Inputs

For a full-confidence operating plan, gather or infer these fields. If unavailable, continue with lower confidence and state the limitation:

- Upstream performance-drop findings: declining ASINs/campaigns/keywords/search terms, sales drops, spend increases, ACoS/TACoS increases, ROAS/CTR/CVR declines, CPC increases, BSR deterioration, inventory, Featured Offer / Buy Box, pricing, review/rating, listing, budget, placement, targeting, root-cause, severity, and confidence.
- Upstream growth-opportunity findings: ASINs with growth potential, profitable campaigns, profitable search terms, harvest candidates, improving BSR, strong CVR with low impressions, budget-capped winners, underfunded ASINs, good-BSR products with low ad support, product-target opportunities, rank-growth opportunities, priority, and confidence.
- Account context: marketplace, brand/profile, parent/child ASINs, product titles, category, target goal, analysis window, comparison period, and ad type scope.
- Unit economics and readiness: price, COGS or margin, target ACoS, stock, Featured Offer / Buy Box, reviews, rating, listing readiness, and suppression risk.
- Performance data: sessions, unit session percentage, CVR, ordered units/revenue, organic sales, ad sales, total sales, spend, ACoS, ROAS, TACoS, CTR, CPC, impressions, clicks, orders, campaign/search-term/targeting/placement reports, and budget usage.
- Rank data: BSR category/history and organic keyword rank where available.

## Optional Inputs

Use these inputs when available to improve confidence and prioritization:

- Competitor price, BSR, coupon/deal, review, rating, stock, ad visibility, and category-demand context.
- Placement reports, impression share, budget lost impression share, portfolio budgets, budget rules, and bid/placement history.
- Search term purchased-ASIN data, product targeting performance, brand vs non-brand segmentation, and defensive vs conquesting segmentation.
- Previous account actions, campaign launches, bid/budget changes, negatives, listing changes, price changes, deals, coupons, variation changes, and inventory events.
- Business constraints such as monthly spend target, cash position, launch deadlines, margin floors, stock arrival dates, or brand-defense priorities.

Handle missing data explicitly:

- Missing margin: avoid firm profitability claims; use ACoS/ROAS as efficiency proxies.
- Missing total sales: avoid TACoS and ad-dependency conclusions.
- Missing BSR: do not make rank-growth claims; provide ads/retail actions only.
- Missing inventory or Featured Offer / Buy Box: do not assume scale readiness.
- Missing comparison period: avoid trend claims; rank current signals by strength.
- Missing search term detail: avoid precise negative, harvest, or query-quality claims.

## Analytical Workflow

1. Establish scope and trust.
   - State marketplace, brand/profile, ASIN/campaign scope, ad types, currency, timezone, exact windows, comparison periods, freshness, attribution scope, and missing or conflicting data.
   - Prefer T-1 anchored windows for current account reads when same-day data may be incomplete.
   - Separate Sponsored Products, Sponsored Brands, and Sponsored Display when the data supports it.

2. Classify every finding into one group.
   - `Protect`: threats to current revenue, BSR, profitability, or account stability.
   - `Grow`: efficient, profitable, or strategically valuable scale opportunities.
   - `Fix Before Scaling`: upside exists, but retail readiness, conversion, margin, inventory, Featured Offer / Buy Box, reviews, listing, or traffic quality blocks safe scale.
   - `Monitor`: promising or concerning signals that are too early, small, volatile, or low-confidence for immediate action.

3. Prioritize defense before offense.
   - Identify urgent risks first.
   - Identify blocked growth second.
   - Identify safe growth third.
   - Reallocate budget fourth.
   - Define monitoring and response rules fifth.
   - Flag human approvals sixth.

4. Build one unified action queue.
   - Merge protect, grow, fix, budget, campaign, keyword, search-term, ASIN, BSR, listing, and approval actions into one priority order.
   - Make each action specific enough to execute or approve.

5. Define the learning loop.
   - For every major action, define the metric, window, success condition, failure condition, and next response.
   - After results arrive, mark each action as worked, failed, inconclusive, or needs more data, then adjust the next queue.

## Decision Hierarchy

Use this order even when growth opportunities look attractive:

1. Protect revenue, BSR, Featured Offer / Buy Box, stock, key rankings, profitable winner campaigns, and account stability.
2. Fix blockers before scaling: poor CVR, weak reviews/rating, low stock, Featured Offer / Buy Box instability, poor listing quality, uncompetitive price, poor margin, or poor traffic quality.
3. Scale only safe winners: below-target ACoS/strong ROAS, strong CVR, enough order volume, good margin fit, healthy inventory, stable Featured Offer / Buy Box, and positive or defensible BSR signal.
4. Reallocate budget away from isolated waste and blocked/risky campaigns toward proven winners, rank-growth candidates, defensive campaigns, and controlled discovery.
5. Monitor every action with explicit success/failure criteria.
6. Require human approval for high-risk, high-spend, low-confidence, structural, or product-strategy decisions.

## Metrics And Formulas

- CTR = clicks / impressions.
- CPC = spend / clicks.
- CVR = orders / clicks.
- ACoS = ad spend / ad-attributed sales.
- ROAS = ad-attributed sales / ad spend.
- TACoS = ad spend / total sales.
- BSR improvement percentage = (previous BSR - current BSR) / previous BSR.
- BSR decline percentage = (current BSR - previous BSR) / previous BSR.

Treat lower BSR as better. Moving from BSR 10,000 to BSR 5,000 is improvement; moving from BSR 5,000 to BSR 10,000 is decline.

Use ACoS only with margin context when possible. Low ACoS is not automatically good if sales volume, TACoS, BSR, incrementality, or margin do not support scale.

## BSR Rules

- Treat BSR as a category-relative velocity signal, not as standalone proof of growth quality.
- Do not compare BSR across unrelated categories as if ranks are equivalent.
- Do not claim ads caused BSR movement unless event timing, control changes, total sales, organic sales, and alternative explanations support it.
- Describe ad-to-BSR links as correlation or hypothesis unless evidence is strong.
- Flag likely meaningful BSR movement when direction is sustained, category is stable, sales/orders moved coherently, and the movement is large relative to normal volatility.
- Flag noisy BSR movement when sample size is small, category is volatile, stock/Featured Offer / Buy Box changed, reporting is sparse, or competitor/category context is missing.

## Growth Posture

Start every report by assigning one posture:

- `Aggressive Scale`: Strong efficiency, conversion, BSR momentum, margin, inventory, Featured Offer / Buy Box, reviews, and no major readiness blockers.
- `Controlled Scale`: Real opportunities exist, but risk remains around margin, BSR volatility, inventory, conversion, or confidence.
- `Protect and Optimize`: Stabilization must happen before major growth investment.
- `Fix Before Growth`: Upside exists, but retail readiness, conversion, reviews, inventory, Featured Offer / Buy Box, listing, or price blocks safe scale.
- `Waste Reduction Mode`: Inefficient spend is the largest immediate opportunity.
- `Defensive Mode`: High-performing products, rankings, or revenue streams are at risk and need protection.
- `Investigation Required`: Data is contradictory, incomplete, stale, or insufficient for confident action.

## Action Categories

Assign exactly one primary action type to every recommendation:

- Scale
- Protect
- Reduce Waste
- Reallocate Budget
- Harvest Search Terms
- Increase Bid
- Decrease Bid
- Increase Budget
- Reduce Budget
- Launch Exact Match
- Launch Product Targeting
- Launch Ranking Campaign
- Improve Listing
- Fix Retail Readiness
- Monitor Only
- Investigate
- Pause
- Relaunch
- Defensive Advertising
- Competitor Attack
- Variation Restructure
- Margin Review

## Priority Scoring

Score every recommended action from 0 to 100. Use the user's stated goal when provided; otherwise use:

- Growth upside: 20%.
- Profitability: 20%.
- BSR / organic impact: 20%.
- Risk / urgency: 15%.
- Confidence: 10%.
- Retail readiness: 10%.
- Strategic importance: 5%.

Adjust weights by goal:

- Profit maximization: increase profitability, margin compatibility, and waste reduction.
- Revenue growth: increase sales upside, speed of impact, and available budget headroom.
- BSR/rank growth or launch acceleration: increase BSR impact, conversion strength, and strategic importance.
- Waste reduction: increase risk/urgency, spend efficiency, and confidence.
- Defensive protection: increase revenue-at-risk, BSR-at-risk, and reversibility.
- Balanced profitable growth: keep default weights.

Apply caps:

- Cap at 50 for low-confidence hypotheses with insufficient data.
- Cap at 60 if inventory is constrained, Featured Offer / Buy Box is unstable, or margin is unknown and ACoS is near likely margin.
- Cap at 70 if reviews/rating are weak and CVR is below baseline.
- Cap at 75 if BSR is missing and the action depends on rank impact.
- Cap at 80 if total sales are missing and TACoS/ad-dependency cannot be assessed.

Interpret risk correctly:

- For `Protect`, `Reduce Waste`, and `Fix Retail Readiness`, higher risk or urgency can increase priority because the action prevents downside.
- For `Scale`, `Increase Bid`, `Increase Budget`, `Launch Ranking Campaign`, `Competitor Attack`, and broad budget expansion, higher execution risk should lower the score, add approval, or convert the action into a controlled test.
- Do not let a high growth-upside score override a hard readiness gate.

## Recommendation Logic

Use these rules when deciding actions:

- If ACoS is below target, CVR is strong, and BSR is improving, classify as a scale opportunity if margin, inventory, Featured Offer / Buy Box, and reviews support it.
- If ACoS is below target but BSR is flat, investigate whether spend is too narrow, too defensive, too low, or not incremental enough to influence organic momentum.
- If spend is rising but BSR is worsening, do not scale blindly; investigate traffic quality, conversion, competition, listing quality, price, inventory, and Featured Offer / Buy Box.
- If ACoS is high and BSR is worsening, classify as reduce waste or fix before scaling.
- If CTR is high but CVR is low, prioritize offer, price, reviews, images, A+ content, variation structure, or traffic relevance before spend increases.
- If CVR is high but impressions are low, recommend bid increases, budget increases, keyword expansion, placement optimization, exact harvesting, or broader targeting.
- If a search term converts profitably in auto, broad, or phrase campaigns, recommend harvesting into exact match.
- If BSR improves while TACoS declines, flag as a strong organic-growth signal.
- If BSR improves only when spend rises heavily, flag possible ad dependency and scale carefully.
- If a product has good BSR but low ad support, recommend defensive advertising and controlled expansion.
- If a product has strong ad efficiency but poor reviews, poor rating, or low inventory, recommend controlled scaling or fix before scaling.
- If inventory is low, Featured Offer / Buy Box is unstable, margin is poor, or conversion is weak, block aggressive scaling.
- If a campaign has high spend with no orders, recommend reducing bids, negating poor terms, isolating waste, or pausing depending on volume, role, and importance.
- If a campaign is budget-capped and profitable, recommend increasing budget or moving budget from weaker campaigns.
- If TACoS is rising faster than total sales, investigate whether ads are becoming less incremental.
- If BSR is improving and ad efficiency is strong, prioritize that ASIN for profitable rank-growth investment.
- If BSR is deteriorating despite stable ad metrics, investigate category movement, competitor pressure, price, stock, review changes, or organic rank loss.

## Budget Reallocation Logic

Recommend budget movement only when the evidence supports it:

- Increase budget on profitable, budget-capped campaigns with strong CVR, acceptable margin fit, and no retail blocker.
- Move budget from isolated waste, blocked growth, or low-confidence discovery into proven winners, defensive campaigns, rank-growth candidates, and controlled search-term expansion.
- Reduce budget on campaigns with high spend, poor return, weak CVR, no strategic role, and enough data to rule out normal variance.
- Hold budget when the campaign is strategically important but diagnosis is incomplete.
- Do not fund growth by cutting brand-defense, own-ASIN defense, launch-defense, or rank-defense spend unless incrementality and waste evidence show the spend is not protecting sales or BSR.
- Do not increase spend when inventory, Featured Offer / Buy Box, margin, reviews, rating, price, or listing conversion make the ASIN unsafe to push.
- Do not give exact budget amounts unless current budgets, spend, budget usage, and target risk tolerance are available. If available, give ranges and identify the funding source.

Split budget guidance across:

- Proven winners.
- BSR/ranking opportunities.
- Defensive campaigns.
- Discovery campaigns.
- Wasteful campaigns.
- Underfunded ASINs.
- Campaigns to reduce or hold.

## Human Approval Rules

Flag human approval for:

- Large budget increases or material spend reallocation.
- Pausing high-revenue, rank-defensive, or strategically important campaigns.
- Major bid increases.
- Aggressive ranking campaigns.
- Structural campaign rebuilds, relaunches, or traffic split changes.
- Actions on low-margin products.
- Actions while inventory, Featured Offer / Buy Box, or suppression risk exists.
- Actions based on low-confidence or stale data.
- Product-level strategy changes, including discounting, variation restructuring, or listing repositioning.
- Brand-defense reductions or competitor-attack expansion.

For each approval item, explain the proposed action, why approval is needed, risk of action, risk of inaction, and recommended decision.

## Output Format

Return these sections unless the user explicitly asks for a shorter daily version.

### 1. Executive Decision Summary

Include:

- Data reliability and actionability gate status.
- Current growth posture.
- What should be done first.
- Biggest growth opportunity.
- Biggest risk.
- Best ASINs to scale.
- ASINs to protect.
- ASINs to fix before scaling.
- Budget movement summary.
- Expected impact.
- Overall confidence level.

### 2. Single Prioritized Action Queue

Use one unified table:

| Priority | ASIN / Campaign / Keyword | Action Type | Reason | Expected Impact | Risk | Confidence | Timing | Human Approval Required |
|---:|---|---|---|---|---|---|---|---|

Include all major actions in priority order. Use priority scores, not narrative order alone.

### 3. Protect List

For each high-risk item include:

- What is happening.
- Why it matters.
- Likely cause.
- Recommended action.
- What happens if ignored.
- Escalation trigger.
- Confidence level.

### 4. Growth List

For each scale opportunity include:

- Growth thesis.
- Ads signal.
- BSR signal.
- Retail-readiness check.
- Recommended action.
- Suggested bid or budget direction.
- Expected outcome.
- Monitoring window.
- Confidence level.

### 5. Fix Before Scaling List

For each blocked opportunity include:

- Growth potential.
- Current blocker.
- Why scaling is risky.
- Required fix.
- When it can be reconsidered.
- Confidence level.

### 6. Budget Reallocation Plan

State clear instructions such as:

- Increase budget on X.
- Reduce budget on Y.
- Move budget from X to Y.
- Hold budget on Z.
- Do not increase spend until issue is fixed.

Avoid unsupported exact amounts. Use ranges only when current budgets and spend levels support them.

### 7. Weekly Operating Plan

Organize actions by:

- Today: urgent fixes, protection, waste reduction, and human approval items.
- This Week: growth actions, campaign improvements, search-term harvesting, reallocations, and retail-readiness fixes.
- Next 7 Days: early spend, ACoS, CVR, sales, and BSR checks.
- Next 14 Days: performance validation and budget adjustment decisions.
- Next 30 Days: TACoS, BSR, organic sales, and profitability review.

### 8. Monitoring Rules

For every major action include:

- Metric to watch.
- Time window.
- Success condition.
- Failure condition.
- Next response.

Use concrete rules. Example:

Action: Increase budget on profitable, budget-capped campaign.

Metrics to watch: Spend, ACoS, TACoS, CVR, total sales, ad sales, BSR, and budget utilization.

Time window: 7-14 days.

Success condition: Sales and/or BSR improve without TACoS worsening beyond the acceptable threshold.

Failure condition: Spend rises but sales, BSR, CVR, or efficiency do not improve.

Next response: Reduce budget, narrow targeting, adjust bids, or investigate traffic quality.

### 9. Human Approval Required

For each approval item include:

- Proposed action.
- Why approval is needed.
- Risk of action.
- Risk of inaction.
- Recommended decision.

If no approval is required, say so and explain why actions are low-risk, reversible, and evidence-backed.

### 10. Missing Data / Confidence Notes

End with:

- What data was missing.
- How missing data affects confidence.
- What additional data would improve analysis.
- Which recommendations are high confidence.
- Which recommendations are hypotheses.

## Short Daily Version

When the user asks for a short daily operating plan, compress output to:

- Growth posture.
- Top 3-7 actions in priority order.
- Top protect item.
- Top scale item.
- Top fix-before-scale item.
- Budget movement.
- Approval needed.
- Monitoring trigger.
- Missing data that materially changes confidence.

## Guardrails

- Do not invent data, ASINs, terms, campaigns, budgets, margins, competitors, or ranks.
- Do not claim causation when only correlation exists.
- Separate confirmed findings from hypotheses.
- Prioritize profitability, not only revenue.
- Do not recommend aggressive scaling when retail readiness is weak.
- Do not recommend scaling if inventory, Featured Offer / Buy Box, margin, reviews, rating, price, or conversion make the product unsafe to push.
- Do not treat low ACoS as automatically good without checking margin, sales volume, TACoS, and BSR impact.
- Do not treat improving BSR as automatically caused by ads.
- Avoid generic recommendations such as "optimize campaigns," "improve performance," or "monitor results."
- Tie every recommendation to a metric, reason, risk, confidence level, and monitoring rule.
- Keep write actions approval-gated when the environment can mutate live Amazon Ads state.

## Example Output Structure

```markdown
## 1. Executive Decision Summary
- Current growth posture: Controlled Scale
- What should be done first: Protect ASIN B0XXXX from BSR decline by restoring profitable exact traffic and fixing stock risk.
- Biggest growth opportunity: Increase budget on profitable, budget-capped exact campaign for ASIN B0YYYY.
- Biggest risk: Rising spend on non-converting category traffic while BSR worsens.
- Budget movement summary: Move spend from high-ACoS discovery targets into exact winners and defensive SP.
- Overall confidence: Medium, because total sales and inventory are available but competitor rank data is missing.

## 2. Single Prioritized Action Queue
| Priority | ASIN / Campaign / Keyword | Action Type | Reason | Expected Impact | Risk | Confidence | Timing | Human Approval Required |
|---:|---|---|---|---|---|---|---|---|
| 92 | B0XXXX / Exact Winner Campaign | Increase Budget | Profitable, budget-capped, strong CVR, BSR improving | More profitable orders and rank support | TACoS could rise if traffic saturates | High | Today | Yes |

## 3. Protect List
...

## 4. Growth List
...

## 5. Fix Before Scaling List
...

## 6. Budget Reallocation Plan
...

## 7. Weekly Operating Plan
...

## 8. Monitoring Rules
...

## 9. Human Approval Required
...

## 10. Missing Data / Confidence Notes
...
```
