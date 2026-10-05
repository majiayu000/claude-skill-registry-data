---
type: Skill
name: design-analytics-reporting
description: Produces marketing performance reports and data-driven recommendations from WooCommerce sales data, social media metrics, and campaign analytics. Use when the task asks for "campaign performance", "ROI analysis", "monthly report", "sales trends", "product velocity", "audience insights", or "KPI tracking". Covers metric definition, reporting templates, slow-mover detection, and insight-to-action frameworks.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Analytics & Reporting

Use this skill when measuring campaign performance, analyzing sales data, identifying trends, or building marketing reports.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for reporting. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai log` | View execution logs for report data extraction |
| `wp mcp-ai health` | System health check before generating reports |
| `wp ezuite low-stock-report` | ERP low stock report for e-commerce analytics |
| `wp shopify-sync cost-report` | Shopify API cost analysis |

## When to use this skill

Trigger when ANY of the following is true:

- The task asks for "campaign performance", "analytics report", or "ROI analysis".
- Tracking social media engagement, reach, or follower growth.
- Analyzing WooCommerce sales data — top sellers, slow movers, revenue trends.
- Identifying overused or underperforming SKUs for campaign rotation.
- Building a monthly or quarterly marketing performance report.
- Comparing campaign results against targets or benchmarks.
- The task mentions "metrics", "KPIs", "conversion rate", or "performance data".
- Feeding analytics insights back into the monthly campaign planning cycle.

## Data Sources & Available Tools

| Data Source | Tool / Method | What You Get |
|---|---|---|
| **WooCommerce orders** | `remote_wp_connection` → `get_wc_orders` | Revenue, products sold, order count |
| **WooCommerce products** | `remote_wp_connection` → `get_wc_products` | Stock levels, prices, product status |
| **Product catalog** | `Products_Export_Converted.json` | Full product list with historical stock |
| **Social media** | Platform native analytics (Instagram, Facebook, etc.) | Reach, engagement, follower data |
| **Web traffic** | Google Analytics / Search Console | Page views, traffic sources, keywords |
| **Industry benchmarks** | `web_search_validated` | Social media engagement averages, conversion benchmarks |
| Report storage (on request) | `paper_store_write` / `paper_store_read` | Persist reports for historical comparison |
| Media report generation | `generate_media_report` | Generate structured reports on media library composition and usage |
| **Pro toolkit CPTs** | `toolkit_cpt` → `mcp_ai_project`, `mcp_ai_task`, `mcp_ai_event` | Campaign projects, tasks, and event data for cross-reference |

## Core Metrics Framework

### Social Media Metrics

| Metric | Formula | What It Tells You |
|---|---|---|
| **Engagement Rate** | (Likes + Comments + Saves + Shares) ÷ Reach × 100 | Content quality and resonance |
| **Reach** | Unique accounts that saw the post | Audience size and distribution |
| **Impressions** | Total times post was displayed | Visibility (includes repeat views) |
| **Follower Growth** | New followers − Unfollows (per period) | Brand momentum |
| **Click-Through Rate** | Link clicks ÷ Impressions × 100 | CTA effectiveness |
| **Save Rate** | Saves ÷ Reach × 100 | Value — "want to come back to this" |
| **Share Rate** | Shares ÷ Reach × 100 | Virality — "want others to see this" |
| **Video Retention** | % watched to end (for reels/videos) | Content holding power |

### E-Commerce Metrics

| Metric | Formula | What It Tells You |
|---|---|---|
| **Revenue** | Sum of completed order totals | Top-line performance |
| **Average Order Value** | Total Revenue ÷ Number of Orders | Basket size |
| **Conversion Rate** | Orders ÷ Site Visits × 100 | Site effectiveness |
| **Units Sold** | Total quantity sold (per period) | Product velocity |
| **Sell-Through Rate** | Units Sold ÷ (Starting Stock + Units Sold) × 100 | Inventory efficiency |
| **Revenue per Product** | Product Revenue ÷ Quantity Sold | Product-level contribution |
| **Refund Rate** | Refunded Orders ÷ Total Orders × 100 | Customer satisfaction |

### Campaign Performance Metrics

| Metric | Formula | What It Tells You |
|---|---|---|
| **Campaign ROAS** | Campaign Revenue ÷ Campaign Ad Spend | Return on ad investment |
| **Cost per Engagement** | Ad Spend ÷ Total Engagements | Content cost efficiency |
| **Attributed Sales** | Sales directly linked to campaign period | Campaign impact |
| **Email Open Rate** | Unique Opens ÷ Emails Delivered × 100 | Subject line + list health |
| **Email Click Rate** | Unique Clicks ÷ Emails Delivered × 100 | Content relevance |
| **Email Conversion** | Purchases ÷ Emails Delivered × 100 | Revenue per email sent |

## Product Velocity Analysis

Identify what's selling and what's sitting:

### Velocity Score (Weekly)

```
Velocity Score = Units Sold per Week ÷ Average Stock Level

