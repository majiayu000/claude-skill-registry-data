---
name: working-with-intervals
description: Work with Interval datasets (time-bounded data) using OPAL. Use when analyzing data with start and end timestamps like distributed traces, batch jobs, or CI/CD pipeline runs. Covers duration calculations, temporal filtering, and aggregating by time properties. Intervals are immutable completed activities with two timestamps, distinct from Events (single timestamp) and Resources (mutable state).
---

# Working with Intervals

Interval datasets represent time-bounded, immutable activities with start and end timestamps. This skill teaches the core patterns for working with any interval data in OPAL.

## When to Use This Skill

- Working with data that has both start_time and end_time fields
- Calculating and analyzing durations (how long things took)
- Filtering by temporal properties (when something started, ended, or its duration)
- Understanding the difference between Intervals, Events, and Resources
- Querying any time-bounded activity data

## Prerequisites

- Access to Observe tenant via MCP
- Understanding that Intervals have TWO timestamps: usually `start_time` and `end_time`
- Dataset with Interval type (check via `discover_context()`)

## Key Concepts

### What Are Interval Datasets?

**Interval datasets** represent completed activities with defined start and end points:

**Temporal Structure**: Two timestamps
- `start_time`, `ValidFrom`, `eventStart`, etc - When the activity began
- `end_time`, `ValidTo`, `eventEnd`, etc - When the activity ended

**Mutability**: Immutable once ended
- Once an interval ends, it never changes
- Represents a completed activity

**Common Examples**:
- Distributed trace spans (HTTP requests, database queries, RPC calls)
- Batch job runs (ETL jobs, data processing tasks)
- CI/CD pipeline executions (build steps, deployment stages)
- Process lifetimes (container start to stop)

### Dataset Type Comparison

| Type | Timestamps | Mutability | Example |
|------|-----------|------------|---------|
| **Event** | Single (`timestamp`) | Immutable | Log entry, audit event |
| **Interval** | Two (`start_time`, `end_time`) | Immutable | Span, batch job, session |
| **Resource** | Two (`Valid From`, `Valid To`) | Mutable | K8s pod, service state |

**Critical distinction**:
- Intervals = completed activities that happened (immutable)
- Resources = evolving entity state (mutable, receives updates)

### Duration in OPAL

OPAL stores durations as a `duration` type (internally nanoseconds).

**Duration unit conversions**:
```opal
duration / 1ms    # Convert to milliseconds
duration / 1s     # Convert to seconds
duration / 1m     # Convert to minutes
duration / 1h     # Convert to hours
```

**No manual math needed** - OPAL handles the conversion.

## Discovery Workflow

**Step 1: Find interval datasets**
```
discover_context("span trace")      # For distributed traces
discover_context("batch job")       # For batch processing
discover_context("pipeline run")    # For CI/CD data
```

**Step 2: Get detailed schema**
```
discover_context(dataset_id="YOUR_DATASET_ID")
```

**Step 3: Verify interval structure**
Look for:
- `start_time` field
- `end_time` field
- `duration` field (usually present)
- Descriptive fields for grouping

## Basic Patterns

### Pattern 1: Calculate Duration Statistics

Get overall duration statistics:

```opal
make_col dur_ms:duration / 1ms
| statsby count:count(),
          avg_dur:avg(dur_ms),
          min_dur:min(dur_ms),
          max_dur:max(dur_ms)
```

**Output**: Single row with duration statistics in milliseconds.

### Pattern 2: Duration Percentiles

Understand duration distribution:

```opal
make_col dur_sec:duration / 1s
| statsby count:count(),
          p50:percentile(dur_sec, 0.50),
          p95:percentile(dur_sec, 0.95),
          p99:percentile(dur_sec, 0.99)
```

**Output**: Percentiles show distribution better than averages.

**Why percentiles**: Less affected by outliers, align with SLO definitions.

### Pattern 3: Filter by Duration

Find long-running activities:

```opal
make_col dur_min:duration / 1m
| filter dur_min > 5
| statsby long_running:count()
```

**Output**: Count of intervals exceeding 5 minutes.

### Pattern 4: Group by Duration Range

Categorize intervals by duration:

```opal
make_col dur_ms:duration / 1ms
| make_col category:if(dur_ms < 100, "fast",
                      if(dur_ms < 1000, "medium", "slow"))
| statsby count:count(), group_by(category)
```

**Output**: Count in each duration category.

**Note**: Must use separate `make_col` statements - can't reference newly created column in same statement.

### Pattern 5: Aggregate by Grouping Field

Compare durations across categories:

```opal
make_col dur_sec:duration / 1s
| statsby count:count(),
          avg:avg(dur_sec),
          p95:percentile(dur_sec, 0.95),
          group_by(service_name)
| sort desc(p95)
| limit 10
```

**Output**: Duration metrics per service, sorted by p95.

**Portable note**: Replace `service_name` with your dataset's grouping field.

## Common Use Cases

### Finding Slowest Individual Intervals

```opal
make_col dur_sec:duration / 1s
| sort desc(dur_sec)
| limit 20
```

**Use case**: Identify specific slow instances for investigation.

### Duration Distribution Analysis

