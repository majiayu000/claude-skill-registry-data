---
name: SQL for Analytics
description: Writing SQL queries for analytics including aggregations, window functions, CTEs, and complex joins to extract insights from large datasets efficiently.
---

# SQL for Analytics

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Data Engineering

---

## Overview

Analytics SQL focuses on aggregations, analysis, and insights rather than transactional operations. Effective analytics SQL uses window functions, CTEs, complex joins, and optimization techniques to query large datasets efficiently.

## Analytics SQL vs Transactional SQL

| Aspect | Transactional SQL | Analytics SQL |
|--------|-------------------|----------------|
| **Purpose** | CRUD operations | Aggregations, analysis |
| **Focus** | Single record | Many records |
| **Operations** | INSERT, UPDATE, DELETE | SELECT, GROUP BY, JOIN |
| **Performance** | Fast queries | Complex queries |
| **Example** | `UPDATE users SET status = 'active'` | `SELECT COUNT(*) FROM users GROUP BY status` |

## Core Analytics Queries

### Aggregations

```sql
-- Basic aggregations
SELECT
    COUNT(*) AS total_orders,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_revenue,
    MIN(revenue) AS min_revenue,
    MAX(revenue) AS max_revenue
FROM orders;

-- Conditional aggregations
SELECT
    COUNT(*) AS total_orders,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed_orders,
    SUM(CASE WHEN status = 'completed' THEN revenue END) AS completed_revenue
FROM orders;
```

### GROUP BY

```sql
-- Group by single dimension
SELECT
    country,
    COUNT(*) AS orders,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY country
ORDER BY total_revenue DESC;

-- Group by multiple dimensions
SELECT
    country,
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS orders,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY country, DATE_TRUNC('month', order_date)
ORDER BY country, month;
```

### HAVING

```sql
-- Filter aggregated results
SELECT
    country,
    COUNT(*) AS orders,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY country
HAVING SUM(revenue) > 100000
ORDER BY total_revenue DESC;
```

### DISTINCT

```sql
-- Count unique values
SELECT
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT country) AS unique_countries
FROM orders;

-- Distinct combinations
SELECT DISTINCT
    user_id,
    country
FROM orders
ORDER BY user_id, country;
```

## Window Functions

### ROW_NUMBER()

```sql
-- Rank rows within groups
SELECT
    user_id,
    order_date,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) AS order_rank
FROM orders;
```

### RANK() and DENSE_RANK()

```sql
-- Rank with ties
SELECT
    product_id,
    revenue,
    RANK() OVER (ORDER BY revenue DESC) AS rank_rank,
    DENSE_RANK() OVER (ORDER BY revenue DESC) AS dense_rank
FROM products;
```

| Revenue | RANK() | DENSE_RANK() |
|----------|---------|--------------|
| 100 | 1 | 1 |
| 100 | 1 | 1 |
| 90 | 3 | 2 |
| 80 | 4 | 3 |

### LAG() and LEAD()

```sql
-- Compare with previous/next row
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS monthly_revenue,
    LAG(SUM(revenue), 1) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS prev_month_revenue,
    SUM(revenue) - LAG(SUM(revenue), 1) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS revenue_change
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### Running Totals

```sql
-- Cumulative sum
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS monthly_revenue,
    SUM(SUM(revenue)) OVER (
        ORDER BY DATE_TRUNC('month', order_date)
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### Moving Averages

```sql
-- 7-day moving average
SELECT
    order_date,
    SUM(revenue) AS daily_revenue,
    AVG(SUM(revenue)) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7day
FROM orders
GROUP BY order_date
ORDER BY order_date;
```

## Date/Time Analysis

### DATE_TRUNC

```sql
-- Group by time periods
SELECT
    DATE_TRUNC('day', order_date) AS day,
    SUM(revenue) AS daily_revenue
FROM orders
GROUP BY DATE_TRUNC('day', order_date)
ORDER BY day;

SELECT
    DATE_TRUNC('week', order_date) AS week,
    SUM(revenue) AS weekly_revenue
FROM orders
GROUP BY DATE_TRUNC('week', order_date)
ORDER BY week;

SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS monthly_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

SELECT
    DATE_TRUNC('quarter', order_date) AS quarter,
    SUM(revenue) AS quarterly_revenue
FROM orders
GROUP BY DATE_TRUNC('quarter', order_date)
ORDER BY quarter;

SELECT
    DATE_TRUNC('year', order_date) AS year,
    SUM(revenue) AS yearly_revenue
FROM orders
GROUP BY DATE_TRUNC('year', order_date)
ORDER BY year;
```

### EXTRACT

```sql
-- Extract date parts
SELECT
    order_date,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    EXTRACT(DAY FROM order_date) AS day,
    EXTRACT(HOUR FROM order_date) AS hour,
    EXTRACT(DOW FROM order_date) AS day_of_week
FROM orders;
```

### Date Arithmetic

```sql
-- Date differences
SELECT
    user_id,
    signup_date,
    first_purchase_date,
    EXTRACT(DAY FROM (first_purchase_date - signup_date)) AS days_to_purchase
FROM users
WHERE first_purchase_date IS NOT NULL;

-- Date addition
SELECT
    order_date,
    order_date + INTERVAL '30 days' AS due_date,
    order_date + INTERVAL '1 month' AS next_month,
    order_date + INTERVAL '1 year' AS next_year
FROM orders;
```

## Common Analytics Patterns

### Daily Active Users (DAU)

```sql
SELECT
    event_date,
    COUNT(DISTINCT user_id) AS dau
FROM events
WHERE event_type = 'page_view'
GROUP BY event_date
ORDER BY event_date;
```

### Monthly Recurring Revenue (MRR)

```sql
SELECT
    DATE_TRUNC('month', start_date) AS month,
    SUM(amount) AS mrr
FROM subscriptions
WHERE status = 'active'
    AND billing_period = 'monthly'
GROUP BY DATE_TRUNC('month', start_date)
ORDER BY month;
```

### Cohort Retention

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),

