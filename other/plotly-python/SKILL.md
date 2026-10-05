---
name: plotly-python
description: Use for writing, reviewing, debugging, or testing interactive Python visualizations with Plotly, including Plotly Express, graph_objects Figure/trace/layout/frames, subplots and facets, hover/customdata, axes and legends, FigureWidget events, and HTML/image export. Do not use for Dash or Streamlit application architecture, Altair specifications, static Matplotlib-only plots, or data analysis without a Plotly figure.
argument-hint: "[Plotly figure task, trace/layout defect, facet, event, or export]"
---

# Plotly Python

Build and verify a figure tree. A Plotly figure has `data` traces, `layout`, and
optional `frames`; it is serialized to Plotly.js for rendering. Keep application
state and event transport in the host that actually supports them.

## Boundary

Use this skill when a project imports Plotly or explicitly requests a Plotly
figure. Do not route Dash callback graphs, Streamlit rerun/state design, Altair
Vega-Lite specs, or Matplotlib-only output here. A figure can contain controls,
but a standalone `Figure` is not a full server application.

## Know the objects

| Object | Meaning | Responsibility |
|---|---|---|
| `go.Figure` | Validated JSON-like figure tree | Own traces, layout, frames, and figure methods. |
| Trace | Typed series/mark set in `figure.data` | Own x/y/z/locations, name, legend group, hover/custom data, marker/line, subplot refs. |
| Layout | Figure-wide non-data presentation | Own title, axes, legend, color axes, annotations, shapes, margins, templates, subplots. |
| Frame | Named animation state | Own per-frame trace/layout changes and stable identity. |
| Plotly Express | High-level constructor returning `go.Figure` | Build common figures from tidy/wide data, color, facet, animation, hover. |
| FigureWidget | Widget-backed figure in an ipywidgets host | Enable Python callbacks on trace events in a displayed widget context. |
| Renderer/export | Host-specific materialization | Notebook/browser HTML, JSON, or image through optional engine. |

Read [the figure and trace model](references/figure-model.md) before mixing
Express with graph objects, editing facets/subplots, or debugging a schema path.

## Ordered workflow

1. State the analytical question, input and displayed grain, trace grouping,
   order, units, missing values, target host, and required interaction/export.
2. Start with Plotly Express for one standard figure described by dataframe
   columns. Use graph objects when trace-by-trace construction, specialized
   types, secondary axes, exact subplot assignment, or incremental mutation is
   essential.
3. Inspect the produced figure tree. Identify which fields create traces and
   which attributes belong to a trace, axis/subplot, color axis, or whole layout.
4. Add only contract-required layout, hover/customdata, ordering, facets,
   annotations, and controls. Do not replace data semantics with visual defaults.
5. For facets/subplots, define category/panel order, shared axes, matches,
   legend duplication, annotation labels, and trace targeting.
6. Choose the actual event host. Use `FigureWidget` callbacks only in a live
   ipywidgets context; use the application's callback/rerun API elsewhere.
7. Validate the JSON-compatible figure, test trace/layout semantics, then render
   or export in the real environment.

## Intent to API family

| Need | Start with | Switch/extend when |
|---|---|---|
| Common chart from dataframe columns | `plotly.express` | Customize returned `Figure` with update/add methods. |
| Exact trace composition | `go.Figure` + typed traces | Trace identity, order, subplot refs, or unsupported Express shape matters. |
| Small multiples | Express `facet_row`/`facet_col` | Use subplots for heterogeneous trace types or layouts. |
| Multiple panels | `make_subplots` + `add_trace(row=..., col=...)` | Secondary axes/specs/rowspan/colspan require explicit grid. |
| Same styling across traces | selector-based `update_traces` | Target by trace type/name/legend group, not fragile index alone. |
| Axes/layout | `update_xaxes`, `update_yaxes`, `update_layout` | Know whether a change is per-subplot or global. |
| Per-point hover payload | `hover_data`/`hovertemplate` + `customdata` | Keep stable record IDs in customdata for host events. |
| Animation | Express animation or `frames` | Frame/category order and trace identity are explicit. |
| Python click callback | `FigureWidget` | Only when displayed in supported ipywidgets context. |
| Web app events | Host framework callback/selection API | A plain figure callback will not execute on static HTML. |

## Canonical anchor

```python
import plotly.express as px


def sales_figure(data):
    fig = px.line(
        data,
        x="date",
        y="revenue",
        color="region",
        markers=True,
        category_orders={"region": ["North", "South", "West"]},
        custom_data=["record_id"],
        labels={"date": "Date", "revenue": "Revenue", "region": "Region"},
    )
    fig.update_layout(title="Revenue by region", hovermode="x unified")
    return fig
```

Express creates one or more traces based on discrete mappings/facets/animation.
Do not assume `fig.data[0]` represents all categories; inspect and target traces
semantically.

## Trace, layout, and facet invariants

- Put data arrays and per-series styling on traces; put figure/subplot guides,
  annotations, and template on layout.
- Keep x/y arrays aligned and define missing-value/line-gap behavior.
- Give traces stable `name`, `legendgroup`, and record identity where host
  events or updates depend on them.
- Set category order explicitly when business order differs from encounter or
  lexical order. Facet order and legend/color order can share that contract.
- With facets, decide axis matching and remove duplicated annotations/legends
  only through targeted figure operations.
- Avoid dual axes unless units and mapping are unmistakable; use small multiples
  when direct comparison would mislead.

Read [composition and events](references/composition-events.md).

## Verification and export

Use `fig.to_dict()`/`to_json()` to inspect semantic nodes. Test trace count/type,
x/y/customdata alignment, names/order, subplot refs, axis titles/types/ranges,
color scale/legend, frames, and absence of sensitive data. Do not snapshot the
entire default template. Read [export and testing](references/export-testing.md).

Inspect the installed version of Plotly and the target host before using a
drift-sensitive trace property, event API, renderer, or image engine. Plotly was
absent from this foundry during authoring, so source/static checks do not prove
rendering.

Completion requires a valid figure tree; correct trace and displayed grain;
explicit order/units/missing policy; no fragile trace-index mutation; truthful
event-host behavior; semantic tests; and a real-host HTML/image/widget render
when appearance or interaction is contractual.

## References

- [Figure, trace, and layout model](references/figure-model.md)
- [Composition, facets, and events](references/composition-events.md)
- [Export and semantic testing](references/export-testing.md)
