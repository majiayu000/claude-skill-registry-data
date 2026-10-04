---
name: ad-budget-optimizer
description: Reallocate ad budget across campaigns and channels using ROAS and marginal return analysis
tags: [budget-optimization, roas, ad-spend, performance-marketing, attribution]
---

# Ad Budget Optimizer

Analyzes campaign performance data (spend, revenue, ROAS, CPA, conversion rate) across campaigns and channels, identifies top performers and underperformers, calculates optimal budget allocation using marginal ROAS analysis, and recommends specific budget shifts. Outputs a reallocation plan with projected impact on overall ROAS and lead volume.

## Prerequisites

- Campaign performance data (can be pasted as CSV, JSON, or described verbally)
- Current budget allocation across campaigns/channels
- Business goals (target CPA, target ROAS, or lead volume target)
- Optional: `agency.config.json` for client context
- Optional: historical performance data for trend analysis

## Capabilities Used

1. `google-ads-builder` -- for restructuring underperforming Google campaigns
2. `meta-ads-builder` -- for restructuring underperforming Meta campaigns
3. `landing-page-auditor` -- for diagnosing conversion issues on high-spend, low-conversion campaigns

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `budget.monthly_total` for total budget context.
3. Extract `kpis.target_cpa` and `kpis.target_roas` for benchmark goals.
4. Check `tools.websearch` availability for benchmarking.
5. Accept parameters:
   - `performance_data` -- (required) campaign performance data in any format (CSV, JSON, or natural language description)
   - `budget_total` -- (optional) total monthly budget. Default: sum from performance data
   - `goal` -- (optional) `minimize_cpa` | `maximize_roas` | `maximize_leads` | `maximize_revenue`. Default: `maximize_roas`
   - `constraints` -- (optional) minimum/maximum spend per campaign or channel
   - `timeframe` -- (optional) data time period for analysis
   - `risk_tolerance` -- (optional) `conservative` | `moderate` | `aggressive`. Default: `moderate`

## Phase 1: Data Ingestion and Normalization

### Parse Performance Data
Accept data in any format and normalize into a standard structure:

| Campaign/Channel | Spend | Revenue | Conversions | CPA | ROAS | CTR | CVR |
|-----------------|-------|---------|-------------|-----|------|-----|-----|
| Campaign A | $X | $Y | N | $Z | X:1 | X% | X% |

### Calculate Missing Metrics
If not all metrics are provided, derive them:
- ROAS = Revenue / Spend
- CPA = Spend / Conversions
- CVR = Conversions / Clicks
- CTR = Clicks / Impressions
- Revenue per conversion = Revenue / Conversions
- Cost per click = Spend / Clicks

### Data Quality Check
- Flag campaigns with insufficient data (< 100 clicks or < 5 conversions) -- not statistically significant
- Flag campaigns with no conversion tracking
- Flag anomalies (sudden spikes/drops that may indicate tracking issues)
- Note data freshness: when was this data collected?

## Phase 2: Performance Analysis

### Tier Classification
Sort campaigns into performance tiers:

**Tier 1: Winners** (scale these)
- ROAS > target ROAS (or CPA < target CPA)
- Conversion volume is meaningful (not just 1-2 lucky conversions)
- Consistent performance over the data period
- Still has room to scale (not at audience saturation)

**Tier 2: Promising** (optimize these)
- ROAS within 20% of target
- Good leading indicators (high CTR, decent CVR) but ROAS not yet optimal
- Recently launched campaigns still in learning phase
- Campaigns with fixable issues (landing page, ad copy, targeting)

**Tier 3: Underperformers** (fix or cut)
- ROAS significantly below target (< 50% of goal)
- High CPA with no improvement trend
- Low CTR and low CVR combined
- No clear path to profitability

**Tier 4: Dead Weight** (kill these)
- Zero or near-zero conversions despite meaningful spend
- CPA > 3x target with no improvement trend
- ROAS < 0.5:1 for more than 30 days
- Audiences exhausted (frequency > 3 on Meta, low impression share on Google)

