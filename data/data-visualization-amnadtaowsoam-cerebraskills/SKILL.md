---
name: Data Visualization
description: Creating effective data visualizations using charts, graphs, and visual representations to communicate insights clearly and accurately following Tufte and Few principles.
---

# Data Visualization

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Data Science

---

## Overview

Data visualization transforms data into visual representations that make insights clear and actionable. Effective data visualization follows principles of clarity, accuracy, and simplicity to help users understand complex data quickly.

## Data Visualization Principles

### Edward Tufte's Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Show the data** | Let data speak for itself | Don't hide behind decoration |
| **Maximize data-ink ratio** | Remove non-data ink | Eliminate chart junk |
| **Integrate text and graphics** | Labels near data | Direct labeling, not legends |
| **Avoid distortion** | Accurate representation | Start Y-axis at zero |
| **Small multiples** | Compare many charts | Side-by-side comparison |

### Stephen Few's Principles

| Principle | Description |
|-----------|-------------|
| **Simplicity** | Remove unnecessary elements |
| **Clarity** | Make message obvious |
| **Accuracy** | Represent data truthfully |
| **Efficiency** | Convey information quickly |
| **Aesthetics** | Pleasing but not distracting |

### Data-Ink Ratio

```
Data-Ink Ratio = Data-Ink / Total Ink
```

**Goal**: Maximize ratio (close to 1)

**Bad**: Lots of decoration, 3D effects, shadows
**Good**: Clean, minimal, data-focused

## Chart Types and Use Cases

### Comprehensive Chart Guide

| Chart Type | Best For | Data Type | Example |
|------------|----------|------------|---------|
| **Line Chart** | Trends over time | Continuous | Revenue over months |
| **Bar Chart** | Compare categories | Categorical | Sales by region |
| **Column Chart** | Compare categories (vertical) | Categorical | Sales by product |
| **Pie Chart** | Parts of whole (max 5) | Categorical | Market share |
| **Donut Chart** | Parts of whole (modern) | Categorical | Budget breakdown |
| **Area Chart** | Cumulative over time | Continuous | Total users over time |
| **Scatter Plot** | Correlation | Two continuous | Price vs. quantity |
| **Bubble Chart** | Three dimensions | Two continuous + size | Sales vs. profit vs. volume |
| **Heatmap** | Two dimensions | Categorical × Categorical | Sales by region × month |
| **Treemap** | Hierarchical parts | Hierarchical | Budget by department |
| **Histogram** | Distribution | Continuous | Order value distribution |
| **Box Plot** | Distribution + outliers | Continuous | Salary distribution |
| **Violin Plot** | Distribution shape | Continuous | Response time distribution |
| **Radar Chart** | Multi-variable comparison | Multiple | Skills assessment |
| **Gauge Chart** | Single metric vs. target | Single | Progress to goal |
| **Funnel Chart** | Process stages | Sequential | Conversion funnel |
| **Sankey Diagram** | Flow between stages | Sequential | User journey |
| **Waterfall Chart** | Cumulative changes | Sequential | Revenue breakdown |
| **Sparkline** | Mini trend | Time series | Stock price trend |

### Line Chart

**Use for**: Time series, trends

```
Revenue ($)
$100k ┤
 $80k ┤  ●───●───●───●───●
 $60k ┤
 $40k ┤
 $20k ┤
   $0 └────────────────────────────
        Jan  Feb  Mar  Apr  May
```

**Best practices**:
- Smooth curves for trends
- Don't connect unrelated points
- Use area charts for cumulative
- Max 5-7 lines

### Bar Chart

**Use for**: Category comparison

```
Sales by Region
North America  ████████████████████████████████████████  $50M
Europe         ████████████████████████████              $35M
Asia           ████████████████████                      $25M
Other          ████████████                              $10M
               0    10M   20M   30M   40M   50M
```

**Best practices**:
- Horizontal bars for many categories
- Sort by value (not alphabetically)
- Start Y-axis at zero
- Use consistent bar widths

### Pie/Donut Chart

**Use for**: Parts of whole (max 5 slices)

```
Market Share
Product A  ████████████████████████████████████████  50%
Product B  ████████████████████                      25%
Product C  ████████████████████                      25%
```

**Best practices**:
- Max 5 slices
- Use donut for modern look
- Consider bar chart instead
- Order slices by size

### Scatter Plot

**Use for**: Correlation between two variables

