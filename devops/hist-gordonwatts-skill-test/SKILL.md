---
name: hist
description: Use when working with the scikit-hep hist library in Python to create, fill, slice, and plot histograms (1D/2D/multi-axis), including UHI indexing, categorical axes, and mplhep plotting conventions.
---

# Hist

## Overview

Use this skill to build and manipulate hist.Hist objects, choose axis/storage types, fill with data and weights, and produce publication-style plots with mplhep styles, all based on matplotlib.

## Quick start

- Create histograms with `Hist.new` plus axis builders (`Reg`, `Var`, `StrCat`) and finish with exactly one storage (`Int64` or `Weight`).
- Make sure axis labels contain a short variable name and units. Histogram titles should contains a slightly longer concise description of what data went into the plot.
- Fill with `.fill(...)` using axis names; note that `.fill` returns `None`.
- Slice or project with UHI indexing (e.g., `h.project("x")` or `h[{"x": 5j}]`).
- Plot with `hist.plot(...)` or `mplhep.hist2dplot(...)`; use `plt.style.use(hep.style.ATLAS)` for HEP-style plots.

## Core tasks

### Create axes and storage

- Use `Reg` for uniform bins and `Var` for variable-width bins.
- Use `StrCat` for categorical axes; set `growth=True` for auto-added categories.
- Choose storage: `Int64` for unweighted counts, `Weight` for weighted fills.

### Fill and access contents

- Fill with named axes (e.g., `h.fill(x=..., y=..., weight=...)`).
- Read counts with `h.view()` and errors from `np.sqrt(h.variances())`.

### Slice, rebin, and project

- Use UHI slicing (complex numbers for bin selection, `::2j` for rebinning).
- Project with `h.project("axis_name")` for 1D plots.

### Plot and save

- Use `hist.plot(histtype="fill")` for 1D; use `mplhep.hist2dplot` for 2D.
- Use `plt.subplots()` without custom `figsize` unless explicitly requested.
- Save with `fig.savefig("name.png")` and close with `plt.close(fig)`.

## References

- Use `references/hist-hints.md` for concrete code snippets and common patterns.
- Use `references/hist-advanced.md` for UHI indexing, plotting gotchas, and label/LaTeX guidance.
- Use `references/lhc-hist-ranges.md` for starting suggestions on histogram axis ranges and binning.
