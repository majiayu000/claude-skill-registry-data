---
name: window-functions-deep-dive
description: Master OPAL window functions for row-relative calculations, rankings, and moving aggregates. Covers lag(), lead(), row_number(), rank(), dense_rank(), moving averages, first(), and last(). Use when comparing rows to neighbors, ranking within partitions, calculating rate of change, or computing time-based moving windows. CRITICAL - OPAL uses window() function wrapper, NOT SQL OVER clause.
---

# Window Functions Deep Dive

## Overview

Window functions perform calculations across sets of rows related to the current row, without collapsing rows like `aggregate` does. They enable:

- **Row comparisons**: Compare current row to previous/next rows (lag/lead)
- **Rankings**: Assign ranks within partitions (row_number/rank/dense_rank)
- **Moving calculations**: Rolling averages, sums over time windows
- **Boundary values**: First/last values in windows or partitions

## CRITICAL: OPAL vs SQL Syntax

**❌ WRONG - SQL OVER Syntax (Does NOT Work)**:
```sql
SUM(val) OVER (PARTITION BY subject ORDER BY time ROWS UNBOUNDED PRECEDING)
# Error: Unknown function 'over()'
```

**✅ CORRECT - OPAL window() Function**:
```opal
window(sum(val), group_by(subject), order_by(time))
```

**Key Difference**: OPAL uses `window()` function wrapper, NOT SQL `OVER` clause. The Observe documentation sometimes shows SQL syntax for reference, but you MUST use the `window()` syntax in actual OPAL queries.

---

## Window Function Categories

### 1. Offset Functions (lag/lead)

Access values from previous or next rows relative to current row.

**Functions**:
- `lag(column, offset)` - Get value from N rows back
- `lead(column, offset)` - Get value from N rows ahead

**Syntax**:
```opal
window(lag(column, N), group_by(partition_columns))
window(lead(column, N), group_by(partition_columns))
```

**Key Points**:
- Offset defaults to 1 if not specified
- Returns `null` when offset goes beyond partition boundary
- MUST specify `group_by()` for partitioning (even if single partition)
- Optional `order_by()` for explicit ordering (default: unspecified)

---

### 2. Ranking Functions

Assign ranks or row numbers within partitions.

**Functions**:
- `row_number()` - Sequential unique numbers (1, 2, 3, 4, ...)
- `rank()` - Ranks with gaps after ties (1, 2, 2, 4, ...)
- `dense_rank()` - Ranks without gaps (1, 2, 2, 3, ...)

**Syntax**:
```opal
window(row_number(), group_by(partition), order_by(sort_col))
window(rank(), group_by(partition), order_by(sort_col))
window(dense_rank(), group_by(partition), order_by(sort_col))
```

**Key Differences**:

| Value | row_number() | rank() | dense_rank() |
|-------|--------------|--------|--------------|
| 59    | 1            | 1      | 1            |
| 53    | 2            | 2      | 2            |
| 43    | 3            | 3      | 3            |
| 3     | 4            | 4      | 4            |
| 3     | 5            | 4      | 4            | (tie)
| 2     | 6            | 6      | 5            | (gap vs no gap)

**When to Use**:
- `row_number()`: Need unique IDs, pagination, sampling
- `rank()`: Olympic-style ranking (ties share rank, gaps for fairness)
- `dense_rank()`: Category ranking (no gaps, continuous numbering)

---

### 3. Aggregate Functions with Time Windows

Calculate rolling aggregates over time-based sliding windows.

**Functions**:
- `avg(column)` - Moving average
- `sum(column)` - Moving sum
- `min(column)` - Moving minimum
- `max(column)` - Moving maximum
- `count(column)` - Moving count

**Syntax**:
```opal
window(aggregate_func(column), group_by(partition), order_by(time_col), frame(back:duration))
```

**Frame Durations**:
- Minutes: `5m`, `15m`, `30m`
- Hours: `1h`, `6h`, `12h`, `24h`
- Days: `1d`, `7d`, `30d`

