---
name: timescaledb-hyperfunctions
description: |
  Use this skill when writing analytical SQL over time-series data with the TimescaleDB Toolkit (timescaledb_toolkit extension) hyperfunctions: approximate percentiles, statistical summaries, time-weighted averages, counter/gauge rates, uptime/heartbeat tracking, state durations, OHLC candlesticks, approximate distinct counts, top-N, and downsampling.

  **Trigger when user asks to:**
  - Compute percentiles/medians/p95/p99 over large or rolled-up time-series data
  - Compute rates or deltas from monotonic counters (Prometheus-style) or gauges
  - Compute time-weighted averages or integrals over irregularly sampled data
  - Track uptime/downtime from heartbeats, or time spent in each state
  - Build OHLC/candlestick or VWAP data for financial ticks
  - Store re-aggregatable summaries in continuous aggregates (two-step aggregation, rollup)
  - Approximate COUNT DISTINCT, find top-N / most frequent values, or downsample for charts

  **Keywords:** timescaledb_toolkit, hyperfunctions, percentile_agg, uddsketch, tdigest, approx_percentile, stats_agg, time_weight, counter_agg, gauge_agg, heartbeat_agg, state_agg, candlestick_agg, hyperloglog, approx_count_distinct, min_n, max_n, mcv_agg, lttb, asap_smooth, rollup, two-step aggregation
license: Apache-2.0
compatibility: Requires PostgreSQL 15+ with TimescaleDB and the timescaledb_toolkit extension (1.16+; gauge_agg needs 1.25+)
metadata:
  author: tigerdata
---

# TimescaleDB Toolkit Hyperfunctions

Hyperfunctions are SQL aggregates and accessors from the `timescaledb_toolkit` extension for analysis that plain PostgreSQL aggregates handle badly: percentiles that can be re-aggregated, rates over resetting counters, averages over irregular samples, uptime, state durations, and more.

## Setup

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb_toolkit;   -- preinstalled on Tiger Cloud
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb_toolkit';
ALTER EXTENSION timescaledb_toolkit UPDATE;           -- after upgrading the package
```

**Only use functions from the default schema in persistent objects.** Anything in the `toolkit_experimental` schema can change between releases, and `ALTER EXTENSION ... UPDATE` **drops** views, continuous aggregates, and functions that depend on it. All functions in this skill are stable.

## The Two-Step Pattern (read this first)

Nearly every hyperfunction works in two steps:

1. An **aggregate** builds a compact summary (`percentile_agg(val)` → `uddsketch`, `time_weight(...)` → `timeweightsummary`, ...).
2. An **accessor** extracts a result from the summary (`approx_percentile(0.95, summary)`, `average(summary)`, ...).

```sql
-- Function-call style
SELECT approx_percentile(0.95, percentile_agg(latency_ms)) FROM requests;

