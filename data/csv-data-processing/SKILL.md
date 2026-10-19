---
name: csv-data-processing
description: >
  Parse, validate, clean, transform, and export CSV and TSV tabular data
  following RFC 4180. Use when handling delimiter ambiguity (comma, semicolon, tab),
  resolving text encodings (UTF-8, UTF-8-BOM, Latin-1), escaping multi-line quoted
  fields, processing multi-gigabyte files via streaming, or preventing CSV injection.
compatibility: >
  Agent Skills-compatible coding agents processing tabular data across Python,
  command-line tools (csvkit, xsv, duckdb), and shell environments.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "csv, tsv, rfc4180, data-processing, streaming, encoding, duckdb"
  topics: "databases, devtools, software-development"
---

# Robust CSV & TSV Data Processing

Comma-Separated Values (CSV) is the ubiquitous format for tabular data interchange. Despite its apparent simplicity, real-world CSV files suffer from conflicting delimiters, inconsistent quoting, byte-order marks (BOM), encoding mismatches, and security injection vectors. High-integrity CSV processing adheres strictly to [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180) and uses streaming architectures for large datasets.

## Core Rules

1. **Adhere to RFC 4180 quoting rules**: Fields containing delimiters, newlines, or double quotes must be enclosed in double quotes. Literal quotes inside fields are escaped by doubling them (`"He said ""Hello"""`).
2. **Never parse CSV with simple `string.split(',')`**: Line splitting fails on quoted strings containing commas or embedded newlines. Always use dedicated CSV parsers (`csv` module, DuckDB, Polars).
3. **Handle encodings defensively**: Default to `utf-8`. If parsing files originating from Windows/Excel, handle `utf-8-sig` (BOM removal) or detect `latin-1`.
4. **Stream large files line by line or in chunks**: Never call `f.readlines()` or load 10GB CSV files entirely into RAM. Use generator iterators.
5. **Mitigate CSV Formula Injection**: If exporting CSVs that users open in Excel, sanitize cells starting with `=`, `+`, `-`, or `@` by prefixing a single quote (`'`).

---

## 1. Robust Reading with Encoding and Sniffing (Python)

Detect delimiter and handle BOM automatically:

```python
import csv
from pathlib import Path

def stream_csv_records(file_path: Path):
    # Use 'utf-8-sig' to automatically strip UTF-8 Byte Order Marks if present
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        # Sample the first 4KB to sniff delimiter and quote style
        sample = f.read(4096)
        f.seek(0)

        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        has_header = csv.Sniffer().has_header(sample)

        reader = csv.DictReader(f, dialect=dialect) if has_header else csv.reader(f, dialect=dialect)

        for row_num, row in enumerate(reader, start=1):
            yield row_num, row

# Usage:
for row_num, record in stream_csv_records(Path("users.csv")):
    print(f"Row {row_num}: {record}")
```

---

## 2. High-Performance SQL Querying on CSV with DuckDB

Query, filter, and join multi-million row CSV files directly using SQL without loading a database server:

```python
import duckdb

# Query CSV files directly with SQL and export to clean parquet or clean CSV
duckdb.sql("""
    SELECT 
        customer_id,
        country,
        SUM(order_total) AS total_spend,
        COUNT(*) AS transaction_count
    FROM read_csv_auto('orders_*.csv', header=True)
    WHERE status = 'COMPLETED'
    GROUP BY customer_id, country
    HAVING total_spend > 1000
    ORDER BY total_spend DESC
""").write_csv("top_customers.csv")
```

---

## 3. Safe Exporting & Formula Injection Prevention

```python
import csv

def sanitize_csv_cell(value: object) -> str:
    """Prevent Formula Injection in spreadsheet programs."""
    str_val = str(value) if value is not None else ""
    # Characters that trigger formula execution in Excel/Sheets: =, +, -, @, \t, \r
    if str_val and str_val[0] in ("=", "+", "-", "@", "\t", "\r"):
        return f"'{str_val}"
    return str_val

def export_clean_csv(output_path: str, records: list[dict]):
    if not records:
        return

    fieldnames = list(records[0].keys())
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\r\n" # Standard RFC 4180 newline
        )
        writer.writeheader()
        for r in records:
            sanitized = {k: sanitize_csv_cell(v) for k, v in r.items()}
            writer.writerow(sanitized)
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `line.split(',')` | Breaks when a column contains a comma or newline in quotes | Use standard `csv.reader` |
| Missing `newline=""` in Python `open()` | Generates extra blank lines (`\r\r\n`) on Windows | Always specify `open(..., newline="")` with csv module |
| Unsanitized formula characters (`=CMD|' /C calc'!A0`) | Arbitrary code execution when victim opens CSV in Excel | Prefix leading `=`, `+`, `-`, `@` with `'` |
| Overwriting input file during in-place cleanup | Data destroyed if script aborts mid-stream | Write to `.tmp` file and rename atomically |

---

## 5. Verification Checklist

- [ ] File opened with `newline=""` and explicit encoding (`utf-8` / `utf-8-sig`).
- [ ] RFC 4180 quote escaping rules respected.
- [ ] CSV formula injection defense implemented on user-supplied strings.
- [ ] Large files processed via streaming/generators without memory leaks.
- [ ] Record row counts verified against expected line counts.
