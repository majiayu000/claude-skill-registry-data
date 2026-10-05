---
name: syncfusion-vue-pivot-table
description: Use this skill when users ask how to implement Syncfusion PivotView pivot tables in Vue. Trigger for Vue pivot grid/OLAP analysis, measures/dimensions, data binding, drill-down/drill-through, grouping, filtering, calculated fields, conditional formatting, exports, or pivot charts. Vue-only, not React/Angular/Blazor.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Grids"
---

# Implementing Syncfusion Vue PivotView

The Syncfusion Vue Pivot Grid is a powerful data visualization and analysis component for creating interactive pivot tables, aggregating multidimensional data, and performing advanced analytics operations.

**Important:** Always verify API class names, properties, and method signatures by consulting the **reference files in this skill** (`references/*.md`). These are maintained with verified, working examples. Do not assume API details from other sources.

## ⚠️ Security Warning: Data Source Validation

**CRITICAL SECURITY NOTICE:** When implementing pivot tables, always use trusted data sources. **Never** fetch or bind data from untrusted or user-provided URLs without proper validation and sanitization.

### Security Best Practices:

1. **Use Local Data**: Prefer local, in-memory data sources for maximum security
2. **Validate Remote Sources**: Only connect to authenticated and authorized API endpoints under your control
3. **Sanitize User Input**: Never allow users to specify arbitrary URLs or data sources
4. **Implement Authentication**: Always use authentication headers and secure API endpoints
5. **Content Validation**: Validate and sanitize all data received from external sources before binding
6. **Use HTTPS**: Always use HTTPS for remote data connections
7. **Rate Limiting**: Implement rate limiting on API endpoints to prevent abuse

### Security Risks:

- **Indirect Prompt Injection**: Untrusted third-party data can contain malicious content that manipulates AI agent behavior
- **Data Exfiltration**: Malicious data sources could attempt to extract sensitive information
- **Code Injection**: Untrusted data may contain scripts or harmful content

### Recommended Approach:

✅ **DO**: Use controlled, authenticated backend APIs
✅ **DO**: Implement server-side data validation
✅ **DO**: Use environment variables for API endpoints
✅ **DO**: Whitelist allowed data sources

❌ **DON'T**: Accept user-provided URLs
❌ **DON'T**: Bind to public, untrusted endpoints
❌ **DON'T**: Skip data validation and sanitization
❌ **DON'T**: Use HTTP for sensitive data

## Table of Contents