-- Arrow style (same result, reads left to right, chains multiple accessors)
SELECT percentile_agg(latency_ms) -> approx_percentile(0.95) FROM requests;
```

The pattern exists so summaries can be **stored and re-aggregated**:

- **`rollup(summary)`** merges summaries correctly. Use it to go from hourly to daily buckets.
- **Combining entities depends on the summary type.** Distribution summaries (`percentile_agg`, `uddsketch`, `tdigest`, `stats_agg`, `hyperloglog`, `mcv_agg`, `min_n`/`max_n`) can be rolled up across entities, e.g. one p99 for all hosts. Time-series summaries (`time_weight`, `counter_agg`, `gauge_agg`, `heartbeat_agg`, `state_agg`) describe one series. They can only be rolled up over consecutive, non-overlapping time ranges of the **same** entity: rolling up overlapping summaries from different hosts raises an ordering error. Compute the per-entity result first, then combine the numbers (e.g. `SUM` of per-host rates for a fleet-wide rate).
- **Never average averages, percentiles, or rates.** `AVG(p95_hourly)` is not a daily p95. `rollup(hourly_sketch) -> approx_percentile(0.95)` is the correct value.
- Store the **summary** in a continuous aggregate, not the final number. Then any accessor works at query time.

## Choosing a Function

| Question | Aggregate | Key accessors |
|---|---|---|
| p50/p95/p99, median | `percentile_agg`, `uddsketch`, `tdigest` | `approx_percentile`, `approx_percentile_array`, `approx_percentile_rank`, `mean`, `error` |
| avg/stddev/variance that can be rolled up; regression | `stats_agg` (1D or 2D) | `average`, `stddev`, `variance`, `skewness`, `kurtosis`, `num_vals`, `sum`; 2D: `slope`, `intercept`, `corr`, `determination_coeff`, `covariance` |
| Average over irregular sampling | `time_weight` | `average`, `integral`, `interpolated_average`, `first_val`, `last_val` |
| Rate/delta of monotonic counters with resets | `counter_agg` | `delta`, `rate`, `extrapolated_rate`, `irate_right`, `num_resets`, `interpolated_rate` |
| Rate/delta/trend of gauges (no reset handling) | `gauge_agg` (1.25+) | `delta`, `rate`, `extrapolated_rate`, `irate_right`, `slope`, `num_changes`, `interpolated_delta` |
| Uptime/downtime from heartbeats | `heartbeat_agg` | `uptime`, `downtime`, `live_ranges`, `dead_ranges`, `live_at`, `num_gaps`, `interpolated_uptime` |
| Time spent in each state | `state_agg` | `duration_in`, `state_timeline`, `state_periods`, `state_at`, `into_values` |
| OHLC / VWAP | `candlestick_agg` (ticks), `candlestick` (pre-aggregated bars) | `open`, `high`, `low`, `close`, `volume`, `vwap`, `open_time`, ... |
| Approx COUNT DISTINCT | `hyperloglog`, `approx_count_distinct` | `distinct_count`, `stderror` |
| Top-N / bottom-N values (with rows) | `max_n`, `min_n`, `max_n_by`, `min_n_by` | `into_values`, `into_array` |
| Most frequent values | `mcv_agg` | `topn`, `max_frequency`, `min_frequency`, `into_values` |
| Downsample for charting | `lttb`, `asap_smooth` | `unnest` |

TimescaleDB core (not the toolkit) provides `time_bucket`, `time_bucket_gapfill`, `locf`, `interpolate`, `first`, and `last`. Combine them freely with hyperfunctions.

## Percentiles

```sql
SELECT time_bucket('5 minutes', ts) AS bucket,
       service,
       percentile_agg(latency_ms) -> approx_percentile(0.5)  AS p50,
       percentile_agg(latency_ms) -> approx_percentile(0.99) AS p99
FROM requests
WHERE ts > now() - INTERVAL '1 day'
GROUP BY bucket, service;

-- Several percentiles from one sketch; fraction of requests under 200 ms
WITH s AS (SELECT percentile_agg(latency_ms) AS sketch FROM requests)
SELECT approx_percentile_array(ARRAY[0.5, 0.9, 0.99], sketch),
       approx_percentile_rank(200, sketch)
FROM s;
```

- **`percentile_agg(value)`**: default choice. It is a `uddsketch` with sensible defaults and a bounded relative error.
- **`uddsketch(size, max_error, value)`**, e.g. `uddsketch(200, 0.001, v)`: guaranteed relative error. Use when you need to tune accuracy or memory.
- **`tdigest(buckets, value)`**, e.g. `tdigest(100, v)`: more accurate at extreme tails (p99.9). Error is not bounded, and results depend on input order.
- Results are approximate. Use `PERCENTILE_CONT` when exact values are required and the data is small.

## Statistical Summaries

```sql
-- Re-aggregatable average/stddev
SELECT device_id,
       stats_agg(temperature) -> average() AS avg_temp,
       stats_agg(temperature) -> stddev()  AS sd_temp
FROM readings GROUP BY device_id;

-- 2D: linear regression of y on x
SELECT stats_agg(power_w, temperature) -> slope() AS watts_per_degree,
       stats_agg(power_w, temperature) -> corr()  AS correlation
FROM readings;

-- Rolling 7-day average from daily summaries (window function over summaries)
SELECT bucket,
       rolling(daily_stats) OVER (ORDER BY bucket ROWS 6 PRECEDING) -> average() AS avg_7d
FROM daily_rollup;
```

Accessors such as `stddev` and `variance` take an optional `'population'` or `'sample'` argument (default `'sample'`). In 2D, `stats_agg(y, x)` puts the dependent variable first. Use `average_x()`, `average_y()`, and similar accessors for per-axis stats.

## Time-Weighted Averages

`AVG()` overweights periods with dense sampling. `time_weight` weights each value by how long it was in effect.

```sql
SELECT time_bucket('1 hour', ts) AS bucket, sensor_id,
       time_weight('Linear', ts, value) -> average() AS tw_avg,
       time_weight('LOCF', ts, value) -> integral('hour') AS value_hours
