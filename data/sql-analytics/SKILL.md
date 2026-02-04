---
name: sql-analytics
description: Master analytical SQL including window functions, CTEs, aggregations, and query optimization for BI workloads
sasmp_version: "1.3.0"
bonded_agent: 03-sql-analytics
bond_type: PRIMARY_BOND
parameters:
  query_type:
    type: string
    required: true
    enum: [aggregation, window_function, cte, time_series, cohort, funnel]
  database:
    type: string
    enum: [postgresql, mysql, sqlserver, bigquery, snowflake, redshift]
    default: postgresql
  optimization_level:
    type: string
    enum: [basic, intermediate, advanced]
    default: intermediate
retry_config:
  max_retries: 3
  backoff_ms: [1000, 2000, 4000]
---

# SQL Analytics Skill

Master analytical SQL patterns for business intelligence, including window functions, CTEs, cohort analysis, and performance optimization.

## Quick Start (5 minutes)

```sql
-- The 3 essential patterns for BI analysts:

-- 1. Aggregation with GROUP BY
SELECT region, SUM(sales) as total_sales
FROM orders GROUP BY region;

-- 2. Window function for running total
SELECT date, sales,
       SUM(sales) OVER (ORDER BY date) as running_total
FROM daily_sales;

-- 3. CTE for readable complex queries
WITH monthly AS (
    SELECT DATE_TRUNC('month', date) as month, SUM(sales) as sales
    FROM orders GROUP BY 1
)
SELECT * FROM monthly ORDER BY month;
```

## Core Concepts

### Query Building Blocks

```
SELECT      → What columns to return
FROM        → Source table(s)
JOIN        → Combine tables
WHERE       → Filter rows (before aggregation)
GROUP BY    → Aggregate grouping
HAVING      → Filter groups (after aggregation)
WINDOW      → Analytical functions
ORDER BY    → Sort results
LIMIT       → Restrict row count
```

### Aggregation Functions

```sql
-- Basic Aggregates
COUNT(*)           -- Count all rows
COUNT(DISTINCT x)  -- Count unique values
SUM(x)             -- Total
AVG(x)             -- Average
MIN(x) / MAX(x)    -- Extremes
STDDEV(x)          -- Standard deviation

-- Conditional Aggregates
COUNT(*) FILTER (WHERE condition)           -- PostgreSQL
SUM(CASE WHEN condition THEN 1 ELSE 0 END)  -- Universal
```

### Window Functions Reference

```sql
-- Ranking
ROW_NUMBER() OVER (...)  -- Unique sequential
RANK() OVER (...)        -- Gaps on ties
DENSE_RANK() OVER (...)  -- No gaps on ties
NTILE(n) OVER (...)      -- Divide into n buckets

-- Offset
LAG(col, n) OVER (...)   -- Previous row value
LEAD(col, n) OVER (...)  -- Next row value
FIRST_VALUE(col) OVER (...) -- First in partition
LAST_VALUE(col) OVER (...)  -- Last in partition

-- Aggregate
SUM(col) OVER (...)      -- Running/cumulative sum
AVG(col) OVER (...)      -- Moving average
COUNT(col) OVER (...)    -- Running count

-- Frame Specification
ROWS BETWEEN n PRECEDING AND CURRENT ROW
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
```

## Code Examples

### Year-over-Year Comparison
```sql
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS revenue
    FROM orders
    WHERE order_date >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '2 years'
    GROUP BY 1
)
SELECT
    month,
    revenue AS current_revenue,
    LAG(revenue, 12) OVER (ORDER BY month) AS prior_year_revenue,
    revenue - LAG(revenue, 12) OVER (ORDER BY month) AS yoy_change,
    ROUND(
        (revenue - LAG(revenue, 12) OVER (ORDER BY month))
        / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0) * 100,
        2
    ) AS yoy_growth_pct
FROM monthly_sales
WHERE EXTRACT(YEAR FROM month) = EXTRACT(YEAR FROM CURRENT_DATE)
ORDER BY month;
```

