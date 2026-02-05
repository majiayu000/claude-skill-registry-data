---
name: d3-charts
description: Create interactive, production-grade charts with D3.js. Use this skill when the user asks to build D3.js visualizations including scatter plots, pie/donut charts, bar charts, bar chart races, line charts, line chart races, heatmaps, treemaps, or any SVG-based data visualization. Covers animated entry transitions, keyframe animations, progressive line reveals, hierarchical layouts, sequential color scales, theme-aware color schemes (with custom Streamlit-inspired palettes), tooltips, legends, and responsive design. Generates polished, accessible code that avoids generic AI aesthetics.
---

# D3.js Chart Patterns

## Quick Reference

| Chart Type | Use Case | Key APIs |
|------------|----------|----------|
| Scatter | Correlation, clusters, distributions | `scaleLinear`, `circle`, `symbol` |
| Pie/Donut | Part-to-whole, allocations | `pie`, `arc`, `scaleOrdinal` |
| Bar | Comparisons, rankings | `scaleBand`, `rect` |
| Bar Race | Animated rankings over time | `scaleBand`, `rect`, keyframes |
| Line | Time series, trends | `line`, `curveMonotoneX` |
| Line Race | Animated time series progression | `line`, `setInterval`, dynamic domains |
| Heatmap | Matrix data, correlations, calendars | `scaleBand`, `scaleSequential`, `rect` |
| Treemap | Hierarchical part-to-whole | `treemap`, `hierarchy`, `scaleOrdinal` |

## Animation Patterns

### Scatter Plot Entry Animation

**Required behavior:**
1. X axis starts at domain `[0, 0]` with `opacity: 0`
2. Dots positioned at `x=0` (clustered left)
3. X axis transitions to actual domain with fade-in (2s)
4. Dots animate to final positions with staggered delay (`i * 3ms`)
5. Markers/annotations appear after dots (delay 2.5s)

```typescript
// 1. Initialize X scale collapsed
const xScale = d3.scaleLinear().domain([0, 0]).range([0, innerWidth]);

// 2. Create axis hidden
const xAxisGroup = g.append('g')
  .attr('transform', `translate(0, ${innerHeight})`)
  .attr('opacity', 0)
  .call(d3.axisBottom(xScale));

// 3. Add dots at initial position
const circles = chartArea.selectAll('.point')
  .data(data)
  .join('circle')
  .attr('cx', d => xScale(d.x))  // All at 0
  .attr('cy', d => yScale(d.y))
  .attr('r', 1.5)
  .attr('opacity', 0.6);

// 4. Update domain and animate
xScale.domain([xMin - padding, xMax + padding]);

xAxisGroup.transition().duration(2000)
  .attr('opacity', 1)
  .call(d3.axisBottom(xScale));

circles.transition()
  .delay((_, i) => i * 3)
  .duration(2000)
  .attr('cx', d => xScale(d.x))
  .attr('r', 3);
```

### Pie Chart Smooth Transitions

**Required behavior:**
1. Use key function for object constancy
2. Store `_current` arc on DOM element
3. Interpolate between old/new arc states
4. Stable sort by key prevents slice jumping

```typescript
const pie = d3.pie<DataItem>()
  .value(d => d.value)
  .sort((a, b) => d3.ascending(a.key, b.key));  // Stable order

svg.selectAll<SVGPathElement, PieArcDatum>('path.slice')
  .data(pie(data), d => d.data.key)  // Key function
  .join(
    enter => enter.append('path')
      .attr('class', 'slice')
      .each(function(d) { (this as any)._current = d; }),
    update => update,
    exit => exit.transition().duration(500).style('opacity', 0).remove()
  )
  .transition().duration(800)
  .attrTween('d', function(d) {
    const el = this as any;
    const interp = d3.interpolate(el._current || { startAngle: 0, endAngle: 0 }, d);
    el._current = d;
    return t => arc(interp(t)) || '';
  });
```

### Bar Chart Race Animation

**Required behavior:**
1. Data organized into keyframes (date + ranked items)
2. Bars enter from previous rank, exit to next rank
3. Labels animate position and interpolate values
4. Ticker displays current time period
5. X axis updates dynamically to top value

