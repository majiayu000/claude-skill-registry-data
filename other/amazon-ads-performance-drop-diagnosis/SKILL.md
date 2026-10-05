---
name: amazon-ads-performance-drop-diagnosis
description: Diagnose why Amazon advertising performance declined for a product, ASIN, campaign, marketplace, or account. Use when the user asks why sales, orders, ROAS, ACOS, TACoS, profit, BSR, rank, traffic, conversion rate, or campaign performance dropped, asks for dropped campaigns, says investigate drop/drop analysis, or asks about wasted spend, negative keywords, negative targets, keywords, targets, or search terms in a drop context.
---

# Amazon Ads Performance Drop Diagnosis

## Objective

Diagnose the cause of a decline. Do not produce a generic performance recap. Trace when the break started, quantify the impact, isolate the entities causing the loss, connect ads movement to BSR/rank movement, and recommend only the actions supported by evidence gates. Protect sales velocity and organic momentum; do not optimize only for lower ACOS or lower spend.

## Public-Safe And Vendor-Neutral Guidance

This skill is intended for reusable public guidance. Do not include client-sensitive, account-sensitive, competitor-sensitive, or private examples in the skill, its references, or generated reusable templates. Use synthetic examples only when examples are necessary.

Do not depend on or name any specific third-party retail-data vendor. Refer generically to `retail intelligence data`, `rank history`, `offer snapshot`, `cached retail data`, or `external retail data source`.

## Repeatable Drop Analysis Flow

Use this flow in order for every account, ASIN, campaign, marketplace, or product performance-drop diagnosis unless the user explicitly narrows the scope. If Rocketcart tools are available, use Rocketcart trusted data/API paths and canonical optimization endpoints. Screenshots and stale exports are validation inputs only and must not drive optimization recommendations.

### Default Periods

- Freshness check: latest trusted reporting date; anchor recent analytics on T-1.
- Drop window: T-7 through T-1 unless the user supplies a dated incident window.
- Baseline window: T-14 through T-8 unless the user supplies a better matched baseline.
- Control-change audit: at least 14 days before the break through the drop window; expand to 30 days when changes are sparse, delayed, or disputed.
- Retail, rank, and competitor context: 30-90 days when dated history is available, plus current-state snapshots for offer/readiness checks.

For any explicit audit, print the exact baseline and drop dates used. Do not compare partial current-day data against completed historical days.

### Flow 1: Account Drop Sizing

1. Confirm profile/account, marketplace, currency, and timezone.
2. Validate data freshness and define T-1 anchored baseline and drop windows.
3. Compare account KPIs: sales, orders, spend, ROAS, ACoS, CVR, CPC, impressions, clicks, CTR, and AOV/ASP when available.
4. Split by SP, SB, and SD when the data supports it.
5. Classify whether the drop is sales-volume, efficiency, traffic, conversion, AOV/ASP, query/placement mix, control-change, retail-readiness, rank, or market driven.
6. Output an account-level verdict with exact dates, the primary ad type or scope causing the drop, and whether ASIN-level drilldown is required.

### Flow 2: ASIN Drop Contribution

1. Aggregate performance by advertised ASIN and, where available, purchased ASIN.
2. Compare baseline vs drop windows for each ASIN.
3. Calculate absolute sales/order drop, per-day drop, percent change, and percent contribution to the total account drop.
4. Group parent/child or variation ASINs where relevant and label ambiguity.
5. Flag attribution risk as `Clean ASIN`, `Halo-heavy`, `Mixed campaign`, or `Unknown`.
6. Select priority ASINs by contribution, business importance, and actionability.
7. Output a ranked ASIN drop table and the ASINs selected for deep diagnosis.

### Flow 3: Retail Signals Check-Up Of Each Dropped ASIN

1. Check stock/availability and Featured Offer / Buy Box status.
2. Check price, coupon, promo, deal, and delivery promise.
3. Check BSR/rank movement before, during, and after the drop when dated rank history exists.
4. Check review count, rating, listing suppression, content, and variation issues.
5. Check competitor movement: price, coupon, rank, reviews, availability, and offer strength where available.
6. Compare timing: did a retail or competitor move happen before ads performance broke?
7. Output a retail cause verdict per ASIN: `Likely`, `Possible`, `Rejected`, or `Missing Data`.

### Flow 4: Deep ASIN Ads Diagnosis

