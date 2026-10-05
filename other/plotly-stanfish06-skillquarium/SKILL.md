---
name: plotly
description: >
  Use when creating interactive Python visualizations with Plotly, including
  pan, zoom, hover charts, dashboard figures, interactive HTML output, or 3D
  plots. Trigger terms include plotly, interactive chart, interactive plot,
  dashboard chart, hover, and plotly express. For static publication figures
  use matplotlib or seaborn; for visualization strategy use
  scientific-visualization.
license: MIT
allowed-tools:
  - Read
  - Write
  - Bash
compatibility: Requires Python 3.9+ and Plotly 5.24+ (examples target 6.x, current as of 2026). Install with `uv add plotly` or `pip install plotly`. Static image export needs Kaleido; on Plotly 6.1.1+ use Kaleido v1 (`pip install kaleido`) plus a locally installed Chrome (`plotly_get_chrome`). Interactive charts render in browsers, Jupyter, and VS Code with no extra JS.
metadata: {"version": "1.0", "skill-author": "vault-audit"}
---

# Plotly

## Overview

Plotly is Python's main library for **interactive** visualization. Every figure is a
JSON-backed object rendered by plotly.js in the browser, so charts pan, zoom, and show
hover tooltips out of the box, and can be embedded in HTML pages, Jupyter notebooks, or
Dash apps. Two APIs sit on the same figure model:

- **`plotly.express` (px)** — high-level, one call per chart, tidy-DataFrame oriented.
  Returns a fully-built `go.Figure`. Start here for almost everything.
- **`plotly.graph_objects` (go)** — low-level. You assemble a figure from **traces**
  (the data: `go.Scatter`, `go.Bar`, ...) and a **layout** (axes, legend, title). Use
  when you need mixed trace types, secondary axes, or fine control px does not expose.

Because px *returns* a `go.Figure`, the normal workflow is "build with px, then refine
with `go` methods" (`update_layout`, `update_traces`, `add_trace`).

## Installation

```bash
uv add plotly           # or: pip install plotly
# Static image export (PNG/PDF/SVG). Plotly 6.1.1+ uses Kaleido v1:
uv add kaleido
plotly_get_chrome       # one-time: installs the Chrome that Kaleido v1 drives
```

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio      # renderers, templates, export helpers
```

`px` bundles sample datasets: `df = px.data.iris()`, `px.data.gapminder()`, `px.data.tips()`.

## Core workflow

### plotly.express (high-level)

```python
df = px.data.gapminder().query("year == 2007")

# Scatter with color/size/hover encodings — px maps DataFrame columns to visuals
fig = px.scatter(
    df, x="gdpPercap", y="lifeExp",
    color="continent", size="pop", size_max=60,
    hover_name="country", log_x=True,
    labels={"gdpPercap": "GDP per capita", "lifeExp": "Life expectancy"},
    title="Wealth vs. health, 2007",
)
fig.show()   # opens interactive chart (browser / inline in notebook)
```

Common chart types share the same signature — swap the function:

```python
px.line(px.data.stocks(), x="date", y="GOOG")                 # line / time series
px.bar(df, x="continent", y="pop", color="continent")          # bar (barmode="group"|"stack")
px.box(px.data.tips(), x="day", y="total_bill", color="smoker")# box
px.violin(px.data.tips(), y="total_bill", x="day", box=True)   # violin
px.histogram(px.data.tips(), x="total_bill", nbins=30)         # histogram
px.imshow(df.corr(numeric_only=True), text_auto=".2f",         # heatmap (matrix)
          color_continuous_scale="RdBu", zmin=-1, zmax=1)
px.scatter_3d(px.data.iris(), x="sepal_length", y="sepal_width",
              z="petal_width", color="species")                # 3D scatter
```

**Faceting** (small multiples) is a keyword, not a separate API:

```python
fig = px.scatter(px.data.tips(), x="total_bill", y="tip",
                 color="sex", facet_col="time", facet_row="smoker")
```

### graph_objects (low-level)

Use `go` when a single px call cannot express the figure — e.g. overlaying a bar and a
line series, or a secondary y-axis:

```python
fig = go.Figure()
fig.add_trace(go.Bar(x=months, y=revenue, name="Revenue"))
fig.add_trace(go.Scatter(x=months, y=margin, name="Margin %",
                         yaxis="y2", mode="lines+markers"))
