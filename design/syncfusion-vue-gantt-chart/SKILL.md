---
name: syncfusion-vue-gantt-chart
description: "Implement Syncfusion Vue Gantt Chart (@syncfusion/ej2-vue-gantt) for Vue 2 and Vue 3. Use this when building project scheduling interfaces with task timelines, dependencies, and resource management. Covers data binding, task scheduling, columns, filtering, editing, Excel/PDF export, critical path, and resource allocation. Supports ejs-gantt and GanttComponent."
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Implementing Syncfusion Vue Gantt Chart

A project management component that renders a Microsoft Project-like interface for scheduling and managing tasks, dependencies, and resources in Vue 2 and Vue 3 applications.

## When to Use This Skill

Use this skill when the user needs to:
- **Set up the Gantt Chart** in a Vue 2 (Vue CLI) or Vue 3 (Vite) project
- **Bind data** — local arrays, self-referential data, or remote DataManager sources
- **Schedule tasks** — auto/manual modes, duration, baselines, unscheduled tasks, work calendar
- **Manage task dependencies** — FS, FF, SS, SF predecessor types, connector lines
- **Edit tasks** — cell editing, dialog editing, taskbar drag/resize, adding/deleting rows, indent/outdent
- **Work with resources** — assign resources, resource view, multi-taskbar view
- **Configure columns** — reorder, resize, freeze, span, templates, WBS, checkbox
- **Customize the timeline** — top/bottom tiers, zooming, time units (hour to decade), infinite scrolling
- **Filter and sort** — column menu filter, Excel-like filter, toolbar search, sorting
- **Select rows or cells** — row/cell selection, selection events
- **Use the toolbar** — built-in items (Add, Edit, Delete, Search, ExpandAll…) and custom items
- **Customize taskbars and labels** — templates, data markers/indicators, tooltips (taskbar / connector line / baseline / timeline), label settings
- **Add event markers and holidays** — project milestone lines, non-working days
- **Export** — Excel (single/multiple Gantt, custom data) and PDF (headers, footers, custom)
- **Control layout** — splitter position, loading animation, state persistence
- **Undo / Redo** actions in the Gantt
- **Enable virtual scrolling** for large datasets
- **Configure timezone and globalization** — locale, RTL, timezone offset
- **Context menu** — right-click quick actions for rows and column headers
- **Critical path** — highlight tasks that determine the project end date

## Component Overview

| Feature | Module to Inject | Key Property / API |
|---|---|---|
| Editing | `Edit` | `editSettings` |
| Filtering | `Filter` | `allowFiltering` |
| Sorting | `Sort` | `allowSorting` |
| Selection | `Selection` | `selectionSettings` |
| Toolbar | `Toolbar` | `toolbar` |
| Day Markers | `DayMarkers` | `eventMarkers`, `holidays` |
| Excel Export | `ExcelExport` | `excelExport()` |
| PDF Export | `PdfExport` | `pdfExport()` |
| Virtual Scroll | `VirtualScroll` | `enableVirtualization` |
| Critical Path | `CriticalPath` | `enableCriticalPath` |
| Undo / Redo | `UndoRedo` | `enableUndoRedo`, `undoRedoStepsCount`, `undoRedoActions` |
| Column Menu | `ColumnMenu` | `showColumnMenu` |
| Context Menu | `ContextMenu` | `contextMenuItems` |

**Package:** `@syncfusion/ej2-vue-gantt`  
**Component tag:** `<ejs-gantt>`  
**Composition API import:** `GanttComponent as EjsGantt`  
**Options API component key:** `'ejs-gantt': GanttComponent`

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vite (Vue 3) and Vue CLI (Vue 2) project setup
- Installing `@syncfusion/ej2-vue-gantt` and theme package
- CSS reference using Syncfusion theme packages
- Composition API and Options API registration
- Minimal working example with `taskFields`
- Module injection pattern (`provide`)
- Quasar framework setup
- Error handling with `actionFailure`

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local array data (hierarchical and self-referential/flat with `parentID`)
- Remote data with DataManager (ODataV4, WebAPI)
- Remote save persistence with `RemoteSaveAdaptor` (`batchUrl`)
- Sending extra parameters to the server via `load` + `Query.addParams()`
- Handling server exceptions using `actionFailure`
- Binding data from external Ajax requests (local binding)
- Load-on-demand (lazy load child rows)
- Immutable data mode
- Large data virtual scrolling

