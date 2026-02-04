---
name: duckdb-remote-parquet-query
description: Query remote Parquet files via HTTP without downloading using DuckDB httpfs. Leverage column pruning, row filtering, and range requests for efficient bandwidth usage. Use for crypto/trading data distribution and analytics.
---

# DuckDB Remote Parquet Query

## Overview

This skill teaches how to query remote Parquet files over HTTP/HTTPS without downloading the entire file, using DuckDB's httpfs extension. This pattern is essential for distributing large datasets (crypto OHLCV data, trade history, orderbook snapshots) while allowing users to run filtered queries with minimal bandwidth.

**Core Pattern**: DuckDB httpfs extension → HTTP range requests → Column/row pruning → Query only needed data

**Use Cases**:
- Query 20 MB Parquet database to get 1 symbol's history (downloads ~60 KB vs 20 MB)
- Aggregate daily statistics without downloading raw tick data
- Explore schema and sample data before committing to full download
- Build APIs that serve filtered subsets from static Parquet files

## When to Use This Skill

Use this skill when you need to:

1. **Distribute Data** - Serve Parquet files to users without building a backend API
2. **Query Large Files** - Access specific rows/columns from multi-GB Parquet files
3. **Minimize Bandwidth** - Users on slow networks or metered connections
4. **Optimize Documentation** - Show users how to query your published datasets efficiently
5. **Prototype APIs** - Test query patterns before building dedicated infrastructure

**Common Questions**:
- "How do I let users query my Parquet database without downloading it?"
- "What's the most efficient way to serve historical OHLCV data?"
- "Can DuckDB query GitHub Releases directly?"
- "How do I reduce query latency for remote Parquet files?"

## Quick Start

### Prerequisites

```bash
# Install DuckDB (Python)
pip install duckdb>=1.0.0

# Or install DuckDB CLI
brew install duckdb  # macOS
```

### Minimal Example

```python
import duckdb

# 1. Setup connection with httpfs extension
conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs")
conn.execute("LOAD httpfs")

# 2. Query remote Parquet file (replace URL)
url = "https://cdn.jsdelivr.net/gh/org/repo@tag/data.parquet"

result = conn.execute(f"""
    SELECT date, symbol, close_price
    FROM read_parquet('{url}')
    WHERE symbol = 'BTCUSDT'
      AND date >= '2024-01-01'
    LIMIT 10
""").fetchall()

# Network transfer: ~60 KB (not full 20 MB file!)
for row in result:
    print(row)
```

**Key Points**:
- No full download required (uses HTTP range requests)
- Column pruning: Only reads `date`, `symbol`, `close_price` columns
- Row filtering: WHERE clause skips irrelevant row groups
- Works with any HTTP/HTTPS URL serving Parquet files

## Core Concepts

### HTTP Range Requests

DuckDB's httpfs extension uses HTTP `Range: bytes=X-Y` headers to read only required portions of Parquet file:

1. **Metadata read** - Fetch file footer (< 10 KB) to understand schema and row groups
2. **Column chunks** - Download only requested columns from relevant row groups
3. **Row groups** - Skip row groups outside WHERE filter range

**Example**:
- Parquet file: 20 MB, 1M rows, 20 columns
- Query: `SELECT date FROM table WHERE symbol = 'BTCUSDT'` (1 of 327 symbols)
- Network transfer: ~60 KB (0.3% of file size)

**Requirements**:
- Server must return `Accept-Ranges: bytes` header
- Works with: S3, GCS, Azure Blob, CDNs (jsDelivr, Cloudflare)
- **Doesn't work**: GitHub Releases direct URLs (use jsDelivr proxy)

### Column Pruning

Only downloads columns referenced in SELECT/WHERE/ORDER BY:

```sql
-- Bad: Downloads all 20 columns
SELECT * FROM read_parquet('https://example.com/data.parquet')

-- Good: Downloads only 3 columns (85% bandwidth reduction)
SELECT date, symbol, volume FROM read_parquet('https://example.com/data.parquet')
```

### Predicate Pushdown

DuckDB pushes WHERE filters to Parquet reader, skipping entire row groups:

```sql
-- Skips row groups where date < '2024-01-01'
SELECT * FROM read_parquet('https://example.com/data.parquet')
WHERE date >= '2024-01-01'  -- Filter pushed to Parquet reader
```

