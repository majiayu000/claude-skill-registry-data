---
name: revenue-forecaster
description: Revenue forecast from pipeline data with stage-weighted probability and sensitivity analysis
tags: [revenue, forecast, pipeline, finance, planning]
---

# Revenue Forecaster

Generates revenue forecasts from pipeline data using stage-weighted probability. Projects monthly and quarterly revenue, compares forecasts to targets, and runs sensitivity analysis across best, expected, and worst case scenarios. Designed for agencies and B2B businesses with a stage-based sales pipeline.

## Prerequisites

- `agency.config.json` in the project root
- Pipeline data: deals by stage with values and expected close dates
- Optional: historical close rates for model calibration
- Optional: revenue targets for comparison
- Optional: `crm-writer` integration for pulling live pipeline data

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract pipeline configuration:
   - `crm.stages[]` -- pipeline stages with names and order
   - `crm.stage_probabilities` -- conversion probability per stage (if defined)
   - `pricing.minimum_retainer` -- minimum deal size
   - `pricing.average_deal_size` -- for gap-filling estimates
3. Extract `tools.crm` for data access method.
4. Extract `targets.revenue.monthly` and `targets.revenue.quarterly` if defined.
5. If `crm.stage_probabilities` is not defined, use defaults:
   ```
   New Lead: 5%
   Qualified: 15%
   Discovery Call: 30%
   Proposal Sent: 50%
   Negotiation: 70%
   Verbal Commit: 85%
   Closed Won: 100%
   Closed Lost: 0%
   ```

## Phase 1: Gather Pipeline Data

Collect or retrieve current pipeline. Each deal needs:

```json
{
  "deal_id": "deal_001",
  "company": "Acme Corp",
  "deal_value": 75000,
  "recurring": true,
  "billing_cycle": "monthly",
  "stage": "Proposal Sent",
  "expected_close_date": "2024-04-15",
  "days_in_stage": 12,
  "owner": "sales_rep_1",
  "notes": "Waiting on budget approval"
}
```

**Data sources:**
- CRM pull via `crm-writer`
- Manual input (user provides deal list)
- Spreadsheet import (CSV/JSON)

Validate the data:
- Flag deals with missing close dates (estimate based on average cycle)
- Flag deals with no value (use `pricing.average_deal_size`)
- Flag stale deals (in same stage for over 30 days)
- Flag deals past their expected close date

## Phase 2: Stage-Weighted Pipeline Calculation

Apply stage probability to each deal:

```
WEIGHTED PIPELINE
===
Deal              | Stage           | Value    | Probability | Weighted Value
------------------|-----------------|----------|-------------|---------------
Acme Corp         | Proposal Sent   | $75,000  | 50%         | $37,500
Beta Inc          | Discovery Call  | $50,000  | 30%         | $15,000
Gamma Ltd         | Negotiation     | $100,000 | 70%         | $70,000
Delta Co          | Qualified       | $40,000  | 15%         | $6,000
                  |                 |          |             |
TOTAL PIPELINE    |                 | $265,000 |             | $128,500
```

Summary metrics:
- **Total pipeline value**: sum of all deal values
- **Weighted pipeline value**: sum of all weighted values
- **Pipeline coverage ratio**: weighted pipeline / monthly target (aim for 3x+)
- **Average deal size**: mean deal value
- **Deal count by stage**: distribution across stages

## Phase 3: Monthly and Quarterly Projections

Project revenue by expected close date:

```
MONTHLY REVENUE PROJECTION
===
Month     | Deals Expected | Weighted Revenue | Cumulative
----------|---------------|------------------|----------
April     | 5             | $52,500          | $52,500
May       | 8             | $78,000          | $130,500
June      | 3             | $31,000          | $161,500

Q2 TOTAL  | 16            | $161,500         |
```

For each month:
1. Filter deals with expected close date in that month
2. Apply stage-weighted probability
3. Sum weighted values

For recurring revenue deals:
- Include the recurring amount in all subsequent months after close
- Track MRR (monthly recurring revenue) growth separately

```
MRR TRAJECTORY
===
Month     | New MRR  | Churned MRR | Net MRR  | Total MRR
----------|----------|-------------|----------|----------
April     | $15,000  | $0          | $15,000  | $45,000
May       | $20,000  | $5,000      | $15,000  | $60,000
June      | $8,000   | $0          | $8,000   | $68,000
```

## Phase 4: Compare to Targets

If revenue targets are defined:

```
FORECAST vs TARGET
===
Period    | Target    | Forecast  | Gap       | On Track?
----------|-----------|-----------|-----------|----------
April     | $60,000   | $52,500   | -$7,500   | AT RISK
May       | $60,000   | $78,000   | +$18,000  | AHEAD
June      | $60,000   | $31,000   | -$29,000  | BEHIND
Q2 Total  | $180,000  | $161,500  | -$18,500  | AT RISK
```

