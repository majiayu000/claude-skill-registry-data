---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: data-graph-image
description: >
  Generate branded chart, graph, analytics, KPI, and data infographic images
  with Egaki and ChatGPT Image. Use when a user asks for a graph image,
  usage graphic, metric card, social data visualization, or branded chart.
---

# Branded data graph images

Turn verified data into a branded editorial graphic with Egaki and
`chatgpt-image-latest`. Preserve numerical accuracy and the repository's visual
identity.

## Load Egaki first

Always load the `egaki` skill before generating an image. Follow its current
README and CLI-help workflow. Always pass an explicit model:

```bash
-m chatgpt-image-latest
```

## Discover the design system

Read the design system before writing the image prompt.

1. Search the repository recursively for `design.md`. Read the nearest relevant
   file, then any root-level design guide.
2. Search for `docs.json`. For Holocron sites, read `colors`, `appearance`,
   `icons`, and `decorativeLines`.
3. Read the site's global CSS and the main hero, layout, and navigation
   components. Extract real colors, fonts, radii, border treatment, and shadows.
4. Locate logo, favicon, and wordmark files under `public/`, `assets/`, or paths
   declared in `docs.json`.
5. Prefer explicit design tokens from code over colors inferred from a
   screenshot.

If no design guide exists, report the inferred choices before generation. Do
not invent a brand system silently.

## Build a graph specification

Write a compact source of truth before prompting the model:

```text
Title: 17.73 billion tokens in 5 days
Range: Aug 22–26, 2026 UTC
Series:
  Aug 22: cache 2.98B, other 0.27B, total 3.25B
  Aug 23: cache 2.94B, other 0.38B, total 3.32B
Legend: Cache reads; Other token work
Source: production telemetry
```

Rules:

- Use verified source data. Never ask the image model to calculate values.
- Calculate totals and percentages before generation.
- Define whether dates are calendar periods or rolling windows.
- State units on every axis and value label.
- Preserve full-precision calculations separately from rounded display values.
- If rounded labels do not sum to the rounded headline, add a concise note or
  increase displayed precision.
- Limit a graphic to one main message. Split dense data into separate images.

## Choose the chart

Use the simplest chart that answers the question:

- Time series: vertical bars or a line chart.
- Composition: one horizontal stacked bar.
- Ranked categories: horizontal bars.
- One KPI with context: large number plus a small supporting chart.
- Process or architecture: a directional flow diagram, not a statistical chart.

Avoid 3D charts, decorative fake axes, unexplained colors, and donut charts with
many small categories.

## Pass references to Egaki

Pass layout references first and brand assets after them. Explain each input's
role in the prompt.

```bash
egaki image 'Use the first image only as a layout and hierarchy reference. Do
not copy it. Use the second image as the exact company logo and preserve its
shape. Create the graph from the exact specification below: ...' \
  -m chatgpt-image-latest \
  --input "$LAYOUT_REFERENCE" \
  --input "$LOGO_PATH" \
  --quality high \
  --json \
  -o "$OUTPUT_PATH"
```

Pass additional references with repeated `--input` flags. Use a website
screenshot only for composition or mood. Use the original logo file for the
logo itself.

For Egaki 0.10.0 with ChatGPT Image:

- Do not pass `--output-format`; it sends the wrong OpenAI parameter name.
- Do not pass `--aspect-ratio`; the provider ignores it. State landscape,
  portrait, and intended placement in the prompt instead.
- Default to `--quality high` for publishable graphics.

## Prompt template

```text
Use reference 1 only for editorial layout and information hierarchy. Make an
original composition. Use reference 2 as the exact logo. Preserve its geometry.

Create a premium landscape data graphic for [company].

Exact text:
- Brand: [brand]
- Eyebrow: [range and source]
- Headline: [main finding]
- Axis labels: [exact labels]
- Data labels: [exact values]
- Legend: [exact series names]

Chart geometry:
- [chart type]
- [axis minimum, maximum, and ticks]
- [bar or segment proportions]
- exactly [N] visual series and [N] legend colors

Design system:
- primary: [hex]
- background and text: [hex]
- series palette: [hex list]
- fonts: [families and weights]
- borders/radii/shadows: [rules]

Use crisp flat geometry, restrained decoration, generous spacing, and readable
typography. No fake data, extra labels, extra numbers, 3D, glass effects,
unexplained colors, or invented logos.
```

## Beat the staircase prior

The image model wants every bar chart to rise from left to right. It will draw a
clean staircase and ignore a dip, even when the labels are correct.

State the geometry as an explicit ranking, and name the single shortest and
tallest bar:

```text
Rank the seven bars shortest to tallest:
1st shortest = Aug 21 (2.36B). This is THE SHORTEST BAR IN THE ENTIRE CHART.
2nd shortest = Aug 20 (2.57B), taller than Aug 21, shorter than every other bar.
3rd = Aug 22. 4th = Aug 23. 5th = Aug 24. 6th = Aug 26.
Tallest = Aug 25 (4.11B), top stays BELOW the 4.5B gridline.
Left to right the tops go DOWN, then jump up, rise three times, then drop.
```

Percent-of-plot-height instructions alone do not work. The ranking does.

## Prefer regeneration over edit passes

An edit pass regenerates the whole image. Text drifts even when the prompt says
to preserve it: labels get duplicated, values shift by one position, and axis
ticks change. A geometry fix requested through an edit is unreliable.

- Fix chart geometry by **regenerating from the full prompt**, not by editing.
- Use an edit pass only for a single isolated text or color change.
- Change **one thing per edit pass**.
- After any edit, re-validate **every** label, not just the edited one. Keep the
  previous version until the edit is proven better.
- When an edit trades a correct data label for a correct axis tick, keep the
  version with correct data labels.

## Validate every result

Use image analysis after every generation. Ask it to:

1. Transcribe every visible word and number.
2. Compare all values with the graph specification.
3. **Measure** bar heights and segment widths against the gridlines and report
   the implied value for each. Never accept an eyeballed "looks right".
4. Rank the bars by visual height and compare that ranking to the data.
5. Check legend-entry count against distinct fill colors.
6. Check logo fidelity, text legibility, and unwanted extra content.
7. Report image dimensions and flag duplicated labels.

Do not publish a known inaccurate chart.

Common defects to reject:

- **A duplicated value label.** The model copies a neighbouring number.
- **An extra visual shade.** A second tint inside one series, or a translucent
  band across the plot area, reads as an undeclared third category.
- **A bar crossing its own axis maximum.**
- **A sub-1% segment** rendered as an invisible sliver. Merge tiny categories or
  move their labels outside the bar.

## Produce a coherent set

When the user asks for several images, default to three complementary views:

1. Trend over time.
2. Composition or category ranking.
3. One headline KPI with context.

Keep the same canvas orientation, logo placement, type hierarchy, background,
palette, axis treatment, and footer format across the set.

When working through Discord, upload final validated files with
`kimaki upload-to-discord`. Keep draft and rejected files out of the upload.
