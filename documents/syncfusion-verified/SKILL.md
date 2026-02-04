---
name: syncfusion-verified
description: Use when implementing, editing, or discussing any SyncFusion EJ2 React component (Grid, Gantt, Schedule, Kanban, Dialog, etc). Contains only officially verified best practices from SyncFusion documentation. For styling/layout/icons, also use syncfusion-styling skill. Theme-agnostic rules that work with Fluent2, Material, Bootstrap, etc.
allowed-tools: Read, Grep, Glob, WebFetch
---

# SyncFusion EJ2 React - Verified Best Practices

This skill contains **only officially verified** rules from SyncFusion documentation.

## 🎯 CORE PRINCIPLES (Verified)

### 1. MODULE INJECTION - MANDATORY ✅

**Source:** SyncFusion Grid/Gantt/Schedule official documentation

Features like paging, sorting, filtering, editing require explicit module injection:

```typescript
import { GridComponent, Inject, Page, Sort, Filter } from '@syncfusion/ej2-react-grids';

// ✅ CORRECT - Modules injected
<GridComponent allowPaging={true} allowSorting={true}>
  <Inject services={[Page, Sort, Filter]} />
</GridComponent>

// ❌ WRONG - Features won't work without Inject
<GridComponent allowPaging={true} allowSorting={true} />
```

**Common service modules by component:**

**Grid:**
```typescript
import { Page, Sort, Filter, Group, Edit, Toolbar } from '@syncfusion/ej2-react-grids';
<Inject services={[Page, Sort, Filter, Group, Edit, Toolbar]} />
```

**Gantt:**
```typescript
import { Edit, Filter, Sort, Selection } from '@syncfusion/ej2-react-gantt';
<Inject services={[Edit, Filter, Sort, Selection]} />
```

**Schedule:**
```typescript
import { Day, Week, WorkWeek, Month, Agenda } from '@syncfusion/ej2-react-schedule';
<Inject services={[Day, Week, WorkWeek, Month, Agenda]} />
```

**TreeGrid:**
```typescript
import { Page, Sort, Filter, Edit, Toolbar } from '@syncfusion/ej2-react-treegrid';
<Inject services={[Page, Sort, Filter, Edit, Toolbar]} />
```

**Kanban:** No Inject required

---

### 2. DIRECT IMPORTS ✅

**Source:** All SyncFusion official examples

Import components directly from SyncFusion packages:

```typescript
// ✅ CORRECT - Direct import
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';
import { ScheduleComponent } from '@syncfusion/ej2-react-schedule';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// ❌ AVOID - Custom wrappers (unless absolutely necessary)
import { MyCustomGrid } from './components/MyCustomGrid';
```

---

### 3. THEME CSS IMPORTS ✅

**Source:** SyncFusion Theme Documentation

**Recommended approach:** Use optimized lite CSS files

```typescript
// main.tsx or App.tsx
// Fluent2 theme
import '@syncfusion/ej2/fluent2-lite.css';

// OR individual component imports (larger bundle)
import '@syncfusion/ej2-base/styles/fluent2.css';
import '@syncfusion/ej2-buttons/styles/fluent2.css';
import '@syncfusion/ej2-react-grids/styles/fluent2.css';
// ... etc
```

**For other themes:** Replace `fluent2` with `material`, `bootstrap`, `fabric`, etc.