### Cohort Retention Analysis
```sql
WITH customer_cohorts AS (
    -- Assign each customer to their first purchase month
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
),
customer_activity AS (
    -- Track activity relative to cohort
    SELECT
        c.customer_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS activity_month,
        DATE_PART('month', AGE(
            DATE_TRUNC('month', o.order_date),
            c.cohort_month
        )) AS period_number
    FROM customer_cohorts c
    JOIN orders o ON c.customer_id = o.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM customer_cohorts
    GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    ca.period_number,
    COUNT(DISTINCT ca.customer_id) AS active_customers,
    cs.cohort_customers,
    ROUND(
        COUNT(DISTINCT ca.customer_id)::DECIMAL / cs.cohort_customers * 100,
        2
    ) AS retention_pct
FROM customer_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
GROUP BY ca.cohort_month, ca.period_number, cs.cohort_customers
ORDER BY ca.cohort_month, ca.period_number;
```

### Funnel Analysis
```sql
WITH funnel_steps AS (
    SELECT
        user_id,
        MAX(CASE WHEN event = 'visit' THEN 1 ELSE 0 END) AS visited,
        MAX(CASE WHEN event = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event = 'checkout_start' THEN 1 ELSE 0 END) AS started_checkout,
        MAX(CASE WHEN event = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM events
    WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT
    'Visit' AS step,
    COUNT(*) AS users,
    100.0 AS pct_of_total,
    100.0 AS conversion_rate
FROM funnel_steps WHERE visited = 1

UNION ALL

SELECT
    'Add to Cart',
    SUM(added_to_cart),
    ROUND(SUM(added_to_cart)::DECIMAL / NULLIF(SUM(visited), 0) * 100, 2),
    ROUND(SUM(added_to_cart)::DECIMAL / NULLIF(SUM(visited), 0) * 100, 2)
FROM funnel_steps

UNION ALL

SELECT
    'Start Checkout',
    SUM(started_checkout),
    ROUND(SUM(started_checkout)::DECIMAL / NULLIF(SUM(visited), 0) * 100, 2),
    ROUND(SUM(started_checkout)::DECIMAL / NULLIF(SUM(added_to_cart), 0) * 100, 2)
FROM funnel_steps

UNION ALL

SELECT
    'Purchase',
    SUM(purchased),
    ROUND(SUM(purchased)::DECIMAL / NULLIF(SUM(visited), 0) * 100, 2),
    ROUND(SUM(purchased)::DECIMAL / NULLIF(SUM(started_checkout), 0) * 100, 2)
FROM funnel_steps;
```

### Moving Average with Gap Handling
```sql
WITH date_spine AS (
    -- Generate continuous date range
    SELECT generate_series(
        (SELECT MIN(date) FROM daily_sales),
        (SELECT MAX(date) FROM daily_sales),
        '1 day'::interval
    )::date AS date
),
filled_sales AS (
    -- Fill gaps with zeros
    SELECT
        ds.date,
        COALESCE(s.sales, 0) AS sales
    FROM date_spine ds
    LEFT JOIN daily_sales s ON ds.date = s.date
)
SELECT
    date,
    sales,
    ROUND(AVG(sales) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_7d
FROM filled_sales
ORDER BY date;
```

## Best Practices

### SQL Style Guide
```sql
-- Keywords: UPPERCASE
-- Identifiers: snake_case
-- Indentation: 4 spaces
-- One clause per line
-- Align ON with JOIN

WITH
    -- Comment each CTE's purpose
    base_data AS (
        SELECT
            customer_id,
            order_date,
            amount
        FROM orders
        WHERE order_date >= '2024-01-01'
    )

SELECT
    bd.customer_id,
    COUNT(*) AS order_count,
    SUM(bd.amount) AS total_revenue
FROM base_data bd
INNER JOIN customers c
    ON bd.customer_id = c.id
WHERE c.status = 'active'
GROUP BY bd.customer_id
HAVING COUNT(*) > 1
ORDER BY total_revenue DESC
LIMIT 100;
```

### Performance Guidelines
```
1. Filter early (WHERE before JOIN when possible)
2. Use appropriate indexes (columns in WHERE, JOIN, ORDER BY)
3. Avoid SELECT * (specify only needed columns)
4. Use LIMIT during development
5. Prefer EXISTS over IN for large subqueries
6. Materialize CTEs if reused multiple times
7. Use EXPLAIN ANALYZE to understand query plan
```