```
Quantity
100 ┤     ●
     │   ●   ●
 50 ┤ ●   ●   ●
     │ ●   ●   ●
  0 └────────────────────
     0   50  100  150
          Price
```

**Best practices**:
- Add trend line
- Color by category
- Identify outliers
- Use transparency for overlapping points

### Heatmap

**Use for**: Two-dimensional data

```
Sales by Region × Month
         Jan   Feb   Mar   Apr
US      ■■■■■ ■■■■■ ■■■■■ ■■■■■
EU      ■■■■  ■■■■  ■■■■  ■■■■
Asia    ■■■   ■■■   ■■■   ■■■
```

**Best practices**:
- Use color scale
- Include legend
- Label both axes
- Consider diverging colors for +/- data

### Histogram

**Use for**: Distribution of continuous data

```
Order Value Distribution
$0-10    ████████████████████████████████████████  100
$10-20   ████████████████████████████              80
$20-30   ████████████████████                      60
$30-40   ████████████                              40
$40-50   ██████████                                20
$50+     ██████                                    10
```

**Best practices**:
- Choose appropriate bin size
- Show normal distribution if applicable
- Label axes clearly
- Consider density plot for smooth curves

### Box Plot

**Use for**: Distribution with outliers

```
Salary Distribution
┌─────────────────────────────────────┐
│          ┌───┐                   │
│          │   │                   │
│      ┌───┤   ├───┐               │
│      │   │   │   │               │
│      │   │   │   │               │
│      └───┴───┴───┘               │
└─────────────────────────────────────┘
 Min  Q1  Med  Q3   Max
```

**Best practices**:
- Show outliers as points
- Compare multiple box plots
- Label quartiles
- Use for skewed distributions

## Color Theory

### Color Palettes

#### Sequential (Ordered Data)

Use for continuous, ordered data.

```
Viridis: #440154 → #3b528b → #21918c → #5ec962 → #fde725
Blues:   #f7fbff → #deebf7 → #c6dbef → #9ecae1 → #6baed6
Greens:  #f7fcf5 → #e5f5e0 → #c7e9c0 → #a1d99b → #74c476
```

#### Diverging (Deviation from Center)

Use for data with meaningful midpoint.

```
RdYlGn: #a50026 → #d73027 → #f46d43 → #fdae61 → #fee08b
         → #d9ef8b → #a6d96a → #66bd63 → #1a9850 → #006837
```

#### Qualitative (Categorical)

Use for distinct categories.

```
Set1: #e41a1c, #377eb8, #4daf4a, #984ea3, #ff7f00
Set2: #66c2a5, #fc8d62, #8da0cb, #e78ac3, #a6d854
```

### Semantic Colors

| Color | Meaning | Use Case |
|-------|---------|----------|
| **Green** | Positive, good | Above target, growth |
| **Red** | Negative, bad | Below target, decline |
| **Yellow/Orange** | Warning | Near threshold |
| **Blue** | Neutral, information | Default state |
| **Gray** | Inactive, placeholder | Disabled elements |

### Colorblind-Friendly Design

**Tips**:
- Avoid red-green only
- Use patterns + color
- Test with colorblind simulators
- Use diverging palettes

**Safe Palettes**:
- Viridis (colorblind-safe)
- ColorBrewer (designed for accessibility)
- Okabe-Ito (8 colorblind-safe colors)

## Visual Perception

### Preattentive Attributes

Attributes processed instantly (before conscious thought).

| Attribute | Speed | Example |
|------------|--------|---------|
| **Color** | Fast | Highlighting important data |
| **Size** | Fast | Larger = more important |
| **Orientation** | Fast | Angles, lines |
| **Motion** | Very fast | Animations |
| **Position** | Fast | Top-left = primary |

### Ranking of Visual Attributes

From most to least accurate for quantitative data:

1. **Position** (most accurate)
2. Length
3. Angle
4. Direction
5. Area
6. Volume
7. Color saturation
8. Color hue (least accurate)

**Implication**: Use position/length for precise values, color for categories.

### Gestalt Principles

| Principle | Description | Application |
|------------|-------------|--------------|
| **Proximity** | Near items grouped together | Group related charts |
| **Similarity** | Similar items grouped | Use consistent colors |
| **Continuity** | Eye follows lines | Use flow in layouts |
| **Closure** | Complete incomplete shapes | Don't over-complete |
| **Figure-Ground** | Separate foreground/background | Use white space |

## Chart Design Best Practices

### 1. Direct Labeling

