---
name: responsive-layout
description: "Use when writing or reviewing layout CSS, a component's responsive behaviour, or a screen that must work from phone to wide desktop: breakpoints, fluid sizing, viewport units, overflow, wide tables, stacked fixed bars, hover and pointer input, mobile keyboard, and how the stylesheet itself is organised (specificity, layers, naming, themes, print)."
paths: "**/*.css, **/*.scss, **/*.vue, **/*.tsx, **/*.jsx"
---

# responsive-layout

Step 6 of the pipeline (`WORKFLOW.md`), next to `skills/accessibility` (reflow and zoom in `skills/accessibility` §3, target size
and focus in `skills/accessibility` §1) and `skills/webperf` (layout shift, image weight). This block owns the geometry: where a
layout breaks and what it does instead. It is written against CSS and the web platform, not against a framework or a tool. It states no pixel thresholds; a figure here would be a recalled
number (`skills/source-freshness`), so sizes come from the design system's tokens or the cited standard.

## When
A stylesheet, a layout component or a template with columns, bars, grids or fixed sizes is written or
changed, and when a page is reported as broken "on my phone" or "on a small laptop".

## Steps

**Read the file whose trigger the task meets.** The steps are numbered across files so a citation such as
"step 11" still resolves.

| Steps | Covers | Read it when | File |
|---|---|---|---|
| 1-12 | Breakpoints, continuous states, small-end design, dynamic viewport, grids, overflow, fixed widths, navigation, fixed bars, mobile keyboard, sweeping, text growth | any layout change | [`01-layout-steps.md`](./references/01-layout-steps.md) |
| 13-19 | `100vw`, hover and pointer capability, wide tables, stacked sticky layers, one-line controls, line length, short landscape viewports | full-bleed sections, hover or pointer behaviour, a wide table, several fixed bars, or long prose | [`02-input-tables-bars.md`](./references/02-input-tables-bars.md) |
| 20-29 | Specificity, cascade layers, naming, container queries, themes, print, reflow test, field font size, logical properties, units | a stylesheet grows, third-party CSS comes in, a theme or a print view is added | [`03-css-architecture.md`](./references/03-css-architecture.md) |

## Output / checkpoint
No pipeline checkpoint. What it owes: no horizontal page scroll across a swept width range, no content
cut by `overflow: hidden`, fixed bars that do not hide content, and a stated behaviour for the middle
range.

## Guardrails
- **Never introduce a breakpoint without the content failure that justifies it.**
- **Never hide an overflow bug with `overflow: hidden`**; fix the wide child.
- **Never copy a pixel threshold from memory**: tokens or the cited standard (`skills/source-freshness`).
- Never disable zoom (`user-scalable=no`, `maximum-scale`) to stop a layout from breaking.
- Never size a child with `100vw` to reach the edges, and never gate a capability on a device guess.

## Origin
Provenance is in [`references/origin.md`](./references/origin.md).
