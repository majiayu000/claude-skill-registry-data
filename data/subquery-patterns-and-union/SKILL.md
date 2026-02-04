---
name: subquery-patterns-and-union
description: Use OPAL subquery syntax (@labels) and union operations to combine multiple datasets or time periods. Essential for period-over-period comparisons, multi-dataset analysis, and complex data transformations. Covers @label <- @ syntax, timeshift for temporal shifts, union for combining results, and any_not_null() for collapsing grouped data.
---

# Subquery Patterns and Union Operations

## Overview

OPAL subqueries using `@label` syntax enable powerful multi-dataset and multi-period analysis. This skill covers:
- Subquery syntax with `@label <- @dataset`
- Union operations to combine multiple result sets
- Timeshift for period-over-period comparisons
- Best practices for complex data transformations

## When to Use This Skill

Use subqueries and union when you need to:
- **Period-over-period comparison**: Compare current vs previous hour/day/week (metrics or events)
- **Time-series comparison**: Chart trends over time with period-over-period data
- **Complex transformations**: Build intermediate results for multi-stage calculations (e.g., SLO tracking, error budgets)

## Core Concepts

### Subquery Syntax

```opal
# Basic pattern
@label <- @dataset_reference {
    # OPAL pipeline
}

# Reference primary input
@current <- @ {
    # Process primary dataset
}

# Reference named dataset (requires dataset_aliases parameter)
@other <- @dataset_name {
    # Process other dataset
}

# Use subquery results
<- @label {
    # Continue processing
}
```

**Key Points**:
- `@` alone references the primary input dataset
- `@dataset_name` references a named dataset via aliases
- `@label` creates a reusable intermediate result
- `<- @label` continues the pipeline from that subquery

### Union Operation

Union combines multiple result sets with matching columns:

```opal
@set_a <- @ {
    # First result set
}

@set_b <- @ {
    # Second result set with same column structure
}

<- @set_a {
    union @set_b
    # Combined results
}
```

**Important**:
- Union requires matching column names
- Rows from both sources appear in output
- Use `any_not_null()` to collapse sparse union results
- Union happens AFTER aggregation, not before

### Timeshift Verb

Timeshift moves row timestamps forward (positive) or backward (negative):

```opal
timeshift 1h          # Move 1 hour forward
timeshift -1d         # Move 1 day backward
timeshift 30m         # Move 30 minutes forward
```

**Critical Rule**: Apply timeshift BEFORE align when working with metrics!

```opal
# CORRECT
timeshift 1h
align rate:sum(m("metric"))

# WRONG
align rate:sum(m("metric"))
timeshift 1h  # Too late! Align already processed time buckets
```

## Pattern 1: Period-Over-Period Comparison (Metrics)

**Use Case**: Compare current metrics to previous period (hour, day, week)

**Strategy**:
1. Create `@current` subquery with current period aggregation
2. Create `@previous` subquery with timeshift + same aggregation
3. Union both, then collapse with `any_not_null()`
4. Calculate change and percentage change

### Example: Compare Current Hour vs Previous Hour

```opal
# Current period (last 1h)
@current <- @ {
    align rate:sum(m("span_call_count_5m"))
    aggregate current_sum:sum(rate), group_by(service_name)
}

# Previous period (1h before that)
@previous <- @ {
    timeshift 1h                        # Shift BEFORE align!
    align rate:sum(m("span_call_count_5m"))
    aggregate prev_sum:sum(rate), group_by(service_name)
}

# Combine both periods
@combined <- @current {
    union @previous
    aggregate current:any_not_null(current_sum),
              previous:any_not_null(prev_sum),
              group_by(service_name)
}

# Calculate changes
<- @combined {
    make_col change:current - previous
    make_col pct_change:if(previous > 0, (change / previous) * 100, 0)
    make_col abs_pct_change:if(pct_change < 0, -pct_change, pct_change)
    filter abs_pct_change > 50          # Show only significant changes
    sort desc(abs_pct_change)
}
```

**Why This Works**:
- `timeshift 1h` moves the "previous" data timestamps forward by 1 hour
- When combined with current data, both align to same time buckets
- `any_not_null()` picks the non-null value from each period
- Result: side-by-side comparison in same row

