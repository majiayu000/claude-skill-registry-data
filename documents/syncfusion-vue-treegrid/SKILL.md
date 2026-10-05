---
name: syncfusion-vue-treegrid
description: Implements Syncfusion Vue TreeGrid for hierarchical data with sorting, filtering, editing, exporting, paging, virtual scrolling, and advanced features. Supports configuration, CRUD, aggregates, templates, state persistence, and performance optimization in Vue applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "grids"
---

# Implementing Syncfusion Vue TreeGrid

The Syncfusion Vue TreeGrid is a powerful data visualization component for displaying hierarchical data in a tree-like structure with grid functionality. It provides features for sorting, filtering, editing, exporting, and advanced data management.

## ⚠️ Security & Trust Boundary
 
- The TreeGrid skill does not perform any remote data access.
- All external API interaction is handled by a separate DataManager skill outside this skill’s trust boundary.

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Vue 3 Setup](#vue-3-setup)
- [Vue 2 Setup](#vue-2-setup)
- [API Reference](#api-reference)
- [Data Structure & Binding](#data-structure--binding)
- [Columns & Configuration](#columns--configuration)
- [Frozen Columns & Rows](#frozen-columns--rows)
- [Row Management & Features](#row-management--features)
- [Data Operations](#data-operations)
- [Scrolling & Large Data Handling](#scrolling--large-data-handling)
- [Editing & Validation](#editing--validation)
- [Toolbar & Commands](#toolbar--commands)
- [Export & Reports](#export--reports)
- [Performance & Display](#performance--display)
- [Appearance & Interaction](#appearance--interaction)
- [Advanced Features & Configuration](#advanced-features--configuration)
- [Modules](#modules)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)

## When to Use This Skill

Use this skill when you need to:
- Display hierarchical or tree-structured data in a Vue application
- Implement data editing, sorting, filtering, or searching functionality
- Export data to Excel or PDF formats
- Create responsive data tables with advanced features
- Handle large datasets with virtual scrolling or pagination
- Implement row selection, cell templates, and custom styling
- Add keyboard navigation, drag-and-drop, and context menus
- Fine-tune performance for complex data scenarios

## Vue 3 Setup

📄 **Read** [references/getting-started-vue3.md](references/getting-started-vue3.md)
- Installation and package setup for Vue 3
- Composition API setup
- Data binding with Vue 3
- Tree structure concepts

## Vue 2 Setup

📄 **Read** [references/getting-started-vue2.md](references/getting-started-vue2.md)
- Installation and package setup for Vue 2
- Basic TreeGrid configuration
- Data binding fundamentals
- Tree structure concepts

## API Reference

Complete API documentation for all TreeGrid properties, methods, and events:

📄 **Properties:** [references/properties.md](references/properties.md)
- TreeGrid configuration properties
- Option types and defaults

📄 **Methods:** [references/methods.md](references/methods.md)
- TreeGrid methods for programmatic operations
- Method signatures and parameters

📄 **Events:** [references/events.md](references/events.md)
- TreeGrid events and event handlers
- Event trigger points


## Data Structure & Binding

📄 **Read:** [references/data-handling.md](references/data-handling.md)
- Local and remote data source binding
- Complex data binding with dot notation
- Dynamic data updates and state persistence
- Hierarchical data structure setup

## Columns & Configuration

📄 **Read:** [references/columns.md](references/columns.md)
- Column definitions and properties
- Column formatting and custom headers
- Headers and custom header templates

### Column Features

📄 **Read:** [references/column-resizing.md](references/column-resizing.md)
- Column resizing strategies and configuration
- Min and max width constraints
- Auto-fit and manual resize modes

📄 **Read:** [references/column-reorder.md](references/column-reorder.md)
- Column reordering and drag-drop configuration
- Reorder events and state persistence
- Programmatic reordering methods

📄 **Read:** [references/column-spanning.md](references/column-spanning.md)
- Column span configuration for merged cells
- Spanning rules and constraints
- Complex spanning scenarios

📄 **Read:** [references/column-menu.md](references/column-menu.md)
- Column menu configuration and customization
- Menu items and filtering from column menu
- Column menu events

📄 **Read:** [references/column-chooser.md](references/column-chooser.md)
- Column chooser for showing/hiding columns
- Column chooser configuration and styling
- Programmatic column visibility control

## Frozen Columns & Rows

📄 **Read:** [references/frozen-rows-and-columns.md](references/frozen-rows-and-columns.md)
- Frozen column configuration
- Frozen row configuration
- Left and right freezing
- Scrolling with frozen columns and rows

## Row Management & Features

📄 **Read:** [references/row.md](references/row.md)
- Row detail templates for expanded content
- Row indentation controls
- Row styling and templates

📄 **Read:** [references/selection.md](references/selection.md)
- Cell and row selection modes
- Checkbox selection configuration
- Selection events and state management
- Programmatic selection methods

## Data Operations

### Sorting

📄 **Read:** [references/sorting.md](references/sorting.md)
- Single and multi-column sorting
- Sort direction and initial sort configuration
- Sort methods and programmatic sorting
- Sort event handling

### Searching

📄 **Read:** [references/searching.md](references/searching.md)
- Column-based searching
- Global search across all columns
- Real-time search filtering
- Search methods and options

### Filtering

📄 **Read:** [references/filtering.md](references/filtering.md)
- Filter bar, filter menu, and excel-like filters
- Filter configuration and templates
- Advanced filtering with custom predicates
- Programmatic filtering methods

### Aggregation

📄 **Read:** [references/aggregation.md](references/aggregation.md)
- Aggregate types (sum, average, count, min, max)
- Footer aggregates and custom aggregate templates
- Aggregate configuration per column
- Dynamic aggregate updates

### Paging

📄 **Read:** [references/paging.md](references/paging.md)
- Paging setup and configuration
- Page size modes (All vs Root level)
- Programmatic page navigation
- Pager customization

## Scrolling & Large Data Handling

### Virtual Scrolling

📄 **Read:** [references/virtual-scrolling.md](references/virtual-scrolling.md)
- Virtual scrolling architecture and performance
- Row height and buffer configuration
- Dynamic row height handling
- Memory optimization with virtual scrolling

### Infinite Scrolling

📄 **Read:** [references/infinite-scrolling.md](references/infinite-scrolling.md)
- Infinite scroll loading for large datasets
- Load event and data fetching
- Real-time loading indicators
- Memory management patterns

## Editing & Validation

📄 **Read:** [references/editing.md](references/editing.md)
- Inline editing, dialog editing, and batch editing modes
- Cell editing and row editing workflows
- Command column with action buttons
- Edit event handling and custom validators

📄 **Read:** [references/validation.md](references/validation.md)
- Edit validation rules and patterns
- Custom validators and error handling
- Validation triggers (blur, submit, etc.)
- Server-side validation integration

## Toolbar & Commands

📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items (Add, Edit, Delete, Export)
- Custom toolbar buttons and actions
- Toolbar templates and styling
- Search and filtering from toolbar
- Toolbar events and interaction

## Export & Reports

### Excel Export

📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Excel export functionality and configuration
- Headers and footers in Excel exports
- Cell style customization
- Server-side export options

### PDF Export

📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- PDF export functionality and configuration
- Headers and footers in PDF exports
- Page orientation and custom styling
- Server-side export options

## Performance & Display

📄 **Read:** [references/immutable.md](references/immutable.md)
- Immutable data handling patterns
- Change detection with immutable data
- Performance benefits of immutable mode
- Implementation strategies

📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Virtual scrolling for large datasets
- Infinite scroll loading
- Horizontal and vertical scrolling
- Frozen columns and rows

## Appearance & Interaction

📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS customization and styling
- Theme modes and responsive design
- Adaptive UI rendering
- Cell features (wrapping, clipping, alignment)

📄 **Read:** [references/adaptive.md](references/adaptive.md)
- Adaptive UI behavior
- Responsive design patterns
- Mobile-friendly configurations

📄 **Read:** [references/cell.md](references/cell.md)
- Cell properties and configuration
- Cell templates and styling
- Cell interactions and editing

📄 **Read:** [references/keyboard-navigation.md](references/keyboard-navigation.md)
- Keyboard shortcuts and navigation patterns
- Custom keyboard handlers
- Accessibility considerations
- Navigation between cells and rows

📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Context menu configuration
- Custom menu items and actions
- Menu event handling

📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy/paste operations
- Clipboard configuration
- Data transfer handling

## Advanced Features & Configuration

📄 **Read:** [references/print.md](references/print.md)
- Print functionality
- Page layout and orientation
- Print styling and customization

📄 **Read:** [references/loading-animation.md](references/loading-animation.md)
- Loading animation configuration
- State indicators and visual feedback
- Custom loading templates

📄 **Read:** [references/localization.md](references/localization.md)
- Localization and internationalization
- Language configuration
- Translation of UI text

### State Persistence

📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- Persisting grid state (columns, sorting, filtering, selection)
- Local storage and session storage options
- State restoration on page reload
- Best practices for state management

## Modules

📄 **Read:** [references/modules.md](references/modules.md)
- Module injection and dependency resolution
- Available modules (Sort, Filter, Page, Edit, etc.)
- Tree Grid specific modules
- Performance impact of module selection

## Quick Start Example

```vue
<template>
  <ejs-treegrid :dataSource="data" :columns="columns" :treeColumnIndex="0" 
    :allowPaging="true" :pageSettings="pageSettings" :allowSorting="true">
  </ejs-treegrid>
</template>

<script setup>
import { ej2grid } from '@syncfusion/ej2-vue-grids';
import { provide } from 'vue';
import { TreeGridComponent as EjsTreegrid, Inject, Page, Sort } from '@syncfusion/ej2-vue-treegrid';

const data = [
  { TaskID: 1, TaskName: 'Planning', Duration: 10 },
  { TaskID: 2, TaskName: 'Design', Duration: 5 },
];

const columns = [
  { field: 'TaskID', headerText: 'Task ID', width: 90 },
  { field: 'TaskName', headerText: 'Task Name', width: 150 },
  { field: 'Duration', headerText: 'Duration', width: 100 },
];

const pageSettings = { pageSize: 10 };

provide('treegrid', [Page, Sort]);
</script>
```

For complete working examples, visit: `../code-snippet/treegrid/`

## Common Patterns

### Pattern 1: Editable Data Grid with Validation
1. Enable editing via `allowEditing`
2. Set edit mode (inline or dialog)
3. Configure `editSettings`
4. Add `Inject` with Edit module
5. Reference: `code-snippet/treegrid/editing/`

### Pattern 2: Filterable & Sortable List
1. Enable filtering with `allowFiltering`
2. Enable sorting with `allowSorting`
3. Configure filter settings
4. Reference: `code-snippet/treegrid/filtering/`, `code-snippet/treegrid/sorting/`

### Pattern 3: Paginated Large Dataset
1. Enable paging with `allowPaging`
2. Configure `pageSettings` with page size
3. Bind to remote data source
4. Reference: `code-snippet/treegrid/paging/`, `code-snippet/treegrid/data-binding/`

### Pattern 4: Excel Report Export
1. Configure TreeGrid with data
2. Call `excelExport()` method
3. Customize headers, footers, styling
4. Reference: `code-snippet/treegrid/excel/`

### Pattern 5: Advanced Selection
1. Set selection mode (row, cell, or checkbox)
2. Configure checkbox selection column
3. Handle selection events
4. Reference: `code-snippet/treegrid/selection/`

