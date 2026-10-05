---
name: syncfusion-vue-kanban
description: "Implements the Syncfusion Vue Kanban component for column-based task board UIs with drag-and-drop, swimlanes, WIP constraints, and virtual scrolling. Use this when building sprint boards, kanban boards, workflow trackers, or any column-based task management UI. Covers data binding (local and remote), cards, columns, dialog, events, and accessibility."
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion Vue Kanban

A column-based task board that groups cards by a status field, supports drag-and-drop reordering,
swimlane row grouping, column validation (WIP limits), and virtual scrolling for large datasets.

## When to Use This Skill

- User needs a Kanban / sprint board with status columns (To Do, In Progress, Done, etc.)
- User wants drag-and-drop card movement between columns or across swimlane rows
- User needs to bind Kanban to a REST API, OData, or local JSON dataset
- User wants to group cards by assignee, team, or any field (swimlanes)
- User needs WIP limits (min/max card counts per column)
- User wants virtual scrolling for 1000+ cards without performance issues
- User wants to customize card layout with a template or apply custom CSS

## Component Overview

| Concept | What it does |
|---|---|
| `keyField` | Board-level field that maps data records to columns (e.g. `"Status"`) |
| `cardSettings` | Specifies `headerField` (unique ID) and `contentField` (body text) |
| `<e-columns>` | Declare each board column; `keyField` on column matches data values |
| `swimlaneSettings` | Groups cards into horizontal rows by a data field |
| `allowDragAndDrop` | Enables/disables card drag between columns (default: `true`) |
| `enableVirtualization` | Enables virtual scrolling for large datasets |

## Documentation and Navigation Guide

### Component Overview
📄 **Read:** [references/overview.md](references/overview.md)
- Full feature list with descriptions (drag-and-drop, swimlanes, WIP, virtual scrolling, etc.)
- When-to-use decision table matching user needs to features
- Package installation and all required CSS imports
- Minimal working example

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance summary
- All WAI-ARIA attributes (`aria-label`, `aria-expanded`, `aria-selected`, `aria-grabbed`, etc.)
- Full keyboard shortcut reference
- Disabling keyboard interaction (`allowKeyboard: false`)
- Screen reader support details
- RTL accessibility with `enableRtl`
- Testing with axe-core and accessibility checker tools

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vite + Vue 3 project setup
- Package installation (`@syncfusion/ej2-vue-kanban`)
- CSS imports (tailwind3 theme)
- Minimal Kanban with columns
- Populating cards from a local data array
- Enabling swimlanes on first render

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding local JSON arrays
- Remote data with `DataManager` + `ODataAdaptor` / `ODataV4Adaptor`
- Web API binding with `WebApiAdaptor`
- CRUD operations with `UrlAdaptor` (`insertUrl`, `updateUrl`, `removeUrl`)
- Custom adaptor by extending `ODataAdaptor`
- Sending extra query parameters with `Query.addParams`
- Loading data dynamically via Ajax
- Handling HTTP errors with `actionFailure`

### Cards
📄 **Read:** [references/cards.md](references/cards.md)
- `headerField` (mandatory unique ID) and `contentField`
- Hiding the card header with `showHeader: false`
- Custom card layout using Vue component template
- Card selection: None / Single / Multiple (`selectionType`)
- Multi-select with Ctrl+click / Shift+click

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Single-key and multi-key column mapping
- Column header text and header templates
- Toggle columns (expand/collapse) with `allowToggle`
- Rendering a column initially collapsed (`isExpanded: false`)
- Stacked headers grouping multiple columns
- Column-level drag-and-drop reordering (`allowColumnDragAndDrop`)

### Dialog (Add / Edit / Delete Cards)
📄 **Read:** [references/dialog.md](references/dialog.md)
- Default built-in dialog (double-click to open)
- Custom dialog fields with `dialogSettings.fields`
- Custom field labels and field types
- Field validation with `validationRules`
- Full dialog template using Vue component
- Preventing dialog open with `dialogOpen` event
- Programmatic `openDialog()` and `closeDialog()`

### Dimensions (Height and Width)
📄 **Read:** [references/dimensions.md](references/dimensions.md)
- Auto height/width (default)
- Pixel dimensions (`height="550px"`, `:width="650"`)
- Percentage dimensions (`width="100%"`, `height="100%"`)
- When to use each mode

