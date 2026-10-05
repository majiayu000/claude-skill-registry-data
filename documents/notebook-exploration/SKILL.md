---
name: notebook-exploration
description: "House pattern for looking at what a stage produced — a live-kernel Python notebook brushing an embedding with jscatter, or a rendered Quarto/R notebook re-plotting the numbers. Ask the user what they need to see and which flavor before scaffolding. Exploration informs a judgement; it latches nothing and blocks nothing."
license: MIT
---

# Notebook Exploration

## Overview

A stage finishes and someone has to look. Is that high-mito FOXP3 corner one donor or a real
population? Does the significance cut hold up across contrasts? These are questions a summary
table cannot settle — you have to see the data and turn it over.

This skill is the house pattern for that looking. Two flavors, one purpose:

- **Python, live kernel** — jscatter linked panels you brush and lasso, selections pulled into
  pandas and characterized on the spot.
- **Quarto/R, rendered** — a read-only notebook that re-plots what the stage wrote and lays out
  the numbers, committed so others can read it on GitHub.

Exploration produces **evidence and a reading**. It records no verdict a machine consumes, and
nothing downstream waits on it. What you conclude goes to a topic note under
`docs/_internal/<stage-stem>/` (skill: `reasoning-trace`). A notebook cell is a working surface
that the next run overwrites; the note is the record.

---

## Ask before you scaffold

**Do not infer the shape of the notebook from context. Ask the user.** Two questions, plainly,
before any file is created:

1. **What do you want to see, and what will you do with it?** A pocket of cells to identify, a
   threshold to sanity-check, a comparison across conditions, a first look with nothing
   specific in mind — each leads somewhere different, and guessing wastes the setup.
2. **Python live kernel, or Quarto/R rendered?**

If the answer to (1) is *relabel or drop cells across many sessions*, this is the wrong skill —
use `notebook-annotation`, which owns multi-round selection campaigns.

Put the choice to the user in one line each:

| | Python, live kernel | Quarto/R, rendered |
|---|---|---|
| You want to | brush, lasso, recolor, pull cells into pandas | re-plot the stage's numbers and read them |
| Needs | a running Jupyter kernel (VS Code, JupyterLab) | nothing live; `Rscript render.R` |
| Produces | barcodes + a labelled snapshot | committed GFM markdown + PNGs, and HTML |
| Shareable | no — it is a steering surface | yes — renders inline on GitHub |
| Data | compact parquet under `03_results/interactive/` | reads `03_results/` + config directly |

Mixed answers are common and fine: brush in Python to find the thing, then write the Quarto
notebook that shows it to everyone else.

---

## Both flavors are read-only

Whichever flavor, the notebook **computes nothing a later stage consumes**. It reads
`03_results/` and `02_analysis/config/analysis_config.yaml` and re-plots. Authoritative outputs
belong to numbered stages (skill: `analysis-code-conventions`). Keep the notebook in its own
folder under `02_analysis/notebooks/<NN>_<stage>_<explore|review>/` so its outputs stage as one
unit.

---

## Python flavor — live kernel and jscatter

### Export-first discipline

**Never open the multi-GB `.h5ad` checkpoint in the explorer kernel.** A project-owned
`02_analysis/stages/export_explorers.py` (copy `assets/export_explorers_skeleton.py` and fill
the `# TODO(project):` stubs) materializes a **compact parquet per inflection point** under
`03_results/interactive/`:

```
03_results/interactive/
├── 01_qc_explore.parquet          # x,y + a few QC obs + a handful of markers/scores
├── 02_annotation_explore.parquet  # x,y + frozen labels + markers
└── ...
```

Each table is 2D coords + a few obs columns + a handful of gene/score columns, indexed by cell
barcode. `load_explorer("01_qc", config=config)` reads it instantly. The exporter is a
**read-only projection** of already-computed checkpoints; it recomputes no biology. Re-run it
whenever the upstream checkpoint changes.

### The OOM lifecycle contract (read this first)

**This is the #1 reliability requirement.** jscatter panels are **ipywidgets**: every panel a
cell builds stays alive in the kernel until you call `.widget.close()` on it. A live session
re-runs the grid cell many times while brushing — and each re-run *adds* four more live panels
on top of the old ones. Within a dozen re-runs the accumulated dead widgets **OOM the kernel**.

The contract that prevents this: **always drive panels through `grid()` / `close_panels()` /
`live_panels()`; never a raw `_mk` loop in a cell.**

```python
PANELS = grid(df, CHANNELS)     # closes ALL prior panels first, then builds + registers the new ones
sel = first_selection()          # reads the live panels grid() registered — no variable-name traps
close_panels()                   # manual escape hatch: free every live panel (a standalone cell)
```

