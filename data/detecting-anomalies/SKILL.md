---
name: detecting-anomalies
description: Detect anomalies in metrics and time-series data using OPAL statistical methods. Use when you need to identify unusual patterns, spikes, drops, or outliers in observability data. Covers statistical outlier detection (Z-score, IQR), threshold-based alerts, rate-of-change detection with window functions, and moving average baselines. Choose pattern based on data distribution and anomaly type.
---

# Detecting Anomalies

Detect anomalies in metrics and time-series data using OPAL statistical methods. This skill covers multiple detection patterns for different types of anomalies: statistical outliers, sudden spikes/drops, threshold violations, and deviations from moving baselines.

Use when you need to:
- Identify unusual spikes or drops in request volume, errors, latency
- Detect values exceeding normal statistical bounds
- Alert on sudden percentage changes (traffic doubling, sudden drops)
- Compare current values to moving averages
- Find outliers in skewed distributions

## Key Concepts

### Anomaly Detection Approaches

**Statistical Methods** (good for gradual changes):
- Z-Score (standard deviation) - Assumes normal distribution
- IQR (Interquartile Range) - Robust to skewed data
- Percentile thresholds - Compare to historical baseline

**Temporal Methods** (good for sudden changes):
- Rate of change - Detect sudden spikes/drops
- Moving average deviation - Compare to recent baseline

**Threshold Methods** (simple and interpretable):
- Static thresholds - Known limits (CPU > 90%)
- Dynamic thresholds - Calculated from baseline (current > avg * 1.5)

### When to Use Each Pattern

```
What type of anomaly?
├─ Known threshold (e.g., "CPU > 90%")
│  └─> Threshold-Based Detection (Pattern 3)
│
├─ Statistical outliers (unusual values)
│  ├─ Normal distribution?
│  │  └─> Z-Score Method (Pattern 1)
│  │
│  └─ Skewed distribution?
│     └─> IQR Method (Pattern 2)
│
├─ Sudden spikes/drops
│  └─> Rate of Change (Pattern 4)
│
└─ Deviation from recent baseline
   └─> Moving Average (Pattern 5)
```

## Pattern 1: Statistical Outlier Detection (Z-Score)

**Concept**: Detect values beyond N standard deviations from the mean

**When to use**:
- Metrics with relatively stable baseline
- Data roughly follows normal distribution
- Need statistically grounded detection

**Query**:
```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| aggregate avg_val:avg(metric_value),
          stddev_val:stddev(metric_value),
          current_val:sum(metric_value),
          group_by(service_name)
| make_col z_score:(current_val - avg_val) / stddev_val
| make_col upper_bound:avg_val + (2 * stddev_val)
| make_col lower_bound:avg_val - (2 * stddev_val)
| make_col is_anomaly:if(z_score > 2 or z_score < -2, true, false)
| filter is_anomaly = true
| sort desc(z_score)
| limit 20
```

**Threshold tuning**:
- `z > 2` or `z < -2`: ~95% confidence (moderate sensitivity)
- `z > 3` or `z < -3`: ~99.7% confidence (low false positives)
- `z > 1.5` or `z < -1.5`: ~87% confidence (high sensitivity)

**Example result**:
```
service_name: featureflagservice
avg_val: 11.5
stddev_val: 13.9
current_val: 46
z_score: 2.48
is_anomaly: true
```

**Pros**:
- Statistically grounded
- Well-understood confidence intervals
- Good for normally distributed data

**Cons**:
- Assumes normal distribution
- Sensitive to extreme outliers in baseline
- Requires sufficient historical data

## Pattern 2: IQR (Interquartile Range) Method

**Concept**: Detect values beyond the interquartile range using Tukey's fences

**When to use**:
- Skewed distributions (latency, error counts)
- Presence of natural outliers in baseline
- More robust alternative to Z-score

**Query**:
```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| aggregate p25:percentile(metric_value, 0.25),
          p75:percentile(metric_value, 0.75),
          current_val:sum(metric_value),
          group_by(service_name)
| make_col iqr:p75 - p25
| make_col upper_fence:p75 + (1.5 * iqr)
| make_col lower_fence:p25 - (1.5 * iqr)
| make_col is_outlier:if(current_val > upper_fence or current_val < lower_fence, true, false)
| filter is_outlier = true
| sort desc(current_val)
| limit 20
```

