---
name: data-analysis-hygiene
description: Data-handling rules for this research repo. Use when loading datasets, merging/joining tables, running EDA or Table 1, building features, or handling any patient-level / PHI data.
allowed-tools: Read, Write, Edit, Bash
---

# Data Analysis Hygiene

## When to Use
- Loading, merging, or transforming datasets
- Before any EDA, Table 1, or modeling step
- Anytime patient-level or PHI-adjacent data is involved

## Rules
1. **Missingness audit first.** Before EDA / Table 1 / modeling on any finalized dataset, produce a missingness audit (per-column % missing, patterns). The analyst decides the imputation strategy from it - do not silently impute.
2. **Skip existing outputs.** If an extraction / feature / metric output already exists on disk, integrate from that cache instead of re-running the pipeline.
3. **Step-by-step merges.** For multi-step joins, print per-step key-intersection counts and row-count diagnostics after each join. Take user-provided file paths literally.
4. **PHI safety.** Never print, log, commit, or send patient-level data to any external service. Treat everything under `data/` as sensitive.
5. **iCloud-evicted files.** Files under `~/Documents` may be dataless (iCloud-evicted); materialize with `dd if=<file> of=/dev/null bs=1m` before a pandas read fails.

## Missingness Audit Snippet
```python
def missingness(df):
    m = df.isna().mean().sort_values(ascending=False)
    return (m[m > 0] * 100).round(1).rename("pct_missing").to_frame()
```

## Integration
- Pair with [[publication-figures]] for any plots produced from audited data.
