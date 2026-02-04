---
name: sql-analysis
description: Master SQL for data analysis with complex queries, joins, aggregations, window functions, and query optimization.
---

# SQL Analysis

Master SQL for extracting, transforming, and analyzing data using complex queries, joins, aggregations, and advanced SQL techniques.

## When to Use This Skill

- Data extraction
- Business reporting
- Ad-hoc analysis
- Data exploration
- Metric calculation
- Customer segmentation
- Funnel analysis
- Cohort analysis

## Core Concepts

### 1. Complex Joins

```sql
-- Customer purchase analysis with multiple joins
SELECT 
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.quantity * oi.price) as total_revenue,
    AVG(o.order_total) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT o.order_id) >= 3
ORDER BY total_revenue DESC;
```

### 2. Window Functions

```sql
-- Monthly revenue with running total and growth
SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(order_total) as monthly_revenue,
    SUM(SUM(order_total)) OVER (
        ORDER BY DATE_TRUNC('month', order_date)
    ) as running_total,
    LAG(SUM(order_total)) OVER (
        ORDER BY DATE_TRUNC('month', order_date)
    ) as prev_month_revenue,
    ROUND(
        (SUM(order_total) - LAG(SUM(order_total)) OVER (ORDER BY DATE_TRUNC('month', order_date))) 
        / LAG(SUM(order_total)) OVER (ORDER BY DATE_TRUNC('month', order_date)) * 100,
        2
    ) as growth_pct
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;
```

### 3. CTEs (Common Table Expressions)

```sql
-- Customer cohort retention analysis
WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(order_date) as cohort_month
    FROM orders
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT 
        fp.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        EXTRACT(MONTH FROM AGE(o.order_date, fp.cohort_month)) as months_since_first
    FROM first_purchase fp
    JOIN orders o ON fp.customer_id = o.customer_id
)
SELECT 
    cohort_month,
    months_since_first,
    COUNT(DISTINCT customer_id) as active_customers
FROM monthly_activity
GROUP BY cohort_month, months_since_first
ORDER BY cohort_month, months_since_first;
```

## Best Practices

1. **Use CTEs** - Readable, maintainable complex queries
2. **Index aware** - Understand query performance
3. **Avoid SELECT *** - Specify needed columns
4. **Comment queries** - Explain business logic
5. **Test incrementally** - Build queries step by step
6. **Handle NULLs** - Use COALESCE, proper joins
7. **Aggregate before join** - Reduce data volume
8. **Use EXPLAIN** - Analyze query plans

## Resources

- **Mode SQL Tutorial**: https://mode.com/sql-tutorial/
- **SQL Style Guide**: https://www.sqlstyle.guide/
