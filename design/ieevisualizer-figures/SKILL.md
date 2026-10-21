---
name: ieevisualizer-figures
description: "Use when an agent makes a figure with ieeVisualizer: choosing a registered template vs composing FigureSpec marks (and when to escalate to a specialist adapter or, rarely, bespoke code), binding data with dtypes, units, nulls and provenance, validating, rendering to PNG/SVG/PDF, looking at the rendered image, fixing problems with JSON-pointer patches instead of regenerating, and exporting with a provenance manifest."
license: CC-BY-4.0
---

# Making figures with ieeVisualizer

ieeVisualizer turns evidence into figures; it does not fetch data, compute
statistics or decide what the evidence means. Your job: pick the cheapest
form that expresses the claim, bind the data honestly, check the result by
looking at it, and leave a reproducible record.

## The extensibility ladder

Climb only as far as the figure needs.

1. **Registered template.** A proven pattern with typed slots and built-in
   checks. Today: `timeseries` (units, forecast split, caller-supplied bounds,
   target line), `bar_comparison`, `estimate_comparison`, `funnel`,
   `vector_field_2d`, `distribution` (named distributions from closed
   forms), `sample_distribution` (histogram + KDE, ECDF, quantile dotplot),
   `fan_chart` (quantile bands over time), and the network templates
   `network`, `org_chart`, `dependency_map`.
   `templates.list_templates()`, `templates.describe(name)`.
2. **Compose registered primitives.** Write a `FigureSpec` from the eight
   marks (`line`, `scatter`, `bar`, `area`, `histogram`, `heatmap`, `quiver`,
   `function`), axes and annotations. Novel figures, declaratively; patchable.
3. **Specialist adapter or plugin.** A renderer or component for what the
   primitives cannot express (3D meshes, animation, Manim). Selected by
   capability; `CapabilityError` lists what is missing.
4. **Bespoke frontend code.** Rare, consciously authorised escape hatch:
   sandboxed, versioned, scoped to explicit data and permissions, tested for
   accessibility, and a candidate for promotion to a component if it recurs.

Anti-patterns: hand-written Matplotlib or a generated Vue/React app for a
line chart, bar chart, KPI or flowchart (no validation, no provenance, no
patching); the opposite, forcing a scientific figure into a dashboard
template that cannot express it.

Beyond single figures: a `ViewSpec` (`ieeVisualizer.view`, docs/VIEWS.md)
composes figures with text, KPI tiles, tables, notes and flow diagrams;
`ieeVisualizer.network` draws graphs (docs/NETWORKS.md). Themes are
registered, versioned data (`themes.list_themes()`); name one in
`spec.theme`, pinned as `name@version` for reproducibility, instead of
styling by hand. Intervals: `band` and `errorbar` marks, or `y_lower` /
`y_upper` on a line, scatter or vertical bar, each with its `interval_kind`
and `interval_level` (docs/SPEC.md "Intervals"). Simulated inputs:
`ieeVisualizer.stochastic` (`random_walk`, `gbm`), seeded and marked
synthetic. Not yet available: small multiples in one FigureSpec,
subtitles, an ensemble mark drawing every trajectory. Do not fake them;
say what is missing and use the nearest honest form.

## Workflow

1. **Write the claim and the reader** (one sentence with a number; manager,
   researcher, public). Decide whether a chart is needed at all
   (`chart-choice-by-relationship`).
2. **Discover.** `list_templates()`; `describe(name)` returns columns,
   parameters, notes and an example payload. Start from the example.
3. **Bind data.** Each column: `dtype`, `unit`, and where relevant
   `description`, `denominator`, `aggregation`. Missing values are `None`.
   Dataset `provenance`: `source`, `query`, `retrieved_at` (with offset),
   `timezone`, `run_id`. Never convert units, fill nulls or compute intervals
   here; that belongs upstream.
4. **Check.** Template: `t.check(data, **params)` (never raises), then
   `t.build(...)`. Composed: `validate(spec)`. Every issue has a JSON-pointer
   `path`, a `code`, a `message` naming the fix, and a `severity`.
