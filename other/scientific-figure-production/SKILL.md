---
name: scientific-figure-production
description: "Use when producing a figure for a paper, preprint, slide, poster, email report or web page: final size and resolution, format choice (SVG/PDF vs PNG), fonts legible at final size, multi-panel consistency, showing raw points for small samples instead of bar-of-means, self-contained captions, export provenance and reproducible re-rendering. Also use when checking an exported file before it is sent."
license: CC-BY-4.0
---

# Producing a figure that survives publication

A figure is judged at its final size, in its final medium, by someone who has
not seen your notebook. Design for that and check the exported file, not the
preview.

## Rules

1. **Decide medium and size first.** Email (raster, ~600–800 px wide body),
   slide (16:9, read from distance), journal column (one or two columns; the
   journal's own guide is authoritative and changes: check it live), web
   (responsive, vector). Render at that size; do not scale afterwards.
2. **Text legible at final size.** Axis and tick labels must be readable in
   the printed or emailed figure, not only on your monitor. If you need to
   zoom to read it, so will the reader.
3. **Vector for line art, raster for email.** SVG/PDF for print and web;
   PNG for email clients (no SVG support in many). Never upscale a raster to
   fake resolution.
4. **Show the data when n is small.** For fewer than about 15–20 points per
   group, plot every point (dot/strip plot) with the summary on top. A bar of
   the mean hides the distribution: very different datasets give identical
   bars.
5. **Panels are consistent.** Same axis limits for compared panels, same
   colour for the same entity across panels and across figures in one report,
   same units, panels labelled (A, B, …) and referenced in the caption.
6. **Caption is self-contained.** What is plotted, n and unit of replication,
   what intervals mean, data source and date, any transformation (log,
   smoothing, normalisation, exclusions). A reader of the figure alone can
   interpret it.
7. **Do not trust defaults.** Default tick density, colours, legend placement
   and line widths are someone else's compromise. Check each against the
   message.
8. **Grayscale and colour-vision check.** Series stay distinguishable in
   grayscale and under common colour-vision deficiencies (line style, marker,
   direct label). See `color-and-accessibility`.
9. **Reproducible from a record.** Keep the spec, data snapshot hash, code
   version and render settings next to the output so the exact figure can be
   regenerated and audited. A figure that cannot be regenerated cannot be
   corrected.
10. **Inspect the exported file.** Open the PNG/SVG/PDF that will be sent:
    clipping, overlapping labels, legend covering data, missing series,
    unreadable ticks, wrong aspect ratio.

## ieeVisualizer support

| Need | API |
|---|---|
| Final size | `RenderRequest(width=, height=, units="in" or "px", dpi=)`; a PNG measures exactly `request.size_px` |
| Formats | `png`, `svg`, `pdf` from the matplotlib adapter |
| Themes | a registered theme name or `name@version` (`RenderRequest(theme=)` or `spec.theme`); `themes.list_themes()` lists them, built-ins include `default`, `minimal`, `presentation` |
| Determinism | same spec + library versions → byte-identical SVG and PDF |
| Provenance | `ieeVisualizer.artifacts.export(spec, ["png", "svg"], writer)` writes figure files, canonical `spec.json`, `manifest.json` (spec hash, dataset hashes, provenance, library versions, warnings) |
| Inspection | `build_figure(spec)` returns the Matplotlib figure and per-layer artists without exporting; read `RenderResult.warnings` |
| Legend placement | `legend.position = "auto"` moves the legend outside when it would cover data |

Limits today: one plot per FigureSpec (render panels separately with equal
`axes.*.limits`); SVG text is drawn as paths (`svg.fonttype="path"`), so text
in the SVG is not editable or searchable; there is no subtitle field, so use
the `caption` for measure, unit and period.

## Good / bad

Bad: bar chart of mean task completion time for 4 participants per
condition, ± unlabelled bars, exported at 300 px and scaled to a slide.
Good: dot plot of all 8 times, mean marked, caption "n = 4 per condition;
line = mean", rendered at slide size with the `presentation` theme.

Bad: email report embeds an SVG and a 2,400 px PNG with 6 pt ticks.
Good: 1,200 × 750 px PNG at `dpi=150` (rendered at 8 × 5 in), tick labels
checked readable at 600 px display width.

## Checklist

- [ ] Medium and final size chosen before rendering; rendered at that size.
- [ ] Text readable at final size (checked on the exported file).
- [ ] Format fits the medium (PNG for email, vector for print/web).
- [ ] Small-n groups show every point.
- [ ] Compared panels share limits, colours and units.
- [ ] Caption states n, interval meaning, source, date and transforms.
- [ ] Spec, data hash and render settings stored with the output (manifest).
- [ ] Exported file opened and inspected for clipping, overlap and missing series.

Adapted in part from ieeVisualizer's own docs (MIT), K-Dense
`scientific-visualization` (MIT), Rougier et al. 2014 (CC0) and Weissgerber et
al. 2015 (CC BY 4.0); changed: rewritten and condensed, ieeVisualizer mapping
added. Sources and licences: `SOURCES.md`.