user_activities AS (
    SELECT
        user_id,
        DATE_TRUNC('month', event_date) AS activity_month
    FROM events
    WHERE event_type = 'page_view'
)

SELECT
    c.cohort_month,
    ua.activity_month,
    COUNT(DISTINCT ua.user_id) AS retained_users,
    COUNT(DISTINCT c.user_id) AS cohort_size,
    100.0 * COUNT(DISTINCT ua.user_id) / COUNT(DISTINCT c.user_id) AS retention_pct
FROM cohorts c
LEFT JOIN user_activities ua ON c.user_id = ua.user_id
GROUP BY c.cohort_month, ua.activity_month
ORDER BY c.cohort_month, ua.activity_month;
```

### Conversion Funnel

```sql
WITH funnel_steps AS (
    SELECT
        session_id,
        'visit' AS step,
        1 AS step_number
    FROM page_views
    WHERE page_url = '/'

    UNION ALL

    SELECT
        session_id,
        'product_view' AS step,
        2 AS step_number
    FROM page_views
    WHERE page_url LIKE '/product/%'

    UNION ALL

    SELECT
        session_id,
        'add_to_cart' AS step,
        3 AS step_number
    FROM events
    WHERE event_type = 'add_to_cart'

    UNION ALL

    SELECT
        session_id,
        'purchase' AS step,
        4 AS step_number
    FROM events
    WHERE event_type = 'purchase'
)

SELECT
    step,
    step_number,
    COUNT(DISTINCT session_id) AS users,
    LAG(COUNT(DISTINCT session_id)) OVER (ORDER BY step_number) AS previous_users,
    ROUND(100.0 * COUNT(DISTINCT session_id) / LAG(COUNT(DISTINCT session_id)) OVER (ORDER BY step_number), 2) AS conversion_rate
FROM funnel_steps
GROUP BY step, step_number
ORDER BY step_number;
```

### Customer LTV

```sql
WITH user_revenue AS (
    SELECT
        user_id,
        SUM(revenue) AS total_revenue,
        COUNT(*) AS order_count,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order
    FROM orders
    GROUP BY user_id
)

SELECT
    AVG(total_revenue) AS avg_ltv,
    AVG(order_count) AS avg_orders,
    AVG(EXTRACT(DAY FROM (last_order - first_order))) AS avg_lifetime_days
FROM user_revenue;
```

### Year-Over-Year Growth

```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        EXTRACT(YEAR FROM order_date) AS year,
        EXTRACT(MONTH FROM order_date) AS month_num,
        SUM(revenue) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)

SELECT
    year,
    month_num,
    revenue,
    LAG(revenue, 12) OVER (ORDER BY year, month_num) AS revenue_prev_year,
    ROUND(100.0 * (revenue - LAG(revenue, 12) OVER (ORDER BY year, month_num)) /
          LAG(revenue, 12) OVER (ORDER BY year, month_num), 2) AS yoy_growth