Calculate:
- **Forecast accuracy**: weighted pipeline / target
- **Gap to target**: additional pipeline needed
- **Deals needed to close gap**: gap / average deal size
- **Leads needed**: deals needed / average conversion rate

## Phase 5: Sensitivity Analysis

Run three scenarios:

**Best Case:**
- Stage probabilities increased by 20% (capped at 100%)
- All deals close on time
- No deals move to Closed Lost

**Expected Case:**
- Stage probabilities as configured
- Historical win rate applied
- Average slip of 2 weeks for deals in early stages

**Worst Case:**
- Stage probabilities decreased by 30%
- 20% of deals slip by one month
- Highest-value deal in each month removed (largest deal risk)

```
SENSITIVITY ANALYSIS
===
Scenario     | Q2 Revenue  | vs Target  | Confidence
-------------|-------------|------------|----------
Best Case    | $210,000    | +$30,000   | 15% likely
Expected     | $161,500    | -$18,500   | 55% likely
Worst Case   | $95,000     | -$85,000   | 30% likely
```

Run a **single-deal risk analysis**:
- What happens if the largest deal is lost?
- What percentage of the forecast depends on the top 3 deals?
- Is revenue concentrated or distributed?

```
CONCENTRATION RISK
===
Top 1 deal: $100,000 (38% of pipeline)  -- HIGH concentration risk
Top 3 deals: $225,000 (85% of pipeline) -- CRITICAL concentration risk
Remaining 13 deals: $40,000 (15% of pipeline)
```

## Phase 6: Velocity Analysis

Calculate pipeline velocity metrics:

```
PIPELINE VELOCITY
===
Metric                        | Value    | Trend
------------------------------|----------|------
Average days to close         | 34 days  | Improving (was 42)
Average days per stage        | 8 days   | Stable
Fastest close (last 90 days)  | 12 days  |
Slowest close (last 90 days)  | 78 days  |
Stale deals (30+ days)        | 4 deals  | Action needed
```

Identify bottleneck stages:
- Which stage has the longest average duration?
- Which stage has the highest drop-off rate?
- Recommendations for accelerating each bottleneck

## Phase 7: Output

Return structured JSON:

```json
{
  "revenue_forecast": {
    "generated_date": "2024-03-15",
    "pipeline_summary": {
      "total_deals": 16,
      "total_pipeline_value": 265000,
      "weighted_pipeline_value": 128500,
      "average_deal_size": 16563,
      "pipeline_coverage_ratio": 2.1
    },
    "stage_distribution": [
      { "stage": "Qualified", "deals": 4, "value": 80000 },
      { "stage": "Discovery Call", "deals": 5, "value": 75000 }
    ],
    "monthly_projection": [
      {
        "month": "2024-04",
        "deals_expected": 5,
        "weighted_revenue": 52500,
        "target": 60000,
        "gap": -7500,
        "status": "at_risk"
      }
    ],
    "quarterly_projection": {
      "quarter": "Q2 2024",
      "forecast": 161500,
      "target": 180000,
      "gap": -18500,
      "status": "at_risk"
    },
    "sensitivity": {
      "best_case": { "revenue": 210000, "probability": 0.15 },
      "expected": { "revenue": 161500, "probability": 0.55 },
      "worst_case": { "revenue": 95000, "probability": 0.30 }
    },
    "concentration_risk": {
      "top_deal_pct": 0.38,
      "top_3_deals_pct": 0.85,
      "risk_level": "critical"
    },
    "velocity": {
      "avg_days_to_close": 34,
      "avg_days_per_stage": 8,
      "stale_deals": 4,
      "bottleneck_stage": "Proposal Sent"
    },
    "recommendations": [
      "Close the $7,500 April gap by accelerating 2 Discovery Call deals",
      "Reduce concentration risk by adding 5+ smaller deals to pipeline",
      "Address 4 stale deals: either advance or disqualify"
    ]
  }
}
```

## Example Usage

**Trigger phrases:**
- "Forecast revenue for next quarter"
- "What does our pipeline look like for April?"
- "Run a revenue forecast from our CRM data"
- "Will we hit our Q2 target?"
- "Show me pipeline coverage and forecast"
- "What's our worst-case revenue scenario?"

```
User: Forecast Q2 revenue from our pipeline
Assistant: [pulls pipeline data, applies stage weights, projects $161K against $180K target, flags $18.5K gap, identifies concentration risk in top 3 deals, recommends pipeline-building actions]
```

```
User: Are we going to hit target this month?
Assistant: [filters to current month deals, runs weighted forecast, compares to monthly target, runs sensitivity showing 55% likely to miss by $7.5K, suggests specific deals to accelerate]
```
