---
name: chart
description: Turn a CSV into a clean bar or line chart, embedded as an SVG in a standalone HTML page (multi-series, light and dark, no dependencies).
---

# chart

Render a CSV as a good-looking chart. The first column is the category (x-axis);
every other numeric column becomes a series. Bars are grouped; lines are drawn per
series. The result is one self-contained HTML file that opens in any browser.

## How to run

```
python3 <skill_dir>/run.py <input.csv> <output.html> [--type bar|line] [--title "Title"]
```

- `<input.csv>` — a CSV with a header row (an allowed folder, or the out-box).
- `<output.html>` — a path **inside the out-box**.
- `--type` — `bar` (default) or `line`.
- `--title` — optional chart title.

Standard library only. After running, tell the user the saved path.