### Channel-Level Analysis
Aggregate by channel (Google Search, Google Display, Meta, LinkedIn, etc.):
- Channel ROAS and CPA
- Channel contribution to total revenue
- Channel efficiency trend (improving or declining?)
- Cross-channel attribution considerations

## Phase 3: Marginal ROAS Calculation

### Diminishing Returns Analysis
For each campaign, estimate the marginal ROAS curve:

At current spend levels:
- What is the incremental ROAS of the last 10% of spend?
- Is the campaign on the rising, flat, or declining portion of its returns curve?
- Signs of saturation: increasing CPA over time, declining CTR, rising frequency (Meta), declining impression share improvement (Google)

### Marginal ROAS Ranking
Rank all campaigns by estimated marginal ROAS:
1. Campaigns with rising ROAS at current spend (scale opportunity)
2. Campaigns with stable ROAS at current spend (maintain or modest scale)
3. Campaigns with declining ROAS at current spend (at or past optimal spend)
4. Campaigns with consistently negative ROAS (cut)

### Optimal Allocation Model
Using marginal ROAS estimates:
- Shift budget from low-marginal-ROAS campaigns to high-marginal-ROAS campaigns
- Stop increasing when marginal ROAS of the scaled campaign equals the marginal ROAS of the reduced campaign
- Apply constraints (minimum spend floors, maximum spend caps)

## Phase 4: Budget Reallocation Plan

### Recommended Changes
For each campaign, specify:
- Current spend
- Recommended spend
- Change amount and percentage
- Rationale for the change
- Expected impact on ROAS/CPA
- Risk level of the change

### Reallocation Rules by Risk Tolerance

**Conservative**
- Maximum 15% shift per campaign per period
- No campaign reduced below 50% of current spend
- Only shift to campaigns with proven ROAS > target
- Monitor for 2 weeks before additional shifts

**Moderate**
- Maximum 30% shift per campaign per period
- Campaigns can be reduced to 25% of current spend
- Shift to campaigns with ROAS > 80% of target
- Monitor for 1 week before additional shifts

**Aggressive**
- Maximum 50% shift per campaign per period
- Kill underperformers entirely (reallocate 100%)
- Shift to campaigns showing positive marginal ROAS trends
- Monitor daily, iterate quickly

### Implementation Timeline
- **Week 1**: Apply budget shifts, maintain ad creative
- **Week 2**: Monitor performance, adjust bids
- **Week 3**: Second round of optimization based on new data
- **Week 4**: Full review, set new baseline

## Phase 5: Projected Impact

### Before vs After Projections

| Metric | Current | Projected | Change |
|--------|---------|-----------|--------|
| Total Spend | $X | $X (same) | 0% |
| Total Revenue | $Y | $Y' | +X% |
| Blended ROAS | X:1 | Y:1 | +X% |
| Blended CPA | $X | $Y | -X% |
| Total Conversions | N | N' | +X% |

### Confidence Level
- High confidence: based on > 1000 clicks and > 50 conversions per campaign
- Medium confidence: based on > 100 clicks and > 10 conversions per campaign
- Low confidence: limited data, projections are directional only

### Scenario Modeling
Provide three scenarios:
- **Best case**: all winners scale efficiently, no saturation effects
- **Base case**: expected diminishing returns on scaled campaigns
- **Worst case**: scaled campaigns hit saturation quickly, some regression

## Phase 6: Diagnostic Recommendations

### For Underperforming Campaigns (before killing)
Diagnose the root cause:

**Low CTR + Low CVR** -- wrong audience or wrong message
- Recommendation: rebuild targeting and ad creative

**High CTR + Low CVR** -- landing page problem
- Recommendation: run `landing-page-auditor` on the destination URL

**Low CTR + High CVR** -- message resonates with buyers but doesn't attract clicks
- Recommendation: improve ad creative, test new hooks

**High CPA + High ROAS** -- working but expensive
- Recommendation: maintain if LTV justifies, optimize for efficiency