**Bad** (legend):
```
[Chart]
Legend: Blue = A, Red = B, Green = C
```

**Good** (direct labels):
```
[Chart with labels on chart]
  Series A ●───●───●
  Series B ●───●───●
  Series C ●───●───●
```

### 2. Start Y-Axis at Zero

**Bad** (truncated):
```
$100k ┤  ●
 $98k ┤
 $96k ┤  ●
 $94k ┤
       └────────
```

**Good** (starts at zero):
```
$100k ┤  ●
 $50k ┤
   $0 ┤  ●
       └────────
```

**Exception**: When zero is not meaningful (e.g., temperature)

### 3. Sort by Value

**Bad** (alphabetical):
```
Zebra    ████████
Apple    ████████████████
Banana   ████████████
```

**Good** (by value):
```
Apple    ████████████████
Banana   ████████████
Zebra    ████████
```

### 4. Remove Chart Junk

**Bad** (cluttered):
```
[Chart with grid, borders, 3D effects, shadows, gradients]
```

**Good** (clean):
```
[Clean chart with minimal decoration]
```

### 5. Use Consistent Scales

**Bad** (different scales):
```
Chart A: 0-100
Chart B: 0-1000
```

**Good** (consistent scales):
```
Chart A: 0-100
Chart B: 0-100 (normalized)
```

## Interactive Visualizations

### Interactive Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Tooltips** | Hover for details | Show exact values |
| **Zoom** | Zoom into data | Explore details |
| **Pan** | Move around zoomed data | Navigate |
| **Filter** | Filter data | Focus on subset |
| **Highlight** | Highlight selection | Compare |
| **Brush** | Select range | Time range selection |
| **Click** | Click for drill-down | Navigate hierarchy |

### Tooltip Design

**Good tooltip**:
```
┌─────────────────────────────────────┐
│  January 2024                     │
│  ───────────────────────────────  │
│  Revenue: $1,234,567             │
│  Orders: 1,234                   │
│  AOV: $1,000                     │
│  ▲ 12.3% vs previous month       │
└─────────────────────────────────────┘
```

### Zoom and Pan

```
Before zoom:
┌─────────────────────────────────────┐
│  ●───●───●───●───●───●───●───●  │  ← Full view
└─────────────────────────────────────┘

After zoom:
┌─────────────────────────────────────┐
│           ●───●───●              │  ← Zoomed in
└─────────────────────────────────────┘
```

## Accessibility

### WCAG Guidelines

| Guideline | Requirement |
|------------|-------------|
| **Color contrast** | 4.5:1 for text, 3:1 for large text |
| **Color independence** | Don't rely on color alone |
| **Keyboard navigation** | All features accessible via keyboard |
| **Screen reader support** | Provide alt text, ARIA labels |
| **Focus indicators** | Visible focus state |

### Color Contrast Checker

**Good contrast** (7:1):
```
Black text on white background
#000000 on #FFFFFF
```

**Poor contrast** (1.5:1):
```
Light gray on white background
#CCCCCC on #FFFFFF
```

### Color Independence

**Bad** (color only):
```
Red = Negative, Green = Positive
```

**Good** (color + pattern/icon):
```
Red ↓ = Negative, Green ↑ = Positive
```

### Alt Text for Charts

**Example**:
```html
<figure>
  <img src="revenue-chart.png" alt="Line chart showing revenue
  increasing from $1M in January to $1.5M in June, with a
  12% month-over-month growth rate.">
  <figcaption>Revenue Growth Q1-Q2 2024</figcaption>
</figure>
```

## Tools

### JavaScript Libraries

| Library | Strengths | Learning Curve |
|----------|-----------|---------------|
| **D3.js** | Most flexible, powerful | Steep |
| **Plotly** | Easy, interactive | Gentle |
| **Chart.js** | Simple, popular | Gentle |
| **Recharts** | React-friendly | Gentle |
| **Victory** | React, declarative | Gentle |
| **Nivo** | React, beautiful | Gentle |

### Python Libraries

| Library | Strengths | Use Case |
|----------|-----------|----------|
| **Matplotlib** | Foundation, flexible | All-purpose |
| **Seaborn** | Statistical plots | Data analysis |
| **Plotly** | Interactive | Web dashboards |
| **Altair** | Declarative grammar | Statistical |
| **Bokeh** | Interactive | Web apps |

### R Libraries

