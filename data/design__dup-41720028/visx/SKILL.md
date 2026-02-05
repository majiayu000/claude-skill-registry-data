---
name: visx
description: Build data visualizations with visx (React + D3). Use for charts, graphs, and interactive data exploration.
---

# visx

Build data visualizations with React using visx (Airbnb's React + D3 library).

## Status: Starter

Patterns will evolve with use.

## When to Use

- Custom charts beyond basic chart libraries
- Interactive data exploration
- Dashboards with specific design requirements
- When you need D3 power with React patterns

## Why visx over other options

| Library | Good for |
|---------|----------|
| visx | Custom, interactive, design-specific charts |
| Recharts | Quick standard charts |
| Chart.js | Simple, canvas-based |
| D3 direct | Maximum control, non-React |

visx = D3 primitives as React components. Full control, React-friendly.

## Setup

```bash
# Core
pnpm add @visx/group @visx/scale @visx/shape @visx/axis @visx/grid

# Common additions
pnpm add @visx/tooltip @visx/responsive @visx/gradient @visx/curve

# All of visx (larger bundle)
pnpm add @visx/visx
```

## Basic Patterns

### Line Chart

```tsx
import { LinePath } from '@visx/shape'
import { scaleLinear, scaleTime } from '@visx/scale'
import { AxisBottom, AxisLeft } from '@visx/axis'
import { Group } from '@visx/group'

interface DataPoint {
  date: Date
  value: number
}

const data: DataPoint[] = [
  { date: new Date('2024-01'), value: 10 },
  { date: new Date('2024-02'), value: 25 },
  { date: new Date('2024-03'), value: 15 },
]

const width = 600
const height = 400
const margin = { top: 20, right: 20, bottom: 40, left: 40 }

const innerWidth = width - margin.left - margin.right
const innerHeight = height - margin.top - margin.bottom

const xScale = scaleTime({
  domain: [Math.min(...data.map(d => d.date)), Math.max(...data.map(d => d.date))],
  range: [0, innerWidth],
})

const yScale = scaleLinear({
  domain: [0, Math.max(...data.map(d => d.value))],
  range: [innerHeight, 0],
})

export function LineChart() {
  return (
    <svg width={width} height={height}>
      <Group left={margin.left} top={margin.top}>
        <AxisBottom scale={xScale} top={innerHeight} />
        <AxisLeft scale={yScale} />
        <LinePath
          data={data}
          x={d => xScale(d.date)}
          y={d => yScale(d.value)}
          stroke="currentColor"
          strokeWidth={2}
        />
      </Group>
    </svg>
  )
}
```

### Bar Chart

```tsx
import { Bar } from '@visx/shape'
import { scaleBand, scaleLinear } from '@visx/scale'
import { Group } from '@visx/group'

interface DataPoint {
  label: string
  value: number
}

const data: DataPoint[] = [
  { label: 'A', value: 30 },
  { label: 'B', value: 80 },
  { label: 'C', value: 45 },
]

const xScale = scaleBand({
  domain: data.map(d => d.label),
  range: [0, innerWidth],
  padding: 0.2,
})

const yScale = scaleLinear({
  domain: [0, Math.max(...data.map(d => d.value))],
  range: [innerHeight, 0],
})

export function BarChart() {
  return (
    <svg width={width} height={height}>
      <Group left={margin.left} top={margin.top}>
        {data.map(d => (
          <Bar
            key={d.label}
            x={xScale(d.label)}
            y={yScale(d.value)}
            width={xScale.bandwidth()}
            height={innerHeight - yScale(d.value)}
            fill="currentColor"
          />
        ))}
      </Group>
    </svg>
  )
}
```

### Responsive Container

```tsx
import { ParentSize } from '@visx/responsive'

export function ResponsiveChart() {
  return (
    <ParentSize>
      {({ width, height }) => (
        <LineChart width={width} height={height} />
      )}
    </ParentSize>
  )
}
```

### Tooltip

```tsx
import { useTooltip, TooltipWithBounds } from '@visx/tooltip'
import { localPoint } from '@visx/event'

const { showTooltip, hideTooltip, tooltipData, tooltipLeft, tooltipTop } = useTooltip()

// In your component:
<circle
  onMouseMove={(event) => {
    const point = localPoint(event)
    showTooltip({
      tooltipData: dataPoint,
      tooltipLeft: point.x,
      tooltipTop: point.y,
    })
  }}
  onMouseLeave={hideTooltip}
/>

{tooltipData && (
  <TooltipWithBounds left={tooltipLeft} top={tooltipTop}>
    {tooltipData.value}
  </TooltipWithBounds>
)}
```

## Styling with Tailwind

visx renders SVG - style with className or inline styles:

```tsx
<LinePath
  stroke="hsl(var(--primary))"
  className="transition-all duration-200"
/>
```

## Reference

- visx docs: https://airbnb.io/visx/
- visx gallery: https://airbnb.io/visx/gallery
- D3 scales: https://github.com/d3/d3-scale

## TODO

- [ ] First real chart to establish patterns
- [ ] Add area chart pattern
- [ ] Add pie/donut pattern
- [ ] Add animation patterns
- [ ] Integrate with tRPC data fetching
