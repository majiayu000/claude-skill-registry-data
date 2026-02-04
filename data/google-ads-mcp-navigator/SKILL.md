---
name: google-ads-mcp-navigator
description: Streamlined guide for Google Ads API queries via MCP. Use when querying campaign performance, keyword metrics, conversion data, auction insights, or ad group analysis. Reduces context overhead by providing curated field references and common query patterns. Triggers on Google Ads, SEM performance, campaign analysis, keyword research, or auction insights requests.
---

# Google Ads MCP Navigator

This skill provides efficient navigation of the Google Ads MCP tool, reducing context overhead by documenting common query patterns, curated field lists, and RDC-specific account configurations.

## Quick Reference

### RDC Account IDs

| Account | Customer ID | Vertical | Notes |
|---------|-------------|----------|-------|
| RDC SEM Main | *see accessible_customers* | Buy/Mixed | Primary B2C search |
| RDC Rentals | *see accessible_customers* | Rent | Rentals vertical |
| RDC Seller | *see accessible_customers* | Sell | Seller marketplace |
| RDC New Construction | *see accessible_customers* | NC | Builder campaigns |

*Run `list_accessible_customers` to get current account IDs*

### Core Resources

| Resource | Use Case | Key Metrics Available |
|----------|----------|----------------------|
| `campaign` | Campaign settings, status, budget | bidding strategy, status, dates |
| `ad_group` | Ad group settings, bids | CPC bids, status, targeting |
| `ad_group_ad` | Ad creative, approval status | ad strength, policy status |
| `ad_group_criterion` | Keywords, audiences | quality score, bids |
| `search_term_view` | Search query data | search terms, match type |
| `keyword_view` | Keyword performance | joins with metrics |
| `geographic_view` | Geo performance | location type |
| `campaign_budget` | Budget settings | amount, delivery method |

### Metrics Resource

All performance metrics come from the `metrics` resource and must be joined with a primary resource.

## Workflow

1. **Identify the analysis type:**
   - Campaign performance → `campaign` + `metrics`
   - Keyword analysis → `ad_group_criterion` or `keyword_view` + `metrics`
   - Search query mining → `search_term_view` + `metrics`
   - Auction insights → `auction_insight` resource (special)
   - Geographic performance → `geographic_view` + `metrics`

2. **Load field references:**
   - Campaign fields → [references/campaign_fields.md](references/campaign_fields.md)
   - Metrics fields → [references/metrics_fields.md](references/metrics_fields.md)
   - Segment fields → [references/segment_fields.md](references/segment_fields.md)

3. **Apply required conditions:**
   - Always filter by date range (required for metrics)
   - Filter by campaign status for active-only analysis
   - Use segments for dimensional breakdowns

## Essential Field Lists

### Campaign Performance (Minimal)
```
Fields: campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, 
        metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, 
        metrics.conversions_value
Resource: campaign
Conditions: segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

### Keyword Performance (Minimal)
```
Fields: ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
        ad_group_criterion.quality_info.quality_score, metrics.impressions, metrics.clicks,
        metrics.cost_micros, metrics.conversions
Resource: ad_group_criterion
Conditions: ad_group_criterion.type = 'KEYWORD', segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

### Search Terms (Minimal)
```
Fields: search_term_view.search_term, search_term_view.status, 
        metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
Resource: search_term_view
Conditions: segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

### Geographic Performance (Minimal)
```
Fields: geographic_view.location_type, segments.geo_target_region,
        metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