### Events
📄 **Read:** [references/events.md](references/events.md)
- Action events: `actionBegin`, `actionComplete`, `actionFailure`
- Card events: `cardClick`, `cardDoubleClick`, `cardRendered`
- Column drag events: `columnDragStart`, `columnDrag`, `columnDrop`
- Data events: `dataBinding`, `dataBound`, `dataSourceChanged`, `dataStateChange`
- Dialog events: `dialogOpen`, `dialogClose`
- Card drag events: `dragStart`, `drag`, `dragStop`
- Lifecycle: `created`, `queryCellInfo`

### Swimlanes
📄 **Read:** [references/swimlane.md](references/swimlane.md)
- Rendering swimlane rows with `swimlaneSettings.keyField`
- Custom row label text with `textField`
- Custom swimlane header template
- Sorting rows (Ascending / Descending)
- Cross-row drag-and-drop (`allowDragAndDrop: true` in swimlaneSettings)
- Empty row display (`showEmptyRow`)
- Card count badge (`showItemCount`)
- Frozen swimlane header while scrolling (`enableFrozenRows`)

### Drag and Drop
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Disabling drag-and-drop globally (`allowDragAndDrop: false`)
- Per-column drag/drop control (`allowDrag`, `allowDrop`)
- Cross-swimlane drag-and-drop
- Kanban-to-Kanban drag-and-drop (`externalDropId`, `dragStop`, `addCard`, `deleteCard`)
- Kanban to TreeView drag-and-drop
- Kanban to Scheduler drag-and-drop

### Localization and RTL
📄 **Read:** [references/localization.md](references/localization.md)
- All locale keys reference table
- Loading translations with `L10n.load()`
- Setting `locale` prop on the board
- Right-to-left (RTL) mode with `enableRtl`

### Public Methods
📄 **Read:** [references/methods.md](references/methods.md)
- Card CRUD: `addCard`, `updateCard`, `deleteCard`, `getCardDetails`
- Column methods: `addColumn`, `deleteColumn`, `showColumn`, `hideColumn`, `getColumnData`
- Dialog: `openDialog`, `closeDialog`
- Data: `getSwimlaneData`
- Selection: `getSelectedCards`
- UI: `refreshHeader`, `refreshUI`, `showSpinner`, `hideSpinner`, `destroy`

### State Persistence
📄 **Read:** [references/persistence.md](references/persistence.md)
- Enabling `enablePersistence` to save state in `localStorage`
- Persisted state: data source, column expand/collapse, swimlane expand/collapse
- Setting a unique `id` to avoid key collisions
- Clearing persisted state

### Priority and Sort Settings
📄 **Read:** [references/priority-and-sort.md](references/priority-and-sort.md)
- `cardSettings.priority` for rank-based card positioning
- `sortSettings.sortBy`: `'Index'`, `'DataSourceOrder'`, `'Custom'`
- `sortSettings.field` for field-mapped ordering
- `sortSettings.direction`: `'Ascending'` / `'Descending'`

### Responsive Mode
📄 **Read:** [references/responsive-mode.md](references/responsive-mode.md)
- Mobile layout: column sizing, swipe navigation, tap-and-hold drag
- Swimlane popup menu on mobile
- Single and multiple card selection on touch devices

### Tooltip
📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Enabling default card tooltip (`enableTooltip`)
- `e-tooltip-text` class for custom element tooltips
- Custom tooltip template via `tooltipTemplate`

### Customization and Troubleshooting
📄 **Read:** [references/customization-and-troubleshooting.md](references/customization-and-troubleshooting.md)
- CSS class reference table
- Sticky/fixed column headers
- Column WIP validation (`minCount`, `maxCount`, `constraintType`)
- WAI-ARIA attributes
- Full keyboard shortcut reference
- Theme Studio

### Virtual Scrolling
📄 **Read:** [references/virtual-scrolling.md](references/virtual-scrolling.md)
- Enabling virtualization (`enableVirtualization: true`)
- Setting `cardHeight` in pixels
- Remote data service configuration for virtual scrolling
- Known limitations (swimlane + virtualization, card position, % height)

### How-To Recipes
📄 **Read:** [references/how-to.md](references/how-to.md)
- Dynamically change column properties at runtime
- Replace all columns at runtime
- Filter cards with a `Query`
- Search cards by text with `Query.search()`
- Handle column header double-click