**IMPORTANT**: OPAL only supports time-based frames (`back:duration`), NOT row-based frames like SQL's `ROWS N PRECEDING`.

---

### 4. Value Functions (first/last)

Retrieve first or last value within partition or window.

**Functions**:
- `first(column)` - First value (by order_by)
- `last(column)` - Last value (by order_by)

**Syntax**:
```opal
# Entire partition
window(first(column), group_by(partition), order_by(sort_col))
window(last(column), group_by(partition), order_by(sort_col))

# Sliding window
window(first(column), group_by(partition), order_by(sort_col), frame(back:duration))
window(last(column), group_by(partition), order_by(sort_col), frame(back:duration))
```

---

## Pattern 1: Rate of Change Detection (lag/lead)

**Use Case**: Detect sudden spikes or drops in metrics.

```opal
align 5m, rate:sum(m("span_call_count_5m"))
| make_col previous_rate:window(lag(rate, 1), group_by(service_name))
| make_col next_rate:window(lead(rate, 1), group_by(service_name))
| make_col rate_change:rate - previous_rate
| make_col pct_change:if(previous_rate > 0, (rate_change / previous_rate) * 100, 0)
| make_col is_spike:if(pct_change > 100 or pct_change < -50, true, false)
| filter is_spike = true
| topk 20, max(pct_change)
```

**Result**:
```
service_name  previous_rate  rate  pct_change  is_spike
frontend      2              50    2400%       true      # 24x increase!
frontend      50             2     -96%        true      # 96% drop
cartservice   10             80    700%        true      # 8x increase
```

**How It Works**:
1. `lag(rate, 1)` gets previous time bucket's rate
2. `lead(rate, 1)` gets next time bucket's rate (for forward detection)
3. Calculate percentage change: `(current - previous) / previous * 100`
4. Flag spikes: >100% increase or >50% decrease
5. `topk` sorts by largest changes

**When to Use**:
- Detect traffic spikes or drops
- Identify service anomalies
- Alert on sudden behavior changes
- Compare bucket-to-bucket changes

---

## Pattern 2: Top-N Per Time Bucket (Ranking)

**Use Case**: Find top 5 busiest services in each 5-minute window.

```opal
align 5m, rate:sum(m("span_call_count_5m"))
| aggregate total:sum(rate), group_by(service_name, _c_bucket)
| make_col rank:window(rank(), group_by(_c_bucket), order_by(desc(total)))
| filter rank <= 5
| sort asc(_c_bucket), asc(rank)
```

**Result**:
```
_c_bucket  service_name             total  rank
5877542    frontend-proxy           59     1
5877542    frontend                 53     2
5877542    featureflagservice       43     3
5877542    productcatalogservice    31     4
5877542    cartservice              8      5
5877543    frontend                 61     1
5877543    frontend-proxy           55     2
...
```

**How It Works**:
1. Aggregate to get total per service per bucket
2. `rank()` within each `_c_bucket` partition
3. `order_by(desc(total))` ranks highest first
4. Filter to top 5
5. Sort for readable output

**When to Use**:
- Top-N queries within time windows
- Identify busiest/slowest services per period
- Compare rankings across time
- Dashboard "top services" widgets

**Variation - Use dense_rank() for No Gaps**:
```opal
make_col dense_rank:window(dense_rank(), group_by(_c_bucket), order_by(desc(total)))
```

Use `dense_rank()` when ties should count as one rank (no gaps).

---

## Pattern 3: Moving Average Baseline

**Use Case**: Detect anomalies by comparing current value to 30-minute moving average.

```opal
align 5m, rate:sum(m("span_call_count_5m"))
| make_col baseline:window(avg(rate), group_by(service_name), order_by(asc(valid_from)), frame(back:30m))
| make_col deviation:rate - baseline
| make_col pct_deviation:if(baseline > 0, (deviation / baseline) * 100, 0)
| make_col is_anomaly:if(pct_deviation > 50 or pct_deviation < -50, true, false)
| filter is_anomaly = true
| topk 20, max(pct_deviation)
```

