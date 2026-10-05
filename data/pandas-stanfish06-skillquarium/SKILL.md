---
name: pandas
description: The workhorse library for in-memory tabular data in Python. Use for loading, cleaning, reshaping, joining, grouping, and analyzing labeled row/column data. Trigger terms include "pandas", "dataframe", "series", "csv", "parquet", "tabular data", "groupby", "pivot", "merge", "data wrangling", "data cleaning". Covers pandas 2.x and the 3.0 changes (Copy-on-Write, default string dtype, PyArrow-backed dtypes).
license: MIT
allowed-tools: Read
metadata: {"version": "1.0", "skill-author": "vault-audit"}
---

# pandas

## Overview

pandas is Python's standard library for labeled, in-memory tabular data. The two core objects are the `Series` (a 1-D labeled array) and the `DataFrame` (a 2-D table of aligned columns sharing a row `Index`). Every operation is index-aligned: arithmetic, joins, and assignments match on labels, not position. Reach for pandas for exploratory analysis, ETL, cleaning, reshaping, and feeding tabular data into plotting, stats, or ML libraries. For datasets that outgrow memory or need columnar speed, see the disambiguation at the end.

## Installation

As of 2026 the current stable major is **pandas 3.0.x** (latest 3.0.5); **2.3.x** is the final 2.x maintenance line. Pin explicitly:

```bash
uv pip install "pandas==3.0.5"
# PyArrow is an optional (not required) dependency; install it for faster
# string/columnar backends and Parquet/Feather IO:
uv pip install "pandas[pyarrow]==3.0.5"
```

```python
import pandas as pd
import numpy as np
```

## Core workflow

### Construct

```python
s = pd.Series([1, 2, 3], index=["a", "b", "c"], name="vals")
df = pd.DataFrame({"g": ["a", "a", "b"], "x": [1, 2, 3], "y": [4.0, np.nan, 6.0]})
```

### IO with dtype control

```python
df = pd.read_csv(
    "data.csv",
    usecols=["id", "amount", "ts"],   # read only what you need
    dtype={"id": "int32", "amount": "float64"},
    parse_dates=["ts"],
    na_values=["", "NA", "null"],
)
df.to_parquet("data.parquet")         # columnar, typed, fast (needs pyarrow)
df2 = pd.read_parquet("data.parquet")

# Opt into Arrow-backed dtypes for the whole frame (requires pyarrow):
dfa = pd.read_csv("data.csv", dtype_backend="pyarrow")
```

### Selection: label vs position, never chained

```python
df.loc[df["x"] > 1, "y"]        # label-based: rows by mask, one column
df.iloc[0:2, [0, 2]]            # integer-position based
df.loc[df["g"].eq("a") & (df["x"] > 0)]   # combine masks with & | ~, parenthesize
df.loc[df["g"].isin(["a", "b"])]
# Assign through a SINGLE .loc — this is the correct, CoW-safe pattern:
df.loc[df["x"] > 1, "y"] = 0.0
```

### groupby: agg, transform, apply

```python
# Named aggregation -> flat, well-named output columns:
df.groupby("g").agg(x_sum=("x", "sum"), y_mean=("y", "mean")).reset_index()

# transform broadcasts the group result back to original row shape:
df["x_grp_total"] = df.groupby("g")["x"].transform("sum")

# Multiple funcs per column:
df.groupby("g")["x"].agg(["min", "max", "count"])
```

### merge / join / concat

```python
pd.merge(left, right, on="id", how="left")              # SQL-style join on columns
pd.merge(left, right, left_on="uid", right_on="id", how="inner")
left.join(right, how="left")                            # join on the index
pd.concat([df1, df2], axis=0, ignore_index=True)        # stack rows
pd.concat([df1, df2], axis=1)                           # align columns by index
```

Always check `merge(..., validate="one_to_many")` and inspect row counts to catch accidental fan-out.

### Reshaping

```python
df.pivot_table(index="g", columns="k", values="x", aggfunc="mean")  # aggregating pivot
df.pivot(index="g", columns="k", values="x")                        # no aggregation, unique keys
df.melt(id_vars="g", value_vars=["x", "y"])   # wide -> long (variable/value cols)
df.set_index("g").stack()                     # columns -> rows (MultiIndex)
wide.unstack()                                # rows -> columns
```

