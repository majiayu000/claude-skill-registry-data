---
name: clickhouse-io
description: ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads.
origin: ECC
---

# ClickHouse Analytics Patterns

ClickHouse-specific patterns for high-performance analytics and data engineering.

## When to Activate

- Designing ClickHouse table schemas (MergeTree engine selection)
- Writing analytical queries (aggregations, window functions, joins)
- Optimizing query performance (partition pruning, projections, materialized views)
- Ingesting large volumes of data (batch inserts)
- Migrating from PostgreSQL/MySQL to ClickHouse for analytics
- Implementing real-time dashboards or time-series analytics

## Overview

ClickHouse is a column-oriented database management system (DBMS) for online analytical processing (OLAP). It's optimized for fast analytical queries on large datasets.

**Key Features:**
- Column-oriented storage
- Data compression
- Parallel query execution
- Distributed queries
- Real-time analytics

## Table Design Patterns

### MergeTree Engine (Most Common)

```sql
CREATE TABLE markets_analytics (
    date            Date,
    market_id       LowCardinality(String),   -- repeated string; LowCardinality cuts storage ~3-10×
    market_name     String,
    volume          UInt64,
    trades          UInt32,
    unique_traders  UInt32,
    avg_trade_size  Float64,
    created_at      DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, market_id)   -- low-cardinality columns first for best data skipping
SETTINGS index_granularity = 8192;
```

### Trading Tick Data (High-Precision Timestamps)

For nanosecond-precision trading data use `DateTime64(9)`, `LowCardinality`, `Enum`, and `Decimal`:

```sql
CREATE TABLE trades_tick (
    symbol    LowCardinality(String),
    exchange  LowCardinality(String),
    side      Enum8('buy' = 1, 'sell' = 2),
    price     Decimal64(8),
    quantity  Decimal64(8),
    trade_id  String,
    ts        DateTime64(9)          -- nanosecond precision
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(ts)
ORDER BY (symbol, ts)
SETTINGS index_granularity = 8192;
```

### ReplacingMergeTree (Deduplication)

```sql
-- ver column controls which row wins: highest ver survives the merge.
-- Deduplication is EVENTUAL — it happens at merge time, not on insert.
-- Queries must add FINAL or GROUP BY workarounds to see deduplicated data.
CREATE TABLE user_events (
    event_id    String,
    user_id     LowCardinality(String),
    event_type  LowCardinality(String),
    updated_at  DateTime,
    ver         UInt64,         -- monotonically increasing version (e.g. Unix ms)
    properties  String
) ENGINE = ReplacingMergeTree(ver)
PARTITION BY toYYYYMM(updated_at)
ORDER BY (user_id, event_id);  -- ORDER BY defines the dedup key — exclude timestamp

-- Query with FINAL to get deduplicated rows (slower; use projections for hot paths)
SELECT event_id, user_id, event_type, updated_at
FROM user_events FINAL
WHERE user_id = 'u-123';
```

### AggregatingMergeTree (Pre-aggregation)

```sql
CREATE TABLE market_stats_hourly (
    hour          DateTime,
    market_id     LowCardinality(String),
    total_volume  AggregateFunction(sum, UInt64),
    total_trades  AggregateFunction(count),          -- count takes no type argument
    unique_users  AggregateFunction(uniq, String)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, market_id);

-- INSERT must use -State combinators, not raw values
INSERT INTO market_stats_hourly
SELECT
    toStartOfHour(timestamp) AS hour,
    market_id,
    sumState(amount)        AS total_volume,
    countState()            AS total_trades,
    uniqState(user_id)      AS unique_users
FROM trades
GROUP BY hour, market_id;

-- Query with -Merge combinators
SELECT
    hour,
    market_id,
    sumMerge(total_volume)   AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users)  AS users
FROM market_stats_hourly
WHERE hour >= toStartOfHour(now() - INTERVAL 24 HOUR)
GROUP BY hour, market_id
ORDER BY hour DESC;
```

### SummingMergeTree (Additive Metrics)

Useful for cumulative trading metrics (P&L, position size) where values are simply summed at merge time:

```sql
CREATE TABLE position_daily (
    date       Date,
    symbol     LowCardinality(String),
    strategy   LowCardinality(String),
    pnl        Float64,
    volume     Float64
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, symbol, strategy);
```

## Query Optimization Patterns

### Efficient Filtering

