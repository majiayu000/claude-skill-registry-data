---
name: pandas
description: Use when analyzing or transforming tabular data in Python. Covers vectorized operations, memory-efficient dtypes, correct joins, groupby patterns, and avoiding the silent errors pandas makes easy.
metadata:
  category: data
  version: 1.0.0
  tags: [pandas, python, dataframe, analysis, polars]
---

# Pandas

## Purpose

Transform and analyze tabular data correctly and at speed. Pandas makes it easy to write code that is slow, and easier still to write code that is silently wrong.

## When to Use

- Cleaning, transforming, or analyzing tabular data in Python.
- A pandas operation that is slow or exhausting memory.
- Reviewing analysis code for correctness.
- Deciding whether the dataset has outgrown pandas.

## Capabilities

- Vectorized operations and eliminating row-wise loops.
- Memory reduction through dtype selection.
- Merge and join semantics, including the ones that silently duplicate rows.
- Groupby, aggregation, and window functions.
- Chunked processing and the migration path to Polars or DuckDB.

## Inputs

- The data source, its size, and its schema.
- The transformation or analysis required.
- The memory available.

## Outputs

- Vectorized transformations with no `iterrows`.
- Explicit dtypes, including categoricals for low-cardinality strings.
- Joins with verified cardinality.

## Workflow

1. **Set dtypes at read time** — Reading a CSV without `dtype` gives you `object` columns and `float64` for everything numeric. This is usually a 5-10x memory difference.
2. **Vectorize** — Any `for` loop or `iterrows` over a DataFrame should be a vectorized expression, a `groupby`, or a `merge`. `apply` is a loop with better syntax.
3. **Verify every join** — `merge(..., validate="one_to_many")`. An unvalidated join that is secretly many-to-many silently multiplies your rows, and the resulting totals will be wrong in a way that is hard to notice.
4. **Aggregate with groupby, not with loops** — And use named aggregation so the output columns are readable.
5. **Chunk or switch when it does not fit** — Pandas holds everything in memory, typically at several times the file size. Above a few gigabytes, use chunked processing, Polars, or DuckDB.

## Best Practices

- `df.iterrows()` is roughly a hundred times slower than the vectorized equivalent and should essentially never appear in production code.
- Chained assignment (`df[df.a > 1]["b"] = 0`) may modify a copy and silently do nothing. Use `.loc[]`. In pandas 3.0 copy-on-write makes this an error rather than a silent no-op — which is an improvement.
- A `merge` without `validate=` is a bet that the join keys are unique. When that bet is wrong, you get more rows than you started with and no warning.
- `category` dtype for a string column with few distinct values can reduce memory by 90% and speeds up groupby substantially.
- `inplace=True` does not save memory (it usually still copies) and prevents method chaining. It has no advantages.
- Read only the columns you need with `usecols`. The cheapest optimization is not loading the data.

## Examples

**Reading efficiently, and joining safely:**

```python
import pandas as pd

orders = pd.read_csv(
    "orders.csv",
    usecols=["order_id", "customer_id", "status", "total_cents", "created_at"],
    dtype={
        "order_id": "string",
        "customer_id": "string",
        "status": "category",        # 4 distinct values: 90% less memory than object
        "total_cents": "int64",
    },
    parse_dates=["created_at"],
)

customers = pd.read_csv("customers.csv", usecols=["customer_id", "segment"],
                        dtype={"customer_id": "string", "segment": "category"})

# validate= turns a silent row explosion into a loud, immediate error.
enriched = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",          # many orders, one customer. Anything else raises.
)
```

**Vectorized instead of looped — and correct:**

```python
# Slow (~100x) and easy to get wrong.
for idx, row in df.iterrows():
    df.at[idx, "band"] = "high" if row["total_cents"] > 10_000 else "low"

# Vectorized, readable, and it does not mutate while iterating.
df["band"] = pd.cut(
    df["total_cents"],
    bins=[0, 10_000, 50_000, float("inf")],
    labels=["low", "mid", "high"],
)

# Named aggregation: the output columns are named, not a MultiIndex to unpick.
summary = (
    df.groupby(["segment", "band"], observed=True)
      .agg(
          order_count=("order_id", "count"),
          revenue_cents=("total_cents", "sum"),
          median_cents=("total_cents", "median"),
      )
      .reset_index()
)
```

## Notes

- `observed=True` on a groupby with categorical keys is important: without it, pandas produces a row for every *possible* category combination, including the ones with no data. On two categoricals with many levels this can generate an enormous, mostly empty frame.
- Polars is typically 5-30x faster than pandas on the same operations, uses less memory, and has a stricter API that catches errors pandas silently permits. For new analysis code on non-trivial data, it is the better default.
- DuckDB queries Parquet and CSV files directly with SQL, without loading them into memory. For "I need one aggregate from a 20 GB file", it is far simpler than any pandas approach.