FROM readings
GROUP BY bucket, sensor_id;
```

- **`'Linear'`** interpolates between points. Use it for continuously varying signals such as temperature.
- **`'LOCF'`** (last observation carried forward) holds each value until the next one. Use it for set-points, prices, and state-like values.
- `average()` returns NULL for a bucket with a single point, because there is no time span to weight. Use `interpolated_average` (below), or a larger bucket, for sparse series.
- `integral(unit)` takes `'microsecond'`, `'millisecond'`, `'second'` (default), `'minute'`, or `'hour'`.

**Bucket edges.** A plain `average()` only sees points inside the bucket. To account for values that span bucket boundaries, pass the neighbouring buckets' summaries:

```sql
WITH t AS (
  SELECT time_bucket('1 hour', ts) AS bucket, sensor_id,
         time_weight('LOCF', ts, value) AS tw
  FROM readings GROUP BY 1, 2
)
SELECT bucket, sensor_id,
       tw -> interpolated_average(
               bucket, INTERVAL '1 hour',
               LAG(tw)  OVER w,
               LEAD(tw) OVER w) AS tw_avg
FROM t
WINDOW w AS (PARTITION BY sensor_id ORDER BY bucket);
```

## Counters and Gauges

**Counters** only increase and reset to zero on restart (Prometheus counters, byte totals, request totals). `counter_agg` detects resets and corrects for them.

```sql
SELECT time_bucket('5 minutes', ts) AS bucket, host,
       counter_agg(ts, bytes_total) -> delta()        AS bytes,
       counter_agg(ts, bytes_total) -> rate()         AS bytes_per_sec,
       counter_agg(ts, bytes_total) -> num_resets()   AS restarts,
       counter_agg(ts, bytes_total) -> irate_right()  AS instant_rate
FROM metrics
GROUP BY bucket, host;
```

- `rate()` is per second, measured between the first and last sample in the bucket.
- For Prometheus-compatible extrapolation to the bucket edges, give the aggregate bounds: `counter_agg(ts, v, tstzrange(bucket, bucket + '5 min')) -> extrapolated_rate('prometheus')`. You can also set bounds afterwards with `with_bounds(summary, range)`.
- For edge-accurate deltas across buckets, use `interpolated_delta(bucket, interval, LAG(summary) OVER w, LEAD(summary) OVER w)` or `interpolated_rate(...)`, following the `interpolated_average` pattern above.

### Gauges

**Gauges** go up and down: memory in use, queue depth, temperature, connection count. `gauge_agg(ts, value)` gives counter-style change metrics but treats every drop as a real decrease, not a reset. Requires toolkit 1.25+.

```sql
SELECT time_bucket('15 minutes', ts) AS bucket, queue,
       gauge_agg(ts, depth) -> delta()        AS net_change,     -- last - first
       gauge_agg(ts, depth) -> rate()         AS change_per_sec, -- delta / time_delta
       gauge_agg(ts, depth) -> slope()        AS trend_per_sec,  -- least-squares fit
       gauge_agg(ts, depth) -> num_changes()  AS changes,
       gauge_agg(ts, depth) -> irate_right()  AS latest_rate     -- last two points
FROM queue_depth
GROUP BY bucket, queue;
```

- **Accessors** (stable in 1.25): `delta`, `rate`, `time_delta`, `idelta_left`/`idelta_right`, `irate_left`/`irate_right`, `slope`, `intercept`, `corr`, `num_changes`, `num_elements`, `zero_time` (as `-> zero_time()`; the function form is `gauge_zero_time(summary)`), and `extrapolated_delta`/`extrapolated_rate`. The extrapolated accessors take no method argument and need bounds, from `gauge_agg(ts, v, tstzrange(...))` or `with_bounds(summary, range)`.
- **Edge-accurate deltas across buckets**: call `interpolated_delta` or `interpolated_rate` in function form, with the summary first. The arrow form is not stable for gauges.

  ```sql
  SELECT bucket, queue,
         interpolated_delta(ga, bucket, INTERVAL '15 minutes',
                            LAG(ga) OVER w, LEAD(ga) OVER w) AS net_change
  FROM (SELECT time_bucket('15 minutes', ts) AS bucket, queue,
               gauge_agg(ts, depth) AS ga
        FROM queue_depth GROUP BY 1, 2) t
  WINDOW w AS (PARTITION BY queue ORDER BY bucket);
  ```
- **Not available on gauges**: `num_resets`, and `first_val`/`last_val`. Use `time_weight` if you need first/last values or a time-weighted average of the gauge.
- **Choosing gauge or counter**: if a value only ever falls on a restart, use `counter_agg`. If falls are real, such as memory being freed, use `gauge_agg`. `stats_agg` or `time_weight` are often better for "average level". `gauge_agg` answers "how much and how fast did it change".

## Heartbeats and Uptime

`heartbeat_agg(ts, start, range, heartbeat_interval)`: each heartbeat at `ts` marks the system live until `ts + heartbeat_interval`. `start` and `range` define the window that the aggregate covers.

```sql
-- Store per day, e.g. as continuous aggregate daily_heartbeats
SELECT time_bucket('1 day', ts) AS day, service,
       heartbeat_agg(ts, time_bucket('1 day', ts), '1 day', '2 minutes') AS hb
