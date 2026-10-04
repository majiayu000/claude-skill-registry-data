---
name: campaign-analyzer
description: Cross-channel campaign performance analysis with blended CAC and budget recommendations
tags: [campaign, analytics, cross-channel, performance, marketing]
---

# Campaign Analyzer

Performs cross-channel campaign performance analysis across email outreach, paid ads, social media, organic traffic, and LinkedIn outreach. Normalizes metrics across channels, identifies top and bottom performers, calculates blended CAC, and produces budget reallocation recommendations. Designed to run weekly or monthly as part of a marketing review cadence.

## Prerequisites

- `agency.config.json` in the project root
- Performance data from active channels (manual input, analytics exports, or API pulls)
- Optional: `attribution-analyzer` output for attribution-weighted view
- Optional: channel spend data for ROI and CAC calculations

## Capabilities Used

1. `attribution-analyzer` -- for multi-touch attribution layer on top of channel performance
2. `crm-writer` -- for pulling pipeline data correlated to campaigns
3. `revenue-forecaster` -- for connecting campaign performance to revenue impact

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract active channels:
   - `outreach.channels[]` -- channels in use
   - `outreach.cadence[]` -- email/LinkedIn sequence details
3. Extract `tools.*` for data source access:
   - `tools.email_sending` -- email platform (Gmail, Smartlead, Instantly)
   - `tools.ads` -- ad platforms (Meta Ads, Google Ads, LinkedIn Ads)
   - `tools.analytics` -- website analytics (GA4, Mixpanel)
   - `tools.social` -- social media tools
4. Extract `targets.*` for benchmark comparison:
   - `targets.leads_per_week`
   - `targets.demos_per_week`
   - `targets.cac_target`

## Phase 1: Gather Channel Performance Data

Collect metrics for each active channel. Request data from user or pull via integrations:

### Email Outreach
```
EMAIL METRICS (period: [date range])
===
Emails sent: [N]
Delivery rate: [%]
Open rate: [%]
Click rate: [%]
Reply rate: [%]
Positive reply rate: [%]
Demos booked from email: [N]
Unsubscribe rate: [%]
Bounce rate: [%]
Cost (tools + time): $[X]
```

### Paid Ads (per platform)
```
[PLATFORM] AD METRICS (period: [date range])
===
Impressions: [N]
Clicks: [N]
CTR: [%]
CPC: $[X]
Spend: $[X]
Conversions: [N]
CPA: $[X]
ROAS: [X]x
Landing page conversion rate: [%]
```

### LinkedIn Outreach
```
LINKEDIN METRICS (period: [date range])
===
Connection requests sent: [N]
Acceptance rate: [%]
Messages sent: [N]
Reply rate: [%]
Positive reply rate: [%]
Demos booked: [N]
Profile views generated: [N]
Cost (Dripify/tool + time): $[X]
```

### Organic / Content
```
ORGANIC METRICS (period: [date range])
===
Website sessions: [N]
Unique visitors: [N]
Blog posts published: [N]
Organic leads captured: [N]
Lead magnet downloads: [N]
Top pages by traffic: [list]
SEO keywords ranking: [count]
Social media posts: [N]
Social engagement rate: [%]
Cost (content creation time): $[X]
```

## Phase 2: Normalize Metrics

Create a unified performance view across channels:

```
NORMALIZED CHANNEL COMPARISON
===
Channel          | Reach    | Engagements | Leads | Demos | Cost    | CPL     | Cost/Demo
-----------------|----------|-------------|-------|-------|---------|---------|----------
Cold Email       | 500 sent | 125 opens   | 15    | 5     | $200    | $13.33  | $40.00
LinkedIn         | 200 sent | 80 accepts  | 8     | 3     | $350    | $43.75  | $116.67
Meta Ads         | 50K imp  | 800 clicks  | 20    | 4     | $2,000  | $100.00 | $500.00
Google Ads       | 10K imp  | 300 clicks  | 12    | 2     | $1,500  | $125.00 | $750.00
Organic          | 5K visits| 200 leads   | 10    | 2     | $500    | $50.00  | $250.00
Instagram        | 20K imp  | 500 engage  | 3     | 0     | $300    | $100.00 | N/A
```

**Normalization rules:**
- All channels measured by the same funnel: Reach -> Engagement -> Lead -> Demo -> Close
- Cost includes both direct spend and estimated labor cost
- CPL = Cost / Leads generated
- Cost per Demo = Cost / Demos booked
- If a channel has no demos, it still gets measured on lead generation

## Phase 3: Identify Top and Bottom Performers

Rank channels by multiple dimensions:

```
CHANNEL RANKINGS
===
By Volume (most leads):
1. Meta Ads (20 leads)
2. Cold Email (15 leads)
3. Google Ads (12 leads)

By Efficiency (lowest CPL):
1. Cold Email ($13.33/lead)
2. LinkedIn ($43.75/lead)
3. Organic ($50.00/lead)

By Demo Conversion (leads -> demos):
1. Cold Email (33% conversion)
2. LinkedIn (37.5% conversion)
3. Organic (20% conversion)

By Cost per Demo:
1. Cold Email ($40/demo)
2. LinkedIn ($117/demo)
3. Organic ($250/demo)

TOP PERFORMER: Cold Email -- lowest CPL, highest demo conversion, lowest cost/demo
BOTTOM PERFORMER: Instagram -- 3 leads, 0 demos, $100 CPL with no pipeline impact
```

