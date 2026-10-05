---
name: engineer-figure
description: >-
  Engineering-focused publication figure workflow for Python or R. Use whenever the user asks to create, revise, audit, or polish manuscript figures, multi-panel scientific plots, engineering/deep-learning/modeling/simulation/control figures, creative mechanism/process/evidence figures, Chinese paper/report figures, or journal-ready SVG/PDF/TIFF outputs for Nature-family, Science, IEEE, Elsevier, Springer, or other high-impact engineering venues. Before plotting, define the figure's conclusion, evidence logic, visual concept, export needs, and review risks. If the user has not chosen Python or R, ask "Python or R?" and stop. Use only the selected backend for figure generation, previewing, exporting, and QA. Supports matplotlib/seaborn and ggplot2/patchwork/ComplexHeatmap. Not for dashboards or Illustrator/Figma-first infographics.
---

# Engineer Figure Skill

A guide for producing publication-quality scientific figures as a visual argument, not
as isolated pretty plots. Every figure starts from a claim, an evidence hierarchy, and a
review-risk check before code or aesthetics.

The Python/matplotlib rules in this skill remain valid. The skill now also supports
R, especially `ggplot2 + patchwork + ComplexHeatmap + ggrepel + svglite/cairo_pdf + ragg`.
If the user provides a private plotting template collection, use it only as an internal
adaptation source and do not reveal its path, filenames, or provenance in user-facing output.

Color policy: prefer **unified method families across all panels** over maximal hue separation.
For dense Nature Machine Intelligence-style figure pages, use the low-saturation `NMI pastel`
family described in `references/api.md` and reserve green/red mainly for gains, drops, and other directional cues.

## First move: figure contract before plotting

Before generating or editing code, establish the contract below.

**Backend selection is a blocking gate.** If the user has not explicitly chosen Python
or R in the current request or provided a clearly language-specific input file/workflow,
ask one concise question: **Python or R?** Then stop and wait for the user's answer.
Do not generate mock data, write scripts, create figures, or choose Python/R by default.
This overrides general autonomy/default-execution behavior for figure tasks.

**The selected backend is exclusive for all figure generation.** Once Python or R is
selected, every plotting script, preview image, SVG/PDF/TIFF/PNG export, QA render,
and visual workaround must be produced by that same backend. Do not use Python to
draw a preview for an R figure, and do not use R to draw a preview for a Python figure,
even if the selected runtime or packages are missing locally. The non-selected language
may only be used for non-visual file inspection or data conversion when it does not
open a graphics device, import plotting libraries, create image/vector files, or
change the final visual appearance.

**Missing runtime/package rule.** After the backend is selected, check the selected
runtime early (`Rscript`/R for R; Python and required plotting packages for Python).
If the selected runtime or required packages are unavailable, stop before rendering
and report the exact blocker. You may provide a selected-backend script and installation
commands, or ask permission to install dependencies, but you must not fall back to the
other language to make a substitute figure.

Only recommend a backend when the user explicitly asks you to choose or recommend one.
In that case, use `references/backend-selection.md`, state the reason, and then proceed
with the recommended backend.

1. Core conclusion: write the one-sentence claim the figure must defend.
2. Concept card: identify the reviewer question, visual job, evidence roles, and
   whether the figure should lead with mechanism/process rather than metrics. Use
   `references/figure-concept-card.md`.
3. Evidence chain: map each planned panel to the claim, and drop panels that do not carry
   a unique piece of evidence.
4. Innovation route: choose a defensible visual structure from
   `references/visual-innovation-atlas.md` before defaulting to bars, lines, or plain
   heatmaps. For engineering, deep learning, modeling, simulation, control, robotics,
   or interception-style figures, also load `references/engineering-reference-atlas.md`
   and choose the closest reference route. For manuscript-facing figures, consider at
   least a conservative option and a mechanism/process-led option.
5. Archetype: classify the figure as `quantitative grid`, `schematic-led composite`,
   `image plate + quant`, or `asymmetric mixed-modality figure`.
6. Visual direction: define the intended visual family, panel hierarchy, palette roles,
   legend strategy, density level, and the closest internal/reference pattern before
   writing plotting code. Use `references/visual-quality-loop.md`; for engineering or
   AI-control topics, name the closest engineering atlas ID.
7. Typography/layout contract: before rendering, lock the primary font, Chinese font
   fallback, font-size ladder, figure size, subplot gutters, legend reserve, and
   outer margins. Use `references/typography-layout-contract.md`, especially for
   Chinese manuscript/report figures or when prior drafts looked too small.