**Best filters** (highest selectivity):
- Date ranges (if Parquet sorted by date)
- Equality: `symbol = 'BTCUSDT'`
- IN clauses: `symbol IN ('BTCUSDT', 'ETHUSDT')`

## Using Bundled Resources

### `scripts/remote_query_example.py`

Comprehensive working examples demonstrating:

1. **Basic queries** - Count rows, schema inspection
2. **Column pruning** - SELECT specific columns to reduce bandwidth
3. **Row filtering** - WHERE clauses with predicate pushdown
4. **Aggregations** - Remote grouping to minimize network transfer
5. **Performance comparison** - Measure speedup from optimization
6. **Local caching** - Download filtered subset once, query many times
7. **Export** - Save filtered data to local Parquet/CSV

**Usage**:
```bash
# View examples
cat skills/duckdb-remote-parquet-query/scripts/remote_query_example.py

# Run examples (replace URL first!)
python skills/duckdb-remote-parquet-query/scripts/remote_query_example.py
```

**Copy-paste friendly**: Each function is self-contained, can be adapted to your use case.

### `references/performance-optimization.md`

In-depth guide covering:

- **Optimization patterns** - Column pruning, predicate pushdown, aggregation before export
- **Performance benchmarks** - Bandwidth/latency for different query types
- **Troubleshooting** - Diagnose slow queries, high bandwidth usage
- **CDN proxy setup** - Use jsDelivr for GitHub Releases (no native range support)
- **Configuration tuning** - HTTP timeout, retries, memory limits

**Usage**: Reference when optimizing query performance or troubleshooting issues.

## Workflow

### Step 1: Verify Server Supports Range Requests

```bash
# Check HTTP headers
curl -I https://example.com/data.parquet

# Look for:
# HTTP/1.1 200 OK
# Accept-Ranges: bytes  ← Required for efficient queries
```

**If missing**: Use CDN proxy (jsDelivr, Cloudflare) or download full file.

### Step 2: Install and Load httpfs Extension

```python
import duckdb

conn = duckdb.connect(":memory:")  # Or persistent: "local.duckdb"
conn.execute("INSTALL httpfs")    # Download extension (once)
conn.execute("LOAD httpfs")       # Load into connection
```

### Step 3: Inspect Schema (Optional but Recommended)

```python
url = "https://cdn.jsdelivr.net/gh/org/repo@tag/data.parquet"

# Check available columns and types
schema = conn.execute(f"""
    DESCRIBE SELECT * FROM read_parquet('{url}')
""").fetchall()

for col in schema:
    print(f"{col[0]:<20} {col[1]:<15}")  # column_name, type
```

**Why**: Avoid trial-and-error queries, plan optimal SELECT statement.

### Step 4: Write Optimized Query

**Checklist**:
- ✅ SELECT only needed columns (not `SELECT *`)
- ✅ WHERE filter on high-selectivity columns (date, symbol)
- ✅ Aggregate remotely if possible (GROUP BY reduces network transfer)
- ✅ LIMIT with WHERE filter (avoid ORDER BY without filter)

**Example**:
```python
result = conn.execute(f"""
    SELECT date, symbol, volume, close_price
    FROM read_parquet('{url}')
    WHERE symbol = 'BTCUSDT'
      AND date >= '2024-01-01'
    ORDER BY date DESC
    LIMIT 100
""").fetchall()
```

### Step 5: Cache Locally if Repeated Queries

```python
# Download filtered subset once
conn.execute(f"""
    CREATE TABLE local_cache AS
    SELECT *
    FROM read_parquet('{url}')
    WHERE date >= '2024-01-01'
      AND symbol IN ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')
""")

# Run many queries on local table (fast, no network)
counts = conn.execute("SELECT symbol, COUNT(*) FROM local_cache GROUP BY symbol").fetchall()
trends = conn.execute("SELECT date, AVG(volume) FROM local_cache GROUP BY date").fetchall()
```

**When to cache**:
- Running >3 queries on same data
- Interactive exploration (Jupyter notebooks)
- Dashboards that refresh frequently

### Step 6: Export Results

```python
# Export to Parquet
conn.execute("""
    COPY (SELECT * FROM local_cache)
    TO '/tmp/filtered_data.parquet' (FORMAT PARQUET)
""")

# Export to CSV
conn.execute("""
    COPY (SELECT * FROM local_cache)
    TO '/tmp/filtered_data.csv' (HEADER, DELIMITER ',')
""")
```

## Domain Context: Crypto/Trading Data

