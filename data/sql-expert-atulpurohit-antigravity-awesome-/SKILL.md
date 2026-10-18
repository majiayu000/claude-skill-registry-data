---
name: sql-expert
description: "Write complex, optimized SQL queries for analytics, reporting, and data manipulation. Covers window functions, CTEs, subqueries, performance tuning, and database-specific features."
category: data
tags: [sql, postgresql, mysql, queries, optimization, analytics]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# SQL Expert

## Purpose
Write advanced SQL queries for analytics, data manipulation, and reporting with optimal performance.

## Advanced SQL Patterns

### 1️⃣ Window Functions
```sql
-- Running totals and cumulative sums
SELECT
    date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY date) AS cumulative_revenue,
    AVG(daily_revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7day_avg
FROM daily_sales;

-- Ranking users by revenue within each country
SELECT
    user_id,
    country,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY country ORDER BY revenue DESC) AS country_rank,
    RANK()       OVER (PARTITION BY country ORDER BY revenue DESC) AS country_rank_with_ties,
    NTILE(4)     OVER (ORDER BY revenue DESC) AS revenue_quartile
FROM user_revenue;

-- Lead/Lag for day-over-day comparison
SELECT
    date,
    orders,
    LAG(orders, 1) OVER (ORDER BY date) AS prev_day_orders,
    ROUND((orders - LAG(orders, 1) OVER (ORDER BY date))::numeric / 
          LAG(orders, 1) OVER (ORDER BY date) * 100, 2) AS growth_rate_pct
FROM daily_orders;
```

### 2️⃣ CTEs for Complex Analytics
```sql
-- Cohort analysis: retention by signup month
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', created_at) AS cohort_month
    FROM users
),
user_activity AS (
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('month', created_at) AS activity_month
    FROM orders
),
cohort_data AS (
    SELECT
        c.cohort_month,
        a.activity_month,
        COUNT(DISTINCT c.user_id) AS users,
        EXTRACT(EPOCH FROM (a.activity_month - c.cohort_month)) / 2592000 AS months_since_signup
    FROM user_cohorts c
    JOIN user_activity a USING (user_id)
    GROUP BY 1, 2, 4
)
SELECT
    cohort_month,
    months_since_signup,
    users,
    FIRST_VALUE(users) OVER (PARTITION BY cohort_month ORDER BY months_since_signup) AS cohort_size,
    ROUND(users::numeric / FIRST_VALUE(users) OVER (PARTITION BY cohort_month ORDER BY months_since_signup) * 100, 1) AS retention_pct
FROM cohort_data
ORDER BY 1, 2;
```

### 3️⃣ Pivot / Cross-Tab
```sql
-- Pivot: revenue by product per month
SELECT
    product_name,
    SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 1 THEN amount END) AS jan,
    SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 2 THEN amount END) AS feb,
    SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 3 THEN amount END) AS mar,
    SUM(amount) AS total
FROM sales
JOIN products USING (product_id)
WHERE EXTRACT(YEAR FROM sale_date) = 2026
GROUP BY product_name
ORDER BY total DESC;
```

### 4️⃣ Performance Optimization Queries
```sql
-- Find slow queries (PostgreSQL)
SELECT
    query,
    calls,
    ROUND(total_exec_time::numeric / calls, 2) AS avg_ms,
    ROUND(total_exec_time::numeric, 2) AS total_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Find missing indexes
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > 0
  AND seq_tup_read / seq_scan > 1000  -- Tables with large sequential scans
ORDER BY seq_tup_read DESC;

-- Check index usage
SELECT
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- Unused indexes (waste of storage + write overhead)
  AND schemaname = 'public';
```

### 5️⃣ Upsert and Merge Patterns
```sql
-- PostgreSQL upsert
INSERT INTO user_stats (user_id, page_views, last_seen)
VALUES (:user_id, 1, NOW())
ON CONFLICT (user_id) DO UPDATE SET
    page_views = user_stats.page_views + 1,
    last_seen  = EXCLUDED.last_seen;

-- MySQL upsert
INSERT INTO user_stats (user_id, page_views, last_seen)
VALUES (?, 1, NOW())
ON DUPLICATE KEY UPDATE
    page_views = page_views + 1,
    last_seen  = VALUES(last_seen);
```

## Outputs
1. Optimized queries for specific analytics needs
2. Window function examples for time-series analysis
3. Cohort and funnel analysis queries
4. Performance tuning recommendations
5. Index strategy for query patterns