### Task Scheduling
📄 **Read:** [references/task-scheduling.md](references/task-scheduling.md)
- Auto, Manual, Custom scheduling modes (`taskMode`)
- `Auto` (default): dates validated against working time, holidays, weekends, predecessors
- `Manual`: all dates taken as-is from data source — no auto-adjustment
- `validateManualTasksOnLinking: true` — enforce predecessor dates even in Manual mode
- Custom mode: per-task scheduling via `taskFields.manual` boolean field (`true` = manual)
- `taskFields` mapping (id, name, startDate, endDate, duration, durationUnit, progress, parentID, dependency, work, type, notes, etc.)
- Global duration unit (`durationUnit` — `day`, `hour`, `minute`; default `day`)
- Map per-task duration unit via `taskFields.durationUnit` data field
- Inline duration unit in duration string: `'3days'`, `'12hours'`, `'1800minutes'`
- Unscheduled task types: start-only, end-only, duration-only, milestone (`duration: 0`)
- `allowUnscheduledTasks: false` auto-fills missing dates with duration=1 + project start
- Working time range (`dayWorkingTime` with `from`/`to` — inject `DayMarkers`)
- Per-day working hours (`weekWorkingTime` — overrides `dayWorkingTime` for listed days; unlisted days fall back to `dayWorkingTime`)
- Non-working days: `workWeek` array + `highlightWeekends`
- `includeWeekend: true` to count weekends in duration calculations

### Baseline
📄 **Read:** [references/baseline.md](references/baseline.md)
- Enabling baseline visualization (`renderBaseline: true`)
- Baseline field mapping (`baselineStartDate`, `baselineEndDate`, `baselineDuration`)
- Baseline milestone creation (`baselineDuration: 0`)
- Color customization via `baselineColor` property or `.e-baseline-bar` CSS class
- **Baseline templates** — `baselineTemplate` for custom rendering, multiple baselines per task (original vs revised)
- Template API access to internal metrics (`baselineTop`, `baselineHeight`, `taskBarHeight`, `getTaskLeft()`)
- Render multiple baselines (compare original/revised/draft schedules)
- Best for: schedule variance tracking, milestone planning, phase comparisons

### Task Constraints
📄 **Read:** [references/task-constraints.md](references/task-constraints.md)
- 8 constraint types table: ASAP (0), ALAP (1), MSO (2), MFO (3), SNET (4), SNLT (5), FNET (6), FNLT (7)
- `taskFields.constraintType` — maps numeric constraint type field from data
- `taskFields.constraintDate` — maps the constraint date field from data
- Strict constraint types that trigger violation popup: MSO, MFO, SNLT, FNLT
- `actionBegin` with `requestType === 'validateTaskViolation'` — intercept violations
- `args.validateMode.respectMustStartOn/Off` flags — silent enforcement (suppress popup)
- All four flags: `respectMustStartOn`, `respectMustFinishOn`, `respectStartNoLaterThan`, `respectFinishNoLaterThan`
- Display constraint name as right label via named slot + `data.ganttProperties.constraintType`
- Required modules: `Selection`, `Toolbar`, `DayMarkers`, `Edit`, `Filter`, `Sort`, `ContextMenu`

