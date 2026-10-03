---
name: figure-creation
description: Design and build publication figures for ML venues using the design decisions and the mechanical export steps that accepted NeurIPS, ICML, and ICLR papers follow. Use when a paper needs a new figure, when a system diagram is authored in Figma, when a data plot is built in matplotlib, or when an existing figure must be audited for column width, font size, vector output, and color accessibility before submission. Applies the one-job rule, the form heuristic, the two authoring tracks, the never-smaller-than-the-caption rule, redundant encoding, and the pre-submission checklist.
---

# Figures (master method)

Follow `figure-guide.md` in this folder, the complete plain-English method.
This file is the operating summary.
## Process

1. **Name the one job in a sentence.** Write the claim the figure discharges
   before drawing anything: "rejecting low-confidence items raises bin purity."
   A figure with no nameable claim is decoration; delete it or turn it into a
   sentence. One figure, one job; a second claim earns a second panel.
2. **Pick the form from the question.** Comparison takes bars or dots sorted by
   value. Distribution takes a histogram or ECDF. Relationship takes a scatter,
   or a line when x is ordered. Composition takes a stacked bar with a
   meaningful total. Flow and architecture take a diagram. Under about twenty
   numbers that readers will quote, a table wins.
3. **Size the canvas to the column before drawing.** NeurIPS and ICLR give a
   5.5 in wide text block; ICML gives two 3.25 in columns inside a 6.75 in
   block. Build at that exact width so `\includegraphics` scales by 1.0. Every
   rescale multiplies the type size by the same factor.
4. **Diagram track, author in Figma.** One frame per figure, width in pixels set
   to inches times 72 (5.5 in is 396 px, 3.25 in is 234 px). Snap to an 8 px
   grid, make repeated blocks components, use auto layout for padding, and bind
   color and text styles so the figure family stays consistent. Name every
   layer, and export PDF at 1x.
5. **Plot track, author in matplotlib.** Set `figure.figsize` to the column
   width in inches and `pdf.fonttype` to 42 (the default 3 is rejected by some
   venues). Match the paper's serif family, keep line widths at or above 0.5 pt,
   drop the top and right spines, and save to PDF.
6. **Set type at final printed size.** Figure text is never smaller than the
   caption text, which is 9 pt at ICML. Labels carry data only: axis quantity,
   unit, category name. Model names, hedges, and qualifiers belong in the
   caption, not on the canvas.
7. **Encode every series twice.** Color plus line style plus marker, drawn from
   the Okabe-Ito set, so the reading survives grayscale printing and color
   vision deficiency. Convert the figure to gray and read it before shipping.
8. **Export vector, then verify the file.** `pdfinfo` must report the page size
   you designed (3.25 in reads as 234 pts). `pdffonts` must show every font
   embedded and no Type 3. Raster only for photographs and pixel grids, at 300
   dpi or better.
9. **Place it and hand off the caption.** Include at `\columnwidth` or
   `\linewidth` with no scale factor, put the figure at the top of a page or
   column, then write the caption with the `caption-writing` skill. The figure
   and its caption ship as one exhibit.
10. **Run the mechanical checklist.** Vector, fonts embedded, no rescale, axis
    labels with units, legend not repeating the caption, every mark decoded
    somewhere, grayscale legible, axes not truncated without a stated reason.
## Core rules

- One figure discharges one claim. Name the claim first, in words, then draw.
- Build at the final printed width. A figure that gets rescaled has the wrong
  font size by definition.
- Figure text is never smaller than the caption text (ICML accessibility rule);
  if 9 pt labels collide, remove content or widen the figure, never shrink type.
- Figure text carries data only: quantities, units, category names. No model
  names, no qualifiers, no claims on the canvas.
- Color never carries information alone. Every series gets a line style and a
  marker too, and the figure survives a grayscale conversion.
- Reject jet and rainbow colormaps: they impose gradients the data lacks.
  Sequential data takes viridis, diverging data takes a two-hue map, categorical
  data takes Okabe-Ito.
- Vector for anything drawn (PDF), raster only for photographs and pixel grids.
- Do not trust plotting defaults: matplotlib ships a 6.4 by 4.8 in canvas and
  Type 3 fonts, both wrong for a paper.
- Every axis states its quantity and unit. Every mark on the canvas is decoded
  in the legend or the caption, exactly once, never in both.
- Truncated axes, pie charts, and 3D effects on 2D data mislead. Show the full
  range or state the truncation in the caption.
- Prose axioms for all figure and caption text: sentences <= ~28 words, zero
  "can"/"could", no bare This/These, no em dashes, numbers glued to objects.
## Reference file

- `figure-guide.md`: full guide: term translations, the one-job rule, the form
  heuristic and the table-versus-plot test, the Figma diagram track (frame
  sizing, 8 px grid, components, styles, alignment discipline, export traps),
  the matplotlib plot track with a publication rcParams block, typography and
  size, the color system, the pre-submission mechanical checklist, a worked
  example from claim to shipped PDF on a toy system, and the handoff to
  `caption-writing`. Every venue number is attributed to its source with a URL.
