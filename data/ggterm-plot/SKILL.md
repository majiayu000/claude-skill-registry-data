---
name: ggterm-plot
description: Create terminal data visualizations using Grammar of Graphics. Use when plotting data, creating charts, graphing, visualizing distributions, or when the user mentions plot, chart, graph, histogram, scatter, boxplot, or visualize.
allowed-tools: Bash(bun:*), Read
---

# Terminal Plotting with ggterm

Create plots using the CLI tool. Start by inspecting the data, then plot.

## Step 1: Inspect Data (Recommended)

```bash
bun packages/core/src/cli-plot.ts inspect <data.csv>
```

Shows column names, types (numeric/categorical/date), unique counts, and sample values.

## Step 2: Get Suggestions (Optional)

```bash
bun packages/core/src/cli-plot.ts suggest <data.csv>
```

Returns ready-to-run plot commands based on column types.

## Step 3: Create Plot

```bash
bun packages/core/src/cli-plot.ts <data.csv> <x> <y> [color] [title] [geom]
```

Arguments:
- `data.csv` - Path to CSV file (use absolute path or relative to ggterm dir)
- `x` - Column name for x-axis
- `y` - Column name for y-axis (use `-` for histogram)
- `color` - Column name for color (optional, use `-` to skip)
- `title` - Plot title (optional, use `-` to skip)
- `geom` - Geometry type: `point` (default), `line`, `path`, `step`, `bar`, `col`, `histogram`, `freqpoly`, `density`, `boxplot`, `violin`, `ridgeline`, `joy`, `beeswarm`, `quasirandom`, `dumbbell`, `lollipop`, `waffle`, `sparkline`, `bullet`, `braille`, `calendar`, `flame`, `icicle`, `corrmat`, `sankey`, `treemap`, `area`, `ribbon`, `rug`, `errorbar`, `errorbarh`, `crossbar`, `linerange`, `pointrange`, `smooth`, `segment`, `curve`, `rect`, `tile`, `raster`, `bin2d`, `text`, `label`, `contour`, `contour_filled`, `density_2d`, `qq`, `qq_line`, `hline`, `vline`, `abline`

## Examples

Scatter plot:
```bash
bun packages/core/src/cli-plot.ts data/iris.csv sepal_length sepal_width species "Iris Dataset" point
```

Line chart:
```bash
bun packages/core/src/cli-plot.ts data/stocks.csv date price symbol "Stock Prices" line
```

Histogram:
```bash
bun packages/core/src/cli-plot.ts data/iris.csv sepal_width - - "Sepal Width Distribution" histogram
```

Box plot:
```bash
bun packages/core/src/cli-plot.ts data/experiment.csv treatment response_time - "Response by Treatment" boxplot
```

## Workflow

1. Identify the data file from $ARGUMENTS or ask user
2. Run `inspect` to see column names and types
3. Run `suggest` to get recommended visualizations (or choose based on user request)
4. Run the plot command
5. Briefly describe what the plot shows

$ARGUMENTS

## Geom Selection Guide

| Data Question | Geom | Example |
|---------------|------|---------|
| Relationship between 2 variables | `geom_point()` | Scatter plot |
| Trend over time | `geom_line()` | Time series |
| Distribution of 1 variable | `geom_histogram()` | Frequency distribution |
| Smoothed distribution | `geom_density()` | Kernel density estimate |
| Distribution by group | `geom_boxplot()` | Compare medians |
| Density shape | `geom_violin()` | Distribution shape |
| Stacked distributions | `geom_ridgeline()` | Joy plot / ridgeline |
| Individual points | `geom_beeswarm()` | Avoid overlap in groups |
| Before/after comparison | `geom_dumbbell()` | Two connected points |
| Sparse rankings | `geom_lollipop()` | Clean bar alternative |
| Part-of-whole | `geom_waffle()` | Grid-based pie alternative |
| Inline trends | `geom_sparkline()` | Word-sized charts |
| KPI progress | `geom_bullet()` | Progress with target |
| High resolution | `geom_braille()` | 8x detail using braille |
| Activity over time | `geom_calendar()` | GitHub-style heatmap |
| Performance profiling | `geom_flame()` | Call stack visualization |
| Variable correlations | `geom_corrmat()` | Correlation matrix |
| Flow between categories | `geom_sankey()` | Source to target flows |
| Hierarchical proportions | `geom_treemap()` | Nested rectangles by value |
| Category comparison | `geom_bar()` | Counts per category |
| Known values per category | `geom_col()` | Bar heights from data |
| Trend with uncertainty | `geom_smooth()` | Fitted line |
| 2D density | `geom_density_2d()` | Contour density |
| Filled region | `geom_area()` | Cumulative or stacked |
| Error ranges | `geom_errorbar()` | Confidence intervals |
| Normality check | `geom_qq()` | Q-Q plot |
| Multi-distribution comparison | `geom_freqpoly()` | Overlaid frequency lines |

## Common Plot Types

### Scatter Plot
```typescript
gg(data)
  .aes({ x: 'weight', y: 'height', color: 'species' })
  .geom(geom_point({ size: 2 }))
```

### Line Chart
```typescript
gg(data)
  .aes({ x: 'date', y: 'value', color: 'category' })
  .geom(geom_line())
```

### Histogram
```typescript
import { geom_histogram } from '@ggterm/core'

gg(data)
  .aes({ x: 'value' })
  .geom(geom_histogram({ bins: 20 }))
```

