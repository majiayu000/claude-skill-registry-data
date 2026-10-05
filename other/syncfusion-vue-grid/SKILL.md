---
name: syncfusion-vue-grid
description: Implements Syncfusion Vue Grid component for feature-rich data tables and grids. Use this when working with data display, sorting, filtering, grouping, aggregates, editing, or exporting. This skill covers grid configuration, CRUD operations, virtual scrolling or infinite scrolling,  hierarchy grids, state persistence, and advanced data management features for data-intensive applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Grids"
---

# Implementing Vue Grid Component

The Syncfusion Vue Grid is an enterprise-grade data table component for Vue 2 and Vue 3 that enables powerful data visualization and manipulation capabilities. It's essential for creating responsive, feature-rich data applications.

## ⚠️ Security & Trust Boundary
 
- The Grid skill does not perform any remote data access.
- All external API interaction is handled by a separate DataManager skill outside this skill’s trust boundary.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation Map](#documentation-map)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)
- [Key Props Reference](#key-props-reference)
- [Top Use Cases](#top-use-cases)
- [Module Injection](#module-injection)

## When to Use This Skill

Use this skill when you need to:
- Display and manage tabular data with advanced interactions
- Implement CRUD (Create, Read, Update, Delete) operations
- Build feature-rich data tables with sorting, filtering, and grouping
- Create responsive dashboards with data visualization
- Connect grids to various data sources (local, APIs, databases)
- Export data to multiple formats (Excel, PDF, CSV)
- Implement real-time grids with virtual scrolling and performance optimization

## Component Overview

The Vue Grid is built on Syncfusion's Essential JS 2 framework and provides:

- **Data Binding**: Local and remote data sources with DataManager
- **Column Management**: Type definitions, templates, reordering, resizing, freezing
- **Data Operations**: Sorting, filtering (multiple modes), grouping, aggregates
- **Selection**: Row, cell, column, and checkbox selection modes
- **Editing**: Inline, dialog, batch editing with validation
- **Export**: Excel, PDF, CSV export with templates
- **Templates**: Custom row, cell, and header templates
- **Performance**: Virtual scrolling, infinite scroll, immutable mode
- **UI Features**: Context menu, toolbar, state management, clipboard
- **Internationalization**: Localization, RTL support, multiple formats
- **Accessibility**: WCAG compliance, keyboard navigation

## Documentation Map

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and setup (Vue 2 & Vue 3)
- Package configuration
- Quasar Framework setup
- CSS theme imports
- First component creation
- Enable core features

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding
- Remote data binding
- DataManager adaptors
- CRUD operations
- Loading indicators
- Real-time updates
- Refreshing and updating data
- Offline mode
- Immutable mode
- Timezone handling
- Export operations

### Connecting to Adaptors
📄 **Read:** [references/adaptors.md](references/adaptors.md)
- URL adaptor
- ODataV4 adaptor
- Web API adaptor
- GraphQL adaptor
- Web method adaptor
- RemoteSave adaptor
- Custom adaptor configuration

### Grid Feature Modules
📄 **Read:** [references/module.md](references/module.md)
- What are modules
- Complete module list
- Default injected modules
- Module injection examples
- Feature dependencies

### Vue 2 Configuration
📄 **Read:** [references/vue2.md](references/vue2.md)
- Columns
- Rows
- Cells
- Adaptive UI
- Modules
- Performance optimization
- Data binding (Vue 2)
- Editing
- Sorting
- Grouping
- Filtering
- Scrolling
- Searching
- Paging
- Selection
- Export operations
- Aggregates
- Printing
- Hierarchical binding
- State management
- Toolbar

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Column data types
- Column width
- Column formatting
- Field mapping
- Column rendering
- Column templates
- Column headers
- Foreign key columns
- Column chooser
- Column menu
- Column reordering
- Column resizing
- Row and column spanning

### Frozen Columns
📄 **Read:** [references/frozen.md](references/frozen.md)
- Freeze columns
- Freeze direction (left, right, both)
- Programmatic freeze/unfreeze
- Split view configurations

### Cells
📄 **Read:** [references/cell.md](references/cell.md)
- Cell styling
- Cell content
- Cell wrapping and clipping
- Cell tooltips
- Grid lines
- Cell events
- Cell formatting

### Clipboard
📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy to clipboard functionality
- Copy with headers
- Copy via external buttons
- AutoFill by dragging
- Paste operations
- Keyboard shortcuts (Ctrl+C, Ctrl+Shift+H)

### Rows
📄 **Read:** [references/rows.md](references/rows.md)
- Row data types
- Row styling
- Row height
- Row templates
- Detail templates
- Row drag-drop
- Row spanning
- Row pinning
- Row selection

### Filtering
📄 **Read:** [references/filtering.md](references/filtering.md)
- Basic filtering
- Filter bar
- Filter menu
- Excel-like filters
- Checkbox filters
- Filter configuration
- Diacritics filter
- Filtering events
- Common filtering patterns

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- Basic sorting
- Sort direction
- Multi-column sorting
- Foreign key sorting
- Custom sort comparers
- Culture-based sorting
- Programmatic sorting
- Sort events
- Touch and gesture sorting
- Sort icon customization

### Paging
📄 **Read:** [references/paging.md](references/paging.md)
- Paging configuration
- Page size options
- Pager customization
- Pager position
- Page navigation
- Custom pager template

### Scrolling
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Basic scrolling
- Virtual scrolling
- Infinite scrolling
- Column virtualization
- Sticky headers
- Scrollbar customization
- Performance tuning
- Advanced scrolling

### Performance Best Practices
📄 **Read:** [references/performance.md](references/performance.md)
- Improving loading performance with large datasets
- Paging for large datasets
- Row virtualization
- Infinite scrolling
- Column virtualization
- Optimizing rendering with templates
- CRG optimization
- Server-side data operations
- Handling large JSON payloads
- Excel export limitations

### Editing
📄 **Read:** [references/editing.md](references/editing.md)
- Enabling editing
- Edit modes (Normal, Dialog, Batch, Template)
- Edit types (text, numeric, dropdown, date)
- Inline editing
- Dialog editing
- Batch editing
- Template editing
- Server persistence
- Advanced editing

### Column Validation
📄 **Read:** [references/validation.md](references/validation.md)
- Required field validation
- Numeric validation
- Email validation
- Min length validation
- Custom validation rules
- Custom validation based on dropdown change
- Dynamically add or remove validation rules
- Prevent duplicate rows

### Command Column Editing
📄 **Read:** [references/command-column.md](references/command-column.md)
- Basic command column
- Custom command column
- CRUD action buttons (Edit, Delete, Save, Cancel)
- Custom command handlers
- Customize button appearance and icons

### Grouping
📄 **Read:** [references/grouping.md](references/grouping.md)
- Basic grouping
- Prevent grouping for specific columns
- Multi-level grouping
- Reorder grouped columns
- Group with paging
- Group caption templates
- Group by format
- Collapse/expand groups
- Programmatic grouping
- Sort grouped columns
- Lazy load grouping
- Grouping events

### Aggregates
📄 **Read:** [references/aggregates.md](references/aggregates.md)
- Basic aggregates
- Aggregate types (Sum, Average, Count, Max, Min)
- Footer aggregates
- Group aggregates
- Custom aggregates
- Reactive aggregates
- Multiple aggregates

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Row selection
- Cell selection
- Column selection
- Checkbox selection
- Multi-select
- Keyboard shortcuts
- Selection events

### Hierarchical Binding
📄 **Read:** [references/hierarchical-binding.md](references/hierarchical-binding.md)
- Master-detail grid
- Child grid configuration
- Detail templates
- Expand-collapse
- Hierarchy events

### State Management
📄 **Read:** [references/state-management.md](references/state-management.md)
- Grid state
- Save state
- Restore state
- Local storage persistence
- Immutable mode

### Toolbar
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Toolbar configuration
- Built-in toolbar items (Export, Edit, Delete, Search)
- Custom toolbar items
- Toolbar positioning
- Enable or disable toolbar items
- Customize toolbar with CSS

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Enable context menu
- Left click context menu
- Enable/disable menu items
- Show/hide menu items
- Custom menu items
- Menu events
- Practical examples

### Printing
📄 **Read:** [references/printing.md](references/printing.md)
- Enable printing
- Print toolbar configuration
- Print modes (All, Current Page, Selected)
- Print customization
- Print events

### Excel Export
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Basic excel export
- Export options (selected, current page, all data)
- Customize export
- Styling and formatting
- Advanced features
- CSV export limitations

### PDF Export
📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- Basic PDF export
- Export options (selected, current page, all data)
- Customize export
- Header and footer configuration
- Advanced features

### Searching
📄 **Read:** [references/searching.md](references/searching.md)
- Enable search functionality
- Search bar configuration
- Programmatic search
- Search events
- Advanced search

### Globalization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Locale settings (50+ languages)
- Loading translations
- Number formatting
- Date formatting
- Internationalization
- RTL support (Arabic, Hebrew, Persian, Urdu)
- Custom translations
- Practical examples

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WAI-ARIA attributes
- Keyboard navigation
- Custom keyboard shortcuts
- Preventing default key behavior
- Screen reader support
- WCAG compliance

### Style and Appearance
📄 **Read:** [references/style-and-appearance.md](references/style-and-appearance.md)
- Theme selection (Material, Bootstrap, Fluent, Tailwind)
- CSS styling
- Cell styling
- Row styling
- Header styling
- Paging styling
- Sorting styling
- Filtering styling
- Grouping styling
- Toolbar styling
- Editing styling
- Aggregate styling
- Selection styling
- Responsive design
- Dark mode

### Adaptive UI
📄 **Read:** [references/adaptive.md](references/adaptive.md)
- Enable adaptive UI
- Adaptive rendering modes (Details, Grid, Both)
- Adaptive UI with virtualization
- Mobile device handling
- Responsive columns
- Adaptive detail templates

### Grid Properties
📄 **Read:** [references/grid-properties.md](references/grid-properties.md)
- Overview of all properties
- Data management properties
- Display properties
- Feature flags and toggles
- Configuration properties
- Advanced feature properties
- Status properties
- Behavioral properties
- Module references

### Grid Events
📄 **Read:** [references/grid-events.md](references/grid-events.md)
- Data binding events
- Action events
- Editing events
- Selection events
- Column events
- Sorting and filtering events
- Grouping events
- Row events
- Cell events
- Export and print events
- Menu events
- Template events
- Batch mode events
- Lifecycle events

### Grid Methods
📄 **Read:** [references/grid-methods.md](references/grid-methods.md)
- Record management methods
- Cell and row methods
- Selection methods
- Column methods
- Sorting and filtering methods
- Grouping methods
- Paging methods
- Export and print methods
- Data binding methods
- Search methods
- Editing methods
- Template and lifecycle methods
- UI control methods
- Utility methods

### Testing the Vue Grid with Jest
📄 **Read:** [references/test-case.md](references/test-case.md)
- Setup Jest environment
- Adding Grid component
- Creating test cases
- Snapshot testing
- DOM testing
- Running tests

## Quick Start Example

```vue
<template>
  <div id="app">
    <ejs-grid :dataSource="data" :allowPaging="true" :allowSorting="true" :allowFiltering="true">
      <e-columns>
        <e-column field="OrderID" headerText="Order ID" textAlign="right" width="100"></e-column>
        <e-column field="CustomerID" headerText="Customer ID" width="100"></e-column>
        <e-column field="OrderDate" headerText="Order Date" type="date" format="yMd" width="130"></e-column>
        <e-column field="Freight" headerText="Freight" type="number" format="C2" width="100"></e-column>
      </e-columns>
    </ejs-grid>
  </div>
</template>

<script setup>
import { GridComponent as EjsGrid, ColumnDirective as EColumn, ColumnsDirective as EColumns, Page, Sort, Filter } from "@syncfusion/ej2-vue-grids";
import { data } from './datasource.js';
import { provide } from 'vue';

provide('grid', [Page, Sort, Filter]);
</script>

<style>
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-vue-grids/styles/material3.css";
</style>
```

## Common Patterns

### Pattern 1: Grid with CRUD Operations
1. Enable `editSettings` (allowEditing, allowAdding, allowDeleting)
2. Configure `toolbar` with Edit, Add, Delete, Update, Cancel items
3. Set primary key with `isPrimaryKey: true`
4. Handle `actionComplete` event for server updates
5. Use `allowPaging` for large datasets

### Pattern 2: Data-Driven Grid with Filtering & Sorting
1. Bind `dataSource` to DataManager with remote data
2. Enable `allowSorting` and `allowFiltering`
3. Configure column `type` for proper filter UI
4. Use `filterSettings` for default filters
5. Enable search with `toolbar: ['Search']`

### Pattern 3: Grouped Data with Aggregates
1. Enable `allowGrouping` and inject `Group` module
2. Set `groupSettings` with column names
3. Add `e-aggregates` with aggregate columns
4. Define `footerTemplate` for summary display
5. Use `groupCaptionTemplate` for group headers

## Key Props Reference

**Essential Grid Props:**
- `dataSource` - Data source (array, DataManager, or URL)
- `allowPaging` - Enable paging (boolean)
- `pageSettings` - Pager configuration
- `allowSorting` - Enable sorting (boolean)
- `allowFiltering` - Enable filtering (boolean)
- `allowGrouping` - Enable grouping (boolean)
- `allowSelection` - Enable row selection (boolean)
- `selectionSettings` - Selection configuration
- `editSettings` - CRUD configuration
- `toolbar` - Toolbar items
- `height` - Grid height (pixel or percentage)
- `enableVirtualization` - Virtual scrolling

**Column Props:**
- `field` - Data field binding
- `headerText` - Column header text
- `width` - Column width (pixel or percentage)
- `type` - Column data type (string, number, date, boolean, checkbox)
- `isPrimaryKey` - Primary key column identifier
- `allowSorting` - Allow sorting on column
- `allowFiltering` - Allow filtering on column
- `template` - Custom cell template
- `editTemplate` - Custom edit template

## Top Use Cases

1. **E-Commerce Product Management**: Display products with sorting, filtering, editing, and Excel export
2. **Financial Reporting**: Group data by category, show aggregates (Sum, Average), export to PDF
3. **CRM Dashboard**: Multi-column filtering, row selection for bulk actions, virtual scrolling
4. **Performance Monitoring**: Real-time grid updates, virtual scrolling for 10K+ rows
5. **Admin Panels**: Inline editing with validation, hierarchical data, state persistence
6. **Data Analytics**: Complex grouping, aggregates, templates for custom visualizations
7. **Inventory Systems**: Batch editing, search, export, database connectivity
8. **Survey/Form Collection**: Dialog editing, custom validators, PDF export

---

## Module Injection

Most advanced features require module injection in the `provide` section:

```javascript
provide('grid', [
  Page,           // Paging
  Sort,           // Sorting
  Filter,         // Filtering
  Search,         // Search feature
  Group,          // Grouping
  Aggregate,      // Aggregates
  Edit,           // CRUD editing
  ExcelExport,    // Excel export
  PdfExport,      // PDF export
  Resize,         // Column resize
  Reorder,        // Column reorder
  ColumnMenu,     // Column menu
  Selection,      // Row selection
  Toolbar,        // Toolbar
  CommandColumn   // Command column
])
```