### Task Dependencies
📄 **Read:** [references/task-dependencies.md](references/task-dependencies.md)
- Predecessor types: FS, SS, FF, SF — format `"{ID}{Type}"` e.g. `"2FS"`, `"3SS"`
- Lag/lead with unit suffix: `"2FS+2days"`, `"4FF+960m"`, `"7SS+16h"`, `"3FS-1days"`
- Multiple predecessors comma-separated: `"2FS,3FF"`
- `taskFields.dependency` — maps predecessor string field
- `allowParentDependency: true` (default) — allow parent-to-parent/child links
- Connector lines render automatically when `dependency` is mapped
- Interactive drawing: drag taskbar handle — requires `Edit` module + `allowTaskbarEditing: true`
- `autoUpdatePredecessorOffset: true` — recalculates offsets on initial load to match calendar-adjusted positions
- Runtime toggle: `this.$refs.gantt.ej2Instances.autoUpdatePredecessorOffset = value`
- `updateOffsetOnTaskbarEdit: false` — disables auto offset update when dragging taskbar
- `actionBegin` with `requestType === 'validateLinkedTask'` — handle dependency validation
- `args.validateMode.respectLink` — revert edit if it violates link
- `args.validateMode.removeLink` — remove link and keep edit
- `args.validateMode.preserveLinkWithEditing` — update offset and keep both (default `true`)
- Validation dialog: shown when all modes disabled; 2 or 3 options depending on direction
- Show/hide lines: `.e-gantt-dependency-view-container` `visibility` CSS toggle

### Managing Tasks (Editing)
📄 **Read:** [references/managing-tasks.md](references/managing-tasks.md)
- Enabling editing (`editSettings`) — inject `Edit` module
- Cell editing (Auto mode), dialog editing, taskbar editing
- Cell edit types: `numericedit`, `dropdownedit`, `booleanedit`, `datepickeredit`, `datetimepickeredit`
- Cell edit template (`create`/`write`/`read`/`destroy` hooks)
- Disable editing for a specific column (`columns.allowEditing: false`)
- Read-only Gantt (`readOnly: true`)
- Adding tasks via toolbar, context menu, or `editModule.addRecord()`
- Open new task dialog with default values (`actionBegin` + `beforeOpenAddDialog`)
- Customize dialog tabs (`addDialogFields` / `editDialogFields` with `fields` and `additionalParams`)
- Customize Notes tab with RTE `inlineMode` via `additionalParams`
- Deleting tasks via toolbar or `editModule.deleteRow()`; confirm dialog with `showDeleteConfirmDialog`
- Indent and outdent — toolbar items or `indent()` / `outdent()` methods
- Splitting tasks at load time — **Hierarchical** (`taskFields.segments` with embedded `Segments` array) or **Self-referential** (`taskFields.segmentId` + `segmentData` flat collection), dynamically via context menu, dialog, or `splitTask()`
- Merging segments via context menu or drag; limitations (no parent/milestone splits)
- Taskbar editing: drag, resize, progress handle, connector points
- Prevent taskbar editing for specific tasks (`taskbarEditing` event + `args.cancel`)
- Hide taskbar edit handles via `queryTaskbarInfo` + CSS `.e-preventEdit`
- Taskbar editing tooltip (`tooltipSettings.editing` template)
- Touch interaction: double-tap, tap-and-drag, connector point tap
- Column validation rules (`columns.validationRules`)
- Custom validation (callback function in `validationRules`)
- Dependency/Resource grid validation via `actionBegin` (`beforeOpenEditDialog`)
- Server-side CRUD with `UrlAdaptor` + `batchUrl` (`added`/`changed`/`deleted` collections)
- `updateRecordByID()`, `addRecord()`, `deleteRecord()`, `indent()`, `outdent()`

### Resources
📄 **Read:** [references/resources.md](references/resources.md)
- Defining resource collection and `resourceFields`
- Assigning resources to tasks (`resourceInfo`)
- Resource view layout
- Multi-taskbar view
- Resource unit and work allocation

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Column definition (`field`, `headerText`, `width`, `format`)
- `ColumnsDirective` / `e-columns` + `e-column` directives
- Column reordering, resizing, spanning
- Frozen columns
- Column menu
- Column templates
- WBS (work breakdown structure) column
- Responsive columns
- Checkbox selection column