**Threshold tuning**:
- `1.5 * IQR`: Standard outliers (moderate sensitivity)
- `3 * IQR`: Extreme outliers (low false positives)
- `1 * IQR`: More sensitive detection

**Example result**:
```
service_name: featureflagservice
p25: 1.75
p75: 16.75
iqr: 15
upper_fence: 39.25
current_val: 46
is_outlier: true
```

**Pros**:
- Robust to skewed distributions
- Not affected by extreme values
- Based on quartiles (median-based)

**Cons**:
- Less interpretable than Z-score
- May miss anomalies in heavy-tailed distributions
- Requires sufficient data for percentile calculation

## Pattern 3: Threshold-Based Detection

**Concept**: Simple comparison against fixed or dynamic thresholds

**When to use**:
- Known capacity limits (CPU > 90%, memory > 80%)
- SLO violations (error rate > 1%, latency > 500ms)
- Business rules (orders < 100 per hour)

**Static Threshold**:
```opal
align options(bins: 1), total_calls:sum(m("span_call_count_5m"))
aggregate current_rate:sum(total_calls), group_by(service_name)
make_col threshold:100000
| make_col is_high:if(current_rate > threshold, true, false)
| filter is_high = true
| sort desc(current_rate)
```

**Dynamic Threshold** (baseline comparison):
```opal
align options(bins: 1), metric_value:sum(m("span_call_count_5m"))
aggregate baseline:avg(metric_value),
          current:sum(metric_value),
          group_by(service_name)
make_col threshold:baseline * 1.5
| make_col is_anomaly:if(current > threshold, true, false)
| filter is_anomaly = true
```

**Threshold multiplier guidance**:
- `1.5x`: High sensitivity (more alerts)
- `2x`: Moderate sensitivity (balanced)
- `3x`: Low sensitivity (only major spikes)

**Pros**:
- Simple and interpretable
- No assumptions about distribution
- Clear business meaning

**Cons**:
- Requires domain knowledge to set thresholds
- Static thresholds may not adapt to changing baselines
- May miss subtle anomalies

## Pattern 4: Rate of Change Detection

**Concept**: Detect sudden spikes or drops by comparing to previous time period

**When to use**:
- Detect sudden traffic spikes or drops
- Identify rapid changes in behavior
- Alert on percentage change thresholds

**Query**:
```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| make_col previous_value:window(lag(metric_value, 1), group_by(service_name))
| make_col value_change:metric_value - previous_value
| make_col pct_change:if(previous_value > 0, (value_change / previous_value) * 100, 0)
| make_col is_spike:if(pct_change > 100 or pct_change < -50, true, false)
| filter is_spike = true
| sort desc(pct_change)
| limit 20
```

**Critical syntax**: Use `window(lag(...), group_by(...))` NOT `lag(...) over (partition by...)`

**Threshold examples**:
- `pct_change > 100`: 2x increase (doubling)
- `pct_change > 200`: 3x increase
- `pct_change < -50`: 50% drop
- `pct_change < -75`: 75% drop

**Example result**:
```
service_name: frontend
metric_value: 50
previous_value: 2
value_change: 48
pct_change: 2400
is_spike: true
```

**Pros**:
- Detects sudden changes regardless of absolute value
- Adapts to current baseline automatically
- Effective for early spike detection

**Cons**:
- Sensitive to very low baseline values (small numbers can cause large percentage changes)
- May produce false positives during normal ramp-up/down
- Requires at least 2 time periods of data

**Best practices**:
- Add minimum value filter to avoid division by small numbers
- Use different thresholds for increases vs decreases
- Consider absolute change threshold in addition to percentage

## Pattern 5: Moving Average Baseline

**Concept**: Compare current value to recent moving average using sliding window

**When to use**:
- Smooth noisy metrics for baseline
- Detect deviations from recent average
- Adaptive baseline that follows trends

**Query**:
```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| make_col moving_avg:window(avg(metric_value), group_by(service_name), frame(back:30m))
| make_col deviation:metric_value - moving_avg
| make_col pct_deviation:if(moving_avg > 0, (deviation / moving_avg) * 100, 0)
| make_col is_anomaly:if(pct_deviation > 50 or pct_deviation < -50, true, false)
| filter is_anomaly = true
| sort desc(pct_deviation)
| limit 20
```

**Frame options**:
- `frame(back:10m)`: Short-term baseline (10-minute average)
- `frame(back:30m)`: Medium-term baseline (30-minute average)
- `frame(back:1h)`: Longer-term baseline (1-hour average)