```opal
make_col dur_ms:duration / 1ms
| statsby count:count(),
          p50:percentile(dur_ms, 0.50),
          p75:percentile(dur_ms, 0.75),
          p90:percentile(dur_ms, 0.90),
          p95:percentile(dur_ms, 0.95),
          p99:percentile(dur_ms, 0.99)
```

**Use case**: Understand full duration distribution for SLO analysis.

### Filtering by Temporal Window

Find intervals that started in a specific time range (use MCP tool call time range)

```opal
make_col dur_min:duration / 1m
| statsby count:count(), avg_dur:avg(dur_min)
```

**Use case**: Analyze intervals from specific time period (incident investigation).

### Combining Duration and Other Filters

```opal
make_col dur_sec:duration / 1s
| filter dur_sec > 10
| filter environment = "production"
| statsby count:count(), group_by(job_type)
```

**Use case**: Complex filtering by duration AND attributes.

## Complete Example

**Scenario**: You have CI/CD pipeline run data and want to identify slow build stages.

**Step 1: Discover dataset**
```
discover_context("pipeline build")
```

Found dataset ID: `12345678` with fields:
- `start_time`, `end_time`, `duration`
- `stage_name` (build, test, deploy)
- `pipeline_id`

**Step 2: Analyze stage durations**
```opal
make_col dur_min:duration / 1m
| statsby run_count:count(),
          avg_min:avg(dur_min),
          p95_min:percentile(dur_min, 0.95),
          max_min:max(dur_min),
          group_by(stage_name)
| sort desc(p95_min)
```

**Step 3: Interpret results**

| stage_name | run_count | avg_min | p95_min | max_min |
|------------|-----------|---------|---------|---------|
| build | 150 | 3.2 | 5.8 | 12.3 |
| test | 150 | 8.5 | 15.2 | 22.1 |
| deploy | 150 | 2.1 | 3.5 | 6.8 |

**Insight**: Test stage has highest p95 (15.2 min) and should be optimized.

## Common Pitfalls

### Pitfall 1: Referencing Column in Same make_col

❌ **Wrong**:
```opal
make_col dur_ms:duration / 1ms,
         is_slow:if(dur_ms > 1000, 1, 0)
```

✅ **Correct**:
```opal
make_col dur_ms:duration / 1ms
| make_col is_slow:if(dur_ms > 1000, 1, 0)
```

**Why**: OPAL processes columns in order - can't reference column being created in same statement.

### Pitfall 2: Using Averages Instead of Percentiles

❌ **Wrong** (for duration analysis):
```opal
statsby avg_dur:avg(duration / 1s)
```

✅ **Correct**:
```opal
make_col dur_sec:duration / 1s
| statsby p50:percentile(dur_sec, 0.50),
          p95:percentile(dur_sec, 0.95),
          p99:percentile(dur_sec, 0.99)
```

**Why**: Averages are skewed by outliers. Percentiles show true distribution.

### Pitfall 3: Confusing Intervals with Events

❌ **Wrong assumption**:
```
Intervals have a single timestamp field
```

✅ **Correct understanding**:
```
Intervals always have start_time AND end_time (two timestamps)
Events have a single timestamp
```

**Why**: Different dataset types have different temporal structures.

### Pitfall 4: Confusing Intervals with Resources

❌ **Wrong assumption**:
```
Intervals track state changes over time
```

✅ **Correct understanding**:
```
Intervals = immutable completed activities
Resources = mutable state tracking
```

**Why**: Once an interval ends, it never changes. Resources receive updates and track evolving state.

## Duration Unit Reference

Common duration conversions:

```opal
make_col dur_ms:duration / 1ms     # Milliseconds
make_col dur_sec:duration / 1s     # Seconds
make_col dur_min:duration / 1m     # Minutes
make_col dur_hr:duration / 1h      # Hours
```

You can also combine units:
```opal
make_col dur_mins:duration / 1m
| filter dur_mins > 30              # Over 30 minutes
```

## Best Practices

1. **Convert duration** for human readability
2. **Use percentiles not averages** for duration analysis
3. **Separate make_col statements** when referencing derived columns
4. **Choose appropriate time units** (ms for fast operations, min/hr for long-running)
5. **Filter by duration thresholds** to focus on interesting cases
6. **Include count** in aggregations to understand volume
7. **Sort by meaningful metrics** (p95, p99) in addition to averages
8. **Use limit or topk** to avoid overwhelming results

## Related Skills

- **filtering-event-datasets** - For single-timestamp log data (Events)
- **aggregating-event-datasets** - For summarizing event data with statsby
- **time-series-analysis** - For trending intervals over time with timechart
- **working-with-resources** - For mutable state tracking (Resources)

## Summary

Intervals represent time-bounded, immutable activities:
- **Two timestamps**: start_time and end_time
- **Duration field**: Automatically calculated
- **Immutable**: Once ended, never change
- **Core operation**: Convert duration using `/ 1ms`, `/ 1s`, `/ 1m`, `/ 1h`
- **Analysis**: Use percentiles (p50, p95, p99) for distribution understanding

**Key distinction**: Intervals are completed activities (happened once, done), not evolving state (Resources) or point-in-time occurrences (Events).

---
**Last Updated**: November 14, 2025
**Version**: 2.0
**Tested With**: Observe OPAL (OpenTelemetry Span dataset)