### Timeline
📄 **Read:** [references/timeline.md](references/timeline.md)
- `timelineSettings` — top tier and bottom tier units
- Time units: Hour, Day, Week, Month, Year, Decade
- Custom timeline labels / formatters
- Zooming (zoom in, zoom out, zoom to fit)
- `timelineUnitSize`
- `timelineViewMode` shortcut (set both tiers at once)
- `viewStartDate` / `viewEndDate` — fixed visible date range
- `weekStartDay` — custom first day of week (0–6)
- `updateTimescaleView` — auto-update timescale on task changes
- `showTooltip` — timeline cell tooltip on hover
- `showWeekend` — show or hide weekend columns
- `timelineTemplate` — custom cell content for timeline tiers
- `enableInfiniteTimelineScroll` — enable infinite horizontal scrolling (extends timeline dynamically as user navigates)

### Filtering and Sorting
📄 **Read:** [references/filtering-and-sorting.md](references/filtering-and-sorting.md)
- Column menu filtering (`allowFiltering`)
- Excel-like filter
- Toolbar search box
- `filterSettings` configuration
- Column sorting (`allowSorting`)
- Multi-column sorting
- `sortSettings`
- Programmatic `gantt.search(key)` method
- `searchSettings` — fields, operator, ignoreCase
- Keyboard shortcuts for sort add / remove
- Sorting events via `actionBegin` / `actionComplete` (`args.requestType === 'sorting'`)
- Touch sorting: tap column headers; multi-column sorting uses a popup

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- `allowSelection: false` — disable selection
- Selection mode: `'Row'` / `'Cell'` / `'Both'`
- Selection type: `'Single'` / `'Multiple'`
- `selectedRowIndex` — pre-select a row on initial load
- Select rows dynamically (`selectRow`, `selectRows`)
- Select rows based on condition via `dataBound`
- Cell selection — `getSelectedRowCellIndexes()`
- Multiple cell selection with Ctrl+Click
- Select cell dynamically (`selectCell`)
- Toggle selection (`enableToggle`)
- Hover highlighting (`enableHover`)
- `selectionSettings` full reference table
- Programmatic APIs (`clearSelection`, `getSelectedRecords`, `getSelectedRowIndexes`)
- Full events table (rowSelecting, rowSelected, rowDeselecting, rowDeselected, cellSelecting, cellSelected, cellDeselected)
- Prevent row selection via `rowSelecting` (`args.cancel = true`)
- Prevent cell selection via `cellSelecting` (`args.cancel = true`)
- Checkbox selection with `checkboxMode` options
- Touch interaction (single tap + multi-select popup)

### Toolbar
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items: Add, Edit, Update, Delete, Cancel, Search, ExpandAll, CollapseAll, ZoomIn, ZoomOut, ZoomToFit, ExcelExport, PdfExport, PrevTimeSpan, NextTimeSpan, Undo, Redo
- Custom toolbar items with `click` handler
- Toolbar events

### Taskbar and Labels
📄 **Read:** [references/taskbar-and-labels.md](references/taskbar-and-labels.md)
- Taskbar customization (height, color, template)
- `labelSettings` — left, right, taskLabel
- Data markers / indicators
- Task tooltips
- Connector line tooltip
- Baseline tooltip
- Timeline tooltip
- Progress bar customization
- Parent and milestone taskbar appearance

### Event Markers and Holidays
📄 **Read:** [references/event-markers-and-holidays.md](references/event-markers-and-holidays.md)
- `eventMarkers` — vertical lines with labels on key dates
- `holidays` — non-working day highlights
- Working time configuration
- Weekend highlights (`highlightWeekends`)
- Inject `DayMarkers` module

### Export (Excel and PDF)
📄 **Read:** [references/export.md](references/export.md)
- Excel export (basic, custom data source, multiple Gantt charts)
- PDF export (basic, header/footer, customization)
- Export properties and callbacks