- `grid()` calls `close_panels()` **before** building, so re-running the grid cell never
  accumulates widgets — the count of live panels stays bounded by one grid.
- `first_selection()` with no argument reads `live_panels()`, so `df.iloc[first_selection()]`
  works no matter which panel you lassoed.
- Keep a **standalone `close_panels()` cell** as an escape hatch: if a grid ever lags, run it to
  free every live widget before rebuilding.

**Anti-pattern (do NOT do this):**

```python
# WRONG — leaks a new panel per channel per re-run → kernel OOM
PANELS = [_mk(c) for c in CHANNELS]
jscatter.compose([(s, c) for s, c in zip(PANELS, CHANNELS)], ...)
```

### Keep it small

One notebook per inflection point, three moving parts: **one** `CHANNELS = [...]` selector you
edit and re-run to recolor; **one** 2–4 panel linked grid; **one** pandas extraction. Resist a
second and third notebook, per-panel dashboards, or a widget for every knob — the value is in
looking and lassoing.

### The `interactive:` config block

Project-specific lists are config-driven, never hardcoded in the helper lib. Copy
`assets/interactive-config-snippet.yaml` into `02_analysis/config/analysis_config.yaml`:

| Key | Default | Governs |
|---|---|---|
| `export_stages` | `[]` | which stage checkpoints the exporter materializes |
| `load_coords_obsm` | `""` | which `obsm` embedding the exporter reads as x,y |
| `save_selection_cols` | `[x, y]` | columns persisted per selection (extend, do not shrink) |
| `categorical_obs` | `[]` | obs columns `grid()` always treats categorical |
| `marker_genes` | `[]` | marker genes the exporter adds as columns |
| `signatures` | `{}` | named gene sets the exporter scores per cell |
| `summary_stats` | `[]` | composition stats in the selection summary (`{name, column, value?}`) |

`grid_height`, `grid_rows`, and `cmap` are also read from this block with sensible floors.

### Quick start

```bash
# 1. one explorer per inflection point, in its own folder
mkdir -p 02_analysis/notebooks/01_qc_explore
cp $SKILL/assets/explorer.qmd 02_analysis/notebooks/01_qc_explore/01_qc_explore.qmd

# 2. copy the exporter skeleton into the project and fill the # TODO(project): stubs
cp $SKILL/assets/export_explorers_skeleton.py 02_analysis/stages/export_explorers.py

# 3. add the interactive: block to config
cat $SKILL/assets/interactive-config-snippet.yaml >> 02_analysis/config/analysis_config.yaml

# 4. build the compact tables, then open the .qmd on a LIVE kernel
python 02_analysis/stages/export_explorers.py
```

Verify:

```bash
ls 03_results/interactive/*_explore.parquet          # compact tables exist
ls 02_analysis/notebooks/01_qc_explore/eda/selection_*.csv
ls 02_analysis/notebooks/01_qc_explore/eda/*.png
```

### The loop

```python
from helpers.interactive_style import (
    load_interactive_config, load_explorer, grid, first_selection, save_selection, snapshot)

config = load_interactive_config()
df = load_explorer("01_qc", config=config)

CHANNELS = ["FOXP3", "pct_counts_mt", "leiden", "tissue"]
PANELS = grid(df, CHANNELS, cat=["leiden", "tissue"])   # closes prior panels, builds + registers

# ...brush/lasso a pocket in any panel...
sel = first_selection()
sub = df.iloc[sel]
save_selection(df, sel, label="mt_hi_pocket", subdir="01_qc_explore", config=config)
snapshot(df, "FOXP3", name="mt_hi_pocket", subdir="01_qc_explore", indices=sel, config=config)
```

Characterize before you save, so the note you write is grounded:

```python
cols = [c for c in ["FOXP3", "CTLA4", "pct_counts_mt", "n_genes_by_counts"] if c in df.columns]
import pandas as pd
pd.DataFrame({"selected": df.iloc[sel][cols].mean(), "all": df[cols].mean()}).round(3)
```

Barcodes are the durable currency — re-derive indices in a later session from the saved CSV:

```python
saved = pd.read_csv("02_analysis/notebooks/01_qc_explore/eda/selection_mt_hi_pocket.csv", index_col=0)
sel_reloaded = df.index.get_indexer(saved.index)
sel_reloaded = sel_reloaded[sel_reloaded >= 0]     # keep barcodes still present in df
```

---

## Quarto/R flavor — rendered and shareable

### Layout

Each notebook lives in **its own folder** so its rendered outputs stage as one unit:

```
02_analysis/notebooks/
├── render.R                                  # one renderer for all notebooks
└── [NN]_[stage]_review/
    ├── [NN]_[stage]_review.qmd               # source
    ├── [NN]_[stage]_review.md                # committed GFM (renders on GitHub)
    ├── [NN]_[stage]_review.html              # committed standalone HTML
    └── [NN]_[stage]_review_files/figure-gfm/ # committed PNGs the .md references
```