This skill is optimized for:

**Data Types**:
- OHLCV klines (1m, 5m, 1h, 1d bars)
- Trade ticks (timestamp, price, quantity, side)
- Orderbook snapshots (bid/ask levels, depths)
- Funding rates, liquidations, open interest
- Availability/coverage metadata (which symbols have data for which dates)

**Common Patterns**:
- **Symbol filtering**: `WHERE symbol IN (...)` (1 of 300+ symbols → 99% data skipped)
- **Date ranges**: `WHERE date BETWEEN '2024-01-01' AND '2024-12-31'`
- **Volume thresholds**: `WHERE volume > 1000000` (filter low-liquidity periods)
- **Aggregations**: Daily/hourly rollups from minute data

**Performance Examples** (20 MB Parquet, 327 symbols, 2019-2025 history):
- Full scan: 20 MB download, 3.0s
- Single symbol: 60 KB download, 0.3s (10x faster)
- Daily aggregation: 10 KB download, 0.2s (15x faster)

## Tips for Success

1. **Always SELECT specific columns** - `SELECT *` defeats purpose of remote queries
2. **Test filters for selectivity** - `symbol = 'BTCUSDT'` (high) vs `volume > 0` (low)
3. **Aggregate remotely** - `GROUP BY date` reduces network transfer 100-1000x
4. **Use CDN proxy for GitHub Releases** - jsDelivr adds range request support
5. **Cache locally for exploration** - Download once, query many times
6. **Check schema first** - `DESCRIBE SELECT *` shows available columns without data transfer
7. **Monitor bandwidth** - Compare query time to verify optimization working

## Common Pitfalls to Avoid

1. **Using SELECT *** - Downloads all columns, wastes bandwidth
2. **ORDER BY without WHERE** - Sorts entire file (downloads everything)
3. **Repeated identical queries** - Cache locally after first query
4. **Low-selectivity filters** - `WHERE volume > 0` doesn't skip row groups
5. **GitHub Releases direct URLs** - Don't support range requests, use jsDelivr proxy
6. **HTTP instead of HTTPS** - Some CDNs require HTTPS for range support
7. **No error handling** - Network failures should raise, not return empty results

## Troubleshooting

### Query downloads full file (not using range requests)

**Diagnose**:
```bash
curl -I https://your-url/data.parquet | grep "Accept-Ranges"
```

**Solutions**:
- If no `Accept-Ranges: bytes`: Use CDN proxy (jsDelivr)
- If HTTP: Switch to HTTPS
- If GitHub Releases: Use `https://cdn.jsdelivr.net/gh/org/repo@tag/file.parquet`

### Query is slow (>5 seconds for small result)

**Diagnose**:
```sql
EXPLAIN SELECT ... FROM read_parquet('url') WHERE ...
```

**Solutions**:
- Add explicit column list (not `SELECT *`)
- Add WHERE filter on date/symbol
- Check network speed: `curl -w "@curl-format.txt" URL`

### DuckDB can't find httpfs extension

**Solution**:
```python
# Install extension manually
conn.execute("INSTALL httpfs FROM 'https://extensions.duckdb.org'")
conn.execute("LOAD httpfs")
```

### Memory error on large queries

**Solution**:
```sql
SET memory_limit = '4GB';  -- Increase limit (default: 80% of RAM)
```

## Real-World Example: Binance Futures Availability

```python
import duckdb

# Setup
conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs; LOAD httpfs")

# Query availability database (327 symbols, 2019-2025, 20 MB file)
url = "https://cdn.jsdelivr.net/gh/org/binance-futures@v1.0.0/availability.parquet"

# Get BTCUSDT availability for 2024 (downloads ~60 KB vs 20 MB)
result = conn.execute(f"""
    SELECT date, is_available, file_size_bytes
    FROM read_parquet('{url}')
    WHERE symbol = 'BTCUSDT'
      AND date >= '2024-01-01'
    ORDER BY date
""").fetchall()

# Calculate uptime percentage
total_days = len(result)
available_days = sum(1 for row in result if row[1])
uptime_pct = 100.0 * available_days / total_days

print(f"BTCUSDT availability in 2024: {uptime_pct:.2f}% ({available_days}/{total_days} days)")
```

**Performance**:
- Network transfer: ~60 KB (0.3% of file)
- Query time: 0.3s (cold), 0.1s (warm)
- Bandwidth savings: 99.7%
