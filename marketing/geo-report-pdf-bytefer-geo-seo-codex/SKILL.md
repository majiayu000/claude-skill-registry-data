---
name: geo-report-pdf
description: "Generate a professional PDF report from a GEO audit using pandoc plus a Chrome/Chromium-compatible headless browser. Converts GEO-AUDIT-REPORT.md into a styled, client-ready PDF with a cover page, color-coded score tables, severity-tagged findings, and a 90-day roadmap."
---

# GEO PDF Report Generator (pandoc pipeline)

## Prerequisites

- **pandoc** — install through Homebrew, Chocolatey, Scoop, apt, or your platform package manager
- **Chrome/Chromium-compatible browser** — Google Chrome, Microsoft Edge, Chromium, or Brave

No Python dependencies. No ReportLab. No JSON data wrangling.

## How It Works

1. Read `GEO-AUDIT-REPORT.md` in the current directory (created by `$geo-audit`)
2. Extract cover metadata from the report (brand name, domain, GEO score, date, locations)
3. Run `pandoc` with the bundled CSS + HTML template to produce a self-contained `GEO-REPORT.html`
4. Run a Chrome/Chromium-compatible browser in headless mode to print the HTML to `GEO-REPORT.pdf`

Resolve `GEO_ROOT` from `CODEX_GEO_ROOT`, the loaded plugin/repository root, or the classic installer path `${CODEX_HOME:-$HOME/.codex}/skills/geo`. The pandoc template (`$GEO_ROOT/templates/geo-report-template.html`) injects:
- A full-bleed dark navy cover section with the GEO score badge
- Per-section cover metadata (date, business type, locations, platform)
- JavaScript that runs inside Chrome before printing to color-code score cells and severity-tag finding sections

## Workflow

### Step 1: Check for audit report

Look for `GEO-AUDIT-REPORT.md` in the current directory. If absent, tell the user to run `$geo-audit <url>` first.

### Step 2: Extract cover metadata from the report

Read the top of `GEO-AUDIT-REPORT.md` and extract:

| Field | Where to find it |
|---|---|
| `brand_name` | First H1 title (after "GEO Audit Report:") |
| `domain` | Second bold line (e.g. `**Domain:** alexamediasolutions.com`) |
| `geo_score` | Line matching `## Overall GEO Score: XX / 100` |
| `score_label` | Word after the score on that same line (e.g. "Poor", "Fair", "Good") |
| `date` | `**Audit Date:**` line |
| `business_type` | `**Business Type:**` line |
| `locations` | `**Locations:**` line |
| `platform` | `**CMS:**` line |

### Step 3: Run pandoc

```bash
GEO_ROOT="${CODEX_GEO_ROOT:-}"
if [ -z "$GEO_ROOT" ]; then
  for candidate in "$PWD" "$PWD/.." "$PWD/../.." "${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}/geo"; do
    if [ -f "$candidate/templates/geo-report-template.html" ]; then
      GEO_ROOT="$candidate"
      break
    fi
  done
fi
if [ -z "$GEO_ROOT" ]; then
  echo "GEO runtime root not found. Set CODEX_GEO_ROOT to the geo-seo-codex plugin/repo root."
  exit 1
fi

pandoc GEO-AUDIT-REPORT.md \
  --to html5 \
  --standalone \
  --embed-resources \
  --template "$GEO_ROOT/templates/geo-report-template.html" \
  --css "$GEO_ROOT/templates/geo-report-style.css" \
  --metadata title="GEO Audit Report — <brand_name>" \
  --metadata brand_name="<brand_name>" \
  --metadata domain="<domain>" \
  --metadata geo_score="<geo_score>" \
  --metadata score_label="<score_label>" \
  --metadata date="<date>" \
  --metadata business_type="<business_type>" \
  --metadata locations="<locations>" \
  --metadata platform="<platform>" \
  -o GEO-REPORT.html
```

Replace `<field>` placeholders with values extracted in Step 2. If a field is not found in the report, omit that `--metadata` flag — the template has sensible defaults.

### Step 4: Run Chrome/Chromium headless

```bash
GEO_CHROME="${GEO_CHROME:-}"
if [ -z "$GEO_CHROME" ]; then
  for candidate in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
    google-chrome chromium chromium-browser chrome msedge; do
    if command -v "$candidate" >/dev/null 2>&1 || [ -x "$candidate" ]; then
      GEO_CHROME="$candidate"
      break
    fi
  done
fi

if [ -z "$GEO_CHROME" ]; then
  echo "Chrome/Chromium executable not found. Set GEO_CHROME to Chrome, Edge, Chromium, or Brave."
  exit 1
fi

"$GEO_CHROME" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --print-to-pdf="$(pwd)/GEO-REPORT.pdf" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  --virtual-time-budget=5000 \
  "file://$(pwd)/GEO-REPORT.html"
```

### Step 5: Report completion

Tell the user:
- `GEO-REPORT.pdf` was generated in the current directory
- File size
- Optionally: `open GEO-REPORT.pdf` to preview it

## What the PDF Contains

- **Cover page** — Dark navy gradient, brand name, domain, GEO score badge (colored by score), audit date, business type, locations, CMS platform
- **Score tables** — Cells containing `XX/100` are color-coded: ≥80 green, ≥65 blue, ≥50 amber, ≥35 orange, <35 red
- **Finding sections** — `h3` headings containing "Critical / High / Medium / Low" get severity-colored left-border callout blocks (red / orange / yellow / green)
- **Section page breaks** — Major sections (High Priority, 90-Day Roadmap, Component Score Summary, Generated Schema) break to new pages automatically
- **Code blocks** — JSON schema templates render with dark theme monospace styling
- **Page footer** — Brand name · GEO Audit · date + page numbers (via CSS `@page`)

## Customizing the Report

- **Colors / typography** — Edit `$GEO_ROOT/templates/geo-report-style.css`
- **Cover layout** — Edit `$GEO_ROOT/templates/geo-report-template.html`
- **Score thresholds for color-coding** — Edit the `scoreColor()` function in the template's `<script>` block
- **Which sections get page breaks** — Edit the `breakBefore` array in the template's `<script>` block

## Troubleshooting

| Problem | Fix |
|---|---|
| `pandoc: command not found` | Install pandoc with the package manager for your platform |
| Chrome not found | Set `GEO_CHROME` to a Chrome, Edge, Chromium, or Brave executable |
| PDF is blank / empty | Increase `--virtual-time-budget` to 8000 |
| Cover metadata missing | Check GEO-AUDIT-REPORT.md has the standard header format |
| Fonts not loading | PDF is rendered offline; system fonts are used as fallback — this is expected |
