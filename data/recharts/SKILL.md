---
name: recharts
description: Recharts for React data visualization. Covers line, bar, area, pie charts with responsive containers and customization. Triggers on recharts, chart, LineChart, BarChart.
triggers: ["recharts", "chart", "LineChart", "BarChart", "AreaChart", "PieChart", "ResponsiveContainer"]
---

<objective>
Build data visualizations using Recharts - a composable React charting library built on D3. Create responsive, interactive charts with minimal code.
</objective>

<mcp_first>
**CRITICAL: Fetch Recharts documentation before implementing.**

```
MCPSearch({ query: "select:mcp__plugin_devtools_octocode__githubSearchCode" })
```

```typescript
// Recharts component patterns
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["LineChart", "XAxis", "YAxis", "Tooltip"],
  owner: "recharts",
  repo: "recharts",
  path: "src/chart",
  mainResearchGoal: "Understand Recharts component structure",
  researchGoal: "Find chart composition patterns",
  reasoning: "Need current API for chart components"
})

// ResponsiveContainer
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["ResponsiveContainer", "width", "height"],
  owner: "recharts",
  repo: "recharts",
  path: "src/component",
  mainResearchGoal: "Understand responsive charts",
  researchGoal: "Find responsive container patterns",
  reasoning: "Need current API for responsive charts"
})
```
</mcp_first>

<quick_start>
**Line chart:**

```tsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { month: "Jan", sales: 4000, profit: 2400 },
  { month: "Feb", sales: 3000, profit: 1398 },
  { month: "Mar", sales: 2000, profit: 9800 },
];

function SalesChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="sales" stroke="#8884d8" />
        <Line type="monotone" dataKey="profit" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

**Bar chart:**

```tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function RevenueChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

**Area chart:**

```tsx
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function TrendChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#8884d8"
          fill="#8884d8"
          fillOpacity={0.3}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

**Pie chart:**

```tsx
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

function DistributionChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
          label
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}
```
</quick_start>

<chart_types>
| Component | Use Case |
|-----------|----------|
| `LineChart` | Trends over time |
| `BarChart` | Comparisons |
| `AreaChart` | Volume/cumulative data |
| `PieChart` | Part-to-whole |
| `ScatterChart` | Correlations |
| `RadarChart` | Multi-dimensional comparisons |
| `ComposedChart` | Mixed chart types |
</chart_types>

<customization>
**Custom tooltip:**

```tsx
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null;

  return (
    <div className="bg-white p-2 border rounded shadow">
      <p className="font-bold">{label}</p>
      {payload.map((entry) => (
        <p key={entry.name} style={{ color: entry.color }}>
          {entry.name}: {entry.value}
        </p>
      ))}
    </div>
  );
};

<Tooltip content={<CustomTooltip />} />
```

**Custom axis tick:**

```tsx
const CustomTick = ({ x, y, payload }) => (
  <g transform={`translate(${x},${y})`}>
    <text textAnchor="middle" dy={16}>
      {formatDate(payload.value)}
    </text>
  </g>
);

<XAxis tick={<CustomTick />} />
```
</customization>

<constraints>
**Required:**
- Always wrap in `ResponsiveContainer` for responsive sizing
- Provide `width` and `height` to ResponsiveContainer
- Use `dataKey` to map data fields

**Performance:**
- Limit data points for large datasets
- Use `isAnimationActive={false}` for static charts
- Consider virtualization for very large datasets
</constraints>

<success_criteria>
- [ ] Chart wrapped in ResponsiveContainer
- [ ] Proper axes with labels
- [ ] Tooltip for interactivity
- [ ] Appropriate chart type for data
- [ ] Accessible colors (sufficient contrast)
</success_criteria>