1. Filter ads data to dropped ASINs.
2. Split by campaign, ad group, keyword/target, search term, placement, product ad, and ad type where available.
3. Run bridge math: impressions -> clicks -> spend -> orders -> CVR -> sales -> ROAS.
4. Identify whether each ASIN lost traffic, conversion, AOV/ASP, placement quality, query mix, or budget/bid/state support.
5. Separate brand, generic, auto, competitor, own-ASIN defense, discovery, launch/rank-defense, and exploratory traffic when data supports it.
6. Compare SP, SB, and SD where available.
7. Output the exact ads driver per ASIN and the top broken routes.

### Flow 5: Lost-Traction Target Isolation

1. For each dropped ASIN, compare target-level baseline vs drop performance.
2. Flag targets losing sales, orders, impressions, clicks, spend, CVR, ROAS, placement quality, or query relevance.
3. Rank targets by sales loss first, then order loss, then strategic relevance.
4. Mark target type: keyword, auto target, product target, category target, search term, placement, or product ad route.
5. Preserve exact IDs when available: campaign ID, ad group ID, keyword ID, target ID, product ad ID, and serving state.
6. Output a lost-traction target table with `what exactly dropped` per row.

### Flow 6: Mixed-ASIN Safety Check

1. Check whether each campaign/ad group advertises one ASIN or multiple ASINs.
2. Check purchased-ASIN distribution, same-SKU share, other-SKU halo, and brand/view-through attribution risk.
3. Mark each target/action candidate as `Action-safe`, `Directional`, or `Blocked`.
4. Downgrade mixed-ASIN rows unless ASIN attribution is clean enough for the proposed action.
5. Prevent unsafe conclusions such as cutting a target that helps another ASIN or suppresses brand/rank defense.
6. Output a safety gate beside every target and action candidate.

### Flow 7: Bid / State / Placement / Budget / Negative Keywords Change Audit

1. Build a 14-30 day control-change timeline.
2. Check bids for each lost target: decreases, increases, or unchanged.
3. Check keyword/target state: enabled, paused, archived, newly created, or removed.
4. Check campaign, ad group, and product-ad state changes.
5. Check budget and placement changes, including Top of Search, Rest of Search, and Product Pages where available.
6. Check negative keywords and negative product targets added, removed, archived, or unarchived.
7. Verify attachment: was the negative applied to the campaign/ad group serving the dropped ASIN or route?
8. Verify timing: did the change happen before or during the drop, not only after it as a fix?
9. Output a control-change table beside each dropped target with a causality label.

### Flow 8: Final Causality Read

1. Combine account, ASIN, retail, ads, target, mixed-ASIN, and control-change evidence.
2. Separate facts from hypotheses.
3. Assign a cause label per ASIN and target: `Confirmed`, `Likely`, `Directional`, `Rejected`, or `Missing Data`.
4. Identify primary cause, secondary causes, and non-causes.
5. Convert findings into recovery actions, but keep writes approval-gated.
6. Define monitoring windows: 3 days, 7 days, and 14 days.
7. Output the final `what dropped and why` narrative plus action-safe next steps.

## Required Inputs

Gather, derive from available data, or mark unavailable before diagnosing:

- Marketplace, profile/account, currency, timezone, and ASIN/product/campaign scope.
- Suspected drop window and baseline comparison period, defaulting to the T-1 anchored windows above.
- Primary KPI and target KPI, such as sales, orders, ACOS, TACoS, ROAS, BSR, profit, or rank.
- Amazon Ads metrics by SP/SB/SD where available: spend, sales, orders, impressions, clicks, CTR, CPC, CVR, ACOS, ROAS, budgets, budget usage, placements, campaigns, ad groups, keywords, targets, search terms, product ads, advertised ASINs, and purchased ASINs.
- Total retail sales/orders for TACoS or organic-momentum claims; if unavailable, do not diagnose TACoS.
- BSR/rank history for the affected advertised ASINs, including category and date granularity.
- Retail intelligence freshness/coverage labels before making BSR/rank trend claims; distinguish dated trend history from a point-in-time offer or rank snapshot.
- Retail readiness: Buy Box, stock, suppression, Prime/FBA/shipping promise, price, coupon/promo/deal, reviews/ratings, listing/content changes, and parent/child variation changes.
- Change history: bids, budgets, placements, campaign/ad group/keyword/target/product ad states, negatives added/removed/archived/unarchived, newly enabled or removed keywords/targets, product ad mapping, campaign launches, pauses, portfolio budgets, budget rules, automated rules, bulk edits, and third-party optimization changes.
- Optimization memory status and event history: check shared optimization memory first, including intent/applied/failed/unknown events, pending evaluations, entity history, and any local-only/spool warnings; use legacy changelogs only as fallback or explicit import evidence.
- Negative and waste evidence: current negative keyword and negative product-target inventory for affected campaigns/ad groups; zero-order waste for targets, keywords, and search terms across L7, L14, and L30; search-term and target history for affected routes; and timing confidence for any negative or target change.
- Competitor/category context: competitor BSR/rank, price, coupon/deal, reviews/ratings, stock, ad visibility, and category demand where available.