```typescript
// === CONFIGURATION ===
const n = 12;              // Number of bars to show
const barSize = 48;        // Height per bar
const duration = 250;      // ms per keyframe
const margin = { top: 16, right: 6, bottom: 6, left: 0 };

// === SCALES ===
const x = d3.scaleLinear([0, 1], [margin.left, width - margin.right]);
const y = d3.scaleBand<number>()
  .domain(d3.range(n + 1))
  .rangeRound([margin.top, margin.top + barSize * (n + 1 + 0.1)])
  .padding(0.1);

// === BARS UPDATE FUNCTION ===
function bars(svg: d3.Selection<SVGSVGElement, unknown, null, undefined>) {
  let bar = svg.append('g')
    .attr('fill-opacity', 0.6)
    .selectAll('rect');

  return ([date, data]: [Date, RankedItem[]], transition: d3.Transition<any, any, any, any>) => {
    bar = bar
      .data(data.slice(0, n), (d: any) => d.name)
      .join(
        enter => enter.append('rect')
          .attr('fill', d => color(d.category))
          .attr('height', y.bandwidth())
          .attr('x', x(0))
          .attr('y', d => y((prev.get(d) || d).rank)!)
          .attr('width', d => x((prev.get(d) || d).value) - x(0)),
        update => update,
        exit => exit.transition(transition).remove()
          .attr('y', d => y((next.get(d) || d).rank)!)
          .attr('width', d => x((next.get(d) || d).value) - x(0))
      )
      .call(bar => bar.transition(transition)
        .attr('y', d => y(d.rank)!)
        .attr('width', d => x(d.value) - x(0)));
  };
}

// === LABELS UPDATE FUNCTION ===
function labels(svg: d3.Selection<SVGSVGElement, unknown, null, undefined>) {
  let label = svg.append('g')
    .style('font', 'bold 12px var(--sans-serif)')
    .style('font-variant-numeric', 'tabular-nums')
    .attr('text-anchor', 'end')
    .selectAll('text');

  return ([date, data]: [Date, RankedItem[]], transition: d3.Transition<any, any, any, any>) => {
    label = label
      .data(data.slice(0, n), (d: any) => d.name)
      .join(
        enter => enter.append('text')
          .attr('transform', d => `translate(${x((prev.get(d) || d).value)},${y((prev.get(d) || d).rank)})`)
          .attr('y', y.bandwidth() / 2)
          .attr('x', -6)
          .attr('dy', '-0.25em')
          .text(d => d.name)
          .call(text => text.append('tspan')
            .attr('fill-opacity', 0.7)
            .attr('font-weight', 'normal')
            .attr('x', -6)
            .attr('dy', '1.15em')),
        update => update,
        exit => exit.transition(transition).remove()
          .attr('transform', d => `translate(${x((next.get(d) || d).value)},${y((next.get(d) || d).rank)})`)
      )
      .call(bar => bar.transition(transition)
        .attr('transform', d => `translate(${x(d.value)},${y(d.rank)})`)
        .call(g => g.select('tspan')
          .textTween((d: any) => (t: number) => 
            formatNumber(d3.interpolateNumber((prev.get(d) || d).value, d.value)(t))
          )
        )
      );
  };
}

// === TICKER (TIME DISPLAY) ===
function ticker(svg: d3.Selection<SVGSVGElement, unknown, null, undefined>) {
  const now = svg.append('text')
    .style('font', `bold ${barSize}px var(--sans-serif)`)
    .style('font-variant-numeric', 'tabular-nums')
    .attr('text-anchor', 'end')
    .attr('x', width - 6)
    .attr('y', margin.top + barSize * (n - 0.45))
    .attr('dy', '0.32em')
    .text(formatDate(keyframes[0][0]));

  return ([date]: [Date, RankedItem[]], transition: d3.Transition<any, any, any, any>) => {
    transition.end().then(() => now.text(formatDate(date)));
  };
}

// === MAIN ANIMATION LOOP ===
async function animate() {
  const updateBars = bars(svg);
  const updateLabels = labels(svg);
  const updateTicker = ticker(svg);

  for (const keyframe of keyframes) {
    const transition = svg.transition()
      .duration(duration)
      .ease(d3.easeLinear);

    x.domain([0, keyframe[1][0].value]);  // Top bar sets domain

    updateBars(keyframe, transition);
    updateLabels(keyframe, transition);
    updateTicker(keyframe, transition);

    await transition.end();
  }
}
```

### Line Chart Race Animation

**Required behavior:**
1. Data split into progressive chunks (frames)
2. Line draws incrementally as time progresses
3. Axes update dynamically to fit current data range
4. Circles mark current data points with labels
5. Time indicator shows current period