FROM monthly_revenue
ORDER BY year, month_num;
```

## CTEs (Common Table Expressions)

### Basic CTE

```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)

SELECT
    month,
    revenue,
    AVG(revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS ma_3month
FROM monthly_revenue
ORDER BY month;
```

### Multiple CTEs

```sql
WITH user_orders AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(revenue) AS total_revenue
    FROM orders
    GROUP BY user_id
),

user_segments AS (
    SELECT
        user_id,
        order_count,
        total_revenue,
        CASE
            WHEN total_revenue > 1000 THEN 'high_value'
            WHEN total_revenue > 500 THEN 'medium_value'
            ELSE 'low_value'
        END AS segment
    FROM user_orders
)

SELECT
    segment,
    COUNT(*) AS user_count,
    AVG(order_count) AS avg_orders,
    AVG(total_revenue) AS avg_revenue
FROM user_segments
GROUP BY segment
ORDER BY avg_revenue DESC;
```

## JOINs for Analytics

### LEFT JOIN (Keep all from left)

```sql
-- All users, with orders if they have any
SELECT
    u.user_id,
    u.signup_date,
    COUNT(o.order_id) AS order_count,
    SUM(o.revenue) AS total_revenue
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.signup_date;
```

### INNER JOIN (Only matches)

```sql
-- Only users who have made orders
SELECT
    u.user_id,
    u.signup_date,
    COUNT(o.order_id) AS order_count,
    SUM(o.revenue) AS total_revenue
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.signup_date;
```

### SELF JOIN (Compare rows in same table)

```sql
-- Find users who made multiple orders in same day
SELECT
    o1.user_id,
    o1.order_date,
    COUNT(*) AS orders_same_day
FROM orders o1
INNER JOIN orders o2 ON o1.user_id = o2.user_id
    AND DATE(o1.order_date) = DATE(o2.order_date)
GROUP BY o1.user_id, o1.order_date
HAVING COUNT(*) > 1;
```

### Multiple JOINs

```sql
-- Join users, orders, and products
SELECT
    u.user_id,
    u.country,
    COUNT(o.order_id) AS order_count,
    SUM(o.revenue) AS total_revenue,
    AVG(p.price) AS avg_product_price
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN products p ON o.product_id = p.product_id
GROUP BY u.user_id, u.country
ORDER BY total_revenue DESC;
```

## CASE Statements

### Conditional Logic

```sql
-- Bucketing
SELECT
    user_id,
    revenue,
    CASE
        WHEN revenue < 50 THEN 'low'
        WHEN revenue < 100 THEN 'medium'
        WHEN revenue < 200 THEN 'high'
        ELSE 'very_high'
    END AS revenue_tier
FROM orders;
```

### Pivot-like Transformation

```sql
-- Pivot months to columns
SELECT
    product_id,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 1 THEN revenue END) AS jan_revenue,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 2 THEN revenue END) AS feb_revenue,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 3 THEN revenue END) AS mar_revenue,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 4 THEN revenue END) AS apr_revenue
FROM orders
GROUP BY product_id;
```

## Subqueries

### Scalar Subquery

```sql
-- Single value
SELECT
    user_id,
    revenue,
    (SELECT AVG(revenue) FROM orders) AS avg_revenue,
    revenue - (SELECT AVG(revenue) FROM orders) AS revenue_diff
FROM orders;
```

### Correlated Subquery

```sql
-- Subquery references outer query
SELECT
    user_id,
    order_date,
    revenue,
    (SELECT AVG(revenue)
     FROM orders o2
     WHERE o2.user_id = o1.user_id
    ) AS user_avg_revenue
FROM orders o1;
```

### Subquery in FROM

```sql
-- Use subquery as table
SELECT
    month,
    revenue,
    ma_3month
FROM (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue) AS revenue,
        AVG(SUM(revenue)) OVER (
            ORDER BY DATE_TRUNC('month', order_date)
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS ma_3month
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
) monthly_revenue
ORDER BY month;
```

## Performance Optimization

### EXPLAIN

```sql
-- Analyze query plan
EXPLAIN ANALYZE
SELECT
    user_id,
    COUNT(*) AS order_count,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY user_id;
```

### Indexes

```sql
-- Create index on filter column
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Create index on join column
CREATE INDEX idx_orders_product_id ON orders(product_id);

-- Create composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Create index on date for range queries
CREATE INDEX idx_orders_date ON orders(order_date);
```

### Avoid SELECT *

```sql
-- Bad: Select all columns
SELECT * FROM orders;

