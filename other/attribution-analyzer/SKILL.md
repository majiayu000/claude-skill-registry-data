---
name: attribution-analyzer
description: Multi-touch attribution analysis across marketing channels with multiple models
tags: [attribution, analytics, marketing, roi, channels]
---

# Attribution Analyzer

Performs multi-touch attribution analysis on lead-to-conversion journey data. Applies five attribution models (first-touch, last-touch, linear, time-decay, U-shaped) to the same dataset and compares outputs. Identifies highest-impact channels and touchpoints, calculates channel ROI, and recommends budget allocation shifts. Works with CRM data or manually provided touchpoint logs.

## Prerequisites

- `agency.config.json` in the project root
- Touchpoint data: lead journeys with channel, timestamp, and conversion status
- Optional: channel spend data for ROI calculations
- Optional: `crm-writer` integration for pulling journey data from CRM

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract channel configuration:
   - `outreach.channels[]` -- active marketing channels
   - `outreach.cadence[]` -- touchpoint sequence and timing
3. Extract `tools.crm` for CRM data access method.
4. Extract `tools.analytics` for any analytics platform integration.
5. Check for `attribution.default_model` preference in config.

## Phase 1: Gather Touchpoint Data

Collect or retrieve lead journey data. Each journey record needs:

```json
{
  "lead_id": "lead_001",
  "converted": true,
  "conversion_value": 5000,
  "conversion_date": "2024-03-15",
  "touchpoints": [
    {
      "channel": "linkedin_ad",
      "timestamp": "2024-02-01T10:00:00Z",
      "type": "impression",
      "content": "CRO case study carousel"
    },
    {
      "channel": "cold_email",
      "timestamp": "2024-02-05T14:30:00Z",
      "type": "email_open",
      "content": "Touch 1 -- PAS framework"
    },
    {
      "channel": "website",
      "timestamp": "2024-02-06T09:00:00Z",
      "type": "page_visit",
      "content": "Case study page"
    },
    {
      "channel": "cold_email",
      "timestamp": "2024-02-10T11:00:00Z",
      "type": "email_reply",
      "content": "Touch 2 follow-up"
    },
    {
      "channel": "demo_call",
      "timestamp": "2024-02-15T15:00:00Z",
      "type": "meeting",
      "content": "Discovery call"
    }
  ]
}
```

**Data sources:**
- Manual input (user provides CSV or JSON)
- CRM pull via `crm-writer` (read from Outreach CRM tab)
- Analytics export (Google Analytics, Mixpanel)

If data is incomplete, flag gaps and proceed with available data.

## Phase 2: Apply Attribution Models

Apply all five models to every converted lead's touchpoint chain:

### Model 1: First-Touch Attribution
- 100% credit to the first touchpoint in the journey
- Use case: understanding which channels drive awareness and initial discovery
- Formula: `credit = conversion_value` assigned entirely to touchpoint[0]

### Model 2: Last-Touch Attribution
- 100% credit to the last touchpoint before conversion
- Use case: understanding which channels close deals
- Formula: `credit = conversion_value` assigned entirely to touchpoint[n-1]

### Model 3: Linear Attribution
- Equal credit distributed across all touchpoints
- Use case: valuing every interaction in the journey equally
- Formula: `credit_per_touch = conversion_value / touchpoint_count`

### Model 4: Time-Decay Attribution
- More credit to touchpoints closer to conversion
- Use case: understanding recent influence while acknowledging earlier touches
- Formula: `weight = 2^((days_before_conversion * -1) / half_life)` where half_life = 7 days
- Normalize weights so they sum to 1.0

### Model 5: U-Shaped (Position-Based) Attribution
- 40% to first touch, 40% to last touch, 20% split among middle touches
- Use case: valuing both discovery and closing while acknowledging the nurture
- Formula:
  - First touch: `0.4 * conversion_value`
  - Last touch: `0.4 * conversion_value`
  - Middle touches: `(0.2 * conversion_value) / middle_touch_count`

For each model, aggregate credit by channel across all converted leads.

## Phase 3: Compare Model Outputs

Build a comparison matrix:

```
CHANNEL ATTRIBUTION COMPARISON
===
Channel          | First-Touch | Last-Touch | Linear  | Time-Decay | U-Shaped
-----------------|-------------|------------|---------|------------|--------
LinkedIn Ads     | $12,000     | $3,000     | $7,500  | $5,200     | $8,400
Cold Email       | $8,000      | $15,000    | $10,000 | $11,800    | $9,600
Website/Organic  | $3,000      | $2,000     | $6,500  | $4,000     | $3,200
Demo Calls       | $0          | $18,000    | $6,000  | $12,000    | $7,200
Referrals        | $2,000      | $0         | $3,000  | $1,500     | $1,600
```