```typescript
// === CONFIGURATION ===
const duration = 1000;  // ms per frame
const margin = { top: 60, right: 120, bottom: 60, left: 60 };

// === SCALES ===
const x = d3.scaleTime().range([0, innerWidth]);
const y = d3.scaleLinear().range([innerHeight, 0]);

// === LINE GENERATOR ===
const line = d3.line<DataPoint>()
  .x(d => x(d.date))
  .y(d => y(d.value))
  .curve(d3.curveMonotoneX);

// === AXES ===
const xAxis = d3.axisBottom(x).ticks(6);
const yAxis = d3.axisLeft(y).ticks(8);

// === GRADIENT DEFINITIONS ===
function createGradient(svg: d3.Selection<SVGGElement, unknown, null, undefined>, id: string, colors: string[]) {
  const gradient = svg.append('defs')
    .append('linearGradient')
    .attr('id', id)
    .attr('x1', '0%').attr('y1', '0%')
    .attr('x2', '100%').attr('y2', '0%');
  
  colors.forEach((color, i) => {
    gradient.append('stop')
      .attr('offset', `${(i / (colors.length - 1)) * 100}%`)
      .attr('stop-color', color);
  });
}

// === UPDATE FUNCTIONS ===
function updateAxis() {
  svg.select('.x-axis')
    .transition().ease(d3.easeLinear).duration(duration)
    .call(xAxis as any);
  
  svg.select('.y-axis')
    .transition().ease(d3.easeCubic).duration(duration)
    .call(yAxis as any);
}

function updateLine(data: DataPoint[], seriesIndex: number) {
  const path = svg.select(`.line-${seriesIndex}`)
    .datum(data)
    .attr('d', line);
  
  // Animate line drawing
  const totalLength = (path.node() as SVGPathElement).getTotalLength();
  path
    .attr('stroke-dasharray', `${totalLength} ${totalLength}`)
    .attr('stroke-dashoffset', totalLength)
    .transition().duration(duration).ease(d3.easeLinear)
    .attr('stroke-dashoffset', 0);
}

function updateCircle(data: DataPoint[], seriesIndex: number, color: string) {
  const lastPoint = data[data.length - 1];
  
  svg.select(`.circle-${seriesIndex}`)
    .transition().duration(duration)
    .attr('cx', x(lastPoint.date))
    .attr('cy', y(lastPoint.value))
    .attr('fill', color);
}

function updateLabel(data: DataPoint[], seriesIndex: number, label: string) {
  const lastPoint = data[data.length - 1];
  
  svg.select(`.label-${seriesIndex}`)
    .transition().duration(duration)
    .attr('x', x(lastPoint.date) + 10)
    .attr('y', y(lastPoint.value))
    .text(`${label}: ${formatValue(lastPoint.value)}`);
}

// === MAIN ANIMATION ===
function animateLineChart(frames: DataPoint[][], series: SeriesConfig[]) {
  let index = 0;
  
  function update() {
    if (index >= frames.length) {
      clearInterval(intervalId);
      return;
    }
    
    const currentData = frames[index];
    
    // Update domains
    x.domain(d3.extent(currentData, d => d.date) as [Date, Date]);
    y.domain([0, d3.max(currentData, d => d.value)! * 1.1]).nice();
    
    updateAxis();
    
    series.forEach((s, i) => {
      const seriesData = currentData.filter(d => d.series === s.key);
      updateLine(seriesData, i);
      updateCircle(seriesData, i, s.color);
      updateLabel(seriesData, i, s.label);
    });
    
    // Update time indicator
    svg.select('.time-indicator')
      .text(formatDate(currentData[currentData.length - 1].date));
    
    index++;
  }
  
  const intervalId = setInterval(update, duration);
}
```

### Heatmap

**Required behavior:**
1. Use `scaleBand` for both X and Y axes (categorical)
2. Use `scaleSequential` with interpolator for color
3. Rounded corners via `rx`/`ry` for modern look
4. Interactive tooltip on hover with cell highlight