## Diagnostic Gates

Start every diagnosis with a data reliability and actionability gate:

- Classify the case as `Actionable`, `Directional`, or `Non-actionable`.
- Print exact windows, freshness/T-1 status, ad type scope, attribution window, ASIN scope, and any reconciliation gaps.
- Flag mixed-ASIN contamination, brand-halo/view-through risk, reporting lag, missing BSR, missing total sales, missing retail readiness, missing competitor data, or weak sample size.
- For ASIN-scoped work, explicitly state whether product-level KPIs are reliable and whether keyword, target, search-term, negative, bid, and pause actions are `Action-safe`, `Directional only`, or `Blocked` because of mixed-ASIN ad groups, halo/other-SKU attribution, weak sample size, or unresolved retail-readiness risk.
- For any campaign, keyword, target, or search-term drop, complete the `Negative Keyword/Target Multi-Window Gate` from the diagnostic reference before finalizing. If required reads fail or are unavailable, say the negative gate is incomplete and do not present negative, pause, or bid-cut recommendations as action-safe.
- Do not make definitive root-cause claims when missing data could materially change the diagnosis.
- Do not recommend bid, budget, negative, pause, or relaunch execution unless the relevant action gate in the diagnostic reference is satisfied.

## Workflow

1. Establish data coverage, freshness, and exact windows.
   - Anchor recent windows on T-1 when current data may be incomplete.
   - Print exact date ranges used for freshness, drop, baseline, L7, L14, L30, L60, L90, and control-change audit windows.
   - Define any `fresh baseline snapshot` as the current trusted ads, retail/rank, campaign-control, and action-state baseline captured before optimization changes are made.
   - Separate SP, SB, and SD when the data supports it; do not blend ad types unless the user asks for an all-ad-type view.
   - Normalize uneven windows to per-day values before comparing them.

2. Find the break point.
   - Inspect daily or weekly trends for the first sustained change in sales/orders, clicks, impressions, CPC, CVR, ACOS/ROAS, TACoS, budget usage, placement mix, and BSR.
   - Build a control-change timeline for at least 14 days before the break through the drop window, plus any post-drop fixes that should not be treated as root causes.
   - Read shared optimization memory before legacy changelogs so actions from another machine, pending evaluations, unknown writes, and recently applied changes are not missed.
   - For each suspected break date, list budget, bid increase/decrease, placement modifier, campaign/ad group/keyword/target/product ad state, product ad mapping, portfolio, budget rule, automation, negative, newly enabled or removed keyword/target, or structure changes within +/- 7 days.
   - For negative keyword or negative product-target changes, verify whether the changed negative was attached to campaigns/ad groups serving the affected ASIN, whether the blocked/unblocked query or product target had historical sales, whether the ASIN also dropped in untouched campaigns, and whether the change happened before/during the measured drop or only after it.
   - Mark whether the break is abrupt, gradual, intermittent, or isolated to a campaign/entity.

3. Quantify impact and decompose drivers.
   - Build an impact table with baseline, drop window, absolute delta, percent delta, per-day delta, confidence, and driver read.
   - Use bridge math whenever baseline and drop-window metrics exist: impressions, clicks, CTR, CPC, spend, orders, CVR, AOV/ASP, sales, ACOS, and ROAS.
   - Classify the primary driver as traffic loss, CPC inflation, conversion-rate decline, AOV/ASP decline, query/placement mix shift, control-change driven, retail-readiness driven, rank/BSR driven, market driven, or mixed.
   - Include spend efficiency and volume together. ACOS, ROAS, and TACoS changes are symptoms; do not treat them as root causes.