Fast Mover:    ≥ 1.0  (selling faster than restocking)
Healthy:       0.5–1.0  (steady, predictable)
Slow:          0.1–0.5  (moving, but slowly)
Dead:          < 0.1  (barely or not moving)
```

### Slow Mover Identification

Use `remote_wp_connection` to pull product data, then flag:

```
Slow Mover Criteria (any 2 of 3):
  1. Stock > 3 AND no sales in last 30 days
  2. Price above category average AND < 1 unit sold/month
  3. Listed > 60 days AND total sales < 2 units
```

### Overused SKU Detection

```
Overused SKU Warning Signs:
  ● Featured in 3+ campaigns in last 6 months
  ● Appears in > 50% of monthly content calendars
  ● Engagement rate declining over time (audience fatigue)
  ● Stock depleting faster than restock cycle

Action: Rotate out for 2 months minimum.
```

## Reporting Templates

### Monthly Marketing Report

```
═══════════════════════════════════════════════════
           MONTHLY MARKETING REPORT
           [Month Year] — The Parfumerie
═══════════════════════════════════════════════════

1. EXECUTIVE SUMMARY
   Campaign theme: [Theme]
   Total revenue: Rs. XX,XXX (vs target: Rs. XX,XXX)
   Highlights: [2–3 key wins]
   Lowlights: [1–2 areas to improve]