```typescript
// === DATA FORMAT ===
interface HeatmapCell {
  group: string;    // X category (column)
  variable: string; // Y category (row)
  value: number;    // Cell value for color mapping
}

// === SCALES ===
const groups = Array.from(new Set(data.map(d => d.group)));
const variables = Array.from(new Set(data.map(d => d.variable)));

const x = d3.scaleBand<string>()
  .range([0, innerWidth])
  .domain(groups)
  .padding(0.05);

const y = d3.scaleBand<string>()
  .range([innerHeight, 0])
  .domain(variables)
  .padding(0.05);

// === COLOR SCALE (Sequential) ===
const colorScale = d3.scaleSequential()
  .interpolator(d3.interpolateRgbBasis(SEQUENTIAL_COLORS))  // Custom warm gradient
  .domain(d3.extent(data, d => d.value) as [number, number]);

// Alternative built-in interpolators:
// .interpolator(d3.interpolateInferno)
// .interpolator(d3.interpolateViridis)
// .interpolator(d3.interpolatePlasma)

// === AXES (minimal, no domain line) ===
svg.append('g')
  .attr('transform', `translate(0, ${innerHeight})`)
  .call(d3.axisBottom(x).tickSize(0))
  .call(g => g.select('.domain').remove());

svg.append('g')
  .call(d3.axisLeft(y).tickSize(0))
  .call(g => g.select('.domain').remove());

// === TOOLTIP ===
const tooltip = d3.select('#container')
  .append('div')
  .attr('class', 'tooltip')
  .style('opacity', 0)
  .style('position', 'absolute')
  .style('background-color', 'white')
  .style('border', '2px solid #333')
  .style('border-radius', '5px')
  .style('padding', '8px');

// === CELLS ===
svg.selectAll<SVGRectElement, HeatmapCell>('rect.cell')
  .data(data, d => `${d.group}:${d.variable}`)  // Key function
  .join('rect')
  .attr('class', 'cell')
  .attr('x', d => x(d.group)!)
  .attr('y', d => y(d.variable)!)
  .attr('rx', 4)
  .attr('ry', 4)
  .attr('width', x.bandwidth())
  .attr('height', y.bandwidth())
  .style('fill', d => colorScale(d.value))
  .style('stroke', 'none')
  .style('opacity', 0.8)
  .on('mouseenter', function(event, d) {
    tooltip.style('opacity', 1);
    d3.select(this).style('stroke', '#333').style('opacity', 1);
  })
  .on('mousemove', function(event, d) {
    tooltip
      .html(`<strong>${d.group} × ${d.variable}</strong><br/>Value: ${d.value}`)
      .style('left', `${event.pageX + 10}px`)
      .style('top', `${event.pageY - 10}px`);
  })
  .on('mouseleave', function() {
    tooltip.style('opacity', 0);
    d3.select(this).style('stroke', 'none').style('opacity', 0.8);
  });
```

### Treemap

**Required behavior:**
1. Hierarchical data with `d3.hierarchy()` + `.sum()` + `.sort()`
2. Layout with `d3.treemap()` and tiling algorithm
3. Color by top-level parent category
4. Clip paths prevent text overflow
5. Multi-line labels with value on last line

