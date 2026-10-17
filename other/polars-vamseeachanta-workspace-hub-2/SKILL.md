---
name: polars
version: 1.0.0
description: High-performance DataFrame library for fast data processing with lazy
  evaluation, parallel execution, and memory efficiency
type: reference
author: workspace-hub
category: data-analysis
capabilities:
- Lazy evaluation and query optimization
- Parallel processing on all CPU cores
- Memory-efficient operations for large datasets
- Expression-based API for complex transformations
- Streaming processing for out-of-memory datasets
- Zero-copy data sharing with Arrow
tools:
- polars
- pyarrow
- connectorx
tags:
- polars
- dataframe
- performance
- parallel
- lazy-evaluation
- arrow
- rust
- data-processing
platforms:
- python
- rust
related_skills:
- pandas-data-processing
- numpy-numerical-analysis
- streamlit
- dash
requires: []
scripts_exempt: true
---

# Polars

## When to Use This Skill

### USE Polars when:

- **Large datasets** - Working with data too large for pandas (10GB+)
- **Performance critical** - Need maximum speed for data transformations
- **Memory constrained** - Limited RAM requires efficient memory usage
- **Parallel processing** - Want to utilize all CPU cores automatically
- **Complex aggregations** - Group by, window functions, rolling calculations
- **Lazy evaluation** - Query optimization before execution matters
- **ETL pipelines** - Building production data pipelines
- **Streaming data** - Processing data larger than memory
### DON'T USE Polars when:

- **Pandas ecosystem required** - Need specific pandas-only libraries
- **Small datasets** - Under 100MB where pandas is sufficient
- **Legacy code** - Extensive existing pandas codebase
- **Matplotlib/Seaborn direct integration** - These work better with pandas
- **Time series with specialized needs** - Some pandas time series features are more mature

## Prerequisites

```bash
# Basic installation
pip install polars

# With all optional dependencies
pip install 'polars[all]'

# Specific extras
pip install 'polars[numpy,pandas,pyarrow,fsspec,connectorx,xlsx2csv,deltalake,timezone]'

# Using uv (recommended)
uv pip install polars pyarrow connectorx
```

## Complete Examples

### Example 1: ETL Pipeline for Sales Data

```python
import polars as pl
from pathlib import Path
from datetime import datetime

def etl_sales_pipeline(
    input_dir: Path,
    output_dir: Path,
    min_date: str = "2025-01-01"
) -> dict:

*See sub-skills for full details.*
### Example 2: Time Series Analysis

```python
import polars as pl
import numpy as np
from datetime import datetime, timedelta

def analyze_time_series(
    df: pl.DataFrame,
    value_column: str,
    time_column: str,
    group_column: str = None

*See sub-skills for full details.*
### Example 3: Large-Scale Data Processing with Streaming

```python
import polars as pl
from pathlib import Path
import time

def process_large_dataset(
    input_pattern: str,
    output_path: str,
    chunk_report_every: int = 1_000_000
) -> dict:

*See sub-skills for full details.*

## Version History

- **1.0.0** (2026-01-17): Initial release with comprehensive Polars coverage
  - Core DataFrame operations
  - Lazy evaluation patterns
  - Expression API reference
  - GroupBy and window functions
  - Join operations
  - ETL pipeline examples
  - Time series analysis
  - Streaming for large datasets
  - Integration examples
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://docs.pola.rs/
- **User Guide**: https://docs.pola.rs/user-guide/
- **API Reference**: https://docs.pola.rs/api/python/stable/reference/
- **GitHub**: https://github.com/pola-rs/polars
- **Cookbook**: https://docs.pola.rs/user-guide/misc/cookbook/

---

**Use Polars for maximum performance on large datasets with intuitive, expressive data transformations!**

## Sub-Skills

- [1. DataFrame Creation and I/O](1-dataframe-creation-and-io/SKILL.md)
- [2. Lazy Evaluation and Query Optimization](2-lazy-evaluation-and-query-optimization/SKILL.md)
- [3. Expression API](3-expression-api/SKILL.md)
- [4. GroupBy and Aggregations (+1)](4-groupby-and-aggregations/SKILL.md)
- [6. Joins and Concatenation](6-joins-and-concatenation/SKILL.md)
- [Polars with Plotly Visualization (+1)](polars-with-plotly-visualization/SKILL.md)
- [1. Use Lazy Evaluation by Default (+4)](1-use-lazy-evaluation-by-default/SKILL.md)
- [Common Issues](common-issues/SKILL.md)