### Properties Reference
📄 **Read:** [references/properties.md](references/properties.md)
- Complete root-level prop table (all types, defaults, descriptions)
- `cardSettings` sub-properties (`headerField`, `contentField`, `selectionType`, `priority`, etc.)
- `columns` sub-properties (`keyField`, `allowToggle`, `minCount`, `maxCount`, `transitionColumns`, etc.)
- `dialogSettings` and `DialogFieldsModel` fields
- `sortSettings`, `swimlaneSettings`, `stackedHeaders` interfaces
- All enum values: `SelectionType`, `ConstraintType`, `SortOrderBy`, `SortDirection`

### Style and CSS Customization
📄 **Read:** [references/style.md](references/style.md)
- Full CSS class reference table for header cells and WIP limit indicators
- CSS classes for card elements (header, content, footer, tags, color stripe)
- Swimlane row and cell CSS selectors
- Compact table-scoped selector variants
- Fixed / sticky Kanban header (height-based and `position: sticky`)
- Theme Studio for generating custom themes

### Validation (WIP Limits)
📄 **Read:** [references/validation.md](references/validation.md)
- `minCount` — minimum cards required per column/cell
- `maxCount` — maximum cards allowed per column/cell
- `constraintType`: `'Column'` (default) vs `'Swimlane'` scope
- Visual feedback: highlight colors when limits are violated
- CSS classes to customize validation highlight colors

## Quick Start

```vue
<template>
  <div id="app">
    <ejs-kanban id="kanban" keyField="Status" :dataSource="kanbanData" :cardSettings="cardSettings">
      <e-columns>
        <e-column headerText="To Do"       keyField="Open"></e-column>
        <e-column headerText="In Progress" keyField="InProgress"></e-column>
        <e-column headerText="Testing"     keyField="Testing"></e-column>
        <e-column headerText="Done"        keyField="Close"></e-column>
      </e-columns>
    </ejs-kanban>
  </div>
</template>

<script setup>
import { KanbanComponent as EjsKanban, ColumnDirective as EColumn, ColumnsDirective as EColumns }
  from '@syncfusion/ej2-vue-kanban';
import { extend } from '@syncfusion/ej2-base';

const rawData = [
  { Id: 1, Status: 'Open',       Summary: 'Analyze requirements', Assignee: 'Nancy' },
  { Id: 2, Status: 'InProgress', Summary: 'Improve performance',  Assignee: 'Andrew' },
  { Id: 3, Status: 'Testing',    Summary: 'Fix IE browser bug',   Assignee: 'Janet' },
  { Id: 4, Status: 'Close',      Summary: 'Deploy to production', Assignee: 'Nancy' },
];

const kanbanData = extend([], rawData, null, true);
const cardSettings = { contentField: 'Summary', headerField: 'Id' };
</script>

<style>
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-vue-kanban/styles/tailwind3.css';
</style>
```

## Common Patterns

### Add swimlanes (group by assignee)

```vue
<ejs-kanban keyField="Status" :dataSource="kanbanData"
  :cardSettings="cardSettings" :swimlaneSettings="swimlaneSettings">
  ...columns...
</ejs-kanban>

<script setup>
const swimlaneSettings = { keyField: 'Assignee' };
</script>
```

### Bind to remote OData service

```vue
<script setup>
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';

const kanbanData = new DataManager({
  url: 'https://your-api.com/api/Tasks',
  adaptor: new ODataAdaptor(),
  crossDomain: true
});
</script>
```

### Enable WIP limits on a column

```vue
<e-column headerText="In Progress" keyField="InProgress" :maxCount="5" :minCount="1"></e-column>
```

### Enable virtual scrolling for large data

```vue
<ejs-kanban :enableVirtualization="true" keyField="Status" :dataSource="largeDataset"
  :cardSettings="{ headerField: 'Id', contentField: 'Summary' }">
  ...
</ejs-kanban>
```

## Key Props Reference

| Prop | Type | Purpose |
|---|---|---|
| `keyField` | String | Data field that maps records to columns |
| `dataSource` | Array / DataManager | Cards data source |
| `cardSettings` | Object | `headerField` (required), `contentField`, `template`, `selectionType` |
| `swimlaneSettings` | Object | `keyField`, `textField`, `allowDragAndDrop`, `showEmptyRow`, `enableFrozenRows` |
| `allowDragAndDrop` | Boolean | Board-level card drag-and-drop (default: `true`) |
| `allowColumnDragAndDrop` | Boolean | Reorder columns by dragging headers |
| `enableVirtualization` | Boolean | Virtual scrolling for large datasets |
| `enableTooltip` | Boolean | Show tooltip on card hover |
| `constraintType` | String | `'Column'` or `'Swimlane'` for WIP validation |