**Deviation thresholds**:
- `> 50%`: Moderate deviation from recent average
- `> 100%`: Doubling compared to recent average
- `> 25%`: More sensitive detection

**Pros**:
- Adapts to changing baselines and trends
- Smooths noisy data
- Good for metrics with daily/hourly patterns

**Cons**:
- Slower to detect anomalies (due to averaging)
- May miss anomalies during rapid baseline shifts
- Requires sufficient lookback data

**Best practices**:
- Choose frame duration based on metric volatility
- Shorter frames for fast-changing metrics
- Longer frames for more stable baselines

## Pattern 6: Percentile-Based Threshold

**Concept**: Compare current value to historical percentile (p95, p99)

**When to use**:
- SLO violations (latency > p95)
- Detect values above "normal high"
- Comparing current to historical baseline

**Query**:
```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| aggregate p95:percentile(metric_value, 0.95),
          p99:percentile(metric_value, 0.99),
          current:sum(metric_value),
          group_by(service_name)
| make_col is_anomaly:if(current > p95, true, false)
| filter is_anomaly = true
| sort desc(current)
```

**Percentile choices**:
- `p95`: Detect top 5% unusual values (moderate sensitivity)
- `p99`: Detect top 1% extreme values (low false positives)
- `p90`: Detect top 10% (high sensitivity)

**Pros**:
- Percentile-based SLOs are industry standard
- Automatically adapts to data distribution
- Clear meaning (top X% of values)

**Cons**:
- Unidirectional (only detects high values, not drops)
- Requires sufficient historical data
- May not detect subtle shifts in distribution

## Common Patterns

### Pattern: Combine Multiple Detection Methods

Increase confidence by requiring multiple methods to agree:

```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| aggregate avg_val:avg(metric_value),
          stddev_val:stddev(metric_value),
          p95:percentile(metric_value, 0.95),
          current:sum(metric_value),
          group_by(service_name)
| make_col z_score:(current - avg_val) / stddev_val
| make_col is_zscore_anomaly:if(z_score > 2 or z_score < -2, true, false)
| make_col is_percentile_anomaly:if(current > p95, true, false)
| make_col is_anomaly:if(is_zscore_anomaly = true and is_percentile_anomaly = true, true, false)
| filter is_anomaly = true
```

**Use case**: Reduce false positives by requiring consensus

### Pattern: Multi-Metric Correlation

Detect anomalies across correlated metrics:

```opal
align options(bins: 1),
  requests:sum(m("span_call_count_5m")),
  errors:sum(m("span_error_count_5m"))
aggregate total_requests:sum(requests),
          total_errors:sum(errors),
          group_by(service_name)
make_col error_rate:if(total_requests > 0, (float64(total_errors) / float64(total_requests)) * 100, 0)
| make_col threshold:1.0
| make_col is_high_error:if(error_rate > threshold and total_requests > 100, true, false)
| filter is_high_error = true
```

**Use case**: Alert when error rate AND request volume both indicate issues

### Pattern: Time-Series Trending

Track anomalies over time using timechart:

```opal
align 5m, metric_value:sum(m("span_call_count_5m"))
| aggregate avg_val:avg(metric_value),
          stddev_val:stddev(metric_value),
          current:sum(metric_value),
          group_by(service_name)
| make_col z_score:(current - avg_val) / stddev_val
| make_col is_anomaly:if(z_score > 2 or z_score < -2, true, false)
| filter is_anomaly = true
```

**Result**: Multiple rows per service showing anomalies across time buckets

**Use case**: Visualize when and how often anomalies occur

## OPAL Syntax Key Points

### Window Functions (LAG/LEAD)

**CRITICAL**: OPAL uses `window()` function, NOT SQL `OVER` clause!

**✅ CORRECT Syntax**:
```opal
make_col prev:window(lag(column, 1), group_by(dimension))
make_col next:window(lead(column, 1), group_by(dimension))
make_col moving_avg:window(avg(column), group_by(dimension), frame(back:30m))
```

**❌ WRONG Syntax** (SQL-style):
```opal
lag(column, 1) over (partition by dimension order by time)
```

**Window function components**:
- `lag(column, offset)`: Access previous row value
- `lead(column, offset)`: Access next row value
- `group_by(dimension)`: Partition by dimension
- `frame(back:duration)`: Sliding window lookback period