**Result**:
```
service_name        rate  baseline  deviation  pct_deviation  is_anomaly
featureflagservice  150   30        120        400%           true
frontend            2     26        -24        -92%           true
cartservice         80    20        60         300%           true
```

**How It Works**:
1. `frame(back:30m)` creates 30-minute sliding window
2. `avg(rate)` calculates average within that window
3. Compare current `rate` to `baseline`
4. Flag deviations >50% above or below baseline

**When to Use**:
- Anomaly detection with dynamic baseline
- Smooth out noise in metrics
- Detect sustained changes vs temporary blips
- Performance monitoring (latency vs moving average)

**Frame Duration Guidance**:
- `back:15m` - Very responsive, more false positives
- `back:30m` - Balanced (recommended for most use cases)
- `back:1h` - Stable baseline, less sensitive
- `back:24h` - Day-over-day trending

---

## Pattern 4: Detect Return to Baseline

**Use Case**: Alert when error rate exceeds initial rate by 2x for more than 1 hour.

```opal
align 5m, error_rate:sum(m("span_error_count_5m"))
| make_col first_rate:window(first(error_rate), group_by(service_name), order_by(asc(valid_from)), frame(back:1h))
| make_col current_elevated:if(error_rate > first_rate * 2, true, false)
| filter current_elevated = true
| statsby incidents:count(), avg_elevation:avg(error_rate / first_rate), group_by(service_name)
| sort desc(incidents)
```

**Result**:
```
service_name     incidents  avg_elevation
checkoutservice  15         3.2x          # Error rate 3.2x higher than 1h ago
paymentservice   8          2.8x
fraudservice     3          2.1x
```

**How It Works**:
1. `first(error_rate)` with `frame(back:1h)` gets rate from 1 hour ago
2. Compare current to first: `error_rate > first_rate * 2`
3. Aggregate to count incidents and average elevation

**When to Use**:
- Detect if metric returned to baseline
- Track sustained elevations
- SLO violations (errors above initial threshold)
- Performance degradation alerts

---

## Pattern 5: Smooth Noisy Metrics

**Use Case**: Smooth CPU usage with 10-minute moving average for charting.

```opal
align 1m, cpu:avg(m("cpu_usage_percent"))
| make_col smooth_cpu:window(avg(cpu), group_by(host), order_by(asc(valid_from)), frame(back:10m))
| pick_col valid_from, valid_to, host, cpu, smooth_cpu
```

**Result**:
```
valid_from     host       cpu    smooth_cpu
1763259000...  web-01     85.2   78.5       # Raw vs smoothed
1763259060...  web-01     92.1   79.2       # Spike smoothed out
1763259120...  web-01     76.4   79.8       # Averages over 10m
```

**How It Works**:
1. Align to 1-minute buckets (high resolution)
2. Calculate 10-minute moving average
3. Use `smooth_cpu` for charting, `cpu` for alerts

**When to Use**:
- Smooth spiky metrics for visualization
- Reduce noise in dashboards
- Calculate trends without losing detail
- Separate signal from noise

---

## Pattern 6: Consecutive Threshold Violations

**Use Case**: Alert only if latency exceeds SLO for 3 consecutive buckets.

```opal
align 5m, p95:percentile(duration_ms, 0.95)
| make_col prev1:window(lag(p95, 1), group_by(service_name))
| make_col prev2:window(lag(p95, 2), group_by(service_name))
| make_col all_high:if(p95 > 500 and prev1 > 500 and prev2 > 500, true, false)
| filter all_high = true
| statsby first_violation:min(valid_from), duration_mins:count() * 5, group_by(service_name)
```

**Result**:
```
service_name     first_violation       duration_mins
checkoutservice  2025-11-15 10:30:00   45            # Violated for 45 min
paymentservice   2025-11-15 11:15:00   20            # Violated for 20 min
```

