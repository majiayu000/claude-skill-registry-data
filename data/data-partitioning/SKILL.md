---
name: data-partitioning
description: "**Monthly Partitions:**"
---

# Data Partitioning (Verbose)

## Time-Based Partitioning

**Monthly Partitions:**
```sql
CREATE TABLE events (
  event_id BIGINT,
  user_id INT,
  event_time TIMESTAMP
) PARTITION BY RANGE (YEAR_MONTH(event_time)) (
  PARTITION p202601 VALUES LESS THAN ('202602'),
  PARTITION p202602 VALUES LESS THAN ('202603'),
  PARTITION p202603 VALUES LESS THAN ('202604'),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

**Automatic Partition Creation:**
```sql
-- In BigQuery
CREATE OR REPLACE TABLE events
PARTITION BY DATE(event_time) AS
SELECT * FROM raw_events;
```

## Partition Key Selection

| Key | Best For | Cons |
|-----|----------|------|
| Date | Time-series, archival | Imbalanced growth |
| Customer ID | Multi-tenant | Uneven distribution |
| Region | Geo data | Compliance data residency |
| Hash | Even distribution | Hard to query ranges |

## Query Performance Optimization

**Partition Pruning (Critical):**
```sql
-- ✅ GOOD: WHERE clause matches partition key
SELECT * FROM orders 
WHERE created_date >= '2026-04-01' 
AND created_date < '2026-05-01'
-- Only scans April 2026 partition!

-- ❌ BAD: No partition filtering
SELECT * FROM orders WHERE customer_id = 123
-- Scans ALL partitions (slow!)
```

**Performance Impact:**
- 100M rows → 10 partitions = 10M rows per partition
- Full table scan: 100M rows → 30 seconds
- Partition pruned: 10M rows → 3 seconds (10x faster!)

## Partition Maintenance

**Archive Old Data:**
```bash
# Move 2024 data to cold storage (S3)
gsutil mv gs://warehouse/orders/2024/* \
         gs://cold-storage/orders/2024/
         
# Query via external table if needed
CREATE EXTERNAL TABLE orders_2024
LOCATION 'gs://cold-storage/orders/2024/*'
```

**Automatic Partition Expiration:**
```sql
ALTER TABLE orders
SET OPTIONS (partition_expiration_ms = 31536000000);
-- Delete partitions > 1 year old
```

**Monitor Partition Sizes:**
```sql
SELECT 
  partition_key,
  COUNT(*) as row_count,
  ROUND(SIZE_BYTES/1024/1024/1024, 2) as size_gb
FROM `project.dataset.orders$__PARTITIONS_SUMMARY__`
GROUP BY partition_key
ORDER BY size_gb DESC
```

## Anti-Patterns

❌ Too many partitions (>1000)  
✅ Keep partitions between 1GB - 100GB

❌ Non-sequential partition keys  
✅ Use date/time (naturally sequential)

❌ Partitioning by high-cardinality column  
✅ Partition by date, filter by ID