### Derived Columns Must Use Separate make_col

**❌ WRONG** - Cannot reference derived column in same make_col:
```opal
make_col upper_bound:avg + (2 * stddev),
         is_anomaly:if(value > upper_bound, true, false)
```

**✅ CORRECT** - Use separate make_col statements:
```opal
make_col upper_bound:avg + (2 * stddev)
| make_col is_anomaly:if(value > upper_bound, true, false)
```

### Metrics Query Patterns

**Summary (one row per group)**:
```opal
align options(bins: 1), metric:sum(m("metric_name"))
aggregate result:sum(metric), group_by(dimension)
```
**Note**: No pipe `|` between `align options(bins: 1)` and `aggregate`!

**Time-series (multiple rows per group)**:
```opal
align 5m, metric:sum(m("metric_name"))
| aggregate result:sum(metric), group_by(dimension)
```
**Note**: Pipe `|` required between `align 5m` and `aggregate`!

### Period-Over-Period Comparison with Timeshift + Union

For comparing entire periods (e.g., "this hour" vs "exactly 1 hour ago"), use the `timeshift` + `union` pattern with subquery definitions.

**Key Difference**:
- **`window(lag())`**: Compares adjacent buckets (5-min to 5-min, approximate)
- **`timeshift + union`**: Compares entire periods (exact time offset: 1h, 1d, 1w)

**Working Example** (✅ works in all query contexts):
```opal
@current <- @ {
    align rate:sum(m("span_call_count_5m"))
    aggregate current_sum:sum(rate), group_by(service_name)
}
@previous <- @ {
    timeshift 1h                        # Shift BEFORE align!
    align rate:sum(m("span_call_count_5m"))
    aggregate prev_sum:sum(rate), group_by(service_name)
}
@combined <- @current {
    union @previous
    aggregate current:any_not_null(current_sum),
              previous:any_not_null(prev_sum),
              group_by(service_name)
    make_col change:current - previous
    make_col pct_change:if(previous > 0, (change / previous) * 100, 0)
    make_col abs_pct_change:if(pct_change < 0, -pct_change, pct_change)
}
<- @combined {
    filter abs_pct_change > 50
    sort desc(abs_pct_change)
    limit 10
}
```

**Critical Points**:
1. **`@subquery <- @`**: Use `@` alone to reference the primary input dataset
2. **`timeshift` BEFORE `align`**: Operates on raw data, shifts timestamps before aggregation
3. **Separate aggregation**: Both series must be aggregated independently
4. **`any_not_null()` collapses union**: Combines current/previous into single row per dimension
5. **Works everywhere**: MCP queries, worksheets, and monitors all support this syntax

**Use Cases**:
- Day-over-day comparison: "Today vs yesterday" (use `timeshift 1d`)
- Week-over-week trending: "This week vs last week" (use `timeshift 7d`)
- Hour-over-hour spikes: "This hour vs 1 hour ago" (use `timeshift 1h`)
- SLA violations: "Current vs same period last month" (use `timeshift 30d`)

**Tested Results**:
- ✅ Detected 200% increase in service request rate (18 vs 6)
- ✅ Detected 92% drop in request volume (1 vs 13)
- ✅ Works with any timeshift duration (1h, 6h, 1d, 7d, etc.)

**Comparison with window(lag())**:

| Feature | window(lag(rate, N)) | timeshift + union |
|---------|---------------------|-------------------|
| **Time precision** | Approximate (N buckets back) | Exact (fixed time offset) |
| **Example** | `lag(rate, 12)` ≈ 1 hour (if buckets are 5min) | `timeshift 1h` = exactly 60 minutes |
| **Complexity** | Simple, one query | More complex, subqueries + union |
| **Use case** | Real-time spike detection | Period-over-period reporting |
| **Best for** | "Current vs previous bucket" | "Current vs same time yesterday" |

**When to use each**:
- Use `window(lag())` for: Real-time alerts, simple spike detection, fast queries
- Use `timeshift + union` for: Exact period comparison, day-over-day reports, SLA tracking

## Troubleshooting

### Issue: "Unknown function 'over()'"

**Cause**: Using SQL window function syntax instead of OPAL syntax

**Solution**: Use `window(lag(...), group_by(...))` instead of `lag(...) over (...)`

