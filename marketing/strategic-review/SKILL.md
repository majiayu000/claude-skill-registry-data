---
name: strategic-review
description: >
  Monthly strategic review playbook. Chains pipeline-review + campaign-analyzer
  + win-loss-analyzer + gtm-analyzer. Outputs executive summary with KPIs,
  channel ROI, competitive shifts, and strategic recommendations.
tags: [strategy, review, monthly, leadership, kpi, executive]
---

# Strategic Review

Monthly strategic review playbook for leadership. Aggregates data from pipeline, campaigns, win/loss analysis, and GTM performance into a single executive-level report with KPIs, trends, insights, and strategic recommendations.

Run this on the first Monday of each month.

## Prerequisites

- `agency.config.json` populated (agency info, services, ICP, scoring)
- CRM data accessible via `crm-writer`/CRM webhook
- Campaign data available (ad platforms, email metrics)
- At least one month of pipeline history

## Composites & Capabilities Used

1. `pipeline-review` composite -- pipeline health, stage conversion, velocity
2. `campaign-analyzer` composite -- channel performance, spend, ROI
3. `win-loss-analyzer` composite -- deal outcomes, patterns, feedback
4. `gtm-analyzer` composite -- overall GTM strategy assessment
5. `crm-writer` capability -- read CRM data for analysis

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name` -- for report branding
- `services[]` -- for service-level analysis
- `icp.segments[]` -- for segment-level performance
- `scoring.thresholds` -- for pipeline quality benchmarking
- `crm` -- for data access

Accept parameters:
- `review_period` -- (required) month/year string: "March 2026" or date range
- `compare_period` -- (optional) previous period for comparison. Default: previous month
- `focus_areas` -- (optional) array to emphasize: `pipeline`, `campaigns`, `deals`, `competitors`, `team`. Default: all
- `revenue_target` -- (optional) monthly revenue target for goal tracking
- `include_recommendations` -- boolean. Default: `true`

## Phase 1: Pipeline Review

Execute `pipeline-review` for the review period:

### Metrics to Collect
```
PIPELINE HEALTH -- [Review Period]
---
Total leads generated: [N] (vs [N] last month, [+/-X%])
Lead sources:
  Outbound: [N] ([%] of total)
  Inbound: [N] ([%] of total)
  Referral: [N] ([%] of total)

Lead quality:
  HOT: [N] ([%])
  WARM: [N] ([%])
  COOL: [N] ([%])
  Average lead score: [N]

Stage conversion rates:
  NEW -> ENRICHED: [%]
  ENRICHED -> CONTACTED: [%]
  CONTACTED -> REPLIED: [%]
  REPLIED -> DEMO_BOOKED: [%]
  DEMO_BOOKED -> PROPOSAL_SENT: [%]
  PROPOSAL_SENT -> CLOSED_WON: [%]

Pipeline velocity:
  Average days NEW -> CONTACTED: [N]
  Average days CONTACTED -> DEMO: [N]
  Average days DEMO -> CLOSE: [N]
  Total cycle time: [N] days

Pipeline value:
  Total pipeline value: [currency]
  Weighted pipeline: [currency]
  Average deal size: [currency]
```

### Trend Analysis
- Compare all metrics to previous month
- Flag metrics with > 20% change (positive or negative)
- Identify bottleneck stages (lowest conversion rate)

## Phase 2: Campaign Analysis

Execute `campaign-analyzer` for the review period:

### Metrics by Channel
```
CAMPAIGN PERFORMANCE -- [Review Period]
---
Channel: Cold Email
  Sent: [N]
  Open rate: [%]
  Reply rate: [%]
  Demos from channel: [N]
  Cost: [currency]
  Cost per demo: [currency]

Channel: LinkedIn (Dripify)
  Connection requests: [N]
  Acceptance rate: [%]
  Conversations started: [N]
  Demos from channel: [N]
  Cost: [currency]
  Cost per demo: [currency]

