---
name: databricks-aibi-custom-viz-vega
description: >
  Build high-fidelity custom charts inside Databricks AI/BI (Lakeview) dashboards using
  Vega-Lite custom visualizations (Public Preview). Covers the documented contract — the
  `databricks_query` data source, Fields-section Name references, theme-aware signals
  (`colors`, `mode`, `dashboardTheme`), and cross-filtering via the reserved
  `databricks_mark_selection` parameter. Use when the built-in widget types in
  02-databricks-aibi-dashboards cannot express the chart you need, but you still want a
  documented, per-widget, cross-filter-capable visualization. For full-page bespoke React
  layouts (composite cards, KPI tiles, in-cell sparklines), see 06-databricks-aibi-custom-pages-react.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: dashboards
deploy_verb: bundle_deploy
deploy_note: "A Vega-Lite custom visualization is a single widget on an otherwise standard AI/BI dashboard. The dashboard still deploys via `bundle deploy --target dev` (runDatabricksCli on Genie Code) or the base64 Workspace Import path from 02-databricks-aibi-dashboards. On Genie Code, write the generated .lvdash.json under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "0.2"
  domain: monitoring
  role: worker
  pipeline_stage: 7
  pipeline_stage_name: observability
  called_by:
    - observability-setup
  standalone: true
  keywords:
    - databricks
    - ai/bi
    - lakeview
    - custom visualization
    - vega-lite
    - vega
    - high-fidelity chart
    - cross-filter
    - dashboard
  last_verified: "2026-09-21"
  volatility: medium
  status: "Public Preview (feature is officially documented but pre-GA — spec surface may change)"
  upstream_sources:
    - name: "Databricks docs — Custom visualizations in AI/BI dashboards"
      url: "https://docs.databricks.com/aws/en/dashboards/manage/visualizations/custom-visualizations"
      relationship: "authoritative"
      last_synced: "2026-09-21"
    - name: "Empirical exemplars — deployed AI/BI dashboards (Fleet Reliability; Flight Ops OTP) with 28 custom-vega-viz widgets"
      relationship: "reverse-engineered"
      last_synced: "2026-09-21"
---

# AI/BI Custom Visualizations (Vega-Lite)

## Overview

**Custom visualizations** let you render charts in an AI/BI (Lakeview) dashboard that go beyond
the built-in widget types documented in `02-databricks-aibi-dashboards`. They use the
**Vega-Lite** grammar: you write a JSON specification, bind it to a dashboard dataset, and the
dashboard renders it — theme-aware, and able to drive cross-filtering.

This is the **documented, supported** path for high-fidelity charts. It is per-widget (one chart
per custom-viz widget), not a full-page takeover. For a full-page bespoke layout (composite cards,
KPI rows, in-cell sparklines, narrative "wow" surfaces), use the React mechanism in
`06-databricks-aibi-custom-pages-react` instead.

> **Status:** This feature is in **Public Preview** (Databricks docs, last verified 2026-09-21).
> The Vega-Lite spec contract below is stable and documented; treat it as `volatility: medium`.

## Fidelity Decision Gate (read first)

Pick the **lowest** tier that satisfies the requirement. Do not escalate for aesthetics alone.

| Need | Use | Skill |
|------|-----|-------|
| Standard chart (bar, line, pie, area, table, pivot, map, sankey, KPI counter) | Built-in widget | `02-databricks-aibi-dashboards` |
| A **chart type or encoding** the built-ins don't offer (phylogenetic tree, radial/nightingale, bullet, sunburst, custom highlight/annotation), but still one chart bound to one dataset, and you want native cross-filter | **Vega-Lite custom viz** | **this skill** |
| A **full-page bespoke layout** — composite multi-metric cards, in-cell sparklines, custom filter chips, email-preview surfaces — beyond a single chart | React custom page | `06-databricks-aibi-custom-pages-react` |

**Before choosing this skill, confirm the built-in widgets in `02` genuinely cannot express the
chart.** If they can, stop and use `02` — built-ins are simpler to maintain and validate.

**Output a one-line Fidelity Decision Record** before authoring, e.g.:
`Fidelity: Vega custom viz — built-ins lack a bullet chart with pace/target/current bands; single dataset; cross-filter needed.`

