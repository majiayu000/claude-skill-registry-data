---
name: data-analysis
description: "Analyze Excel/CSV files with DuckDB SQL via bash."
allowed-tools:
  - bash
  - read_file
  - write_file
enabled: true
related-skills: [consulting-analysis]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Data Analysis

## Overview

Analyzes user-provided Excel (.xlsx/.xls) or CSV files using DuckDB — an
in-process analytical SQL engine. Supports schema inspection, SQL querying,
statistical summaries, and result export.

> **Poirot note:** The original deer-flow skill uses a bundled
> `scripts/analyze.py` helper. Poirot doesn't bundle that script, so this
> version uses `bash` with `python3` + `duckdb` directly. Install duckdb first:
> `pip install duckdb`.

## When to Use

- User uploads Excel/CSV files and wants analysis
- User wants statistics, summaries, pivot tables, or SQL queries on data
- User wants to filter, join, or aggregate structured data

## Prerequisites

```bash
# Install duckdb if not present
pip install duckdb openpyxl
```

## Workflow

### Step 1: Inspect File Structure

```bash
python3 -c "
import duckdb
con = duckdb.connect()
# For CSV
result = con.execute(\"DESCRIBE SELECT * FROM read_csv_auto('data.csv')\").fetchall()
for col in result:
    print(f'{col[0]:30s} {col[1]}')

# For Excel (each sheet = a table)
result = con.execute(\"SELECT * FROM st_read('data.xlsx', layer='Sheet1') LIMIT 0\").fetchall()

# Row count
count = con.execute(\"SELECT COUNT(*) FROM read_csv_auto('data.csv')\").fetchone()[0]
print(f'Rows: {count}')
"
```

### Step 2: Statistical Summary

```bash
python3 -c "
import duckdb
con = duckdb.connect()
# Describe statistics
print(con.execute(\"SUMMARIZE SELECT * FROM read_csv_auto('data.csv')\").df().to_string())
"
```

### Step 3: SQL Queries

```bash
python3 -c "
import duckdb
con = duckdb.connect()

# Aggregation
result = con.execute('''
    SELECT category, COUNT(*) as count, AVG(price) as avg_price
    FROM read_csv_auto('data.csv')
    GROUP BY category
    ORDER BY count DESC
''').fetchall()
for row in result:
    print(row)

# Join two files
result = con.execute('''
    SELECT a.id, a.name, b.amount
    FROM read_csv_auto('orders.csv') a
    JOIN read_csv_auto('payments.csv') b ON a.id = b.order_id
''').fetchall()
"
```

### Step 4: Export Results

```bash
python3 -c "
import duckdb
con = duckdb.connect()
# Export to CSV
con.execute(\"COPY (SELECT * FROM read_csv_auto('data.csv') WHERE amount > 100) TO 'filtered.csv' (HEADER, DELIMITER ',')\")
# Export to JSON
con.execute(\"COPY (SELECT * FROM read_csv_auto('data.csv')) TO 'output.json' (FORMAT JSON)\")
"
```

## Common Patterns

### Pivot table

```sql
SELECT
    product,
    SUM(CASE WHEN month = 'Jan' THEN amount ELSE 0 END) AS jan,
    SUM(CASE WHEN month = 'Feb' THEN amount ELSE 0 END) AS feb,
    SUM(CASE WHEN month = 'Mar' THEN amount ELSE 0 END) AS mar
FROM read_csv_auto('sales.csv')
GROUP BY product
```

### Percentiles

```sql
SELECT
    percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY price) AS p95
FROM read_csv_auto('data.csv')
```

### Multi-sheet Excel

```bash
python3 -c "
import duckdb
con = duckdb.connect()
# List sheets
sheets = con.execute(\"SELECT table_name FROM st_geometry_tables()\").fetchall()
# Query specific sheet
result = con.execute(\"SELECT * FROM st_read('data.xlsx', layer='Sheet2') LIMIT 10\").fetchall()
"
```

## Pitfalls

- **DuckDB not installed**: `pip install duckdb openpyxl` first
- **Large files**: DuckDB handles large files well, but `SUMMARIZE` on very
  large datasets may be slow. Sample first: `SELECT * FROM ... TABLESAMPLE 10%`
- **Encoding**: CSV with non-UTF-8 encoding may fail. Specify encoding in
  `read_csv_auto` options.
- **Date parsing**: DuckDB auto-detects dates, but ambiguous formats may need
  explicit `strptime` parsing.
- **Excel formulas**: `st_read` reads cell values, not formula results. Use
  `openpyxl` directly if you need computed values.
