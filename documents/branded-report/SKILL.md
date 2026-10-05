---
name: branded-report
description: Turn a Markdown report into a polished, consistently branded document in HTML, PDF, and DOCX — all three from one source and one theme, so every report looks identical. The theme (brand colors, fonts, logo, organization name) can be auto-extracted from a PowerPoint/Office template (.pptx/.potx/.thmx/.docx/.xlsx), or — when there is no Office file — sampled from an image, a website URL, or a PDF, so the output matches the corporate identity. Use when the user wants a standardized, branded, or "nicely formatted" report/document, wants the same report as PDF and/or Word and/or HTML, asks for a company-templated report, wants output that matches a PowerPoint/website/PDF design or color theme, or wants to derive brand colors and a logo from a template, image, web page, or PDF. Requires Python 3.8+ (markdown, python-docx, beautifulsoup4; pillow/pypdfium2/pypdf for image/PDF theme extraction); PDF output additionally needs a headless Chrome/Edge/Chromium.
license: MIT
compatibility: Requires Python 3.8+ with markdown, python-docx and beautifulsoup4; PDF output additionally needs a headless Chrome/Edge/Chromium browser on the machine
metadata:
  version: "1.2.2"
---

# Branded Report

> Generates **HTML, PDF, and DOCX** from a single Markdown file and a single theme, so a
> series of reports always looks the same. The agent supplies the content (Markdown) and
> the cover metadata; the script does the rendering. Deterministic — no LLM is called.

`SCRIPT` = this skill's `scripts/build_report.py`. Theme extraction =
`scripts/extract_theme.py`. The theme schema and styling details are in
[REFERENCE.md](REFERENCE.md).

## The theme (do this once per brand)

The look is driven by a small `theme.json` (colors, fonts, logo, organization). Get one by:
- **From an Office template** (most accurate) — reads the real color scheme + fonts:
  ```bash
  python EXTRACT --template "Brand.pptx" --out theme.json --logo-dir ./assets
  ```
  Works with **`.pptx`, `.potx`, `.thmx`, `.dotx`, `.docx`, `.xlsx`** — anything carrying an
  OOXML theme. Then open `theme.json` and pick the right `logo` (a dark/colored logo for
  white pages; **DOCX needs a PNG/JPG** logo via `logo_raster` — SVG embeds only in HTML/PDF).
- **From an image, a website, or a PDF** (when there is no Office theme) — `extract_theme_visual.py`
  renders the source and samples its brand colors (heuristic; review the result):
  ```bash
  python VISUAL --image brand.png  --out theme.json
  python VISUAL --url https://acme.example --out theme.json --logo-dir ./assets   # + logo + org + fonts
  python VISUAL --pdf branded.pdf --page 1 --out theme.json
  ```
  A PDF or image of an already-branded document gives accurate colors; a website yields its
  on-screen palette + logo to tune. See [REFERENCE.md](REFERENCE.md) for the reliability notes.
- **Or hand-write it** from [theme.example.json](theme.example.json).

> The theme file is **organization-specific** — keep it local (alongside the user's
> documents), not in this repo. The skill ships only the neutral `theme.example.json`.

## Generate the report

```bash
python SCRIPT --input report.md --theme theme.json \
    --formats html,pdf,docx --output-dir out --name my-report \
    --title "Report title" --subtitle "Subtitle" \
    --meta "**Date:** 2026-06-12" --meta "**Author:** ..." \
    --footer-note "Confidential" --json
```

| Flag | Meaning |
|------|---------|
| `--input` | Markdown source (headings, **bold**, lists, tables, ``` code ```, > quotes, `---`) |
| `--theme` | The brand theme JSON (omit for a neutral default theme) |
| `--formats` | Any of `html,pdf,docx` (default all three) |
| `--output-dir` / `--name` | Where, and the base filename (default: input stem) |
| `--title` / `--subtitle` | Cover page (omit `--title` to skip the cover entirely) |
| `--meta` | A cover metadata line; repeatable. `**Label:**` renders the label bold |
| `--footer-note` | Small note at the bottom of the cover |
| `--json` | Print a machine-readable `{status, outputs}` summary |

## What you (the agent) do

1. **Write or assemble the report as Markdown** (use the structure the report needs —
   headings map to the branded section bands, tables and code blocks are styled).
2. **Run the script** with the user's theme and the cover fields. Parse the JSON output.
3. **Report which files were produced** and where. If PDF was skipped, say why (no headless
   browser found) and offer the HTML (the user can Print-to-PDF from a browser).
4. **Keep the same theme + title conventions across a report series** so output is uniform.

## Errors & fallbacks

- **PDF skipped** → no Chrome/Edge/Chromium found. HTML and DOCX still produced; install a
  browser or open the HTML and print to PDF.
- **DOCX logo missing** → the theme's `logo` is an SVG; Word can't embed SVG. Point `logo`
  at a PNG/JPG (or the organization name is used as a text wordmark on the DOCX cover).
- **`ModuleNotFoundError`** → `pip install markdown python-docx beautifulsoup4` (the repo
  installer does this from `skill.install.json`).