5. **Render** at the final size: `render(spec, RenderRequest(format="png",
   width=, height=, dpi=))`. Read `result.warnings`; each one is either fixed
   or explained in the caption.
6. **Look at the image.** Open the PNG and run the inspection list below.
   Specs that validate can still clip a title, put the biggest bar at the
   bottom, or claim more than the data shows.
7. **Patch, do not regenerate.** `apply_patch(spec, [{"op": "replace",
   "path": "/axes/x/label", "value": "…"}])` returns a new validated spec.
8. **Export** with `artifacts.export(spec, ["png", "svg"], writer)`; report
   the `artifact_id` and any warnings alongside the figure.

Runnable examples (template and composed): `references/examples.md`.

## Inspection list (on the rendered image)

- [ ] Title readable and not clipped at the final width; it states a claim
      the data supports, including any missing category.
- [ ] Axis labels in words with units; no raw column names (`conv_rate`);
      the unit does not just repeat the label ("Orders (orders)").
- [ ] Sparse series (a few weekly points, points between gaps) have markers.
- [ ] Ranked bars: largest at the top (categories are placed in order of
      first appearance, bottom-up on a horizontal bar chart).
- [ ] Bars and areas start at zero (`axes.*.limits: [0, null]`).
- [ ] Gaps visible and explained ("no data" slots, broken lines).
- [ ] Forecast visibly different from observed and named in the legend.
- [ ] Legend not covering data (automatic placement can still overlap; patch
      `/legend/position`); few series; colours distinguishable.
- [ ] Caption: measure, period, source, retrieval time, gaps, forecasts.

## What the library enforces vs what you guard

| Rule | Enforced by ieeVisualizer | How |
|---|---|---|
| Nulls never drawn as 0 | yes | null stays null; gaps, "no data" bar slots, `null_values_omitted`; `empty_series`, `all_null_column`, `empty_dataset` errors |
| Units never converted | yes | units stored verbatim; `mixed_units`, `unit_override_conflict` (templates), `axis_unit_conflict` (validate) |
| Forecast distinct from observed | yes | `role="forecast"` always dashed/translucent/hatched; `forecast_style_overridden` |
| No invented uncertainty | yes | bounds only from caller columns, drawn as given; a null bound is a gap |
| Interval states level and kind | yes | `interval_kind` + `interval_level` required (`missing_interval_kind`, `missing_interval_level`); shown in the legend, or the caption when the legend is hidden |
| Dual y-axes impossible | yes | spec 1.0 has one y axis |
| Dates are not numbers | yes | `scale_dtype_mismatch` for numbers on a time axis |
| Log axes positive | yes | `log_scale_nonpositive` |
| Reproducible output | yes | canonical JSON, `spec_hash`, byte-identical SVG/PDF, manifest |
| Bars from zero | **no** | you set limits; check the image |
| Provenance filled in | **no** | empty `source` validates; treat it as a blocker |
| Title/caption truthful | **no** | `headline-and-deck`, `figure-review-redteam` |
| Complete periods, fair comparisons | **no** | `when-numbers-lie-audit` |
| Colour contrast, alt text | **no** | `color-and-accessibility` |

## Errors you will meet

| Exception / code | Meaning | Do |
|---|---|---|
| `TemplateInputError` (`.issues`) | request does not fit the template | fix the parameter/column at `issue.path`; messages offer did-you-mean |
| `SpecValidationError` | spec has errors | patch at each `issue.path` |
| `SpecParseError` | malformed JSON form (unknown key, bad `schema_version`) | rebuild that part from `describe()`/docs |
| `UnresolvedDatasetError` | a `DatasetRef` needs a resolver | pass `resolver=` |
| `CapabilityError` | no adapter can draw this | simplify, or climb the ladder |
| `RenderError` `empty_series` | a layer has no complete row | drop the layer and say why |

Adapted in part from ieeVisualizer's own documentation (`docs/`, MIT);
changed: rewritten as an agent workflow with an inspection list.
Sources and licences: `SOURCES.md`.