**Example**:
```opal
# WRONG
make_col prev:lag(value, 1) over (partition by service order by time)

# CORRECT
make_col prev:window(lag(value, 1), group_by(service))
```

### Issue: High false positive rate

**Cause**: Threshold too sensitive or baseline includes anomalies

**Solutions**:
1. **Increase threshold**: Use 3-sigma instead of 2-sigma for Z-score
2. **Combine methods**: Require multiple detection methods to agree
3. **Filter baseline**: Exclude known anomaly periods from baseline calculation
4. **Add minimum value filter**: Avoid alerting on very low absolute values

**Example with minimum value filter**:
```opal
| make_col is_spike:if(pct_change > 100 and metric_value > 10, true, false)
```

### Issue: Missing anomalies (false negatives)

**Cause**: Threshold too strict or wrong detection method for data type

**Solutions**:
1. **Decrease threshold**: Use 1.5-sigma or lower percentile (p90 instead of p95)
2. **Try different method**: IQR if data is skewed, rate-of-change for sudden spikes
3. **Check data distribution**: Visualize baseline to understand normal range
4. **Use multiple methods**: Catch different types of anomalies

### Issue: Division by zero or very small numbers

**Cause**: Calculating percentage change when previous value is zero or very small

**Solution**: Add conditional check for minimum denominator:

```opal
make_col pct_change:if(previous_value > 5, (value_change / previous_value) * 100, 0)
```

### Issue: Window function returns null values

**Cause**: First row in group has no previous value for `lag()`

**Solution**: This is expected behavior - first row will have `null` for `lag()`. Filter nulls or provide default:

```opal
make_col previous_value:window(lag(metric_value, 1), group_by(service_name))
| filter not is_null(previous_value)
```

Or use default value (though not directly supported in current lag syntax):
```opal
make_col pct_change:if(is_null(previous_value), 0, (value_change / previous_value) * 100)
```

## Key Takeaways

1. **Choose detection method based on anomaly type and data distribution**
   - Z-Score for normal distributions
   - IQR for skewed data
   - Rate-of-change for sudden spikes
   - Moving average for trend deviations

2. **OPAL window functions use different syntax from SQL**
   - Use `window(lag(...), group_by(...))` NOT `lag(...) over (...)`
   - Works with both metrics (align) and raw datasets

3. **Combine multiple methods to reduce false positives**
   - Require Z-score AND percentile agreement
   - Add minimum value filters for rate-of-change
   - Correlate multiple metrics (requests + errors)

4. **Tune thresholds based on metric characteristics**
   - Volatile metrics: Higher thresholds (3-sigma, 100% change)
   - Stable metrics: Lower thresholds (2-sigma, 50% change)
   - Test and iterate based on false positive rate

5. **Derived columns require separate make_col statements**
   - Cannot reference newly created column in same make_col
   - Use pipeline of make_col statements for sequential calculations

6. **Frame specification enables sliding window calculations**
   - `frame(back:30m)` for 30-minute moving average
   - Shorter frames for fast-changing metrics
   - Longer frames for stable baselines

7. **Metrics queries have two distinct patterns**
   - `options(bins: 1)` for summary (no pipe before aggregate)
   - `align 5m` for time-series (pipe required before aggregate)

8. **Statistical methods work best with sufficient historical data**
   - Need enough data points for meaningful stddev/percentiles
   - Consider minimum sample size (e.g., 24 hours of 5m buckets = 288 samples)

9. **Rate-of-change detection is powerful but requires careful tuning**
   - Very effective for early spike detection
   - Prone to false positives with low baseline values
   - Add minimum value and absolute change filters

10. **Test detection patterns against historical data**
    - Validate false positive rate on known-good periods
    - Verify detection on known anomaly events
    - Adjust thresholds based on operational feedback

## When to Use This Skill

Use detecting-anomalies skill when:
- User asks to check for anomalies
- Creating alert rules for unusual behavior
- Investigating performance degradation or incidents
- Identifying outliers in service metrics
- Detecting sudden traffic spikes or drops
- Comparing current values to historical baselines
- Setting up SLO violation alerts
- Analyzing metrics for unusual patterns

Cross-references:
- aggregating-gauge-metrics (for metric query patterns)
- analyzing-tdigest-metrics (for percentile-based detection)
- time-series-analysis (for temporal trending)
- working-with-intervals (for span-based anomaly detection)
- window-functions-deep-dive (to better understand window functions)
