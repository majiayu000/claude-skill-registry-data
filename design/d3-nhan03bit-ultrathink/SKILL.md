---
name: d3
description: D3.js data visualization — scales, axes, SVG rendering, force layouts, transitions, geo projections, and idiomatic React integration patterns
layer: domain-specialist
category: visualization
triggers:
  - "d3 chart"
  - "data visualization"
  - "svg chart"
  - "force layout"
  - "d3 scales"
  - "bar chart"
  - "line chart"
  - "scatter plot"
  - "d3 transition"
  - "d3 react"
inputs:
  - Data shape (array of objects, nested, time series)
  - Chart type (bar, line, scatter, force, geo, treemap, etc.)
  - Interaction requirements (tooltips, zoom, brush, drag)
  - Target framework (vanilla, React, Svelte)
outputs:
  - Complete chart component with scales, axes, and rendering
  - Responsive SVG layout with proper viewBox handling
  - Transition and animation code
  - Accessibility attributes (aria-label, role, desc)
linksTo:
  - react
  - animation
  - responsive-design
  - css-variables
linkedFrom:
  - ui-ux-pro
  - design-systems
preferredNextSkills:
  - animation
  - responsive-design
fallbackSkills:
  - threejs
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Adds d3 dependencies to project
  - May add SVG elements to DOM
---

# D3.js Data Visualization Skill

## Purpose

D3 (Data-Driven Documents) binds data to DOM elements and applies data-driven transformations. This skill covers idiomatic D3 v7 patterns, React integration (letting D3 handle math, React handle DOM), and production-quality chart architecture.

## Key Concepts

### D3's Role: Math, Not DOM

In modern apps, D3 should compute — scales, layouts, paths, projections — while the framework (React, Svelte) owns the DOM. Only use D3's DOM manipulation (`select`, `append`, `enter/exit`) in vanilla JS or when D3 transitions are essential.

```
D3 Responsibility Split:
  D3 owns:  Scales, axes generators, path generators, layouts, transitions
  React owns:  DOM rendering, event handling, state, lifecycle
```

### Core Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Scales** | Map data domain to visual range | `scaleLinear().domain([0, 100]).range([0, 500])` |
| **Axes** | Generate tick marks and labels | `axisBottom(xScale).ticks(5)` |
| **Shapes** | Generate SVG path strings | `line().x(d => xScale(d.date)).y(d => yScale(d.value))` |
| **Layouts** | Compute positions from data | `forceSimulation(nodes).force('charge', forceManyBody())` |
| **Selections** | Bind data to DOM elements | `selectAll('rect').data(data).join('rect')` |
| **Transitions** | Animate between states | `select(el).transition().duration(300).attr('y', newY)` |

## Workflow

### Step 1: Define the Data Contract

Always type your data before building:

```typescript
interface DataPoint {
  date: Date;
  value: number;
  category: string;
}

interface ChartDimensions {
  width: number;
  height: number;
  margin: { top: number; right: number; bottom: number; left: number };
}

function useDimensions(margin: ChartDimensions['margin']): ChartDimensions & {
  innerWidth: number;
  innerHeight: number;
} {
  const width = 800;
  const height = 400;
  return {
    width,
    height,
    margin,
    innerWidth: width - margin.left - margin.right,
    innerHeight: height - margin.top - margin.bottom,
  };
}
```

### Step 2: Build Scales

```typescript
import { scaleLinear, scaleTime, scaleBand, scaleOrdinal, extent, schemeTableau10 } from 'd3';

// Linear scale (continuous -> continuous)
const yScale = scaleLinear()
  .domain([0, Math.max(...data.map(d => d.value))])
  .range([innerHeight, 0])
  .nice(); // Round domain to nice values

// Time scale
const xScale = scaleTime()
  .domain(extent(data, d => d.date) as [Date, Date])
  .range([0, innerWidth]);

// Band scale (categorical -> continuous, for bar charts)
const xBand = scaleBand<string>()
  .domain(data.map(d => d.category))
  .range([0, innerWidth])
  .padding(0.2); // Gap between bars

// Ordinal color scale
const colorScale = scaleOrdinal<string>()
  .domain(categories)
  .range(schemeTableau10);
```

### Step 3: React Integration Pattern (Recommended)

