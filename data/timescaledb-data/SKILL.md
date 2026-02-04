---
name: timescaledb-data
description: TimescaleDB data modeling and operations for crypto market time-series data
license: MIT
compatibility: opencode
metadata:
  database: timescaledb
  version: "pg17"
  domain: time-series
---

## What I Do

Guide TimescaleDB data modeling, schema design, and operations for cryptocurrency market time-series data in the crypto-scout ecosystem.

## Database Architecture

### Schema Overview
```sql
-- Main schema
crypto_scout
├── stream_offsets              -- Stream offset tracking
├── bybit_spot_tickers          -- Spot market tickers
├── bybit_spot_kline_{1m,5m,15m,60m,240m,1d}  -- Spot klines
├── bybit_spot_public_trade     -- Spot public trades
├── bybit_spot_order_book_{1,50,200,1000}     -- Spot order books
├── bybit_linear_tickers        -- Linear market tickers
├── bybit_linear_kline_{1m,5m,15m,60m,240m,1d} -- Linear klines
├── bybit_linear_public_trade   -- Linear public trades
├── bybit_linear_order_book_{1,50,200,1000}   -- Linear order books
├── bybit_linear_all_liquidation -- Liquidation events
├── cmc_fgi                     -- Fear & Greed Index
├── cmc_kline_{1d,1w}          -- CMC BTC/USD klines
├── bybit_lpl                  -- Liquidation pressure level
├── btc_price_risk             -- BTC price risk mapping
└── btc_risk_price             -- Current risk assessment
```

### Hypertable Pattern
```sql
-- Create standard table first
CREATE TABLE crypto_scout.bybit_spot_kline_1m (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    turnover DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Convert to hypertable
SELECT create_hypertable('crypto_scout.bybit_spot_kline_1m', 'time');
```

## Table Definitions

### Kline Tables (Candlestick Data)
```sql
CREATE TABLE crypto_scout.bybit_spot_kline_1m (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    turnover DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (time, symbol)
);

-- Indexes for common queries
CREATE INDEX idx_bybit_spot_kline_1m_symbol_time 
ON crypto_scout.bybit_spot_kline_1m (symbol, time DESC);
```

### Ticker Tables
```sql
CREATE TABLE crypto_scout.bybit_spot_tickers (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    last_price DOUBLE PRECISION NOT NULL,
    high_price_24h DOUBLE PRECISION NOT NULL,
    low_price_24h DOUBLE PRECISION NOT NULL,
    volume_24h DOUBLE PRECISION NOT NULL,
    turnover_24h DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (time, symbol)
);
```

### Trade Tables
```sql
CREATE TABLE crypto_scout.bybit_spot_public_trade (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    trade_id TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    qty DOUBLE PRECISION NOT NULL,
    side TEXT NOT NULL,
    PRIMARY KEY (time, trade_id)
);
```

### Order Book Tables
```sql
CREATE TABLE crypto_scout.bybit_spot_order_book_200 (
    time TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL,  -- 'bid' or 'ask'
    price DOUBLE PRECISION NOT NULL,
    qty DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (time, symbol, side, price)
);
```

### Stream Offsets (for exactly-once processing)
```sql
CREATE TABLE crypto_scout.stream_offsets (
    stream_name TEXT PRIMARY KEY,
    offset_value BIGINT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Performance Optimization

### Compression Policy
```sql
-- Enable compression after data ages
ALTER TABLE crypto_scout.bybit_spot_kline_1m 
SET (timescaledb.compress, timescaledb.compress_segmentby = 'symbol');

-- Auto-compress after 7 days
SELECT add_compression_policy(
    'crypto_scout.bybit_spot_kline_1m', 
    INTERVAL '7 days'
);
```

### Retention Policy
```sql
-- Remove old data after 90 days
SELECT add_retention_policy(
    'crypto_scout.bybit_spot_kline_1m', 
    INTERVAL '90 days'
);
```

### Reorder Policy
```sql
-- Optimize query performance for recent data
SELECT add_reorder_policy(
    'crypto_scout.bybit_spot_kline_1m', 
    'idx_bybit_spot_kline_1m_symbol_time'
);
```

## JDBC Operations

### Repository Pattern
```java
public final class BybitSpotRepository {
    private final DataSource dataSource;
    
