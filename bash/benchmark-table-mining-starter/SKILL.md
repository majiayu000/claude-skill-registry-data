---
name: benchmark-table-mining-starter
description: Parse small benchmark markdown tables from paper notes and summarize datasets, metrics, and best-performing methods.
---

# Benchmark Table Mining Starter

Use this starter on locally prepared markdown notes that contain one or more benchmark tables.

The wrapper:

- scans all markdown table blocks in the note
- selects the most leaderboard-like table instead of assuming the first table is the benchmark
- preserves canonical leaderboard fields such as `task`, `dataset`, `metric`, `model`, and `score` when they exist

```bash
python3 skills/scientific-knowledge/benchmark-table-mining-starter/scripts/run_benchmark_table_mining.py \
  --input skills/scientific-knowledge/benchmark-table-mining-starter/examples/benchmark_note.md
```

For a broader Papers-with-Code-style note that includes an earlier non-leaderboard table, use:

```bash
python3 skills/scientific-knowledge/benchmark-table-mining-starter/scripts/run_benchmark_table_mining.py \
  --input skills/scientific-knowledge/benchmark-table-mining-starter/examples/sample_benchmark_notes.md
```