-- Good: Select only needed columns
SELECT order_id, user_id, revenue, order_date
FROM orders;
```

### Filter Early

```sql
-- Bad: Filter after JOIN
SELECT
    u.user_id,
    COUNT(o.order_id) AS order_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date >= '2024-01-01'
GROUP BY u.user_id;

-- Good: Filter before JOIN
SELECT
    u.user_id,
    COUNT(o.order_id) AS order_count
FROM users u
LEFT JOIN (
    SELECT order_id, user_id
    FROM orders
    WHERE order_date >= '2024-01-01'
) o ON u.user_id = o.user_id
GROUP BY u.user_id;
```

## Advanced Aggregations

### PERCENTILE_CONT()

```sql
-- Median and quartiles
SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue) AS median_revenue,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY revenue) AS q25_revenue,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY revenue) AS q75_revenue
FROM orders;
```

### STRING_AGG() / ARRAY_AGG()

```sql
-- Concatenate values
SELECT
    user_id,
    STRING_AGG(product_name, ', ') AS products_purchased
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY user_id;

-- Aggregate to array
SELECT
    user_id,
    ARRAY_AGG(product_id) AS product_ids
FROM orders
GROUP BY user_id;
```

### FILTER Clause (PostgreSQL)

```sql
-- Conditional aggregation
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed_orders,
    COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled_orders,
    SUM(revenue) FILTER (WHERE status = 'completed') AS completed_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### ROLLUP / CUBE

```sql
-- Subtotals with ROLLUP
SELECT
    country,
    city,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY ROLLUP(country, city)
ORDER BY country, city;

-- All combinations with CUBE
SELECT
    country,
    city,
    product_category,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY CUBE(country, city, product_category)
ORDER BY country, city, product_category;
```

## Database-Specific Features

### PostgreSQL

```sql
-- JSON functions
SELECT
    user_id,
    metadata->>'country' AS country,
    metadata->>'preferences'->>'theme' AS theme
FROM users;

-- LATERAL joins
SELECT
    u.user_id,
    o.order_id,
    o.revenue
FROM users u
CROSS JOIN LATERAL (
    SELECT order_id, revenue
    FROM orders
    WHERE user_id = u.user_id
    ORDER BY order_date DESC
    LIMIT 3
) o;
```

### MySQL

```sql
-- JSON functions
SELECT
    user_id,
    JSON_EXTRACT(metadata, '$.country') AS country
FROM users;

-- GROUP_CONCAT
SELECT
    user_id,
    GROUP_CONCAT(product_name ORDER BY product_name SEPARATOR ', ') AS products
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY user_id;
```

### BigQuery

```sql
-- ARRAY and STRUCT
SELECT
    user_id,
    ARRAY(
        SELECT AS STRUCT order_id, revenue
        FROM orders
        WHERE user_id = u.user_id
        LIMIT 3
    ) AS recent_orders
FROM users u;

-- UNNEST
SELECT
    user_id,
    order.order_id,
    order.revenue
FROM users u,
UNNEST(u.recent_orders) AS order
```

### Snowflake

```sql
-- QUALIFY clause (filter window functions)
SELECT
    user_id,
    order_date,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) AS order_rank
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) <= 3;
```

## Testing Queries

### Test with Sample Data

```sql
-- Use LIMIT to test
SELECT
    user_id,
    COUNT(*) AS order_count,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY user_id
LIMIT 10;
```

### Validate Aggregations

```sql
-- Spot check calculations
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_revenue
FROM orders;
```

### Check for NULLs

```sql
-- Find NULL values
SELECT
    COUNT(*) AS total,
    COUNT(user_id) AS non_null_user_id,
    COUNT(order_date) AS non_null_order_date,
    COUNT(revenue) AS non_null_revenue
FROM orders;
```

### Verify Date Ranges

```sql
-- Check date range
SELECT
    MIN(order_date) AS min_date,
    MAX(order_date) AS max_date,
    COUNT(*) AS total_records
FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';
```

## Query Organization

### Formatting

```sql
-- Consistent indentation and capitalization
SELECT
    u.user_id,
    u.signup_date,
    COUNT(o.order_id) AS order_count,
    SUM(o.revenue) AS total_revenue
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
WHERE u.signup_date >= '2024-01-01'
GROUP BY u.user_id, u.signup_date
ORDER BY total_revenue DESC;
```

### Comments