**How It Works**:
1. `lag(p95, 1)` and `lag(p95, 2)` get two previous buckets
2. Check if current AND both previous exceed 500ms
3. Aggregate to find first violation and total duration

**When to Use**:
- Reduce alert fatigue from transient spikes
- Require sustained violations before alerting
- SLO monitoring with grace period
- Stability checks (N consecutive failures)

---

## Common Window Function Patterns

### Quick Reference

| Pattern | Window Function | Use Case |
|---------|-----------------|----------|
| Bucket-to-bucket change | `lag(col, 1)` | Spike detection, rate of change |
| Forward prediction | `lead(col, 1)` | Pre-emptive alerts |
| Top-N per period | `rank()`, `dense_rank()` | Rankings, leaderboards |
| Unique row IDs | `row_number()` | Sampling, pagination |
| Moving average | `avg()` + `frame(back:30m)` | Smoothing, baseline |
| Rolling sum | `sum()` + `frame(back:1h)` | Hourly totals |
| Start of period | `first()` + `frame(back:24h)` | Day-over-day comparison |
| End of period | `last()` + `frame(back:24h)` | Final value in window |

---

## window() Syntax Reference

### Complete Syntax

```opal
window(
  expression,                     # Function to apply
  group_by(partition_columns),    # Partition into groups
  order_by(sort_expression),      # Order within partitions
  frame(back:duration)            # Optional: time-based window
)
```

### Parameters

**expression** (required):
- Offset: `lag(col, N)`, `lead(col, N)`
- Ranking: `row_number()`, `rank()`, `dense_rank()`
- Aggregate: `avg(col)`, `sum(col)`, `min(col)`, `max(col)`, `count(col)`
- Value: `first(col)`, `last(col)`

**group_by()** (required for most functions):
- Partitions data into groups
- Window function operates independently per partition
- Example: `group_by(service_name)` - separate windows per service

**order_by()** (required for ranking, optional for others):
- Defines row order within partitions
- Example: `order_by(asc(valid_from))` - chronological order
- Example: `order_by(desc(total))` - highest first

**frame()** (optional, only for aggregates and value functions):
- Time-based sliding window: `frame(back:duration)`
- Examples: `frame(back:5m)`, `frame(back:1h)`, `frame(back:24h)`
- NOT supported: Row-based frames (`ROWS N PRECEDING` in SQL)

---

## Limitations and Workarounds

### ❌ Limitation 1: No Row-Based Frames

**Problem**: Cannot specify "last 3 rows" or "next 5 rows".

**SQL Syntax (Does NOT Work)**:
```sql
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
ROWS 5 FOLLOWING
```

**OPAL Reality**:
- Only time-based frames: `frame(back:duration)`
- No row-count-based frames

**Workaround**:
- Use fixed time window: `frame(back:15m)` includes ~3 rows at 5m align
- Use multiple `lag()` calls: `lag(col, 1)`, `lag(col, 2)`, `lag(col, 3)`

---

### ❌ Limitation 2: No Cumulative Sums

**Problem**: Cannot create running totals using window functions.

**SQL Syntax (Does NOT Work)**:
```sql
SUM(val) OVER (ORDER BY time ROWS UNBOUNDED PRECEDING)
```

**OPAL Behavior**:
```opal
window(sum(val), order_by(time))  # Returns total, NOT cumulative
```

**Why**: Without frame, sums entire partition. With `frame(back:duration)`, sums time window.

**Workaround**:
- Use subqueries for cumulative calculations
- Process outside OPAL (in application layer)
- Request feature from Observe team

**Example - Partial Workaround**:
```opal
# NOT cumulative, but moving 1-hour sum
window(sum(val), group_by(service), order_by(time), frame(back:1h))
```

---

### ❌ Limitation 3: No OVER Clause

**Problem**: SQL `OVER` clause syntax fails in OPAL.

**SQL Syntax (Does NOT Work)**:
```sql
SUM(val) OVER (PARTITION BY service ORDER BY time)
LAG(val, 1) OVER (PARTITION BY service)
```

**Error**: `Unknown function 'over()'`