FROM pings
GROUP BY day, service;

SELECT day, service,
       hb -> uptime()      AS uptime,
       hb -> downtime()    AS downtime,
       hb -> num_gaps()    AS outages,
       hb -> dead_ranges() AS outage_ranges   -- setof (start, end)
FROM daily_heartbeats;
```

- Make `start` and `range` match the bucket. Otherwise time outside the data is counted as downtime.
- Use `interpolated_uptime(hb, LAG(hb) OVER w)` so a heartbeat just before the bucket boundary counts toward the next bucket.
- `live_at(hb, timestamp)` checks liveness at one point in time. `rollup(hb)` merges adjacent windows.

## State Tracking

`state_agg(ts, state)` takes a `text` or `bigint` state and records how long each state lasted.

```sql
-- One summary per machine per day; store it, e.g. as continuous aggregate machine_states_daily
SELECT time_bucket('1 day', ts) AS day, machine_id, state_agg(ts, status) AS sa
FROM machine_status
GROUP BY day, machine_id;

SELECT day, machine_id,
       sa -> duration_in('running') AS running_time,
       sa -> duration_in('error')   AS error_time
FROM machine_states_daily;

-- Full timeline: one row per contiguous period
SELECT machine_id, (sa -> state_timeline()).*   -- state, start_time, end_time
FROM machine_states_daily
WHERE machine_id = 1
ORDER BY start_time;

-- All periods in one state; time in a state within a sub-range
SELECT machine_id, (sa -> state_periods('error')).* FROM machine_states_daily;
SELECT day, machine_id, duration_in(sa, 'running', day + INTERVAL '8 hours', '8 hours') AS running_8_to_16
FROM machine_states_daily;
```

- `state_at(sa, ts)` returns the state at a given instant. `into_values(sa)` returns the total duration per state.
- Across bucket boundaries, use `interpolated_duration_in`, `interpolated_state_timeline`, and `interpolated_state_periods` with `LAG(sa)`.
- The final state's duration ends at the last observed timestamp. Add a closing row, or use the interpolated variants, if the final state should extend to the end of the bucket.

## Financial: Candlesticks

```sql
-- From raw ticks; store, e.g. as continuous aggregate one_min_candles
SELECT time_bucket('1 minute', ts) AS bucket, symbol,
       candlestick_agg(ts, price, volume) AS candle
FROM ticks GROUP BY bucket, symbol;

-- Accessors (also work after rollup to 1 hour / 1 day)
SELECT bucket, symbol,
       candle -> open() AS open, candle -> high() AS high,
       candle -> low()  AS low,  candle -> close() AS close,
       volume(candle) AS volume, vwap(candle) AS vwap   -- function form only
FROM one_min_candles;
```

`volume` and `vwap` have no arrow form. Call them as functions. Use `candlestick(ts, open, high, low, close, volume)` to wrap bars that are already aggregated, for example from an upstream feed. `open_time`, `high_time`, `low_time`, and `close_time` return when each value occurred.

## Approximate Distinct, Top-N, Frequency

```sql
-- Approx COUNT DISTINCT; hyperloglog buckets are rounded up to a power of 2
SELECT approx_count_distinct(user_id) -> distinct_count() FROM events;
SELECT hyperloglog(32768, user_id) AS hll FROM events GROUP BY day;   -- store, then rollup(hll) -> distinct_count()

-- 5 slowest requests with the full row
SELECT into_values(max_n_by(latency_ms, r, 5), NULL::requests)
FROM requests r;

-- 5 largest values as an array
SELECT max_n(latency_ms, 5) -> into_array() FROM requests;