ClickHouse prunes data using the ORDER BY (primary key) index. Column order in `WHERE` does not affect performance — what matters is whether the filtered column appears in the ORDER BY. Always include ORDER BY columns in filters.

```sql
-- ✅ GOOD: Filter on ORDER BY columns (date, market_id) for index-based pruning
SELECT
    date,
    market_id,
    sum(volume) AS total_volume,
    sum(trades) AS trade_count
FROM markets_analytics
WHERE date >= '2025-01-01'
  AND market_id = 'market-123'
  AND volume > 1000
ORDER BY date DESC
LIMIT 100;

-- ❌ BAD: Filtering only on non-ORDER-BY columns forces a full scan
SELECT date, market_id, volume
FROM markets_analytics
WHERE volume > 1000
  AND market_name LIKE '%election%';
```

### Aggregations

```sql
-- ✅ Use ClickHouse-specific aggregation functions
SELECT
    toStartOfDay(created_at) AS day,
    market_id,
    sum(volume)         AS total_volume,
    count()             AS total_trades,
    uniq(trader_id)     AS unique_traders,
    avg(trade_size)     AS avg_size
FROM trades
WHERE created_at >= now() - INTERVAL 7 DAY   -- now() for DateTime columns; today() for Date
GROUP BY day, market_id
ORDER BY day DESC, total_volume DESC;

-- ✅ quantile() for percentiles — sampling algorithm, faster than exact
--    Use quantileExact() when financial precision is required
SELECT
    quantile(0.50)(trade_size)      AS median,
    quantile(0.95)(trade_size)      AS p95,
    quantile(0.99)(trade_size)      AS p99,
    quantileExact(0.99)(trade_size) AS p99_exact   -- exact; use for SLA/compliance metrics
FROM trades
WHERE created_at >= now() - INTERVAL 1 HOUR;
```

### Window Functions

```sql
SELECT
    date,
    market_id,
    volume,
    sum(volume) OVER (
        PARTITION BY market_id
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_volume
FROM markets_analytics
WHERE date >= today() - INTERVAL 30 DAY
ORDER BY market_id, date;
```

## Setup

```toml
# Cargo.toml
[dependencies]
clickhouse = { version = "0.13", features = ["inserter"] }
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
chrono = "0.4"
tracing = "0.1"

# Pipeline-only: add these only if running ETL or CDC from PostgreSQL
# sqlx = { version = "0.8", features = ["postgres", "runtime-tokio", "chrono"] }
# tokio-postgres = "0.7"
# futures = "0.3"
# serde_json = "1"
```

## Client Setup

```rust
use clickhouse::Client;

// Use https:// URL for TLS-encrypted connections (recommended in production).
// The underlying reqwest client supports TLS via https automatically.
//
// Client is Arc-backed internally — clone or share it freely across tasks.
// Create one instance at startup and pass &Client (or Arc<Client>) through your app.
fn build_client() -> Client {
    let url = std::env::var("CLICKHOUSE_URL").expect("CLICKHOUSE_URL must be set");
    // CLICKHOUSE_URL should be e.g. "https://host:8443" (TLS) or "http://host:8123" (plaintext)
    Client::default()
        .with_url(&url)
        .with_user(std::env::var("CLICKHOUSE_USER").expect("CLICKHOUSE_USER must be set"))
        .with_password(std::env::var("CLICKHOUSE_PASSWORD").expect("CLICKHOUSE_PASSWORD must be set"))
}
```

## Data Insertion Patterns

### Bulk Insert (Recommended)

```rust
use clickhouse::{Client, Row};
use serde::Serialize;

// Serialize only — no Deserialize needed for insert-only types
#[derive(Row, Serialize)]
struct Trade {
    id:        String,
    market_id: String,
    user_id:   String,
    amount:    f64,
    timestamp: i64,  // Unix epoch seconds; maps to ClickHouse Int64 or DateTime64(0)
}

// ✅ Batch insert — one HTTP request for the whole slice
async fn bulk_insert_trades(client: &Client, trades: &[Trade]) -> clickhouse::error::Result<()> {
    let mut insert = client.insert("trades")?;
    for trade in trades {
        insert.write(trade).await?;
    }
    insert.end().await
}

// ❌ Individual inserts — one HTTP request per row; never call this in a loop
async fn insert_one_trade(client: &Client, trade: &Trade) -> clickhouse::error::Result<()> {
    let mut insert = client.insert("trades")?;
    insert.write(trade).await?;
    insert.end().await
}
```

