---
name: layercake
description: Expert guide for Layer Cake, a headless Svelte visualization framework managing scales, dimensions, and data flow while supporting SVG, Canvas, HTML, and WebGL rendering contexts for responsive data visualizations.
license: MIT
---

# Layer Cake Skill

Layer Cake is a foundational visualization framework for Svelte that handles the mathematics of coordinate systems and scales while remaining completely agnostic about visual presentation.

## Core Philosophy

Layer Cake follows a "bring your own components" approach. The framework establishes context through reactive Svelte stores, making D3 scales (linear, time, ordinal, log, threshold) and calculated dimensions available to child components via Svelte's context API. Developers build visualization components that consume these stores rather than managing transforms themselves.

## Primary Components

**LayerCake**: The root wrapper establishing context, calculating scales from data extents, managing responsive dimensions, and providing stores for x/y/r scales to children.

**Svg, Canvas, Html**: Layout containers for different rendering contexts. All coexist in the same coordinate system, allowing hybrid rendering (SVG axes + Canvas marks + HTML tooltips).

**Custom Components**: Build components that consume stores (`xScale$`, `yScale$`, etc.) from context and render visual elements.

## Core Concepts

### Scales and Dimensions

LayerCake automatically creates D3 scales from data extents. Configure domain/range through props:
- `x`, `y`, `r`, `z`: Data accessors for scale dimensions
- `xDomain`, `yDomain`, `rDomain`: Explicit domain overrides (defaults to data extent)
- `padding`: Inner padding applied to container dimensions before scale calculation
- `xScale`, `yScale`, `rScale`: Custom D3 scale instances (replaces default linear scales)

### Data Transformation

Use utility functions before passing to LayerCake:

- `stack()` - D3 stack layout for stacked bar/area charts (returns [[[x0, x1], ...], ...] per series)
- `bin()` - D3 bin layout for histograms (returns bins with x0/x1 bounds and data array)
- `groupLonger()` - Wide→long pivot (creates groups with nested values array)
- `flatten()` - One-level array flattening with accessor support
- `calcExtents()` - Calculate min/max across multiple fields, skipping nulls

### Rendering Contexts

**SVG**: Accessibility, interactivity, animations. Suitable for <500 marks. Provides `<svg>` element with proper dimensions.

**Canvas**: High-performance 2D rendering for 5000+ points. Access raw canvas context via `bind:context`. Handles device pixel ratio scaling via `scaleCanvas()`.

**HTML**: DOM elements (tooltips, labels) positioned in chart space. Use `pointerEvents={false}` to prevent blocking interactions.

## Implementation Patterns

### Basic Time Series

```svelte
<LayerCake x="date" y="temperature" data={weatherData} xScale={scaleTime()}>
  <Svg>
    <AxisX />
    <AxisY />
    <Line stroke="#667eea" />
  </Svg>
</LayerCake>
```

### Stacked Area Chart

Pre-process with `stack()`, then render stacked series accessing baseline+top values from context.

### High-Volume Scatter

Canvas layer for 10,000+ points with SVG axes overlay. Points rendered via canvas context loop over data, accessing scales from context.

### Multi-Scale Responsive

Responsive padding adjusts viewable area. Scales reactively recalculate as container resizes. Use reactive statements (`$:`) to update transforms.

## Key Functions Reference

**calcExtents(data, fields)**: Returns {fieldName: [min, max]} for all specified fields, skipping nulls/NaN.

**stack(data, keys, options)**: Transforms wide data to stacked format. Returns array of series, each with [[baseline, value], ...] tuples. Each tuple has `.data` reference to original object.

**bin(data, accessor, options)**: Histogram binning. Returns array of bins, each with x0, x1, and containing data items.

**groupLonger(data, keys, options)**: Pivots wide columns into long format. Returns {group, values: [...]} objects.

**flatten(data, accessor?)**: Flattens one level with optional accessor for nested arrays.

**scaleCanvas(ctx, width, height)**: Handles device pixel ratio scaling. Call once at canvas setup. Returns actual pixel dimensions.

## Advanced Techniques

**Custom Scales**: Pass any D3 scale instance (scaleLog, scalePower, scaleThreshold). Layer Cake calculates ranges but respects custom scale types.

**Multiple Datasets**: Create separate LayerCake instances or use `r` dimension for third numeric axis.

**Click/Hover Handling**: Inverse-scale mouse position via `xScale.invert()` to find data coordinates.

**Legends**: Build custom legend components accessing scale domain/range from context.

**Accessibility**: SVG layout automatically includes ARIA attributes. Add labels and descriptions via component props.

## Performance Notes

- Scale calculations (O(n)) only occur on data/domain changes
- Responsive dimension updates don't recalculate scales if extents unchanged
- Canvas rendering ~60fps for 10,000 points on modern devices
- Avoid <Svg> for high-volume marks; use Canvas instead
- Memoize data transforms outside render function lifecycle

## Svelte Integration

All reactivity via Svelte stores and reactive statements. When data changes, all subscribed components automatically update. Transitions/animations handled by child components using Svelte `animate:` and `transition:` directives.

Works with SvelteKit for SSR and client-side hydration. Context API integrates seamlessly with nested component hierarchies.