-- 10 most common error codes
SELECT topn(mcv_agg(10, error_code)) FROM errors;
```

- `approx_count_distinct(v)` uses default precision. Use `hyperloglog(buckets, v)` to trade memory for accuracy. `stderror()` reports the expected relative error.
- `max_n_by(sort_value, row, n)` needs the row type in `into_values(agg, NULL::rowtype)` to decode the result.
- `mcv_agg(n, value)` is approximate and assumes a skewed (Zipf-like) distribution. Pass `mcv_agg(n, skew, value)` to tune the assumed skew (default 1.1).

## Downsampling for Charts

```sql
-- Reduce 1M points to ~500 that preserve the visual shape
SELECT time, value
FROM unnest((SELECT lttb(ts, value, 500) FROM readings WHERE sensor_id = 42));

-- Smooth out periodic noise for display
SELECT time, value
FROM unnest((SELECT asap_smooth(ts, value, 800) FROM readings WHERE sensor_id = 42));
```

`lttb` keeps actual points. `asap_smooth` produces smoothed values. Use both for visualization only, not for further statistics.

## Continuous Aggregates with Hyperfunctions

Store summaries in the continuous aggregate, then roll them up and apply accessors at query time.

```sql
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', ts) AS bucket,
       host,
       percentile_agg(latency_ms)          AS latency_pct,
       stats_agg(cpu)                      AS cpu_stats,
       time_weight('Linear', ts, mem_used) AS mem_tw,
       counter_agg(ts, bytes_total)        AS bytes_ctr
FROM metrics
GROUP BY bucket, host;

-- Hierarchical: daily built from hourly via rollup
CREATE MATERIALIZED VIEW metrics_daily
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', bucket) AS bucket,
       host,
       rollup(latency_pct) AS latency_pct,
       rollup(cpu_stats)   AS cpu_stats,
       rollup(mem_tw)      AS mem_tw,
       rollup(bytes_ctr)   AS bytes_ctr
FROM metrics_hourly
GROUP BY 1, host;

-- Distribution summaries: any percentile/statistic across all hosts
SELECT bucket,
       rollup(latency_pct) -> approx_percentile(0.99) AS p99_all_hosts,
       rollup(cpu_stats)   -> average()               AS avg_cpu
FROM metrics_daily
WHERE bucket > now() - INTERVAL '30 days'
GROUP BY bucket;

-- Time-series summaries: evaluate per host, then combine the results
SELECT bucket,
       SUM(bytes_ctr -> rate()) AS fleet_bytes_per_sec,
       AVG(mem_tw -> average()) AS avg_host_mem
FROM metrics_daily
WHERE bucket > now() - INTERVAL '30 days'
GROUP BY bucket;
```

Summaries are a few hundred bytes to a few KB. That is larger than a single float, but it replaces many precomputed columns (p50, p90, p95, p99, ...) and stays correct under rollup.

## Common Mistakes

- **Averaging precomputed statistics over time** (`AVG(p95_hourly)`, `AVG(avg_hourly)` for a daily value): store summaries and use `rollup`.
- **Rolling up time-series summaries across entities** (`rollup(counter_agg)`, `rollup(time_weight)`, etc. without grouping by entity): this fails with an ordering error. Evaluate per entity, then aggregate the results.
- **Feeding time-series aggregates out-of-order rows from a partially compressed chunk** (`ERROR: out of order points`): rows inserted into a compressed chunk stay in the rowstore until it is recompressed, so a scan can return them interleaved with columnstore rows. `counter_agg`, `gauge_agg`, `time_weight`, and similar aggregates then see time ranges that overlap. Recompress the chunk (`compress_chunk`), or sort the input first: `SELECT counter_agg(ts, v) FROM (SELECT * FROM metrics WHERE ... ORDER BY ts) t`.
- **Using `AVG()` on irregularly sampled data**: use `time_weight`.
- **Using `max(v) - min(v)` or `last - first` on counters**: this breaks on resets. Use `counter_agg -> delta()`.
- **Using `counter_agg` on gauges**: a drop is treated as a reset and inflates the delta. Use `gauge_agg`.
- **Building continuous aggregates on `toolkit_experimental.*`**: they are dropped on extension update.
- **Running interpolated accessors without ordering**: the `LAG`/`LEAD` window must be `PARTITION BY` the entity and `ORDER BY` the bucket.
- **Mismatched `heartbeat_agg` window**: `start`/`range` must match the bucket, or the extra time counts as downtime.
- **Expecting exact results from sketches**: `percentile_agg`, `tdigest`, `hyperloglog`, and `mcv_agg` are approximate. Report this when precision matters.

## Reference

Use the `search_docs` tool with source `tiger` (for example "hyperfunctions counter_agg") for full signatures and newer functions. Source: https://github.com/timescale/timescaledb-toolkit
