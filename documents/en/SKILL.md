---
name: ppt-report-generator
description: Report deck generator / data-report presentation builder — turns a data report into a 16:9 web-based slide deck (1600×900 design canvas, auto-scaled to the browser), playable fullscreen with one-click PDF export. Per-slide split source + physical data separation + switchable themes + ECharts charts. **Always use this skill** when the user asks to "make a monthly/quarterly report", "make a work-report deck", "turn data into a web/PDF presentation", or wants to reuse a "one file per slide, data stored separately, themes switchable" deck template. Even if the user never says "PPT" or "slides", any time the task is to turn "several datasets + conclusions" into a presentable/shareable web report, follow this skill's workflow.
---

# PPT Report Generator (web-based slide deck template)

Turn "several business datasets + interim conclusions" into a 16:9 web-based deck that plays fullscreen in a browser and exports to PDF with one click.

## Core promises (design goals)

1. **One slide = three files**: `slides/slide-N.html` + `scripts/slide-N.js` + `styles/slide-N.css`, bundled into a single HTML by `build.py`. Editing one slide touches only that slide — **saves tokens, avoids conflicts**.
2. **Data physically separated from rendering**: all chart/table data lives in `data/slide-N.{xlsx,csv,json}`, auto-converted to JSON and injected at build time. **Edit data in Excel day-to-day**; rendering code stays untouched.
3. **Chart selection has rules**: each data shape maps to one chart type (see `references/chart-mapping.md`) — **don't pick charts on a whim**. Default to **ECharts**.
4. **Information hierarchy has hard rules**: label / title / subtitle (conclusion) / section title / card title / body / caption / helper text — 8 levels, each with fixed font size, weight, and color (see `references/design-system.md`).
5. **Switchable themes**: 5 presets (modern-light / dark-tech / warm-business / brand-blue / minimal-mono), switched via the `data-theme` attribute (see `references/themes.md`).

## When to use this skill

Trigger conditions (any one is enough):

- The user says: "make a monthly/quarterly/project report", "make a work report", "make a data-report deck", "turn this data into a presentable web page"
- The user provides raw data (xlsx / multiple tables / a written description of conclusions) and wants a "report" produced
- The user already has a project with this structure (`src/slides/`, `build.py`, `shell.html`) and wants to add a slide or change the theme
- The user wants to "save this deck so it can be reused next time"

## Workflow (standard steps)

### Step 1 — Understand input and output

- Ask (if unknown): **How many slides? What does each slide say? Where is the key data? Who is the target reader? Is PDF needed?**
- Don't start drawing charts. First list each slide's **(label, title, subtitle/conclusion, body type)** and confirm with the user.

### Step 2 — Pick a template (per slide)

Open `assets/slides-templates/` and pick a starting point by the slide's "body type":

| Body type | Template | Usage |
|---|---|---|
| Monthly delivery overview (multi-section × multi-card) | `kpi-overview.html` | Slide 1, summary-style page |
| Two subjects side by side (e.g. two countries) | `two-country.html` | KPI row + dual-card metric table |
| Three-phase loop + multiple charts | `three-phase.html` | Timeline + multiple chart-cards |
| Multi-subject time trend | `multi-trend.html` | 4-country / 4-channel line chart + milestone markers |
| Categorical bars + trend line combo | `supply-bars.html` | Material/category mini-bars + overall trend |

Templates are skeletons — **copy, then change copy, data, and IDs**.

> **Special-graphic templates (currently Chinese-docs only).** Four more templates ship in
> `assets/slides-templates/` for harder page types — `landscape-map.html` (industry/competitor
> landscape, 3-tier), `value-chain.html` (value-flow horizontal axis for physical industries),
> `matrix-2x2.html` (McKinsey/BCG 2×2 strategic matrix), and `human-portrait.html` (data-driven
> human-silhouette persona: write a `labels` array, and `scripts/silhouette.js`'s
> `renderHumanPortrait()` auto-draws the silhouette, body-part dots, and leader lines). Their
> design specs live in `references/{landscape-skeleton,landscape-qa,matrix-2x2,svg-aesthetics,human-portrait}.md`,
> which are **not yet translated** — read the root (Chinese) versions for now.

### Step 3 — Put data into `src/data/slide-N.{xlsx,csv,json}`

**This step matters most.** Day-to-day, prefer Excel/CSV; build auto-converts to JSON and injects into `window.__DATA_N__`.

**All three formats supported** (priority .json > .xlsx > .csv; with the same name only one is used):

| Format | Use case | Conversion result |
|---|---|---|
| `.xlsx` | Recommended for daily use — data is already in Excel | With multiple sheets: each sheet name → one top-level JSON key |
| `.csv` | Single-table data, exported from somewhere | Whole file → one top-level JSON array |
| `.json` | Machine-generated / complex nested structure | Read directly |

**Conventions** (see the "Data format" section in `references/architecture.md`):
- Row 1 of each sheet / csv is the header; each subsequent row → one object (`[{col: val}, ...]`)
- Sheet names / column names starting with `_` are skipped (used for notes, helper calculations)
- Numeric cells auto-convert to number; others stay string

**xlsx example**: `src/data/slide-3.xlsx` contains 2 sheets "kpis" and "trend" → accessed in JS as:

```js
function initSlide3() {
  const D = window.__DATA_3__;
  // D.kpis  = [{label: 'DAU', value: 12.4, unit: '万'}, ...]
  // D.trend = [{week: 'W1', na: 12.1, eu: 8.4}, ...]
}
```

**Updating data next time**: just edit and save in Excel, rerun `python3 build.py` — rendering code stays completely untouched.

**Standalone debugging**: `python3 xlsx2json.py src/data/slide-3.xlsx` runs the conversion alone to inspect the JSON output.

### Step 4 — Pick a chart (see `references/chart-mapping.md`)

Don't just pick the chart you feel like drawing. Look up the decision table by data shape:

- Time series → line chart (with milestone vertical-line plugin)
- Before/after of a comparison experiment → 100% stacked bars
- Object ranking (Top 20) → horizontal mini-bars (custom div, no chart library)
- Multi-subject single-period comparison → grouped bars
- Share / composition → **no pie chart**; use 100% stacked bars or a treemap

### Step 5 — Information hierarchy (see `references/design-system.md`)

Every piece of text must answer "which level am I?". The slide-label / slide-title / slide-subtitle trio is a **mandatory top structure**. Key numbers in the conclusion must be wrapped in `<strong>` or `<span class="pos|neg|warn">` for highlight.

### Step 6 — Build and preview

```
python3 build.py            # bundle the final HTML (output filename configurable in CONFIG at top of build.py)
open *.html                 # open in browser, ←/→ to navigate
python3 export_pdf.py       # (optional) export PDF
```

### Step 7 — Theme switching (optional)

If the user wants a different style, **don't rewrite the CSS**. Just change the attribute on `<body data-theme="dark-tech">`. See `references/themes.md`.

## Golden rules (violations get rejected in review)

1. **Don't hardcode data in rendering code.** Data goes into `data/slide-N.json` or a top const variable; render functions only take parameters.
2. **Don't let one slide's HTML exceed 200 lines.** If it does, split into sub-components or move to JS rendering.
3. **Don't pile on font sizes freely.** Use only the 8 levels `--fs-label / --fs-title / --fs-subtitle / --fs-h2 / --fs-h3 / --fs-body / --fs-caption / --fs-mini`.
4. **Don't use a pie chart for 5+ share items.** Use 100% stacked bars instead.
5. **Don't hardcode colors.** Use theme variables like `var(--accent)`, `var(--accent2)`, so theme switching doesn't break.
6. **Every slide must have the `slide-label`, `slide-title`, `slide-subtitle` trio.** The subtitle must be **a one-sentence conclusion** containing key numbers.
7. **The design canvas is fixed at 1600×900.** Size every element in these pixels; browser auto-fit is handled by `transform: scale(--fit)`. **Don't use vw/vh.**
8. **Don't manually edit the build output.** Always edit `src/`, then run `python3 build.py`.
9. **Each slide answers one question and has one visual anchor.** More than 12 body elements on a slide = split into two (see `references/layout-principles.md` sections 6/10).
10. **The whole deck needs rhythm.** Don't make 6 straight high-density data slides; interleave low-density "overview/breather/closing" slides (see `layout-principles.md` section 11 "story curve").
11. **Card boundaries must be strictly aligned**: same-row cards share a bottom edge, same-column cards share left/right edges. Use grid `1fr 1fr` + children `flex:1 1 0; min-height:0` + a flexible spacer (e.g. phase-arrow-v) to absorb differences — **don't hardcode height** (see `layout-principles.md` section 7b).

## Detailed reference docs

Read in any order as needed:

- [`references/architecture.md`](references/architecture.md) — split architecture, how build.py works, adaptive scaling
- [`references/design-system.md`](references/design-system.md) — font size / weight / color / spacing hard rules (**how to write text**)
- [`references/layout-principles.md`](references/layout-principles.md) — classic report-deck layout rules: pyramid structure, F/Z reading path, rule of thirds, visual anchor, information density, story curve (**how to place things**)
- [`references/chart-mapping.md`](references/chart-mapping.md) — data shape ↔ chart selection decision table (ECharts config templates)
- [`references/components.md`](references/components.md) — common component library (KPI / card / Phase / Timeline / Mini-bar / Metric-row)
- [`references/themes.md`](references/themes.md) — 5 preset themes + how to customize a theme

## Asset list

Everything under `assets/` is a **ready-to-copy** production file:

- `shell.html` — HTML skeleton (with `{{STYLES}}` `{{SLIDES}}` `{{SCRIPTS}}` placeholders)
- `build.py` — bundle script (concatenates in slide-number order)
- `export_pdf.py` — PDF export (playwright + img2pdf)
- `styles/common.css` — global styles + 5 theme variables
- `styles/components.css` — common components
- `scripts/common.js` — adaptive fit, navigation, ECharts helper
- `scripts/theme-switcher.js` — theme switching UI
- `data/slide-N.json` — data samples
- `slides-templates/*.html` — 5 page templates

## Initializing a new project (recommended flow)

```bash
mkdir my-report && cd my-report
# 1. Copy the whole assets directory into the project as src/
cp -r <skill_path>/assets src
# 2. Copy build.py / export_pdf.py to the project root
cp <skill_path>/assets/build.py <skill_path>/assets/export_pdf.py .
# 3. Pick templates as needed, rename to slide-1.html / slide-2.html ...
# 4. Write data → edit copy → build → preview
```
