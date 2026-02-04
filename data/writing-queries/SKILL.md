---
name: writing-queries
description: Component skill for systematic SQL query development in DataPeeker analysis sessions
---

# Writing Queries

## Purpose

This component skill guides systematic query development for analytics. Use it when:
- Writing SQL queries for analysis tasks
- Need to ensure queries are correct, documented, and reproducible
- Referenced by process skills requiring query execution
- Struggling with how to express an analytical question in SQL

## Prerequisites

- CSV files imported to database (relational database with SQL support)
- SQL query tool available (database CLI, IDE, or query interface)
- Understanding of table schema (use `understanding-data` skill if needed)
- Clear analytical question to answer

## Query Development Process

Create a TodoWrite checklist for the 5-phase query development process:

```
Phase 1: Clarify Analytical Question
Phase 2: Design Query Logic
Phase 3: Write SQL
Phase 4: Verify Results
Phase 5: Document Query
```

Mark each phase as you complete it. Save queries in numbered markdown files.

---

## Phase 1: Clarify Analytical Question

**Goal:** Translate vague analytical question into specific, answerable query requirements.

### Ask Clarifying Questions

Before writing any SQL, ensure you can answer:

1. **What exactly are we measuring?**
   - Specific metric name and calculation method
   - Example: "Total revenue" vs "Average revenue per customer" vs "Revenue per day"

2. **What is the unit of analysis?**
   - Per transaction, per customer, per day, per product, etc.
   - Example: "Daily sales" means one row per date

3. **What time period?**
   - All time, specific date range, rolling window?
   - How to handle incomplete periods (partial weeks/months)?

4. **What filters apply?**
   - Specific products, regions, customer segments?
   - Exclude returns, cancelled orders, test data?

5. **What groupings/segments?**
   - By product category, by region, by customer type?
   - Or overall aggregate with no grouping?

6. **What comparison or context?**
   - Compared to previous period, to average, to another segment?
   - Rank ordering, percentage of total?

### Document Requirements

Before proceeding to Phase 2, write down:

```markdown
## Query Requirements

**Analytical Question:** [Original question in plain language]

**Specific Metric:** [Exact calculation]
- Formula: [e.g., SUM(amount) / COUNT(DISTINCT customer_id)]
- Name: [e.g., "Average Revenue Per Customer"]

**Unit of Analysis:** [e.g., "One row per product category"]

**Time Period:** [e.g., "January 1 - March 31, 2024"]

**Filters:**
- [Filter 1: e.g., "Exclude cancelled orders"]
- [Filter 2: e.g., "Only completed transactions"]

**Grouping:** [e.g., "Group by product_category"]

**Ordering:** [e.g., "Order by total_revenue DESC, show top 10"]
```

**Don't proceed until requirements are crystal clear.**

---

## Phase 2: Design Query Logic

**Goal:** Plan query structure before writing SQL syntax.

### Identify Required Tables

List all tables needed and why:

```markdown
## Tables Needed

1. **orders** - Contains transaction dates and amounts
   - Join key: order_id
   - Columns: order_date, total_amount, customer_id

2. **customers** - Contains customer segment information
   - Join key: customer_id
   - Columns: customer_id, segment, region

3. **order_items** - Contains product details (if needed)
   - Join key: order_id
   - Columns: product_id, quantity, price
```

### Design Join Strategy

If multiple tables are needed:

```markdown
## Join Logic

Main table: orders (one row per transaction)

LEFT JOIN customers ON orders.customer_id = customers.customer_id
- Type: LEFT (to keep orders even if customer record missing)
- Cardinality: many-to-one (many orders per customer)
- Risk: None - customer_id should always match

INNER JOIN order_items ON orders.order_id = order_items.order_id
- Type: INNER (only want orders with items)
- Cardinality: one-to-many (multiple items per order)
- Risk: Row explosion - order totals will be duplicated
- Mitigation: Calculate item metrics separately or use DISTINCT
```

**Check join cardinality before complex joins to avoid row explosion.**

### Plan Calculation Steps

Break complex calculations into logical steps:

```markdown
## Calculation Steps

Step 1: Filter to desired date range and conditions
- WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
- AND status = 'completed'

Step 2: Calculate base metrics
- Total revenue: SUM(amount)
- Transaction count: COUNT(*)
- Unique customers: COUNT(DISTINCT customer_id)

Step 3: Derive calculated metrics
- Average revenue per customer: total_revenue / unique_customers

Step 4: Group and aggregate
- GROUP BY product_category

Step 5: Order results
- ORDER BY total_revenue DESC
- LIMIT 10
```

### Consider Edge Cases

Document potential issues:

```markdown
## Edge Cases to Handle

1. **NULL values:** How to handle NULL in date, amount, or category?
   - Decision: Exclude rows with NULL in critical columns

2. **Zero division:** What if denominator is zero (e.g., no customers)?
   - Decision: Use NULLIF or CASE to avoid division by zero

3. **Duplicate records:** Could there be duplicate transactions?
   - Decision: Check with COUNT(*) vs COUNT(DISTINCT order_id)

4. **Date formatting:** Are dates stored as strings or native DATE type?
   - Decision: Use database date functions to extract components, verify format is consistent
```

---

## Phase 3: Write SQL

**Goal:** Translate design into clean, commented SQL.

### SQL Best Practices

**DO:**

1. **Use clear formatting:**
```sql
SELECT
  column1,
  column2,
  SUM(column3) as total
FROM table_name
WHERE condition = 'value'
GROUP BY column1, column2
ORDER BY total DESC;
```

2. **Add comments for clarity:**
```sql
-- Calculate daily sales metrics for Q1 2024
SELECT
  -- Extract date component (function varies by database)
  -- SQLite: DATE(order_date)
  -- PostgreSQL: order_date::date or DATE(order_date)
  -- MySQL: DATE(order_date)
  CAST(order_date AS DATE) as sale_date,
  COUNT(*) as transaction_count,  -- Total orders per day
  SUM(amount) as total_revenue,   -- Gross revenue before returns
  ROUND(AVG(amount), 2) as avg_order_value
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
  AND status = 'completed'  -- Exclude cancelled/pending
GROUP BY CAST(order_date AS DATE)
ORDER BY sale_date;
```

3. **Use meaningful aliases:**
```sql
-- Good
SELECT product_category as category, SUM(amount) as total_revenue

-- Bad
SELECT product_category as pc, SUM(amount) as t
```

4. **Handle NULLs explicitly:**
```sql
SELECT
  customer_id,
  COUNT(order_id) as order_count,
  COALESCE(SUM(amount), 0) as total_spent  -- Replace NULL with 0
FROM orders
WHERE customer_id IS NOT NULL  -- Explicit NULL handling
GROUP BY customer_id;
```

5. **Use CTEs for complex queries:**
```sql
-- Break complex logic into readable steps
WITH daily_sales AS (
  SELECT
    DATE(order_date) as sale_date,
    SUM(amount) as revenue
  FROM orders
  WHERE status = 'completed'
  GROUP BY DATE(order_date)
),
daily_stats AS (
  SELECT
    AVG(revenue) as avg_daily_revenue,
    -- SQLite doesn't have STDEV() - calculate manually using variance formula
    SQRT(AVG(revenue * revenue) - AVG(revenue) * AVG(revenue)) as stddev_revenue
  FROM daily_sales
)
SELECT
  ds.sale_date,
  ds.revenue,
  ROUND((ds.revenue - dst.avg_daily_revenue) / dst.stddev_revenue, 2) as z_score
FROM daily_sales ds
CROSS JOIN daily_stats dst
ORDER BY ds.sale_date;
```

**DON'T:**

1. **Don't use SELECT * in analysis queries:**
```sql
-- Bad - unclear what columns you're using
SELECT * FROM orders WHERE amount > 100;

-- Good - explicit about needed columns
SELECT order_id, order_date, amount FROM orders WHERE amount > 100;
```

2. **Don't ignore case sensitivity in comparisons:**
```sql
-- Risky - might miss 'PENDING' or 'Pending'
WHERE status = 'pending'

-- Better - normalize case
WHERE LOWER(status) = 'pending'
```

3. **Don't create ambiguous joins:**
```sql
-- Bad - which table's date column?
SELECT date, amount FROM orders JOIN shipments USING (order_id);

-- Good - explicit table prefixes
SELECT o.order_date, o.amount, s.ship_date
FROM orders o
JOIN shipments s ON o.order_id = s.order_id;
```