Calculate the **consensus score** per channel:
- Average attribution value across all 5 models
- Rank channels by consensus score
- Flag channels with high variance (score differs more than 2x between models)

## Phase 4: Channel ROI Analysis

If spend data is available, calculate ROI per channel per model:

```
CHANNEL ROI (by attribution model)
===
Channel          | Spend   | First-Touch ROI | Linear ROI | Time-Decay ROI | Consensus ROI
-----------------|---------|-----------------|------------|----------------|-------------
LinkedIn Ads     | $2,000  | 6.0x            | 3.8x       | 2.6x           | 4.2x
Cold Email       | $500    | 16.0x           | 20.0x      | 23.6x          | 19.2x
Website/Organic  | $1,000  | 3.0x            | 6.5x       | 4.0x           | 3.2x
```

Identify:
- **Highest ROI channel**: best return per dollar regardless of model
- **Most scalable channel**: high ROI with room to increase spend
- **Underperforming channel**: low ROI across multiple models
- **Discovery channel**: high in first-touch but low in last-touch
- **Closing channel**: high in last-touch but low in first-touch

## Phase 5: Touchpoint Sequence Analysis

Beyond channel-level attribution, analyze touchpoint patterns:

**Winning sequences** (most common paths among converted leads):
```
TOP CONVERSION PATHS:
1. LinkedIn Ad -> Cold Email -> Website -> Demo Call (35% of conversions)
2. Cold Email -> Cold Email -> Demo Call (25% of conversions)
3. Referral -> Website -> Demo Call (20% of conversions)
```

**Average touches to conversion:**
- Overall: X touchpoints
- By channel entry point: which first-touch channel leads to fastest conversion
- By deal size: do larger deals require more touches

**Drop-off points:**
- Where in the sequence do leads most commonly go cold
- Which channel transitions have the highest drop-off rate

## Phase 6: Recommendations

Generate actionable recommendations:

```
BUDGET RECOMMENDATIONS:
===
1. INCREASE: [Channel] -- [reason, supported by data]
   Current spend: $X -> Recommended: $Y (+Z%)
   Expected impact: [projected additional revenue]

2. DECREASE: [Channel] -- [reason, supported by data]
   Current spend: $X -> Recommended: $Y (-Z%)
   Expected savings: [amount freed up]

3. TEST: [Channel/tactic] -- [hypothesis to validate]
   Budget: $X for [duration]
   Success metric: [what to measure]

SEQUENCE RECOMMENDATIONS:
===
1. Prioritize [channel] as first touch for [segment]
2. Ensure [channel] is always in the path -- linear model shows consistent contribution
3. [Channel] is most effective as the final touch before conversion
```

## Phase 7: Output

Return structured JSON:

```json
{
  "attribution_report": {
    "analysis_date": "2024-03-15",
    "data_summary": {
      "total_leads": 150,
      "converted_leads": 45,
      "total_revenue": "$225,000",
      "total_touchpoints_analyzed": 487,
      "average_touches_to_conversion": 4.2,
      "date_range": "2024-01-01 to 2024-03-15"
    },
    "models": {
      "first_touch": { "channel_scores": {} },
      "last_touch": { "channel_scores": {} },
      "linear": { "channel_scores": {} },
      "time_decay": { "channel_scores": {}, "half_life_days": 7 },
      "u_shaped": { "channel_scores": {} }
    },
    "consensus_ranking": [
      { "channel": "cold_email", "consensus_score": 19200, "consensus_roi": "19.2x" }
    ],
    "top_conversion_paths": [],
    "drop_off_analysis": {},
    "channel_roi": {},
    "recommendations": {
      "increase": [],
      "decrease": [],
      "test": [],
      "sequence_changes": []
    }
  }
}
```

## Example Usage

**Trigger phrases:**
- "Run attribution analysis on our pipeline"
- "Which channel is driving the most revenue?"
- "Compare first-touch vs last-touch attribution"
- "Analyze our marketing touchpoints for Q1"
- "What's the ROI of our cold email vs LinkedIn ads?"
- "Show me the conversion paths for our best deals"

```
User: Run attribution analysis on our Q1 pipeline
Assistant: [pulls touchpoint data from CRM, applies 5 models, builds comparison matrix, identifies cold email as highest ROI channel, recommends increasing email volume and testing LinkedIn content changes]
```

```
User: Which channel should we invest more in?
Assistant: [runs full attribution, finds LinkedIn drives discovery but email closes deals, recommends maintaining LinkedIn for awareness and doubling email follow-up sequences]
```