4. Isolate the biggest contributors.
   - Rank campaigns, ad groups, keywords, targets, search terms, product ads, advertised ASINs, and purchased ASINs by lost sales/day, lost orders/day, wasted spend, share of total delta, BSR sensitivity, previous-winner status, current state, and attribution risk.
   - Calculate ASIN-level contribution to the total drop before deep target diagnosis so the investigation starts with the business loss, not with the noisiest entity.
   - Run the negative and waste gate across at least L7, L14, and L30. Separate `negative-change causality`, `new negative candidate`, `target waste`, and `previous winner stopped converting` so waste is not mistaken for the cause of the drop.
   - Preserve campaign ID, ad group ID, keyword/target ID, and product ad ID when target-level loss or recovery actions may follow.
   - Segment query mix into branded defense, own-ASIN defense, category generic, competitor brand, competitor ASIN, auto close/loose/substitute/complement, launch/rank-defense, and exploratory discovery where data supports it.
   - Decompose placements for Top of Search, Rest of Search, and Product Pages when placement data exists.

5. Connect PPC, retail readiness, competitors, and BSR.
   - Compare timing and direction of ad orders, total orders, organic sales proxy, retail-readiness changes, BSR/rank, category demand, and competitor rank/offer movement.
   - Require freshness and coverage labels before making BSR/rank trend claims. Handle multiple BSR/rank category series explicitly, and warn when parent/child or variation-level rank sharing makes ASIN-level rank causality ambiguous.
   - Separate current offer snapshots from dated trend history. A current price, deal, Buy Box, or rank snapshot can support a watch item, but it cannot prove a trend without dated observations.
   - Decide whether PPC decline likely caused rank deterioration, rank deterioration likely weakened PPC, both reinforced each other, or both were driven by retail, competitor, or market movement.
   - Treat BSR as a velocity signal, not a standalone cause. Explain the mechanism and confidence.

6. Recommend recovery actions only after gates.
   - Prioritize restoring qualified traffic, conversion, and rank defense before cosmetic ACOS cuts.
   - Avoid spend cuts when spend defends rank, launch velocity, brand defense, or organic momentum unless waste is clearly isolated and low-risk.
   - Separate facts, likely causes, assumptions, missing data, and watchlist items.
   - Keep write actions approval-gated when the environment supports live mutation.

## Output Format

Always return these sections, in this order:

1. **Data Reliability And Actionability Gate**: available data, missing data, reconciliation issues, attribution/scope risks, sample-size confidence, and whether bid/budget/negative/pause/relaunch recommendations are action-safe.
2. **Executive Verdict**: 3-6 bullets with the most likely cause, confidence, impact, what to do first, and which major causes cannot be ruled out because of missing data.
3. **Account Drop Sizing**: account KPI bridge, exact baseline/drop dates, SP/SB/SD split, primary ad type or scope causing the drop, and whether ASIN drilldown is required.
4. **ASIN Drop Contribution**: ranked ASIN table with absolute sales/order loss, percent contribution, parent/variation grouping, and attribution risk.
5. **Retail Signals Check-Up**: per-ASIN stock, offer, price, promo, delivery, BSR/rank, review/listing, competitor timing, and retail cause verdict.
6. **Deep ASIN Ads Diagnosis**: campaign/ad group/target/search-term/placement bridge math, traffic segment read, and top broken routes.
7. **Lost-Traction Target Isolation**: target-level loss table preserving IDs and stating what exactly dropped per row.
8. **Mixed-ASIN Safety Check**: action-safety gate beside every target and candidate.
9. **Control-Change Audit**: bid, state, placement, budget, negative, and product-ad changes beside each dropped target, with timing, attachment, and causality label.
10. **Final Causality Read**: facts vs hypotheses, cause label per ASIN/target, primary causes, secondary causes, non-causes, and action-safe next steps.
11. **Negative Keyword/Target Multi-Window Gate**: L7/L14/L30 waste summaries for targets, keywords, and search terms; current negative inventory attachment; negative-change causality verdict; negative/pause action-safety; and blocked/watch/action-safe candidates.
12. **BSR And Competitor Interpretation**: whether PPC hurt rank, rank hurt PPC, both reinforced each other, or retail/competitor/market factors drove both.
13. **Recommended Actions**: prioritized by expected impact, confidence, urgency, reversibility, rank/velocity risk, and action-gate status.
14. **Verification Plan**: what to check after 3, 7, and 14 days, including KPI thresholds and rollback/scale criteria.

## Diagnostic Reference

Always read [drop-diagnosis-framework.md](references/drop-diagnosis-framework.md) before completing a diagnosis. Use it for cause signatures, decomposition formulas, output table templates, confidence rules, action gates, BSR interpretation, TACoS validation, retail readiness, competitor movement, budget and placement diagnosis, mixed-ASIN contamination, and recommendation safety.