```sql
-- Calculate monthly revenue by user
WITH monthly_user_revenue AS (
    SELECT
        user_id,
        DATE_TRUNC('month', order_date) AS month,
        SUM(revenue) AS monthly_revenue
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY user_id, DATE_TRUNC('month', order_date)
)

-- Calculate average monthly revenue per user
SELECT
    user_id,
    AVG(monthly_revenue) AS avg_monthly_revenue
FROM monthly_user_revenue
GROUP BY user_id
ORDER BY avg_monthly_revenue DESC;
```

### Naming

```sql
-- Descriptive CTE names
WITH user_orders AS (
    -- User order summary
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(revenue) AS total_revenue
    FROM orders
    GROUP BY user_id
),

high_value_users AS (
    -- Users with revenue > $1000
    SELECT
        user_id,
        total_revenue
    FROM user_orders
    WHERE total_revenue > 1000
)

SELECT
    h.user_id,
    h.total_revenue,
    u.country
FROM high_value_users h
JOIN users u ON h.user_id = u.user_id;
```

## Real SQL Examples

### Monthly Active Users (MAU)

```sql
SELECT
    DATE_TRUNC('month', event_date) AS month,
    COUNT(DISTINCT user_id) AS mau
FROM events
WHERE event_type = 'page_view'
GROUP BY DATE_TRUNC('month', event_date)
ORDER BY month;
```

### Cohort Retention

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),

user_activities AS (
    SELECT
        user_id,
        DATE_TRUNC('month', event_date) AS activity_month
    FROM events
    WHERE event_type = 'page_view'
)

SELECT
    c.cohort_month,
    ua.activity_month,
    COUNT(DISTINCT ua.user_id) AS retained_users,
    COUNT(DISTINCT c.user_id) AS cohort_size,
    100.0 * COUNT(DISTINCT ua.user_id) / COUNT(DISTINCT c.user_id) AS retention_pct
FROM cohorts c
LEFT JOIN user_activities ua ON c.user_id = ua.user_id
GROUP BY c.cohort_month, ua.activity_month
ORDER BY c.cohort_month, ua.activity_month;
```

### Revenue by Product Category

```sql
SELECT
    p.category,
    COUNT(o.order_id) AS order_count,
    SUM(o.revenue) AS total_revenue,
    AVG(o.revenue) AS avg_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

### Conversion Funnel

```sql
WITH funnel_steps AS (
    SELECT
        session_id,
        'visit' AS step,
        1 AS step_number
    FROM page_views
    WHERE page_url = '/'

    UNION ALL

    SELECT
        session_id,
        'product_view' AS step,
        2 AS step_number
    FROM page_views
    WHERE page_url LIKE '/product/%'

    UNION ALL

    SELECT
        session_id,
        'add_to_cart' AS step,
        3 AS step_number
    FROM events
    WHERE event_type = 'add_to_cart'

    UNION ALL

    SELECT
        session_id,
        'purchase' AS step,
        4 AS step_number
    FROM events
    WHERE event_type = 'purchase'
)

SELECT
    step,
    step_number,
    COUNT(DISTINCT session_id) AS users,
    LAG(COUNT(DISTINCT session_id)) OVER (ORDER BY step_number) AS previous_users,
    ROUND(100.0 * COUNT(DISTINCT session_id) / LAG(COUNT(DISTINCT session_id)) OVER (ORDER BY step_number), 2) AS conversion_rate
FROM funnel_steps
GROUP BY step, step_number
ORDER BY step_number;
```

### Running Total

```sql
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(revenue) AS monthly_revenue,
    SUM(SUM(revenue)) OVER (
        ORDER BY DATE_TRUNC('month', order_date)
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### Year-Over-Year Growth

```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        EXTRACT(YEAR FROM order_date) AS year,
        EXTRACT(MONTH FROM order_date) AS month_num,
        SUM(revenue) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)

SELECT
    year,
    month_num,
    revenue,
    LAG(revenue, 12) OVER (ORDER BY year, month_num) AS revenue_prev_year,
    ROUND(100.0 * (revenue - LAG(revenue, 12) OVER (ORDER BY year, month_num)) /
          LAG(revenue, 12) OVER (ORDER BY year, month_num), 2) AS yoy_growth
FROM monthly_revenue
ORDER BY year, month_num;
```

## Common Mistakes

### Cartesian Product (Missing JOIN condition)

```sql
-- Bad: No JOIN condition
SELECT
    u.user_id,
    o.order_id
FROM users u
CROSS JOIN orders o;

-- Good: Proper JOIN
SELECT
    u.user_id,
    o.order_id
