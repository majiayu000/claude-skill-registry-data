---
name: academic-figure-generation
description: Plan, design, and produce publication-quality figures for academic journal papers (GIScience, GeoAI, remote sensing, and similar venues such as IJGIS, ISPRS, RSE, TGIS). Covers deciding which figures a paper needs and which content belongs in a table instead, choosing the chart form from the variable types, scripted matplotlib plots with value guards, study-area maps (including HTML maps screenshotted for the paper), prompts for schematic diagrams, captions, file naming, and in-text citation of every figure. Use when the user asks to make, redesign, critique, or renumber a paper figure, plot results for a manuscript, build a study-area map, write figure captions, or pick colors or a chart type for a paper.
---

# Academic Figure Generation

Produce figures that add information to the paper, read at print size, and cannot drift from the reported numbers. Every figure is either **scripted** (code + data → image) or **schematic** (drawn by hand, in draw.io, or from an image-model prompt). Never invent data, coordinates, labels, or module names; when evidence is missing, write a stub script that raises `NotImplementedError` and say what is needed.

## Reference files

| File | Read it when |
|---|---|
| [references/figure-requirements.md](references/figure-requirements.md) | Every figure, before finalizing. Mandatory house standard (fonts, text, panels, output, captions, guards) |
| [references/chart-design.md](references/chart-design.md) | Choosing what to plot and how: table-or-figure, variable type → axis and mark, aggregation, scales, labels. Read before writing any plot code |
| [references/color-palettes.md](references/color-palettes.md) | Picking colors (green–blue house palette by default) |
| [references/maps.md](references/maps.md) | Any study-area or result map, including HTML maps for screenshots |
| [references/diagram-prompt-template.md](references/diagram-prompt-template.md) | A schematic (architecture, workflow, conceptual) produced from an image-model prompt |
| [assets/figstyle.py](assets/figstyle.py) | Starting a paper's figure scripts: copy it into the paper's figures folder as the shared style module |

## Workflow

1. **Inventory.** List the paper's existing figures and tables, with their captions and where the text cites them. Read the results the figure draws on. Find the paper's figures folder and any existing style module before writing new code.
2. **Decide what earns a figure** (chart-design.md, "Table or figure"). A figure must show something the tables do not: a trend across a factor, a distribution, a spatial pattern, a structure. When a proposed figure restates a table, say so and propose an alternative or drop it.
3. **Design before coding.** For each figure, write down the message in one sentence, the variable type of every axis, the mark, the aggregation, the scale, and the exact tick and axis labels in the paper's own terms. Check them against chart-design.md. For a non-trivial redesign, show the user the plan (or a quick draft) before polishing.
4. **Script it.** One script per figure in the paper's figures folder (`figN_<slug>.py`), importing the shared style module. Read data by explicit path. Add value-guard asserts for every number the text reports from this figure. Save as `figureN.png` (300 dpi); add PDF only when the venue or user wants vector.
5. **Render and look.** Open the PNG and inspect it: clipped or overlapping labels, legend covering data or place names, unreadable ticks, panels of unequal visual weight, and colors that collapse in grayscale. Fix and re-render until clean. Report residual issues plainly.
6. **Wire into the paper.** Caption of one brief sentence (about 25 words at most, main elements only, details left to the text and legend, country kept in place names, no colon); cite every figure (and panel letters, matching their case) in the text; renumber and rename files together when the order changes; delete superseded figure files and scripts. If a guard fails, find out whether the text or the data is wrong and tell the user before changing either.

## Decision rules

| Situation | Action |
|---|---|
| Figure would repeat a table | Drop it, or plot what the table cannot show (scaling, spread, per-unit cost) |
| x is a small set of levels (sizes, conditions, models), even if numeric | Categorical axis with equal spacing and labelled levels; bars or points, no continuous axis |
| Several models or runs share one trend | One panel with the mean and a min–max (or CI) whisker, instead of one panel per model |
| Values span orders of magnitude | Log axis, stated in the axis label |
| Reference or baseline series beside measured ones | Grey or neutral fill with hatching; measured series in palette colors |
| Value guard fails | Stop; compare script, data, and text; report; fix the wrong one with the user's agreement |
| User supplies a screenshot or drawn figure | Use it as is; only name it `figureN.png` and cite it |
| Study-area map wanted quickly | Build a self-contained HTML map in the project's UI style and let the user screenshot it (maps.md) |
| Conceptual or system diagram | draw.io (draw-io skill) or an image-model prompt from the template; never a matplotlib imitation |
| Data missing | Stub script plus a short spec; no plausible-looking placeholders |
