---
name: syncfusion-vue-sparkline
description: Guide for implementing Syncfusion Vue Sparkline component for compact data visualization. Use this skill to create line, column, area, pie, and win-loss sparklines with interactive tooltips, custom styling, and accessibility features. Always refer here when users need to display mini charts in dashboards or inline data trends.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue Sparkline Component

The Sparkline component displays data in a compact, space-efficient format—perfect for dashboards, tables, and data summaries. This skill guides you through setup, configuration, and best practices for working with Syncfusion Vue Sparklines.

## When to Use This Skill

**Use this skill when:**
- User needs to display mini trend charts in dashboards or tables
- Creating compact data visualizations within limited space
- Building real-time monitoring displays with small chart indicators
- Implementing multiple chart types (line, column, area, pie, win-loss)
- Configuring interactive features like tooltips and hover tracking
- Customizing sparkline appearance and styling
- Ensuring accessibility compliance for charts
- Adding localization support to sparkline components

**Components covered:** SparklineComponent, SparklineTooltip module

---

## Component Overview

### Key Characteristics

- **Compact Design:** Sparklines render without axes or labels, ideal for inline visualization
- **Multiple Types:** Line, Column, Area, Pie, and Win-Loss types
- **Interactive Features:** Tooltips, track lines, and hover effects
- **Customizable Appearance:** Colors, borders, padding, themes
- **Module-Based Architecture:** Import only required features (SparklineTooltip for interactive features)
- **Accessibility:** WCAG 2.2 support, keyboard navigation (Ctrl+P for print), RTL support

### Common Use Cases

1. **Dashboard Indicators** - Show trends at a glance with mini charts
2. **Table Columns** - Inline sparklines showing historical data per row
3. **KPI Displays** - Visualize performance metrics compactly
4. **Real-time Monitoring** - Update sparklines with live data streams
5. **Comparison Charts** - Multiple sparklines side-by-side for relative analysis

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm package setup
- Vue 2 project setup with Vue-CLI
- Component registration and imports
- Basic sparkline rendering
- Data binding with dataSource property
- Width and height configuration

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Overview
- Properties
- Data Models
- Events
- Methods
- Enums
- Child Directives
- Modules/Services
- Common Usage Patterns
- Additional Resources

### Sparkline Types
📄 **Read:** [references/sparkline-types.md](references/sparkline-types.md)
- Line type for trend visualization
- Column type for categorical data
- Area type for filled trend charts
- Pie type for proportion display
- Win-Loss type for binary outcomes
- When to use each type

### Data Binding and Axis Configuration
📄 **Read:** [references/data-binding-and-axis.md](references/data-binding-and-axis.md)
- Binding data with dataSource property
- xName and yName configuration for data mapping
- Axis settings (min/max values)
- Category vs numeric data types
- Data format requirements
- Dynamic data updates

### User Interaction
📄 **Read:** [references/user-interaction.md](references/user-interaction.md)
- Tooltip configuration and customization
- Tooltip formatting with templates
- Track line setup and styling
- SparklineTooltip module injection
- Interactive patterns and best practices
- Hover and click event handling

### Appearance and Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)
- Border and container area configuration
- Padding and margin settings
- Background color customization
- Fill color and line width
- Theme application (Material, Fabric, Bootstrap, Highcontrast)
- CSS customization patterns

### Data Labels and Markers
📄 **Read:** [references/data-labels-and-markers.md](references/data-labels-and-markers.md)
- Enabling and configuring data labels
- Marker customization (size, color, shape)
- Range band visualization
- Special points highlighting
- Label formatting and positioning

### Advanced Features and Accessibility
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Localization and internationalization
- Accessibility compliance (WCAG 2.2, Section 508)
- Keyboard navigation (Ctrl+P print)
- Right-to-left (RTL) language support
- Screen reader compatibility
- Module injection patterns for performance

### Common Implementation Patterns
📄 **Read:** [references/common-patterns.md](references/common-patterns.md)
- Dashboard sparkline layouts
- Responsive sizing and scaling
- Real-time data streaming updates
- Multiple sparklines in grids
- Performance optimization tips
- Error handling and edge cases