FROM users u
JOIN orders o ON u.user_id = o.user_id;
```

### NULL Handling

```sql
-- Bad: NULL in arithmetic
SELECT
    revenue - discount AS net_revenue
FROM orders;

-- Good: Handle NULL
SELECT
    revenue - COALESCE(discount, 0) AS net_revenue
FROM orders;
```

### GROUP BY Without Aggregation

```sql
-- Bad: Column not in GROUP BY
SELECT
    user_id,
    order_date,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY user_id;

-- Good: All non-aggregated columns in GROUP BY
SELECT
    user_id,
    SUM(revenue) AS total_revenue
FROM orders
GROUP BY user_id;
```

### Division by Zero

```sql
-- Bad: Division by zero error
SELECT
    revenue / discount_rate AS discounted_revenue
FROM orders;

-- Good: Handle division by zero
SELECT
    revenue / NULLIF(discount_rate, 0) AS discounted_revenue
FROM orders;
```

---

## Quick Start

### Common Analytics Queries

```sql
-- Daily active users
SELECT 
  DATE(created_at) as date,
  COUNT(DISTINCT user_id) as dau
FROM events
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Revenue by product
SELECT 
  p.name,
  SUM(oi.quantity * oi.price) as revenue,
  COUNT(DISTINCT o.order_id) as orders
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.name
ORDER BY revenue DESC;

-- Cohort retention
WITH first_purchase AS (
  SELECT 
    user_id,
    MIN(created_at) as first_purchase_date
  FROM orders
  GROUP BY user_id
)
SELECT 
  DATE_TRUNC('month', fp.first_purchase_date) as cohort_month,
  COUNT(DISTINCT fp.user_id) as cohort_size,
  COUNT(DISTINCT o.user_id) as active_users
FROM first_purchase fp
LEFT JOIN orders o ON fp.user_id = o.user_id
  AND DATE_TRUNC('month', o.created_at) = DATE_TRUNC('month', fp.first_purchase_date) + INTERVAL '1 month'
GROUP BY DATE_TRUNC('month', fp.first_purchase_date);
```

---

## Production Checklist

- [ ] **Query Optimization**: Optimize queries for performance
- [ ] **Indexes**: Appropriate indexes for analytics queries
- [ ] **Window Functions**: Use window functions for rankings
- [ ] **CTEs**: Use CTEs for complex queries
- [ ] **NULL Handling**: Handle NULL values properly
- [ ] **Data Quality**: Validate data quality
- [ ] **Documentation**: Document query purpose and logic
- [ ] **Testing**: Test queries with sample data
- [ ] **Performance**: Monitor query performance
- [ ] **Caching**: Cache expensive queries
- [ ] **Version Control**: Version control SQL queries
- [ ] **Review**: Code review for SQL queries

---

## Anti-patterns

### ❌ Don't: SELECT *

```sql
-- ❌ Bad - Select all columns
SELECT * FROM users WHERE status = 'active'
```

```sql
-- ✅ Good - Select only needed columns
SELECT user_id, email, created_at 
FROM users 
WHERE status = 'active'
```

### ❌ Don't: No Indexes

```sql
-- ❌ Bad - Full table scan
SELECT * FROM orders WHERE created_at > '2024-01-01'
-- No index on created_at!
```

```sql
-- ✅ Good - With index
CREATE INDEX idx_orders_created_at ON orders(created_at);
SELECT * FROM orders WHERE created_at > '2024-01-01'
```

### ❌ Don't: Ignore NULLs

```sql
-- ❌ Bad - NULL handling
SELECT AVG(price) FROM products
-- NULLs included in count but not in sum!
```

```sql
-- ✅ Good - Handle NULLs
SELECT AVG(COALESCE(price, 0)) FROM products
-- Or
SELECT AVG(price) FROM products WHERE price IS NOT NULL
```

---

## Integration Points

- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Query results visualization
- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Metric queries
- **Database Optimization** (`04-database/database-optimization/`) - Query optimization

---

## Further Reading

- [SQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [SQL Performance Tuning](https://use-the-index-luke.com/)
- [Analytics SQL Patterns](https://www.mode.com/sql-tutorial/)

### Performance

- [ ] Use EXPLAIN to analyze
- [ ] Create indexes on filter/join columns
- [ ] Avoid SELECT *
- [ ] Filter early
- [ ] Use appropriate JOIN types

### Validation

- [ ] Spot check calculations
- [ ] Verify date ranges
- [ ] Check for NULLs
- [ ] Test edge cases
- [ ] Document queries
