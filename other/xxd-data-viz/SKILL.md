---
name: xxd-data-viz
description: Create chart and data visualization palettes from Chinese traditional colors. Use when a user needs categorical, sequential, diverging, highlight, dashboard, map, ECharts, D3, Chart.js, or colorblind-aware data palettes with Chinese traditional color identity.
---

# xxd-data-viz

## Purpose

Use this skill when colors must encode data. It should not turn a poster palette into a chart palette; it must choose colors by data meaning, distinguishability, ordering, and accessibility.

## Pain Points This Solves

- Attractive palettes fail charts because categories are not distinct or values are not ordered by lightness.
- Designers mix categorical, sequential, and diverging color logic in one chart.
- Chart color often relies on hue alone, which weakens accessibility and makes legends harder to read.

## Data Contract

- This public package is self-contained in `SKILL.md`; no external color-table files are required.
- Use the proven palettes and color-selection rules documented below as the authoritative contract.
- Do not treat poetic color harmony as chart-ready by default; validate distinctness or ordering for the chart mode.
- Do not rely on hue alone. Add label, order, pattern, stroke, marker shape, direct labeling, or interaction guidance when needed.

## Chart Mode Workflow

1. Identify data meaning before picking colors:
   - Categorical: unrelated groups.
   - Sequential: low to high values.
   - Diverging: two directions around a meaningful midpoint.
   - Highlight: one or two emphasized series against quiet context.
   - Dashboard semantic: success, warning, danger, info, selected, neutral.
2. Choose selection criteria:
   - Categorical: maximize hue and lightness separation.
   - Sequential: monotonic lightness is more important than poetic harmony.
   - Diverging: balance perceived strength on both sides and reserve a neutral midpoint.
   - Highlight: keep background series quiet and the target unmistakable.
3. Build the palette from project colors only.
4. Add chart implementation details:
   - Background/grid/axis color.
   - Legend or direct labels.
   - Hover and selection color.
   - Missing data and disabled series.
5. If requested, output ECharts, D3, Chart.js, or CSV arrays.

## Output Shape

- Data context: chart type, series count, background, data meaning.
- Mode decision: categorical, sequential, diverging, highlight, or semantic.
- Palette table: order or series, color name, HEX, role, reason.
- Usage rules: legend, labels, grid, hover, selection, missing data.
- Accessibility notes: where labels, markers, strokes, or patterns are required.
- Optional code in the requested chart format.

For charts with more than 12 categories, recommend grouping, sorting, filtering, or interaction rather than forcing more colors.

## Proven Palette: 3D UCS Surface + Signed Error

Use this palette when a 3D surface encodes a continuous UCS value and lollipop
markers encode signed model error:

```python
from matplotlib.colors import LinearSegmentedColormap

VALUE_CMAP = LinearSegmentedColormap.from_list(
    'ucs_zhongguo_seq',
    [
        '#003152',  # 普鲁士蓝, lowest value
        '#1661AB',  # 靛青
        '#2376B7',  # 花青
        '#1E9EB3',  # 翠蓝
        '#57C3C2',  # 石绿
        '#B6D7A8',  # 松花
        '#F6D58A',  # 杏黄
        '#FFF2B2',  # 乳鸭黄, highest value
    ],
    N=256,
)

POS_BALL = '#D92121'  # 朱砂红, positive error / over-prediction
POS_STEM = '#A61B29'  # 苋菜红
NEG_BALL = '#1A94BC'  # 钴蓝, negative error / under-prediction
NEG_STEM = '#15559A'  # 海涛蓝
COL_SPINE = '#2C2C2C'
COL_GRID = '#DDDDDD'
COL_TEXT = '#1A1A1A'
COL_BG = '#FFFFFF'
```

Usage rules:

- Treat the surface as sequential data; map low-to-high values through the full
  blue-cyan-green-yellow ramp.
- The listed stops are ordered by increasing perceived lightness; do not insert
  a darker warm stop after `#B6D7A8` without rechecking monotonicity.
- Treat signed model error as diverging semantic glyph color: warm red for
  over-prediction and cool blue for under-prediction.
- Add shape/depth cues, not only hue: use lollipop direction, cylinder/sphere
  glyphs, legend labels, and an overall error range.
- Avoid per-point numeric labels when many lollipops are present; they obscure the
  surface and reduce accessibility.

## Required Inputs

Ask for these if missing:

- chart type and data meaning: categorical, sequential, diverging, highlight, semantic dashboard, map, or interaction state;
- number of series/classes and background color;
- accessibility constraints such as colorblind-safe, grayscale print, direct labels, markers, or patterns;
- target implementation format, if any: Matplotlib, ECharts, D3, Chart.js, CSS, JSON, or CSV.

## Output Contract

Return a palette decision that includes:

- data context and chosen palette mode;
- ordered color list with Chinese color name, HEX value, role, and reason;
- usage rules for axes, grid, labels, legend, hover/selection, missing data, and disabled states;
- accessibility notes and optional implementation code in the requested format.

## Local Contents

This lightweight skill keeps its reusable palette rules, proven UCS/error palette, input contract, and output contract entirely in this `SKILL.md`.

- `LICENSE` and `NOTICE.md`: retained MIT terms and upstream provenance.