fig.update_layout(
    title="Revenue and margin",
    yaxis=dict(title="Revenue ($)"),
    yaxis2=dict(title="Margin (%)", overlaying="y", side="right"),
    template="plotly_white",
)
```

### Subplots

`make_subplots` builds a grid; add each trace to its `row`/`col`. Mixed types (e.g. a 3D
scene next to a 2D chart) need a `specs` grid:

```python
fig = make_subplots(rows=1, cols=2, subplot_titles=("Scatter", "Surface"),
                    specs=[[{"type": "xy"}, {"type": "scene"}]])
fig.add_trace(go.Scatter(x=x, y=y, mode="markers"), row=1, col=1)
fig.add_trace(go.Surface(z=z), row=1, col=2)
fig.update_layout(height=500, showlegend=False)
```

### Updating layout, traces, axes

```python
fig.update_layout(title="...", template="plotly_dark",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                  margin=dict(l=40, r=20, t=60, b=40))
fig.update_traces(marker=dict(size=8, line=dict(width=1, color="white")),
                  selector=dict(type="scatter"))   # target specific traces
fig.update_xaxes(title="Time", showgrid=False, rangeslider_visible=True)
fig.update_yaxes(type="log")
```

### Hover and legends

```python
# px: pick tooltip fields
px.scatter(df, x="x", y="y", hover_name="id", hover_data={"pop": ":,.0f", "x": False})

# go / any figure: custom hover template + unified hover across traces
fig.update_traces(hovertemplate="<b>%{x}</b><br>value: %{y:.1f}<extra></extra>")
fig.update_layout(hovermode="x unified")          # or "closest"
fig.update_layout(legend=dict(title="Series"), showlegend=True)
```

### Export

```python
fig.write_html("chart.html")                 # self-contained interactive page
fig.write_html("chart.html", include_plotlyjs="cdn")  # smaller file, needs internet
fig.write_image("chart.png", scale=2, width=1000, height=600)  # static; needs Kaleido
fig.write_image("chart.pdf")                 # also svg, jpeg, webp
html_str = fig.to_html(full_html=False)      # snippet to embed in a larger page
```

## Gotchas / best practices

- **Static export needs Kaleido + Chrome.** `write_image` / `to_image` require Kaleido.
  On Plotly 6.1.1+ (Kaleido v1) Chrome is *not* bundled — run `plotly_get_chrome` (or
  `plotly.io.get_chrome()`) once, or you get a "Chrome not found" error. Do **not** pass
  the `engine=` argument: it is deprecated in Plotly 6.2. For interactive output prefer
  `write_html`, which needs neither Kaleido nor Chrome.
- **px vs go — pick by shape of the work.** Reach for px first: it wires up color/size
  legends, faceting, and hover from a tidy DataFrame in one line. Drop to go only for
  mixed trace types, secondary axes, or per-trace control. Never rebuild a px chart by
  hand — build with px, then `.update_layout()` / `.update_traces()` to refine.
- **Large data → WebGL.** SVG traces (`go.Scatter`) bog down past ~10k points. Use the
  GL-backed equivalents (`go.Scattergl`, `go.Scatter3d`) or `px.scatter(..., render_mode="webgl")`.
  For very dense scatter/heatmap data use `px.density_heatmap` / `go.Histogram2dContour`
  to bin instead of drawing every point. Downsample time series before plotting.
- **Tidy (long-form) DataFrames** make px effortless: one column per variable, one row
  per observation, then map columns to `x`/`y`/`color`/`facet_*`. Reshape wide data with
  `df.melt(...)` first.
- **Themes** via `template=` ("plotly", "plotly_white", "plotly_dark", "simple_white",
  "presentation", ...). Set a default once: `pio.templates.default = "plotly_white"`.
- **Rendering context.** If `fig.show()` shows nothing, set the renderer explicitly:
  `pio.renderers.default = "browser"` (or `"notebook"`, `"vscode"`, `"png"`).
- **Dash for apps.** Turn figures into an interactive web app with callbacks:
  `pip install dash`; put figures in `dcc.Graph(figure=fig)`, wire inputs/outputs with
  `@callback`, and run with `app.run(debug=True)` (Dash 3.x; the old `app.run_server` is
  deprecated). Dash is a separate deployment concern — build and test the figure with
  plotly first, then embed it.

## Use this vs related skills

Use **plotly** for interactive/hover/dashboard charts and interactive HTML; use
**matplotlib**/**seaborn** for static publication figures (PNG/PDF/SVG); use
**scientific-visualization** for the broader figure-strategy and journal-formatting skill.
