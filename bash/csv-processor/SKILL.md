---
name: csv-processor
description: Read a CSV file from disk, compute per-column min/mean/max for every numeric column, emit the result as JSON. Stdlib-only Python; no pandas, no numpy. Demonstrates the simplest possible "give me a file path, get back structured analysis" skill — a deliberate baseline for any skill that processes tabular data locally without an LLM in the loop.
version: "1.0"
license: MIT
metadata:
  category: data
  tag:
    - example
    - csv
    - statistics
    - python
---

# csv-processor

A deterministic, network-free skill — the easiest case. Useful as a control when debugging the agent ↔ skill plumbing: if this fails, the failure is in the runner, not the skill.

## Contract

**Input** (single CLI argument):

```
python src/main.py /path/to/data.csv
```

The script reads `argv[1]` as a filesystem path. CSV must have a header row.

**Output** (stdout, JSON):

```json
{
  "rowCount": 1234,
  "columns": {
    "price": { "min": 1.23, "mean": 42.0, "max": 999.99, "count": 1234 },
    "quantity": { "min": 0, "mean": 7.5, "max": 100, "count": 1230 }
  }
}
```

Only numeric columns appear under `columns`. `count` is the number of cells that parsed successfully (numeric); non-numeric / blank cells are skipped.

**Errors** — written to stderr as `{"error": "..."}` and exit code `1`.

## Run locally

```bash
cd examples/csv-processor
python src/main.py sample.csv
```

A `sample.csv` is bundled so the example runs out of the box.

## Adapt this

- **Different aggregations** — add median, p95, stddev; same shape, more keys per column.
- **Streaming** — for huge files, replace the in-memory accumulation with a running-mean update; one extra variable per column, same output shape.
- **Source other than disk** — accept a URL or stdin instead of `argv[1]`. The aggregation core doesn't care.
