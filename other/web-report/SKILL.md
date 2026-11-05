---
name: web-report
description: Turn Markdown or plain text into a polished, self-contained HTML page (light and dark, system fonts, no external assets) that opens in any browser.
---

# web-report

Render Markdown/plain text into one good-looking, standalone `.html` file. Supports
headings, bold/italic, inline code, bullet and numbered lists, quotes, links, and
horizontal rules. No external assets — the page works offline.

## How to run

1. First write the content as Markdown into the out-box with the `Write` tool
   (e.g. `report.md`).
2. Then convert it:

```
python3 <skill_dir>/run.py <input.md> <output.html> [title]
```

- `<input.md>` — the Markdown file you just wrote (in the out-box).
- `<output.html>` — a path **inside the out-box**.
- `[title]` — optional page title.

Standard library only. After running, tell the user the saved path.