2. SOCIAL MEDIA PERFORMANCE
   ┌──────────┬────────┬──────────┬──────────┬────────┐
   │ Platform │ Posts  │ Reach    │ Engage % │ Growth │
   ├──────────┼────────┼──────────┼──────────┼────────┤
   │ Instagram│ X      │ XX,XXX   │ X.X%     │ +XXX   │
   │ Facebook │ X      │ XX,XXX   │ X.X%     │ +XX    │
   │ TikTok   │ X      │ XX,XXX   │ X.X%     │ +XX    │
   └──────────┴────────┴──────────┴──────────┴────────┘

   Top 3 Posts:
   1. [Post type + topic] — XX,XXX reach, X.X% engagement
   2. [Post type + topic] — XX,XXX reach, X.X% engagement
   3. [Post type + topic] — XX,XXX reach, X.X% engagement

   Bottom 3 Posts (what didn't work):
   1. [Post] — [likely reason]
   2. [Post] — [likely reason]
   3. [Post] — [likely reason]

3. E-COMMERCE PERFORMANCE
   Total orders: XX
   Total revenue: Rs. XX,XXX
   Average order value: Rs. X,XXX
   Top-selling product: [SKU + Name] — X units (Rs. XX,XXX)
   Slowest product: [SKU + Name] — X units (Rs. XX,XXX)

   Sales by category:
   ● Fragrance: Rs. XX,XXX (XX%)
   ● Jewelry:   Rs. XX,XXX (XX%)
   ● Skincare:  Rs. XX,XXX (XX%)

4. CAMPAIGN PERFORMANCE
   Campaign: [Name]
   Products featured: X
   Products sold during campaign: X units
   Revenue attributed: Rs. XX,XXX
   Social engagement during campaign: X.X% (vs monthly avg: X.X%)
   ROI: [Revenue ÷ Cost]

5. PRODUCT VELOCITY SNAPSHOT
   Fast movers (promote more):
   ● [Product] — X units/week (velocity: X.X)

   Slow movers (needs push):
   ● [Product] — X units/month (velocity: X.X)
     Suggested action: [Bundle, discount, feature in campaign]

   Overused (rotate out):
   ● [Product] — Appeared X times in X months. Rest until [Month].

6. AUDIENCE INSIGHTS
   Follower demographics (if available):
   ● Age, gender, location, active hours

   Content preferences:
   ● Best format: [Reel / Static / Story]
   ● Best topic: [Product spotlight / Education / Lifestyle]
   ● Best day/time: [Day + Time with highest engagement]

7. LEARNINGS & NEXT MONTH
   What to keep doing:
   1. [Winning tactic]
   2. [Winning format]

   What to stop doing:
   1. [Failing tactic]
   2. [Underperforming format]

   What to try:
   1. [New experiment]
   2. [New platform or format]

   Next month's theme: [Proposed theme based on data]
   Products to feature: [Based on velocity + rotation rules]
═══════════════════════════════════════════════════
```

### Campaign Post-Mortem (One-Pager)

```
CAMPAIGN: [Name]
Period: [Start Date] – [End Date]

OBJECTIVE:  [What we wanted to achieve]
RESULT:     [What actually happened]

PRODUCTS FEATURED:
  ● [Product 1]: X units sold (before: X/week, during: X/week)
  ● [Product 2]: X units sold (before: X/week, during: X/week)

CONTENT PERFORMANCE:
  ● Reels: X total, avg reach XX,XXX, avg engagement X.X%
  ● Static: X total, avg reach XX,XXX, avg engagement X.X%
  ● Stories: X total, avg reach X,XXX

BUDGET:
  ● Ad spend: Rs. XX,XXX
  ● Revenue attributed: Rs. XX,XXX
  ● ROAS: X.X

WHAT WORKED: [3 bullet points]
WHAT DIDN'T: [2 bullet points]
CHANGES FOR NEXT TIME: [3 bullet points]
```

## Data Collection Workflow

```
WEEKLY (Quick pulse check):
  1. Check top 3 posts by engagement (platform analytics)
  2. Check WooCommerce orders for the week (remote_wp_connection)
  3. Note any anomalies (spike or drop)

MONTHLY (Full report):
  1. Pull all social metrics for the month
  2. Pull WooCommerce orders + product data
  3. Calculate velocity scores for all products
  4. Identify slow movers + overused SKUs
  5. Compare against previous month
  6. Write report (use template above)
  7. Feed insights into next month's campaign plan

QUARTERLY (Strategic review):
  1. Aggregate 3 monthly reports
  2. Trend analysis (is engagement rising or falling?)
  3. Category performance comparison
  4. Audience growth trajectory
  5. Budget efficiency review (ROAS trend)
```

## Using Available Tools for Analytics

### Pulling Sales Data

```
remote_wp_connection {
  connection_id: "conn_8srcad8zylhe"
  action: "get_wc_orders"
  status: "completed"
  per_page: 50
}
→ Returns recent orders with totals, products, dates

remote_wp_connection {
  connection_id: "conn_8srcad8zylhe"
  action: "get_wc_products"
  per_page: 100
}
→ Returns all products with stock levels, prices, status
```

### Researching Benchmarks

```
web_search_validated {
  query: "Instagram engagement rate benchmark Sri Lanka retail 2026"
  max_results: 5
}
→ Compare your rates against industry standards
```

## Setting Targets

### Benchmark Ranges (E-Commerce)

| Metric | Below Average | Average | Good | Excellent |
|---|---|---|---|---|
| **Instagram Engagement** | < 1% | 1–3% | 3–6% | > 6% |
| **Email Open Rate** | < 15% | 15–25% | 25–35% | > 35% |
| **Email Click Rate** | < 1% | 1–3% | 3–5% | > 5% |
| **E-com Conversion Rate** | < 1% | 1–2% | 2–4% | > 4% |
| **Cart Abandonment** | > 80% | 70–80% | 60–70% | < 60% |
| **AOV Growth (MoM)** | Negative | 0–5% | 5–15% | > 15% |

Set realistic targets based on your current baseline, not industry averages alone. An account with 500 followers shouldn't target 3% engagement — aim for steady improvement month over month.

## Insight-to-Action Framework

Analytics are useless without action. Every report should answer: "So what do we do differently?"

```
DATA → INSIGHT → ACTION

"Reels average 3.2% engagement, static posts 1.1%"
  → Reels outperform static by 3×
    → Shift to 2 reels/week, reduce static to 1–2/week

"Slow mover CN29 has 4 units, 0 sales in 60 days"
  → Product isn't moving at current price/positioning
    → Feature in next campaign OR bundle with bestseller OR discount

"Email open rate dropped from 28% to 18% over 3 months"
  → List fatigue or subject lines aren't working
    → Segment dormant subscribers. A/B test new subject line styles.
      Clean list (remove unengaged after 90 days).

"Peak engagement: Friday 6–8 PM, Sunday 10 AM–12 PM"
  → Audience is most active weekend evenings/mornings
    → Schedule reels Friday 6 PM. Post static Sunday 10 AM.
```

## Common Mistakes

```
WRONG:
  ● Reporting vanity metrics with no action ("We got 10K impressions!")
  ● Comparing raw numbers month-to-month without context
    (Jan had a festival sale, Feb didn't — of course Jan was higher)
  ● Tracking everything, understanding nothing (metric overload)
  ● Burying the insight in numbers — "So what should we change?"
  ● Using industry benchmarks as targets instead of your own baseline
  ● Ignoring audience feedback signals (saves, shares, DMs)
  ● Not tracking product-level velocity (miss slow movers until dead stock)

RIGHT:
  ✅ Every metric has a decision attached ("If X < Y, then do Z")
  ✅ Compare like-for-like periods or use per-post averages
  ✅ Track 5–7 core metrics deeply, not 30 metrics shallowly
  ✅ Report ends with 3 clear actions for next month
  ✅ Set targets based on your own trend (+10% MoM), not averages
  ✅ Saves + shares = content value > likes alone
  ✅ Weekly velocity check catches slow movers before they become dead stock
```

## Critical Rules

- **Every metric answers a decision** — don't track anything you won't act on.
- **Compare trends, not snapshots** — one month tells you little. Three months tells a story.
- **Segment by platform and format** — reel performance ≠ static post performance ≠ story performance.
- **Track product velocity weekly** — stock that sits for 60+ days is a problem. Flag it early.
- **Report ends with actions** — every monthly report should produce 3 concrete changes for next month.
- **Use your own baseline** — benchmark against your own historical data first, industry averages second.
- **Clean your data** — exclude outliers (viral post that skews monthly average), note anomalies.
- **Feed insights back into planning** — analytics reports are the input for campaign orchestration and product selection.

## What This Skill Does NOT Cover

- **Creating or scheduling social media posts** — use `schedule_social_post` via **`design-social-publishing`**.
- **Writing social media captions or content** — use **`design-social-content`**.
- **Building campaign plans from analytics insights** — use **`design-campaign-orchestration`**.
- **Generating charts and visual reports** — use the `create_chart_validated` tool directly.
- **Running deep research on market trends** — use `deep_research` via **`design-deep-research`**.
- **Managing CRM data (leads, deals, customers)** — use **`design-crm`**.
- **Direct WooCommerce product management** — use `woo_products` or `remote_wp_connection` tools directly.

## Cross-references

- Run **`design-campaign-orchestration`** to apply analytics insights to next month's campaign plan.
- Run **`design-product-research`** to research underperforming products for better positioning.
- Run **`design-social-content`** to apply format-performance insights to content strategy.
- Run **`design-email-marketing`** to optimize email campaigns based on open/click data.
- Run **`design-seo-content`** to optimize pages based on search performance data.
- Use **`remote_wp_connection`** to pull WooCommerce order and product data.
- Use **`web_search_validated`** to research industry benchmarks and trend data.
- Use **`generate_media_report`** to generate automated reports on media library composition, format distribution, and storage usage.
