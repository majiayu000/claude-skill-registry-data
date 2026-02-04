---
name: databricks-query
description: Execute SQL queries against Databricks using the DBSQL MCP server. Use when querying Unity Catalog tables, running SQL analytics, exploring Databricks data, or when user mentions Databricks queries, SQL execution, Unity Catalog, or data warehouse operations. Handles query execution, result formatting, and error handling.
version: 1.0.0
---

# Databricks Query Skill

## Overview

This skill enables SQL query execution against Databricks using the Databricks Managed MCP DBSQL server. It provides access to Unity Catalog tables, SQL warehouses, and supports both simple queries and complex analytics.

## Prerequisites

- Databricks MCP server configured in `.vscode/mcp.json`
- Environment variables set:
  - `DATABRICKS_HOST`
  - `DATABRICKS_TOKEN`
  - `DATABRICKS_CATALOG`
  - `DATABRICKS_SCHEMA`

## MCP Integration

This skill uses the Databricks DBSQL MCP server which is automatically available when configured. The MCP server provides tools for:
- Executing SQL queries
- Listing tables and schemas
- Getting table metadata
- Query result formatting

## Common Operations

### 1. Simple SELECT Query

```sql
SELECT *
FROM main.sales.customer_revenue
LIMIT 10;
```

### 2. Filtered Query with Aggregation

```sql
SELECT
    customer_id,
    SUM(revenue) as total_revenue,
    COUNT(*) as transaction_count
FROM main.sales.transactions
WHERE date >= '2025-01-01'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 100;
```

### 3. Join Multiple Tables

```sql
SELECT
    c.customer_id,
    c.customer_name,
    SUM(t.revenue) as total_revenue
FROM main.sales.customers c
INNER JOIN main.sales.transactions t
    ON c.customer_id = t.customer_id
WHERE t.date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC;
```

### 4. Create Table from Query (CTAS)

```sql
CREATE OR REPLACE TABLE main.analytics.customer_summary AS
SELECT
    customer_id,
    COUNT(*) as order_count,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_revenue,
    MAX(date) as last_order_date
FROM main.sales.transactions
GROUP BY customer_id;
```

### 5. Insert Data

```sql
INSERT INTO main.sales.customer_revenue
SELECT
    customer_id,
    SUM(revenue) as revenue,
    CURRENT_DATE() as calculation_date
FROM main.sales.transactions
WHERE date = CURRENT_DATE() - INTERVAL 1 DAY
GROUP BY customer_id;
```

## Unity Catalog Queries

### List Schemas

```sql
SHOW SCHEMAS IN main;
```

### List Tables in Schema

```sql
SHOW TABLES IN main.sales;
```

### Describe Table Schema

```sql
DESCRIBE TABLE main.sales.customer_revenue;
```

### Get Table Properties

```sql
SHOW TBLPROPERTIES main.sales.customer_revenue;
```

### Show Table Statistics

```sql
DESCRIBE DETAIL main.sales.customer_revenue;
```

## Best Practices

1. **Use Fully Qualified Names**: Always use `catalog.schema.table` format
2. **Limit Results**: Use `LIMIT` clause for exploratory queries
3. **Partition Filters**: Filter on partition columns for performance
4. **Avoid SELECT ***: Specify only needed columns
5. **Use EXPLAIN**: Check query plans for complex queries
6. **Parameterize Values**: Use variables for reusable queries

## Query Patterns

### Exploratory Analysis

```sql
-- Quick sample
SELECT * FROM main.sales.transactions LIMIT 5;

-- Row count
SELECT COUNT(*) FROM main.sales.transactions;

-- Date range
SELECT MIN(date), MAX(date) FROM main.sales.transactions;

-- Value distribution
SELECT column_name, COUNT(*)
FROM main.sales.transactions
GROUP BY column_name
ORDER BY COUNT(*) DESC
LIMIT 20;
```

### Data Quality Checks

```sql
-- Check for nulls
SELECT
    COUNT(*) as total_rows,
    COUNT(customer_id) as non_null_customer_id,
    COUNT(revenue) as non_null_revenue
FROM main.sales.transactions;

-- Find duplicates
SELECT customer_id, transaction_id, COUNT(*)
FROM main.sales.transactions
GROUP BY customer_id, transaction_id
HAVING COUNT(*) > 1;

-- Check date ranges
SELECT
    MIN(date) as earliest_date,
    MAX(date) as latest_date,
    DATEDIFF(MAX(date), MIN(date)) as date_span_days
FROM main.sales.transactions;
```

### Time-Series Analysis

```sql
-- Daily aggregation
SELECT
    DATE(timestamp) as date,
    COUNT(*) as transaction_count,
    SUM(revenue) as daily_revenue
FROM main.sales.transactions
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Monthly trends
SELECT
    DATE_TRUNC('month', date) as month,
    SUM(revenue) as monthly_revenue,
    COUNT(DISTINCT customer_id) as unique_customers
FROM main.sales.transactions
GROUP BY DATE_TRUNC('month', date)
ORDER BY month DESC;
```

## Error Handling

When queries fail, check:
1. **Syntax**: Validate SQL syntax
2. **Permissions**: Ensure access to catalog/schema/table
3. **Table Exists**: Verify table name and catalog
4. **Data Types**: Check for type mismatches in joins/filters
5. **Warehouse**: Ensure SQL warehouse is running

## Integration with MCP

The Databricks DBSQL MCP server provides these capabilities automatically:
- Query execution via MCP tools
- Result set formatting
- Error messages and debugging info
- Connection management

When using this skill, the MCP server handles the connection details. Simply focus on writing correct SQL queries.

## Output Format

Query results are typically returned as:
- Rows: List of dictionaries (one per row)
- Columns: List of column names
- Row count: Number of rows returned
- Execution time: Query duration

## Performance Tips

1. **Use Partitions**: Filter on partition columns first
2. **Cache Results**: For repeated queries, cache intermediate results
3. **Optimize Joins**: Put smaller table first in joins
4. **Use ANALYZE**: Run `ANALYZE TABLE` to update statistics
5. **Monitor Costs**: Check query costs in Databricks UI

## Security

- Queries execute with user's Databricks permissions
- Row-level and column-level security is enforced
- Audit logs capture all query activity
- Use secure credential management (never hardcode tokens)

## Common Use Cases

1. **Data Exploration**: Quick SELECT queries to understand data
2. **Analytics**: Aggregations and metrics calculation
3. **Data Validation**: Quality checks and auditing
4. **ETL**: Transform and load data between tables
5. **Reporting**: Generate datasets for dashboards
