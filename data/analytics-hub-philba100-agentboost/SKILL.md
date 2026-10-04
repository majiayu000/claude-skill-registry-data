---
name: analytics-hub
description: Enterprise pipeline analytics and business intelligence. Tracks conversion metrics, ROI, deal velocity, lead scoring correlation, and generates executive dashboards with real-time insights.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

### System Instructions
You are equipped with the `analytics-hub` skill for enterprise business intelligence. This tool aggregates data across all agent operations to provide actionable insights and performance metrics.

**CRITICAL:** All data is anonymized for privacy. Provide actionable recommendations based on patterns. Update metrics in real-time.

### Execution Protocol
Call the `run_js` tool with strictly formatted JSON:

```json
{
  "report_type": "pipeline_performance",
  "date_range": {
    "start_date": "2026-01-01",
    "end_date": "2026-04-10"
  },
  "metrics_requested": [
    "lead_volume",
    "qualification_rate",
    "demo_conversion",
    "deal_close_rate",
    "average_deal_size",
    "sales_cycle_length",
    "win_rate_by_industry",
    "roi_by_campaign"
  ],
  "segment_by": ["industry", "deal_size", "sales_rep"],
  "include_forecasts": true,
  "comparison_period": "last_quarter",
  "dashboard_format": "executive_summary"
}
```

### Outputs
The skill delivers:
- **Pipeline Summary:** Total leads, opportunities, revenue
- **Conversion Funnel:** Stage-by-stage conversion rates
- **Deal Metrics:** Average size, velocity, close rate
- **Lead Quality Analysis:** Score correlation with outcomes
- **Campaign Performance:** ROI and lead source quality
- **Trend Analysis:** Month-over-month growth
- **Forecast:** 30/60/90 day revenue projection
- **Bottleneck Analysis:** Where deals stall
- **Top Performers:** Best converting reps/campaigns
- **Executive Dashboard:** One-page visual summary

### Report Types Available
- `pipeline_performance`: Full sales funnel analysis
- `lead_quality_analysis`: Score vs. conversion correlation
- `campaign_roi`: By campaign performance
- `deal_velocity`: Sales cycle metrics
- `forecast`: Revenue projection
- `competitive_analysis`: Win rate vs competitors
- `custom_report`: User-defined metrics

### Example Tool Call
```javascript
run_js(data='{"report_type": "campaign_roi", "date_range": {"start_date": "2026-01-01", "end_date": "2026-04-10"}, "metrics_requested": ["campaign_name", "leads_generated", "qualified_leads", "demos_booked", "deals_closed", "total_revenue", "cost_per_lead", "roi"], "segment_by": ["campaign", "industry"], "include_forecasts": true, "dashboard_format": "detailed"}')
```

### Integration Points
- **Lead Qualifier:** Track score → conversion correlation
- **Meeting Scheduler:** Log demo conversion rates
- **Negotiation Engine:** Track deal close velocity
- **Bidding Engine:** Monitor average deal size
- **Email Orchestrator:** Campaign performance metrics
- **CRM Sync:** Source all operational data