Channel: Instagram DM
  DMs sent: [N]
  Response rate: [%]
  Demos from channel: [N]
  Cost: [currency]

Channel: Inbound (SEO/Content)
  Website visitors: [N]
  Lead captures: [N]
  Demos from channel: [N]
  Cost: [currency]
  Cost per lead: [currency]

Channel: Paid Ads (if applicable)
  Spend: [currency]
  Impressions: [N]
  Clicks: [N]
  CTR: [%]
  Leads: [N]
  Cost per lead: [currency]
  Demos: [N]
  ROAS: [X:1]
```

### Channel ROI Ranking
Rank channels by cost-per-demo-booked (most efficient first).

### Content Performance
- Top 3 performing email subject lines (by open rate)
- Top 3 performing email bodies (by reply rate)
- Top performing social posts (by engagement)
- Top performing blog posts (by traffic/leads)

## Phase 3: Win/Loss Analysis

Execute `win-loss-analyzer` for deals that closed (won or lost) in the review period:

### Won Deals
```
DEALS WON -- [Review Period]
---
Total deals won: [N]
Total revenue closed: [currency]
Average deal size: [currency]
Win rate: [%] (deals won / proposals sent)

Won deal profiles:
  [Deal 1]: [Company] -- [service] -- [deal size] -- [cycle time] -- [source]
  [Deal 2]: ...

Common win factors:
  1. [Factor]: [appeared in X% of won deals]
  2. [Factor]: ...
  3. [Factor]: ...

Best source for won deals: [channel]
Best ICP segment for wins: [segment name]
```

### Lost Deals
```
DEALS LOST -- [Review Period]
---
Total deals lost: [N]
Total revenue lost: [currency]
Average deal size: [currency]

Lost deal reasons:
  1. [Reason]: [N] deals, [%] of losses
  2. [Reason]: [N] deals, [%]
  3. [Reason]: [N] deals, [%]

Common loss patterns:
  Stage where most deals die: [stage]
  Average time before loss: [N] days
  Competitor mentioned: [competitor name, N times]
```

### Win/Loss Insights
- What differentiates won from lost deals?
- Are there ICP segments with consistently higher win rates?
- Are there services with higher close rates?
- Is pricing a factor? What price points close vs don't?

## Phase 4: GTM Strategy Assessment

Execute `gtm-analyzer` for a broader strategic view:

### Market Assessment
```
GTM HEALTH -- [Review Period]
---
ICP segment performance:
  [Segment 1]: [leads / demos / wins / revenue]
  [Segment 2]: ...

Service demand:
  [Service 1]: [inquiries / proposals / wins]
  [Service 2]: ...

Competitive landscape:
  New competitors spotted: [names]
  Competitor moves: [notable actions]
  Market shifts: [trends affecting the business]

Positioning check:
  Are we attracting the right leads? [yes/no + evidence]
  Is our messaging resonating? [reply rate trends]
  Are we competitive on pricing? [win/loss by price point]
```

## Phase 5: Executive Summary

Compile all findings into a leadership-ready summary:

```
STRATEGIC REVIEW -- [Review Period]
================================================================

HEADLINE METRICS
  Revenue closed: [currency] ([+/-X%] vs last month)
  Pipeline value: [currency] ([+/-X%])
  Demos booked: [N] ([+/-X%])
  Win rate: [%] ([+/-X%])
  Cost per demo: [currency] ([+/-X%])

TOP 3 WINS THIS MONTH
  1. [Achievement with metric]
  2. [Achievement]
  3. [Achievement]

TOP 3 CONCERNS
  1. [Issue with data]
  2. [Issue]
  3. [Issue]

CHANNEL EFFICIENCY (ranked by cost-per-demo)
  1. [Channel]: [cost/demo] -- [trend]
  2. [Channel]: [cost/demo] -- [trend]
  3. [Channel]: [cost/demo] -- [trend]

