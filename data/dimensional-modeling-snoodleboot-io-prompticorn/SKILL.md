---
name: dimensional-modeling
description: "**Structure:**"
---

# Dimensional Modeling (Verbose)

## Star Schema Design

**Structure:**
```
              dim_date
                |
dim_product -> fact_sales <- dim_customer
                |
            dim_geography
```

### Fact Table Design
```sql
CREATE TABLE fact_sales (
  -- Surrogate keys (small, sequential)
  sale_id BIGINT PRIMARY KEY,
  
  -- Foreign keys to dimensions
  customer_key INT,
  product_key INT,
  date_key INT,
  region_key INT,
  
  -- Measurements
  quantity INT,
  revenue DECIMAL(12,2),
  discount DECIMAL(12,2),
  profit DECIMAL(12,2),
  
  -- Flags for easy filtering
  is_returned BOOLEAN,
  is_rush_order BOOLEAN
);
```

### Dimension Table Design (Customer Example)
```sql
CREATE TABLE dim_customer (
  -- Surrogate key (lookup speed)
  customer_key INT PRIMARY KEY,
  
  -- Natural/business key (uniqueness)
  customer_id INT,
  
  -- Attributes
  customer_name VARCHAR(100),
  customer_segment VARCHAR(50),
  customer_lifetime_value DECIMAL(12,2),
  
  -- SCD Type 2 support
  start_date DATE,
  end_date DATE,
  is_current BOOLEAN,
  
  -- Audit
  load_date DATE,
  update_date DATE
);
```

## Star vs Snowflake

**Star Schema (Denormalized):**
```sql
-- Fast queries (1-2 joins)
SELECT SUM(revenue)
FROM fact_sales
JOIN dim_customer ON fact_sales.customer_key = dim_customer.customer_key
WHERE dim_customer.segment = 'Premium'
```
Pros: Fast, simple | Cons: Data redundancy

**Snowflake Schema (Normalized):**
```sql
-- More joins, cleaner structure
SELECT SUM(revenue)
FROM fact_sales
JOIN dim_customer ON fact_sales.customer_key = dim_customer.customer_key
JOIN dim_segment ON dim_customer.segment_key = dim_segment.segment_key
WHERE dim_segment.name = 'Premium'
```
Pros: Less redundancy | Cons: More joins

## Design Patterns

**Conformed Dimensions:**
Same dimension used by multiple facts
```
fact_sales ----\
                > dim_customer
fact_returns --/
```

**Junk Dimensions:**
Low cardinality flags combined
```sql
CREATE TABLE dim_flags (
  flag_key INT,
  is_weekend BOOLEAN,
  is_holiday BOOLEAN,
  is_end_of_month BOOLEAN
)
```

## Grain (Atomic Level)
```sql
-- Grain: One row per order line
CREATE TABLE fact_sales (
  order_id INT,
  line_item INT,
  quantity INT,
  revenue DECIMAL
  -- Each row = one line item
)
```

## Aggregation Tables
```sql
-- Pre-aggregated by day (faster for dashboards)
CREATE TABLE fact_sales_daily (
  date_key INT,
  product_key INT,
  region_key INT,
  total_quantity INT,
  total_revenue DECIMAL,
  transaction_count INT
)
```

## Slowly Changing Dimensions

**Type 1: Overwrite (no history)**
```sql
UPDATE dim_customer SET address = '123 New St' 
WHERE customer_id = 1;
```

**Type 2: New Row (full history)**
```sql
-- Deactivate old record
UPDATE dim_customer SET end_date = TODAY, is_current = FALSE
WHERE customer_id = 1 AND is_current = TRUE;

-- Add new record
INSERT INTO dim_customer VALUES (..., '2026-04-11', NULL, TRUE);
```

## Common Mistakes

❌ Too many dimensions → Slow queries  
✅ Keep to 10-15 key dimensions

❌ Fact table too detailed → Slow aggregations  
✅ Create separate aggregation tables

❌ No surrogate keys → Slow joins  
✅ Use INT surrogate keys, not business keys

## Query Examples

```sql
-- Standard star query
SELECT 
  dc.segment,
  dp.category,
  dd.month,
  SUM(fs.revenue) as total_revenue,
  COUNT(*) as transaction_count
FROM fact_sales fs
JOIN dim_customer dc USING (customer_key)
JOIN dim_product dp USING (product_key)
JOIN dim_date dd USING (date_key)
WHERE dd.year = 2026
GROUP BY dc.segment, dp.category, dd.month
ORDER BY total_revenue DESC
```
