---
name: trino-optimizer
description: TD Trino performance optimization including CTAS (5x faster), UDP bucketing for ID lookups, magic comments for join distribution, REGEXP_LIKE vs LIKE, and approx functions.
---

# TD Trino Query Optimizer

## Output Optimization

**CTAS is 5x faster than SELECT** (skips JSON serialization):

```sql
create table results as
select td_time_string(time, 'd!', 'JST') as date, count(*) as events
from events
where td_interval(time, '-1M', 'JST')
group by 1
```

## User-Defined Partitioning (UDP)

Hash partition for fast ID lookups on large tables (>100M rows):

```sql
create table customer_events with (
  bucketed_on = array['customer_id'],
  bucket_count = 512
) as
select * from raw_events
where td_interval(time, '-30d', 'JST')
```

**Accelerated queries** (equality on all bucketing columns):
```sql
select * from customer_events
where customer_id = 12345
  and td_interval(time, '-7d', 'JST')
```

**NOT accelerated** (missing bucketing column):
```sql
select * from customer_events
where td_interval(time, '-7d', 'JST')
```

**UDP for colocated joins:**
```sql
-- set session join_distribution_type = 'PARTITIONED'
-- set session colocated_join = 'true'
select a.*, b.*
from customer_events_a a
join customer_events_b b on a.customer_id = b.customer_id
```

## Magic Comments for Join Distribution

```sql
-- BROADCAST: Small right table fits in memory
-- set session join_distribution_type = 'BROADCAST'
select * from large_table, small_lookup
where large_table.id = small_lookup.id

-- PARTITIONED: Both tables large or memory issues
-- set session join_distribution_type = 'PARTITIONED'
select * from large_table_a, large_table_b
where large_table_a.id = large_table_b.id
```

## REGEXP_LIKE vs Multiple LIKE

```sql
-- BAD: Multiple LIKE clauses
where column like '%android%' or column like '%ios%' or column like '%mobile%'

-- GOOD: Single REGEXP_LIKE
where regexp_like(column, 'android|ios|mobile')
```

## Approximate Functions

```sql
approx_distinct(user_id)              -- vs count(distinct user_id)
approx_percentile(response_time, 0.95)
approx_set(column)                    -- HyperLogLog sketch
```

~2% error rate, dramatically reduced memory.

## Common Errors

| Error | Fix |
|-------|-----|
| Query exceeded memory limit | Narrow time range, use approx functions, try PARTITIONED join |
| PAGE_TRANSPORT_TIMEOUT | Reduce columns, use CTAS, process in smaller chunks |
| Query timeout | Add time filters, use limit for testing |

## Optimization Checklist

- Time filter (td_interval/td_time_range)
- Specific columns (not select *)
- approx_distinct for unique counts
- regexp_like for pattern matching
- CTAS for large results
- UDP for frequent ID lookups