```tsx
import { useRef, useEffect, useMemo } from 'react';
import {
  scaleLinear, scaleBand, axisBottom, axisLeft,
  select, max, line, curveMonotoneX,
} from 'd3';

interface BarChartProps {
  data: { label: string; value: number }[];
  width?: number;
  height?: number;
}

export function BarChart({ data, width = 600, height = 400 }: BarChartProps) {
  const margin = { top: 20, right: 20, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // D3 computes scales (math only)
  const xScale = useMemo(
    () => scaleBand<string>()
      .domain(data.map(d => d.label))
      .range([0, innerWidth])
      .padding(0.2),
    [data, innerWidth]
  );

  const yScale = useMemo(
    () => scaleLinear()
      .domain([0, max(data, d => d.value) ?? 0])
      .range([innerHeight, 0])
      .nice(),
    [data, innerHeight]
  );

  // React renders the SVG — D3 only used for axis rendering via ref
  const xAxisRef = useRef<SVGGElement>(null);
  const yAxisRef = useRef<SVGGElement>(null);

  useEffect(() => {
    if (xAxisRef.current) {
      select(xAxisRef.current).call(axisBottom(xScale));
    }
    if (yAxisRef.current) {
      select(yAxisRef.current).call(axisLeft(yScale).ticks(5));
    }
  }, [xScale, yScale]);

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label={`Bar chart with ${data.length} items`}
    >
      <g transform={`translate(${margin.left},${margin.top})`}>
        {/* Bars — React renders, D3 computes positions */}
        {data.map(d => (
          <rect
            key={d.label}
            x={xScale(d.label)}
            y={yScale(d.value)}
            width={xScale.bandwidth()}
            height={innerHeight - yScale(d.value)}
            fill="var(--color-primary, #6366f1)"
            rx={4}
          >
            <title>{`${d.label}: ${d.value}`}</title>
          </rect>
        ))}

        {/* Axes — D3 renders via refs (imperative) */}
        <g ref={xAxisRef} transform={`translate(0,${innerHeight})`} />
        <g ref={yAxisRef} />
      </g>
    </svg>
  );
}
```

### Step 4: Line Chart with Transitions

```tsx
import { line, curveMonotoneX, select, transition } from 'd3';

function AnimatedLine({
  data,
  xScale,
  yScale,
}: {
  data: DataPoint[];
  xScale: d3.ScaleTime<number, number>;
  yScale: d3.ScaleLinear<number, number>;
}) {
  const pathRef = useRef<SVGPathElement>(null);

  const lineGenerator = useMemo(
    () => line<DataPoint>()
      .x(d => xScale(d.date))
      .y(d => yScale(d.value))
      .curve(curveMonotoneX),
    [xScale, yScale]
  );

  const pathD = lineGenerator(data) ?? '';

  // Animate path on data change
  useEffect(() => {
    if (!pathRef.current) return;
    const path = select(pathRef.current);
    const length = path.node()!.getTotalLength();

    path
      .attr('stroke-dasharray', `${length} ${length}`)
      .attr('stroke-dashoffset', length)
      .transition()
      .duration(800)
      .attr('stroke-dashoffset', 0);
  }, [pathD]);

  return (
    <path
      ref={pathRef}
      d={pathD}
      fill="none"
      stroke="var(--color-primary, #6366f1)"
      strokeWidth={2}
    />
  );
}
```

### Step 5: Force Layout

```typescript
import {
  forceSimulation, forceLink, forceManyBody,
  forceCenter, forceCollide, SimulationNodeDatum,
} from 'd3';

interface Node extends SimulationNodeDatum {
  id: string;
  group: number;
}

interface Link {
  source: string;
  target: string;
  value: number;
}

function useForceLayout(nodes: Node[], links: Link[], width: number, height: number) {
  const [simulatedNodes, setSimulatedNodes] = useState<Node[]>([]);

  useEffect(() => {
    const simulation = forceSimulation(nodes)
      .force('link', forceLink<Node, Link>(links).id(d => d.id).distance(80))
      .force('charge', forceManyBody().strength(-200))
      .force('center', forceCenter(width / 2, height / 2))
      .force('collision', forceCollide().radius(20));

    simulation.on('tick', () => {
      setSimulatedNodes([...simulation.nodes()]);
    });

    return () => { simulation.stop(); };
  }, [nodes, links, width, height]);

  return simulatedNodes;
}
```

### Step 6: Responsive Charts

