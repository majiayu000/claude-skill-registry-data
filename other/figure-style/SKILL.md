---
name: figure-style
description: "The one styling, saving, and captioning contract every viz stage in this repo uses. Use whenever you create, edit, or review a figure under 03_results/. Applies one unified legible style, emits a vector PDF and a raster PNG from a single plot object, and writes the table and caption atomically. Never call ggsave or plt.savefig directly."
license: MIT
---

# Figure-Style Contract

Every viz stage in this repo imports one shim and uses one set of functions. This skill documents that contract so you can write, review, or debug figures without guessing at conventions.

## Why

Figures are judged at two scales simultaneously: shrunk to a journal column (~89 mm) and projected to the back of a conference room. One set of numbers — one `analysis_config.yaml:figures` block — governs both. The contract applies ONE unified, legible style (no print/screen split) and emits it in BOTH formats from a single plot object: a vector `<name>.pdf` (cairo, Unicode glyphs, Illustrator-editable) and a raster `<name>.png`, same geometry, same theme. The font sizes are floors — raise them, do not go under them.

---

## Prerequisites — use the project shim

The per-project shim lives at `02_analysis/helpers/figure_style.{R,py}`. It sources the symlinked contract lib and loads `analysis_config.yaml` once, exposing a stable `FIG_CFG` handle. Import the shim; never source `figure_helpers.{R,py}` directly (the shim applies the fallback when the toolkit symlink is absent).

**R**
```r
source("02_analysis/helpers/figure_style.R")
# FIG_CFG is now available; pass it to every function as config = FIG_CFG
```

**Python**
```python
from helpers.figure_style import set_paper_style, save_overview, FIG_CFG
set_paper_style(config=FIG_CFG)   # call once, near the top of the viz stage
```

---

## The `analysis_config.yaml:figures` block

All geometry, font sizes, and sub-layout names are read from `02_analysis/config/analysis_config.yaml` under the `figures:` key. Key fields:

| Key | Default | Governs |
|---|---|---|
| `base_size` | 14 pt | base font floor (single tier) |
| `title_size` / `axis_title_size` | 16 / 13 pt | title (bold) / axis title (plain) |
| `width` / `height` | 8.5 × 6.5 in | the one shared canvas |
| `width_wide` / `width_narrow` | 13 / 6 in | two-column / single-column presets |
| `dpi` | 300 | raster (PNG) export |
| `formats` | `[pdf, png]` | both emitted for every figure |
| `top_n` | 20 | categorical axis cap |
| `running_sum_ylim` | `[-1, 1]` | shared running-ES y-range for series |
| `running_sum_heights` | `[2.4, 0.7, 0.9]` | running-sum panel proportions |
| `nes_cap` | 3.5 | NES bar-length clamp |
| `by_contrast_dir` | `by_contrast` | per-contrast sub-layout name |
| `overview_dir` | `_overview` | cross-contrast sub-layout name |

---

## Single-variant, dual-format pattern

`save_figure(plot, stage, name)` writes two files from one plot object:

- `<name>.pdf` — vector PDF via cairo, the shared geometry (`width` × `height`). Unicode direction glyphs (↑ ↓) render correctly; text stays Illustrator-editable. Dense layers marked rasterized (see below) embed as raster at `rasterized_dpi`; everything else stays vector.
- `<name>.png` — raster PNG at `dpi`, the same geometry and the same style.

There is no `.print`/`.screen` suffix and no per-variant tier — both files share one geometry and one theme. The caller owns ALL theming: `save_figure` never re-themes the plot, it only writes (so per-figure `theme()` tweaks you add after `project_theme()` survive). Stale same-stem `<name>.{png,pdf}` are purged before writing so the run owns its namespace. Use `wide = TRUE` for the two-column canvas. The legacy `variant=` argument is still accepted but ignored.

### Rasterize dense layers — small, openable PDFs

A vector PDF of a 100k-cell UMAP embeds one vector glyph per cell: tens of MB, slow to open, and it chokes Illustrator. The fix is to rasterize *only the dense dot layer* while keeping axes, ticks, and text vector. `save_figure` writes the PDF at `figures.rasterized_dpi` (default 600) so any rasterized layer stays crisp on a projector; the PNG stays at `figures.dpi` (300).

Mark the dense layer with `rasterize_axes()` — essential for scanpy embeddings, whose plotting calls do not expose a `rasterized=` argument:

**Python**
```python
ax = sc.pl.umap(adata, color="geno", size=POINT_SIZE, show=False)  # returns the Axes
rasterize_axes(ax)                                                 # dot layer → raster in the PDF
save_figure(fig, "02_eda", "umap_geno", config=FIG_CFG)
```

**R** (via `ggrastr`; a no-op with a note if `ggrastr` is absent):
```r
p <- ggplot(df, aes(UMAP1, UMAP2, colour = geno)) + geom_point() + project_theme(config = FIG_CFG)
p <- rasterize_axes(p, config = FIG_CFG)   # rasterise the Point layer
save_figure(p, "02_eda", "umap_geno", config = FIG_CFG)
```

For matplotlib artists you build yourself, pass `rasterized=True` directly (`ax.scatter(..., rasterized=True)`) — `rasterize_axes` is the convenience for plotting calls (scanpy) that hide the artist.

**R**
```r
p <- ggplot(df, aes(x, y)) + geom_point() + project_theme(config = FIG_CFG)
save_figure(p, "02_eda", "umap_clusters", config = FIG_CFG)
```