### Rows and Scrolling
📄 **Read:** [references/rows-and-scrolling.md](references/rows-and-scrolling.md)
- `rowHeight` — uniform row height in pixels (default `46px`)
- `collapseAllParentTasks: true` — start all parents collapsed
- `taskFields.expandState` — map a boolean data field to per-task expand/collapse state
- `expanding` / `collapsing` events — `args.cancel = true` to block specific rows
- `expanded` / `collapsed` events — fire after action (no cancel)
- `rowDataBound` — style entire rows; `queryCellInfo` — style individual cells
- Alternate row styling: `.e-altrow` (grid) + `tr.e-chart-row:nth-child(even)` (chart)
- Row spanning via `queryCellInfo` `args.rowSpan`
- `columns.clipMode` — `Clip` | `Ellipsis` | `EllipsisWithTooltip` (default)
- Row drag and drop — inject `RowDD`, `Edit`; `allowRowDragAndDrop: true`
- `allowTaskbarDragAndDrop` — taskbar position drag between rows
- `rowDragStartHelper` — prevent drag conditionally via `args.cancel`
- `rowDrop` — validate/cancel drop; `args.dropPosition` = `'above'|'below'|'child'`
- `reorderRows(fromIndexes, toIndex, position)` — programmatic row reorder
- `scrollToDate('MM/DD/YYYY')` — scroll timeline to a date
- `scrollToTask('id')` — scroll chart to a task's taskbar
- `setScrollTop(px)` — vertical scroll; also via `ganttChartModule.scrollObject.setScrollTop()`
- Responsive container: `height: '100%'`, `width: '100%'` (parent needs explicit height)
- Virtual scrolling: `enableVirtualization: true`, inject `VirtualScroll`
- `enableTimelineVirtualization` — render only visible timeline columns

### Layout and Splitter
📄 **Read:** [references/layout-and-splitter.md](references/layout-and-splitter.md)
- `splitterSettings` — column index or position
- Loading animation
- State persistence (`enablePersistence`)
- localStorage key format (`'gantt' + componentId`)
- Get / set persisted state manually
- Prevent specific properties from persisting (`addOnPersist` override)
- Restore header templates after reload (`getPersistData` + `treeGrid.setProperties`)
- What does NOT persist (column template, headerText, headerTemplate, formatter, valueAccessor)
- Global and local context configuration
- Height, width, and responsive layout

### Undo / Redo
📄 **Read:** [references/undo-redo.md](references/undo-redo.md)
- Enabling undo/redo (`enableUndoRedo: true`, inject `UndoRedo`)
- `undoRedoStepsCount` — history depth
- `undoRedoActions` — restrict which actions are tracked
- Full supported actions table (19 action types including ZoomIn/Out, ColumnResize, etc.)
- Toolbar Undo/Redo items
- Programmatic `undo()` / `redo()`
- `getUndoActions()` / `getRedoActions()`
- `clearUndoCollection()` / `clearRedoCollection()`

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 Level AA compliance
- Keyboard navigation (grid, toolbar, context menu shortcuts)
- ARIA roles and attributes (treegrid, row, gridcell, columnheader, dialog)
- Theme support (tailwind3, material, material3, bootstrap5, fluent, fabric, highcontrast) via npm theme packages
- Screen reader support (NVDA, JAWS, VoiceOver) — taskbarAriaLabel customization via queryTaskbarInfo
- Focus management and autoFocusTasks