## How it works

You can author either in the UI or directly as JSON (the `.lvdash.json` widget contract is in the
next section — confirmed empirically from 28 custom-vega-viz widgets across two deployed dashboards).

UI flow:

1. Add/select a **dataset** on the dashboard (standard `queryLines` dataset — see `02`).
2. Add a widget → in the visualization config pane, choose **Custom Viz** under
   **Advanced visualization**.
3. In the **Fields** section, add each field you reference. Every field has a unique **Name** —
   your Vega-Lite spec references data by that Name, not by the raw SQL column.
4. Paste your **Vega-Lite JSON specification** into the spec editor.

### The data source: `databricks_query`

Bind the spec's data to the widget's query result with the reserved name:

```json
"data": { "name": "databricks_query" }
```

The renderer feeds the dataset rows (projected to the declared Fields) into this named source.

### Referencing columns

- In encodings: `"field": "{FieldName}"` — the Name you gave the field in the Fields section.
- In expressions/transforms: `datum["{FieldName}"]` or `datum.{FieldName}`.

```json
"encoding": { "x": { "field": "xField", "type": "quantitative" } }
```
```json
{ "calculate": "datum.r * cos(datum.angle)", "as": "x" }
```

### Auto-resize to the widget

Always make the chart fill its tile:

```json
"width": "container",
"height": "container",
"config": { "autosize": { "type": "fit", "contains": "padding" } }
```

## Widget JSON contract (`custom-vega-viz`)

A custom viz is stored as a widget of type `custom-vega-viz`, **version 1**. The Vega-Lite spec is a
**JSON string** under `spec.jsonSpec.spec`; the "Fields section" is `spec.encodings.fields[]`; and the
widget query supplies the rows. This is the observed shape (28 widgets, two deployed dashboards):

```json
{
  "widget": {
    "name": "ata_pareto_w",
    "queries": [
      {
        "name": "main_query",
        "query": {
          "datasetName": "ata_pareto",
          "fields": [
            { "name": "ata_system", "expression": "`ata_system`" },
            { "name": "defects", "expression": "`defects`" },
            { "name": "cumulative_pct", "expression": "`cumulative_pct`" }
          ],
          "disaggregated": true
        }
      }
    ],
    "spec": {
      "version": 1,
      "widgetType": "custom-vega-viz",
      "frame": { "showTitle": true, "title": "…", "showDescription": true, "description": "…" },
      "data": { "queryName": "main_query" },
      "encodings": {
        "fields": [
          { "fieldName": "ata_system" },
          { "fieldName": "defects" },
          { "fieldName": "cumulative_pct" }
        ]
      },
      "jsonSpec": {
        "type": "vega-lite",
        "spec": "{\"$schema\": \"https://vega.github.io/schema/vega-lite/v6.json\", \"data\": {\"name\": \"databricks_query\"}, …}"
      }
    }
  },
  "position": { "x": 0, "y": 8, "width": 7, "height": 5 }
}
```

Alignment rules (all verified in the exemplars):

- `spec.jsonSpec.spec` is the Vega-Lite spec **serialized as a string** (escaped JSON), wrapped in
  `{ "type": "vega-lite", "spec": "…" }`. Build it with `json.dumps` — never hand-escape.
- `spec.data.queryName` must equal a `queries[].name` (e.g. `main_query`).
- Every `spec.encodings.fields[].fieldName` must match a `queries[].query.fields[].name`, and those are
  the **Names** the Vega spec references (`"field": "ata_system"`, `datum.ata_system`).
- Bind the spec's data to `{"name": "databricks_query"}` (see above).

### `disaggregated: true` for custom viz

All 28 exemplar widgets use `disaggregated: true` — the query streams **raw rows** to Vega and the
**Vega-Lite `transform` block** does the aggregation/windowing (`window`, `aggregate`, `stack`,
`joinaggregate`, `fold`, `calculate`). This is the opposite of most built-in widgets. Do the shaping in
Vega, not in a pre-aggregated SQL, unless the row volume is large — then pre-aggregate in the dataset.

### Grid & sizing

