---
name: data-workflow
description: Use this skill for any data or analytics task — querying databases, analyzing metrics, exploring data warehouses, processing datasets, or creating visualizations.
---

# Data Workflow

For any data question, metric lookup, or analytical task, delegate to the `data-triage` skill which orchestrates the full data pipeline:

1. Load the `data-triage` skill
2. Follow its workflow (data-model-explorer → data-analyst)

For file-based data processing (CSV, JSON, Excel, Parquet):

- Install needed packages (pandas, matplotlib, seaborn, scipy)
- Write and iterate on analysis code
- Save outputs to workspace files (charts to `/tmp/data_*.png`, results to `/tmp/`)
