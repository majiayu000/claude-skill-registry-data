---
name: matplotlib-seaborn-to-matlab
description: Recreate, redesign, or optimize quantitative and academic figures as fully independent MATLAB scripts while using the live official Matplotlib Gallery and Seaborn Gallery as visual references. Use when the user asks for MATLAB plotting or MATLAB绘图, a Matplotlib/Seaborn-inspired style, publication-quality Chinese figures, redraws of existing charts, or one-figure-one-script FIG/PNG/PDF deliverables.
---

# Matplotlib/Seaborn to MATLAB

Create reproducible MATLAB figures that borrow visual language from official Matplotlib and Seaborn examples without copying their data or requiring Python at runtime.

## Apply precedence

Resolve every design decision in this order:

1. Follow the user's current instructions and annotated screenshot.
2. Follow the active workspace `AGENTS.md`.
3. Follow the selected official Gallery example.
4. Use this skill's defaults.

Never let a Gallery convention override an explicit user request. For example, if the user asks to retain one reference line and remove all background grids, keep that reference line and set both axes grids off.

## Execute the workflow

1. Read the active `AGENTS.md` completely. Inspect the source data, existing figure, MATLAB script, model outputs, and user-provided visual reference before editing.
2. Identify the chart's evidence structure: categorical comparison, ordered ranking, trend, distribution, relationship, matrix, or multi-panel composition.
3. Browse the live official Matplotlib and Seaborn sites. Select one to three structurally similar examples, open the actual pages, and record their URLs and access date. Read [gallery-routing.md](references/gallery-routing.md) for official entry points and selection guidance.
4. Extract only visual decisions: palette, layout, axes, grid, legend, labels, markers, annotations, and color mapping. Do not copy example data, English labels, or claims.
5. Translate the selected design to MATLAB using [matlab-style-mapping.md](references/matlab-style-mapping.md). Preserve all source values, equations, units, category order, and feasibility conditions.
6. Produce one completely independent plain `.m` script per figure. Each script must resolve paths from `mfilename('fullpath')`, read its own inputs, contain its own styling, create its own output directory, and call no shared plotting script or helper.
7. Keep the final figure open for manual editing. Save an editable FIG, a 300 DPI PNG, and a vector PDF with stable, non-conflicting names. Use Chinese text unless the user explicitly requests English.
8. Run every script separately in MATLAB. Inspect the PNG and a rendered PDF. Apply the complete [quality-checklist.md](references/quality-checklist.md) before claiming completion.

## Use visual defaults

- Use the Matplotlib default color cycle or Seaborn colorblind palette for categorical charts.
- Use perceptually uniform maps such as `viridis` for ordered continuous heatmaps.
- Use `jet` only when the user requires it, an existing paper must remain consistent, or it materially improves interpretation; explain any deliberate departure from an active workspace default.
- Use Microsoft YaHei on Windows with SimHei or Noto Sans CJK as fallback candidates.
- Prefer white figure backgrounds, clear hierarchy, outward ticks, and restrained decoration. Treat grids as optional evidence aids, not mandatory styling.
- Use title sizes near 18 and main labels near 16 when consistent with the workspace and page layout.

## Validate the script

Run the bundled checker before MATLAB execution:

```powershell
python <skill-directory>\scripts\check_matlab_plot_script.py path\to\figure.m
```

The checker verifies portable paths, Chinese-font configuration, script independence, FIG/PNG/PDF outputs, 300 DPI PNG, and vector PDF settings. It cannot verify aesthetics, data truth, or whether a user's screenshot was interpreted correctly; complete those checks visually and against the source data.

## Report the delivery

State:

- each independent MATLAB script path;
- each input data source;
- official reference URLs and adopted visual features;
- FIG, PNG, and PDF output paths;
- MATLAB execution and visual-inspection status;
- PDF font-embedding status;
- any unverified or blocked item.

## Handle failures honestly

- If browsing is unavailable, do not claim real-time reference. Use the saved mappings only when permitted and label the result as a fallback.
- If MATLAB, required data, or a usable Chinese font is unavailable, do not present unexecuted output as verified.
- If Ghostscript or another font checker is unavailable, deliver the vector PDF only with `font embedding unverified` stated explicitly.
- Do not fabricate data, runtime results, reference pages, visual inspections, or font checks.
