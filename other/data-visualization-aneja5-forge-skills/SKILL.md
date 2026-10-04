---
name: data-visualization
description: Use when building dashboards, charts, or data displays, when defining chart type selection rules, when standardizing data color encoding, or when charts look inconsistent across the product.
---

# Data Visualization

## Overview

Pin down chart-type selection rules, data color encoding, axis conventions, responsive behavior, empty states, and load animations *before* charts proliferate. Output is `.forge/data-visualization.md`. Reads `design-system` (color palette, typography) and `component-library` (chart components). Referenced by every dashboard, report, and analytics surface.

## When to Use

- A dashboard or analytics surface is being built and no chart conventions exist
- Charts across the product use 8 different color palettes and 3 different tooltip styles
- A new chart type is being added and the team needs a rule for when to use it
- Data colors don't track design tokens (raw `#3B82F6` inside chart code)
- A report needs to work on mobile and the existing charts don't respond

## When NOT to Use

- A single one-off chart on a marketing page — use the design system colors and move on
- A product with no data surfaces (auth, settings, content)
- A backend-only service

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Just use whatever chart looks good" | Mismatched chart types across a dashboard look like three different products stitched together. |
| "We'll standardize later" | By then you have 8 charts with 8 different palettes and 3 tooltip styles. |
| "Pie charts are fine" | Humans can't accurately compare angles. Donuts with center metrics beat pies; horizontal bars beat both for comparison. |
| "We don't need empty states for charts" | A blank chart area makes users think the product is broken. |
| "Hover tooltips work everywhere" | Hover doesn't exist on touch. Every tooltip needs a tap path. |

## Red Flags

- Pie chart used for comparison (use horizontal bar)
- Color as the only differentiator (no patterns/labels/icons for accessibility)
- Y-axis not starting at 0 (misleading without a "delta" framing)
- Inconsistent date formats across charts (`MMM DD` here, `MM/DD/YY` there)
- Chart with no empty state — just a blank rectangle
- Tooltip that only works on hover (unusable on touch)
- More than 5 distinct colors in one chart

## Core Process

### Step 1: Read upstream artifacts

Read `.forge/design-system.md` for color palette + typography. Read `.forge/component-library.md` for the chart components catalog. If charts aren't yet catalogued, add them in `component-library` first.

### Step 2: Chart type selection — a decision tree, not a vibe

Document the rules. Charts are picked by data shape, not aesthetics.

| Data shape | Chart type |
|---|---|
| Trend over time | Line (or area if cumulative) |
| Part of whole | Donut with center metric (never pie) |
| Comparison across categories | Horizontal bar (labels remain readable) |
| Distribution | Histogram or box plot |
| Correlation | Scatter plot |
| Ranking | Sorted horizontal bar |
| Performance score | Gauge or radial progress |
| Multi-axis comparison | Radar (sparingly — humans struggle past 5 axes) |
| Geographic | Map (only when geography drives the insight) |
| Time-of-day / frequency matrix | Heatmap |

### Step 3: Data color encoding

Semantic, not decorative. All colors come from `design-system` tokens.

- **Performance / positive** → green gradient (`success` token family)
- **Risk / negative** → red gradient (`error` / `danger` token family)
- **Neutral / informational** → blue gradient (`primary` token family)
- **Comparison series** → max 5 distinct colors, ordered by semantic weight (most prominent series gets `accent`)
- **Sequential data** → single-hue gradient, dark to light
- **Accessibility floor:** never color-only. Add patterns (dashes, dots), labels, or icons so the encoding survives grayscale and color blindness.

### Step 4: Axis + label conventions

- Y-axis starts at 0 (exception: change/delta charts, which must be labeled as such)
- Labels inside the chart when space allows, outside when crowded
- Units always shown: `%`, `$`, `count`, `ms`
- Date format consistent product-wide (e.g., `MMM DD` for English locales)
- Truncate long category labels with ellipsis + tooltip; never wrap

### Step 5: Responsive chart behavior

| Breakpoint | Behavior |
|---|---|
| Desktop | Full chart with legend beside; tooltip on hover or tap |
| Tablet | Chart fills width; legend below |
| Mobile | Simplified chart (fewer data points or aggregated bins); legend as dropdown or hidden; tap-only tooltip |
| Touch | Tap toggles tooltip; tooltip dismisses on outside tap |

Never depend on hover. Every interaction has a tap path.

### Step 6: Empty states for charts

A chart with no data is **not** a blank area. Show:
- Headline: "No data yet" (per `brand-identity` voice)
- Context: *"Calls from this week will appear here"* or *"Import data to see trends"*
- Optional CTA: link to the source of data or to documentation

### Step 7: Animation on data load

- **Staggered reveal** per `references/motion-system.md` chart section — bars grow, lines draw, numbers count up
- **Duration:** emphasis-tier (400–500ms) on first load; standard (200–300ms) on update
- **Respect `prefers-reduced-motion`** — collapse to instant appearance, opacity fade only

### Step 8: Domain-specific patterns

If the product is data-heavy, document recurring chart patterns by domain:

- **Score distribution** — histogram with performance bands (red / yellow / green zones)
- **Trend lines** — 7-day moving average overlaid on daily points
- **Team comparison** — grouped bar, sorted by aggregate
- **Volume by time-of-day** — area chart + heatmap; aligns to the analytics narrative

If not data-heavy, skip — don't invent patterns to fill the section.

### Step 9: Write `.forge/data-visualization.md`

Section order: upstream-read confirmation, chart selection rules, color encoding, axis + labels, responsive behavior, empty states, animation, domain-specific patterns. Prepend a `forge:meta` header (`generated_by: data-visualization`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/design-system.md, .forge/component-library.md]` — paths only, never hashes, `generated_from: {.forge/design-system.md: <hash>, .forge/component-library.md: <hash>}` — each upstream's content_hash AT generation time, `content_hash: <sha256 first 8 of THIS file's body>`).

## Verification

- [ ] Chart selection has a rule for every chart type the product uses (no ad-hoc choices)
- [ ] Color encoding is consistent across the product and accessible (not color-only)
- [ ] Every chart type has an empty state with context, not a blank area
- [ ] No chart depends on hover — every tooltip has a tap path
- [ ] Animation respects `prefers-reduced-motion`
- [ ] Y-axis policy documented (starts at 0 except for delta/change charts, which must be labeled)
- [ ] No raw hex in chart code — every color is a `design-system` token
- [ ] Domain-specific patterns documented if the product is data-heavy (or skipped with reason)
- [ ] `.forge/data-visualization.md` written with `forge:meta` header