4. **Don't forget GROUP BY requirements:**
```sql
-- Wrong - product_category not in GROUP BY
SELECT product_category, SUM(amount) FROM orders GROUP BY customer_id;

-- Correct
SELECT product_category, SUM(amount) FROM orders GROUP BY product_category;
```

---

## Phase 4: Verify Results

**Goal:** Ensure query returns correct, sensible results.

### Verification Checklist

Before trusting query results, verify:

**1. Row count makes sense:**
```sql
-- Check: Does row count match expectations?
SELECT COUNT(*) as row_count FROM (
  -- Your query here
);
```

Expected: If grouping by day-of-week, should have 7 rows.
If grouping by month, should have 12 rows (or fewer if partial year).

**2. Aggregates are reasonable:**
```sql
-- Check: Are totals in expected range?
SELECT
  SUM(amount) as total_revenue,
  COUNT(*) as transaction_count,
  MIN(amount) as min_amount,
  MAX(amount) as max_amount,
  AVG(amount) as avg_amount
FROM orders;
```

Ask: Do these values make business sense? Any impossibly high/low values?

**3. No unexpected NULLs:**
```sql
-- Check: Are there NULL values in results?
SELECT
  COUNT(*) as total_rows,
  COUNT(column1) as column1_non_null,
  COUNT(column2) as column2_non_null
FROM (
  -- Your query here
);
```

If critical columns have NULLs, investigate why.

**4. Percentages sum to 100% (if applicable):**
```sql
-- Check: Do percentage columns sum to 100?
SELECT SUM(pct_of_total) as total_pct FROM (
  SELECT
    category,
    100.0 * COUNT(*) / SUM(COUNT(*)) OVER () as pct_of_total
  FROM orders
  GROUP BY category
);
```

Should equal 100.0 (or close, accounting for rounding).

**5. Spot check specific values:**

Pick a specific row from results and verify manually:

```sql
-- Example: Verify March 15 sales total
SELECT SUM(amount) FROM orders WHERE CAST(order_date AS DATE) = '2024-03-15';
```

Compare to what your main query shows for March 15.

**6. Compare to known totals:**

```sql
-- Check: Does grouped data sum to overall total?
-- Total from grouped query:
SELECT SUM(category_total) FROM (
  SELECT category, SUM(amount) as category_total
  FROM orders
  GROUP BY category
);

-- Should equal overall total:
SELECT SUM(amount) FROM orders;
```

### Common Query Errors

**Row explosion from joins:**
```sql
-- Symptom: Totals are too high after joining
-- Cause: One-to-many join duplicates rows
-- Fix: Use DISTINCT or calculate at appropriate grain

-- Wrong - duplicates order amounts
SELECT o.order_id, SUM(o.amount)
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;  -- order amount counted once per item!

-- Right - calculate order and item metrics separately
SELECT
  o.order_id,
  o.amount as order_total,
  COUNT(oi.item_id) as item_count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.amount;
```

**Incorrect grouping:**
```sql
-- Symptom: Unexpected row count or aggregates
-- Cause: Missing or extra columns in GROUP BY
-- Fix: Include ALL non-aggregated columns in GROUP BY

-- Wrong - missing category from GROUP BY
SELECT category, product, SUM(sales)
FROM products
GROUP BY category;  -- Error or wrong results

-- Right
SELECT category, product, SUM(sales)
FROM products
GROUP BY category, product;
```

**Date/time parsing errors:**
```sql
-- Symptom: Date groupings don't match expectations
-- Cause: Date format inconsistency or wrong extraction
-- Fix: Verify date format and use appropriate database function

-- Check date format first
SELECT DISTINCT date_column FROM table LIMIT 10;

-- Extract date components using database-specific functions
-- Postgres: TO_CHAR, DATE_TRUNC, EXTRACT
-- MySQL: DATE_FORMAT, YEAR, MONTH
-- SQLite: STRFTIME, DATE
-- See database documentation for specific syntax

-- Generic approach: Cast to DATE type
SELECT CAST(date_column AS DATE) FROM table;
```

---

## Phase 5: Document Query

**Goal:** Create reproducible documentation for query and results.