---

## Quick Start Example

**Basic sparkline with data binding:**

```vue
<template>
  <div>
    <ejs-sparkline 
      id="sparkline" 
      :dataSource='dataSource' 
      xName='year' 
      yName='sales'
      type='Line'
      :height='height'
      :width='width'>
    </ejs-sparkline>
  </div>
</template>

<script>
import { SparklineComponent } from '@syncfusion/ej2-vue-charts';

export default {
  components: {
    'ejs-sparkline': SparklineComponent
  },
  data: function() {
    return {
      height: '100px',
      width: '80%',
      dataSource: [
        { year: '2018', sales: 25000 },
        { year: '2019', sales: 32000 },
        { year: '2020', sales: 28000 },
        { year: '2021', sales: 35000 },
        { year: '2022', sales: 42000 }
      ]
    }
  }
}
</script>
```

---

## Common Patterns

### Pattern 1: Compact Dashboard Display
Display multiple sparklines showing different metrics:
- Use `type='Column'` for categorical comparisons
- Set consistent `width` and `height` for alignment
- Apply `fill` color for visual distinction
- Configure minimal `padding` to save space

### Pattern 2: Interactive Sparkline with Tooltip
Enable user feedback on data points:
- Inject `SparklineTooltip` module via `provide`
- Set `tooltipSettings.visible = true`
- Use format: `'${xName} : ${yName}'` for readable output
- Customize tooltip appearance with `fill` and `textStyle`

### Pattern 3: Real-time Data Updates
Stream live data to sparklines:
- Bind `dataSource` to reactive Vue data property
- Update array directly (Vue will detect changes)
- Use `type='Line'` or `Area` for continuous trends
- Consider debouncing updates for performance

### Pattern 4: Responsive Sizing
Make sparklines adapt to container:
- Set `width` to percentage (e.g., `'100%'`) for fluid layouts
- Use `height` in pixels for consistent aspect ratio
- Container parent must have defined dimensions
- Test on different screen sizes

---

## Key Props Reference

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `dataSource` | Array | Data to visualize | `[{x: 1, y: 2}, ...]` |
| `xName` | String | X-axis data property | `'year'` |
| `yName` | String | Y-axis data property | `'sales'` |
| `type` | String | Chart type | `'Line'`, `'Column'`, `'Area'`, `'Pie'`, `'WinLoss'` |
| `fill` | String | Series color | `'#007bff'`, `'blue'` |
| `height` | String | Container height | `'100px'`, `'200px'` |
| `width` | String | Container width | `'300px'`, `'80%'` |
| `tooltipSettings` | Object | Tooltip config | `{ visible: true, format: '...' }` |
| `border` | Object | Border style | `{ color: '#000', width: 2 }` |
| `padding` | Object | Padding values | `{ left: 10, right: 10, top: 10, bottom: 10 }` |
| `axisSettings` | Object | Axis configuration | `{ minX: 0, maxX: 10, minY: 0, maxY: 100 }` |
| `theme` | String | Color theme | `'Material'`, `'Fabric'`, `'Bootstrap'`, `'Highcontrast'` |

---

## Implementation Tips

### Module Injection
Always inject required modules for advanced features:
```javascript
provide: {
  sparkline: [SparklineTooltip]  // For interactive features
}
```

### Data Format
Ensure data is properly structured:
- Use consistent property names (`xName` and `yName`)
- Provide numeric or string values matching your chart type
- For Pie charts, ensure numeric values only
- For Win-Loss, use positive/negative or binary values

### Performance Optimization
- Update `dataSource` sparingly for real-time data
- Use `padding` strategically to avoid excessive whitespace
- Cache computed data before binding
- Use computed properties for calculated series

### Styling Best Practices
- Use `theme` prop for consistent color schemes
- Apply `fill` color for series visibility
- Use `border` for container definition
- Customize via `containerArea` for advanced styling

---

## End of Implementing Sparkline Skill

**Next Steps:** Follow the reference files above based on your specific needs, or proceed to test case creation.