    public void saveTickers(final List<Ticker> tickers) throws SQLException {
        final var sql = "INSERT INTO crypto_scout.bybit_spot_tickers " +
            "(time, symbol, last_price, high_price_24h, low_price_24h, volume_24h, turnover_24h) " +
            "VALUES (?, ?, ?, ?, ?, ?, ?) " +
            "ON CONFLICT (time, symbol) DO NOTHING";
        
        try (final var conn = dataSource.getConnection();
             final var stmt = conn.prepareStatement(sql)) {
            
            for (final var ticker : tickers) {
                stmt.setTimestamp(1, Timestamp.from(ticker.time()));
                stmt.setString(2, ticker.symbol());
                stmt.setDouble(3, ticker.lastPrice());
                // ... set remaining parameters
                stmt.addBatch();
            }
            
            stmt.executeBatch();
        }
    }
}
```

### Batch Insert Optimization
```java
// Configure HikariCP for batch inserts
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:postgresql://localhost:5432/crypto_scout");
config.setUsername("crypto_scout_db");
config.setPassword("password");
config.setMaximumPoolSize(10);
config.addDataSourceProperty("reWriteBatchedInserts", "true");
config.addDataSourceProperty("cachePrepStmts", "true");
```

### Offset Management
```java
public void saveWithOffset(
    final List<Data> data, 
    final String streamName, 
    final long offset
) throws SQLException {
    final var insertSql = "INSERT INTO ...";
    final var offsetSql = 
        "INSERT INTO crypto_scout.stream_offsets (stream_name, offset_value) " +
        "VALUES (?, ?) " +
        "ON CONFLICT (stream_name) DO UPDATE SET offset_value = EXCLUDED.offset_value";
    
    try (final var conn = dataSource.getConnection()) {
        conn.setAutoCommit(false);
        try {
            // Insert data
            try (final var stmt = conn.prepareStatement(insertSql)) {
                for (final var d : data) {
                    // set parameters
                    stmt.addBatch();
                }
                stmt.executeBatch();
            }
            
            // Update offset
            try (final var stmt = conn.prepareStatement(offsetSql)) {
                stmt.setString(1, streamName);
                stmt.setLong(2, offset);
                stmt.executeUpdate();
            }
            
            conn.commit();
        } catch (SQLException e) {
            conn.rollback();
            throw e;
        }
    }
}
```

## Query Patterns

### Time-Range Queries
```sql
-- Get klines for last 24 hours
SELECT * FROM crypto_scout.bybit_spot_kline_1m
WHERE symbol = 'BTCUSDT'
  AND time >= NOW() - INTERVAL '24 hours'
ORDER BY time DESC;

-- Get aggregated daily data
SELECT 
    time_bucket('1 day', time) AS day,
    symbol,
    first(open, time) AS open,
    max(high) AS high,
    min(low) AS low,
    last(close, time) AS close,
    sum(volume) AS volume
FROM crypto_scout.bybit_spot_kline_1m
WHERE symbol = 'BTCUSDT'
GROUP BY day, symbol
ORDER BY day DESC;
```

### Continuous Aggregates
```sql
-- Create 1-hour continuous aggregate
CREATE MATERIALIZED VIEW crypto_scout.bybit_spot_kline_1h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    symbol,
    first(open, time) AS open,
    max(high) AS high,
    min(low) AS low,
    last(close, time) AS close,
    sum(volume) AS volume,
    sum(turnover) AS turnover
FROM crypto_scout.bybit_spot_kline_1m
GROUP BY bucket, symbol;

-- Refresh policy
SELECT add_continuous_aggregate_policy(
    'crypto_scout.bybit_spot_kline_1h',
    start_offset => INTERVAL '1 month',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);
```

## Backup and Restore

### Backup
```bash
# Using pg_dump
pg_dump -h localhost -p 5432 -U crypto_scout_db -d crypto_scout > backup.sql

# Using backup sidecar (configured in compose)
# Backups are written to ./backups automatically
```

### Restore
```bash
# From SQL file
psql -h localhost -p 5432 -U crypto_scout_db -d crypto_scout < backup.sql

# From custom format
pg_restore -h localhost -p 5432 -U crypto_scout_db -d crypto_scout backup.dump
```

## When to Use Me

Use this skill when:
- Designing new database tables for time-series data
- Implementing repository classes with JDBC
- Configuring hypertables and compression
- Setting up retention policies
- Optimizing query performance
- Managing stream offsets for exactly-once processing
- Planning backup and recovery strategies
