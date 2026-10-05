---
name: syncfusion-vue-treemap
description: Build hierarchical data visualizations with the Syncfusion Vue TreeMap component. Use this skill when users need to visualize tree-structured or hierarchical data, create hierarchical layouts with multiple levels, apply color mapping and legends, enable drill-down navigation, or customize appearance with labels, tooltips, and animations. The TreeMap is ideal for displaying part-to-whole relationships in large datasets with interactive features like selection and highlight modes.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing the Syncfusion Vue TreeMap Component

The TreeMap is a hierarchical data visualization component that displays tree-structured data as nested rectangles. It efficiently represents part-to-whole relationships and supports interactive features like drill-down navigation, color mapping, legends, selection modes, and customizable styling.

## When to Use This Skill

- Display hierarchical data with multiple levels (organization structure, file system, geographic regions)
- Visualize part-to-whole relationships and proportional data
- Create interactive drill-down experiences for exploring hierarchies
- Apply color mapping based on data values to reveal patterns
- Add legends, tooltips, and labels for better data interpretation
- Implement selection and highlight modes for user interaction

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic TreeMap rendering
- Component registration (Vue 2 & Vue 3)
- CSS imports and theme configuration
- Module injection for advanced features

### Data Binding and Structure
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Flat and hierarchical data structures
- Binding data sources
- Data field mapping with `weightValuePath`
- Leaf item configuration
- Dynamic data updates

### Hierarchical Levels and Layout
📄 **Read:** [references/levels-and-layout.md](references/levels-and-layout.md)
- Creating multi-level hierarchies with `groupPath`
- Layout types (Squarified, SliceAndDiceVertical, SliceAndDiceHorizontal, SliceAndDiceAuto)
- Level styling and borders
- Leaf item appearance
- Nesting strategies for complex data

### Color Mapping and Appearance
📄 **Read:** [references/color-mapping.md](references/color-mapping.md)
- Range color mapping (from/to ranges)
- Equal color mapping (discrete values)
- Palette color mapping
- Desaturation and gradient effects
- Binding colors from data source
- Legend configuration and positioning

### User Interactions (Selection, Highlight, Drilldown)
📄 **Read:** [references/user-interactions.md](references/user-interactions.md)
- Selection settings and modes
- Highlight behavior
- Drill-down navigation
- Event handling (click, hover, selection)
- Interactive state customization

### Labels, Tooltips, and Data Display
📄 **Read:** [references/labels-tooltips-display.md](references/labels-tooltips-display.md)
- Data label configuration
- Label positioning and formatting
- Tooltip templates
- Showing/hiding labels per level
- Custom formatting and truncation

### Internationalization and Accessibility
📄 **Read:** [references/internationalization-accessibility.md](references/internationalization-accessibility.md)
- RTL (Right-to-Left) support
- Localization and translation
- WCAG compliance
- ARIA attributes
- Screen reader support
- Keyboard navigation

## Quick Start Example

```vue
<template>
    <div class="control_wrapper">
        <ejs-treemap 
            id="treemap" 
            :dataSource='dataSource' 
            :weightValuePath='weightValuePath'
            :leafItemSettings='leafItemSettings'>
        </ejs-treemap>
    </div>
</template>

<script setup>
import { TreeMapComponent as EjsTreemap } from "@syncfusion/ej2-vue-treemap";

const dataSource = [
    { State: "Brazil", Count: 25 },
    { State: "Colombia", Count: 12 },
    { State: "Argentina", Count: 9 },
    { State: "Chile", Count: 6 },
];

const weightValuePath = 'Count';
const leafItemSettings = {
    labelPath: 'State'
};
</script>
```

This renders a basic TreeMap with countries sized by their count values and labeled with state names.

## Common Patterns

### Multi-Level Hierarchy with Color Mapping

```vue
<script setup>
const levels = [
    { 
        groupPath: 'Region',
        border: { color: 'black', width: 0.5 }
    },
    { 
        groupPath: 'Country',
        border: { color: 'gray', width: 0.3 }
    }
];

const leafItemSettings = {
    labelPath: 'City',
    colorMapping: [
        { from: 100, to: 500, color: '#FFA07A' },
        { from: 500, to: 1000, color: '#FF6347' }
    ]
};
</script>
```

### Drill-Down with Legend

```vue
<script setup>
import { TreeMapComponent, TreeMapLegend } from "@syncfusion/ej2-vue-treemap";
import { provide } from 'vue';

const enableDrillDown = true;
const legendSettings = {
    visible: true,
    position: 'Top',
    shape: 'Rectangle'
};

provide('treemap', [TreeMapLegend]);
</script>
```

## Key Props

| Prop | Purpose |
|------|---------|
| `dataSource` | Array of data objects with hierarchical structure |
| `weightValuePath` | Field name for sizing rectangles |
| `levels` | Array defining hierarchy with `groupPath` for each level |
| `leafItemSettings` | Appearance of leaf-level items (labels, colors, positions) |
| `colorMapping` | Rules for mapping data values to colors |
| `layoutType` | Algorithm for arranging rectangles (Squarified, SliceAndDice*) |
| `enableDrillDown` | Allow clicking to drill into hierarchy levels |
| `legendSettings` | Legend configuration (visibility, position, shape) |
| `selectionSettings` | Selection behavior and styling |
| `highlightSettings` | Highlight appearance on hover |
| `palette` | Array of colors for auto-coloring groups |

## Common Use Cases

1. **Organization Hierarchy** - Visualize company structure with departments and teams
2. **File System** - Show directory structure with file sizes
3. **Sales by Region** - Display sales performance across regions, countries, and products
4. **Portfolio Analysis** - Show investment allocation by sector, asset class, and holding
5. **Disk Space** - Visualize storage usage across folders and subfolders
6. **Market Share** - Display market segments and competitors proportionally