8. Backend: use the selected Python or R track exclusively for all figure drawing,
   previewing, exporting, and visual QA. Do not cross-render with the other language.
9. Journal/export contract: set final dimensions, editable text, source data, statistics,
   image-integrity notes, and export formats before styling.
10. Preview-and-iterate: after the first render, open or inspect the selected-backend
   preview at final aspect ratio and revise until spacing, hierarchy, labels, legends,
   colors, and typography pass the visual quality checklist. Do not treat a syntactically
   valid export as final.

The highest-priority rule is: **the chart serves the scientific logic**. Aesthetic polish,
template matching, and complex layout are subordinate to making the core conclusion clear,
defensible, and reviewable.

## User-facing privacy rule

Do not disclose private local paths, private filenames, chat-attachment names, internal
reference filenames, template identifiers, or the provenance of private working materials
in user-facing replies, generated code comments, figure legends, reports, or manuscript
text. Use generic descriptions such as "the provided R template collection", "a private
working draft", or "the internal figure contract". Only reveal an exact path or source
file when the user explicitly asks for that audit trail.

## Public release and asset rule

Treat bundled paper figures and template-derived images as reference materials, not as
automatically redistributable assets. Before publishing this skill or copying its assets
into a public repository, verify each source image's license from the article page or
replace the file with metadata links and a short description of the visual lesson.

## Python quick-start

**Python-only execution rule.** When the user has selected Python, do all figure
drawing, previewing, exporting, and visual QA in Python. Do not call R/ggplot2,
ComplexHeatmap, patchwork, or any R graphics device to create a temporary preview,
fallback export, or layout approximation. If Python or required Python plotting
packages are missing, stop before rendering and report the missing dependency. You
may still write the Python script, provide `pip`/environment install commands, or
ask permission to install dependencies, but do not cross-render the figure in R.

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "SimHei", "Arial", "DejaVu Sans", "sans-serif"],
    "axes.unicode_minus": False,
    "svg.fonttype": "none",     # editable text in SVG
    "pdf.fonttype": 42,         # editable TrueType text in PDF
    "font.size": 13,            # Chinese manuscript/report default; see typography-layout-contract.md
    "axes.labelsize": 15,
    "axes.titlesize": 17,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 13,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.95,
    "legend.frameon": False,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.tiff", dpi=dpi, bbox_inches="tight")
```

Use `text.usetex = True` only when LaTeX is installed and math-rich labels are required.

## R quick-start

```r
library(ggplot2)
library(patchwork)

theme_set(
  theme_classic(base_size = 13, base_family = "Microsoft YaHei") +
    theme(
      axis.line = element_line(linewidth = 0.45, colour = "black"),
      axis.ticks = element_line(linewidth = 0.45, colour = "black"),
      axis.title = element_text(size = 15),
      axis.text = element_text(size = 11),
      legend.title = element_text(size = 13),
      legend.text = element_text(size = 13),
      strip.text = element_text(size = 17, face = "bold"),
      plot.title = element_text(size = 17, face = "bold"),
      panel.grid = element_blank()
    )
)

