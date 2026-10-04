---
name: pipeline-dashboard
description: Weekly pipeline metrics, forecast, and trend dashboard in structured markdown
tags: [pipeline, dashboard, metrics, forecast, weekly-review]
---

# Pipeline Dashboard

Generates a weekly pipeline metrics and forecast dashboard. Pulls CRM data, calculates key metrics (pipeline value, new leads, conversion rates, velocity, forecast vs target, channel attribution), compares week-over-week trends, and outputs a structured markdown dashboard. Designed to run every Monday as part of a weekly review cadence.

## Prerequisites

- `agency.config.json` in the project root
- CRM data accessible via `crm-writer`
- Optional: previous week's dashboard for trend comparison
- Optional: `revenue-forecaster` output for forecast integration

## Capabilities Used

1. `revenue-forecaster` -- for stage-weighted pipeline forecast and sensitivity analysis
2. `attribution-analyzer` -- for channel attribution on new leads
3. `crm-auditor` -- for data quality score inclusion
4. `crm-writer` -- for reading pipeline data

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract targets:
   - `targets.revenue.monthly` -- monthly revenue target
   - `targets.leads_per_week` -- weekly lead generation target
   - `targets.demos_per_week` -- weekly demo booking target
   - `targets.deals_per_month` -- monthly close target
3. Extract `crm.stages[]` for pipeline stage definitions.
4. Extract `crm.stage_probabilities` for weighted calculations.
5. Check for previous dashboard: look for `pipeline-dashboard-YYYY-MM-DD.md` in project root.

## Phase 1: Pull Pipeline Data

Read all pipeline data from CRM:

**Data to collect:**
- All active deals with stage, value, owner, dates, and source
- Leads added this week (by creation date)
- Stage changes this week (leads that moved forward or backward)
- Deals closed this week (won and lost)
- Activities logged this week (emails sent, calls made, demos completed)

## Phase 2: Calculate Key Metrics

### Pipeline Overview
```
PIPELINE SNAPSHOT -- Week of [Date]
===
Total active deals: [N]
Total pipeline value: $[X]
Weighted pipeline value: $[Y]
Average deal size: $[Z]
Pipeline coverage ratio: [Y / monthly_target]x
```

### New Activity This Week
```
THIS WEEK'S ACTIVITY
===
New leads added: [N] (target: [target])
Demos booked: [N] (target: [target])
Proposals sent: [N]
Deals closed won: [N] ($[X])
Deals closed lost: [N] ($[X])
Win rate (this week): [%]
```

### Conversion Rates by Stage
```
STAGE CONVERSION RATES
===
Stage               | Deals | Value     | Conversion to Next | Avg Days in Stage
--------------------|-------|-----------|-------------------|------------------
New Lead            | 25    | $125,000  | 60% -> Qualified  | 4 days
Qualified           | 15    | $112,500  | 67% -> Discovery  | 7 days
Discovery Call      | 10    | $100,000  | 70% -> Proposal   | 5 days
Proposal Sent       | 7     | $87,500   | 57% -> Negotiation| 12 days
Negotiation         | 4     | $60,000   | 75% -> Won        | 8 days
```

### Velocity Metrics
```
PIPELINE VELOCITY
===
Average days lead-to-close: [N] days
Average days per stage: [N] days
Deals moving forward this week: [N]
Deals stuck (no movement 14+ days): [N]
Fastest close this quarter: [N] days
```

### Forecast
Integrate `revenue-forecaster` output:
```
REVENUE FORECAST
===
This month forecast: $[X] (target: $[T], gap: $[G])
Next month forecast: $[X]
Quarter forecast: $[X] (target: $[T])

Sensitivity:
  Best case: $[X]
  Expected: $[Y]
  Worst case: $[Z]
```

### Channel Attribution
```
LEAD SOURCES (this week)
===
Channel          | New Leads | % of Total | Demos Booked
-----------------|-----------|------------|-------------
Cold Email       | 8         | 40%        | 3
LinkedIn         | 5         | 25%        | 2
Inbound/Organic  | 4         | 20%        | 1
Referral         | 2         | 10%        | 1
Other            | 1         | 5%         | 0
```

## Phase 3: Week-Over-Week Trends

Compare current week to previous week:

```
WEEK-OVER-WEEK TRENDS
===
Metric                  | Last Week | This Week | Change   | Status
------------------------|-----------|-----------|----------|--------
New leads               | 15        | 20        | +33.3%   | UP
Demos booked            | 4         | 7         | +75.0%   | UP
Pipeline value          | $380K     | $425K     | +11.8%   | UP
Weighted pipeline       | $145K     | $168K     | +15.9%   | UP
Deals closed won        | 1         | 2         | +100.0%  | UP
Deals closed lost       | 2         | 1         | -50.0%   | IMPROVED
Win rate                | 33%       | 67%       | +100.0%  | UP
Avg deal cycle          | 38 days   | 34 days   | -10.5%   | FASTER
Stale deals             | 8         | 6         | -25.0%   | IMPROVED
CRM completeness        | 78%       | 82%       | +5.1%    | IMPROVED
```

Flag items that need attention:
- Metrics trending wrong for 2+ consecutive weeks
- Metrics significantly below target
- New records (best week ever, worst metric, etc.)

## Phase 4: Action Items

Generate specific action items based on the data:

```
PRIORITY ACTIONS THIS WEEK
===
1. [URGENT] Close the $7,500 April gap -- accelerate Acme Corp (Proposal stage, $25K)
2. [HIGH] Follow up on 3 stale Discovery Call leads (12+ days without movement)
3. [MEDIUM] Book 3 more demos to hit weekly target (at 4/7 target)
4. [LOW] Clean up 6 CRM records flagged by crm-auditor

DEALS TO WATCH:
- Acme Corp ($75K, Proposal Sent, 15 days) -- budget decision expected this week
- Beta Inc ($50K, Negotiation, 8 days) -- waiting on contract review
- Gamma Ltd ($100K, Discovery, 3 days) -- demo scheduled Thursday
```

## Phase 5: Output

Generate the dashboard in markdown format and as structured JSON:

**Markdown output** (saved as `pipeline-dashboard-YYYY-MM-DD.md`):
```markdown
# Pipeline Dashboard -- Week of [Date]

## Executive Summary
[2-3 sentences: pipeline health, target status, key wins/concerns]

## Pipeline Snapshot
[Table from Phase 2]

## This Week's Activity
[Activity metrics vs targets]

## Stage Conversion Funnel
[Stage table with conversion rates]

## Revenue Forecast
[Forecast with sensitivity range]

## Lead Sources
[Channel attribution table]

## Trends
[Week-over-week comparison table]

## Priority Actions
[Ordered action items]

## Deals to Watch
[Key deals with status and next steps]

---
Generated by pipeline-dashboard | Data as of [timestamp]
```

**JSON output:**
```json
{
  "pipeline_dashboard": {
    "week_of": "2024-03-11",
    "generated_at": "2024-03-11T09:00:00Z",
    "executive_summary": "",
    "pipeline_snapshot": {
      "total_deals": 61,
      "total_value": 425000,
      "weighted_value": 168000,
      "average_deal_size": 6967,
      "coverage_ratio": 2.8
    },
    "weekly_activity": {
      "new_leads": { "actual": 20, "target": 20, "status": "on_track" },
      "demos_booked": { "actual": 7, "target": 7, "status": "on_track" },
      "deals_won": { "count": 2, "value": 50000 },
      "deals_lost": { "count": 1, "value": 15000 },
      "win_rate": 0.67
    },
    "stage_funnel": [],
    "forecast": {
      "this_month": 52500,
      "target": 60000,
      "gap": -7500,
      "sensitivity": {}
    },
    "lead_sources": [],
    "trends": {},
    "action_items": [],
    "deals_to_watch": [],
    "data_quality_score": 82
  }
}
```

## Example Usage

**Trigger phrases:**
- "Generate the weekly pipeline dashboard"
- "Pipeline review for this week"
- "Show me the pipeline metrics"
- "Weekly sales dashboard"
- "How's the pipeline looking?"
- "Monday morning pipeline check"

```
User: Generate the weekly pipeline dashboard
Assistant: [pulls CRM data, calculates all metrics, compares to last week, identifies 20 new leads (on target), $425K pipeline (+11.8%), flags $7.5K April gap and 3 stale deals, generates dashboard markdown and JSON]
```

```
User: Are we on track this month?
Assistant: [runs pipeline dashboard focused on monthly forecast, shows $52.5K weighted forecast vs $60K target, identifies deals that need to close to bridge the gap, lists specific actions]
```
