---
name: python-data-reviewer
description: |
  WHEN: Pandas/NumPy code review, data processing, vectorization, memory optimization
  WHAT: Vectorization patterns + Memory efficiency + Data validation + Performance optimization + Best practices
  WHEN NOT: Web framework → fastapi/django/flask-reviewer, General Python → python-reviewer
---

# Python Data Reviewer Skill

## Purpose
Reviews data science code for Pandas/NumPy efficiency, memory usage, and best practices.

## When to Use
- Pandas/NumPy code review
- Data processing optimization
- Memory efficiency check
- "Why is my data code slow?"
- ETL pipeline review

## Project Detection
- `pandas`, `numpy` in requirements.txt
- `.ipynb` Jupyter notebooks
- `data/`, `notebooks/` directories
- DataFrame operations in code

## Workflow

### Step 1: Analyze Project
```
**Pandas**: 2.0+
**NumPy**: 1.24+
**Other**: polars, dask, vaex
**Visualization**: matplotlib, seaborn, plotly
**ML**: scikit-learn, xgboost
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full data code review (recommended)
- Vectorization and performance
- Memory optimization
- Data validation
- Code organization
multiSelect: true
```

## Detection Rules

### Vectorization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| iterrows() loop | Use vectorized operations | CRITICAL |
| apply() with simple func | Use built-in vectorized | HIGH |
| Manual loop over array | Use NumPy broadcasting | HIGH |
| List comprehension on Series | Use .map() or vectorize | MEDIUM |

```python
# BAD: iterrows (extremely slow)
for idx, row in df.iterrows():
    df.loc[idx, "total"] = row["price"] * row["quantity"]

# GOOD: Vectorized operation
df["total"] = df["price"] * df["quantity"]

# BAD: apply with simple operation
df["upper_name"] = df["name"].apply(lambda x: x.upper())

# GOOD: Built-in string method
df["upper_name"] = df["name"].str.upper()

# BAD: apply with condition
df["status"] = df["score"].apply(lambda x: "pass" if x >= 60 else "fail")

# GOOD: np.where or np.select
df["status"] = np.where(df["score"] >= 60, "pass", "fail")

# Multiple conditions
conditions = [
    df["score"] >= 90,
    df["score"] >= 60,
    df["score"] < 60,
]
choices = ["A", "B", "F"]
df["grade"] = np.select(conditions, choices)
```

### Memory Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| int64 for small ints | Use int8/int16/int32 | MEDIUM |
| object dtype for categories | Use category dtype | HIGH |
| Loading full file | Use chunks or usecols | HIGH |
| Keeping unused columns | Drop early | MEDIUM |

```python
# BAD: Default dtypes waste memory
df = pd.read_csv("large_file.csv")  # All int64, object

# GOOD: Specify dtypes
dtype_map = {
    "id": "int32",
    "age": "int8",
    "status": "category",
    "price": "float32",
}
df = pd.read_csv("large_file.csv", dtype=dtype_map)

# GOOD: Load only needed columns
df = pd.read_csv(
    "large_file.csv",
    usecols=["id", "name", "price"],
    dtype=dtype_map,
)

# GOOD: Process in chunks
chunks = pd.read_csv("huge_file.csv", chunksize=100_000)
result = pd.concat([process_chunk(chunk) for chunk in chunks])

# Memory check
print(df.info(memory_usage="deep"))

# Convert object to category if low cardinality
for col in df.select_dtypes(include=["object"]).columns:
    if df[col].nunique() / len(df) < 0.5:  # < 50% unique
        df[col] = df[col].astype("category")
```

### Data Validation
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No null check | Validate nulls early | HIGH |
| No dtype validation | Assert expected types | MEDIUM |
| No range validation | Check value bounds | MEDIUM |
| Silent data issues | Raise or log warnings | HIGH |