**Python**
```python
fig, ax = plt.subplots()
ax.scatter(x, y)
save_figure(fig, "02_eda", "umap_clusters", config=FIG_CFG)
```

---

## Results placement and adjacency — prefer `save_overview`

Use `save_overview(...)` for any overview or by-contrast figure. It writes three things atomically in one call:

1. `figures/_overview/<name>.{pdf,png}` (or `by_contrast/<contrast>/` when `contrast=` is given)
2. `tables/_overview/<name>.csv` — the data behind the figure, rounded for byte stability
3. `03_results/<stage>/README.md` — a path-qualified caption section with a **How to read** block

You cannot ship a figure without its neighbor table and caption. `save_overview` enforces this mechanically.

**R**
```r
save_overview(
  p, "04_gsea", "gsea_hallmark_heatmap",
  table     = df_results,
  finding   = "Hallmark IFN-alpha/gamma dominate the ISD90 response.",
  script    = "02_analysis/stages/11_gsea_viz.R",
  fn        = "save_overview",
  config_kv = "figures.nes_cap = 3.5",
  input     = "03_results/objects/gsea.rds",
  how_to_read = "Rows = pathways; color = NES (orange up / blue down); padj < 0.05 = bold.",
  config    = FIG_CFG
)
```

**Python**
```python
save_overview(
    fig, "04_gsea", "gsea_hallmark_heatmap",
    table      = rows,
    finding    = "Hallmark IFN-alpha/gamma dominate the ISD90 response.",
    script     = "02_analysis/stages/11_gsea_viz.py",
    fn         = "save_overview",
    config_kv  = "figures.nes_cap = 3.5",
    input      = "03_results/objects/gsea.rds",
    how_to_read= "Rows = pathways; color = NES (orange up / blue down); padj < 0.05 = bold.",
    config     = FIG_CFG,
)
```

For paths only (no plot to write yet): use `contrast_path(stage, contrast, kind, config)` or `overview_path(stage, kind, config)`. Never hand-build `03_results/...` paths.

---

## Captions

`write_caption` (called internally by `save_overview`) writes an idempotent section in `03_results/<stage>/README.md`. Each section contains:

- A path-qualified heading (`## figures/_overview/<name>.png`)
- A one-sentence scientific **finding**
- A mandatory `**How to read:**` block — glyphs, sign convention, claim tier
- A `| Script | Function | Config | Input |` provenance table

Re-running with the same `filename` replaces the existing section in place (never duplicates). The caption is keyed on the PNG artifact path as the representative deliverable.

---

## Comparability and byte stability

| Function | Purpose |
|---|---|
| `style_series(plot, ylim, config)` | Pin a shared running-ES y-range + single collected legend across a family of figures (identical panel proportions); `style_running_sum` is an alias |
| `scale_color_okabe(config=) / scale_fill_okabe(config=)` (R) · `okabe_palette(config=)` (Py) | Okabe-Ito colorblind-safe categorical palette from `colors.okabe_ito` |
| `append_master_table(df, database, stage, name, config)` | Idempotent cross-stage accumulator; deduped on `database` column; replaces rows on re-run |
| `round_numeric_cols(df, sig=9)` | Round all numeric columns to 9 significant digits for byte-stable CSV re-runs |
| `purge_figures(stage, prefix, ...)` | Delete stale `<prefix>*.{png,pdf}` before writing so a run owns its figure namespace |
| `direction_cue(value)` | Map a signed value to `↑ up` / `↓ down` / `· n.s.` — never a bare `*` |

---

## DO NOT — named anti-patterns

**DO NOT** call `ggsave()`/`plt.savefig()` directly in a viz stage. Route through `save_figure` or `save_overview` so the shared geometry and both formats are emitted and the namespace is purged.

**DO NOT** compute in a viz stage or plot in a compute stage. A compute stage (`02_analysis/stages/NN_<topic>.{R,py}`) writes `.rds`/`.h5ad` objects; its viz twin (`NN_<topic>_viz.{R,py}`, same number and stem) reads those objects and produces figures only. The `ggsave-inside-compute` pattern corrupts this separation.

**DO NOT** use inline `theme()` / `element_text(size=<num>)` / `ggsave(width=<literal>)` or raw hex color strings in a viz stage. All style decisions go through `project_theme(config=FIG_CFG)` (R) or `set_paper_style(config=FIG_CFG)` (Python). Inline overrides break the single-tier font floors silently.

**DO NOT** truncate axis labels or use ambiguous glyphs (`*`, `+`, bare colored dots without a legend key). Use `direction_cue()` for sign labeling. Truncated labels in a column-width PDF are unreadable.

**DO NOT** leave categorical axes uncapped. Cap to `figures.top_n` (default 20) before plotting. An uncapped axis silently pushes the most-important entries off the visible range when the figure is shrunk to print.

**DO NOT** ship a figure without its same-stem source table. `save_overview` writes both atomically; if you call `save_figure` directly you must also write the CSV and caption yourself.

---

## Done when

- Both `<name>.pdf` and `<name>.png` exist under the correct `<stage>/figures/<sub-layout>/` directory.
- A same-stem `<name>.csv` exists under the parallel `<stage>/tables/<sub-layout>/` directory.
- `03_results/<stage>/README.md` contains a path-qualified caption section for this figure with a non-empty `**How to read:**` block.

---

## See also

- `scrna-pipeline-conventions`
- `bulk-rnaseq-gsea`
