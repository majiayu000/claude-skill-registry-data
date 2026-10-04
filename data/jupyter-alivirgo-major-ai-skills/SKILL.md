---
name: jupyter
description: "Build reproducible Jupyter notebooks, manage kernels and execution order, and parameterize runs with papermill."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["jupyter", "notebooks", "python", "reproducibility", "papermill", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Jupyter Notebooks AI Skill Guide

## Overview & Engine Architecture

Jupyter runs code cells against a kernel (usually IPython) with persistent in-memory state. The `.ipynb` JSON stores inputs, outputs, and metadata. Agents keep notebooks linear and restartable, parameterize with papermill when automating, and extract durable logic into `.py` modules once paths stabilize.

```
Notebook UI / VS Code / JupyterLab
      -> kernel (Python/R/Julia)
          -> cells mutate namespace
          -> outputs embedded in .ipynb
```

## When to use this skill

- Exploratory analysis and teaching demos
- Lightweight reports with plots/tables
- Parameterized batch runs via papermill/nbconvert

## Operational directives

1. "Restart kernel & run all" must succeed before sharing or committing.
2. Put secrets in env vars / keyring - never in cells that get committed.
3. Clear oversized outputs before git commits (or use nbstripout).
4. Import project modules instead of duplicating production ETL in cells.
5. Pin kernel/env (`requirements.txt` / conda lock) beside the notebook.

## Minimal reproducible header

```python
# cell 0
from pathlib import Path
import pandas as pd

DATA = Path("data/orders.parquet")
assert DATA.exists(), f"missing {DATA}"

df = pd.read_parquet(DATA)
df.head()
```

## Papermill parameter cell

```python
# tags: parameters
run_date = "2026-08-26"
input_path = "data/orders.parquet"
```

```bash
papermill analysis.ipynb out/analysis_2026-08-26.ipynb -p run_date 2026-08-26
jupyter nbconvert --to html out/analysis_2026-08-26.ipynb
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Works only top-down once | hidden state / out-of-order run | restart & run all |
| Huge git diffs | embedded outputs/images | strip outputs; LFS if needed |
| Wrong package | multiple kernels/envs | select correct kernel; document |
| Kernel dies | memory spike | sample data; move to DuckDB/Polars |

## Best practices

- One narrative per notebook; split mega-notebooks by stage.
- Freeze random seeds when illustrating ML (`@scikit-learn`, `@pytorch`).
- Prefer Parquet inputs over pasted CSVs in repo.
- Use `%matplotlib inline` / explicit `plt.show` consistently for readers.

## Limitations

- Not a production scheduler - wrap with `@airflow` / `@prefect` for pipelines.
- Collaborative merge conflicts on `.ipynb` are painful; prefer scripts for shared logic.
- Remote kernels and HPC proxies need local IT/docs.

## Related skills

- `@pandas` / `@polars` / `@duckdb` - compute inside cells
- `@mlflow` - log notebook experiments
- `@great-expectations` - validate data before analysis
