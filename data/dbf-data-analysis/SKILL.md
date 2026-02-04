---
name: DBF Data Analysis
description: This skill should be used when the user asks to "analyze DBF files", "read DBF data", "query DBF database", "convert DBF to Parquet", "analyze Thai accounting data", "explore legacy database", "run DuckDB queries on DBF", or mentions DBF, Parquet conversion, or Thai legacy accounting systems. Provides comprehensive guidance for reading, converting, and analyzing Thai legacy DBF accounting databases.
---

# DBF Data Analysis

Toolkit for analyzing Thai legacy DBF accounting databases using roonpoo, Parquet, and DuckDB.

## Overview

This skill enables analysis of legacy Thai accounting systems that use DBF (dBase) files with TIS-620/CP874 encoding. The workflow involves:

1. **Reading DBF** - Use roonpoo library to read DBF files with proper Thai encoding
2. **Converting to Parquet** - Transform DBF to columnar Parquet format for efficient querying
3. **Querying with DuckDB** - Run SQL analytics on Parquet files

## Environment Setup

Before starting analysis, ensure the roonpoo library is available:

```bash
cd libs/python
uv sync
```

For Parquet conversion and DuckDB queries:
```bash
uv pip install pyarrow duckdb
```

## Reading DBF Files

### Basic Usage with roonpoo

```python
from roonpoo import DBF

# Stream records (memory-efficient)
for record in DBF('path/to/file.DBF', encoding='tis-620'):
    print(record)

# Preload all records
table = DBF('path/to/file.DBF', encoding='tis-620', preload=True)
print(table.records[0])
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `encoding` | Use `'tis-620'` or `'cp874'` for Thai text |
| `preload` | Load all records into memory |
| `ignore_missing_memo` | Skip if .FPT/.DBT memo file missing |
| `char_decode_errors` | `'strict'`, `'ignore'`, or `'replace'` |

### Inspect Table Structure

```python
table = DBF('file.DBF', encoding='tis-620')

# Metadata
print(f"Version: {table.dbversion}")
print(f"Last modified: {table.date}")
print(f"Records: {table.header.numrecords}")

# Fields
for field in table.fields:
    print(f"{field.name}: type={field.type}, len={field.length}")
```

### Field Types

| Type | Description |
|------|-------------|
| C | Character (string) |
| N | Numeric |
| D | Date |
| L | Logical (boolean) |
| M | Memo (requires .FPT/.DBT) |

## Converting DBF to Parquet

Use the conversion script at `scripts/dbf_to_parquet.py`:

```bash
uv run python scripts/dbf_to_parquet.py /path/to/DATA/*.DBF -o /path/to/output/
```

Or inline:

```python
from roonpoo import DBF
import pyarrow as pa
import pyarrow.parquet as pq
from decimal import Decimal

def convert_dbf_to_parquet(dbf_path, output_path):
    table = DBF(dbf_path, encoding='tis-620', char_decode_errors='replace')
    records = list(table)

    columns = {f.name: [] for f in table.fields}
    for rec in records:
        for field in table.fields:
            val = rec.get(field.name)
            if isinstance(val, Decimal):
                val = float(val)
            columns[field.name].append(val)

    arrow_table = pa.table(columns)
    pq.write_table(arrow_table, output_path)
    return len(records)
```

## Querying with DuckDB

### Setup

```python
import duckdb
con = duckdb.connect()
parquet_dir = 'path/to/parquet/files'
```

### Common Query Patterns

**Query single file:**
```sql
SELECT * FROM 'asParquet/ARMST.parquet' LIMIT 10
```

**List all tables with row counts:**
```sql
SELECT
    replace(filename, 'path/', '') as file,
    count(*) as rows
FROM parquet_scan('asParquet/*.parquet', filename=true)
GROUP BY filename
ORDER BY rows DESC
```

**Cross-table JOIN:**
```sql
SELECT
    a.ACCID,
    m.COMP,
    COUNT(*) as txn_count
FROM 'asParquet/ARTR.parquet' a
JOIN 'asParquet/ARMST.parquet' m ON a.ACCID = m.ACCID
GROUP BY a.ACCID, m.COMP
ORDER BY txn_count DESC
```

**Schema inspection:**
```sql
DESCRIBE SELECT * FROM 'asParquet/ARTR.parquet'
```

## Common Thai Accounting Tables

| Table | Description | Key Fields |
|-------|-------------|------------|
| ARMST | Customer master | ACCID, COMP, NAME, TEL |
| APMST | Vendor master | ACCID, COMP, NAME |
| ARTR | AR transactions | DOCNO, DATEDOC, ACCID, AMOUNT |
| APTR | AP transactions | DOCNO, DATEDOC, ACCID, AMOUNT |
| GLTR | GL transactions | GLID, DEBIT, CREDIT |
| GLTRHD | GL headers | DOCNO, DATEDOC |
| INVLOC | Inventory location | PCODE, LOCID, QTY |

## Workflow Example

Complete analysis workflow:

```python
from roonpoo import DBF
from pathlib import Path
import duckdb

# 1. Explore DBF structure
data_dir = Path('sample_company/ALLDATA/DATA2011')
for dbf_file in sorted(data_dir.glob('*.DBF'))[:5]:
    table = DBF(dbf_file, encoding='tis-620')
    print(f"{dbf_file.name}: {table.header.numrecords} records")

# 2. Convert key tables to Parquet
# (use scripts/dbf_to_parquet.py)

# 3. Query with DuckDB
con = duckdb.connect()
result = con.execute("""
    SELECT GLID, SUM(DEBIT) as total_debit, SUM(CREDIT) as total_credit
    FROM 'asParquet/GLTR.parquet'
    GROUP BY GLID
    ORDER BY total_debit DESC
    LIMIT 10
""").fetchdf()
print(result)
```

## Handling Encoding Issues

For files with encoding problems:

```python
# Replace invalid characters
table = DBF('file.DBF', encoding='tis-620', char_decode_errors='replace')

# Or ignore them
table = DBF('file.DBF', encoding='tis-620', char_decode_errors='ignore')
```

## Additional Resources

### Scripts
- **`scripts/dbf_to_parquet.py`** - Batch convert DBF files to Parquet
- **`scripts/inspect_dbf.py`** - Inspect DBF structure and sample data

### References
- **`references/table-schemas.md`** - Common Thai accounting table schemas
- **`references/query-patterns.md`** - Advanced DuckDB query patterns