Copy `assets/notebook.qmd` as the starting point. It re-plots live from the checkpoints and tables
through `figure-style`, so the notebook always reflects the current config rather than a
baked-in PNG.

### The setup chunk that makes it robust

The one piece you must not simplify. It forces a headless PNG device, resolves the compartment
root from a sentinel, and binds `here()` to that root rather than `getwd()`.

```r
#| label: setup
#| include: false
knitr::opts_chunk$set(echo = FALSE, message = FALSE, warning = FALSE,
                      fig.align = "center", out.width = "80%",
                      dev = "ragg_png", dpi = 150)   # headless PNG → _files/figure-gfm/
options(bitmapType = "cairo")                        # any bare png()/ggsave() stays headless-safe

# Resolve the compartment root: the notebook's own dir when knitr knows it (render),
# else walk up from the wd to a sentinel (interactive line-by-line). Bind here() to the
# resolved root so source()/readRDS() work from ANY launch directory.
.find_root <- function(sentinel = "02_analysis/config/analysis_config.yaml") {
  start <- tryCatch(dirname(knitr::current_input(dir = TRUE)), error = function(e) NA_character_)
  if (is.na(start) || !nzchar(start)) start <- getwd()
  d <- normalizePath(start, mustWork = FALSE)
  while (!file.exists(file.path(d, sentinel))) {
    parent <- dirname(d)
    if (identical(parent, d))
      stop("compartment root (", sentinel, ") not found above ", start,
           "\n  -> launch radian from inside the compartment, or render via notebooks/render.R")
    d <- parent
  }
  d
}
.root <- .find_root()
knitr::opts_knit$set(root.dir = .root)   # render pass runs from the compartment root
if (interactive()) setwd(.root)          # line-by-line runs agree with render
here <- function(...) file.path(.root, ...)   # anchored to root, never getwd()
```

Why each line earns its place is in `references/root-resolution.md` — read it before you
"simplify" the chunk, because the obvious simplifications reintroduce the bug it fixes.

### The body

Structure it as *question → evidence → reading*. Each section: a short framing of what is being
looked at, a plot rebuilt live from the checkpoint through `figure-style`, a table, and a "what
we see" paragraph. Pull parameters from config with inline R so the prose tracks whatever you
tweak.

### Quick start

```bash
mkdir -p 02_analysis/notebooks/17_signature_review
cp $SKILL/assets/notebook.qmd 02_analysis/notebooks/17_signature_review/17_signature_review.qmd
cp $SKILL/assets/render.R   02_analysis/notebooks/render.R          # once per project

# render both targets, from the COMPARTMENT ROOT
Rscript 02_analysis/notebooks/render.R 02_analysis/notebooks/17_signature_review/17_signature_review.qmd both
```

Verify:

```bash
# figures are committed PNGs (GitHub strips base64 data-URIs), not svg/base64
ls 02_analysis/notebooks/17_signature_review/17_signature_review_files/figure-gfm/*.png
grep -q 'figure-gfm/.*\.png' 02_analysis/notebooks/17_signature_review/17_signature_review.md && echo "GFM refs committed PNGs — OK"
```

### Headless / no-VS-Code operation

The pattern is IDE-agnostic. Under `docker exec` + nvim + tmux: launch `radian` from the
compartment root, send lines to the radian pane (`tmux send-keys`, or R.nvim/Nvim-R), and view
plots via **httpgd** served over http to the host browser. `Rscript render.R` produces the
committed GFM/HTML the same way it does under VS Code. See `references/headless-workflow.md`.

---

## Verification Checklist

- [ ] **The user was asked**, and the flavor was chosen rather than assumed.
- [ ] **Read-only:** the notebook writes nothing a later stage reads — grep for `write`,
      `saveRDS`, `ggsave` outside the notebook's own folder.
- [ ] **The reading is durable:** what you concluded, on what numbers, and which alternative you
      rejected are in `docs/_internal/<stage-stem>/`, not only in a cell.
- [ ] Python — **export-first:** the notebook loads `03_results/interactive/*_explore.parquet`,
      never an `.h5ad`. Grep the `.qmd` for `read_h5ad` / `sc.read` (should be absent).
- [ ] Python — **lifecycle-safe:** panels come from `grid(...)`, not a raw `_mk` loop, and a
      standalone `close_panels()` cell exists.
- [ ] Python — **selection persisted:** `eda/selection_<label>.csv` (barcode-indexed) and
      `eda/selections_index.csv` exist after a brush + save.