### Streaming Insert

```rust
use futures::StreamExt;
use std::time::Duration;

// For continuous async ingestion.
// Use impl Stream (not Iterator) so the data source can be I/O-backed without
// blocking the async executor.
async fn stream_inserts(
    client: &Client,
    mut data_source: impl futures::Stream<Item = Trade> + Unpin,
) -> clickhouse::error::Result<()> {
    let mut inserter = client
        .inserter("trades")?
        .with_max_rows(100_000)
        .with_period(Some(Duration::from_secs(5)));

    while let Some(trade) = data_source.next().await {
        inserter.write(&trade).await?;
        // commit() is a cheap threshold check — safe to call on every write.
        // It only sends an HTTP request when max_entries or the period deadline is reached.
        inserter.commit().await?;
    }

    inserter.end().await?;
    Ok(())
}
```

## Querying from Rust

```rust
use clickhouse::Row;
use serde::Deserialize;

// Derive both Row and Deserialize for query results
#[derive(Row, Deserialize)]
struct MarketStat {
    market_id:    String,
    total_volume: f64,
    trade_count:  u64,
}

// ✅ Use .bind() for parameterized queries — never interpolate user input into SQL strings
async fn query_market_stats(
    client: &Client,
    market_id: &str,
    days: u32,
) -> clickhouse::error::Result<Vec<MarketStat>> {
    client
        .query(
            "SELECT market_id,
                    sum(volume)  AS total_volume,
                    sum(trades)  AS trade_count
             FROM markets_analytics
             WHERE date >= today() - ?
               AND market_id = ?
             GROUP BY market_id",
        )
        .bind(days)
        .bind(market_id)
        .fetch_all::<MarketStat>()
        .await
}

// For large result sets, stream rows instead of loading all into memory
async fn stream_market_stats(
    client: &Client,
    market_id: &str,
) -> clickhouse::error::Result<()> {
    let mut cursor = client
        .query("SELECT market_id, sum(volume) AS total_volume, sum(trades) AS trade_count FROM markets_analytics WHERE market_id = ? GROUP BY market_id ORDER BY total_volume DESC")
        .bind(market_id)
        .fetch::<MarketStat>()?;

    while let Some(row) = cursor.next().await? {
        tracing::info!(market_id = %row.market_id, volume = row.total_volume);
    }
    Ok(())
}
```

## Materialized Views

### Real-time Aggregations

```sql
-- Target table must exist first (see AggregatingMergeTree above)
CREATE MATERIALIZED VIEW market_stats_hourly_mv
TO market_stats_hourly
AS SELECT
    toStartOfHour(timestamp) AS hour,
    market_id,
    sumState(amount)        AS total_volume,
    countState()            AS total_trades,
    uniqState(user_id)      AS unique_users
FROM trades
GROUP BY hour, market_id;

-- Query the target table directly
SELECT
    hour,
    market_id,
    sumMerge(total_volume)   AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users)  AS users
FROM market_stats_hourly
WHERE hour >= now() - INTERVAL 24 HOUR
GROUP BY hour, market_id;
```

## Performance Monitoring

### Query Performance

```sql
SELECT
    query_id,
    user,
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
  AND query_duration_ms > 1000
  AND event_time >= now() - INTERVAL 1 HOUR
ORDER BY query_duration_ms DESC
LIMIT 10;
```

### Table Statistics

```sql
-- Exclude system tables; use bytes_on_disk for compressed size
SELECT
    database,
    table,
    formatReadableSize(sum(bytes_on_disk)) AS size,
    sum(rows)                              AS rows,
    max(modification_time)                 AS latest_modification
FROM system.parts
WHERE active
  AND database != 'system'
GROUP BY database, table
ORDER BY sum(bytes_on_disk) DESC;
```

## Common Analytics Queries

### Time Series Analysis