```python
# GOOD: Data validation function
def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean input DataFrame."""

    # Required columns
    required_cols = ["id", "name", "price", "quantity"]
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Null checks
    null_counts = df[required_cols].isnull().sum()
    if null_counts.any():
        logger.warning(f"Null values found:\n{null_counts[null_counts > 0]}")

    # Type validation
    assert df["id"].dtype in ["int32", "int64"], "id must be integer"
    assert df["price"].dtype in ["float32", "float64"], "price must be float"

    # Range validation
    invalid_prices = df[df["price"] < 0]
    if len(invalid_prices) > 0:
        logger.warning(f"Found {len(invalid_prices)} negative prices")
        df = df[df["price"] >= 0]

    # Duplicate check
    duplicates = df.duplicated(subset=["id"])
    if duplicates.any():
        logger.warning(f"Removing {duplicates.sum()} duplicates")
        df = df.drop_duplicates(subset=["id"])

    return df
```

### NumPy Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Python loop over array | Use broadcasting | CRITICAL |
| np.append in loop | Pre-allocate array | HIGH |
| Repeated array creation | Reuse arrays | MEDIUM |
| Copy when not needed | Use views | MEDIUM |

```python
# BAD: Python loop
result = []
for i in range(len(arr)):
    result.append(arr[i] * 2 + 1)
result = np.array(result)

# GOOD: Vectorized
result = arr * 2 + 1

# BAD: np.append in loop (creates new array each time)
result = np.array([])
for x in data:
    result = np.append(result, process(x))

# GOOD: Pre-allocate
result = np.empty(len(data))
for i, x in enumerate(data):
    result[i] = process(x)

# BETTER: Vectorize if possible
result = np.vectorize(process)(data)

# BEST: Pure NumPy operation
result = np.sqrt(data) + np.log(data)

# BAD: Unnecessary copy
subset = arr[arr > 0].copy()  # copy() often not needed

# GOOD: View when modification not needed
subset = arr[arr > 0]  # Returns view
```

### Pandas Best Practices
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Chained indexing | Use .loc/.iloc | HIGH |
| inplace=True | Assign result instead | MEDIUM |
| reset_index() abuse | Keep index when useful | LOW |
| df.append (deprecated) | Use pd.concat | HIGH |

```python
# BAD: Chained indexing (unpredictable)
df[df["price"] > 100]["status"] = "premium"  # May not work!

# GOOD: Use .loc
df.loc[df["price"] > 100, "status"] = "premium"

# BAD: df.append (deprecated)
result = pd.DataFrame()
for chunk in chunks:
    result = result.append(chunk)

# GOOD: pd.concat
result = pd.concat(chunks, ignore_index=True)

# BAD: Multiple operations creating copies
df = df.dropna()
df = df.reset_index(drop=True)
df = df.sort_values("date")

# GOOD: Method chaining
df = (
    df
    .dropna()
    .reset_index(drop=True)
    .sort_values("date")
)
```

## Response Template
```
## Python Data Code Review Results

**Project**: [name]
**Pandas**: 2.1 | **NumPy**: 1.26 | **Size**: ~1M rows

### Vectorization
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | process.py:45 | iterrows() loop - use vectorized ops |

### Memory
| Status | File | Issue |
|--------|------|-------|
| HIGH | load.py:23 | object dtype for 'status' - use category |

### Data Validation
| Status | File | Issue |
|--------|------|-------|
| HIGH | etl.py:67 | No null value handling |

### NumPy
| Status | File | Issue |
|--------|------|-------|
| HIGH | calc.py:12 | np.append in loop - pre-allocate |

### Recommended Actions
1. [ ] Replace iterrows with vectorized operations
2. [ ] Convert low-cardinality columns to category
3. [ ] Add data validation before processing
4. [ ] Pre-allocate NumPy arrays in loops
```

## Performance Tips
```python
# Profile memory usage
df.info(memory_usage="deep")

# Profile time
%timeit df.apply(func)  # Jupyter magic
%timeit df["col"].map(func)

# Use query() for complex filters
df.query("price > 100 and category == 'A'")

# Use eval() for complex expressions
df.eval("profit = revenue - cost")
```

## Best Practices
1. **Vectorize**: Avoid loops, use broadcasting
2. **Dtypes**: Use smallest sufficient type
3. **Validate**: Check data quality early
4. **Profile**: Measure before optimizing
5. **Chunk**: Process large files incrementally

## Integration
- `python-reviewer`: General Python patterns
- `perf-analyzer`: Performance profiling
- `coverage-analyzer`: Test coverage for data code
