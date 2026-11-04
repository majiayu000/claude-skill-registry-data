---
name: store-analytics
description: WooCommerce analytics and reporting. Track sales, analyze customer behavior, identify trends, and generate business insights.
tools_required: [woo_reports, woo_customers, woo_order_track, email]
always_on: false
group: woocommerce
order: 4
suggests: [marketing-strategy]
---

# Store Analytics

Business intelligence and reporting for WooCommerce stores.

## When to Use This Skill

- Generating sales reports
- Analyzing customer behavior
- Tracking revenue trends
- Identifying best-selling products
- Customer segmentation analysis
- Sending performance summaries

## Core Capabilities

### Sales Analytics
- Revenue tracking with `woo_reports`
- Order volume analysis
- Average order value (AOV)
- Conversion rate tracking

### Customer Analytics
- Customer lifetime value (CLV)
- Purchase frequency
- Customer segmentation
- Retention analysis

### Product Analytics
- Best sellers identification
- Slow movers detection
- Category performance
- Product profitability

## Key Metrics

### Revenue Metrics
- **Gross Revenue**: Total sales before deductions
- **Net Revenue**: After refunds and discounts
- **AOV**: Average order value
- **Revenue per Customer**: Lifetime value

### Order Metrics
- **Order Volume**: Total orders
- **Conversion Rate**: Visitors to buyers
- **Cart Abandonment**: Incomplete checkouts
- **Refund Rate**: Returns as % of orders

### Customer Metrics
- **New Customers**: First-time buyers
- **Returning Customers**: Repeat purchasers
- **Customer Retention**: Repeat rate
- **Churn Rate**: Customers lost

## Workflow

### Daily Sales Check

1. **Revenue Summary**
   - Pull daily report with `woo_reports`
   - Compare to previous day/week/year
   - Note significant changes

2. **Order Review**
   - Check new orders
   - Identify high-value orders
   - Note any issues

3. **Quick Alerts**
   - Unusual activity
   - Revenue spikes/drops
   - Customer complaints

### Weekly Analysis

1. **Revenue Trends**
   - Week-over-week comparison
   - Category breakdown
   - Product performance

2. **Customer Insights**
   - New vs. returning with `woo_customers`
   - High-value customer activity
   - At-risk customers

3. **Report Generation**
   - Create summary report
   - Send to stakeholders via `email`
   - Document insights

### Monthly Deep Dive

1. **Comprehensive Report**
   - Full month revenue analysis
   - Customer cohort analysis
   - Product category trends

2. **Trend Analysis**
   - Month-over-month growth
   - Year-over-year comparison
   - Seasonal patterns

3. **Recommendations**
   - Inventory suggestions
   - Marketing opportunities
   - Pricing adjustments

## Report Templates

### Daily Summary
```
📊 Daily Store Report - [Date]

Revenue: $[amount] ([+/-]% vs yesterday)
Orders: [count] ([+/-]% vs yesterday)
AOV: $[amount]
New Customers: [count]

Top Products:
1. [Product] - $[amount]
2. [Product] - $[amount]
3. [Product] - $[amount]
```

### Weekly Summary
```
📈 Weekly Store Report - Week of [Date]

Total Revenue: $[amount] ([+/-]% vs last week)
Total Orders: [count]
Average Daily Revenue: $[amount]
Conversion Rate: [%]

Top Categories:
- [Category]: $[amount] ([%] of total)
- [Category]: $[amount] ([%] of total)

Customer Breakdown:
- New Customers: [count] ([%])
- Returning Customers: [count] ([%])
```

## Customer Segmentation

### RFM Analysis
- **Recency**: When did they last purchase?
- **Frequency**: How often do they buy?
- **Monetary**: How much do they spend?

### Segments
| Segment | Recency | Frequency | Monetary | Action |
|---------|---------|-----------|----------|--------|
| Champions | Recent | Often | High | Reward & retain |
| Loyal | Recent | Often | Medium | Upsell |
| Promising | Recent | Occasional | Low | Nurture |
| At Risk | Old | Often | High | Win back |
| Hibernating | Old | Occasional | Low | Re-engage |

## Best Practices

1. **Set benchmarks** - Know your baseline
2. **Track trends** - Not just snapshots
3. **Segment data** - Don't average everything
4. **Act on insights** - Analysis drives action
5. **Regular cadence** - Daily, weekly, monthly
6. **Share findings** - Keep team informed