**Fix**: Always use `window()` function wrapper.

**Correct OPAL**:
```opal
window(sum(val), group_by(service), order_by(time))
window(lag(val, 1), group_by(service))
```

---

## Decision Tree: Which Window Function?

```
┌─────────────────────────────────────┐
│ What do you need to calculate?     │
└─────────────────────────────────────┘
           │
           ├─ Compare to previous/next row?
           │  └─> Use: lag() or lead()
           │      Examples:
           │      - Spike detection (current vs previous)
           │      - Rate of change (delta between buckets)
           │      - Consecutive violations (check last N via multiple lags)
           │
           ├─ Assign rankings or row numbers?
           │  └─> Use: row_number(), rank(), or dense_rank()
           │      Choose based on tie handling:
           │      - Unique IDs → row_number()
           │      - Olympic ranking (gaps after ties) → rank()
           │      - Continuous numbering (no gaps) → dense_rank()
           │
           ├─ Calculate over time window?
           │  └─> Use: avg/sum/min/max + frame(back:duration)
           │      Examples:
           │      - Moving average baseline
           │      - Rolling sum (hourly totals)
           │      - Smoothing spiky metrics
           │
           └─ Get first/last value in window?
              └─> Use: first() or last()
                  - Entire partition: omit frame()
                  - Sliding window: use frame(back:duration)
                  Examples:
                  - Compare to start of day (first in 24h window)
                  - Detect if returned to baseline
```

---

## Performance Considerations

### Window Function Performance

**Fast** ✅:
- `lag()` and `lead()` with single offset
- `row_number()`, `rank()`, `dense_rank()` within small partitions
- Time-based frames with reasonable durations (<1h)

**Slower** ⚠️:
- Large partitions (millions of rows per service)
- Very long time windows (`back:30d` over large datasets)
- Multiple window functions in single query

**Optimization Tips**:

1. **Filter Before Windowing**:
```opal
# GOOD: Filter first, then window
filter service_name = "frontend"
| make_col prev:window(lag(rate, 1), group_by(service_name))

# SLOW: Window on all services, then filter
make_col prev:window(lag(rate, 1), group_by(service_name))
| filter service_name = "frontend"
```

2. **Use Appropriate Frame Duration**:
```opal
# GOOD: 30m for 5m buckets = ~6 rows
frame(back:30m)

# SLOW: 24h for 5m buckets = ~288 rows
frame(back:24h)
```

3. **Limit Output Early**:
```opal
# GOOD: Filter anomalies first
filter pct_change > 100
| limit 100

# SLOW: Calculate all, limit at end
make_col pct_change:...
| limit 100
```

---

## Common Mistakes and Fixes

### Mistake 1: Using SQL OVER Syntax

**❌ WRONG**:
```opal
make_col prev:lag(rate, 1) over (partition by service_name)
```

**Error**: `Unknown function 'over()'`

**✅ FIX**:
```opal
make_col prev:window(lag(rate, 1), group_by(service_name))
```

---

### Mistake 2: Forgetting group_by()

**❌ WRONG**:
```opal
make_col prev:window(lag(rate, 1))
```

**Error**: Undefined behavior or incorrect partitioning

**✅ FIX**:
```opal
# Partition by service
make_col prev:window(lag(rate, 1), group_by(service_name))

# Single partition (all rows together)
make_col prev:window(lag(rate, 1), group_by())
```

---

### Mistake 3: Expecting Cumulative Sum

**❌ WRONG EXPECTATION**:
```opal
window(sum(value), order_by(time))  # Expecting running total
```

**Reality**: Returns total sum of entire partition for ALL rows.

**✅ WORKAROUND**:
```opal
# Use moving sum instead (not cumulative, but windowed)
window(sum(value), group_by(service), order_by(time), frame(back:1h))
```

---

### Mistake 4: Using Row-Based Frame Syntax

**❌ WRONG**:
```opal
frame(rows: 3 preceding)              # No rows parameter
frame(between: 3 preceding and current)  # No SQL syntax
```

