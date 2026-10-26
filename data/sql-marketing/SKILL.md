---
name: sql-marketing
description: 'SQL for marketing and media data, optimized for BigQuery by default and also Snowflake and PostgreSQL: cohort analysis, LTV, CAC, ROAS, attribution and funnel queries, GA4 BigQuery export, campaign performance, customer journey, window functions and dbt models. Use when the deliverable is a query or a warehouse model. Triggers: SQL, BigQuery, Snowflake, cohort analysis, GA4 BigQuery export, window functions, dbt, attribution query, funnel query.'
---

# sql-marketing

## When to use this skill
Activate when the user asks about: SQL queries for marketing data, BigQuery, Snowflake, PostgreSQL, cohort analysis, LTV, CAC, ROAS in SQL, attribution queries, funnel queries, GA4 BigQuery export, campaign performance SQL, customer journey SQL, window functions for marketing, dbt models, data warehouse marketing patterns.

## Core behavior
- Write optimized SQL for BigQuery by default (unless user specifies otherwise)
- Always partition/filter on date columns to control costs
- Use CTEs for readability — never nested subqueries
- Flag potential JOIN fanout issues (many-to-many joins)
- Include data quality checks (NULL counts, deduplication) in complex queries
- Comment the business logic, not the SQL syntax

## Key patterns

### BigQuery cost-safe query template
```sql
-- Always filter partition column first
WITH base AS (
  SELECT user_pseudo_id, event_name, event_timestamp, traffic_source.source, traffic_source.medium
  FROM `project.analytics_XXXXXX.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '20240101' AND '20240131'
    AND event_name IN ('session_start', 'purchase')
)
```

### Cohort analysis (BigQuery)
```sql
WITH first_purchase AS (
  SELECT user_id, DATE_TRUNC(MIN(purchase_date), MONTH) AS cohort_month
  FROM orders GROUP BY 1
),
activity AS (
  SELECT o.user_id, f.cohort_month,
    DATE_DIFF(DATE_TRUNC(o.purchase_date, MONTH), f.cohort_month, MONTH) AS period
  FROM orders o JOIN first_purchase f USING(user_id)
)
SELECT cohort_month, period, COUNT(DISTINCT user_id) AS users
FROM activity GROUP BY 1,2 ORDER BY 1,2
```

### Attribution: last-touch in SQL
```sql
SELECT session_id, source, medium,
  LAST_VALUE(source) OVER (PARTITION BY user_id ORDER BY timestamp
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_touch_source
FROM sessions
```

### Funnel query
```sql
SELECT
  COUNTIF(step >= 1) AS visits,
  COUNTIF(step >= 2) AS product_views,
  COUNTIF(step >= 3) AS add_to_cart,
  COUNTIF(step = 4) AS purchases,
  ROUND(COUNTIF(step = 4) / COUNTIF(step >= 1) * 100, 2) AS overall_cvr
FROM (
  SELECT user_id, MAX(CASE WHEN event='page_view' THEN 1 END) +
    MAX(CASE WHEN event='view_item' THEN 1 END) +
    MAX(CASE WHEN event='add_to_cart' THEN 1 END) +
    MAX(CASE WHEN event='purchase' THEN 1 END) AS step
  FROM events GROUP BY 1
)
```

## Output formats
- Commented SQL ready to run
- Result interpretation in plain language
- Cost estimate note for BigQuery queries

## Tools
BigQuery (primary), Snowflake, PostgreSQL, dbt, Looker Studio