### Query Documentation Template

Save each query in a numbered markdown file:

```markdown
# [Query Purpose]

## Analytical Question
[What question does this query answer?]

Example: "What are the top 10 product categories by revenue in Q1 2024?"

## Rationale
[Why is this query needed for the analysis?]

Example: "Identifies high-value categories to prioritize for Q2 marketing campaigns."

## Query
```sql
-- Clear, commented SQL
SELECT
  product_category,
  COUNT(DISTINCT order_id) as order_count,
  SUM(amount) as total_revenue,
  ROUND(AVG(amount), 2) as avg_order_value
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
  AND status = 'completed'
GROUP BY product_category
ORDER BY total_revenue DESC
LIMIT 10;
```

## Results
[Paste actual query results - raw output]

```
product_category | order_count | total_revenue | avg_order_value
Electronics      | 1523        | 345678.90     | 226.89
Home & Garden    | 2341        | 298432.10     | 127.48
Clothing         | 3456        | 234567.80     | 67.89
...
```

## Interpretation
[What do the results show? Key takeaways.]

- Electronics generated highest revenue ($345K) despite fewer orders (1,523)
- Electronics has highest average order value ($227) - premium category
- Clothing has most orders (3,456) but lower AOV ($68) - volume category

## Data Quality Notes
[Any issues or caveats about the data]

- No NULL categories found
- Date range: 90 complete days (Jan 1 - Mar 31)
- Excluded 47 cancelled orders from analysis
```

### Documentation Best Practices

**DO:**
- Save queries in version control (git)
- Include exact SQL that was run
- Paste actual results, not summaries
- Note any data quality issues discovered
- Date your analysis files

