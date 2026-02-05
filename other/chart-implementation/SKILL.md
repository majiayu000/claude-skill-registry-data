---
name: chart-implementation
description: Create interactive charts for car registration and COE data visualization using Recharts. Use when adding new chart types, fixing chart bugs, or implementing data visualizations.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Chart Implementation Skill

Uses **Recharts** for data visualization. Always use CSS variables for colors (see `design-language-system` skill).

## Common Chart Types

### Line Chart

```typescript
"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export function TrendChart({ data }: { data: { month: string; value: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="var(--chart-1)" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Bar Chart

```typescript
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export function TopMakesChart({ data }: { data: { make: string; count: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="make" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="var(--chart-1)" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

### Multi-Line Chart (COE Categories)

```typescript
export function COETrends({ data }: { data: any[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="biddingNo" />
        <YAxis />
        <Tooltip formatter={(value) => `$${Number(value).toLocaleString()}`} />
        <Line dataKey="catA" stroke="var(--chart-1)" name="Cat A" />
        <Line dataKey="catB" stroke="var(--chart-2)" name="Cat B" />
        <Line dataKey="catC" stroke="var(--chart-3)" name="Cat C" />
        <Line dataKey="catE" stroke="var(--chart-4)" name="Cat E" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Pie Chart

```typescript
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

export function MarketShareChart({ data }: { data: { name: string; value: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart>
        <Pie data={data} dataKey="value" cx="50%" cy="50%" outerRadius={120}>
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={`var(--chart-${index + 1})`} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

## Custom Tooltip

```typescript
import { TooltipProps } from "recharts";

function CustomTooltip({ active, payload, label }: TooltipProps<number, string>) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-white p-4 rounded-lg shadow-lg border">
      <p className="font-semibold">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }}>{entry.name}: {entry.value?.toLocaleString()}</p>
      ))}
    </div>
  );
}
```

## Performance

### Lazy Load Charts

```typescript
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("./chart"), {
  ssr: false,
  loading: () => <div>Loading chart...</div>,
});
```

### Memoize Data

```typescript
const chartData = useMemo(() => transformData(rawData), [rawData]);
```

## Common Issues

### Chart Not Rendering

Ensure parent has explicit height:

```tsx
// ❌ Wrong
<ResponsiveContainer width="100%" height={400}>

// ✅ Correct - parent with height
<div className="h-[400px]">
  <ResponsiveContainer width="100%" height="100%">
```

### SSR Errors

Use dynamic import with `ssr: false`:

```typescript
const Chart = dynamic(() => import("./chart"), { ssr: false });
```

## Best Practices

1. **ResponsiveContainer** - Always wrap charts
2. **CSS Variables** - Use `var(--chart-N)` for colors
3. **Lazy Load** - Dynamic import with `ssr: false`
4. **Memoize** - Use useMemo for data transformations
5. **Tooltips** - Provide formatted, detailed tooltips
6. **Mobile** - Test on small screens

## References

- Recharts: Use Context7 for latest docs
- Design Language System: See `design-language-system` skill for colors