**✅ FIX**:
```opal
frame(back:15m)  # Time-based only
```

---

## Cross-References

**Related Skills**:
- **detecting-anomalies** - Uses lag() for rate-of-change detection
- **aggregating-gauge-metrics** - Metrics aggregation before windowing
- **time-series-analysis** - Temporal analysis with timechart
- **subquery-patterns-and-union** - Advanced multi-stage calculations

**Common Workflows**:
1. **Spike Detection**: aggregating-gauge-metrics → window-functions (lag) → detecting-anomalies
2. **Top-N Dashboards**: aggregating-gauge-metrics → window-functions (rank) → filtering
3. **Baseline Comparison**: aggregating-gauge-metrics → window-functions (frame) → anomaly filtering
4. **Trend Analysis**: time-series-analysis → window-functions (moving avg) → visualization

---

## Examples Summary

### Example 1: Rate of Change Detection
**Use Case**: Find services with >100% request rate increase

```opal
align 5m, rate:sum(m("span_call_count_5m"))
| make_col prev:window(lag(rate, 1), group_by(service_name))
| make_col pct_change:if(prev > 0, (rate - prev) / prev * 100, 0)
| filter pct_change > 100
```

---

### Example 2: Top 10 Services Per Time Bucket
**Use Case**: Busiest services in each 5-minute window

```opal
align 5m, rate:sum(m("span_call_count_5m"))
| make_col rank:window(rank(), group_by(_c_bucket), order_by(desc(rate)))
| filter rank <= 10
```

---

### Example 3: Anomaly Detection with Moving Baseline
**Use Case**: Alert when current exceeds 30m average by 50%

```opal
align 5m, rate:sum(m("span_call_count_5m"))
| make_col baseline:window(avg(rate), group_by(service_name), order_by(asc(valid_from)), frame(back:30m))
| make_col anomaly:if(rate > baseline * 1.5, true, false)
| filter anomaly = true
```

---

### Example 4: Smoothed Metric for Dashboards
**Use Case**: 15-minute moving average for charts

```opal
align 1m, latency:percentile(duration_ms, 0.95)
| make_col smooth_p95:window(avg(latency), group_by(service_name), order_by(asc(valid_from)), frame(back:15m))
| pick_col valid_from, valid_to, service_name, smooth_p95
```

---

### Example 5: Detect Sustained Violations
**Use Case**: Alert if SLO violated for 3+ consecutive buckets

```opal
align 5m, p95:percentile(duration_ms, 0.95)
| make_col prev1:window(lag(p95, 1), group_by(service_name))
| make_col prev2:window(lag(p95, 2), group_by(service_name))
| make_col sustained:if(p95 > 500 and prev1 > 500 and prev2 > 500, true, false)
| filter sustained = true
```

---

## Quick Syntax Reference Card

| Function | Basic Syntax | With Frame |
|----------|--------------|------------|
| **lag** | `window(lag(col, 1), group_by(dim))` | N/A |
| **lead** | `window(lead(col, 1), group_by(dim))` | N/A |
| **row_number** | `window(row_number(), group_by(dim), order_by(col))` | N/A |
| **rank** | `window(rank(), group_by(dim), order_by(col))` | N/A |
| **dense_rank** | `window(dense_rank(), group_by(dim), order_by(col))` | N/A |
| **avg** | `window(avg(col), group_by(dim))` | `window(avg(col), group_by(dim), order_by(time), frame(back:30m))` |
| **sum** | `window(sum(col), group_by(dim))` | `window(sum(col), group_by(dim), order_by(time), frame(back:1h))` |
| **first** | `window(first(col), group_by(dim), order_by(time))` | `window(first(col), group_by(dim), order_by(time), frame(back:24h))` |
| **last** | `window(last(col), group_by(dim), order_by(time))` | `window(last(col), group_by(dim), order_by(time), frame(back:24h))` |

**Remember**: ALWAYS use `window()` wrapper. NEVER use SQL `OVER` clause.
