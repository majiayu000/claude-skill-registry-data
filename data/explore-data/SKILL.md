---
name: explore-data
description: "Explores data in a Bauplan lakehouse safely using the Bauplan Python SDK. Use to inspect namespaces, tables, schemas, samples, and profiling queries; and to export larger result sets to files. Read-only exploration only; no writes or pipeline runs."
allowed-tools:
  - Bash(bauplan:*)
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Exploring Data in Bauplan

This skill is for exploring and understanding data stored in a Bauplan lakehouse using the Bauplan Python SDK. It is intended for analysis, validation, and data exploration. It must not be used to mutate data or run pipelines.

The Python SDK is preferred over the CLI for exploration because it can return richer metadata objects and can export larger query results to files instead of truncating output in the terminal.

Create a temporary folder in the project called `data-exploration` in which you can create a Python file named `data_explorer.py` and use that to iterate on the code to explore the data.

## Scope and Safety Guarantees

This skill is read-only by construction.

Allowed:

* List namespaces and tables
* Inspect table schemas and metadata
* Preview rows
* Run ad-hoc SELECT queries, including JOINS 
* Compute basic stats and distributions
* Export query results to CSV, Parquet, or JSON for offline inspection

Not allowed:

* Create or modify tables
* Import data
* Run pipelines
* Merge branches
* Any write or publish operation

If the user asks for any operation that writes data, stop and suggest switching to a write-capable skill (for example WAP or creating-bauplan-pipelines).


## Branch and Ref Context

All reads MUST be scoped to a ref (branch name or ref object, also optionally tag and namespace). 

In the Python SDK, most read APIs take `ref=` or `branch=`. ALWAYS make the ref explicit in code; NEVER rely on implicit defaults.

Before starting YOU MUST ask the user what branch(es) and ref(s) she intends to explore.

The examples below use `ref="<ref_to_explore>"`.

## Minimal Setup

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
```

The exact authentication mechanism depends on the user environment (profile vs API key), but `bauplan.Client()` is the entry point.

## Typical Exploration Workflow

1. Pick the branch or ref to explore.
2. Discover namespaces and tables.
3. Inspect schemas and metadata for candidate tables.
4. Preview small samples.
5. Run targeted profiling queries.
6. (optional) Export larger results to files when needed.

## Discover Namespaces

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
namespaces = list(client.get_namespaces(ref=ref))
```

You can filter and limit if you want to keep results small.

## Discover Tables

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
tables_resp = client.get_tables(ref=ref, filter_by_namespace="bauplan")  # optional filter
tables = list(client.get_tables(ref=ref, filter_by_namespace="bauplan"))
```

Use `filter_by_name` and `limit` when exploring large catalogs.

## Inspect Table Schema and Metadata

Use this to answer: does a table exist, what are the fields, how many records.

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
exists = client.has_table(table="my_table", ref=ref)
table = client.get_table(table="my_table", namespace="bauplan", ref=ref)
num_records = table.records
fields = [(c.name, c.type) for c in table.fields]
```

If you need raw Iceberg metadata for debugging, request it explicitly:

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
table = client.get_table(table="my_table", namespace="bauplan", ref=ref, include_raw=True)
raw_metadata = table.raw  # name may differ; inspect the returned object
```

`get_table` is the authoritative source for schema and core metadata on a given ref.

## Preview Rows Safely

Use queries with explicit column selection and a small LIMIT.

```python
import bauplan

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
q = """
SELECT col1, col2, col3
FROM bauplan.my_table
LIMIT 10
"""
res = client.query(q, ref=ref, max_rows=10)
```

Use `max_rows` as an additional guardrail in the SDK.

Rules:

* Always use LIMIT and select explicit columns.
* DO NOT EVER run unbounded queries.
* ALWAYS AVOID wide scans when a filter can reduce data early.

## Preview Rows as DataFrames
Bauplan query method returns a class pyarrow.lib.Table. When useful, use DataFrame libraries like Pandas or Polars to facilitate visualization or manipulation of the tables:

### Polars 
Polars is the cleanest next step because it consumes Arrow zero-copy.

```python
import bauplan
import polars as pl

client = bauplan.Client()
ref = "<ref_to_explore>"  # branch name or ref object
q = """
SELECT col1, col2, col3
FROM bauplan.my_table
LIMIT 10
"""
res = client.query(q, ref=ref, max_rows=10)
df = pl.from_arrow(res.to_arrow())
print(df)

```

### Arrow
Useful when you only need schema or batches.

```python
import bauplan

client = bauplan.Client()

q = """
SELECT col1, col2, col3
FROM bauplan.my_table
LIMIT 10
"""
res = client.query(q, ref=ref, max_rows=10)