```typescript
// === DATA FORMAT ===
interface TreeNode {
  name: string;
  value?: number;        // Leaf nodes have value
  children?: TreeNode[]; // Parent nodes have children
}

// === LAYOUT ===
const width = 800;
const height = 600;

const root = d3.treemap<TreeNode>()
  .tile(d3.treemapSquarify)  // Or: treemapBinary, treemapSlice, treemapDice
  .size([width, height])
  .padding(1)
  .round(true)
(
  d3.hierarchy(data)
    .sum(d => d.value || 0)
    .sort((a, b) => (b.value || 0) - (a.value || 0))
);

// === COLOR SCALE (by top-level parent) ===
const topLevelNames = data.children?.map(d => d.name) || [];
const color = d3.scaleOrdinal<string>()
  .domain(topLevelNames)
  .range(CATEGORICAL_COLORS);

// Helper: get top-level parent
function getTopParent(d: d3.HierarchyRectangularNode<TreeNode>) {
  let node = d;
  while (node.depth > 1 && node.parent) node = node.parent;
  return node;
}

// === LEAVES ===
const leaf = svg.selectAll<SVGGElement, d3.HierarchyRectangularNode<TreeNode>>('g.leaf')
  .data(root.leaves())
  .join('g')
  .attr('class', 'leaf')
  .attr('transform', d => `translate(${d.x0}, ${d.y0})`);

// === TOOLTIP (via <title>) ===
const format = d3.format(',d');
leaf.append('title')
  .text(d => `${d.ancestors().reverse().map(n => n.data.name).join(' → ')}\n${format(d.value || 0)}`);

// === RECTANGLES ===
leaf.append('rect')
  .attr('id', (d, i) => `leaf-${i}`)
  .attr('fill', d => color(getTopParent(d).data.name))
  .attr('fill-opacity', 0.6)
  .attr('width', d => d.x1 - d.x0)
  .attr('height', d => d.y1 - d.y0)
  .attr('rx', 2);

// === CLIP PATHS ===
leaf.append('clipPath')
  .attr('id', (d, i) => `clip-${i}`)
  .append('rect')
  .attr('width', d => d.x1 - d.x0)
  .attr('height', d => d.y1 - d.y0);

// === MULTI-LINE LABELS ===
leaf.append('text')
  .attr('clip-path', (d, i) => `url(#clip-${i})`)
  .selectAll('tspan')
  .data(d => {
    // Split name on camelCase or spaces, add formatted value
    const nameParts = d.data.name.split(/(?=[A-Z][a-z])|\s+/g);
    return [...nameParts, format(d.value || 0)];
  })
  .join('tspan')
  .attr('x', 3)
  .attr('y', (_, i, nodes) => `${(i === nodes.length - 1 ? 0.3 : 0) + 1.1 + i * 0.9}em`)
  .attr('fill-opacity', (_, i, nodes) => i === nodes.length - 1 ? 0.7 : 1)
  .attr('font-size', '10px')
  .text(d => d);
```

## Color Schemes

### Custom Color Palette (Streamlit-Inspired)

```typescript
// Categorical colors (for discrete data: pie, bar, legend)
const CATEGORICAL_COLORS = [
  '#204F80',  // Deep blue
  '#804F1F',  // Warm brown
  '#0A2845',  // Navy
  '#426F99',  // Steel blue
  '#45280A',  // Dark brown
  '#996F42',  // Tan
  '#FF6B6B',  // Coral
  '#4ECDC4',  // Teal
  '#45B7D1',  // Sky blue
  '#96CEB4',  // Sage green
];

// Sequential colors (for continuous data: heatmaps, gradients)
const SEQUENTIAL_COLORS = [
  '#FDF2C5',  // Light cream
  '#FCE584',  // Pale yellow
  '#FBD453',  // Golden yellow
  '#FBC030',  // Amber
  '#F49F1E',  // Orange
  '#DC7702',  // Deep orange
  '#B85300',  // Burnt orange
  '#8F4014',  // Brown
  '#793207',  // Dark brown
  '#441B06',  // Near black
];

// Marker/highlight colors
const MARKER_COLORS = {
  primary:   '#804F1F',  // Warm brown (Max Sharpe style)
  secondary: '#204F80',  // Deep blue (Min Volatility style)
  tertiary:  '#45280A',  // Dark brown (Max Utility style)
};
```

### Sequential (Continuous Data)

For heatmaps, scatter color encoding, gradients:

```typescript
import * as d3Chromatic from 'd3-scale-chromatic';

const sequentialSchemes: Record<string, (t: number) => string> = {
  // Custom warm gradient (cream → dark brown)
  custom:  d3.interpolateRgb('#FDF2C5', '#441B06'),
  // Multi-stop custom gradient
  customMulti: d3.interpolateRgbBasis(SEQUENTIAL_COLORS),
  // Built-in schemes
  inferno: d3Chromatic.interpolateInferno,
  plasma:  d3Chromatic.interpolatePlasma,
  viridis: d3Chromatic.interpolateViridis,
  warm:    d3Chromatic.interpolateWarm,
  cool:    d3Chromatic.interpolateCool,
  magma:   d3Chromatic.interpolateMagma,
};

const colorScale = d3.scaleSequential()
  .domain(d3.extent(data, d => d.value) as [number, number])
  .interpolator(sequentialSchemes.custom);
```

### Categorical (Discrete Data)

For pie charts, grouped bars, legends:

```typescript
const categoricalSchemes: Record<string, readonly string[]> = {
  custom:     CATEGORICAL_COLORS,
  category10: d3Chromatic.schemeCategory10,
  set1:       d3Chromatic.schemeSet1,
  set2:       d3Chromatic.schemeSet2,
  set3:       d3Chromatic.schemeSet3,
  pastel1:    d3Chromatic.schemePastel1,
  pastel2:    d3Chromatic.schemePastel2,
  dark2:      d3Chromatic.schemeDark2,
};

const colorScale = d3.scaleOrdinal<string>()
  .domain(data.map(d => d.category))
  .range(categoricalSchemes.custom);
```

### Theme-Aware Colors

Light and dark mode support with Streamlit-inspired palette:

```typescript
function getThemeColors() {
  const isDark = document.documentElement.classList.contains('dark');
  return {
    // Base colors
    base:        isDark ? '#0E1117' : '#FFFFFF',
    text:        isDark ? '#FAFAFA' : '#1F1916',
    subText:     isDark ? '#E5E7EB' : '#56524D',
    primary:     isDark ? '#FF4B4B' : '#56524D',
    // Chart elements
    axis:        isDark ? '#4B5563' : '#2B2523',
    grid:        isDark ? '#374151' : '#E4E4E4',
    border:      isDark ? '#4B5563' : '#2B2523',
    // Interactive elements
    tooltipBg:   isDark ? '#262730' : '#FFFFFF',
    tooltipBorder: isDark ? '#4B5563' : '#2B2523',
    // Sidebar (if applicable)
    sidebarBg:   isDark ? '#1A1D26' : '#D4D4D4',
    sidebarText: isDark ? '#E5E7EB' : '#1F1916',
  };
}

// Update chart on theme change
window.addEventListener('themechange', () => {
  const colors = getThemeColors();
  svg.selectAll('.x-axis .domain').attr('stroke', colors.axis);
  svg.selectAll('.y-axis .domain').attr('stroke', colors.axis);
  svg.selectAll('.tick line').attr('stroke', colors.axis);
  svg.selectAll('.tick text').attr('fill', colors.subText);
});

// Dispatch from toggle button
window.dispatchEvent(new Event('themechange'));
```

## Interactive Elements

### Tooltip Pattern

```typescript
const tooltip = d3.select('#tooltip');

selection
  .on('mouseenter', (event, d) => {
    d3.select(event.currentTarget).attr('opacity', 1);
    tooltip
      .style('opacity', '1')
      .style('left', `${event.pageX + 10}px`)
      .style('top', `${event.pageY - 10}px`)
      .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
  })
  .on('mouseleave', (event) => {
    d3.select(event.currentTarget).attr('opacity', 0.6);
    tooltip.style('opacity', '0');
  });
```

### Legend with Toggle

```typescript
const legendItems = legend.selectAll('.legend-item')
  .data(categories)
  .join('g')
  .attr('class', 'legend-item')
  .style('cursor', 'pointer')
  .on('click', (_, d) => {
    const points = svg.selectAll(`.point-${d.key}`);
    const visible = points.attr('opacity') > 0.3;
    points.transition().duration(300).attr('opacity', visible ? 0.1 : 0.6);
  });
```

### Symbol Markers

```typescript
const symbols: Record<string, d3.SymbolType> = {
  circle:   d3.symbolCircle,
  star:     d3.symbolStar,
  diamond:  d3.symbolDiamond,
  square:   d3.symbolSquare,
  triangle: d3.symbolTriangle,
  cross:    d3.symbolCross,
};

g.append('path')
  .attr('d', d3.symbol().type(symbols.star).size(200)())
  .attr('fill', '#804F1F')
  .attr('stroke', '#fff')
  .attr('stroke-width', 2);
```

## Structural Patterns

### Margin Convention

```typescript
const margin = { top: 40, right: 30, bottom: 60, left: 65 };
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

const g = svg.append('g')
  .attr('transform', `translate(${margin.left}, ${margin.top})`);
```

### Clip Path for Overflow

```typescript
svg.append('defs')
  .append('clipPath')
  .attr('id', 'chart-clip')
  .append('rect')
  .attr('width', innerWidth)
  .attr('height', innerHeight);

const chartArea = g.append('g').attr('clip-path', 'url(#chart-clip)');
```

### Axis Formatting

```typescript
// Percentage
.tickFormat(d => `${(+d * 100).toFixed(0)}%`)

// Currency
.tickFormat(d => `$${d3.format(',.0f')(d)}`)

// SI prefix (K, M, B)
.tickFormat(d3.format('.2s'))

// Date
.tickFormat(d3.timeFormat('%b %Y'))
```

## Complete Examples

See `references/scatter-template.md` for full scatter plot implementation.
See `references/pie-template.md` for full pie/donut chart implementation.
See `references/bar-race-template.md` for full bar chart race implementation.
See `references/line-race-template.md` for full line chart race implementation.
See `references/heatmap-template.md` for full heatmap implementation.
See `references/treemap-template.md` for full treemap implementation.
See `references/color-schemes.md` for comprehensive color palette reference.