### Null Handling
```sql
-- Division by zero
NULLIF(denominator, 0)  -- Returns NULL if zero
value / NULLIF(total, 0)  -- Safe division

-- Replace nulls
COALESCE(value, 0)  -- First non-null value
COALESCE(a, b, c, default)  -- Chain of fallbacks

-- Null-safe comparison
value IS DISTINCT FROM other  -- NULL-aware inequality
```

## Common Patterns

### Date Dimension Join
```sql
SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.sales) AS total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.quarter, d.month_name
ORDER BY d.year, d.quarter;
```

### Running Total with Reset
```sql
SELECT
    date,
    category,
    amount,
    SUM(amount) OVER (
        PARTITION BY category
        ORDER BY date
        ROWS UNBOUNDED PRECEDING
    ) AS running_total
FROM transactions
ORDER BY category, date;
```

### Percentile Calculation
```sql
SELECT
    category,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) AS p25,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) AS p75
FROM sales
GROUP BY category;
```

## Retry Logic

```typescript
const executeQuery = async (sql: string, params: any[]) => {
  const retryConfig = {
    maxRetries: 3,
    backoffMs: [1000, 2000, 4000],
    retryableErrors: ['TIMEOUT', 'CONNECTION_LOST', 'LOCK_WAIT']
  };

  for (let attempt = 0; attempt <= retryConfig.maxRetries; attempt++) {
    try {
      return await db.query(sql, params);
    } catch (error) {
      if (attempt === retryConfig.maxRetries) throw error;
      if (!retryConfig.retryableErrors.includes(error.code)) throw error;
      console.warn(`Query attempt ${attempt + 1} failed, retrying...`);
      await sleep(retryConfig.backoffMs[attempt]);
    }
  }
};
```

## Logging Hooks

```typescript
const sqlHooks = {
  beforeQuery: (sql, params) => {
    console.log(`[SQL] Executing: ${sql.substring(0, 100)}...`);
    const startTime = Date.now();
    return { startTime };
  },

  afterQuery: (result, context) => {
    const duration = Date.now() - context.startTime;
    console.log(`[SQL] Completed in ${duration}ms, ${result.rowCount} rows`);
    metrics.histogram('sql.query_time', duration);
  },

  onError: (error, sql) => {
    console.error(`[SQL] Error: ${error.message}`);
    metrics.increment('sql.errors');
  }
};
```

## Unit Test Template

```typescript
describe('SQL Analytics Skill', () => {
  describe('Aggregations', () => {
    it('should calculate correct YoY growth', async () => {
      const result = await executeQuery(yoyQuery, ['2024-01-01']);
      expect(result.rows[0].yoy_growth_pct).toBeCloseTo(15.5, 1);
    });
  });

  describe('Window Functions', () => {
    it('should compute running total correctly', async () => {
      const result = await executeQuery(runningTotalQuery);
      const totals = result.rows.map(r => r.running_total);
      expect(totals).toEqual([100, 250, 400, 600]);
    });
  });

  describe('Null Handling', () => {
    it('should handle division by zero', async () => {
      const result = await executeQuery(
        'SELECT 100 / NULLIF(0, 0) AS result'
      );
      expect(result.rows[0].result).toBeNull();
    });
  });
});
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Query timeout | Full table scan | Add indexes, filter early |
| Wrong row count | Cartesian product | Check JOIN conditions |
| Duplicate rows | Missing GROUP BY | Add all non-aggregated columns |
| NULL in results | Unhandled NULLs | Use COALESCE or NULLIF |
| Incorrect totals | Wrong aggregation level | Verify grain and GROUP BY |

## Resources

- **PostgreSQL Docs**: Window Functions
- **Mode Analytics**: SQL Tutorial
- **Use The Index, Luke**: Query Optimization
- **Markus Winand**: Modern SQL (advanced patterns)

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release |
| 2.0.0 | 2025-01 | Production-grade with cohort patterns |
