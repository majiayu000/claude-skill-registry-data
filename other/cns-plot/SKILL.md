---
name: cns-plot
description: Create, restyle, compose, and export compact publication-ready scientific figures with the Python cnsplots library or its source-derived Cell/Nature/Science plotting patterns. Use for cnsplots code, journal-sized Matplotlib/Seaborn figures, editable vector output, semantic scientific color systems, statistical annotations, dense rasterized layers, and mixed-size multi-panel layouts with precise text, artist, padding, margin, and panel-label control. Pair with nature-figure or scientific-visualization for broader figure strategy; use matplotlib, seaborn, adjusttext, or build-complexheatmaps when their lower-level or specialized APIs are needed.
---

# CNS Plot

Build a compact visual argument, not a decorated default plot. Use cnsplots when its
plot types fit; reuse its design language with ordinary Matplotlib or Seaborn when a
custom artist is clearer.

## Start with a figure contract

Before plotting, establish:

1. The claim each panel must support.
2. The data, unit, grouping, uncertainty, and statistical test behind each mark.
3. The final physical width, panel count, and target formats.
4. Whether downstream editing requires live text and vector objects.
5. The categorical identities and continuous quantities that colors must encode.

Do not infer a journal's current submission limits from the library name. Check the
target journal's live guidance when exact limits matter.

## Choose the implementation path

- Use **cnsplots end to end** for its built-in statistical, genomic, survival,
  heatmap, set, Sankey, and multi-panel plots.
- Use **cnsplots styling around Matplotlib/Seaborn** when the chart needs custom
  artists or an API that cnsplots does not expose.
- Use **plain Matplotlib/Seaborn with the distilled rules** when cnsplots is not
  installed or would add unnecessary dependencies.
- Use `nature-figure` first when the figure's evidence structure, panel narrative,
  or journal strategy is still unresolved.

Install the library into the active project rather than the global interpreter:

```bash
uv add cnsplots
```

The inspected upstream version requires Python 3.10+ and uses Matplotlib 3.10.x.
Verify the installed version before relying on version-specific behavior.

## Use the core workflow

### 1. Set style without leaking global state

Prefer a temporary settings context when changing defaults:

```python
import matplotlib as mpl
import cnsplots as cns

with mpl.rc_context(), cns.settings.context(
    palette_qual="OkabeIto",
    palette_seq="YlGnBu_custom",
    title_fontsize=8,
    legend_fontsize=7,
    axes_linewidth=0.5,
):
    cns.figure(width=252, height=180)
    ax = cns.boxplot(data=df, x="group", y="value")
    ax.set(xlabel="", ylabel="Response (a.u.)")
    cns.savefig("figure.svg")
```

Keep width first and height second. cnsplots treats layout units as pixels at a
72-DPI base, so `252 px` is approximately `89 mm`.

### 2. Build on explicit axes

Pass `ax=` whenever a function accepts it. Return and retain each axes for later
label, legend, and limit changes. Use `cns.setup_ax(ax)` to bring axes produced by
another library into the same typographic and spine system.

### 3. Separate semantic mappings

- Map unordered classes to a qualitative palette with stable class-to-color keys.
- Map ordered magnitudes to a sequential colormap.
- Map signed deviations around a meaningful midpoint to a diverging colormap.
- Keep thresholds, reference values, and nonsignificant observations neutral unless
  direction itself is the message.
- Add shape, line style, direct labels, or facets when color alone is insufficient.

### 4. Compose from simple artists

Build unusual plots from a small vocabulary:

- `plot`, `vlines`/`hlines`, and `scatter` for trajectories and lollipops.
- `errorbar` for estimates and confidence intervals.
- `fill_between` for uncertainty bands and flows.
- `bar`/`barh` for counts, proportions, and aligned secondary panels.
- `text`/`annotate` for direct labels; use collision adjustment for dense labels.
- `axvline`/`axhline` for scientifically meaningful references.

Reserve higher `zorder` for marks and annotations; keep supporting stems, bands,
and grids behind them. Rasterize only dense data layers, not labels, axes, or
annotations.

### 5. Lay out panels in final-size units

```python
import cnsplots as cns

mp = cns.multipanel(max_width=518, title="Response overview", loc="left")

ax_a = mp.panel("A", width=150, height=145, pad_left=8, pad_top=6)
cns.boxplot(data=df, x="group", y="value", ax=ax_a)

ax_b = mp.panel(
    "B",
    width=220,
    height=145,
    pad_left=8,
    pad_top=6,
    margin_right=0,
)
cns.scatterplot(data=df2, x="x", y="y", hue="class", ax=ax_b)
cns.take_legend_out(ax=ax_b)
```

Treat `width` and `height` as the axes content area. Treat `pad_left`/`pad_top`
as the gap between the panel label and rendered decorations. Treat margins as
spacing between whole panels. Let the library draw once and remeasure titles,
tick labels, and helper axes before export.

### 6. Export and inspect

Prefer SVG or PDF for plots and high-resolution PNG/TIFF only when raster output is
required. Keep SVG text editable with `svg.fonttype="none"` and PDF fonts as Type 42.
cnsplots uses a MuPDF-assisted SVG cleanup path when `mutool` is available and falls
back to standard Matplotlib SVG otherwise.

Export at least one vector file and one raster preview. Inspect the actual outputs at
final size for clipping, font substitution, panel-label collisions, colorbar/legend
placement, and rasterized text.

## Apply the design language

Read [design-language.md](references/design-language.md) whenever changing text,
colors, graphical objects, panel geometry, or export behavior.

Read [recipes.md](references/recipes.md) when choosing a plot family or implementing
a cnsplots, Matplotlib, Seaborn, heatmap, volcano, forest, or flow pattern.

## Quality gate

Before delivery:

- Verify labels include units and category order is intentional.
- Verify statistical annotations name the test and match the plotted comparison.
- Verify colors retain meaning across panels and remain distinguishable.
- Verify every panel reads at the final physical size.
- Verify legends and colorbars do not obscure data.
- Verify dense layers are rasterized only when useful.
- Verify SVG/PDF text remains editable and Unicode glyphs render correctly.
- Verify the vector and raster exports share the same bounds.
- Keep the plotting code, environment specification, and data transformation
  reproducible.

## Source basis

This skill distills `faridrashidi/cnsplots` at main commit
`f0543f2e07d1b602ce5cff18e06c1c9b91fcae15`, package version `0.5.0`, inspected
2026-07-28. The upstream project is BSD-3-Clause licensed. Reinspect upstream source
and docs when the installed version differs.
