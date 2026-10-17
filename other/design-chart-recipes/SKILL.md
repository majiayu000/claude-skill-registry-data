---
type: Skill
name: design-chart-recipes
description: Author and validate nvoos-chart fenced-JSON chart blocks for NV oOS chat surfaces — 29 chart types across distribution, part-to-whole, ranking, change, special and grid families. Covers type selection, the v2 schema (values/series/data.items, mode, sort, direction, unit, animate, table, target), data-shape rules, the create_chart_fence server validator, the a11y checklist, and copy-paste JSON templates. Use when writing chart fences in assistant responses, choosing a chart type for data, validating chart JSON, or deciding between nvoos-chart, create_chart, generate_chart and generate_mermaid.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Chart Recipes (nvoos-chart)

Use this skill whenever an assistant message should show data as a chart.
The `nvoos-chart` fence renders everywhere the built-in renderer exists
(base chat, chat SPA, Pro SPA) — pure HTML/CSS, no iframe, no CDN.

```
```nvoos-chart
{ "type": "bar", "title": "Weekly sales", "labels": ["Mon","Tue","Wed"], "values": [12, 19, 8] }
```
```

## When to use which tool

| Need | Use |
|---|---|
| Inline, themeable, deterministic chart in chat markdown | `nvoos-chart` fence (this skill) |
| Server-validated fence + plain-text fallback table | `create_chart_fence` tool |
| Interactive Chart.js (tooltips, zoom, canvas) | `create_chart` / `create_chart_validated` |
| Rendered chart image (PNG) | `generate_chart` |
| Flow diagrams, architecture, sequences | `generate_mermaid` (do NOT abuse chart types for diagrams) |
| Infographic composition | markdown headers + `grid` + `waterfall`/`bullet` — not a new fence |

## Chart type selection — which type answers which question

**Distribution family** (shape of the data)
- `histogram` — "how is this distributed?" (binned bars, one series)
- `box` — five-number summary (min/Q1/median/Q3/max) per group
- `strip` / `dot` — raw points along an axis (jittered by row)
- `stem` — magnitude vs index with stems
- `violin` — full density shape per series (KDE, ≤100 points per series)

**Part-to-whole family**
- `donut` — 2–6 slices, total in the hole, legend with values
- `pie` — same but full circle; prefer donut for readability
- `waffle` — small counts as unit cells (≤400 cells, 10-col grid)
- `unit` — icon-style single-value cells (≤60 cells)

**Ranking family** (horizontal comparisons)
- `bar` — horizontal bars, left-anchored for non-negative data
- `lollipop` — same data, cleaner look with many rows
- `diverging` — positive/negative around a center axis
- `race` — animated re-sort over `series` frames (`animate: "race"`)

**Change / time family**
- `line` / `area` — trends over `labels`
- `column` — grouped/stacked vertical bars (`mode`)
- `slope` — before/after pairs (two series, rotated connectors)
- `dumbbell` — start/end range per row (two series)
- `waterfall` — cumulative build-up/break-down (first series = base)
- `candlestick` — OHLC from `[open, high, low, close]` per row
- `gantt` — `[start, end]` spans per named series
- `sparkline` — word-space trend, no axes

**Special family**
- `heatmap` — matrix with row labels + series columns
- `bullet` — value vs `target` (qualitative bands)
- `pyramid` — descending centered bars (population-style)
- `radial` / `dial` — single-value gauge (`values: [x]`, optional `max`)

**Grid small multiples**
- `grid` — `charts: [ …specs… ]`, ≤12 cells, shared context

## Data-shape rules (must follow or the chart falls back to a code block)

- `values: [1,4]` → one unnamed series. `series: [{name, values, color?}]` → multiple (≤12).
- `data: {items: [{label, value} | {label, values}]}` → named rows; `{label, value}` rows are
  coerced into ONE series + `labels` (donut/pie pattern).