- [ ] Quarto — **root robustness:** `cd` into the notebook folder, launch `radian`, source the
      setup chunk; `here("02_analysis/helpers/figure_style.R")` resolves with no manual `setwd()`.
- [ ] Quarto — **headless figures:** the rendered `.md` references committed `figure-gfm/*.png`,
      not `.svg` and not base64 `data:` URIs.

---

## Common Pitfalls

### Pitfall: the kernel OOMs after a few grid re-runs

- **Symptom:** the kernel dies, or panels lag badly, after re-running the grid cell several times.
- **Cause:** raw `_mk` panel construction leaks an ipywidget per channel per re-run.
- **Fix:** build only through `grid()`, which closes all prior panels first. Keep a standalone
  `close_panels()` cell.

### Pitfall: `first_selection()` returns empty even though you lassoed

- **Symptom:** you brushed a clear pocket, and `sel` is empty.
- **Cause:** a later cell shadowed the `PANELS` variable, so the lookup reads a dead grid.
- **Fix:** call `first_selection()` with no argument — it reads the live registry `grid()`
  populated, not a variable.

### Pitfall: the kernel chokes loading the data

- **Symptom:** memory spikes on the first cell.
- **Cause:** the notebook opened the checkpoint `.h5ad` directly.
- **Fix:** export a compact parquet first; the kernel loads that.

### Pitfall: here() bound to getwd() breaks line-by-line runs

- **Symptom:** `source(here("02_analysis/helpers/figure_style.R"))` fails when you run chunks in
  radian, even though `knitr::opts_knit$set(root.dir=...)` is set.
- **Cause:** `opts_knit$set(root.dir)` changes the working directory for the *knit/render* pass
  only; it leaves `getwd()` alone in an interactive session.
- **Fix:** bind `here()` to the sentinel-resolved `.root`, and `if (interactive()) setwd(.root)`.
  Both are in `assets/notebook.qmd`.

### Pitfall: figures render as SVG with an X11 warning

- **Symptom:** `Warning: unable to open connection to X11 display ''`, and `_files/figure-gfm/`
  contains `*.svg`.
- **Cause:** R's default `bitmapType` is `Xlib`, which needs an X server; on a headless container
  `png()` fails and knitr silently falls back to `svg`.
- **Fix:** `knitr::opts_chunk$set(dev = "ragg_png")` plus `options(bitmapType = "cairo")`. Both
  are in the image and both are headless.

### Pitfall: GitHub shows broken images

- **Symptom:** the `.md` renders on GitHub but every figure is a broken-image icon.
- **Cause:** the render embedded base64 `data:` image URIs, which GitHub strips.
- **Fix:** render the GFM target with `rmarkdown::github_document()` (or `quarto render --to
  gfm`), which writes PNG files under `_files/figure-gfm/` and references them by path. Commit
  that directory. `assets/render.R` does this correctly.

---

## Resources

- **jscatter:** https://jupyter-scatter.dev/
- **Quarto with R (knitr engine):** https://quarto.org/docs/computations/r.html
- **GitHub-flavored markdown output:** https://pkgs.rstudio.com/rmarkdown/reference/github_document.html
- **ragg headless raster device:** https://ragg.r-lib.org/
- **Bundled templates:** `assets/explorer.qmd`, `assets/export_explorers_skeleton.py`,
  `assets/interactive-config-snippet.yaml`, `assets/notebook.qmd`, `assets/render.R`
- **Deep dives:** `references/root-resolution.md`, `references/headless-workflow.md`

---

## When not to use

- Do not treat a notebook cell as the record. What you concluded goes to a topic note under
  `docs/_internal/<stage-stem>/`; the notebook is overwritten on the next run.
- Do not let the notebook compute anything a later stage depends on. Authoritative outputs stay
  in numbered stages — use `analysis-code-conventions`.
- Do not run a relabelling campaign across many sessions here. That needs a selection manifest
  and rounds — use `notebook-annotation`.
- Do not `quarto render` the Python flavor as a headless artifact. Brushing has no meaning in a
  batch render.
- Do not use for software architecture or design review. Use `architecture-first-dev`.
- Do not use solely to interpret pathway or TF results. Use `bulk-rnaseq-gsea` or
  `bulk-rnaseq-activity-inference`.

---

## See also

- `figure-style` — Prerequisite; the styling and saving contract both flavors plot through
- `analysis-code-conventions` — Sibling convention; narrative stages and authoritative data flow
- `notebook-annotation` — Multi-round relabelling campaigns with a selection manifest
- `reasoning-trace` — Where the reading you reach becomes a durable, stage-keyed note
- `bulk-rnaseq-pathway-explorer` — A static, shareable HTML dashboard when the look must leave the notebook
- `container-port-tunnel` — Reaching a live server in the devcontainer from a laptop browser
