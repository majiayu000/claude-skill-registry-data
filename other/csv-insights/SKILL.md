---
name: csv-insights
description: Profile a CSV file and produce a Markdown report with row/column counts, fill rates, unique values, and numeric or categorical summaries.
---

# CSV insights

Turn a CSV file into a readable Markdown report: total rows and columns, and for
each column its fill rate, unique values, and either numeric stats
(min/max/mean/std) or the most common categories.

## How to run

Run with Python. Pass the input CSV and an output Markdown path inside the
out-box:

```
python3 <skill_dir>/run.py <input.csv> <output.md> [title]
```

- `<input.csv>` — a CSV in a folder the user allowed, or already in the out-box.
- `<output.md>` — a path **inside the out-box**.
- `[title]` — optional report title.

Standard library only; no packages to install. It reads one CSV and writes one
Markdown file. After running, tell the user the saved path.