**Sample Output**:
```
service_name        current  previous  change    pct_change
frontend-service    45000    15000     30000     200.0
checkout-api        8000     15000     -7000     -46.7
payment-service     500      10000     -9500     -95.0
```

### Day-Over-Day Comparison

```opal
@today <- @ {
    align rate:sum(m("span_call_count_5m"))
    aggregate today_sum:sum(rate), group_by(service_name)
}

@yesterday <- @ {
    timeshift 1d                        # 24 hours
    align rate:sum(m("span_call_count_5m"))
    aggregate yesterday_sum:sum(rate), group_by(service_name)
}

@combined <- @today {
    union @yesterday
    aggregate today:any_not_null(today_sum),
              yesterday:any_not_null(yesterday_sum),
              group_by(service_name)
}

<- @combined {
    make_col change:today - yesterday
    make_col pct_change:if(yesterday > 0, (change / yesterday) * 100, 0)
    sort desc(pct_change)
}
```

### Week-Over-Week Comparison

```opal
@this_week <- @ {
    align 1h, rate:sum(m("span_call_count_5m"))
    aggregate week_sum:sum(rate), group_by(service_name)
}

@last_week <- @ {
    timeshift 7d                        # One week
    align 1h, rate:sum(m("span_call_count_5m"))
    aggregate last_week_sum:sum(rate), group_by(service_name)
}

@combined <- @this_week {
    union @last_week
    aggregate this_week:any_not_null(week_sum),
              last_week:any_not_null(last_week_sum),
              group_by(service_name)
}

<- @combined {
    make_col growth:this_week - last_week
    make_col growth_pct:if(last_week > 0, (growth / last_week) * 100, 0)
    sort desc(growth_pct)
}
```

## Pattern 2: Period-Over-Period Comparison (Events/Intervals)

**Use Case**: Compare raw event/span counts across time periods

**Strategy**: Same union pattern, but use `statsby` instead of `align` + `aggregate`

### Example: Error Count This Hour vs Last Hour

```opal
@current <- @ {
    filter error = true
    statsby current_errors:count(), group_by(service_name)
}

@previous <- @ {
    timeshift 1h
    filter error = true
    statsby prev_errors:count(), group_by(service_name)
}

@combined <- @current {
    union @previous
    aggregate current:any_not_null(current_errors),
              previous:any_not_null(prev_errors),
              group_by(service_name)
}

<- @combined {
    make_col error_change:current - previous
    make_col pct_change:if(previous > 0, (error_change / previous) * 100, 0)
    filter current > 10                 # Only services with significant errors
    sort desc(current)
}
```

**Key Difference**: Use `statsby` for event datasets, `align` + `aggregate` for metrics.

## Pattern 3: Time-Series Period Comparison

**Use Case**: Chart current vs previous period trends over time

### Example: Current vs Previous Week (Hourly Buckets)

```opal
@current <- @ {
    align 1h, rate:sum(m("span_call_count_5m"))
    aggregate current_rate:sum(rate), group_by(service_name)
}

@previous <- @ {
    timeshift 7d
    align 1h, rate:sum(m("span_call_count_5m"))
    aggregate prev_rate:sum(rate), group_by(service_name)
}

@combined <- @current {
    union @previous
    aggregate current:any_not_null(current_rate),
              previous:any_not_null(prev_rate),
              group_by(service_name, _c_bucket)
}

<- @combined {
    make_col change:current - previous
    make_col pct_change:if(previous > 0, (change / previous) * 100, 0)
}
```

**Output**: Time-series with both periods aligned by bucket, suitable for line charts showing trends over time.

**Note**: This pattern returns multiple rows per service (one per time bucket). For summary comparisons, use Pattern 1 instead.

## Pattern 4: Building Intermediate Results

**Use Case**: Complex calculations requiring multiple steps

### Example: Calculate Error Budget Consumption

