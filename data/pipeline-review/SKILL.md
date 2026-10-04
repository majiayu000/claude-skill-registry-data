---
name: pipeline-review
description: Weekly pipeline health analysis with velocity metrics, stage distribution, forecasting, and actionable recommendations
tags: [pipeline, analytics, forecasting, crm, weekly, sales, metrics]
---

# Pipeline Review

Pulls CRM data, calculates pipeline health metrics (total value, stage distribution, velocity, conversion rates, aging deals), compares performance to targets, generates a revenue forecast, and outputs a pipeline health report with prioritized recommendations. Designed to run weekly (typically Monday morning) but can be triggered ad hoc.

## Prerequisites

- `agency.config.json` at repo root with `agency`, `crm`, `outreach`, `services`, and `scoring` sections
- CRM data accessible via `crm-writer` skill (Google Sheets webhook or API)
- Historical pipeline data (at least 2 weeks for trend analysis, 4+ weeks for reliable forecasting)
- Optional: revenue targets for comparison

## Capabilities Used

1. `crm-writer` -- for reading pipeline data from CRM tabs
2. `revenue-forecaster` -- for weighted pipeline and Monte Carlo forecasting (if installed)
3. `win-loss-analyzer` -- for historical conversion pattern data (if installed)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for report header
   - `crm.type` -- CRM platform (google_sheets, etc.)
   - `crm.sheet_id` -- for data access
   - `crm.webhook_url` -- for reading data
   - `crm.tabs.pipeline` -- pipeline data tab name
   - `crm.tabs.outreach_log` -- outreach activity data
   - `crm.tabs.calling` -- calling activity data
   - `crm.tabs.dashboard` -- where to write the report summary
   - `outreach.cadence` -- to assess if cadence is being followed
   - `outreach.daily_caps` -- to assess if activity targets are being met
   - `scoring.thresholds` -- hot/warm/cool definitions
   - `services[]` -- for deal categorization by service type
3. Accept parameters:
   - `review_period` -- timeframe to analyze. Default: `last_7_days`. Options: `last_7_days`, `last_14_days`, `last_30_days`, `mtd`, `qtd`
   - `targets` -- (optional) revenue and activity targets:
     - `monthly_revenue_target` -- target MRR or monthly revenue
     - `quarterly_revenue_target` -- target quarterly revenue
     - `weekly_demos` -- target demos per week
     - `weekly_proposals` -- target proposals per week
     - `daily_outreach` -- target outreach activities per day
   - `compare_period` -- compare to previous period for trend. Default: `previous_week`
   - `forecast_months` -- months to forecast. Default: 3
   - `output_to_crm` -- write report summary to Dashboard tab. Default: true

## Phase 1: Data Collection

Pull data from all relevant CRM tabs using `crm-writer`.

**Pipeline data (from Pipeline tab):**
- All active deals with: company name, deal value, stage, created date, last activity date, assigned to, service type, source (inbound/outbound), expected close date, probability

**Required pipeline stages (map to CRM columns):**
```
LEAD -> QUALIFIED -> DEMO_SCHEDULED -> DEMO_DONE -> PROPOSAL_SENT -> NEGOTIATION -> CLOSED_WON -> CLOSED_LOST
```

If CRM uses different stage names, map them to these standard stages.

**Outreach data (from Outreach CRM tab):**
- All outreach activities in the review period: date, lead name, channel (email/linkedin/instagram/call), activity type (initial/follow-up), response received (y/n)

**Historical data (from Pipeline tab, all time):**
- All closed deals (won and lost) with dates and values for conversion rate calculations

Compile raw data:
```
DATA COLLECTION:
---
Active deals: [count]
Deals in review period: [count]
Outreach activities in review period: [count]
Closed won (all time): [count]
Closed lost (all time): [count]
Data quality issues: [list any missing fields or inconsistencies]
```

## Phase 2: Pipeline Health Metrics

Calculate the core metrics that determine pipeline health.

### 2.1: Pipeline Value

| Metric | Calculation |
|--------|------------|
| Total pipeline value | Sum of all active deal values |
| Weighted pipeline value | Sum of (deal value * stage probability) for all active deals |
| New pipeline added (period) | Sum of deals created during review period |
| Pipeline lost (period) | Sum of deals moved to CLOSED_LOST during review period |
| Net pipeline change | Added - Lost |
| Pipeline-to-target ratio | Weighted pipeline / revenue target |