### Box Plot
```typescript
import { geom_boxplot } from '@ggterm/core'

gg(data)
  .aes({ x: 'group', y: 'value' })
  .geom(geom_boxplot())
```

### Bar Chart
```typescript
import { geom_bar } from '@ggterm/core'

gg(data)
  .aes({ x: 'category', fill: 'category' })
  .geom(geom_bar())  // Counts occurrences
```

## Color and Styling

### Color Scales

```typescript
import { scale_color_viridis, scale_color_brewer } from '@ggterm/core'

// Viridis (perceptually uniform)
gg(data)
  .aes({ x: 'x', y: 'y', color: 'value' })
  .geom(geom_point())
  .scale(scale_color_viridis())

// ColorBrewer palettes
.scale(scale_color_brewer({ palette: 'Set1' }))  // Categorical
.scale(scale_color_brewer({ palette: 'Blues' })) // Sequential
```

### Themes

```typescript
import { themeDark, themeMinimal, themeClassic } from '@ggterm/core'

gg(data)
  .aes({ x: 'x', y: 'y' })
  .geom(geom_point())
  .theme(themeDark())      // Dark background
  // or .theme(themeMinimal())  // Clean, minimal
  // or .theme(themeClassic())  // Traditional
```

## Faceting (Small Multiples)

```typescript
import { facet_wrap, facet_grid } from '@ggterm/core'

// Wrap into grid
gg(data)
  .aes({ x: 'x', y: 'y' })
  .geom(geom_point())
  .facet(facet_wrap({ vars: 'category', ncol: 3 }))

// Grid by two variables
.facet(facet_grid({ rows: 'year', cols: 'region' }))
```

## Scale Transformations

```typescript
import { scale_x_log10, scale_y_sqrt } from '@ggterm/core'

gg(data)
  .aes({ x: 'population', y: 'gdp' })
  .geom(geom_point())
  .scale(scale_x_log10())
  .scale(scale_y_sqrt())
```

## Layering Multiple Geoms

```typescript
gg(data)
  .aes({ x: 'time', y: 'value' })
  .geom(geom_point({ alpha: 0.5 }))  // Points first
  .geom(geom_line())                  // Line on top
  .geom(geom_smooth({ method: 'loess' }))  // Trend line
```

## Annotations

```typescript
import { annotate_text, annotate_hline, annotate_rect } from '@ggterm/core'

gg(data)
  .aes({ x: 'x', y: 'y' })
  .geom(geom_point())
  .annotate(annotate_hline({ yintercept: 0, linetype: 'dashed' }))
  .annotate(annotate_text({ x: 10, y: 5, label: 'Important point' }))
```

## Saving Plot Specifications

For reproducibility, save the PlotSpec alongside output:

```typescript
import { writeFileSync } from 'fs'

const plot = gg(data).aes({ x: 'x', y: 'y' }).geom(geom_point())

// Get JSON-serializable specification
const spec = plot.spec()
writeFileSync('plot-spec.json', JSON.stringify(spec, null, 2))

// Render to terminal
console.log(plot.render({ width: 80, height: 24 }))
```

## Render Options

```typescript
plot.render({
  width: 80,           // Characters wide
  height: 24,          // Lines tall
  renderer: 'auto',    // 'braille' | 'block' | 'sixel' | 'auto'
  colorMode: 'truecolor'  // Use 'truecolor' for full color support
})
```

## Quick Reference

For detailed examples, see [examples/basic-plots.md](examples/basic-plots.md).

### All Available Geoms (52 total)

Point/line: `geom_point`, `geom_line`, `geom_path`, `geom_step`
Bar: `geom_bar`, `geom_col`, `geom_histogram`, `geom_freqpoly`, `geom_density`
Distribution: `geom_boxplot`, `geom_violin`, `geom_ridgeline`, `geom_joy`, `geom_beeswarm`, `geom_quasirandom`, `geom_density_2d`, `geom_qq`, `geom_qq_line`
Comparison: `geom_dumbbell`, `geom_lollipop`
Terminal-native: `geom_waffle`, `geom_sparkline`, `geom_bullet`, `geom_braille`
Specialized: `geom_calendar`, `geom_flame`, `geom_icicle`, `geom_corrmat`, `geom_sankey`, `geom_treemap`
Area: `geom_area`, `geom_ribbon`
Reference: `geom_hline`, `geom_vline`, `geom_abline`, `geom_segment`, `geom_curve`
Text: `geom_text`, `geom_label`
Error bars: `geom_errorbar`, `geom_errorbarh`, `geom_crossbar`, `geom_linerange`, `geom_pointrange`
2D/Tile: `geom_tile`, `geom_raster`, `geom_bin2d`, `geom_rect`, `geom_contour`, `geom_contour_filled`
Other: `geom_rug`, `geom_smooth`

### All Available Scales

Position: `scale_x_continuous`, `scale_y_continuous`, `scale_x_log10`, `scale_y_log10`, `scale_x_sqrt`, `scale_y_sqrt`, `scale_x_reverse`, `scale_y_reverse`, `scale_x_discrete`, `scale_y_discrete`

Color: `scale_color_continuous`, `scale_color_discrete`, `scale_color_viridis`, `scale_color_brewer`, `scale_color_gradient`, `scale_color_gradient2`, `scale_fill_*` (same variants)

Size: `scale_size_continuous`, `scale_size_area`, `scale_size_radius`

DateTime: `scale_x_datetime`, `scale_y_datetime`, `scale_x_date`, `scale_y_date`
