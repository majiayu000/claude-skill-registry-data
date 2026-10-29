---
name: infographics
description: |
  Creates data-driven infographics and charts as accessible SVG. Use when visualizing data, choosing a chart type, generating an SVG chart or infographic, or reviewing a visualization for clarity and accuracy.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-infographics
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: documents
---

# Infographics

## Intro

A good chart starts from a single message, picks the most accurate
visual encoding for the data relationship, and strips everything that
does not support it. Generate standalone SVG with explicit `viewBox`,
semantic text, and accessible metadata so the result is editable,
responsive, and screen-reader friendly.

## Overview

### SVG generation principles

- Emit standalone SVG with `xmlns="http://www.w3.org/2000/svg"`.
- Set an explicit `viewBox` (e.g. `viewBox="0 0 800 600"`) for
  responsive scaling.
- Use `width="100%"` and `height="auto"` for flexible embedding.
- Group related elements with `<g>` and position via `transform`.
- Put reusable styles in `<defs>` and `<style>` blocks.
- Give elements semantic IDs and classes so the file stays editable.
- Keep text as `<text>` elements, not paths, for accessibility.

### Data-to-visual mapping

1. **Identify the message** — what should the viewer learn?
2. **Choose the encoding** — position, length, angle, area, color, or
   shape.
3. **Apply visual hierarchy** — the most important data gets the
   strongest visual treatment.
4. **Add context** — title, axis labels, legend, source attribution.
5. **Simplify** — remove anything that does not support the message.

Encoding effectiveness from most to least accurate for quantitative
data: position > length > angle > area > color saturation > shape.

### Chart type selection

| Data Relationship | Chart Type |
|---|---|
| Change over time | Line chart, area chart |
| Comparison of categories | Bar chart (horizontal for many categories) |
| Part-to-whole | Stacked bar, treemap (avoid pie charts for > 5 slices) |
| Distribution | Histogram, box plot, violin plot |
| Correlation | Scatter plot, bubble chart |
| Ranking | Horizontal bar chart, lollipop chart |
| Flow / process | Sankey diagram, flowchart |
| Geographic | Choropleth map, symbol map |
| Hierarchy | Treemap, sunburst |

### Visual design

- **Color palette:** 3-5 colors max, legible in grayscale.
- **Typography:** one sans-serif font, clear size hierarchy (title >
  subtitle > labels > annotations).
- **Whitespace:** generous margins and padding prevent clutter.
- **Grid lines:** light gray, thin, removed when unnecessary.
- **Data labels:** place directly on chart elements when space
  permits to reduce legend lookups.
- **Aspect ratio:** ~16:9 for presentations, ~4:3 for documents, ~1:1
  for social media.
- **Mobile first:** over 60% of content is consumed on mobile —
  prefer vertical layouts.
- **One focal point:** visuals with a clear focal point outperform
  complex ones by roughly 2x in retention.

### Accessibility

- 4.5:1 contrast for text, 3:1 for large text and UI elements.
- Never rely solely on color to convey information — add patterns,
  labels, or shapes.
- Include `<title>` and `<desc>` for screen readers.
- Use `role="img"` and `aria-label` on the SVG element.

### Alternative formats

When SVG is not the right fit, consider Mermaid for flowcharts and
sequence/Gantt diagrams embeddable in Markdown, ASCII art for
terminals and plain-text READMEs, or a CSV plus narrative when the
user just needs organized data with commentary.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Omitting the `viewBox` attribute.** An SVG without `viewBox` does not scale responsively — it renders at a fixed pixel size that overflows narrow containers and documentation embeds. Always emit `viewBox="0 0 W H"` with explicit dimensions and use `width="100%"` and `height="auto"`.
- **Positioning `<text>` elements without explicit coordinates and alignment attributes.** SVG text without `x`, `y`, `text-anchor`, and `dominant-baseline` renders at the origin or at browser-specific defaults. Lay out every text element explicitly with all four positioning attributes.
- **Encoding data in color alone.** Roughly 8% of men have red-green color vision deficiency. A chart that differentiates categories only by color is inaccessible. Always pair color with a second encoding: pattern, label, shape, or position.
- **Choosing a pie chart for more than 5 slices.** The human eye is poor at comparing angles; with many slices, most segments become indistinguishable. Prefer a horizontal bar chart, which exposes differences via length — the most accurate quantitative encoding.
- **Omitting `<title>` and `<desc>` elements.** Screen readers have no way to announce the chart's content without these elements. Include a `<title>` stating the chart's finding (not just its topic) and a `<desc>` summarizing the key data.
- **Starting a bar chart's y-axis at a non-zero value.** Truncating the axis to exaggerate small differences distorts the viewer's perception of magnitude. For bar charts, the y-axis baseline must be zero.
- **Hardcoding `width` and `height` pixel attributes on the root SVG element.** A chart with fixed pixel dimensions overflows its container on mobile and cannot be embedded responsively. Use `width="100%"` and `height="auto"` and let `viewBox` drive the aspect ratio.