| Library | Strengths | Use Case |
|----------|-----------|----------|
| **ggplot2** | Grammar of graphics | All-purpose |
| **plotly** | Interactive | Web dashboards |
| **lattice** | Trellis displays | Multi-panel |

### BI Tools

| Tool | Strengths |
|------|-----------|
| **Tableau** | Powerful visualizations |
| **Looker** | SQL-based, embedded |
| **Power BI** | Microsoft ecosystem |
| **Metabase** | Open-source, simple |

## Common Mistakes

### 1. 3D Charts

**Problem**: 3D distorts data perception.

**Bad**:
```
[3D bar chart with perspective]
```

**Good**:
```
[2D bar chart, flat]
```

### 2. Truncated Y-Axis

**Problem**: Exaggerates differences.

**Bad**:
```
$100k ┤  ●
 $98k ┤
 $96k ┤  ●
```

**Good**:
```
$100k ┤  ●
   $0 ┤  ●
```

### 3. Too Many Colors

**Problem**: Confusing, hard to distinguish.

**Bad**: 10+ colors
**Good**: 3-5 colors max

### 4. Pie Charts with Many Slices

**Problem**: Hard to compare.

**Bad**: 10+ slices
**Good**: Max 5 slices, use bar chart instead

### 5. Missing Context

**Problem**: Numbers without meaning.

**Bad**: "Revenue: $1.2M"
**Good**: "Revenue: $1.2M ▲ 12% vs last month"

### 6. Rainbow Colors

**Problem**: No meaning, hard to read.

**Bad**: Random colors
**Good**: Semantic colors (red=bad, green=good)

### 7. Small Fonts

**Problem**: Hard to read.

**Bad**: 10px font
**Good**: 12px+ font

## Mobile-Responsive Charts

### Responsive Design

**Desktop**: Wide charts, side-by-side
**Mobile**: Narrow charts, stacked

```
Desktop:          Mobile:
┌─────┬─────┐    ┌─────┐
│  A  │  B  │    │  A  │
├─────┼─────┤    ├─────┤
│  C  │  D  │    │  B  │
└─────┴─────┘    ├─────┤
                 │  C  │
                 ├─────┤
                 │  D  │
                 └─────┘
```

### Touch-Friendly

- Minimum tap target: 44×44px
- Large touch areas
- Swipe gestures

### Performance

- Optimize images
- Lazy load charts
- Use canvas for many points

## Animation and Transitions

### Animation Principles

| Principle | Description |
|-----------|-------------|
| **Purposeful** | Animation should have purpose |
| **Smooth** | 60fps, no jank |
| **Subtle** | Don't distract |
| **Fast** | < 500ms for transitions |

### Transition Types

| Type | Use Case |
|------|----------|
| **Fade** | Show/hide elements |
| **Slide** | Move between states |
| **Scale** | Emphasize elements |
| **Rotate** | Draw attention |

### Example: D3.js Animation

```javascript
// Smooth transition
d3.select('.bar')
  .transition()
  .duration(500)
  .attr('height', newHeight);
```

## Implementation Examples

### Chart.js Example

```javascript
import Chart from 'chart.js/auto';

const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [{
      label: 'Revenue',
      data: [100, 120, 115, 134, 168],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `$${context.parsed.y}K`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return `$${value}K`;
          }
        }
      }
    }
  }
});
```

### D3.js Example

```javascript
import * as d3 from 'd3';

const data = [
  { month: 'Jan', value: 100 },
  { month: 'Feb', value: 120 },
  { month: 'Mar', value: 115 },
  { month: 'Apr', value: 134 },
  { month: 'May', value: 168 }
];

const margin = {top: 20, right: 30, bottom: 40, left: 50};
const width = 800 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

const svg = d3.select('#chart')
  .append('svg')
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);

const x = d3.scaleBand()
  .domain(data.map(d => d.month))
  .range([0, width])
  .padding(0.2);

const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([height, 0]);

svg.append('g')
  .attr('transform', `translate(0,${height})`)
  .call(d3.axisBottom(x));

svg.append('g')
  .call(d3.axisLeft(y));

svg.selectAll('.bar')
  .data(data)
  .enter()
  .append('rect')
  .attr('class', 'bar')
  .attr('x', d => x(d.month))
  .attr('width', x.bandwidth())
  .attr('y', height)
  .attr('height', 0)
  .transition()
  .duration(500)
  .attr('y', d => y(d.value))
  .attr('height', d => height - y(d.value))
  .attr('fill', '#4daf4a');
```

### Plotly Example (Python)