```opal
# Step 1: Get total requests and errors
@base <- @ {
    align options(bins: 1), rate:sum(m("span_call_count_5m")),
                             errors:sum(m("span_error_count_5m"))
    aggregate total_requests:sum(rate),
              total_errors:sum(errors),
              group_by(service_name)
}

# Step 2: Calculate SLO metrics
@slo <- @base {
    make_col error_rate:if(total_requests > 0, total_errors / total_requests, 0)
    make_col success_rate:1 - error_rate
    make_col slo_target:0.999           # 99.9% SLO
    make_col error_budget:1 - slo_target
}

# Step 3: Calculate budget consumption
<- @slo {
    make_col budget_consumed:if(error_budget > 0, error_rate / error_budget, 0)
    make_col budget_remaining:1 - budget_consumed
    make_col status:if(budget_consumed > 1, "VIOLATED",
                    if(budget_consumed > 0.8, "WARNING", "HEALTHY"))
    filter total_requests > 1000        # Only services with traffic
    sort desc(budget_consumed)
}
```

**Sample Output**:
```
service_name     total_requests  error_rate  budget_consumed  status
adservice        870             0.0276      27.6             VIOLATED
cartservice      2303            0.0091      9.1              VIOLATED
frontend         15108           0.0016      1.6              VIOLATED
productcatalog   8838            0.0000      0.0              HEALTHY
```

**Why This Works**:
- `@base` subquery aggregates raw metrics (requests + errors)
- `@slo` subquery builds on `@base`, adding calculated SLO fields
- Final stage uses `@slo` results to compute budget status
- Each stage can reference all columns from previous stages

## Understanding any_not_null()

The `any_not_null()` function is crucial for union patterns:

```opal
# After union, you typically have sparse data:
# Row 1: current_sum=100, prev_sum=null
# Row 2: current_sum=null, prev_sum=80

aggregate current:any_not_null(current_sum),
          previous:any_not_null(prev_sum),
          group_by(service_name)

# Result:
# Row 1: current=100, previous=80
```

**How it works**:
- Groups by service_name (or other dimensions)
- For each group, finds any non-null value across all union rows
- Collapses sparse union into single row per group

**Alternative functions**:
- `any()` - Picks arbitrary value (may be null)
- `min()` / `max()` - Numeric min/max (only for numbers)
- `any_not_null()` - Best for union collapse (picks any non-null)

## Common Patterns Summary

| Use Case | Subqueries Needed | Key Verbs |
|----------|-------------------|-----------|
| Period-over-period (metrics) | 2+ | `timeshift`, `align`, `union`, `any_not_null()` |
| Period-over-period (events) | 2+ | `timeshift`, `statsby`, `union`, `any_not_null()` |
| Time-series comparison | 2+ | `timeshift`, `align`, `union`, `any_not_null()`, `group_by(_c_bucket)` |
| Complex calculations | 1-3 | `make_col`, pipeline stages |

**Note**: For A/B comparisons across different filter conditions, use conditional columns with `if()` statements instead of subqueries. For multi-dataset joins, use `lookup` or `join` verbs (see **working-with-resources** skill).

## Troubleshooting

### Issue: "Columns don't match in union"

**Cause**: Union requires exact column name matches

**Solution**: Ensure both subqueries produce same column names

```opal
# WRONG - column names don't match
@a <- @ { aggregate count_a:count() }
@b <- @ { aggregate count_b:count() }
<- @a { union @b }  # Error!

# CORRECT - same column names
@a <- @ { aggregate cnt:count() }
@b <- @ { aggregate cnt:count() }
<- @a { union @b }  # Works!
```

### Issue: "All nulls after any_not_null()"

**Cause**: group_by dimensions don't align across union sources

**Solution**: Verify both subqueries group by same dimensions

```opal
# WRONG - different group_by
@a <- @ { aggregate cnt:count(), group_by(service_name) }
@b <- @ { aggregate cnt:count(), group_by(namespace) }
<- @a { union @b; aggregate total:any_not_null(cnt), group_by(service_name) }
# Result: Nulls (no matching groups)

# CORRECT - same group_by
@a <- @ { aggregate cnt:count(), group_by(service_name) }
@b <- @ { aggregate cnt:count(), group_by(service_name) }
<- @a { union @b; aggregate total:any_not_null(cnt), group_by(service_name) }
```

### Issue: "Timeshift has no effect"

**Cause**: Timeshift applied AFTER align (too late!)

**Solution**: Always timeshift BEFORE align

