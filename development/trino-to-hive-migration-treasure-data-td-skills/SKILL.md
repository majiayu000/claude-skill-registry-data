---
name: trino-to-hive-migration
description: Convert Trino queries to Hive when memory errors occur. Covers syntax differences (td_time_string→TD_TIME_FORMAT, REGEXP_LIKE→RLIKE, ARRAY_AGG→COLLECT_LIST) and engine selection.
---

# Trino to Hive Migration

## When to Migrate

Use Hive when Trino fails with:
- `Query exceeded per-node memory limit`
- `Query exceeded distributed memory limit`
- Processing > 1 month of data, complex multi-way JOINs, high cardinality GROUP BY

## Syntax Conversion

| Trino | Hive |
|-------|------|
| `td_time_string(time, 'd!', 'JST')` | `TD_TIME_FORMAT(time, 'yyyy-MM-dd', 'JST')` |
| `approx_distinct(col)` | `approx_distinct(col)` (Hivemall - compatible!) |
| `approx_percentile(col, 0.95)` | `percentile(col, 0.95)` |
| `array_agg(col)` | `collect_list(col)` |
| `string_agg(col, ',')` | `concat_ws(',', collect_list(col))` |
| `regexp_like(col, 'pattern')` | `col rlike 'pattern'` |
| Automatic small table join | `/*+ MAPJOIN(t) */` |

## Example Migration

**Trino (fails with memory error):**
```sql
select
  td_time_string(time, 'd!', 'JST') as date,
  approx_distinct(session_id) as sessions
from events
where td_time_range(time, '2024-01-01', '2024-12-31')
group by td_time_string(time, 'd!', 'JST')
```

**Hive (works):**
```sql
select
  TD_TIME_FORMAT(time, 'yyyy-MM-dd', 'JST') as date,
  approx_distinct(session_id) as sessions
from events
where td_time_range(time, '2024-01-01', '2024-12-31', 'JST')
group by TD_TIME_FORMAT(time, 'yyyy-MM-dd', 'JST')
```

## Engine Selection

### In Digdag:
```yaml
+query_trino:
  td>: queries/analysis.sql
  engine: presto

+query_hive:
  td>: queries/analysis.sql
  engine: hive
```

### In TD Toolbelt:
```bash
td query -d database_name -T presto "SELECT ..."
td query -d database_name -T hive "SELECT ..."
```

## Performance Tips for Hive

```sql
-- MAPJOIN hint for small tables
select /*+ MAPJOIN(small_table) */ *
from large_table l
join small_table s on l.id = s.id

-- Process in chunks for very large datasets
where td_interval(time, '-1d', 'JST')  -- Daily instead of yearly
```

## Typical Timeline

- Trino: Fails after 5 min with memory error
- Hive: Completes in 20-30 min successfully
