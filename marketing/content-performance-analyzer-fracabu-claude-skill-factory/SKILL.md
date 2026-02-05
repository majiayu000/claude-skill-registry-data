---
name: content-performance-analyzer
description: Analyzes content marketing metrics to identify top performers, trends, and optimization opportunities. Use when reviewing blog posts, social media, or campaign performance. Accepts CSV data with engagement metrics and provides actionable insights.
---

# Content Performance Analyzer

Transform raw content metrics into actionable insights for improving your content marketing strategy.

## Capabilities

- Analyze engagement metrics (views, clicks, shares, comments)
- Identify top-performing content patterns
- Calculate performance benchmarks
- Detect content trends over time
- Generate optimization recommendations
- Compare performance across channels/formats

## Supported Metrics

| Metric | Description | Benchmark Calculation |
|--------|-------------|----------------------|
| Views/Impressions | Total reach | Average, growth rate |
| Engagement Rate | (Likes+Comments+Shares)/Reach | Industry comparison |
| Click-Through Rate | Clicks/Impressions | % benchmark |
| Time on Page | Average reading time | Content length correlation |
| Bounce Rate | Single-page sessions | Quality indicator |
| Conversion Rate | Desired actions/Total visitors | Goal tracking |

## Instructions

1. **Import Data**: Accept CSV or structured data with content metrics
2. **Validate Fields**: Ensure required metrics are present
3. **Calculate KPIs**: Compute averages, rates, and benchmarks
4. **Identify Patterns**: Find top performers and common traits
5. **Trend Analysis**: Detect performance changes over time
6. **Generate Recommendations**: Provide actionable next steps

## Input Format

CSV with these columns (minimum):
```csv
content_id,title,publish_date,content_type,views,engagement,clicks
```

Optional enhanced columns:
```csv
channel,category,word_count,time_on_page,conversions,shares,comments
```

## Output Format

```markdown
# Content Performance Report

## Executive Summary
- Total content pieces analyzed: X
- Date range: [start] to [end]
- Overall engagement rate: X%

## Top Performers
| Rank | Title | Views | Engagement Rate | Key Success Factor |
|------|-------|-------|-----------------|-------------------|
| 1 | ... | ... | ... | ... |

## Performance by Category
[Chart/Table of metrics by content type]

## Trends Identified
1. [Trend 1 with data support]
2. [Trend 2 with data support]

## Recommendations
1. **Quick Win**: [Immediate action]
2. **Strategic**: [Medium-term improvement]
3. **Experiment**: [Test suggestion]

## Detailed Metrics
[Full breakdown tables]
```

## Example Usage

**Input**: CSV file with 30 days of blog post metrics

**Analysis Request**:
```
Analyze this content performance data and identify:
1. Top 5 performing posts by engagement rate
2. Best performing content categories
3. Optimal publish day/time patterns
4. Content length vs performance correlation
5. Recommendations for next month's content calendar
```

## Analysis Types

### 1. Performance Ranking
- Sort by chosen metric
- Calculate percentile rankings
- Identify outliers (over/under performers)

### 2. Comparative Analysis
- Content type comparison
- Time period comparison
- Channel/platform comparison

### 3. Correlation Analysis
- Length vs engagement
- Publish time vs views
- Topic vs conversion

### 4. Trend Detection
- Week-over-week changes
- Seasonal patterns
- Growth/decline indicators

## Best Practices

1. **Minimum Data**: Need 10+ content pieces for meaningful analysis
2. **Time Range**: 30+ days provides better trend visibility
3. **Consistent Metrics**: Ensure same measurement methods
4. **Segment Analysis**: Break down by type for deeper insights
5. **Action Focus**: Every insight should lead to an action

## Benchmarks Reference

| Content Type | Good Engagement | Great Engagement |
|--------------|-----------------|------------------|
| Blog Post | 2-3% | >5% |
| Social Media | 1-3% | >5% |
| Video | 3-5% | >8% |
| Newsletter | 15-25% open | >30% open |

## Limitations

- Requires structured data input
- Cannot access external analytics platforms directly
- Benchmarks are industry averages; your baseline may differ
- Correlation ≠ causation in trend analysis
- Historical data quality affects insight accuracy