The exemplars lay out custom-viz widgets on a **12-column grid** (widths sum to 12, e.g. a 7+5 split;
heights ~5). Follow the grid convention of the dashboard you are adding to. Always pair grid sizing with
`width/height: "container"` inside the spec so the chart fills the tile.

## Theme-aware styling

Custom visualizations inherit the dashboard theme automatically (fonts, gridline color,
transparent background over the themed tile). Anything you set in your spec's `config` block
overrides the inherited defaults.

To reference theme values inside a Vega expression (`{ "expr": "..." }`):

| Signal | Use for | `[mode]` index? |
|--------|---------|-----------------|
| `colors` | Pre-resolved tokens for the active mode: `colors.textPrimary.default`, `colors.gridColor`, `colors.markHighlightColor` | **No** — already resolved |
| `mode` | The active mode, `'light'` or `'dark'`; use to index `dashboardTheme` per-mode fields | n/a |
| `dashboardTheme` | Full owner theme: fonts (`resolvedFontSettings`), palette (`visualizationColors`), per-mode colors (`gridLineColor`) | **Yes** for per-mode fields |

```json
{ "expr": "dashboardTheme.resolvedFontSettings.fieldValue.fontFamily" }
{ "expr": "dashboardTheme.resolvedFontSettings.fieldTitle.fontColor[mode]" }
{ "expr": "dashboardTheme.visualizationColors[0]" }
{ "expr": "colors.markHighlightColor" }
```

**Rule:** prefer `colors.*` (no `[mode]`); reach for `dashboardTheme.*[mode]` only for fonts, the
full palette, or values `colors` doesn't provide.

### Two theming approaches (know the tradeoff)

| Approach | How | Adapts to light/dark? | Seen in exemplars |
|----------|-----|-----------------------|-------------------|
| **Theme signals** (recommended for portability) | Reference `colors.*` / `dashboardTheme.*[mode]` in `{ "expr": "…" }` | ✅ Yes | No |
| **Static config + brand palette** (pragmatic) | Hardcode hex in `config` and mark `color` | ❌ No — locks to one mode | ✅ All 28 widgets |

The exemplars take the pragmatic route: they set a neutral axis config and use the **Databricks brand
palette** for marks. Use this when you control the dashboard's mode; use theme signals when the
dashboard may be viewed in both modes.

```json
"config": {
  "autosize": { "type": "fit", "contains": "padding" },
  "view": { "stroke": "transparent" },
  "axis": { "labelColor": "#5A6472", "titleColor": "#5A6472", "gridColor": "#EEF1F4" }
}
```

Databricks brand palette used in the exemplars (categorical): `#FF3621` (red/primary), `#1B5162`
(teal), `#FFAB00` (amber), `#8A94A6` (grey), `#2A7E3B` (green). Sequential (heatmaps):
`["#FDE7E2", "#FF3621"]`.

## Cross-filtering (make the chart a filter source)

A custom viz can drive the dashboard's cross-filter state when a user clicks a mark. Add a point
selection parameter with the **exact reserved name** `databricks_mark_selection`:

```json
"params": [
  { "name": "databricks_mark_selection", "select": { "type": "point", "fields": ["categoryName"] } }
]
```

Requirements (all mandatory):

- The parameter `name` must be **exactly** `databricks_mark_selection`. Any other name is a plain
  parameter and does **not** cross-filter.
- `select.type` must be `point`. Interval/brush selections are **not** supported as cross-filter sources.
- `select.fields` lists the **Field Names** from the Fields section — not raw column names.
- List only **dimension** (grouping) fields. Aggregated measures (`SUM(...)`, `AVG(...)`) cannot
  drive a cross-filter.
- Multiple fields: `"fields": ["categoryName", "regionName"]`.

### Highlight the selected marks

On fill marks (`bar`, `arc`, `rect`), keep `color` bound to your field and add `stroke`/`strokeWidth`
conditions; dim unselected marks with `fillOpacity`. Use `{ "expr": "colors.markHighlightColor" }`
for the stroke so it reads in both modes. See `assets/templates/vega-bar-crossfilter.json`.

## Deployment & portability

