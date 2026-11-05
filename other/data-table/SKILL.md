---
name: data-table
description: Turn a CSV into a searchable, click-to-sort HTML table in one self-contained file (light and dark, no external assets).
---

# data-table

Make a CSV easy to explore: a standalone HTML page with a live search box and
sortable columns (numeric-aware). No internet, no dependencies.

## How to run

```
python3 <skill_dir>/run.py <input.csv> <output.html> [title]
```

- `<input.csv>` — a CSV with a header row (an allowed folder, or the out-box).
- `<output.html>` — a path **inside the out-box**.
- `[title]` — optional page title.

Standard library only. After running, tell the user the saved path.