KEY INSIGHT
[One paragraph synthesis: the most important strategic observation from this month's data]
```

## Phase 6: Strategic Recommendations

If `include_recommendations` = true:

Generate 3-5 strategic recommendations based on data:

```
STRATEGIC RECOMMENDATIONS
---
1. [RECOMMENDATION TITLE]
   Data basis: [what data supports this]
   Action: [specific action to take]
   Expected impact: [projected improvement]
   Timeline: [when to implement]
   Owner: [who is responsible]
   Priority: [HIGH / MEDIUM / LOW]

2. ...
```

### Recommendation Categories
- **Double down**: Channels or segments performing above average
- **Fix**: Broken conversion points or declining metrics
- **Experiment**: New approaches to test based on market signals
- **Cut**: Underperforming channels or segments to deprioritize
- **Invest**: Areas needing more resources for growth

## Phase 7: Goal Setting

Propose next month's targets based on trends:

```
NEXT MONTH TARGETS
---
Lead generation: [N] leads (based on [trend])
Demos booked: [N] (based on [conversion rate])
Revenue target: [currency] (based on [pipeline + win rate])
Key initiative: [one strategic focus for next month]
Experiments to run: [1-2 new things to test]
```

## Phase 8: Output

Return structured JSON:

```json
{
  "review_period": "March 2026",
  "compare_period": "February 2026",
  "generated_at": "2026-04-01T09:00:00Z",
  "headline_metrics": {
    "revenue_closed": {"value": "INR 3.5L", "change": "+16%"},
    "pipeline_value": {"value": "INR 12L", "change": "+8%"},
    "demos_booked": {"value": 14, "change": "+27%"},
    "win_rate": {"value": "28%", "change": "+3pp"},
    "cost_per_demo": {"value": "INR 2,100", "change": "-12%"}
  },
  "pipeline": {
    "total_leads": 87,
    "hot_leads": 12,
    "bottleneck_stage": "REPLIED -> DEMO_BOOKED",
    "bottleneck_conversion": "18%",
    "avg_cycle_days": 22
  },
  "channels": [
    {"name": "Cold Email", "demos": 6, "cost_per_demo": "INR 1,800", "trend": "improving"},
    {"name": "LinkedIn", "demos": 4, "cost_per_demo": "INR 2,200", "trend": "stable"},
    {"name": "Inbound", "demos": 3, "cost_per_demo": "INR 1,500", "trend": "improving"},
    {"name": "Instagram", "demos": 1, "cost_per_demo": "INR 4,000", "trend": "declining"}
  ],
  "wins_losses": {
    "deals_won": 4,
    "deals_lost": 10,
    "top_win_factor": "CRO audit as sales tool",
    "top_loss_reason": "Budget/timing",
    "best_segment": "Post-PMF D2C India"
  },
  "recommendations": [
    {
      "title": "Double down on CRO audit as lead magnet",
      "data_basis": "3 of 4 won deals received a CRO audit before proposal",
      "action": "Offer free CRO audit to all HOT leads within 24 hours",
      "expected_impact": "+20% demo-to-proposal conversion",
      "timeline": "Implement this week",
      "priority": "HIGH"
    }
  ],
  "next_month_targets": {
    "leads": 100,
    "demos": 18,
    "revenue": "INR 4L",
    "key_initiative": "Launch inbound content engine (2 blog posts/week + social calendar)",
    "experiments": ["Test video testimonial in outreach sequence", "Try Reddit community engagement"]
  }
}
```

## Automation

This playbook is designed to run monthly:
1. **Manual**: Run `/strategic-review` on the first Monday of each month
2. **Cron**: Schedule for 1st of each month at 9 AM
3. **Reminder**: Set a recurring calendar event

## Example Usage

Trigger phrases:
- "Run the monthly strategic review for March"
- "Generate the executive summary for last month"
- "How did we perform this month?"
- "Pull together the monthly leadership report"
- "Compare this month's performance to last month"
- "What are our strategic priorities for next month?"