- A custom viz is one widget on an otherwise standard AI/BI dashboard, so the **dataset, filters,
  Global Filters page, parameters, and deployment** are exactly as in `02-databricks-aibi-dashboards`
  (base64 Workspace Import or `bundle deploy`).
- Author the widget JSON directly using the `custom-vega-viz` contract above (build the
  `spec.jsonSpec.spec` string with `json.dumps`), or build in the UI and export. Keep the Vega-Lite
  spec + the Fields Name list under version control (see `assets/templates/`).
- The embedding contract here is empirically confirmed but the feature is Public Preview — after
  deploying, **preview in the workspace** to confirm the widget renders as expected.

## Validation

- Run `scripts/validate_vega_viz.py <spec.json> --fields f1 f2 ...` to confirm the spec is valid JSON,
  uses `data.name = "databricks_query"`, sets `width/height = "container"`, and references only Field
  Names you declared (catches the #1 error: a `field`/`datum.x` that has no matching Fields entry).
- Runtime rendering still needs a workspace preview — a spec can be structurally valid yet visually
  wrong. Preview in the dashboard before shipping.

## Common mistakes

| Mistake | Fix |
|--------|-----|
| Binding data by table/column instead of `databricks_query` | Use `"data": { "name": "databricks_query" }` |
| Referencing raw SQL columns in the spec | Reference the **Field Name** from the Fields section |
| Naming the selection param anything but `databricks_mark_selection` | Use the exact reserved name |
| Using an interval/brush selection for cross-filter | Cross-filter needs `select.type: "point"` |
| Listing an aggregated measure in `select.fields` | List only dimension fields |
| Indexing `colors.*` with `[mode]` | `colors` is pre-resolved — no `[mode]`; only `dashboardTheme.*` per-mode fields take `[mode]` |
| Chart clipped / not resizing | Add `width/height: "container"` + `autosize: fit/padding` |
| Treemap | Not supported by Vega-Lite — choose another encoding |
| `spec.jsonSpec.spec` stored as an object | It must be a **string** — `{"type":"vega-lite","spec":"<escaped JSON>"}`. Serialize with `json.dumps` |
| `spec.data.queryName` doesn't match a query | Set it to a `queries[].name` (e.g. `main_query`) |
| A Field in `encodings.fields` missing from the query | Every `encodings.fields[].fieldName` must equal a `queries[].query.fields[].name` |
| Pre-aggregating in SQL then re-aggregating in Vega | For custom viz use `disaggregated: true` and aggregate in the Vega `transform` block |

## References

- [`references/vega-lite-contract.md`](references/vega-lite-contract.md) — the full data/Fields/spec
  contract plus the exact `custom-vega-viz` widget shape and a `json.dumps` builder.
- [`references/theming-and-crossfilter.md`](references/theming-and-crossfilter.md) — theme signals and
  `databricks_mark_selection` patterns.
- [`references/recipe-gallery.md`](references/recipe-gallery.md) — **real, working spec recipes**
  extracted from the exemplars: Pareto (dual-axis), rolling-mean line, heatmap, bump chart, sunburst,
  plus the query fields each needs.
- [`assets/templates/vega-bar-crossfilter.json`](assets/templates/vega-bar-crossfilter.json) — themed
  bar chart that acts as a cross-filter source.
- [`assets/templates/vega-pareto-dual-axis.json`](assets/templates/vega-pareto-dual-axis.json) — bars +
  cumulative line + 80% rule with independent dual y-axes.
- [`assets/templates/vega-heatmap.json`](assets/templates/vega-heatmap.json) — sequential-color rect
  heatmap.
- [`scripts/validate_vega_viz.py`](scripts/validate_vega_viz.py) — offline validator (bare spec **or**
  a full `.lvdash.json` with `custom-vega-viz` widgets).
- Official docs: https://docs.databricks.com/aws/en/dashboards/manage/visualizations/custom-visualizations

## Related skills

- `monitoring/02-databricks-aibi-dashboards` — built-in widgets, datasets, filters, deployment (this
  skill reuses all of that plumbing).
- `monitoring/06-databricks-aibi-custom-pages-react` — full-page React custom pages for bespoke layouts.