Resource: geographic_view
Conditions: segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
```

## Common Query Patterns

### Campaign Summary (Last 30 Days)
```python
resource: "campaign"
fields: [
    "campaign.id",
    "campaign.name", 
    "campaign.status",
    "campaign.advertising_channel_type",
    "campaign.bidding_strategy_type",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros",
    "metrics.conversions",
    "metrics.conversions_value",
    "metrics.search_impression_share"
]
conditions: [
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'",
    "campaign.status = 'ENABLED'"
]
```

### Keyword Quality Score Analysis
```python
resource: "ad_group_criterion"
fields: [
    "campaign.name",
    "ad_group.name",
    "ad_group_criterion.keyword.text",
    "ad_group_criterion.keyword.match_type",
    "ad_group_criterion.quality_info.quality_score",
    "ad_group_criterion.quality_info.creative_quality_score",
    "ad_group_criterion.quality_info.post_click_quality_score",
    "ad_group_criterion.quality_info.search_predicted_ctr",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros"
]
conditions: [
    "ad_group_criterion.type = 'KEYWORD'",
    "ad_group_criterion.status = 'ENABLED'",
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'"
]
```

### Search Query Mining
```python
resource: "search_term_view"
fields: [
    "campaign.name",
    "ad_group.name",
    "search_term_view.search_term",
    "search_term_view.status",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros",
    "metrics.conversions",
    "metrics.conversions_value"
]
conditions: [
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'",
    "metrics.impressions > 0"
]
orderings: ["metrics.cost_micros DESC"]
limit: 1000
```

### Daily Performance Trend
```python
resource: "campaign"
fields: [
    "segments.date",
    "campaign.name",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros",
    "metrics.conversions"
]
conditions: [
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'",
    "campaign.status = 'ENABLED'"
]
orderings: ["segments.date ASC"]
```

### Device Performance
```python
resource: "campaign"
fields: [
    "campaign.name",
    "segments.device",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros",
    "metrics.conversions"
]
conditions: [
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'"
]
```

### Hour of Day Analysis
```python
resource: "campaign"
fields: [
    "campaign.name",
    "segments.hour",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.cost_micros",
    "metrics.conversions"
]
conditions: [
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'"
]
```

## Metric Calculations

### Derived Metrics (Calculate Post-Query)
| Metric | Calculation |
|--------|-------------|
| Cost | `cost_micros / 1,000,000` |
| CPC | `cost_micros / clicks / 1,000,000` |
| CTR | `clicks / impressions` |
| Conv Rate | `conversions / clicks` |
| CPA | `cost_micros / conversions / 1,000,000` |
| ROAS | `conversions_value / (cost_micros / 1,000,000)` |

### Impression Share Metrics
- `search_impression_share` - % of eligible impressions received
- `search_budget_lost_impression_share` - Lost due to budget
- `search_rank_lost_impression_share` - Lost due to rank
- `search_absolute_top_impression_share` - % in position 1

## Date Handling

**Critical**: The Google Ads API requires explicit date formatting.

- Format: `YYYY-MM-DD` (e.g., `2024-12-01`)
- Always use explicit dates, not literals like `TODAY` or `LAST_30_DAYS`
- Date conditions use `segments.date`

### Date Range Examples
```python
# Last 7 days (calculate actual dates)
conditions: [
    "segments.date >= '2024-12-10'",
    "segments.date <= '2024-12-17'"
]

# Specific month
conditions: [
    "segments.date >= '2024-11-01'",
    "segments.date <= '2024-11-30'"
]
```

## Status Values

### Campaign Status
- `ENABLED` - Active
- `PAUSED` - Paused by user
- `REMOVED` - Deleted

### Ad Group Criterion Status
- `ENABLED` - Active keyword
- `PAUSED` - Paused keyword
- `REMOVED` - Deleted keyword

### Search Term Status
- `ADDED` - Added as keyword
- `EXCLUDED` - Added as negative
- `ADDED_EXCLUDED` - Both
- `NONE` - Not actioned

## Channel Types

### Advertising Channel Types
- `SEARCH` - Search Network
- `DISPLAY` - Display Network
- `SHOPPING` - Shopping campaigns
- `VIDEO` - YouTube/Video
- `PERFORMANCE_MAX` - PMax campaigns
- `LOCAL` - Local campaigns
- `SMART` - Smart campaigns
- `DEMAND_GEN` - Demand Gen campaigns

## Integration with Snowflake

Cross-reference Google Ads data with RDC Snowflake tables:

| Google Ads Field | Snowflake Field | Table |
|------------------|-----------------|-------|
| `campaign.id` | `campaign_id` | `sem_summary` |
| `campaign.name` | `campaign_name` | `sem_summary` |
| N/A (calculated) | `google_click_id` | `clickstream_detail` |

### Joining Pattern
Query Google Ads for campaign IDs, then use in Snowflake:
```sql
SELECT * FROM rdc_marketing.agg_reporting.sem_summary
WHERE campaign_id IN (12345, 67890)  -- From Google Ads query
  AND event_date >= DATEADD('day', -30, CURRENT_DATE());