table = res.to_arrow()
print(table.schema)
print(table.num_rows)

```

### Pandas
```python

import bauplan
import pandas 

client = bauplan.Client()

q = """
SELECT col1, col2, col3
FROM bauplan.my_table
LIMIT 10
"""
res = client.query(q, ref=ref, max_rows=10)

df = res.to_pandas() 
print(df.head())
```

## Basic Profiling Queries

Row count:

```python
res = client.query("SELECT COUNT(*) AS n FROM bauplan.my_table", ref=ref, max_rows=1)
```

Null rate:

```python
q = """
SELECT
  COUNT(*) AS total_rows,
  COUNT(user_id) AS non_null_user_id
FROM bauplan.my_table
"""
res = client.query(q, ref=ref, max_rows=1)
```

Top values:

```python
q = """
SELECT status, COUNT(*) AS n
FROM bauplan.my_table
GROUP BY status
ORDER BY n DESC
LIMIT 20
"""
res = client.query(q, ref=ref, max_rows=20)
```

Time range:

```python
q = """
SELECT MIN(event_time) AS min_t, MAX(event_time) AS max_t
FROM bauplan.my_table
"""
res = client.query(q, ref=ref, max_rows=1)
```

The SDK query API supports `ref` scoping and `max_rows`. ([docs.bauplanlabs.com][1])

## Export Larger Results to Files

When terminal output or in-memory objects are too limiting, export results to a file and inspect locally.

CSV export:

```python
client.query_to_csv_file(
  path="results.csv",
  query="SELECT * FROM bauplan.my_table WHERE event_date >= '2026-01-01'",
  ref=ref,
  max_rows=1_000_000,
)
```

Parquet export (preferred for large results):

```python
client.query_to_parquet_file(
  path="results.parquet",
  query="SELECT * FROM bauplan.my_table WHERE event_date >= '2026-01-01'",
  ref=ref,
  max_rows=10_000_000,
)
```

JSON/JSONL export:

```python
client.query_to_json_file(
  path="results.jsonl",
  query="SELECT * FROM bauplan.my_table LIMIT 10000",
  file_format="jsonl",
  ref=ref,
  max_rows=10_000,
)
```

These file-writing helpers exist specifically to handle larger result sets beyond what the CLI is comfortable with.

## Comparing Data Across Refs

There is no “checkout” in Python. Instead, run the same operation twice with different `ref=` and compare.

Example: compare row counts:

```python
q = "SELECT COUNT(*) AS n FROM bauplan.my_table"

n_main = client.query(q, ref="main", max_rows=1)
n_dev = client.query(q, ref="<username>.<branch>", max_rows=1)
```

Example: compare schemas:

```python
t_main = client.get_table("my_table", namespace="bauplan", ref="main")
t_dev  = client.get_table("my_table", namespace="bauplan", ref="<username>.<branch>")

schema_main = [(c.name, c.type) for c in t_main.fields]
schema_dev  = [(c.name, c.type) for c in t_dev.fields]
```

Never claim equality between branches without checking both schema and at least one data-level signal.

## Interpreting Results

When reporting results:

* State the branch and table explicitly.
* Distinguish facts from assumptions.
* Do not infer business meaning unless the user asks.
* Highlight anomalies clearly (unexpected nulls, empty tables, schema drift).
* Avoid speculation. If data is insufficient, say so.
* Avoid business interpretation unless the user explicitly asked for it.



## When to Stop Exploration

Stop and ask for confirmation if:

* The user’s next step implies writing data.
* The exploration reveals missing or inconsistent inputs.
* Source tables required for a pipeline do not exist.
* The user’s stated goal conflicts with observed data shape.

At that point, recommend switching to pipeline creation or revision.

## Final Output: Structured Summary (Required)

At the end of the exploration, generate a structured textual summary in Markdown.
This summary is the default final output unless the user explicitly requests a different format (for example, a file export).

The summary MUST:

- Clearly state the ref(s) and branche(s) that were explored.
- List the tables inspected, grouped by namespace. 
- For each table, include: Table name, Approximate row count (if available), Key columns and their types (omit extremely wide schemas; show only relevant or representative columns), Partitioning (if any), Notable observations (null-heavy columns, empty tables, schema drift, unexpected types, missing keys), Explicitly separate observations (facts derived from inspection) from assumptions or hypotheses (if any).

The summary MUST NOT:

- Include raw row values beyond illustrative examples already discussed.
- Include exported files or links unless explicitly requested.
- Speculate about intent, semantics, or downstream usage.

This Markdown summary should be concise, factual, and readable by a human, and serve as a handoff artifact for subsequent steps such as pipeline design or data validation.
