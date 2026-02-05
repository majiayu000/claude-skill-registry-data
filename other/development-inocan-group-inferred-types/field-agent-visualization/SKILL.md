---
name: field-agent-visualization
description: Professional Plotly visualization best practices for Field Agents including chart specifications, color palettes, formatting standards, and JSON structure requirements for executive-ready data visualizations
---

# Field Agent Visualization Best Practices

This skill provides comprehensive guidelines for creating professional, executive-ready visualizations for Field Agents using Plotly. Follow these standards to ensure clean, readable, and impactful data visualizations.

## When to Use This Skill

Use this skill when you need to:
- Create Plotly visualizations for Field Agent outputs
- Generate charts for data analysis and reporting
- Build dashboards with KPI indicators
- Design executive-ready visual presentations
- Ensure consistent visualization standards across agents

## Core Principles

### Golden Rules
1. **Create SINGLE CHARTS ONLY** - NO SUBPLOTS for analysis charts
2. **Always use descriptive titles, axis labels, and legends**
3. **Ensure proper formatting and readability**
4. **Use the specified color palette consistently**
5. **Always show numbers/percentages in bar charts and heatmaps**
6. **LEGENDS MUST BE VISIBLE** for pie charts and comparison charts
7. **NEVER CREATE SUBPLOTS** for analysis - Always create separate individual charts

## MANDATORY Color Palette

Always use this Treasure Data color palette for consistency:

```python
TD_COLORS = [
    '#44BAB8',  # Teal (Primary)
    '#8FD6D4',  # Light Teal
    '#DAF1F1',  # Pale Teal
    '#2E41A6',  # Navy Blue
    '#828DCA',  # Purple
    '#D5D9ED',  # Light Purple
    '#8CC97E',  # Green
    '#BADFB2',  # Light Green
    '#E8F4E5',  # Pale Green
    '#EEB53A',  # Accent Yellow
    '#F5D389',  # Light Yellow
    '#5FCFD8',  # Cyan
    '#A05EB0',  # Magenta
    '#C69ED0'   # Light Magenta
]
```

**Usage:**
- Use `#44BAB8` (Teal) as primary color for single-series charts
- Use `#2E41A6` (Navy) for text and titles
- Cycle through colors for multi-series charts
- Use color scales for heatmaps (DAF1F1 → 8FD6D4 → 44BAB8)

### Color Conversion Helper Function

For charts requiring RGB/RGBA format (e.g., transparency effects):

```python
def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple

    Args:
        hex_color (str): Hex color code (e.g., '#44BAB8' or '44BAB8')

    Returns:
        tuple: RGB values as (R, G, B) where each value is 0-255

    Example:
        >>> hex_to_rgb('#44BAB8')
        (68, 186, 184)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgba(hex_color, alpha=1.0):
    """Convert hex color to RGBA string for Plotly

    Args:
        hex_color (str): Hex color code (e.g., '#44BAB8')
        alpha (float): Opacity value 0.0-1.0

    Returns:
        str: RGBA color string (e.g., 'rgba(68, 186, 184, 0.5)')

    Example:
        >>> hex_to_rgba('#44BAB8', 0.5)
        'rgba(68, 186, 184, 0.5)'
    """
    r, g, b = hex_to_rgb(hex_color)
    return f'rgba({r}, {g}, {b}, {alpha})'

# Usage examples:
td_primary_rgb = hex_to_rgb('#44BAB8')  # (68, 186, 184)
td_primary_transparent = hex_to_rgba('#44BAB8', 0.3)  # 'rgba(68, 186, 184, 0.3)'
```

---

## CRITICAL: JSON Structure Requirements

### ✅ CORRECT JSON Format

Always use proper JSON objects with native arrays and objects:

```json
{
  "data": [
    {
      "type": "bar",
      "x": ["A", "B", "C"],
      "y": [10, 20, 30],
      "marker": {"color": "#44BAB8"},
      "text": ["10", "20", "30"],
      "textposition": "outside",
      "textfont": {"size": 11, "color": "black"}
    }
  ],
  "layout": {
    "title": {
      "text": "Chart Title",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "showlegend": true,
    "margin": {"t": 120, "b": 80, "l": 80, "r": 80},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

### ❌ NEVER DO: String Data (Causes Errors)

```json
{
  "data": "[{\"type\": \"bar\", \"x\": [\"A\", \"B\"], \"y\": [10, 20]}]"
}
```

**Critical**: Data must be JSON objects and arrays, NOT stringified JSON.

---

## CRITICAL: Missing Elements Fixes

### For Bar Charts - MANDATORY Properties

```json
{
  "data": [{
    "type": "bar",
    "x": ["Category A", "Category B", "Category C"],
    "y": [45, 30, 25],
    "name": "Series Name",
    "marker": {"color": "#44BAB8"},
    "text": [45, 30, 25],  // ⚠️ CRITICAL: Must include for numbers on bars
    "textposition": "outside",  // ⚠️ CRITICAL: Shows numbers above bars
    "textfont": {"size": 11, "color": "black"}
  }],
  "layout": {
    "title": {"text": "Bar Chart Title", "x": 0.5, "font": {"size": 18}},
    "height": 500,
    "showlegend": true,  // ⚠️ CRITICAL: Must be true for multi-series
    "legend": {
      "orientation": "h",
      "yanchor": "bottom",
      "y": 1.05,  // ⚠️ CRITICAL: Must be above 1.0 to be visible
      "xanchor": "center",
      "x": 0.5
    },
    "margin": {"t": 120, "b": 80, "l": 80, "r": 80},  // ⚠️ CRITICAL: Extra top margin for legend
    "xaxis": {"title": {"text": "Categories", "font": {"size": 14}}},
    "yaxis": {"title": {"text": "Values", "font": {"size": 14}}},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

### For Heatmaps - MANDATORY Properties

```json
{
  "data": [{
    "type": "heatmap",
    "x": ["Col A", "Col B", "Col C"],
    "y": ["Row 1", "Row 2", "Row 3"],
    "z": [[23.4, 45.6, 12.3], [34.5, 56.7, 23.1], [45.2, 67.8, 34.5]],
    "text": [[23.4, 45.6, 12.3], [34.5, 56.7, 23.1], [45.2, 67.8, 34.5]],  // ⚠️ CRITICAL: Numbers to display
    "texttemplate": "%{text:.1f}",  // ⚠️ CRITICAL: Format to 1 decimal
    "textfont": {"size": 12, "color": "black"},  // ⚠️ CRITICAL: Visible text
    "showscale": true,  // ⚠️ CRITICAL: Show color scale
    "colorscale": [
      [0, "#DAF1F1"],
      [0.5, "#8FD6D4"],
      [1, "#44BAB8"]
    ],
    "colorbar": {
      "title": {"text": "Value", "font": {"size": 12}},
      "titleside": "right"
    },
    "hovertemplate": "<b>%{y}</b> - <b>%{x}</b><br>Value: %{z:.1f}<extra></extra>"
  }],
  "layout": {
    "title": {"text": "Heatmap Title", "x": 0.5, "font": {"size": 18}},
    "height": 500,
    "xaxis": {"title": {"text": "X Axis", "font": {"size": 14}}},
    "yaxis": {"title": {"text": "Y Axis", "font": {"size": 14}}},
    "margin": {"t": 80, "b": 80, "l": 80, "r": 100},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

### Common Issues Fix Checklist

Before generating any chart, verify:

- [ ] **Bar charts**: Include `"text"`, `"textposition": "outside"`, `"textfont"`
- [ ] **Multi-series**: Include `"showlegend": true`, legend `"y": 1.05` or higher
- [ ] **Legend spacing**: Top margin `"t": 120` minimum for horizontal legends
- [ ] **Heatmaps**: Include `"text"`, `"texttemplate": "%{text:.1f}"`, `"showscale": true`
- [ ] **Text visibility**: Use `"textfont": {"color": "black"}` for contrast
- [ ] **JSON format**: Use proper objects/arrays, NOT stringified JSON
- [ ] **Color palette**: Use TD colors exclusively
- [ ] **No subplots**: Create individual charts for analysis

---

## Chart-Specific Guidelines

### 1. Pie Charts - LEGEND MANDATORY

Pie charts **ALWAYS** require visible legends.

```json
{
  "data": [{
    "type": "pie",
    "values": [45, 30, 25],
    "labels": ["Channel A", "Channel B", "Channel C"],
    "marker": {
      "colors": ["#44BAB8", "#8FD6D4", "#DAF1F1"]
    },
    "textinfo": "label+percent",
    "textposition": "auto",
    "textfont": {"size": 14, "color": "black"},
    "hovertemplate": "<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>"
  }],
  "layout": {
    "title": {
      "text": "Attribution Distribution",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "showlegend": true,
    "legend": {
      "orientation": "v",
      "yanchor": "middle",
      "y": 0.5,
      "xanchor": "left",
      "x": 1.02,
      "font": {"size": 12}
    },
    "margin": {"t": 80, "b": 80, "l": 80, "r": 150},
    "font": {"family": "Arial", "size": 12},
    "paper_bgcolor": "white"
  }
}
```

**Key Points:**
- Use vertical legend positioned to the right (`x: 1.02`)
- Include extra right margin (`r: 150`) for legend space
- Show both label and percent in slices
- Use TD color palette for consistent branding

---

### 2. Bar Charts with Comparison - LEGEND VISIBLE

Multi-series bar charts require horizontal legends positioned above the chart.

```json
{
  "data": [
    {
      "type": "bar",
      "x": ["Channel A", "Channel B", "Channel C"],
      "y": [45, 30, 25],
      "name": "Metric 1",
      "marker": {"color": "#44BAB8"},
      "text": [45, 30, 25],
      "textposition": "outside",
      "textfont": {"size": 11, "color": "black"}
    },
    {
      "type": "bar",
      "x": ["Channel A", "Channel B", "Channel C"],
      "y": [35, 40, 30],
      "name": "Metric 2",
      "marker": {"color": "#8FD6D4"},
      "text": [35, 40, 30],
      "textposition": "outside",
      "textfont": {"size": 11, "color": "black"}
    }
  ],
  "layout": {
    "title": {
      "text": "Channel Comparison",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "barmode": "group",
    "showlegend": true,
    "legend": {
      "orientation": "h",
      "yanchor": "bottom",
      "y": 1.05,
      "xanchor": "center",
      "x": 0.5,
      "font": {"size": 12}
    },
    "xaxis": {
      "title": {"text": "Channels", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "yaxis": {
      "title": {"text": "Performance %", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "margin": {"t": 120, "b": 80, "l": 80, "r": 80},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

**Key Points:**
- Set `barmode` to `"group"` for side-by-side or `"stack"` for stacked
- Horizontal legend above chart (`y: 1.05`)
- Adequate top margin (`t: 120`)
- Numbers displayed on all bars

---

### 3. Single Bar Chart - NO Legend Needed

```json
{
  "data": [{
    "type": "bar",
    "x": ["Product A", "Product B", "Product C", "Product D"],
    "y": [1200, 950, 800, 650],
    "marker": {"color": "#44BAB8"},
    "text": ["$1,200", "$950", "$800", "$650"],
    "textposition": "outside",
    "textfont": {"size": 11, "color": "black"}
  }],
  "layout": {
    "title": {
      "text": "Revenue by Product",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "showlegend": false,
    "xaxis": {
      "title": {"text": "Products", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "yaxis": {
      "title": {"text": "Revenue ($)", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "margin": {"t": 80, "b": 80, "l": 80, "r": 80},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

**Key Points:**
- Single series = no legend needed (`showlegend: false`)
- Use primary TD color (#44BAB8)
- Show formatted values on bars

---

### 4. Heatmaps - Numbers with 1 Decimal

```json
{
  "data": [{
    "type": "heatmap",
    "x": ["Channel A", "Channel B", "Channel C"],
    "y": ["Week 1", "Week 2", "Week 3"],
    "z": [
      [23.4, 45.6, 12.3],
      [34.5, 56.7, 23.1],
      [45.2, 67.8, 34.5]
    ],
    "colorscale": [
      [0, "#DAF1F1"],
      [0.5, "#8FD6D4"],
      [1, "#44BAB8"]
    ],
    "showscale": true,
    "colorbar": {
      "title": {"text": "Performance", "font": {"size": 12}},
      "titleside": "right"
    },
    "text": [
      [23.4, 45.6, 12.3],
      [34.5, 56.7, 23.1],
      [45.2, 67.8, 34.5]
    ],
    "texttemplate": "%{text:.1f}",
    "textfont": {"size": 12, "color": "black"},
    "hovertemplate": "<b>%{y}</b> - <b>%{x}</b><br>Value: %{z:.1f}<extra></extra>"
  }],
  "layout": {
    "title": {
      "text": "Performance Heatmap",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "xaxis": {
      "title": {"text": "Channels", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "yaxis": {
      "title": {"text": "Time Periods", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "margin": {"t": 80, "b": 80, "l": 80, "r": 100},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

**Key Points:**
- Include `text` array matching `z` values
- Use `texttemplate: "%{text:.1f}"` for 1 decimal formatting
- Use TD color scale (light to dark)
- Show color scale bar

---

### 5. Line Charts with Multiple Series

```json
{
  "data": [
    {
      "type": "scatter",
      "mode": "lines+markers",
      "x": ["Jan", "Feb", "Mar", "Apr"],
      "y": [10, 15, 20, 25],
      "name": "Channel A",
      "line": {"color": "#44BAB8", "width": 3},
      "marker": {"color": "#44BAB8", "size": 8}
    },
    {
      "type": "scatter",
      "mode": "lines+markers",
      "x": ["Jan", "Feb", "Mar", "Apr"],
      "y": [8, 12, 18, 22],
      "name": "Channel B",
      "line": {"color": "#8FD6D4", "width": 3},
      "marker": {"color": "#8FD6D4", "size": 8}
    }
  ],
  "layout": {
    "title": {
      "text": "Performance Trends",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "showlegend": true,
    "legend": {
      "orientation": "h",
      "yanchor": "bottom",
      "y": 1.02,
      "xanchor": "center",
      "x": 0.5,
      "font": {"size": 12}
    },
    "xaxis": {
      "title": {"text": "Time Period", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "yaxis": {
      "title": {"text": "Performance", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "margin": {"t": 100, "b": 80, "l": 80, "r": 80},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

**Key Points:**
- Use `scatter` type with `mode: "lines+markers"`
- Different colors for each series from TD palette
- Horizontal legend above chart
- Visible markers on data points

---

### 6. Sankey Diagrams

```json
{
  "data": [{
    "type": "sankey",
    "orientation": "h",
    "node": {
      "pad": 15,
      "thickness": 30,
      "line": {"color": "black", "width": 0.5},
      "label": ["Source A", "Source B", "Destination X", "Destination Y"],
      "color": ["#44BAB8", "#8FD6D4", "#2E41A6", "#828DCA"]
    },
    "link": {
      "source": [0, 1, 0, 1],
      "target": [2, 2, 3, 3],
      "value": [10, 20, 15, 25],
      "color": [
        "rgba(68, 186, 184, 0.4)",
        "rgba(143, 214, 212, 0.4)",
        "rgba(68, 186, 184, 0.4)",
        "rgba(143, 214, 212, 0.4)"
      ]
    }
  }],
  "layout": {
    "title": {
      "text": "Customer Journey Flow",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 600,
    "margin": {"t": 80, "b": 50, "l": 50, "r": 50},
    "font": {"family": "Arial", "size": 12},
    "paper_bgcolor": "white"
  }
}
```

**Key Points:**
- Node colors from TD palette
- Semi-transparent link colors (0.4 opacity)
- Clear node labels
- Adequate height (600px) for visibility

---

## Legend Configuration Standards

### When to Show Legends

| Chart Type | Show Legend? | Position |
|------------|--------------|----------|
| **Pie Chart** | ✅ ALWAYS | Vertical, right side |
| **Multi-Series Bar** | ✅ ALWAYS | Horizontal, top |
| **Single Bar** | ❌ NEVER | N/A |
| **Multi-Series Line** | ✅ ALWAYS | Horizontal, top |
| **Single Line** | ❌ NEVER | N/A |
| **Heatmap** | ❌ (Use colorbar) | N/A |
| **Sankey** | ❌ (Labels in nodes) | N/A |

### Pie Charts - Vertical Legend (Right Side)

```json
{
  "showlegend": true,
  "legend": {
    "orientation": "v",
    "yanchor": "middle",
    "y": 0.5,
    "xanchor": "left",
    "x": 1.02,
    "font": {"size": 12}
  },
  "margin": {"t": 80, "b": 80, "l": 80, "r": 150}
}
```

### Bar/Line Charts - Horizontal Legend (Top)

```json
{
  "showlegend": true,
  "legend": {
    "orientation": "h",
    "yanchor": "bottom",
    "y": 1.05,
    "xanchor": "center",
    "x": 0.5,
    "font": {"size": 12}
  },
  "margin": {"t": 120, "b": 80, "l": 80, "r": 80}
}
```

---

## Text and Number Formatting

### Percentage Display

```json
// Option 1: Add % in template
{
  "text": [45.2, 30.1, 24.7],
  "texttemplate": "%{text}%",
  "textposition": "outside",
  "textfont": {"size": 11, "color": "black"}
}

// Option 2: Pre-formatted strings
{
  "text": ["45.2%", "30.1%", "24.7%"],
  "textposition": "outside",
  "textfont": {"size": 11, "color": "black"}
}
```

### Currency Display

```json
// Option 1: Format with template
{
  "text": [1200000, 850000, 650000],
  "texttemplate": "$%{text:,.0f}",
  "textposition": "outside",
  "textfont": {"size": 11, "color": "black"}
}

// Option 2: Pre-formatted strings
{
  "text": ["$1.2M", "$850K", "$650K"],
  "textposition": "outside",
  "textfont": {"size": 11, "color": "black"}
}
```

### Heatmap Numbers (1 Decimal)

```json
{
  "text": [[23.4, 45.6], [34.5, 56.7]],
  "texttemplate": "%{text:.1f}",
  "textfont": {"size": 12, "color": "black"},
  "hovertemplate": "Value: %{z:.1f}<extra></extra>"
}
```

---

## KPI Indicators (ONLY Use Case for Subplots)

KPI indicators are the **ONLY** exception where subplots are allowed. Use simple number indicators only.

### Simple Number Indicators (NO GAUGES)

```json
{
  "data": [
    {
      "type": "indicator",
      "mode": "number+delta",
      "value": 5240,
      "delta": {"reference": 4800, "suffix": " customers"},
      "title": {"text": "Total Customers", "font": {"size": 12, "color": "#2E41A6"}},
      "number": {"font": {"size": 32, "color": "#44BAB8"}},
      "domain": {"x": [0, 0.25], "y": [0, 1]}
    },
    {
      "type": "indicator",
      "mode": "number+delta",
      "value": 42.5,
      "delta": {"reference": 38.2, "suffix": "%"},
      "title": {"text": "Conversion Rate", "font": {"size": 12, "color": "#2E41A6"}},
      "number": {"prefix": "", "suffix": "%", "font": {"size": 32, "color": "#44BAB8"}},
      "domain": {"x": [0.25, 0.5], "y": [0, 1]}
    },
    {
      "type": "indicator",
      "mode": "number+delta",
      "value": 1250000,
      "delta": {"reference": 1100000, "valueformat": "$,.0f"},
      "title": {"text": "Total Revenue", "font": {"size": 12, "color": "#2E41A6"}},
      "number": {"prefix": "$", "valueformat": ",.0f", "font": {"size": 32, "color": "#44BAB8"}},
      "domain": {"x": [0.5, 0.75], "y": [0, 1]}
    },
    {
      "type": "indicator",
      "mode": "number+delta",
      "value": 25.3,
      "delta": {"reference": 22.1, "suffix": "%"},
      "title": {"text": "Champions %", "font": {"size": 12, "color": "#2E41A6"}},
      "number": {"suffix": "%", "font": {"size": 32, "color": "#44BAB8"}},
      "domain": {"x": [0.75, 1], "y": [0, 1]}
    }
  ],
  "layout": {
    "height": 150,
    "margin": {"t": 20, "b": 20, "l": 20, "r": 20},
    "paper_bgcolor": "white"
  }
}
```

**Key Points for KPI Indicators:**
- Maximum 4 indicators per row
- **Number + Delta ONLY** - no gauges, no fancy visuals
- Large number (32pt), clear title (12pt)
- Show change vs. previous period
- Clean, minimal design
- Use domains to position: `[0, 0.25]`, `[0.25, 0.5]`, `[0.5, 0.75]`, `[0.75, 1]`

---

## Quality Checklist

Before generating any visualization, verify:

### Required for Every Chart
- [ ] Descriptive title with proper positioning (`"x": 0.5`)
- [ ] Clear axis labels with appropriate font size (`"font": {"size": 14}`)
- [ ] TD color palette used consistently
- [ ] Proper height (500-600px based on chart type)
- [ ] Adequate margins (minimum 80px, more for legends)
- [ ] White background (`"plot_bgcolor": "white", "paper_bgcolor": "white"`)
- [ ] Readable font size (12px minimum)
- [ ] Legends visible for multi-category/multi-series charts
- [ ] Numbers displayed on bars/heatmaps with proper formatting

### Legend Requirements
- [ ] `"showlegend": true` for pie charts and comparisons
- [ ] Proper orientation (vertical for pie, horizontal for others)
- [ ] Adequate margin space for legend display
- [ ] Readable font size for legend items
- [ ] Legend positioned visibly (y > 1.0 for horizontal)

### Text Display Requirements
- [ ] Values shown on bars with `"text"` and `"textposition"`
- [ ] Heatmap values formatted to 1 decimal place
- [ ] Hover templates with meaningful information
- [ ] Consistent text formatting across similar chart types
- [ ] Black text for visibility (`"textfont": {"color": "black"}`)

---

## Forbidden Patterns

### ❌ NEVER DO

1. **Subplots for analysis** (`yaxis2`, `xaxis2`, domain specifications)
   - Exception: KPI indicators only
2. **String data format** (`"data": "[...]"`)
3. **Missing legends** on pie charts or comparisons
4. **Legend positioned below visible area** (e.g., `"y": -0.3`)
5. **Missing `"text"` property on bar charts** - numbers won't show
6. **Missing `"textposition"` on bar charts** - numbers won't be positioned
7. **Missing `"texttemplate"` on heatmaps** - numbers won't be formatted
8. **Missing `"showscale"` on heatmaps** - color scale won't appear
9. **Insufficient top margin** for legends (`"t": 80` insufficient, use `"t": 120`)
10. **Unformatted numbers** in heatmaps
11. **Empty or generic titles**
12. **Non-TD colors**
13. **Gauges in KPI indicators** - use number+delta only

### ✅ ALWAYS DO

1. **Individual separate charts** for analysis
2. **JSON array data format** (proper objects, not strings)
3. **Visible legends**: `"y": 1.05` for horizontal, adequate margins
4. **Numbers on bars**: `"text": [...]`, `"textposition": "outside"`
5. **Numbers on heatmaps**: `"text": [...]`, `"texttemplate": "%{text:.1f}"`
6. **Adequate margins**: `"t": 120` minimum for legends
7. **Formatted numbers** with appropriate decimals
8. **Descriptive titles** and axis labels
9. **TD color palette** consistently
10. **Black text color** for visibility: `"textfont": {"color": "black"}`
11. **Simple KPI indicators** - number + delta only

---

## Complete Examples

### Example 1: Customer Segment Distribution (Pie Chart)

```json
{
  "data": [{
    "type": "pie",
    "values": [1250, 2100, 1500, 390],
    "labels": ["Champions", "Loyal Customers", "At Risk", "Lost"],
    "marker": {
      "colors": ["#44BAB8", "#8FD6D4", "#EEB53A", "#828DCA"]
    },
    "textinfo": "label+percent",
    "textposition": "auto",
    "textfont": {"size": 14, "color": "black"},
    "hovertemplate": "<b>%{label}</b><br>Customers: %{value}<br>Percentage: %{percent}<extra></extra>"
  }],
  "layout": {
    "title": {
      "text": "Customer Segment Distribution",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "showlegend": true,
    "legend": {
      "orientation": "v",
      "yanchor": "middle",
      "y": 0.5,
      "xanchor": "left",
      "x": 1.02,
      "font": {"size": 12}
    },
    "margin": {"t": 80, "b": 80, "l": 80, "r": 150},
    "font": {"family": "Arial", "size": 12},
    "paper_bgcolor": "white"
  }
}
```

### Example 2: Revenue by Channel (Multi-Series Bar)

```json
{
  "data": [
    {
      "type": "bar",
      "x": ["Email", "Social", "Search", "Display"],
      "y": [125000, 98000, 156000, 67000],
      "name": "Q3 2024",
      "marker": {"color": "#44BAB8"},
      "text": ["$125K", "$98K", "$156K", "$67K"],
      "textposition": "outside",
      "textfont": {"size": 11, "color": "black"}
    },
    {
      "type": "bar",
      "x": ["Email", "Social", "Search", "Display"],
      "y": [142000, 115000, 178000, 73000],
      "name": "Q4 2024",
      "marker": {"color": "#8FD6D4"},
      "text": ["$142K", "$115K", "$178K", "$73K"],
      "textposition": "outside",
      "textfont": {"size": 11, "color": "black"}
    }
  ],
  "layout": {
    "title": {
      "text": "Revenue by Marketing Channel",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "barmode": "group",
    "showlegend": true,
    "legend": {
      "orientation": "h",
      "yanchor": "bottom",
      "y": 1.05,
      "xanchor": "center",
      "x": 0.5,
      "font": {"size": 12}
    },
    "xaxis": {
      "title": {"text": "Marketing Channels", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "yaxis": {
      "title": {"text": "Revenue ($)", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "margin": {"t": 120, "b": 80, "l": 80, "r": 80},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

### Example 3: Performance Heatmap

```json
{
  "data": [{
    "type": "heatmap",
    "x": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "y": ["Email", "Social", "Search", "Display"],
    "z": [
      [85.3, 92.1, 88.7, 94.2],
      [72.5, 78.3, 81.2, 76.8],
      [91.4, 89.6, 93.8, 95.1],
      [68.2, 71.5, 69.9, 73.4]
    ],
    "colorscale": [
      [0, "#DAF1F1"],
      [0.5, "#8FD6D4"],
      [1, "#44BAB8"]
    ],
    "showscale": true,
    "colorbar": {
      "title": {"text": "Performance %", "font": {"size": 12}},
      "titleside": "right"
    },
    "text": [
      [85.3, 92.1, 88.7, 94.2],
      [72.5, 78.3, 81.2, 76.8],
      [91.4, 89.6, 93.8, 95.1],
      [68.2, 71.5, 69.9, 73.4]
    ],
    "texttemplate": "%{text:.1f}",
    "textfont": {"size": 12, "color": "black"},
    "hovertemplate": "<b>%{y}</b> - <b>%{x}</b><br>Performance: %{z:.1f}%<extra></extra>"
  }],
  "layout": {
    "title": {
      "text": "Weekly Channel Performance",
      "x": 0.5,
      "font": {"size": 18, "color": "#2E41A6"}
    },
    "height": 500,
    "xaxis": {
      "title": {"text": "Week", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "yaxis": {
      "title": {"text": "Channel", "font": {"size": 14, "color": "#2E41A6"}}
    },
    "margin": {"t": 80, "b": 80, "l": 100, "r": 100},
    "font": {"family": "Arial", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white"
  }
}
```

---

## Success Criteria

Your visualization is ready when:

✅ Executives can instantly understand the key message
✅ All text is readable at standard screen sizes
✅ Colors are consistent with TD branding
✅ Legends are visible and descriptive (where needed)
✅ Numbers are formatted appropriately
✅ Chart tells a clear story
✅ JSON structure is valid (not stringified)
✅ No subplots for analysis charts
✅ Clean, professional, executive-ready appearance

---

By following these guidelines, your Field Agent visualizations will be professional, consistent, and immediately actionable for decision-makers.
