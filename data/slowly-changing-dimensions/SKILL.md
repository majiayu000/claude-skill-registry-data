---
name: slowly-changing-dimensions
description: "**When:** Not important (contact info)"
---

# Slowly Changing Dimensions (Verbose)

## Type 1: Overwrite History

**When:** Not important (contact info)
**Implementation:**
```sql
UPDATE dim_customer 
SET email = 'newemail@example.com'
WHERE customer_id = 123;
```

**Pros:** Simple, minimal storage  
**Cons:** Lose history, hard to debug

## Type 2: Add New Row (Full History)

**When:** Important for analysis (customer value, status)
**Implementation:**
```sql
-- Deactivate current record
UPDATE dim_customer 
SET end_date = '2026-04-10', is_current = FALSE
WHERE customer_id = 123 AND is_current = TRUE;

-- Insert new record
INSERT INTO dim_customer (
  customer_key, customer_id, name, segment,
  start_date, end_date, is_current
) VALUES (
  999, 123, 'John Smith', 'Premium',
  '2026-04-11', NULL, TRUE
);
```

**Query with SCD Type 2:**
```sql
-- How much revenue from each segment at that time?
SELECT 
  dc.segment,
  SUM(fs.revenue)
FROM fact_sales fs
JOIN dim_customer dc 
  ON fs.customer_key = dc.customer_key
  AND fs.date_key BETWEEN dc.start_date AND dc.end_date
WHERE fs.date >= '2026-01-01'
GROUP BY dc.segment
```

**Pros:** Full history, good for trend analysis  
**Cons:** More rows, complex queries

## Type 3: Add Columns (Current + Previous)

**When:** Need recent history (current + previous)
```sql
ALTER TABLE dim_customer ADD previous_segment VARCHAR;
ALTER TABLE dim_customer ADD change_date DATE;

-- Update
UPDATE dim_customer
SET previous_segment = segment,
    segment = 'Premium',
    change_date = '2026-04-11'
WHERE customer_id = 123;
```

**Pros:** Simple, tracks previous  
**Cons:** Only 2 versions (current + previous)

## Type 4: Slowly Changing Facts

**When:** Fact attributes change (price changes)
```sql
-- Store price at transaction time
CREATE TABLE fact_sales (
  sale_id INT,
  product_id INT,
  price_sold DECIMAL,  -- Price at sale time
  current_price DECIMAL  -- Price today (for comparison)
);
```

## Implementation Patterns

**ELT Pattern (Load Then Transform):**
```sql
-- Load raw customer data
INSERT INTO stg_customer
SELECT * FROM raw_customer_data;

-- Identify changes
SELECT * FROM stg_customer sc
LEFT JOIN dim_customer dc 
  ON sc.customer_id = dc.customer_id AND dc.is_current
WHERE sc.segment != dc.segment
  OR sc.status != dc.status;

-- Apply SCD Type 2
-- Deactivate old, insert new
```

## Decision Matrix

| Attribute | Change Frequency | Business Impact | SCD Type |
|-----------|------------------|-----------------|----------|
| Email | Rare | Low | 1 |
| Segment | Few times/year | High | 2 |
| Address | Few times/year | Medium | 2 |
| Phone | Rare | Low | 1 |
| Salary | Annual | High | 2 |
| Status | Frequent | High | 2 |

## Performance Considerations

**Type 1 (Simple):**
- No extra rows
- Fast inserts

**Type 2 (Complex):**
- 2x-10x more rows
- Slower dimension lookups
- Requires SCD join logic

**Optimization:**
```sql
-- Denormalize current values
CREATE TABLE dim_customer_current AS
SELECT * FROM dim_customer WHERE is_current = TRUE;
-- Use this for most queries, fallback to full for historical
```

## Common Mistakes

❌ Type 2 for everything → Bloats dimensions  
✅ Use Type 1 for unimportant fields

❌ Missing end_date/is_current flag → Complex queries  
✅ Always add status columns

❌ SCD applied to fact table → Breaks grain  
✅ Apply to dimensions only