```python
import plotly.express as px
import pandas as pd

data = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'revenue': [100, 120, 115, 134, 168]
})

fig = px.line(
    data,
    x='month',
    y='revenue',
    title='Revenue Trend',
    labels={'revenue': 'Revenue ($K)', 'month': 'Month'},
    markers=True
)

fig.update_layout(
    yaxis_range=[0, 200],
    hovermode='x unified'
)

fig.update_traces(
    line=dict(width=3, color='#4daf4a'),
    marker=dict(size=8)
)

fig.show()
```

### Seaborn Example (Python)

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    'region': ['North', 'South', 'East', 'West'],
    'sales': [50, 35, 25, 10]
})

plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=data,
    x='sales',
    y='region',
    palette='viridis'
)

ax.set_xlabel('Sales ($M)')
ax.set_ylabel('Region')
ax.set_title('Sales by Region')

# Add value labels
for i, v in enumerate(data['sales']):
    ax.text(v + 1, i, f'${v}M', va='center')

plt.tight_layout()
plt.show()
```

## Summary Checklist

### Before Creating Visualization

- [ ] Understand audience and goal
- [ ] Choose appropriate chart type
- [ ] Select color palette
- [ ] Plan layout
- [ ] Consider accessibility

### During Creation

- [ ] Use direct labeling
- [ ] Start Y-axis at zero (if appropriate)
- [ ] Sort by value
- [ ] Remove chart junk
- [ ] Add context
```

---

## Quick Start

### Basic Chart with Chart.js

```javascript
import { Chart } from 'chart.js'

const ctx = document.getElementById('myChart')
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [{
      label: 'Revenue',
      data: [1000, 1200, 1100, 1300],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
})
```

### D3.js Basic Bar Chart

```javascript
import * as d3 from 'd3'

const data = [10, 20, 30, 40, 50]
const svg = d3.select('body').append('svg')
  .attr('width', 400)
  .attr('height', 300)

svg.selectAll('rect')
  .data(data)
  .enter()
  .append('rect')
  .attr('x', (d, i) => i * 50)
  .attr('y', d => 300 - d * 5)
  .attr('width', 40)
  .attr('height', d => d * 5)
```

---

## Production Checklist

- [ ] **Chart Selection**: Choose appropriate chart type for data
- [ ] **Data Accuracy**: Ensure data is accurate and up-to-date
- [ ] **Accessibility**: Charts accessible to screen readers
- [ ] **Responsive**: Charts work on all screen sizes
- [ ] **Performance**: Charts render efficiently with large datasets
- [ ] **Color**: Use color-blind friendly palettes
- [ ] **Labels**: Clear labels and legends
- [ ] **Context**: Provide context and explanations
- [ ] **Interactivity**: Add tooltips and interactions where helpful
- [ ] **Testing**: Test with real data
- [ ] **Documentation**: Document chart purpose and data source
- [ ] **Updates**: Keep charts current with data changes

---

## Anti-patterns

### ❌ Don't: Misleading Y-Axis

```javascript
// ❌ Bad - Y-axis doesn't start at zero
chart.options.scales.y.min = 90  // Misleading!
```

```javascript
// ✅ Good - Y-axis starts at zero
chart.options.scales.y.min = 0  // Accurate representation
```

### ❌ Don't: Chart Junk

```javascript
// ❌ Bad - Too many decorations
chart.options.plugins.legend.display = true
chart.options.plugins.title.display = true
chart.options.plugins.annotation = { /* decorations */ }
// Too much!
```

```javascript
// ✅ Good - Clean, focused
chart.options.plugins.legend.display = true  // Only if needed
// Remove unnecessary decorations
```

### ❌ Don't: Wrong Chart Type

```javascript
// ❌ Bad - Line chart for categories
type: 'line'  // Categories don't have trends
```

```javascript
// ✅ Good - Bar chart for categories
type: 'bar'  // Better for comparing categories
```

---

## Integration Points

- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Dashboard layouts
- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Metric visualization
- **SQL for Analytics** (`23-business-analytics/sql-for-analytics/`) - Data queries

---

## Further Reading

- [Edward Tufte's Books](https://www.edwardtufte.com/tufte/)
- [D3.js Documentation](https://d3js.org/)
- [Chart.js Documentation](https://www.chartjs.org/)

### After Creation

- [ ] Test for accessibility
- [ ] Verify on mobile
- [ ] Check color contrast
- [ ] Get feedback
- [ ] Iterate based on feedback