- Labels ≤40 (heatmap rows ≤20), points ≤120 per series, strings ≤60 chars, title ≤120.
- Non-finite values (`NaN`, `Infinity`, `"abc"`) are dropped; numeric strings are coerced.
- Negative bar/column data switches the baseline to the center; each side scales to its own max.
- Colors: `#hex`, `rgb()`, `hsl()` only — anything else is stripped (never escaped into the DOM).
- ≤6 series for readability; ≤7 labels on bar/column; sort with `sort: "desc"` for rankings.

## v2 schema keys (all optional, all backward compatible)

| Key | Values | Effect |
|---|---|---|
| `mode` | `grouped` (default) \| `stacked` \| `100` | bar/column series layout |
| `direction` | `horizontal` \| `vertical` | bar/column axis |
| `sort` | `asc` \| `desc` | row order by value |
| `unit` | string ≤60 | appended to value labels |
| `animate` | `true` \| `"race"` | CSS entry animation / race replay |
| `table` | `true` (default) \| `false` | collapsed `<details>` data table (SC 1.1.1) |
| `target` | number | bullet chart target line |
| `caption` | string | chart caption |

## Accessibility checklist

- Always include `title` (becomes `aria-label`) or rely on the type label.
- Keep the auto data `table` unless `table: false` (screen-reader alternative).
- Colors must be distinguishable in both light/dark themes; prefer the default palette.
- Animations respect `prefers-reduced-motion` automatically — never rely on motion alone.
- No raw HTML in labels/titles: text is escaped by construction.

## Copy-paste templates

Trend:
```json
{ "type": "line", "title": "Sessions", "labels": ["Jan","Feb","Mar"], "values": [1200, 1450, 1620], "unit": "k" }
```

Ranking:
```json
{ "type": "bar", "title": "Top pages", "labels": ["/home","/pricing","/blog"], "values": [45, 28, 19], "sort": "desc" }
```

Composition:
```json
{ "type": "donut", "title": "Traffic mix", "data": { "items": [ { "label": "Organic", "value": 62 }, { "label": "Paid", "value": 24 }, { "label": "Direct", "value": 14 } ] } }
```

Comparison:
```json
{ "type": "column", "title": "Q1 vs Q2", "labels": ["Jan","Feb","Mar"], "series": [ { "name": "Q1", "values": [3, 4, 5] }, { "name": "Q2", "values": [4, 5, 6] } ], "mode": "grouped" }
```

Distribution:
```json
{ "type": "histogram", "title": "Order value", "values": [12, 18, 22, 23, 25, 31, 42, 55] }
```

Before/after:
```json
{ "type": "slope", "title": "Conversion", "labels": ["A","B","C"], "series": [ { "name": "Before", "values": [2.1, 3.0, 2.6] }, { "name": "After", "values": [2.8, 3.4, 3.9] } ] }
```

Gauge:
```json
{ "type": "dial", "title": "Health score", "values": [78], "max": 100 }
```

Small multiples:
```json
{ "type": "grid", "title": "Weekly per channel", "charts": [ { "type": "line", "title": "Email", "values": [1,2,3] }, { "type": "line", "title": "Social", "values": [2,1,4] } ] }
```

## Server validation

Use the `create_chart_fence` tool when the fence must be validated before it
reaches the client: it mirrors the client schema (same whitelist, caps, color
regex), returns the normalised fence plus a pipe-table fallback, and fails with
a `WP_Error` instead of guessing. In standalone PHP contexts, the tool is at
`includes/tools/class-wp-mcp-ai-tool-create-chart-fence.php`; the client rules
live in `assets/js/chat-chart-recipes.js`, `addons/chat-spa/src/api/chartRecipes.ts`
and `addons/pro/assets/spa-v2/src/components/shared/chartRecipes.ts` (keep all four in sync).

## Test fixtures

Shared conformance cases live in `addons/pro/assets/spa-v2/src/__tests__/chart-fixtures.json`
(canonical), mirrored at `addons/chat-spa/src/__tests__/chart-fixtures.json` and
`tests/js/chart-fixtures.json`. When changing schema behavior, add a fixture case
and update all three copies byte-identically.