save_pub_r <- function(plot, filename, width_mm = 183, height_mm = 120, dpi = 600,
                       base_family = "Microsoft YaHei") {
  w <- width_mm / 25.4
  h <- height_mm / 25.4
  svglite::svglite(paste0(filename, ".svg"), width = w, height = h)
  print(plot)
  dev.off()
  grDevices::cairo_pdf(paste0(filename, ".pdf"), width = w, height = h, family = base_family)
  print(plot)
  dev.off()
  ragg::agg_tiff(paste0(filename, ".tiff"), width = w, height = h, units = "in", res = dpi)
  print(plot)
  dev.off()
}
```

## Default operating stance

- Start by classifying the requested figure into one of four archetypes:
  `quantitative grid`, `schematic-led composite`, `image plate + quant`, or `asymmetric mixed-modality figure`.
- Do not default to a bar chart, line chart, or plain heatmap just because the input is
  numeric. First decide whether the figure's job is mechanism, process, decision logic,
  uncertainty, multi-agent interaction, spatial/trajectory evidence, or metric comparison.
- For engineering, deep learning, modeling, simulation, control, robotics, digital-twin,
  or interception-like requests, load `references/engineering-reference-atlas.md` before
  using the generic chart atlas. Use the chart atlas when metric comparison is truly
  the figure's main job.
- Prefer one **hero panel** plus subordinate evidence panels over filling the canvas with equal-sized subplots.
- If the user asks for a single chart, still identify its role in the manuscript claim:
  discovery, mechanism, validation, comparison, robustness, or engineering relevance.
- Keep the background white for plots and diagrams; switch to black only for raster or simulation image plates that require it.
- Prefer direct labels over legends when categories are spatially fixed or the legend would force unnecessary eye travel.
- Keep one restrained palette per figure: usually one neutral family, one signal family, and one accent family.
- Treat statistics, `n`, error-bar definitions, source-data traceability, and image-integrity notes as part of the figure,
  not as optional caption cleanup.
- For manuscript-facing figures with underspecified design, load
  `references/figure-concept-card.md` and `references/visual-innovation-atlas.md`.
  Use metrics as evidence, not automatically as the main visual story.
- For Chinese figures or figures intended for Word/PDF manuscript insertion, do not use tiny
  `Nature final-size` defaults as the first draft. Load `references/typography-layout-contract.md`
  and start from the readable Chinese ladder unless the user explicitly requests exact journal
  final-size assembly.
- For any figure that the user expects to look polished, load `references/visual-quality-loop.md`
  and run the visual brief + preview audit before final delivery.
- When the user references `nature-figure` or an older scientific-figure workflow,
  treat this skill as the engineering successor and use `references/engineering-reference-atlas.md`
  plus the generic chart atlas assets.

## When to load this skill

- Python or R figures for **papers, slides, or reports** targeting Nature, Science, IEEE, NeurIPS, ICLR, Elsevier, Springer, or similar engineering/AI venues.
- Requests involving **grouped bars, trend lines, heatmaps, radar plots, multi-panel grids**, or **PDF/SVG/high-DPI** output.
- Any mention of "engineering figure", "Nature style", "publication figure", "paper figure", "SCI figure", "scientific-figure-making", "R plotting template", or "high-quality scientific plot".
- Requests to improve a figure's logic, aesthetics, panel layout, figure legend, export quality, or journal-readiness.

## When NOT to load

- Plotly, Altair, Bokeh, or other interactive/web-first plotting.
- EDA-only plots without a publication target.
- Primary workflow is 3D, GIS, or non-scientific illustration tooling.
- Illustrator / Figma–first layout.

## Related files

| File | Open when |
|------|-----------|
| [references/figure-contract.md](references/figure-contract.md) | Need to convert a user request into core conclusion, evidence hierarchy, panel map, and review-risk checks |
| [references/figure-concept-card.md](references/figure-concept-card.md) | Need to design the figure's claim, reviewer question, evidence roles, and mechanism/process story before choosing chart types |
| [references/visual-innovation-atlas.md](references/visual-innovation-atlas.md) | Need non-traditional, mechanism/process/evidence-driven structures beyond bars, lines, and plain heatmaps |
| [references/engineering-reference-atlas.md](references/engineering-reference-atlas.md) | Engineering, deep learning, modeling, simulation, control, robotics, digital-twin, neural-operator, or inverse-design figures need high-quality reference structures |
| [references/visual-quality-loop.md](references/visual-quality-loop.md) | Need the figure to look polished, choose an aesthetic direction, or iterate after a disappointing render |
| [references/typography-layout-contract.md](references/typography-layout-contract.md) | Chinese text, font consistency, readable font sizes, whitespace, subplot spacing, legends, or clipping are relevant |
| [references/backend-selection.md](references/backend-selection.md) | User has not chosen Python/R, asks for a recommendation, or a mixed Python/R workflow is possible |
| [references/r-workflow.md](references/r-workflow.md) | User chooses R or provides R scripts/templates/data |
| [references/r-template-index.md](references/r-template-index.md) | Need to adapt a user-provided or private R template collection without exposing source paths |
| [references/qa-contract.md](references/qa-contract.md) | Before final delivery, revision package, raster/simulation image figure, or journal-specific audit |
| [references/design-theory.md](references/design-theory.md) | Typography, color theory, layout rationale, export policy |
| [references/api.md](references/api.md) | Python PALETTE, helper function signatures, validation rules |
| [references/common-patterns.md](references/common-patterns.md) | Python layout patterns: hero panels, legend-only axes, dark image plates, asymmetric layouts |
| [references/tutorials.md](references/tutorials.md) | End-to-end walkthroughs: bars, trends, heatmaps |
| [references/chart-types.md](references/chart-types.md) | Radar, 3D sphere, fill_between, scatter patterns |
