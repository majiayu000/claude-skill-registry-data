---
name: google-ads-depth-of-analysis
description: "Use for any Google Ads audit, performance review, optimization request, strategy question, or account restructuring. Covers 8 analytical dimensions: hierarchical drill-down, breakdowns, temporal trends, attribution rigor."
metadata:
  source: "prompts/skills/google_ads/depth-of-analysis"
---

# Google Ads - Depth of Analysis

> **When to apply**: Audits, performance reviews, optimization requests, strategy questions, account restructuring.
> **Skip for**: Simple data fetches, campaign listings, metric lookups.

## 1. Hierarchical Drill-Down

Never make recommendations based solely on campaign-level aggregates. Before concluding on any entity, drill deeper.

**Required flow:**
- Asked about a campaign → check ad group performance within it
- Asked about an ad group → check keyword + search term performance within it
- Asked about PMax → check asset group performance, search term categories, URL expansion config

**How:**
```
google_ads_run_gaql: SELECT campaign, ad_group, metrics FROM ad_group WHERE campaign.id = X
google_ads_run_gaql: SELECT search_term_view, metrics FROM search_term_view WHERE campaign.id = X
```

For PMax: search term data is limited — check search term category insights, asset group performance differences, and correlate PMax delivery changes with Brand Search impression share.

Identify which specific child entities drive the aggregate. Quantify: "Ad Group X accounts for 65% of campaign spend but CPA is 2x the campaign average."

## 2. Objective-Contextual Evaluation

Evaluate each campaign against its bid strategy target, not just absolute performance.

**Check first:**
- Bid strategy type: tCPA, tROAS, Maximize Conversions, Manual CPC, etc.
- Bid strategy target value (if set)
- Campaign type: Search, PMax, Shopping, Display, YouTube

**Apply correct evaluation:**
| Bid Strategy | Evaluate against | Red flag |
|-------------|-----------------|----------|
| tCPA | Actual CPA vs target CPA | CPA 30%+ above target |
| tROAS | Actual ROAS vs target ROAS | ROAS 30%+ below target |
| Maximize Conversions (no target) | CPA trend direction | Rising CPA with no constraint |
| Manual CPC | CPC vs Quality Score implied CPC | Paying premium due to low QS |

**Flag unconstrained strategies:** If tROAS target is 0.5x on a campaign achieving 3x — the algorithm isn't actually constrained. If tCPA is set 3x above actual CPA — same problem. Call this out.

**PMax maturity gate:** PMax must meet ONE of: age ≥ 30 days (ideally 60) OR total conversions ≥ 50. If neither met, flag as "insufficient data — premature to optimize." Exception: if campaign is clearly burning money (ROAS < 0.3x target after spend ≥ 3x AOV), recommend pausing.

## 3. Breakdown & Segmentation Analysis

Before concluding, check at least 2 of these breakdown dimensions:

**Required breakdowns:**
```
google_ads_run_gaql: SELECT segments.device, metrics FROM campaign WHERE campaign.id = X
google_ads_run_gaql: SELECT geographic_view, metrics FROM geographic_view WHERE campaign.id = X
google_ads_run_gaql: SELECT segments.day_of_week, metrics FROM campaign WHERE campaign.id = X
google_ads_run_gaql: SELECT campaign, metrics.search_impression_share WHERE segments.ad_network_type = 'SEARCH' vs 'SEARCH_PARTNERS'
```

**What to look for:**
- Device performance divergence — mobile vs desktop CPA gap
- Search Partners conversion rate vs Search network — quantify the gap (e.g., "Search Partners converts at 35% the rate of Search")
- Geographic variations — regions with high spend and poor conversion rates
- Day-of-week patterns — budget waste on low-converting days
- Cross-reference bid adjustments against actual segment performance — are adjustments aligned with data?

**Statistical significance:** Do not make segment-level recommendations from <50 clicks or <5 conversions. Call out low-confidence segments.

## 4. Temporal & Trend Analysis

Never treat the date range as a single number. Always compare time windows.