### Missing data

```python
df["y"].isna().sum()
df.dropna(subset=["y"])
df["y"] = df["y"].fillna(df["y"].median())
df["y"] = df["y"].ffill()     # forward-fill (fillna(method=...) was removed)
```

### Vectorize instead of apply

```python
# Prefer vectorized/columnar ops — they run in C, apply() loops in Python:
df["z"] = df["x"] * 2 + df["y"]                     # fast
df["z"] = df["x"].where(df["x"] > 0, 0)             # conditional, vectorized
df["z"] = np.select([df.x > 2, df.x > 0], ["hi", "lo"], default="none")
# Reserve apply for genuinely per-row logic that has no vectorized form:
df["z"] = df.apply(lambda r: custom(r["x"], r["y"]), axis=1)
df2 = df.map(str)   # elementwise over a whole DataFrame (was applymap, removed in 3.0)
```

### Method chaining

```python
result = (
    df
    .assign(z=lambda d: d["x"] * 2)
    .query("x > 1")
    .groupby("g", as_index=False)
    .agg(z_sum=("z", "sum"))
    .sort_values("z_sum", ascending=False)
    .pipe(lambda d: d)          # pipe() slots arbitrary funcs into the chain
)
```

### Datetime

```python
df["ts"] = pd.to_datetime(df["ts"])       # parse; 3.0 may infer datetime64[us]
df["month"] = df["ts"].dt.month           # .dt accessor: year/month/day/hour/dayofweek
df = df.set_index("ts")
df.resample("D")["amount"].sum()          # time-based downsampling (needs datetime index)
df["ts"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
```

## Gotchas / best practices

- **Copy-on-Write (CoW) is the default and only mode in pandas 3.0** — it cannot be disabled (the `mode.copy_on_write` option is deprecated and setting it does nothing). Under CoW, no operation ever mutates data another object shares; you always get predictable copy semantics.
- **Chained indexing assignment silently fails.** `df[df.x > 0]["y"] = 1` modifies a temporary and never touches `df` (it may raise `ChainedAssignmentError`). Always assign through one indexer: `df.loc[df.x > 0, "y"] = 1`. Note the historical `SettingWithCopyWarning` is gone in 3.0 because CoW makes the semantics unambiguous — the fix is the same single-`.loc` rule.
- **Default string dtype changed.** In 3.0, string columns infer as the new `str` (`StringDtype`), not `object`. This is faster and NA-aware. It uses PyArrow when installed and a NumPy fallback otherwise, so the default requires no extra dependency. Code that assumed `object` (e.g. `df.select_dtypes("object")` to grab text, or storing mixed Python objects in a "string" column) may need updating.
- **PyArrow-backed dtypes are opt-in and require PyArrow.** `dtype="int64[pyarrow]"`, `dtype_backend="pyarrow"`, or `df.convert_dtypes(dtype_backend="pyarrow")` raise `ImportError` without PyArrow installed. Reach for them for large text/categorical data, true nullable semantics across all dtypes, faster IO, and zero-copy interchange with Arrow/Polars/DuckDB. The default NumPy backend is fine for typical numeric work.
- **NA vs NaN.** NumPy float columns use `np.nan`; nullable and Arrow dtypes use `pd.NA`. Test with `.isna()` (works for both), never `== np.nan`.
- **Set dtypes at read time**, not after — `dtype=` in `read_csv` avoids a costly object-inference pass and silent upcasting.
- **Reset or name your index** before merging/exporting; unexpected `MultiIndex` or duplicate labels are a frequent source of surprises. Use `df.reset_index(drop=True)` to drop it.
- **Avoid `inplace=True`** — it is not faster under CoW and hurts chaining; reassign instead (`df = df.dropna()`).

## Use this vs related skills

Use **pandas** for in-memory labeled tabular analysis; use **polars** for larger-than-memory or faster columnar/lazy work, **geopandas** for geospatial (geometry) dataframes, and **pandera-validation** for declarative dataframe schema validation.
