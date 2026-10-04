---
name: stata-style-figures
description: Style every matplotlib figure like the Stata 18/19 default (stcolor) scheme — Arial embedded as TrueType, white background, recessive light-gray grid below the data, no top/right spines, unframed legends, and the validated blue/red/gray palette. Use whenever a task generates or restyles charts, plots, or figures for papers, reports, or slides, even if the user doesn't mention Stata — this is the house style for all publication figures. Also use when asked to make figures "look like Stata", match the stcolor scheme, or restyle existing matplotlib output.
---

# Stata-style (stcolor) matplotlib figures

House style for publication figures, extracted from validated generators. Paste the
rcParams block, use the palette constants, follow the grid rule, and never let a
restyle change data content.

## rcParams — paste at the top of every figure script

```python
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial", "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "pdf.fonttype": 42, "ps.fonttype": 42,   # embed fonts as TrueType
    "font.size": 9, "axes.linewidth": 0.6, "axes.edgecolor": "0.2",
    "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True,
})
```

`font.size` 9 for single/1x2 panels; drop to 8.5 when panels are dense (many tick
labels). Figure width 6.5 in = `\textwidth` at 1-inch margins; include at
`width=\textwidth` so fonts render at stated size (no downscaling).

## Palette

```python
STC_BLUE       = "#1f77b4"   # protagonist series
STC_RED        = "#d62728"   # accent / contrast series
STC_GRAY       = "0.62"      # de-emphasised series
STC_BLUE_LIGHT = "#c1d9ec"   # shaded bands / intervals (light step of the blue)
STC_GRID       = "#e3e6e8"   # gridlines
```

Baseline-vs-corrected comparisons: dashed gray baseline (`color="0.50", ls="--"`)
vs solid blue corrected. Background/context shading: `axvspan(..., color="0.93")`.

## Per-axes styling

```python
ax.grid(axis="y", color=STC_GRID, lw=0.6, zorder=0)   # horizontal gridlines only
ax.tick_params(length=2.5, color="0.4")
ax.legend(frameon=False)
```

Grid rule: value-axis gridlines only. Vertical charts (time series, vertical bars)
get `axis="y"`; horizontal bar/dot charts get `axis="x"` instead. Never both.
White figure and axes background (matplotlib default — don't set facecolors),
no chart junk.

## Output format — PNG by default

Save charts, figures, and visual diagrams as `.png` unless the task explicitly
asks for another format (a LaTeX manuscript pipeline that `\includegraphics` a
PDF, for instance, keeps PDF):

```python
fig.savefig(path.with_suffix(".png"), dpi=300)
```

300 dpi keeps text crisp at print size. The font-embedding rcParams
(`pdf.fonttype`) are harmless for PNG — keep the block as is so a later PDF
export just works.

## Semantics rule — restyling never changes content

A restyle touches colour and font only. Encodings that captions or notes describe
— filled vs open markers, dashed vs solid lines, shading, marker sizes that carry
meaning — stay exactly as they were. Verify: hash the underlying data artifacts
(tables, JSON, parquet the figure is built from) before and after; they must be
identical. If the generator emits a numbers JSON or .tex alongside the figure,
those hashes are the check.

## Chart-type patterns

The style was validated across these chart types; the rcParams block and palette
above carry everything needed to reproduce them:

- multi-panel time series with a shaded band and baseline-vs-corrected series
- horizontal dot/lollipop rankings (vertical-only grid; filled/open/gray marker semantics)
- median curve with a min-max band (`STC_BLUE_LIGHT` fill)
- grouped-bar and reinstatement-style variants