```sql
-- Daily active users (timestamp is DateTime — use now(), not today())
SELECT
    toDate(timestamp)   AS date,
    uniq(user_id)       AS daily_active_users
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date;

-- Retention analysis
-- Use a nested subquery to avoid referencing SELECT aliases within the same SELECT level
SELECT
    signup_date,
    countIf(days_since_signup = 0)  AS day_0,
    countIf(days_since_signup = 1)  AS day_1,
    countIf(days_since_signup = 7)  AS day_7,
    countIf(days_since_signup = 30) AS day_30
FROM (
    SELECT
        user_id,
        first_seen                                  AS signup_date,
        activity_date,
        dateDiff('day', first_seen, activity_date)  AS days_since_signup
    FROM (
        SELECT
            user_id,
            min(toDate(timestamp)) AS first_seen,
            toDate(timestamp)      AS activity_date
        FROM events
        GROUP BY user_id, activity_date
    )
)
GROUP BY signup_date
ORDER BY signup_date DESC;
```

### Funnel Analysis

```sql
-- Conversion funnel aggregated across all sessions for the day
-- Guard against division by zero with if()
SELECT
    countIf(step = 'viewed_market')    AS viewed,
    countIf(step = 'clicked_trade')    AS clicked,
    countIf(step = 'completed_trade')  AS completed,
    round(if(viewed   > 0, clicked   / viewed   * 100, 0), 2) AS view_to_click_rate,
    round(if(clicked  > 0, completed / clicked  * 100, 0), 2) AS click_to_completion_rate
FROM (
    SELECT
        user_id,
        session_id,
        event_type AS step
    FROM events
    WHERE event_date = today()
);
```

### Cohort Analysis

```sql
SELECT
    toStartOfMonth(signup_date)    AS cohort,
    toStartOfMonth(activity_date)  AS month,
    dateDiff('month', toStartOfMonth(signup_date), toStartOfMonth(activity_date)) AS months_since_signup,
    count(DISTINCT user_id)        AS active_users
FROM (
    SELECT
        user_id,
        min(toDate(timestamp)) OVER (PARTITION BY user_id) AS signup_date,
        toDate(timestamp)                                   AS activity_date
    FROM events
)
GROUP BY cohort, month, months_since_signup
ORDER BY cohort, months_since_signup;
```

## Data Pipeline Patterns

### ETL Pattern

```rust
use futures::TryStreamExt;
use tokio::time::{interval, Duration};

#[derive(Row, Serialize)]
struct MarketSummary {
    date:      String,
    market_id: String,
    volume:    f64,
    trades:    u32,
}

async fn etl_pipeline(
    pg: &sqlx::PgPool,
    ch: &Client,
) -> anyhow::Result<()> {
    // Cast NUMERIC to FLOAT8 in SQL — avoids a string round-trip in Rust.
    // fetch() streams rows one at a time, avoiding loading the full result into memory.
    // For very large tables, add LIMIT/OFFSET or keyset pagination to bound each run.
    let mut rows = sqlx::query!(
        "SELECT created_at, market_slug,
                total_volume::FLOAT8 AS total_volume,
                trade_count
         FROM market_snapshots
         ORDER BY created_at"
    )
    .fetch(pg);

    let mut insert = ch.insert("market_summaries")?;
    while let Some(r) = rows.try_next().await? {
        // Log and skip rows with invalid trade_count rather than silently zeroing them.
        let trades = match u32::try_from(r.trade_count) {
            Ok(v) => v,
            Err(_) => {
                tracing::warn!(trade_count = r.trade_count, "skipping row: trade_count out of u32 range");
                continue;
            }
        };
        insert.write(&MarketSummary {
            date:      r.created_at.date_naive().to_string(),
            market_id: r.market_slug,
            volume:    r.total_volume.unwrap_or(0.0),
            trades,
        }).await?;
    }
    insert.end().await?;

    Ok(())
}

// Run periodically with tokio.
// interval() fires immediately on the first tick; the tick() at the top of the
// loop delays execution until the first interval has elapsed.
async fn run_hourly_etl(pg: sqlx::PgPool, ch: Client) {
    let mut ticker = interval(Duration::from_secs(3600));
    loop {
        ticker.tick().await;
        if let Err(e) = etl_pipeline(&pg, &ch).await {
            tracing::error!("ETL failed: {e}");
        }
    }
}
```

### Change Data Capture (CDC)

> **WARNING:** `NoTls` transmits credentials and data in plaintext. Use `postgres-openssl`
> or `tokio-postgres-rustls` in production. Set `CLICKHOUSE_URL=https://...` for TLS to
> ClickHouse as well.