## Phase 4: Calculate Blended CAC

```
BLENDED CAC CALCULATION
===
Total marketing spend: $4,850
Total demos booked: 16
Total clients closed (this period): 3
Revenue from closed clients: $225,000

Blended cost per demo: $303.13
Blended CAC: $1,616.67
LTV:CAC ratio: [LTV] / $1,616.67 = [X]:1

CAC by channel:
- Cold Email: $40/demo, $200/client (estimated)
- LinkedIn: $117/demo, $350/client (estimated)
- Meta Ads: $500/demo, $2,000/client (estimated)
```

Compare to `targets.cac_target` from config. Flag if blended CAC exceeds target.

## Phase 5: Trend Analysis

If historical data is available, compare week-over-week or month-over-month:

```
WEEK-OVER-WEEK TRENDS
===
Metric              | Last Week | This Week | Change  | Direction
--------------------|-----------|-----------|---------|----------
Total leads         | 55        | 68        | +23.6%  | UP
Total demos         | 12        | 16        | +33.3%  | UP
Blended CPL         | $82.50    | $71.32    | -13.5%  | IMPROVING
Email reply rate    | 3.2%      | 4.1%      | +28.1%  | UP
LinkedIn acceptance | 42%       | 40%       | -4.8%   | STABLE
Ad ROAS             | 2.1x      | 1.8x      | -14.3%  | DECLINING
```

Flag significant changes (>20% movement in either direction).

## Phase 6: Budget Recommendations

Based on performance data, recommend budget shifts:

```
BUDGET RECOMMENDATIONS
===
Current allocation:
  Cold Email: $200 (4.1%)
  LinkedIn: $350 (7.2%)
  Meta Ads: $2,000 (41.2%)
  Google Ads: $1,500 (30.9%)
  Organic: $500 (10.3%)
  Instagram: $300 (6.2%)
  TOTAL: $4,850

Recommended reallocation:
  Cold Email: $400 (+$200, +100%) -- highest efficiency, scale volume
  LinkedIn: $500 (+$150, +43%) -- strong demo conversion, increase reach
  Meta Ads: $1,500 (-$500, -25%) -- high CPA, test new creatives first
  Google Ads: $1,200 (-$300, -20%) -- diminishing returns at current spend
  Organic: $750 (+$250, +50%) -- building long-term pipeline at low cost
  Instagram: $0 (-$300, -100%) -- no demos generated, pause and reassess
  TOTAL: $4,350 (saved $500)

Projected impact:
  Additional leads: +12 (from email and LinkedIn scaling)
  Additional demos: +4
  Projected new CPL: $58.47 (from $71.32)
```

## Phase 7: Output

Return structured JSON:

```json
{
  "campaign_analysis": {
    "analysis_date": "2024-03-15",
    "period": "2024-03-08 to 2024-03-15",
    "channels": [
      {
        "channel": "cold_email",
        "metrics": {
          "reach": 500,
          "engagements": 125,
          "leads": 15,
          "demos": 5,
          "cost": 200,
          "cpl": 13.33,
          "cost_per_demo": 40.00
        },
        "rank_volume": 2,
        "rank_efficiency": 1,
        "rank_demo_conversion": 1,
        "status": "top_performer"
      }
    ],
    "blended_metrics": {
      "total_spend": 4850,
      "total_leads": 68,
      "total_demos": 16,
      "blended_cpl": 71.32,
      "blended_cac": 1616.67,
      "ltv_cac_ratio": null
    },
    "top_performer": { "channel": "cold_email", "reason": "lowest CPL and cost/demo" },
    "bottom_performer": { "channel": "instagram", "reason": "zero demos, high CPL" },
    "trends": {},
    "budget_recommendation": {
      "current_total": 4850,
      "recommended_total": 4350,
      "changes": [],
      "projected_impact": {
        "additional_leads": 12,
        "additional_demos": 4,
        "new_blended_cpl": 58.47
      }
    }
  }
}
```

## Example Usage

**Trigger phrases:**
- "Analyze campaign performance across channels"
- "Which marketing channel is performing best?"
- "Run a cross-channel performance review"
- "What's our blended CAC this month?"
- "Where should we reallocate marketing budget?"
- "Weekly campaign review"

```
User: Run a cross-channel campaign analysis for this week
Assistant: [gathers metrics from email, LinkedIn, ads, organic; normalizes into comparison table; identifies cold email as top performer; calculates $71 blended CPL; recommends pausing Instagram and scaling email volume]
```

```
User: Where should we shift ad budget?
Assistant: [analyzes ROAS and CPA across Meta and Google, compares to organic and outreach channels, recommends moving $800 from underperforming ads to email and LinkedIn outreach]
```