### Programmatic Methods
📄 **Read:** [references/gantt-methods.md](references/gantt-methods.md)
- Access instance via `this.$refs.gantt` (Options API) — `ref="gantt"` on `<ejs-gantt>`
- **Column:** `autoFitColumns(fieldNames?)`, `getGanttColumns()`, `getGridColumns()`, `refreshColumns()`, `reorderColumns(from, to)`
- **Task editing:** `cancelEdit()`, `changeTaskMode(data)`, `convertToMilestone(id)`, `deleteRecord(taskDetail)`, `updateRecordByIndex(index, data)`, `updateTaskId(currentId, newId)`
- **Row expand/collapse:** `expandByID()`, `expandByIndex()`, `collapseByID()`, `collapseByIndex()`
- **Split/Merge:** `splitTask(taskId, splitDate)`, `mergeTask(taskId, segmentIndexes)`
- **Predecessor:** `removePredecessor(id)`
- **Querying:** `getRecordByID(id)`, `getRecordByIndex()`, `getTaskByUniqueID(id)`, `getTaskInfo(taskId)`, `getCurrentViewData()`, `getExpandedRecords(records)`, `getCriticalTasks()`
- **DOM access:** `getRowByID(id)`, `getRowByIndex(index)`, `getTaskbarHeight()`
- **Formatting helpers:** `getDurationString(duration, unit)`, `getWorkString(work, unit)`
- **Scroll:** `scrollToTask(taskId)`, `setScrollTop(scrollTop)`, `updateChartScrollOffset(left, top)`
- **Data:** `updateDataSource(dataSource, args)`
- **Sort:** `removeSortColumn(columnName)`
- **Selection:** `selectCells(rowCellIndexes)` — requires `selectionSettings.mode: 'Cell'`

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Inject `ContextMenu`, `Edit`, `Sort`, `Resize`, `Selection` modules
- Enable: `enableContextMenu: true`, `allowSorting: true`, `allowResizing: true`
- Default built-in items table: `AutoFit`, `AutoFitAll`, `SortAscending`, `SortDescending`, `TaskInformation`, `Add`, `Indent`, `Outdent`, `DeleteTask`, `Save`, `Cancel`, `DeleteDependency`, `Convert`
- Custom items: mix built-in strings + descriptor objects `{ text, id, target, iconCss }`
- `target: '.e-content'` restricts item to row right-click; `target: '.e-gridheader'` to header
- `contextMenuClick` event — handle custom actions via `args.item.id`
- `contextMenuOpen` event — hide items dynamically via `args.hideItems`; check `args.type !== 'Header'`
- Touch: long press on a row to open context menu

### Critical Path
📄 **Read:** [references/critical-path.md](references/critical-path.md)
- Enabling critical path (`enableCriticalPath`, inject `CriticalPath`)
- Toolbar toggle button (`'CriticalPath'`)
- Customizing critical taskbar colors via `queryTaskbarInfo`
- `data.isCritical` and `data.slack` properties
- Near-critical task detection using slack time

### Timezone and Globalization
📄 **Read:** [references/timezone-and-globalization.md](references/timezone-and-globalization.md)
- `timezone` — IANA string (e.g. `'UTC'`, `'America/New_York'`) applied at render time
- `timezone: 'UTC'` — display same times for all users regardless of local clock
- Hourly timeline: combine `timezone` + `durationUnit: 'Hour'` + `dateFormat: 'hh:mm a'` + bottom tier `unit: 'Hour'`
- CRUD with timezone: edits operate in configured timezone; `actionComplete` receives local-time-reversed date for DB persistence
- `args.data.ganttProperties.endDate` in `actionComplete` — post-edit value already converted back to local time
- `Timezone` class (`@syncfusion/ej2-base`) — manual timezone arithmetic
- `timezone.offset(date, tz)` → offset in minutes from UTC
- `timezone.convert(date, fromOffset, toOffset)` → date in target timezone (IANA or numeric)
- `timezone.remove(date, tz)` → strips offset, returns wall-clock time as plain date
- Locale and globalization (`locale`, `L10n.load()`)
- RTL support (`enableRtl: true` + locale strings)
- Date format configuration on columns (`format: 'dd/MM/yyyy'` or `'yMd'`)
- `currencyCode` — set currency for monetary columns

---

## Quick Start (Vue 3 — Composition API)

```bash
npm install @syncfusion/ej2-vue-gantt --save
```

```vue
<template>
  <ejs-gantt
    id="gantt"
    :dataSource="data"
    :taskFields="taskFields"
    height="450px"
  ></ejs-gantt>
</template>

<script setup>
import { GanttComponent as EjsGantt } from '@syncfusion/ej2-vue-gantt';

const data = [
  { TaskID: 1, TaskName: 'Planning', StartDate: new Date('04/02/2019'), EndDate: new Date('04/06/2019'), ParentID: null },
  { TaskID: 2, TaskName: 'Identify location', StartDate: new Date('04/02/2019'), Duration: 4, Progress: 50, ParentID: 1 },
  { TaskID: 3, TaskName: 'Perform soil test', StartDate: new Date('04/02/2019'), Duration: 4, Progress: 50, ParentID: 1 },
];

const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  duration: 'Duration',
  progress: 'Progress',
  parentID: 'ParentID'
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-tailwind3-theme/styles/gantt/index.css";
</style>
```