**Theme customization:** Use [Theme Studio](https://ej2.syncfusion.com/themestudio/) for custom themes

---

### 4. GRID EDITING MODES ✅

**Source:** SyncFusion Grid Editing Documentation

Three official edit modes:

```typescript
const editSettings = {
  allowEditing: true,
  allowAdding: true,
  allowDeleting: true,
  mode: 'Normal' // or 'Dialog', 'Batch'
};

<GridComponent editSettings={editSettings}>
  <Inject services={[Edit, Toolbar]} />
</GridComponent>
```

**Mode descriptions:**
- **Normal:** Inline editing, one row at a time
- **Dialog:** Opens edit form in dialog popup
- **Batch:** Edit multiple cells/rows, then click Update to save all

**Editable columns require:**
- `isPrimaryKey={true}` on ID column
- `editType` prop: `'numericedit'`, `'dropdownedit'`, `'datepickeredit'`, etc.

```typescript
<ColumnDirective
  field="price"
  editType="numericedit"
  edit={{ params: { format: 'N2', min: 0 } }}
/>
```

---

### 5. DIALOG VISIBILITY CONTROL ✅

**Source:** SyncFusion Dialog Documentation

Control dialog visibility with `visible` prop:

```typescript
const [isVisible, setIsVisible] = useState(false);

<DialogComponent
  visible={isVisible}
  isModal={true}
  close={() => setIsVisible(false)}
  header="Dialog Title"
>
  <div>Dialog content</div>
</DialogComponent>
```

**Key props:**
- `visible`: Boolean to show/hide
- `isModal`: Boolean for modal overlay
- `close`: Event handler when dialog closes
- `target`: Optional container element

---

### 6. BUTTONCOMPONENT ONCLICK IN DIALOG - KNOWN ISSUE ✅

**Source:** SyncFusion Support Forum (React 17 event delegation bug)

**Problem:** ButtonComponent onClick doesn't work inside DialogComponent in React 17+

**Official Solutions:**

**Option 1 - Use `content` property (Recommended by SF):**
```typescript
const dialogContent = () => (
  <div>
    <ButtonComponent onClick={handleClick}>Save</ButtonComponent>
  </div>
);

<DialogComponent content={dialogContent} />
```

**Option 2 - Use `buttons` prop:**
```typescript
const dialogButtons = [
  {
    click: handleSave,
    buttonModel: { content: 'Save', isPrimary: true }
  }
];

<DialogComponent buttons={dialogButtons} />
```

**Option 3 - Use native HTML buttons with SF classes:**
```typescript
<DialogComponent>
  <button className="e-btn e-primary" onClick={handleSave}>
    Save
  </button>
</DialogComponent>
```

**Option 4 - Set proper `target`:**
```typescript
<DialogComponent target="#app-container">
  <ButtonComponent onClick={handleClick}>Save</ButtonComponent>
</DialogComponent>
```

---

### 7. DATA BINDING ✅

**Source:** SyncFusion Data Binding Documentation

Two approaches: Local data or DataManager

**Local array:**
```typescript
const data = [
  { id: 1, name: 'Task 1', status: 'Open' },
  { id: 2, name: 'Task 2', status: 'InProgress' }
];

<GridComponent dataSource={data} />
```

**Remote data with DataManager:**
```typescript
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'https://api.example.com/tasks',
  adaptor: new UrlAdaptor(),
  crossDomain: true
});

<GridComponent dataSource={dataManager} />
```

---

### 8. GANTT TASK FIELDS MAPPING ✅

**Source:** SyncFusion Gantt Documentation

Always map required task fields:

```typescript
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  progress: 'Progress',
  dependency: 'Predecessor',  // For dependencies
  child: 'subtasks'            // For hierarchical data
};

<GanttComponent taskFields={taskFields} />
```

**Predecessor format for dependencies:**
```typescript
// String format (not number!)
{ TaskID: 3, Predecessor: '2' }      // Finish-to-Start
{ TaskID: 4, Predecessor: '2FS+2' }  // FS with 2-day lag
{ TaskID: 5, Predecessor: '3SS-1' }  // Start-to-Start with -1 day lag
```

**Dependency types:**
- `FS`: Finish-to-Start (default)
- `SF`: Start-to-Finish
- `SS`: Start-to-Start
- `FF`: Finish-to-Finish

---

### 9. SCHEDULE EVENT DATA FORMAT ✅

**Source:** SyncFusion Schedule Documentation

Events must use **Date objects** (not strings):

```typescript
// ✅ CORRECT - Date objects
const events = [
  {
    Id: 1,
    Subject: 'Meeting',
    StartTime: new Date(2025, 9, 25, 10, 0), // Month is 0-indexed!
    EndTime: new Date(2025, 9, 25, 12, 0),
    IsAllDay: false
  }
];

// ❌ WRONG - String dates won't display
const events = [
  {
    Id: 1,
    Subject: 'Meeting',
    StartTime: '2025-10-25',
    EndTime: '2025-10-26'
  }
];
```

**Month indexing:** January = 0, December = 11

---

### 10. PERFORMANCE OPTIMIZATION ✅

**Source:** SyncFusion Performance Documentation

**Virtual Scrolling** for large datasets (>1000 rows):

```typescript
// Grid
<GridComponent
  dataSource={largeData}
  enableVirtualization={true}
  height="600px"  // Fixed height required for virtualization
/>

// Gantt
<GanttComponent
  enableVirtualization={true}
  enableTimelineVirtualization={true}
/>

// Kanban
<KanbanComponent
  enableVirtualization={true}
  height="600px"
/>
```

**Pagination** for better UX:

```typescript
<GridComponent
  allowPaging={true}
  pageSettings={{
    pageSize: 20,
    pageCount: 5,
    pageSizes: [10, 20, 50, 100]
  }}
>
  <Inject services={[Page]} />
</GridComponent>
```

---

## 📚 COMPONENT QUICK REFERENCE

### GridComponent
```typescript
import {
  GridComponent,
  ColumnsDirective,
  ColumnDirective,
  Inject,
  Page,
  Sort,
  Filter,
  Group,
  Edit,
  Toolbar
} from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  allowPaging={true}
  allowSorting={true}
  allowFiltering={true}
  editSettings={{ allowEditing: true, mode: 'Normal' }}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  <ColumnsDirective>
    <ColumnDirective field="id" isPrimaryKey={true} />
    <ColumnDirective field="name" headerText="Name" />
    <ColumnDirective field="price" editType="numericedit" />
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter, Group, Edit, Toolbar]} />
</GridComponent>
```

### GanttComponent
```typescript
import {
  GanttComponent,
  Inject,
  Edit,
  Selection,
  Toolbar
} from '@syncfusion/ej2-react-gantt';

<GanttComponent
  dataSource={tasks}
  taskFields={{
    id: 'TaskID',
    name: 'TaskName',
    startDate: 'StartDate',
    duration: 'Duration',
    dependency: 'Predecessor'
  }}
  editSettings={{ allowEditing: true }}
  toolbar={['Add', 'Edit', 'Delete']}
>
  <Inject services={[Edit, Selection, Toolbar]} />
</GanttComponent>
```

### ScheduleComponent
```typescript
import {
  ScheduleComponent,
  ViewsDirective,
  ViewDirective,
  Inject,
  Day,
  Week,
  Month
} from '@syncfusion/ej2-react-schedule';

<ScheduleComponent
  currentView="Week"
  eventSettings={{ dataSource: events }}
>
  <ViewsDirective>
    <ViewDirective option="Day" />
    <ViewDirective option="Week" />
    <ViewDirective option="Month" />
  </ViewsDirective>
  <Inject services={[Day, Week, Month]} />
</ScheduleComponent>
```

### DialogComponent
```typescript
import { DialogComponent } from '@syncfusion/ej2-react-popups';

const dialogButtons = [
  { click: handleSave, buttonModel: { content: 'Save', isPrimary: true } },
  { click: handleClose, buttonModel: { content: 'Cancel' } }
];

<DialogComponent
  visible={isOpen}
  isModal={true}
  header="Dialog Title"
  buttons={dialogButtons}
  close={handleClose}
>
  <div>Dialog content</div>
</DialogComponent>
```

### KanbanComponent
```typescript
import {
  KanbanComponent,
  ColumnsDirective,
  ColumnDirective
} from '@syncfusion/ej2-react-kanban';

<KanbanComponent
  dataSource={cards}
  keyField="Status"
  cardSettings={{
    contentField: 'Summary',
    headerField: 'Title'
  }}
>
  <ColumnsDirective>
    <ColumnDirective headerText="To Do" keyField="Open" />
    <ColumnDirective headerText="In Progress" keyField="InProgress" />
    <ColumnDirective headerText="Done" keyField="Close" />
  </ColumnsDirective>
</KanbanComponent>
```

---

## 🔗 VERIFICATION SOURCES

All rules in this skill are verified against:

- **Official Documentation:** https://ej2.syncfusion.com/react/documentation/
- **Theme Studio:** https://ej2.syncfusion.com/themestudio/
- **Support Forum:** https://www.syncfusion.com/forums/ (for known bugs)
- **API Reference:** https://ej2.syncfusion.com/react/documentation/api/

**When in doubt:** Always consult official SyncFusion documentation using WebFetch tool.

---

## ⚠️ THEME INDEPENDENCE

All rules in this skill are **theme-agnostic**:
- ✅ Works with Fluent2, Material, Bootstrap, Fabric, Tailwind CSS, etc.
- ✅ Only CSS import path changes between themes
- ✅ Component API remains identical

**Current project theme:** Fluent2 (see CLAUDE.md for project-specific preferences)

---

**Skill Version:** 1.1 (Verified)
**Created:** 2025-10-25
**Updated:** 2025-10-25 (added styling skill reference)
**Verification:** All rules verified against SyncFusion official documentation
**Theme:** Theme-agnostic (tested with Fluent2)
**Related Skills:** syncfusion-styling (for layout/colors/icons)
