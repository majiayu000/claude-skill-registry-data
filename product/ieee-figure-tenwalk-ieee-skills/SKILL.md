---
name: ieee-figure
description: >-
  Produce publication-grade result figures for IEEE communications papers (JSAC, TWC, TC/TCOM,
  WCL, CL) — correct column widths, embedded fonts, vector output (PDF/EPS), grayscale- and
  colorblind-safe palettes, readable fonts, and the comms-standard plot types: BER/outage vs SNR
  on a log y-axis, achievable/sum rate vs SNR or antennas, convergence curves, CDFs, the
  analysis-line + simulation-marker overlay, learning curves (NMSE vs SNR, training/validation
  loss), and ISAC plots (rate–CRB tradeoff, beampattern, ROC). Use whenever the user wants to
  make or fix a figure for a comms paper: "make a result plot", "BER curve", "误码率曲线", "中断概率图",
  "和速率曲线", "收敛曲线", "仿真图", "NMSE曲线", "训练损失曲线", "CRB折中图", "波束方向图", "IEEE figure", "single/double
  column figure", "图太小看不清". For deciding which metrics to plot, use ieee-experiments; for
  captions-as-argument, see ieee-writing.
---

# IEEE Publication Figures

Use this skill to generate or repair figures that will survive IEEE production: vector, correctly
sized for the column, with embedded fonts and readable text at print size.

## Core stance

- **Size to the column from the start.** Single-column ≈ 3.5 in (88.9 mm) wide; double-column ≈
  7.16 in (181.6 mm). Design at final size so fonts end up readable — never shrink a big figure.
- **Vector first.** Output PDF or EPS for line/vector art; embed fonts. Use high-res raster only
  for photographic content (≥ 300 dpi color/grayscale, ≥ 600 dpi for line art / combinations).
- **Readable and grayscale-safe.** Minimum ~8 pt text at final size; distinguish series by
  marker/linestyle/hatch as well as colour so the figure survives B/W printing; use a
  colorblind-safe palette.
- **Comms axis conventions.** Error/outage curves use a log y-axis (`semilogy`); keep the SNR
  range wide enough to show the high-SNR slope (diversity order); define the SNR axis (transmit
  vs receive). Plot a derived expression as a line and its Monte-Carlo check as markers.
- **One panel, one question.** No two panels answer the same thing. The figure must be legible
  and self-explanatory with its caption.
- **No fabricated data.** Plot only the user's real numbers; if data is missing, ask or stub with
  a clearly labelled placeholder.

## When to open extra files

| File | Open when |
|---|---|
| [references/ieee-figure-spec.md](references/ieee-figure-spec.md) | Sizing, resolution, fonts, colour/grayscale, file format, multi-panel layout, caption rules, submission checklist |
| [references/matplotlib-patterns.md](references/matplotlib-patterns.md) | Concrete matplotlib setup (rcParams for embedded fonts, sizing, palettes) and ready patterns for BER/outage-vs-SNR (semilog), rate vs SNR/antennas, analysis-vs-simulation overlay, convergence, CDF, NMSE-vs-SNR, training/validation loss, and ISAC plots (rate–CRB tradeoff, beampattern, ROC) |

## Workflow

1. **Target column:** ask single- or double-column; set the width accordingly.
2. **Pick the chart type** that matches the result (see matplotlib-patterns.md): BER/outage vs SNR
   (semilog y) for reliability, line vs SNR/antennas for rate/efficiency, analysis-line +
   simulation-marker overlay to validate a derivation, objective-vs-iteration for convergence, CDF
   for distributions.
3. **Set the rendering rcParams first** (embedded fonts, sans-serif, sizes) — before any plotting.
4. **Plot the real data;** encode each scheme redundantly (colour + marker/linestyle). Use
   `semilogy` for error/outage; floor the y-axis at the lowest reliably simulated value.
5. **Label fully:** axis titles with units (dB, bps/Hz), defined SNR axis, legend; text ≥ 8 pt.
6. **Export** `.pdf` (or `.eps`) as primary and a 300–600 dpi `.png` preview.
7. **Grayscale check:** convert to gray and confirm series are still distinguishable.
8. **Return** the script, the output paths, and a one-line caption draft.

## Output format

1. `Script:` a self-contained, runnable plotting script (matplotlib) using the user's data.
2. `Outputs:` the vector file path + a PNG preview path.
3. `Caption:` a one-sentence draft stating what the figure shows (the question it answers).
4. `Checks:` confirmation of size, font embedding, and grayscale legibility.