```opal
# WRONG - timeshift after align
@previous <- @ {
    align rate:sum(m("metric"))
    timeshift 1h                # Too late!
}

# CORRECT - timeshift before align
@previous <- @ {
    timeshift 1h                # First!
    align rate:sum(m("metric"))
}
```

### Issue: "Can't reference @label"

**Cause**: Trying to use label before it's defined

**Solution**: Define subquery first, then reference it

```opal
# WRONG - @combined used before definition
<- @combined { ... }
@combined <- @ { ... }

# CORRECT - define first
@combined <- @ { ... }
<- @combined { ... }
```

## Performance Considerations

### When to Use Subqueries vs Single Query

**Use subqueries when**:
- Period-over-period comparison (timeshift required)
- Building complex intermediate results
- Readability improves significantly

**Avoid subqueries when**:
- Simple A/B comparison (use conditional columns)
- Single metric aggregation
- Performance is critical (subqueries add overhead)

### Optimization Tips

1. **Filter early**: Apply filters in subqueries, not after union
   ```opal
   # GOOD
   @current <- @ {
       filter service_name = "frontend"  # Filter early
       align rate:sum(m("metric"))
   }

   # BAD
   @current <- @ {
       align rate:sum(m("metric"))
   }
   <- @current {
       filter service_name = "frontend"  # Filter late (processes all services)
   }
   ```

2. **Use options(bins: 1) for summaries**: Reduces data volume in union
   ```opal
   @current <- @ {
       align options(bins: 1), rate:sum(m("metric"))  # Single row per service
       aggregate total:sum(rate), group_by(service_name)
   }
   ```

3. **Limit union sources**: Each union source adds processing cost

## Comparison: Subquery Union vs Window Functions

Both can solve period-over-period comparison, but have different tradeoffs:

| Aspect | Subquery + Union | Window(lag) |
|--------|------------------|-------------|
| **Syntax** | More verbose | More concise |
| **Flexibility** | Can compare any time periods | Limited to adjacent rows |
| **Performance** | Processes data twice | Single pass |
| **Time buckets** | Aligns arbitrary periods | Only sequential buckets |
| **Use case** | Day-over-day, week-over-week | Row-to-row change detection |

**Example: Hour-over-hour rate of change**

```opal
# Window approach (simpler for sequential buckets)
align 1h, rate:sum(m("span_call_count_5m"))
| make_col prev_rate:window(lag(rate, 1), group_by(service_name))
| make_col change:rate - prev_rate
| make_col pct:if(prev_rate > 0, (change / prev_rate) * 100, 0)

# Union approach (more flexible, can compare any offset)
@current <- @ {
    align 1h, rate:sum(m("span_call_count_5m"))
    aggregate current:sum(rate), group_by(service_name)
}
@previous <- @ {
    timeshift 1h
    align 1h, rate:sum(m("span_call_count_5m"))
    aggregate prev:sum(rate), group_by(service_name)
}
@combined <- @current {
    union @previous
    aggregate current:any_not_null(current), prev:any_not_null(prev), group_by(service_name)
}
<- @combined {
    make_col change:current - prev
    make_col pct:if(prev > 0, (change / prev) * 100, 0)
}
```

**Recommendation**:
- Use **window(lag)** for simple sequential comparisons (previous hour, previous bucket)
- Use **union + timeshift** for arbitrary period comparisons (same hour yesterday, last week)

## Related Skills

- **window-functions-deep-dive** - Covers window(lag/lead/avg) patterns
- **detecting-anomalies** - Uses both union and window patterns
- **aggregating-gauge-metrics** - Foundation for metric aggregation
- **time-series-analysis** - Time bucketing with timechart

## Key Takeaways

1. **Subquery syntax**: `@label <- @dataset { pipeline }`
2. **Union combines**: Same schema, different filters/time periods
3. **Timeshift before align**: Critical for metric comparisons
4. **any_not_null()**: Collapses sparse union results
5. **Not always best**: Consider conditional columns for simple A/B tests
6. **Performance matters**: Union processes data multiple times

When in doubt about subquery syntax or complex union patterns, use `learn_observe_skill("OPAL subquery")` for official documentation.