```tsx
function useResizeObserver(ref: React.RefObject<HTMLDivElement>) {
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect;
      setDimensions({ width, height });
    });

    observer.observe(el);
    return () => observer.disconnect();
  }, [ref]);

  return dimensions;
}

function ResponsiveChart({ data }: { data: DataPoint[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const { width, height } = useResizeObserver(containerRef);

  return (
    <div ref={containerRef} style={{ width: '100%', aspectRatio: '16/9' }}>
      {width > 0 && (
        <BarChart data={data} width={width} height={height} />
      )}
    </div>
  );
}
```

## Common Pitfalls

1. **D3 fighting React for DOM control** — Never use `d3.select().append()` inside React components for elements React should own. Use D3 for math only; let React render SVG elements. Exception: axes (use refs).
2. **Missing key prop on mapped SVG elements** — D3's `join()` handles enter/update/exit, but React needs `key`. Always add unique keys to mapped `<rect>`, `<circle>`, etc.
3. **Not using `viewBox`** — Hardcoded `width`/`height` without `viewBox` breaks responsive behavior. Always set `viewBox` and let CSS control the actual size.
4. **Forgetting `.nice()` on scales** — Domain `[0, 97]` produces ugly axis ticks. `.nice()` rounds to `[0, 100]`.
5. **Importing all of D3** — `import * as d3 from 'd3'` bundles ~500KB. Import specific modules: `d3-scale`, `d3-shape`, `d3-axis`.
6. **Transition memory leaks** — D3 transitions on unmounted elements throw. Always clean up simulations and cancel transitions in `useEffect` cleanup.

## Examples

### Example 1: Dashboard Sparkline (Minimal)

```tsx
function Sparkline({ data, width = 120, height = 32 }: {
  data: number[];
  width?: number;
  height?: number;
}) {
  const xScale = scaleLinear().domain([0, data.length - 1]).range([0, width]);
  const yScale = scaleLinear().domain(extent(data) as [number, number]).range([height - 2, 2]);

  const pathD = line<number>()
    .x((_, i) => xScale(i))
    .y(d => yScale(d))
    .curve(curveMonotoneX)(data);

  return (
    <svg width={width} height={height} aria-label="Sparkline trend">
      <path d={pathD ?? ''} fill="none" stroke="currentColor" strokeWidth={1.5} />
    </svg>
  );
}
```

### Example 2: Donut Chart

```tsx
import { pie, arc, PieArcDatum } from 'd3';

function DonutChart({ data }: { data: { label: string; value: number }[] }) {
  const size = 200;
  const radius = size / 2;
  const innerRadius = radius * 0.6;

  const pieGen = pie<{ label: string; value: number }>().value(d => d.value).sort(null);
  const arcGen = arc<PieArcDatum<{ label: string; value: number }>>()
    .innerRadius(innerRadius)
    .outerRadius(radius)
    .cornerRadius(4)
    .padAngle(0.02);

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <g transform={`translate(${radius},${radius})`}>
        {pieGen(data).map((d, i) => (
          <path
            key={d.data.label}
            d={arcGen(d) ?? ''}
            fill={schemeTableau10[i % 10]}
          >
            <title>{`${d.data.label}: ${d.data.value}`}</title>
          </path>
        ))}
      </g>
    </svg>
  );
}
```

### Example 3: Geo/Map Projection

```typescript
import { geoMercator, geoPath, GeoPermissibleObjects } from 'd3';

const projection = geoMercator()
  .center([-98, 39])  // Center on US
  .scale(800)
  .translate([width / 2, height / 2]);

const pathGenerator = geoPath().projection(projection);

// In JSX:
// {geoData.features.map(feature => (
//   <path
//     key={feature.id}
//     d={pathGenerator(feature) ?? ''}
//     fill={colorScale(feature.properties.value)}
//     stroke="#fff"
//     strokeWidth={0.5}
//   />
// ))}
```

## Best Practices

- **Tree-shake imports**: `import { scaleLinear } from 'd3-scale'` not `from 'd3'`
- **Memoize generators**: Wrap `useMemo` around scale/line/arc generators that depend on data/dimensions
- **Accessibility**: Add `role="img"`, `aria-label`, `<title>` on SVG, `<desc>` for complex charts
- **Color**: Use `d3-scale-chromatic` for perceptually uniform palettes; test with colorblindness simulators
- **Performance**: For >10K elements, use Canvas (`d3` can compute positions, draw to `<canvas>` instead of SVG)