## Full reference

### Tufte's core rules

1. **Show the data** — maximize the data-ink ratio (data-ink / total
   ink).
2. **Avoid chartjunk** — decorative elements that do not convey
   information.
3. **Use small multiples** — repeat a chart design across subsets for
   comparison.
4. **Integrate text and graphics** — labels belong on the chart, not
   in a distant legend.

### Cleveland & McGill encoding ranking

Perceptual accuracy, most to least accurate for quantitative data:

1. Position along a common scale
2. Position along non-aligned scales
3. Length
4. Angle / slope
5. Area
6. Volume / curvature
7. Color saturation / shading
8. Color hue

Always pick the highest-ranked encoding that fits the relationship.

### Color palettes

- **Sequential** (low to high): single hue, varying lightness (e.g.
  `#f7fbff` to `#08306b`). Good for heatmaps, choropleths, and
  continuous data.
- **Diverging** (negative to positive with neutral center): two hues
  with light center (red-white-blue, brown-white-teal). Good for
  deviation from a baseline.
- **Categorical**: maximally distinct hues at similar lightness.
  Limit to 5-7 colors. A safe set: `#4e79a7` `#f28e2b` `#e15759`
  `#76b7b2` `#59a14f` `#edc948` `#b07aa1`.
- **Colorblind safety** (~8% of men): avoid red-green as the only
  cue. Test with deuteranopia and protanopia simulators. Safe pairs:
  blue/orange, blue/red, purple/green.

### Typography scale

| Element | Size (relative) | Weight | Case |
|---|---|---|---|
| Title | 1.5x base | Bold | Sentence |
| Subtitle | 1.2x base | Regular | Sentence |
| Axis labels | 1x base | Medium | Sentence |
| Tick labels | 0.85x base | Regular | As-is |
| Annotations | 0.85x base | Regular | Sentence |
| Source note | 0.7x base | Regular | Sentence |

### SVG layout template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500"
     role="img" aria-label="Chart description">
  <title>Chart Title</title>
  <desc>Detailed description for screen readers</desc>

  <style>
    .title { font: bold 24px sans-serif; fill: #1a1a1a; }
    .subtitle { font: 16px sans-serif; fill: #666; }
    .axis-label { font: 14px sans-serif; fill: #333; }
    .tick-label { font: 12px sans-serif; fill: #666; }
    .grid-line { stroke: #e0e0e0; stroke-width: 1; }
    .data-label { font: 12px sans-serif; fill: #333; }
    .source { font: 10px sans-serif; fill: #999; }
  </style>

  <!-- Margin convention: top=50, right=30, bottom=60, left=80 -->
  <g transform="translate(80, 50)">
    <!-- Chart content here -->
    <!-- Plot area: 690 x 390 -->
  </g>

  <text x="80" y="30" class="title">Chart Title</text>
  <text x="80" y="48" class="subtitle">Supporting context</text>
  <text x="80" y="490" class="source">Source: Data source</text>
</svg>
```

Consistent margins for an 800x500 canvas: top 50 (title and
subtitle), right 30 (breathing room), bottom 60 (x-axis label plus
tick labels), left 80 (y-axis label plus tick labels).

### Chart-specific guidelines

- **Bar charts:** gap between bars 40-50% of bar width. Sort by value
  descending unless order is meaningful. Horizontal bars for long
  category labels. Always start the y-axis at zero.
- **Line charts:** cap at 5-7 lines before it gets cluttered. Label
  lines directly when possible. Add dots at data points for fewer
  than 15 points. Consider area fills for 1-2 series.
- **Scatter plots:** use 0.3-0.7 opacity when points overlap. Size by
  area, not radius. Add a trend line only when the correlation is
  meaningful. Label outliers directly.
- **Tables (when better than charts):** use when precise values
  matter more than patterns. Right-align numbers, left-align text.
  Subtle row striping for readability. Highlight key values with
  bold or color.

### Common pitfalls

- **Truncated y-axis:** non-zero start exaggerates differences.
- **3D effects:** distort value perception — always 2D.
- **Pie charts:** hard to compare — bar charts are more precise.
- **Dual y-axes:** confusing — use small multiples instead.
- **Excessive decoration:** chartjunk distracts from data.
- **Poor contrast:** light colors on white backgrounds.
- **Missing units:** always label what the numbers mean.
- **Rainbow colormaps:** perceptually non-uniform — use sequential
  or diverging palettes.

### Responsive considerations

Use `viewBox` without fixed width and height for fluid scaling. Test
readability at 50% and 200% zoom. Keep minimum effective text size
around 10px. On mobile, stack small multiples vertically and prefer
horizontal bars.

### References

- `references/best-practices.md` — Tufte, Cleveland & McGill, color
  palettes, SVG template, and chart-specific guidelines source.