- [Overview](#overview)
- [Core APIs & Properties](#core-apis--properties)
- [Events](#events)
- [Getting Started](#getting-started)
- [Data Binding & Sources](#data-binding--sources)
- [Data Operations & Formatting](#data-operations--formatting)
- [Data Analysis & Pivot Operations](#data-analysis--pivot-operations)
- [Drill-Down & Navigation](#drill-down--navigation)
- [Visualization & Layout](#visualization--layout)
- [Export & Toolbar](#export--toolbar)
- [State & Performance](#state--performance)

---

## Overview

The Syncfusion Vue PivotView (Pivot Table) component provides a powerful, interactive way to analyze and visualize large datasets. It supports:

- **Multiple data sources** (JSON, OLAP, relational databases like MySQL, SQL Server, MongoDB)
- **Rich drill-down functionality** for detailed exploration
- **Pivot charts** for visual data representation
- **Export to Excel, CSV, and PDF**
- **Customizable layouts** (Compact and Classic/Tabular)
- **Performance optimization** for large datasets
- **State persistence** for user experience continuity

Use this skill whenever implementing:
- Pivot Tables in Vue applications
- Data aggregation and analysis UI
- Interactive data exploration interfaces
- Business intelligence dashboards

---

## Core APIs & Properties

### Component Props

| Property | Type | Description |
|----------|------|-------------|
| `dataSourceSettings` | `IDataOptions` | Configure data source, rows, columns, values, filters, formatting |
| `height` | `number \| string` | Set component height in pixels or percentage |
| `width` | `number \| string` | Set component width in pixels or percentage |
| `gridSettings` | `IGridSettings` | Control layout (Compact/Tabular), column width, row height, resizing |
| `displayOption` | `IDisplayOption` | Control Grid vs Chart view: `{ view: 'Grid' \| 'Chart' \| 'Both' }` |
| `chartSettings` | `IChartSettings` | Configure chart type, series, legend, axes, tooltip |
| `groupingBarSettings` | `IGroupingBarSettings` | Customize grouping bar appearance and behavior |
| `allowExcelExport` | `boolean` | Enable Excel export functionality |
| `allowPdfExport` | `boolean` | Enable PDF export functionality |
| `allowCsvExport` | `boolean` | Enable CSV export functionality |
| `allowMemberFilter` | `boolean` | Enable member filtering in UI |
| `allowLabelFilter` | `boolean` | Enable label filtering in UI |
| `allowValueFilter` | `boolean` | Enable value filtering in UI |
| `allowSorting` | `boolean` | Enable sorting functionality |
| `allowDrilling` | `boolean` | Enable drill-down/drill-through actions |
| `allowDrillThrough` | `boolean` | Enable drill-through to detail data (more granular than allowDrilling) |
| `allowResizing` | `boolean` | Enable column and row resizing |
| `allowNumberFormatting` | `boolean` | Show number formatting options in toolbar and dialogs |
| `allowConditionalFormatting` | `boolean` | Enable conditional formatting feature via toolbar button |
| `allowCalculatedField` | `boolean` | Enable calculated field creation |
| `showFieldList` | `boolean` | Display field list panel (UI for field configuration) |
| `showGroupingBar` | `boolean` | Display grouping bar at top (UI for drag-drop field organization) |
| `showToolbar` | `boolean` | Display toolbar with export/report/field management buttons |
| `toolbar` | `string[]` | Array of toolbar items: `['New', 'Save', 'SaveAs', 'Rename', 'Remove', 'Load', 'Grid', 'Chart', 'MDX', 'Export', 'SubTotal', 'GrandTotal', 'ConditionalFormatting', 'NumberFormatting', 'FieldList']` |
| `showTooltip` | `boolean` | Display tooltips when hovering over cells |
| `enablePersistence` | `boolean` | Save pivot state to local storage automatically |
| `conditionalFormatSettings` | `IConditionalFormatSettings[]` | Pre-define conditional formatting rules: value ranges, operators, styling |
| `aggregateTypes` | `string[]` | Limit available aggregation types in dropdown |
| `maxNodeLimitInMemberEditor` | `number` | Maximum members to load in member filter dialog (default 1000) |
| `saveReport` | `Function(args)` | Callback when user saves a report via toolbar |
| `loadReport` | `Function(args)` | Callback when user loads a report via toolbar |
| `renameReport` | `Function(args)` | Callback when user renames a report via toolbar |
| `removeReport` | `Function(args)` | Callback when user removes a report via toolbar |
| `newReport` | `Function(args)` | Callback when user creates a new report via toolbar |
| `fetchReport` | `Function()` | Callback to retrieve list of saved reports |

### DataSourceSettings Properties

| Property | Type | Description |
|----------|------|-------------|
| `dataSource` | `any[]` | JSON array or DataManager instance with data |
| `type` | `'JSON' \| 'CSV'` | Data source type (default: 'JSON') |
| `rows` | `IField[]` | Fields to display in row axis |
| `columns` | `IField[]` | Fields to display in column axis |
| `values` | `IField[]` | Value/measure fields for aggregation |
| `filters` | `IField[]` | Fields to display in filter axis |
| `expandAll` | `boolean` | Expand all row/column groups initially |
| `drilledMembers` | `IDrilledMember[]` | Pre-drilled members: `[{ name: 'Country', items: ['France'] }]` |
| `filterSettings` | `IFilter[]` | Member/label/value filters to apply |
| `sortSettings` | `ISort[]` | Sort rules for fields |
| `formatSettings` | `IFormatSettings[]` | Number formatting: `[{ name: 'Amount', format: 'C0' }]` |
| `calculatedFieldSettings` | `ICalculatedFieldSettings[]` | Calculated field formulas |

### Core Methods

```typescript
// Export methods
excelExport()                          // Export pivot to Excel (.xlsx)
pdfExport()                            // Export pivot to PDF
csvExport()                            // Export pivot to CSV

// Dialog methods
createCalculatedFieldDialog()          // Show calculated field creation dialog
showConditionalFormattingDialog()      // Open conditional formatting dialog
createDrillThroughDialog()             // Show drill-through data dialog

// Data manipulation
refresh()                              // Refresh pivot with current settings
setProperties({...})                   // Update properties dynamically

// Data retrieval
getFieldList()                         // Get all available fields from data source
getDataSourceSettings()                // Get current dataSourceSettings configuration

// Persistence
getPersistData()                       // Get serialized pivot state
loadPersistData(data)                  // Restore pivot state
```

---

## Events

All events from PivotViewComponent documentation are listed below. Use Vue's `:eventName="handler"` syntax to bind.

### Data Manipulation Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **actionBegin** | `dataSourceSettings`, `actionName`, `fieldInfo`, `cancel` | Before any pivot operation (filtering, sorting, aggregation, calculated field) |
| **actionComplete** | `dataSourceSettings`, `actionName`, `fieldInfo`, `actionInfo` | After pivot operation completes successfully |
| **actionFailure** | `actionName`, `errorInfo` | Pivot operation fails or encounters error |

**Common actionName values:**
- `"Aggregate field"` - When aggregation type is selected
- `"Field filtered"` - When member/label/value filter applied
- `"Field sorted"` - When field sorted via UI
- `"Edit pivot table"` - When cell edited in pivot
- `"Remove field"` / `"Add field"` - When field removed/added from grouping bar

### Cell Interaction Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **aggregateCellInfo** | `rowHeaders`, `columnHeaders`, `value`, `valueField`, `aggregateType` | Each value cell renders (use to override value or skip formatting) |
| **cellClick** | Cell coordinates, member info | User clicks on pivot cell |
| **cellDoubleClick** | Cell coordinates, member info | User double-clicks on pivot cell |

### Field Configuration Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **calculatedFieldCreate** | `calculatedField`, `calculatedFieldSettings`, `fieldName`, `dataSourceSettings`, `cancel` | User creates/edits calculated field in dialog |

### Export Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **beforeExcelExport** | `dataSourceSettings`, `isCollapsedStateSaved` | Before Excel export starts |
| **excelExportComplete** | Export result data | After Excel export completes |
| **beforePdfExport** | `dataSourceSettings`, `isCollapsedStateSaved` | Before PDF export starts |
| **pdfExportComplete** | Export result data | After PDF export completes |
| **beforePrint** | `dataSourceSettings` | Before printing starts |
| **printComplete** | Print result | After printing completes |

### Drill & Expand Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **drillThrough** | Row/column headers, raw data records | User initiates drill-through action |
| **beginDrillThrough** | Cell context, member info | Before drill-through action starts (set `args.cancel = true` to prevent) |

### Field Configuration & Grouping Bar Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **fieldDrop** | Field being dropped, destination axis (rows/columns/values/filters) | Field dropped in grouping bar to add it |
| **fieldDragStart** | Field being dragged, source axis | Field drag initiated from grouping bar |
| **fieldRemove** | Field being removed, source axis | Field removed from grouping bar |
| **onFieldDropped** | Field dropped, destination axis | After field successfully dropped (similar to fieldDrop but triggers after) |
| **aggregateMenuOpen** | Field, current aggregation type | Aggregation type dropdown opened in grouping bar/field list |

### Export Customization Events

| Event | Parameters | Triggered When |
|-------|-----------|-----------------|
| **excelQueryCellInfo** | Cell data, row/column info, cell type | For each cell during Excel export (customize cell styling, value, formatting) |
| **excelHeaderQueryCellInfo** | Header cell info, row/column hierarchy | For each header cell in Excel export (customize header styling) |
| **pdfQueryCellInfo** | Cell data, row/column info, pdfCell | For each cell during PDF export (customize PDF cell appearance) |
| **headerCellInfo** | Header cell context, style info | For each header cell render in UI (customize header appearance) |
| **queryCellInfo** | Value cell data, style, aggregateType | For each value cell render in UI (customize cell appearance, value, formatting) |

**Example Event Usage:**

```vue
<template>
  <ejs-pivotview 
    :dataSourceSettings="dataSourceSettings"
    @actionBegin="onActionBegin"
    @actionComplete="onActionComplete"
    @aggregateCellInfo="onAggregateCellInfo">
  </ejs-pivotview>
</template>

<script setup>
const onActionBegin = (args) => {
  if (args.actionName === 'Aggregate field') {
    console.log('User changing aggregation for:', args.fieldInfo.name);
    // Set args.cancel = true to prevent action
  }
};

const onActionComplete = (args) => {
  if (args.actionName === 'Field filtered') {
    console.log('Filter applied successfully');
  }
};

const onAggregateCellInfo = (args) => {
  // Override cell value: args.value = customValue;
  // Skip formatting: args.isFormatted = false;
};
</script>
```

---

## Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

- Installation steps and dependencies
- Setting up a basic PivotView
- Configuration fundamentals
- **CSS imports and theming** — including the Tailwind 3 single-import theme package (`@syncfusion/ej2-tailwind3-theme`)
- **Theme application methods** — npm theme package, CDN, CRG, Theme Studio
- Vue 2 and Vue 3 compatibility
- **Field List Component** - UI for dynamic field configuration
- **Grouping Bar Component** - Inline field organization and drag-drop
- **Loading States & Indicators** - Managing UI feedback during data loading
- **Accessibility Basics** - WCAG compliance, keyboard navigation, screen readers

---

## Data Binding & Sources

### JSON Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)

- Binding local JSON data
- Using DataManager with JsonAdaptor
- File upload and JSON loading
- Local vs remote data approaches
- **Server-Side Pivot Processing** - Backend aggregation for large datasets
- **Complex Data Binding Patterns** - Multi-source, real-time updates, lazy loading

### External Data Sources
📄 **Read:** [references/connecting-to-data-source.md](references/connecting-to-data-source.md)

- MySQL database connections
- SQL Server integration
- MongoDB connectivity
- PostgreSQL, Oracle, Elasticsearch, Snowflake
- Creating Web API controllers for data retrieval

### OLAP (Analysis Services)
📄 **Read:** [references/olap.md](references/olap.md)

- SQL Server Analysis Services (SSAS) configuration
- OLAP field naming convention `[Dimension].[Hierarchy]`
- Connecting to SSAS cubes for multi-dimensional analysis
- Handling massive datasets (millions of rows)
- OLAP vs JSON binding comparison
- Drill-down with OLAP hierarchies

---

## Data Operations & Formatting

### Data Formatting
📄 **Read:** [references/data-formatting.md](references/data-formatting.md)

- Number formatting (currency, percentages, decimals)
- Date and time value formatting
- Custom format patterns
- Format settings configuration
- **Internationalization & Localization** - Multi-language support, RTL, regional formatting
- **Accessible Styling** - High contrast, color-blind friendly, font sizing

### Conditional Formatting
📄 **Read:** [references/conditional-formatting.md](references/conditional-formatting.md)

- Enable conditional formatting feature
- Define formatting rules with conditions and operators
- Apply styles based on cell values (backgroundColor, color, fontFamily, etc.)
- Pre-define rules in dataSourceSettings
- Show conditional formatting dialog via toolbar
- Dynamic rule modification and effects

### Data Shaping & Field Configuration
📄 **Read:** [references/data-shaping.md](references/data-shaping.md)

- Defining rows, columns, and values
- Field hierarchy and nesting
- Captions and field organization
- Expand/collapse behaviors
- Configuration best practices

### Row & Column Properties
📄 **Read:** [references/row-and-column.md](references/row-and-column.md)

- Setting width and height (pixels, percentage, auto)
- Row height customization
- Column width settings
- Responsive sizing
- Minimum width guarantees

### Show/Hide Totals
📄 **Read:** [references/show-hide-totals.md](references/show-hide-totals.md)

- Grand total visibility control
- Subtotal positioning and display
- Summary row configuration
- Conditional total display

---

## Data Analysis & Pivot Operations

### Filtering Data
📄 **Read:** [references/filtering.md](references/filtering.md)

- Member filtering (include/exclude specific members, select all, search, sort)
- Label filtering (contains, starts with, ends with, between, etc., for string, number, and date)
- Value filtering (filter by aggregated value ranges, including **Top N** and **Bottom N**)
- Programmatic filter configuration via `filterSettings`
- Filter dialog UI features (search, select all, sort, **append current selection to filter**)
- OLAP-specific options: `loadOnDemandInMemberEditor` and `levelCount`
- Large dataset filter optimization with `maxNodeLimitInMemberEditor`
- Filter-related events: `memberFiltering`, `memberEditorOpen`, `actionBegin`, `actionComplete`, `actionFailure`

### Sorting Fields & Values
📄 **Read:** [references/sorting.md](references/sorting.md)

- Member sorting (ascending/descending)
- Value sorting (sort by aggregated values)
- Custom sorting (user-defined member order)
- Alphanumeric sorting (numeric vs alphabetical)
- Sort settings configuration
- Multi-level sorting in complex hierarchies

### Aggregation & Calculated Fields
📄 **Read:** [references/aggregation-and-calculated-fields.md](references/aggregation-and-calculated-fields.md)

- Aggregation types (Sum, Average, Count, Min, Max, etc.)
- Percentage aggregations (% of Total, % of Row, % of Parent, etc.)
- Comparative aggregations (Difference From, Percentage Difference)
- Running totals and percentage of running totals (cumulative % of running totals; client-side engine only)
- Aggregation dropdown customization
- Hiding aggregation labels for cleaner UI
- Calculated fields and custom formulas

### Grouping Data
📄 **Read:** [references/grouping.md](references/grouping.md)

- Number grouping (ranges like 1-5, 6-10)
- Date grouping (Year, Quarter, Month, Week, Day)
- Custom grouping (business-specific categories)
- Programmatic grouping configuration
- Multi-type grouping in same pivot
- Grouping UI operations and ungroup functionality

### Editing Cell Data
📄 **Read:** [references/editing.md](references/editing.md)

- Cell editing modes (Normal, Dialog, Batch, Command Columns)
- CRUD operations (Create, Read, Update, Delete)
- Edit settings configuration
- Confirmation dialogs for safety
- Edit events and validation
- Bulk editing with batch mode
- **Data Grid Editor Configuration** - Grid behavior, selection, performance, pagination

---

## Drill-Down & Navigation

### Drill-Down & Drill-Up
📄 **Read:** [references/drill-down-up.md](references/drill-down-up.md)

- Expand/collapse hierarchical data
- Drill position and specific member drilling
- expandAll property configuration
- Expand specific fields only
- Drill member exclusions
- Position-aware drilling

### Report Manipulation
📄 **Read:** [references/report-manipulation.md](references/report-manipulation.md)

- Dynamic report modification
- Field list interactions
- Grouping bar operations
- Report updates and refresh
- **Loading Predefined Reports** - Report templates, server-side templates, initial report loading

### Hyperlinks
📄 **Read:** [references/hyperlink.md](references/hyperlink.md)

- Enable hyperlinks in cells
- Hyperlink settings configuration
- Row header hyperlinks
- Column header hyperlinks
- Value cell hyperlinks
- Summary cell hyperlinks
- Conditional hyperlink rules
- Custom CSS styling

---

## Visualization & Layout

### Classic/Tabular Layout
📄 **Read:** [references/classic-layout.md](references/classic-layout.md)

- Tabular layout benefits and setup
- Row field side-by-side display
- Grand total positioning
- Subtotal placement
- Layout configuration (`gridSettings.layout`)
- Limitations and compatibility notes

### Pivot Chart Integration
📄 **Read:** [references/pivot-chart.md](references/pivot-chart.md)

- Pivot Chart setup and display modes
- 21+ chart types (Line, Column, Area, Bar, Bubble, Scatter, etc.)
- Display options (Grid only, Chart only, Both)
- Primary view selection
- Chart customization (series, axes, legends)
- Drill-down in charts

### Tooltip Configuration
📄 **Read:** [references/tooltip.md](references/tooltip.md)

- Enable/disable tooltips with `showTooltip` property
- Custom tooltip templates with HTML and dynamic placeholders
- Template placeholders: `${rowHeaders}`, `${columnHeaders}`, `${valueField}`, `${aggregateType}`, `${value}`
- Basic and advanced template examples with CSS styling
- Chart-specific tooltips via `chartSettings.tooltip`
- Tooltip positioning and mobile considerations
- Accessibility best practices and keyboard support

---

## Export & Toolbar

### Export to Excel & PDF
📄 **Read:** [references/export.md](references/export.md)

- Excel export (.xlsx format)
- CSV export functionality
- PDF export capabilities
- Export method invocation
- Toolbar export options
- Data preservation during export

### Toolbar & Report Management
📄 **Read:** [references/toolbar.md](references/toolbar.md)

- Enable toolbar with `showToolbar` property
- Configure toolbar items array (New, Save, SaveAs, Load, Rename, Remove, Grid, Chart, Export, ConditionalFormatting, etc.)
- Report lifecycle callbacks: saveReport(), loadReport(), renameReport(), removeReport()
- fetchReport() to retrieve saved reports
- Custom toolbar items and styling
- Report data persistence and retrieval
- **Sizing & Layout Configuration** - Component dimensions, responsive behavior, container sizing

---

## State & Performance

### State Persistence
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)

- Enable persistence (`enablePersistence`)
- Automatic state saving to local storage
- Layout retention across sessions
- Save and load pivot layout programmatically
- `getPersistData()` and `loadPersistData()` methods
- Custom persistence workflows

### Performance Best Practices
📄 **Read:** [references/performance.md](references/performance.md)

- Virtual scrolling for large datasets
- Paging implementation
- Server-side pivot engine
- Data compression techniques
- Defer layout update feature
- Sorting optimization
- Member filtering performance
- Grouping impacts and alternatives

---

## Quick Start Example

```vue
<template>
  <div id="app">
    <ejs-pivotview
      :dataSourceSettings="dataSourceSettings"
      :height="height"
      :width="width"
      :gridSettings="gridSettings"
      :showFieldList="showFieldList">
    </ejs-pivotview>
  </div>
</template>

<script setup>
import { PivotViewComponent as EjsPivotview, FieldList } from "@syncfusion/ej2-vue-pivotview";
import { pivotData } from './pivotData.js';
import { provide } from "vue";

const dataSourceSettings = {
  dataSource: pivotData,
  expandAll: false,
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [
    { name: 'Sold', caption: 'Units Sold' },
    { name: 'Amount', caption: 'Sold Amount' }
  ],
  formatSettings: [{ name: 'Amount', format: 'C0' }],
  filters: []
};

const height = '450px';
const width = '100%';
const showFieldList = true;
const gridSettings = { columnWidth: 120, layout: 'Compact' };

provide('pivotview', [FieldList]);
</script>

<style>
/* Tailwind 3 theme package — single import covers all Pivot Table dependencies */
@import "../node_modules/@syncfusion/ej2-tailwind3-theme/styles/pivotview/index.css";
</style>
```

---

## Common Patterns

### Pattern 1: Aggregated Analysis
Define `rows`, `columns`, and `values` to create aggregated summaries of your data.

### Pattern 2: Drill-Down Exploration
Use `expandAll: false` with drill-down icons to allow users to explore hierarchical data.

### Pattern 3: Multi-Source Analysis  
Use `dataSourceSettings.type` to bind different data sources (JSON, OLAP, relational databases).

### Pattern 4: Visual Representation
Enable Pivot Chart with `displayOption: { view: 'Chart' }` for graphical insights.

### Pattern 5: Large Dataset Handling
Combine `virtualScrolling: true`, `allowPaging: true`, or server-side engine for performance.

---

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `dataSourceSettings` | Object | Defines data source, fields, and aggregation rules |
| `gridSettings` | Object | Controls layout, dimensions, and grid behavior |
| `displayOption` | Object | Controls Grid vs Chart visibility |
| `chartSettings` | Object | Configures chart type and appearance |
| `hyperlinkSettings` | Object | Enables and configures hyperlinks |
| `allowExcelExport` | Boolean | Enables Excel export functionality |
| `allowPaging` | Boolean | Enables paging for large datasets |
| `enableVirtualization` | Boolean | Enables virtual scrolling |
| `enablePersistence` | Boolean | Preserves component state in local storage |
| `showFieldList` | Boolean | Displays field list UI |
| `showGroupingBar` | Boolean | Displays grouping bar UI |

---

## When to Read Each Reference

- **Need to set up PivotView?** → `getting-started.md`
- **Binding data?** → `data-binding.md` or `connecting-to-data-source.md`
- **Configuring fields/layout?** → `data-shaping.md`, `row-and-column.md`
- **Adding drill-down?** → `drill-down-up.md`, `report-manipulation.md`
- **Showing charts?** → `pivot-chart.md`
- **Adding hyperlinks?** → `hyperlink.md`
- **Exporting data?** → `export.md`, `toolbar.md`
- **Saving state?** → `state-persistence.md`
- **Optimizing performance?** → `performance.md`

---

## Next Steps

1. Start with [getting-started.md](references/getting-started.md) to set up your first PivotView
2. Bind your data using [data-binding.md](references/data-binding.md) or [connecting-to-data-source.md](references/connecting-to-data-source.md)
3. Configure fields and layout with [data-shaping.md](references/data-shaping.md)
4. Customize appearance and behavior with the relevant reference guides
5. Implement export and persistence features as needed
6. Optimize performance for large datasets using [performance.md](references/performance.md)