**DON'T:**
- Paraphrase results (show actual numbers)
- Round or simplify results prematurely
- Skip documenting failed queries (document what didn't work and why)
- Forget to note filters and exclusions

---

## Common Query Patterns

### Pattern 1: Time Series Analysis

**Use case:** Analyze metrics over time (daily, weekly, monthly trends)

```sql
-- Daily trend
SELECT
  CAST(order_date AS DATE) as date,
  COUNT(*) as order_count,
  SUM(amount) as revenue,
  ROUND(AVG(amount), 2) as avg_order_value
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY CAST(order_date AS DATE)
ORDER BY date;

-- Weekly trend (implementation varies by database)
-- Postgres: DATE_TRUNC('week', order_date)
-- MySQL: DATE_SUB(order_date, INTERVAL WEEKDAY(order_date) DAY)
-- SQLite: DATE(order_date, 'weekday 0', '-6 days')
SELECT
  -- Use database-specific function to get week start date
  [week_start_function] as week_start,
  COUNT(*) as order_count,
  SUM(amount) as revenue
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
GROUP BY week_start
ORDER BY week_start;

-- Monthly trend (implementation varies by database)
-- Postgres: TO_CHAR(order_date, 'YYYY-MM')
-- MySQL: DATE_FORMAT(order_date, '%Y-%m')
-- SQLite: STRFTIME('%Y-%m', order_date)
SELECT
  -- Use database-specific function to extract year-month
  [year_month_function] as year_month,
  COUNT(*) as order_count,
  SUM(amount) as revenue
FROM orders
GROUP BY year_month
ORDER BY year_month;
```

### Pattern 2: Segmentation Analysis

**Use case:** Compare metrics across categories or segments

```sql
-- Basic segmentation
SELECT
  segment,
  COUNT(*) as count,
  SUM(amount) as total,
  ROUND(AVG(amount), 2) as average,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_total
FROM orders
GROUP BY segment
ORDER BY total DESC;

-- Multi-level segmentation
SELECT
  region,
  customer_type,
  COUNT(*) as order_count,
  SUM(amount) as revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY region, customer_type
ORDER BY region, revenue DESC;
```

### Pattern 3: Ranking and Top N

**Use case:** Identify top/bottom performers

```sql
-- Top 10 by revenue
SELECT
  product_name,
  SUM(amount) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Top 20% of customers (by revenue)
-- NOTE: PERCENT_RANK() requires SQLite 3.28+
WITH customer_revenue AS (
  SELECT
    customer_id,
    SUM(amount) as total_revenue
  FROM orders
  GROUP BY customer_id
),
ranked_customers AS (
  SELECT
    customer_id,
    total_revenue,
    PERCENT_RANK() OVER (ORDER BY total_revenue DESC) as percentile_rank
  FROM customer_revenue
)
-- Must use CTE to filter on window function results
SELECT
  customer_id,
  total_revenue,
  percentile_rank
FROM ranked_customers
WHERE percentile_rank <= 0.20
ORDER BY total_revenue DESC;

-- Top 3 products per category
WITH ranked_products AS (
  SELECT
    category,
    product_name,
    SUM(amount) as revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(amount) DESC) as rank
  FROM products
  GROUP BY category, product_name
)
SELECT category, product_name, revenue
FROM ranked_products
WHERE rank <= 3
ORDER BY category, rank;
```

### Pattern 4: Period-over-Period Comparison

**Use case:** Compare current period to previous period

```sql
-- Month-over-month comparison
WITH monthly_sales AS (
  SELECT
    -- Extract year-month (use database-specific function)
    [year_month_function] as year_month,
    SUM(amount) as revenue
  FROM orders
  GROUP BY year_month
)
SELECT
  year_month,
  revenue as current_month_revenue,
  LAG(revenue) OVER (ORDER BY year_month) as previous_month_revenue,
  revenue - LAG(revenue) OVER (ORDER BY year_month) as revenue_change,
  ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year_month)) /
        LAG(revenue) OVER (ORDER BY year_month), 2) as pct_change
FROM monthly_sales
ORDER BY year_month;

-- Year-over-year comparison
-- Extract month and year components (use database-specific functions)
SELECT
  [month_function] as month,
  SUM(CASE WHEN [year_function] = '2023' THEN amount ELSE 0 END) as revenue_2023,
  SUM(CASE WHEN [year_function] = '2024' THEN amount ELSE 0 END) as revenue_2024,
  SUM(CASE WHEN [year_function] = '2024' THEN amount ELSE 0 END) -
  SUM(CASE WHEN [year_function] = '2023' THEN amount ELSE 0 END) as yoy_change
FROM orders
WHERE [year_function] IN ('2023', '2024')
GROUP BY month
ORDER BY month;
```

### Pattern 5: Cohort Analysis

**Use case:** Analyze behavior of groups defined by time of first action

```sql
-- Customer cohort by first purchase month
WITH first_purchase AS (
  SELECT
    customer_id,
    -- Extract year-month from first purchase (use database-specific function)
    [year_month_function(MIN(order_date))] as cohort_month
  FROM orders
  GROUP BY customer_id
)
SELECT
  fp.cohort_month,
  COUNT(DISTINCT o.customer_id) as customers,
  COUNT(o.order_id) as total_orders,
  SUM(o.amount) as total_revenue,
  ROUND(1.0 * COUNT(o.order_id) / COUNT(DISTINCT o.customer_id), 2) as orders_per_customer
FROM first_purchase fp
JOIN orders o ON fp.customer_id = o.customer_id
GROUP BY fp.cohort_month
ORDER BY fp.cohort_month;
```

### Pattern 6: Distribution Analysis

**Use case:** Understand distribution of values (percentiles, buckets)

```sql
-- Value distribution by buckets
SELECT
  CASE
    WHEN amount < 25 THEN '$0-24'
    WHEN amount < 50 THEN '$25-49'
    WHEN amount < 100 THEN '$50-99'
    WHEN amount < 250 THEN '$100-249'
    ELSE '$250+'
  END as amount_bucket,
  COUNT(*) as order_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_orders,
  SUM(amount) as total_revenue,
  ROUND(100.0 * SUM(amount) / SUM(SUM(amount)) OVER (), 2) as pct_of_revenue
FROM orders
GROUP BY amount_bucket
ORDER BY MIN(amount);

-- Percentile calculation (manual approach for SQLite)
WITH ranked_orders AS (
  SELECT
    amount,
    ROW_NUMBER() OVER (ORDER BY amount) as row_num,
    COUNT(*) OVER () as total_count
  FROM orders
)
SELECT
  'P25' as percentile,
  amount
FROM ranked_orders
WHERE row_num = CAST(total_count * 0.25 AS INTEGER)
UNION ALL
SELECT 'P50', amount
FROM ranked_orders
WHERE row_num = CAST(total_count * 0.50 AS INTEGER)
UNION ALL
SELECT 'P75', amount
FROM ranked_orders
WHERE row_num = CAST(total_count * 0.75 AS INTEGER);
```

---

## Database-Specific Implementation

This skill provides database-agnostic query guidance. For database-specific syntax:

- **SQLite**: Use the `using-sqlite` skill for SQLite-specific date functions (STRFTIME), CLI invocation patterns, and SQLite idioms
- **PostgreSQL, MySQL, etc.**: Consult database documentation for date/time functions, string operations, and window function syntax

**Core SQL patterns** (SELECT, JOIN, GROUP BY, CTEs, window functions) are consistent across databases. **Function syntax** (date extraction, string manipulation) varies by database.

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Premature Aggregation

**Problem:** Aggregating too early loses detail needed for further analysis

```sql
-- Bad - can't drill down further
SELECT
  category,
  SUM(amount) as total
FROM orders
GROUP BY category;

-- Better - keep grain, aggregate in visualization/reporting layer
-- Or use CTE to preserve both detail and summary
WITH category_totals AS (
  SELECT category, SUM(amount) as total
  FROM orders
  GROUP BY category
)
SELECT
  o.*,
  ct.total as category_total,
  ROUND(100.0 * o.amount / ct.total, 2) as pct_of_category
FROM orders o
JOIN category_totals ct ON o.category = ct.category;
```

### Anti-Pattern 2: Ignoring NULL Semantics

**Problem:** NULLs behave unexpectedly in comparisons and aggregates

```sql
-- Bad - NULL != NULL, so this misses NULL values
SELECT * FROM orders WHERE status != 'completed';

-- Good - explicitly handle NULLs
SELECT * FROM orders
WHERE status != 'completed' OR status IS NULL;

-- Bad - COUNT(*) includes NULLs, COUNT(column) doesn't
SELECT COUNT(column) FROM table;  -- May not match row count!

-- Good - be explicit
SELECT
  COUNT(*) as total_rows,
  COUNT(column) as non_null_count,
  COUNT(*) - COUNT(column) as null_count
FROM table;
```

### Anti-Pattern 3: Implicit Type Conversion

**Problem:** SQLite's dynamic typing can cause unexpected behavior

```sql
-- Bad - comparing number to string
SELECT * FROM orders WHERE amount > '100';  -- Works but risky

-- Good - explicit types
SELECT * FROM orders WHERE CAST(amount AS REAL) > 100.0;

-- Bad - date comparison as strings might fail
WHERE date_column > '2024-1-1'  -- Might not work as expected

-- Good - proper date format
WHERE date_column > '2024-01-01'  -- ISO format: YYYY-MM-DD
```

### Anti-Pattern 4: Over-Reliance on Subqueries

**Problem:** Nested subqueries are hard to read and debug

```sql
-- Bad - deeply nested subqueries
SELECT * FROM (
  SELECT * FROM (
    SELECT * FROM orders WHERE amount > 100
  ) WHERE category = 'Electronics'
) WHERE order_date > '2024-01-01';

-- Good - use CTEs for readability
WITH high_value_orders AS (
  SELECT * FROM orders WHERE amount > 100
),
electronics_orders AS (
  SELECT * FROM high_value_orders WHERE category = 'Electronics'
)
SELECT * FROM electronics_orders
WHERE order_date > '2024-01-01';
```

### Anti-Pattern 5: Cartesian Products

**Problem:** Forgetting join conditions creates row explosion

```sql
-- Bad - missing join condition
SELECT o.*, c.*
FROM orders o, customers c;  -- Every order paired with every customer!

-- Good - explicit join
SELECT o.*, c.*
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

---

## Integration with Process Skills

Process skills reference this component skill with:

```markdown
Use the `writing-queries` component skill to develop SQL queries systematically, ensuring correctness and documentation.
```

When writing queries during analysis:
1. Clarify what you're measuring (Phase 1)
2. Design query logic before coding (Phase 2)
3. Write clean, commented SQL (Phase 3)
4. Verify results make sense (Phase 4)
5. Document in numbered file (Phase 5)

This systematic approach prevents common SQL errors and ensures reproducible analysis.