**Required comparisons:**
```
google_ads_run_gaql: SELECT segments.date, metrics FROM campaign WHERE segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

Analyze at minimum:
- Last 7 days vs previous 7 days (week-over-week)
- Separate day-of-week seasonality from structural trends
- Identify direction for each key metric: improving, declining, stable

**Distinguish:** "Metric is bad" vs "metric is getting worse" — the direction matters more than the absolute value.

**Connect the chain:** Impression share declining → CPC increasing → this is competitive pressure, not quality degradation. Correlate timing: "CPC started rising on [date], coinciding with impression share loss — suggests new competitor entered the auction."

## 5. Cross-Entity Dependency Recognition

Do not analyze campaigns in isolation. Map relationships.

**Check for:**
- Brand Search ↔ PMax overlap: Are both active on brand terms? Check search term reports for brand term leakage in PMax.
- Non-brand Search → Remarketing: Does non-brand search activity feed remarketing lists?
- Shopping ↔ Search overlap: Same products advertised in both? Check for cannibalization.

**How to detect PMax brand cannibalization:**
```
google_ads_run_gaql: SELECT search_term_view.search_term, metrics FROM search_term_view WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```
Check for brand terms appearing in PMax search terms. Correlate PMax spend/conversion trends with Brand Search impression share trends over the same period.

**Flag dependencies:** "PMax and Brand Search are both converting on brand terms. Total reported conversions across both campaigns likely exceed actual unique conversions. Before scaling PMax based on its ROAS, consider that some conversions are cannibalized from Brand Search."

## 6. Platform Mechanic Awareness

Explain how Google Ads mechanics affect the specific situation. Do not just mention them — explain the compound interaction.

**Common compound effects:**

| Signal | Mechanic | Consequence |
|--------|----------|-------------|
| Broad match + rising CPC | Query expansion | Algorithm expanding to less relevant queries → QS drops → CPC rises → tCPA struggles |
| Low QS + high CPC | Ad relevance | Paying premium for same position — fix ad relevance, not just bid |
| tCPA + low conversion volume | Smart Bidding data | Insufficient signal for Smart Bidding if below minimum conversion thresholds (see guardrails) — consider Manual CPC |
| PMax + declining Brand Search IS | Brand cannibalization | PMax claiming brand conversions → inflated PMax ROAS, deflated Brand Search |
| Maximize Conversions + no target | Unconstrained spend | Algorithm will spend full budget at any CPA — add a tCPA target |

**Quality Score diagnosis:** When CPC is high, decompose QS into its 3 components (expected CTR, ad relevance, landing page experience). Identify which component is dragging and recommend specific fixes for that component.

## 7. Proactive Signal Detection

After answering the user's question, always surface 2-3 additional concerns or opportunities they did not ask about.

**Scan for:**
- Quality Score trending downward in any high-spend ad group
- Impression share declining toward a delivery constraint (budget-lost or rank-lost)
- Search terms report showing irrelevant queries consuming budget
- Any campaign with conversion volume below Smart Bidding minimum thresholds
- CPC inflation trend that will erode profitability if unchecked
- PMax impression share eating into Brand Search impression share

**Format:** "Outside your question, I noticed [signal] in [entity] — this suggests [predicted consequence] within [timeframe]."

## 8. Attribution & Measurement Rigor

Do not take reported conversion numbers at face value.

**Always check:**
- Attribution model in use (last click, data-driven, etc.)
- Conversion lag: are recent days' conversions still incomplete?
- What share of conversions are "estimated" (modeled) vs observed?

**Flag these situations:**
- Display/YouTube campaigns with high view-through conversions — separate view-through from click-through when assessing ROAS
- PMax + Brand Search both active on brand terms — total reported conversions likely exceed actual unique conversions
- Long attribution windows (90-day) on retargeting — inflates attributed conversions
- Conversion count includes micro-conversions (page views, scroll depth) mixed with macro-conversions (purchases, leads) — separate them

**Frame as caveat:** "Before scaling this campaign based on its reported 5x ROAS, note that [specific attribution concern] means the true incremental ROAS is likely lower."