```

## Auction Insights

Auction Insights provides competitive intelligence showing how your ads perform against other advertisers in the same auctions. Available for Search and Shopping campaigns only.

### Key Segment
- `segments.auction_insight_domain` - Returns competitor domain names (required for auction insights)

### Auction Insight Metrics
| Metric | Description |
|--------|-------------|
| `metrics.auction_insight_search_impression_share` | % of impressions you received vs. total eligible |
| `metrics.auction_insight_search_overlap_rate` | How often competitor showed alongside you |
| `metrics.auction_insight_search_position_above_rate` | How often competitor ranked above you |
| `metrics.auction_insight_search_top_impression_percentage` | % of impressions at top of page |
| `metrics.auction_insight_search_absolute_top_impression_percentage` | % of impressions in position #1 |
| `metrics.auction_insight_search_outranking_share` | % of auctions where you outranked competitor |

### Campaign-Level Auction Insights
```python
resource: "campaign"
fields: [
    "campaign.id",
    "campaign.name",
    "segments.auction_insight_domain",
    "metrics.auction_insight_search_impression_share",
    "metrics.auction_insight_search_overlap_rate",
    "metrics.auction_insight_search_position_above_rate",
    "metrics.auction_insight_search_top_impression_percentage",
    "metrics.auction_insight_search_absolute_top_impression_percentage",
    "metrics.auction_insight_search_outranking_share"
]
conditions: [
    "campaign.status = 'ENABLED'",
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'"
]
```

### Keyword-Level Auction Insights
```python
resource: "ad_group_criterion"
fields: [
    "campaign.name",
    "ad_group.name",
    "ad_group_criterion.keyword.text",
    "segments.auction_insight_domain",
    "metrics.auction_insight_search_impression_share",
    "metrics.auction_insight_search_overlap_rate",
    "metrics.auction_insight_search_position_above_rate"
]
conditions: [
    "ad_group_criterion.type = 'KEYWORD'",
    "ad_group_criterion.status = 'ENABLED'",
    "segments.date >= 'YYYY-MM-DD'",
    "segments.date <= 'YYYY-MM-DD'"
]
```

### Interpreting Results
- **Treat Analysis as Relative to historical performance**: rather than relying on a hard threshold, develop an understanding of previous behavior vs. current behavior, and interpret the difference. When there is no previous behavior to compare, use the following rules.
- **High overlap rate (>50%)**: Frequent direct competition
- **Position above rate >50%**: Competitor usually beats you
- **Outranking share**: Combines position wins + showing when they didn't
- Results include your own domain as benchmark

**See [references/auction_insights.md](references/auction_insights.md) for comprehensive guidance.**

## Reference Documents

- **[campaign_fields.md](references/campaign_fields.md)** - All campaign resource fields
- **[metrics_fields.md](references/metrics_fields.md)** - All metrics fields with descriptions
- **[segment_fields.md](references/segment_fields.md)** - All segmentation options
- **[keyword_fields.md](references/keyword_fields.md)** - Keyword and criterion fields
- **[auction_insights.md](references/auction_insights.md)** - Competitive analysis and auction insights

## Tips for Efficient Queries

1. **Minimize fields** - Only request fields you need
2. **Use limits** - Add `limit` for exploratory queries
3. **Filter early** - Use conditions to reduce data volume
4. **Segment wisely** - Each segment dimension multiplies rows
5. **Check status** - Filter to ENABLED for active items only
6. **Date ranges** - Shorter ranges = faster queries
7. **Batch accounts** - Query one customer_id at a time