```rust
use std::time::Duration;
use tokio_postgres::{AsyncMessage, NoTls};

#[derive(Row, Serialize)]
struct MarketUpdateEvent {
    market_id:  String,
    event_type: String,  // INSERT, UPDATE, DELETE
    timestamp:  i64,     // Unix epoch seconds; maps to ClickHouse Int64 or DateTime64(0)
    data:       String,
}

// Listen to PostgreSQL changes and sync to ClickHouse.
//
// tokio-postgres splits into two halves: `pg` (Client) for sending queries,
// and `conn` (Connection) which must be driven to process the protocol.
// We pump conn in a spawned task and forward messages over a channel so
// both halves can be used concurrently.
async fn cdc_pipeline(ch: Client) -> anyhow::Result<()> {
    let (pg, mut conn) = tokio_postgres::connect(
        &std::env::var("DATABASE_URL").expect("DATABASE_URL must be set"),
        NoTls,  // replace with TLS connector in production
    )
    .await?;

    // Drive the connection and forward all async messages via a channel.
    let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<AsyncMessage>();
    tokio::spawn(async move {
        loop {
            match futures::future::poll_fn(|cx| conn.poll_message(cx)).await {
                Ok(msg) => {
                    if tx.send(msg).is_err() {
                        break; // receiver dropped, shut down
                    }
                }
                Err(e) => {
                    tracing::error!("PostgreSQL connection error: {e}");
                    break;
                }
            }
        }
    });

    pg.execute("LISTEN market_updates", &[]).await?;

    // Use Inserter to batch notifications — not one HTTP request per event.
    // 50_000 entries keeps part sizes well above ClickHouse's recommended minimum (~10k rows).
    let mut inserter = ch
        .inserter("market_updates")?
        .with_max_rows(50_000)
        .with_period(Some(Duration::from_secs(5)));

    while let Some(msg) = rx.recv().await {
        if let AsyncMessage::Notification(n) = msg {
            let payload: serde_json::Value = serde_json::from_str(n.payload())?;
            let event = MarketUpdateEvent {
                market_id: payload["id"]
                    .as_str()
                    .ok_or_else(|| anyhow::anyhow!("CDC payload missing 'id'"))?
                    .to_string(),
                event_type: payload["operation"]
                    .as_str()
                    .ok_or_else(|| anyhow::anyhow!("CDC payload missing 'operation'"))?
                    .to_string(),
                timestamp: chrono::Utc::now().timestamp(),
                data: serde_json::to_string(&payload["new_data"])?,
            };
            inserter.write(&event).await?;
            // commit() is a cheap threshold check — safe to call on every write.
            inserter.commit().await?;
        }
    }

    inserter.end().await?;
    Ok(())
}
```

## Best Practices

### 1. Partitioning Strategy
- Partition by time (usually month or day)
- Avoid too many partitions (performance impact)
- Use `Date` type for partition key

### 2. Ordering Key
- Put **low-cardinality** columns first (e.g., `date` before `market_id`) — this maximises data skipping and compression
- Columns appearing in frequent `WHERE` filters should be early in the ORDER BY
- Higher-cardinality columns (like `trade_id`) belong at the end or are omitted

### 3. Data Types
- Use smallest appropriate integer type (`UInt32` vs `UInt64`)
- Use `LowCardinality(String)` for columns with < ~10k distinct values (symbols, exchanges, statuses)
- Use `Enum8` / `Enum16` for fixed categorical data
- Use `DateTime64(9)` for nanosecond-precision trading timestamps
- Use `Decimal64(8)` for prices and quantities (avoid `Float64` for financial values)

### 4. Avoid
- `SELECT *` — columnar storage reads every column from disk; specify only what you need
- `FINAL` on hot query paths — it triggers a blocking merge; use pre-aggregation or projections instead
- Too many JOINs — denormalize for analytics
- Small frequent inserts — batch into ≥10,000 rows per request
- Parallel insert streams without coordination — too many concurrent inserters cause part proliferation

### 5. Connection Lifecycle
- `Client` is Arc-backed internally; cloning is cheap — share one instance across the application
- Pass `&Client` to functions; store one `Client` (or `Arc<Client>`) in your application state
- The `Client` does not maintain a persistent connection; each insert/query opens an HTTP request

### 6. Monitoring
- Track query performance via `system.query_log`
- Monitor disk usage via `system.parts`
- Check merge operations via `system.merges`
- Review slow query log regularly

**Remember**: ClickHouse excels at analytical workloads. Design tables for your query patterns, batch inserts into large blocks, and leverage materialized views for real-time aggregations.