**Pipeline-to-target ratio benchmarks:**
- Healthy: 3x or higher (you need 3x your target in pipeline to hit it)
- Caution: 2-3x
- Critical: under 2x

### 2.2: Stage Distribution

Count and value deals at each stage:

| Stage | Deal Count | Total Value | Avg Deal Size | % of Pipeline |
|-------|-----------|-------------|---------------|---------------|
| LEAD | | | | |
| QUALIFIED | | | | |
| DEMO_SCHEDULED | | | | |
| DEMO_DONE | | | | |
| PROPOSAL_SENT | | | | |
| NEGOTIATION | | | | |

**Stage health indicators:**
- **Top-heavy**: too many deals in LEAD/QUALIFIED, not enough advancing = prospecting without qualifying
- **Bottleneck**: disproportionate count at one stage = process issue at that stage
- **Bottom-heavy**: too many in PROPOSAL/NEGOTIATION = slow closing or pricing issues
- **Balanced**: roughly equal distribution with natural funnel narrowing = healthy

### 2.3: Velocity Metrics

| Metric | Calculation |
|--------|------------|
| Average days in stage | For each stage, average days deals spend before moving |
| Average sales cycle | Average days from LEAD to CLOSED_WON |
| Stage-to-stage conversion rate | % of deals that advance from each stage to the next |
| Overall win rate | CLOSED_WON / (CLOSED_WON + CLOSED_LOST) |
| Velocity score | (# of deals * avg deal size * win rate) / avg sales cycle |

**Velocity trend:**
- Compare velocity score to previous period
- Increasing velocity = deals are moving faster and/or getting bigger
- Decreasing velocity = something is slowing down (identify which variable)

### 2.4: Aging Analysis

Identify stale deals that need attention:

| Aging Category | Definition | Action |
|----------------|-----------|--------|
| Fresh | Last activity within 3 days | No action |
| Active | Last activity 4-7 days ago | Monitor |
| Cooling | Last activity 8-14 days ago | Follow up immediately |
| Stale | Last activity 15-30 days ago | Escalate: call or break-up |
| Dead | Last activity 30+ days ago | Move to CLOSED_LOST or archive |

List all COOLING and STALE deals with:
- Company name
- Deal value
- Current stage
- Days since last activity
- Recommended action

### 2.5: Activity Metrics

| Metric | Actual | Target | % of Target |
|--------|--------|--------|-------------|
| Emails sent (period) | | | |
| LinkedIn touches (period) | | | |
| Instagram touches (period) | | | |
| Calls made (period) | | | |
| Total outreach activities | | | |
| Response rate | | | |
| Demos booked (period) | | | |
| Proposals sent (period) | | | |

Compare to `outreach.daily_caps` multiplied by business days in the period.

## Phase 3: Conversion Analysis

Analyze where deals are being won and lost.

### 3.1: Conversion Funnel

```
LEAD -> QUALIFIED: [X%] conversion ([N] leads -> [M] qualified)
QUALIFIED -> DEMO: [X%] conversion
DEMO -> PROPOSAL: [X%] conversion
PROPOSAL -> WON: [X%] conversion
---
Overall LEAD -> WON: [X%] conversion
```

**Identify the weakest conversion point** -- this is where the biggest improvement opportunity exists.

### 3.2: Win/Loss by Segment

| Segment | Deals Won | Deals Lost | Win Rate | Avg Deal Size |
|---------|-----------|------------|----------|---------------|
| India D2C | | | | |
| US/UK/AU D2C | | | | |
| [Service 1] | | | | |
| [Service 2] | | | | |
| Inbound | | | | |
| Outbound | | | | |

Identify the highest-performing segments by win rate and deal size.

### 3.3: Loss Reasons

If loss reasons are tracked in CRM, aggregate:

| Reason | Count | % of Losses | Trend |
|--------|-------|------------|-------|
| Price | | | up/down/stable |
| Timing | | | |
| Went with competitor | | | |
| No decision/ghosted | | | |
| Scope mismatch | | | |

## Phase 4: Forecasting

Generate a revenue forecast based on pipeline data.

### 4.1: Weighted Pipeline Forecast

Apply stage-specific probabilities:

| Stage | Probability | Deal Value | Weighted Value |
|-------|------------|------------|----------------|
| LEAD | 5% | | |
| QUALIFIED | 15% | | |
| DEMO_SCHEDULED | 25% | | |
| DEMO_DONE | 40% | | |
| PROPOSAL_SENT | 60% | | |
| NEGOTIATION | 80% | | |

**Total weighted forecast: $[sum]**

### 4.2: Scenario Forecasting

| Scenario | Method | Amount |
|----------|--------|--------|
| Conservative | Only PROPOSAL + NEGOTIATION deals at 50% probability | $X |
| Moderate | Weighted pipeline (all stages) | $Y |
| Best case | All active deals at stage probability + historical win rate adjustment | $Z |

### 4.3: Time-Based Forecast

Based on expected close dates:

| Month | Deals Expected | Weighted Value | Confidence |
|-------|---------------|----------------|-----------|
| This month | | | |
| Next month | | | |
| Month +2 | | | |

### 4.4: Pipeline Coverage

```
Revenue target: $[target]
Weighted pipeline: $[weighted]
Coverage ratio: [weighted/target]x
---
Need to add: $[shortfall * 3] in new pipeline to hit target (at 3x coverage)
= [shortfall * 3 / avg_deal_size] new qualified leads needed
```

## Phase 5: Trend Analysis

Compare current period to previous period(s).

| Metric | Current | Previous | Change | Trend |
|--------|---------|----------|--------|-------|
| Total pipeline value | | | | up/down |
| New deals added | | | | |
| Deals closed (won) | | | | |
| Win rate | | | | |
| Average deal size | | | | |
| Sales cycle length | | | | |
| Outreach volume | | | | |
| Response rate | | | | |
| Velocity score | | | | |

**Flag concerning trends:**
- 2+ consecutive weeks of declining pipeline value
- Win rate dropping below historical average
- Sales cycle lengthening
- Outreach volume below 80% of target
- Response rate declining

## Phase 6: Recommendations

Generate prioritized, actionable recommendations based on the analysis.

**Recommendation categories:**

1. **Immediate actions (this week):**
   - Stale deals to follow up on (list with suggested action)
   - Bottleneck stages to unblock (specific deals + actions)
   - Activity gaps to fill (which channels are underperforming)

2. **Process improvements (this month):**
   - Stage conversion issues to address
   - Segment-specific strategy adjustments
   - Outreach mix optimization (shift activity to higher-performing channels)

3. **Strategic recommendations (this quarter):**
   - Pipeline coverage gaps and required lead volume
   - Service/segment mix optimization based on win rate and deal size
   - Pricing and positioning adjustments based on loss reasons

**Priority scoring for recommendations:**

| Factor | Weight |
|--------|--------|
| Revenue impact | 40% |
| Effort required | 30% |
| Urgency (time-sensitive) | 30% |

Rank all recommendations by priority score. Top 3 become the "Weekly Focus."

## Phase 7: Output

Return structured JSON:

```json
{
  "report_metadata": {
    "agency": "Agency Name",
    "review_period": "2026-03-03 to 2026-03-09",
    "generated_at": "2026-03-10T09:00:00Z",
    "data_quality": "good",
    "data_issues": []
  },
  "pipeline_snapshot": {
    "total_value": 450000,
    "weighted_value": 185000,
    "deal_count": 18,
    "avg_deal_size": 25000,
    "new_this_period": 4,
    "lost_this_period": 1,
    "net_change": 75000,
    "pipeline_to_target_ratio": 3.2,
    "health": "healthy"
  },
  "stage_distribution": [
    {"stage": "LEAD", "count": 5, "value": 125000, "pct_of_pipeline": 0.28},
    {"stage": "QUALIFIED", "count": 4, "value": 100000, "pct_of_pipeline": 0.22},
    {"stage": "DEMO_SCHEDULED", "count": 3, "value": 75000, "pct_of_pipeline": 0.17},
    {"stage": "DEMO_DONE", "count": 2, "value": 50000, "pct_of_pipeline": 0.11},
    {"stage": "PROPOSAL_SENT", "count": 3, "value": 75000, "pct_of_pipeline": 0.17},
    {"stage": "NEGOTIATION", "count": 1, "value": 25000, "pct_of_pipeline": 0.06}
  ],
  "stage_health": "slightly_top_heavy",
  "velocity": {
    "avg_sales_cycle_days": 28,
    "velocity_score": 4821,
    "velocity_trend": "stable",
    "stage_durations": [
      {"stage": "LEAD_to_QUALIFIED", "avg_days": 5},
      {"stage": "QUALIFIED_to_DEMO", "avg_days": 7},
      {"stage": "DEMO_to_PROPOSAL", "avg_days": 4},
      {"stage": "PROPOSAL_to_CLOSE", "avg_days": 12}
    ]
  },
  "aging": {
    "fresh": 8,
    "active": 5,
    "cooling": 3,
    "stale": 2,
    "dead": 0,
    "attention_needed": [
      {"company": "Company A", "value": 30000, "stage": "PROPOSAL_SENT", "days_stale": 12, "action": "Call this week -- proposal sent 12 days ago with no response"},
      {"company": "Company B", "value": 20000, "stage": "QUALIFIED", "days_stale": 18, "action": "Re-engage or move to lost"}
    ]
  },
  "activity_metrics": {
    "emails_sent": 22,
    "linkedin_touches": 18,
    "instagram_touches": 8,
    "calls_made": 6,
    "total_activities": 54,
    "target_activities": 75,
    "pct_of_target": 0.72,
    "response_rate": 0.12,
    "demos_booked": 2,
    "proposals_sent": 1
  },
  "conversion_funnel": {
    "lead_to_qualified": 0.65,
    "qualified_to_demo": 0.55,
    "demo_to_proposal": 0.70,
    "proposal_to_won": 0.35,
    "overall_lead_to_won": 0.09,
    "weakest_point": "proposal_to_won",
    "weakest_point_insight": "35% proposal-to-close rate suggests pricing objections or proposal quality issues"
  },
  "forecast": {
    "weighted_total": 185000,
    "scenarios": {
      "conservative": 100000,
      "moderate": 185000,
      "best_case": 290000
    },
    "monthly_forecast": [
      {"month": "March 2026", "weighted_value": 75000, "deal_count": 4},
      {"month": "April 2026", "weighted_value": 65000, "deal_count": 3},
      {"month": "May 2026", "weighted_value": 45000, "deal_count": 2}
    ],
    "pipeline_coverage": {
      "target": 150000,
      "weighted_pipeline": 185000,
      "ratio": 1.23,
      "shortfall": 0,
      "new_leads_needed": 0
    }
  },
  "trends": {
    "pipeline_value_trend": "up",
    "win_rate_trend": "stable",
    "deal_size_trend": "up",
    "cycle_length_trend": "stable",
    "activity_trend": "down",
    "concerning_trends": ["Outreach activity 28% below target for 2nd consecutive week"]
  },
  "recommendations": {
    "weekly_focus": [
      {"priority": 1, "action": "Follow up on 3 cooling deals worth $70K combined", "category": "immediate", "revenue_impact": "high"},
      {"priority": 2, "action": "Increase outreach volume to hit daily caps -- 28% below target", "category": "immediate", "revenue_impact": "medium"},
      {"priority": 3, "action": "Review proposal template -- 35% close rate is below benchmark", "category": "process", "revenue_impact": "high"}
    ],
    "immediate_actions": [],
    "process_improvements": [],
    "strategic_recommendations": []
  }
}
```

## Phase 8: Report Distribution

After generating the report:

1. **Present to user**: show the key metrics, concerning trends, and weekly focus items
2. **Write to CRM**: if `output_to_crm` is true, write a summary row to the Dashboard tab via `crm-writer`
3. **Flag urgent items**: if any deals are stale and high-value, highlight prominently
4. **Compare to last week**: show week-over-week changes for the top 5 metrics

## Phase 9: Review

Present the pipeline review:

1. Lead with the health verdict: healthy / caution / critical
2. Show pipeline snapshot (total value, weighted value, deal count)
3. Highlight the 3 weekly focus actions
4. Show the forecast scenarios
5. Flag any concerning trends
6. List stale deals needing immediate attention
7. Ask if any data needs correction or if the user wants to drill into a specific area

## Example Usage

Trigger phrases:
- "Run a pipeline review"
- "How is the pipeline looking?"
- "Weekly pipeline check"
- "What is our forecast for this quarter?"
- "Which deals need attention?"
- "Pipeline health report"
- "How are we tracking against targets?"

```
User: Run a pipeline review for this week
Assistant: [reads config, pulls CRM data via crm-writer, calculates all metrics, identifies stale deals, generates forecast, compares to previous week, returns health report with 3 focus actions]
```

```
User: How is the pipeline looking? Any deals going stale?
Assistant: [pulls pipeline data, runs aging analysis, identifies cooling and stale deals, returns deal-level recommendations with urgency ranking]
```