## Quick Start (Vue 3 — Options API)

```vue
<script>
import { GanttComponent, Edit, Filter, Sort, Toolbar, Selection, DayMarkers } from '@syncfusion/ej2-vue-gantt';

export default {
  name: 'App',
  components: { 'ejs-gantt': GanttComponent },
  data() {
    return {
      data: [...],
      taskFields: { id: 'TaskID', name: 'TaskName', startDate: 'StartDate', duration: 'Duration', progress: 'Progress', parentID: 'ParentID' },
      toolbar: ['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'ExpandAll', 'CollapseAll'],
      editSettings: { allowAdding: true, allowEditing: true, allowDeleting: true, allowTaskbarEditing: true }
    };
  },
  provide: {
    gantt: [Edit, Filter, Sort, Toolbar, Selection, DayMarkers]
  }
};
</script>
```

## Common Patterns

### Pattern 1 — Inject Only What You Use

Features in the Gantt Chart require explicit module injection. Only inject modules for features you enable to keep bundle size lean:

```js
// Composition API (Vue 3)
import { provide } from 'vue';
import { Edit, Filter, Sort, Toolbar } from '@syncfusion/ej2-vue-gantt';
provide('gantt', [Edit, Filter, Sort, Toolbar]);

// Options API
provide: { gantt: [Edit, Filter, Sort, Toolbar] }
```

### Pattern 2 — Self-Referential vs Hierarchical Data

```js
// Self-referential (flat array with ParentID — recommended for CRUD)
taskFields: { id: 'TaskID', name: 'TaskName', startDate: 'StartDate', duration: 'Duration', parentID: 'ParentID' }

// Hierarchical (nested subtasks array)
taskFields: { id: 'TaskID', name: 'TaskName', startDate: 'StartDate', duration: 'Duration', child: 'subtasks' }
```

### Pattern 3 — Full-Featured Gantt

```vue
<ejs-gantt
  :dataSource="data"
  :taskFields="taskFields"
  :editSettings="editSettings"
  :toolbar="toolbar"
  :allowFiltering="true"
  :allowSorting="true"
  :splitterSettings="{ columnIndex: 2 }"
  :timelineSettings="{ topTier: { unit: 'Week' }, bottomTier: { unit: 'Day' } }"
  height="500px"
></ejs-gantt>
```

## Key Props Reference

| Prop | Type | Purpose |
|---|---|---|
| `dataSource` | Array / DataManager | Task data |
| `taskFields` | Object | Maps data fields to Gantt fields |
| `height` | String | Component height (e.g., `'450px'`) |
| `toolbar` | Array | Toolbar item names or custom item objects |
| `editSettings` | Object | Controls which edit operations are allowed |
| `allowFiltering` | Boolean | Enables column filter menu |
| `allowSorting` | Boolean | Enables column header sorting |
| `timelineSettings` | Object | Top/bottom tier units and format |
| `splitterSettings` | Object | Grid/chart panel width split |
| `labelSettings` | Object | Left, right, and task label fields |
| `resources` | Array | Resource collection |
| `resourceFields` | Object | Maps resource id/name fields |
| `eventMarkers` | Array | Vertical marker lines with labels |
| `holidays` | Array | Non-working day definitions |
| `projectStartDate` | Date | Explicit project start |
| `projectEndDate` | Date | Explicit project end |
| `enableVirtualization` | Boolean | Virtual row rendering for large data |
| `enableCriticalPath` | Boolean | Highlights critical path tasks |
| `baselineTemplate` | function/string | Custom baseline rendering for planned schedules and advanced baseline layouts |
| `enableInfiniteTimelineScroll` | boolean | Enable infinite horizontal timeline scrolling by extending the visible range as the user navigates |