### For Cross-Channel Shifts
If recommending shifting budget between channels:
- Use `google-ads-builder` to structure new Google campaigns
- Use `meta-ads-builder` to structure new Meta campaigns
- Account for platform learning periods (Meta needs 50 conversions to exit learning phase)

## Phase 7: Output

Return structured JSON:

```json
{
  "analyzed_at": "2024-01-15T14:30:00Z",
  "goal": "maximize_roas",
  "risk_tolerance": "moderate",
  "total_budget": "100000 INR",
  "current_performance": {
    "total_spend": "100000 INR",
    "total_revenue": "250000 INR",
    "blended_roas": "2.5:1",
    "blended_cpa": "1250 INR",
    "total_conversions": 80
  },
  "campaign_tiers": {
    "winners": [
      {
        "campaign": "Shopify Dev - Google Search",
        "current_spend": "30000 INR",
        "roas": "4.2:1",
        "cpa": "600 INR",
        "tier": "Winner",
        "marginal_roas": "Rising",
        "recommendation": "Scale by 30%",
        "new_spend": "39000 INR",
        "rationale": "Highest ROAS, still under target impression share, room to scale"
      }
    ],
    "promising": [],
    "underperformers": [
      {
        "campaign": "Brand Awareness - Meta Display",
        "current_spend": "20000 INR",
        "roas": "0.8:1",
        "cpa": "2500 INR",
        "tier": "Underperformer",
        "marginal_roas": "Declining",
        "recommendation": "Reduce by 50%, diagnose landing page",
        "new_spend": "10000 INR",
        "rationale": "CPA 2x target, declining ROAS trend, landing page audit needed"
      }
    ],
    "dead_weight": []
  },
  "reallocation_plan": [
    { "campaign": "Shopify Dev - Google Search", "current": "30000", "new": "39000", "change": "+9000 (+30%)" },
    { "campaign": "Brand Awareness - Meta Display", "current": "20000", "new": "10000", "change": "-10000 (-50%)" },
    { "campaign": "CRO Services - Meta Lead Gen", "current": "25000", "new": "26000", "change": "+1000 (+4%)" }
  ],
  "projected_impact": {
    "scenario_base": {
      "total_revenue": "295000 INR",
      "blended_roas": "2.95:1",
      "blended_cpa": "1050 INR",
      "total_conversions": 95,
      "improvement": "+18% revenue, +18% ROAS, -16% CPA"
    },
    "scenario_best": {
      "improvement": "+25% revenue"
    },
    "scenario_worst": {
      "improvement": "+8% revenue"
    },
    "confidence_level": "Medium"
  },
  "diagnostic_actions": [
    { "campaign": "Brand Awareness - Meta Display", "diagnosis": "High CTR + Low CVR = landing page problem", "action": "Run landing-page-auditor on destination URL" }
  ],
  "implementation_timeline": {
    "week_1": "Apply budget shifts, monitor daily",
    "week_2": "Evaluate initial impact, adjust bids",
    "week_3": "Second optimization round",
    "week_4": "Full review, set new baselines"
  }
}
```

## Example Usage

Trigger phrases:
- "Optimize my ad budget allocation"
- "Reallocate budget based on ROAS"
- "Which campaigns should I scale or cut?"
- "Ad budget optimization for [business]"
- "Analyze campaign performance and recommend budget shifts"

```
User: Here's my campaign data: [pastes CSV]. Optimize for ROAS.
Assistant: [parses data, classifies campaigns into tiers, calculates marginal ROAS, recommends specific budget shifts, projects impact]
```

```
User: I'm spending $5K/month across Google and Meta. Which campaigns should I scale?
Assistant: [analyzes performance by campaign, identifies winners and losers, recommends reallocation with projected ROI improvement]
```

```
User: My Meta ads CPA is too high. Should I shift budget to Google?
Assistant: [compares cross-channel performance, analyzes marginal returns, recommends optimal channel mix with implementation timeline]
```
