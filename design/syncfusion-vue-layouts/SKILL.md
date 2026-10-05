---
name: syncfusion-vue-layouts
description: Comprehensive guide for implementing Syncfusion Vue 3 Layout components including Card, DashboardLayout, ListView, Splitter, and Timeline. Use when building card-based content containers, customizable draggable dashboards, interactive data lists, resizable multi-pane layouts, and chronological event timelines. Covers installation, data binding, templating, customization, drag-and-drop, resizing, panel management, virtualization, accessibility, and styling in Vue 3 applications.
metadata:
  author: "Syncfusion Inc"
  category: "Layouts"
  version: "34.1.29"
---

# Implementing Syncfusion Vue 3 Layouts

The Syncfusion Vue 3 Layout components provide a suite of UI building blocks for organizing content, data, and interactive panels in Vue 3 applications. This unified package covers five complementary components: **Card** for content containers, **DashboardLayout** for customizable panel grids, **ListView** for interactive lists, **Splitter** for resizable panes, and **Timeline** for chronological event displays. All examples use the Vue 3 Composition API with `<script setup>` SFCs.

## Package Installation

Most layout components ship from the `@syncfusion/ej2-vue-layouts` package. The Card component uses `@syncfusion/ej2-vue-layouts` (CSS only). The ListView component uses `@syncfusion/ej2-vue-lists`.

```bash
# Card, Dashboard Layout, Splitter, Timeline
npm install @syncfusion/ej2-vue-layouts

# ListView
npm install @syncfusion/ej2-vue-lists @syncfusion/ej2-data
```

### CSS Imports

```css
/* Card, DashboardLayout, Splitter, Timeline */
@import '@syncfusion/ej2-base/styles/tailwind3.css';
@import '@syncfusion/ej2-vue-layouts/styles/tailwind3.css';

/* ListView */
@import '@syncfusion/ej2-base/styles/tailwind3.css';
@import '@syncfusion/ej2-vue-lists/styles/tailwind3.css';
```

---

## Table of Contents

1. [Card](#card)
2. [DashboardLayout](#dashboardlayout)
3. [ListView](#listview)
4. [Splitter](#splitter)
5. [Timeline](#timeline)
6. [Shared Conventions](#shared-conventions)
7. [Common Pitfalls](#common-pitfalls)
8. [Component Selection Guide](#component-selection-guide)

---

## Card

The Syncfusion Vue 3 **Card** is a lightweight, CSS-based container for displaying organized content. It supports headers, images, dividers, action buttons, and horizontal layouts. No JavaScript instance is required—build cards with `e-card-*` CSS classes. Card is a presentational component, so you build it directly with Vue template syntax.

### Quick Start

```vue
<template>
  <div class="e-card">
    <div class="e-card-header">
      <div class="e-card-header-caption">
        <div class="e-card-header-title">Card Title</div>
        <div class="e-card-sub-title">Subtitle</div>
      </div>
    </div>
    <div class="e-card-content">
      Card body content goes here.
    </div>
    <div class="e-card-actions">
      <button class="e-card-btn">View</button>
      <button class="e-card-btn">Share</button>
    </div>
  </div>
</template>

<script setup>
import '@syncfusion/ej2-vue-layouts/styles/tailwind3.css';
</script>
```

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/cards-getting-started.md](references/cards-getting-started.md)
- Package installation and CSS imports
- Minimal card structure
- CSS classes overview (e-card, e-card-header, e-card-content, e-card-actions)
- Theme support (tailwind3, bootstrap5, material3, fluent2)

#### Card Structure & Headers
📄 **Read:** [references/cards-card-structure-headers.md](references/cards-card-structure-headers.md)
- Header container and caption pattern
- Title and subtitle classes
- Header images with rounded corners
- Multiple content sections with separators

#### Images, Titles & Dividers
📄 **Read:** [references/cards-images-titles-dividers.md](references/cards-images-titles-dividers.md)
- Full-width card images (e-card-image)
- Image title overlay positioning (e-card-bottom-left, e-card-top-right, etc.)
- Divider usage (e-card-separator)
- Image styling with backgroundImage and backgroundSize

#### Action Buttons
📄 **Read:** [references/cards-action-buttons.md](references/cards-action-buttons.md)
- Action container (e-card-actions) and buttons (e-card-btn)
- Horizontal (default) and vertical (e-card-vertical) layouts
- Icon buttons and image icons
- Disabled and styled buttons
- Interactive e-commerce, team, and settings examples

#### Layouts & Customization
📄 **Read:** [references/cards-layouts-customization.md](references/cards-layouts-customization.md)
- Horizontal layout (e-card-horizontal)
- Stacked sections (e-card-stacked)
- Image title position classes reference
- Advanced custom styling with reactive state
- Card grid layout patterns
- Responsive card patterns (mobile-first, CSS media queries)

#### Embedding Components
📄 **Read:** [references/cards-embedding-components.md](references/cards-embedding-components.md)
- ListView in cards (todo lists, project tasks)
- Grid in cards (sales data)
- Chart in cards (trend visualization)
- Button, DropDown, and form components in cards
- Dynamic content with reactive state

### Common Patterns

#### Horizontal Product Card

```vue
<template>
  <div class="e-card e-card-horizontal" style="width: 400px;">
    <img src="./product.jpg" alt="Product" style="width: 150px; height: 150px; object-fit: cover;" />
    <div class="e-card-stacked">
      <div class="e-card-header-title">Philips Trimmer</div>
      <div class="e-card-content">Premium quality product.</div>
      <div class="e-card-actions">
        <button class="e-card-btn" style="flex: 1;">View</button>
        <button class="e-card-btn" style="flex: 1;">Buy Now</button>
      </div>
    </div>
  </div>
</template>
```

#### Card with Image Title Overlay

```vue
<template>
  <div class="e-card">
    <div class="e-card-image" :style="{ backgroundImage: 'url(./city.jpg)', height: '250px' }">
      <div class="e-card-title e-card-bottom-left">Beautiful City</div>
    </div>
    <div class="e-card-content">Description text.</div>
  </div>
</template>
```

### Key CSS Classes

| Class | Purpose |
|-------|---------|
| `e-card` | Root card container (required) |
| `e-card-horizontal` | Horizontal layout |
| `e-card-stacked` | Vertical stack within horizontal |
| `e-card-header` / `-title` / `-sub-title` | Header structure |
| `e-card-image` / `e-card-title` | Image with overlay |
| `e-card-separator` | Divider line |
| `e-card-content` | Main content area |
| `e-card-actions` / `e-card-btn` / `e-card-vertical` | Action buttons |

---

## DashboardLayout

The Syncfusion Vue 3 **DashboardLayoutComponent** is a grid-based dashboard builder with draggable, resizable, and floating panels. It supports state persistence, responsive breakpoints, dynamic panel management, and event tracking for monitoring layout changes.

### Quick Start

```vue
<template>
  <DashboardLayoutComponent
    ref="dashboardRef"
    id="dashboard"
    :columns="5"
    :cellSpacing="[10, 10]"
    :panels="panels"
    :allowDragging="true"
    :allowResizing="true"
    :allowFloating="true"
  />
</template>

<script setup>
import { ref } from 'vue';
import { DashboardLayoutComponent } from '@syncfusion/ej2-vue-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-vue-layouts/styles/tailwind3.css';

const dashboardRef = ref(null);

const panels = [
  { id: 'sales', row: 0, col: 0, sizeX: 2, sizeY: 2, header: 'Sales', content: 'Sales data' },
  { id: 'users', row: 0, col: 2, sizeX: 2, sizeY: 2, header: 'Users', content: 'User data' },
  { id: 'reports', row: 2, col: 0, sizeX: 4, sizeY: 1, header: 'Reports', content: 'Reports' }
];
</script>
```

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/dashboard-getting-started.md](references/dashboard-getting-started.md)
- Package installation and CSS theme imports
- Minimal DashboardLayoutComponent
- Static vs. dynamic panels
- First functional dashboard
- Common setup issues (styles, refs, TypeScript, mobile)

#### Core Functionality
📄 **Read:** [references/dashboard-core-functionality.md](references/dashboard-core-functionality.md)
- PanelModel interface (id, row, col, sizeX, sizeY, header, content)
- Disabling panels (enabled: false)
- Size constraints (minSizeX/Y, maxSizeX/Y)
- Floating behavior (allowFloating)
- Grid configuration and state persistence

#### Properties Reference
📄 **Read:** [references/dashboard-properties-reference.md](references/dashboard-properties-reference.md)
- Layout properties (columns, cellSpacing, cellAspectRatio, panels)
- Interaction properties (allowDragging, allowResizing, draggableHandle, resizableHandles)
- Customization (showGridLines, enableRtl, enableHtmlSanitizer)
- Advanced (mediaQuery, enablePersistence)

#### Panel Templates
📄 **Read:** [references/dashboard-panel-templates.md](references/dashboard-panel-templates.md)
- Header templates (string, HTML, interactive)
- Content templates (HTML string, Vue template, dynamic)
- Embedding Charts and DataGrids in panels
- Dynamic content updates with updatePanel method
- Template best practices and computed memoization

#### Styling & Customization
📄 **Read:** [references/dashboard-styling-customization.md](references/dashboard-styling-customization.md)
- CSS selectors (.e-panel, .e-panel-header, .e-panel-content, .e-resize-handle)
- Resize handle directions (e-south-east, e-east, e-west, e-north, etc.)
- Theme integration (Tailwind, Bootstrap, Material, Fluent)
- Header and content area styling
- Dragging state and placeholder styling
- Custom CSS classes per panel

#### Dragging Behavior
📄 **Read:** [references/dashboard-dragging-behavior.md](references/dashboard-dragging-behavior.md)
- Drag events (dragStart, drag, dragStop)
- Collision detection and panel pushing
- Custom drag handles (header-only, icon-only, multiple)
- Disabling specific panels via dragStart
- Visual feedback (.e-panel.e-dragging, .e-placeholder)
- Programmatic panel movement (movePanel)

#### Resizing & Floating
📄 **Read:** [references/dashboard-resizing-floating.md](references/dashboard-resizing-floating.md)
- Resize handle directions and configurations
- Size constraints (minSizeX/Y, maxSizeX/Y)
- Resize events (resizeStart, resize, resizeStop)
- Floating behavior and gap filling
- Programmatic resizing (resizePanel)
- Lock panel size with constraint matching

#### Cell Configuration
📄 **Read:** [references/dashboard-cell-configuration.md](references/dashboard-cell-configuration.md)
- Grid columns and cell distribution
- Cell sizing (sizeX, sizeY)
- Cell aspect ratio (1, 0.5, 2, 1.5)
- Cell spacing ([horizontal, vertical])
- Cell calculation examples
- Responsive cell configuration
- Advanced grid patterns

#### Responsive Design
📄 **Read:** [references/dashboard-responsive-design.md](references/dashboard-responsive-design.md)
- Built-in responsive behavior (default 600px)
- mediaQuery property and custom breakpoints
- Standard breakpoint system (xs, sm, md, lg, xl, xxl)
- Adaptive layouts and panel sizing
- Mobile-first approach
- Touch device support and optimization

#### State Persistence
📄 **Read:** [references/dashboard-state-persistence.md](references/dashboard-state-persistence.md)
- serialize() method for layout export
- localStorage integration patterns
- sessionStorage for temporary persistence
- Database/API integration
- Auto-save with debouncing
- Versioning and migration

#### Methods Reference
📄 **Read:** [references/dashboard-methods-reference.md](references/dashboard-methods-reference.md)
- addPanel(panel), removePanel(id), removeAll()
- updatePanel(panel), movePanel(id, row, col), resizePanel(id, sizeX, sizeY)
- serialize() returns PanelModel[]
- refreshDraggableHandle(), destroy()
- Complete method patterns and use cases

#### Events Reference
📄 **Read:** [references/dashboard-events-reference.md](references/dashboard-events-reference.md)
- Lifecycle events (created, destroyed)
- Drag events (dragStart, drag, dragStop)
- Resize events (resizeStart, resize, resizeStop)
- change event with addedPanels, removedPanels, changedPanels
- Event argument types (DragStartArgs, ResizeArgs, ChangeEventArgs)

#### Accessibility (WCAG)
📄 **Read:** [references/dashboard-accessibility-wcag.md](references/dashboard-accessibility-wcag.md)
- WCAG 2.2 Level AA compliance
- Section 508 standards
- WAI-ARIA roles, properties, and states
- Keyboard navigation and focus management
- Screen reader support and announcements
- RTL language support

#### Advanced Features
📄 **Read:** [references/dashboard-advanced-features.md](references/dashboard-advanced-features.md)
- Dynamic panel creation and removal
- Custom CSS classes per panel
- Header and content templates
- Performance optimization (computed memoization, debouncing)
- Vuex/Pinia integration
- API integration for save/load

### PanelModel Interface

```typescript
interface PanelModel {
  id: string;              // Unique identifier (required)
  row: number;             // Row position (required)
  col: number;             // Column position (required)
  sizeX: number;           // Width in cells (default: 1)
  sizeY: number;           // Height in cells (default: 1)
  header?: string | HTMLElement | Function;
  content?: string | HTMLElement | Function;
  cssClass?: string;
  enabled?: boolean;
  minSizeX?: number;
  minSizeY?: number;
  maxSizeX?: number;
  maxSizeY?: number;
  zIndex?: number;
}
```

### Common Patterns

#### Save/Restore Layout

```vue
<script setup>
import { ref } from 'vue';
import { DashboardLayoutComponent } from '@syncfusion/ej2-vue-layouts';

const dashboardRef = ref(null);

const saveLayout = () => {
  const layout = dashboardRef.value?.serialize();
  localStorage.setItem('userDashboard', JSON.stringify(layout));
};

const restoreLayout = () => {
  const saved = localStorage.getItem('userDashboard');
  if (saved) {
    const layout = JSON.parse(saved);
    dashboardRef.value?.removeAll();
    layout.forEach(panel => dashboardRef.value?.addPanel(panel));
  }
};
</script>
```

#### Dynamic Panel Management

```vue
<script setup>
import { ref } from 'vue';
import { DashboardLayoutComponent } from '@syncfusion/ej2-vue-layouts';

const dashboardRef = ref(null);

const addPanel = () => {
  dashboardRef.value?.addPanel({
    id: `panel-${Date.now()}`,
    header: 'New Panel',
    content: 'Content',
    row: 0, col: 0, sizeX: 2, sizeY: 1
  });
};

const removePanel = (panelId) => {
  dashboardRef.value?.removePanel(panelId);
};
</script>
```

#### Monitor Layout Changes

```vue
<template>
  <DashboardLayoutComponent
    :panels="panels"
    @change="handleChange"
  />
</template>

<script setup>
const handleChange = (args) => {
  console.log('Added:', args.addedPanels);
  console.log('Removed:', args.removedPanels);
  console.log('Changed:', args.changedPanels);
  console.log('User interaction:', args.isInteracted);
};
</script>
```

---

## ListView

The Syncfusion Vue 3 **ListViewComponent** displays collections of items with rich templating, single/multiple selection, filtering, grouping, drag-drop, and virtualization. Supports local arrays, DataManager remote sources, checkboxes, animations, RTL, and WCAG 2.1 AA accessibility.

### Quick Start

```vue
<template>
  <ListViewComponent
    id="list"
    :dataSource="data"
    :fields="fields"
  />
</template>

<script setup>
import { ListViewComponent } from '@syncfusion/ej2-vue-lists';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-vue-lists/styles/tailwind3.css';

const data = [
  { id: '1', text: 'Item 1' },
  { id: '2', text: 'Item 2' },
  { id: '3', text: 'Item 3' }
];

const fields = { text: 'text', id: 'id' };
</script>
```

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/listview-getting-started.md](references/listview-getting-started.md)
- Installation (@syncfusion/ej2-vue-lists, @syncfusion/ej2-data)
- CSS imports and theme setup
- Basic ListViewComponent usage
- Local array and object data sources
- Minimal working example

#### Data Binding & Rendering
📄 **Read:** [references/listview-data-binding-rendering.md](references/listview-data-binding-rendering.md)
- Local arrays, object mapping with fields
- Remote data with DataManager
- Query filtering on remote data
- Load on demand and pagination
- Dynamic data updates

#### Item Management (CRUD)
📄 **Read:** [references/listview-item-management.md](references/listview-item-management.md)
- addItem(data, fields?), removeItem(item), removeMultipleItems
- Update items by replacing dataSource
- Batch operations and finding items
- Managing nested list items

#### Selection & Filtering
📄 **Read:** [references/listview-selection-filtering.md](references/listview-selection-filtering.md)
- Single and multiple selection
- Checkbox-based selection (showCheckBox, checkBoxPosition)
- Programmatic selection (selectItem, selectMultipleItems)
- Filtering list items and search functionality
- Selection events and callbacks

#### Templating & Customization
📄 **Read:** [references/listview-templating-customization.md](references/listview-templating-customization.md)
- Custom item templates (Vue slot, function, string)
- Header templates (headerTemplate)
- Group header templates (groupTemplate)
- Template data context
- Dynamic templates based on device
- CSS customization with classes
- RTL template support

#### Advanced Features
📄 **Read:** [references/listview-advanced-features.md](references/listview-advanced-features.md)
- Grouping and sorting (groupBy, sortOrder)
- Nested lists with hierarchy (up to 3 levels)
- Checkbox state management
- Animations and effects
- Custom icons and image display
- Enable/disable item states

#### Layout & Alignment Patterns
📄 **Read:** [references/listview-layout-alignment-patterns.md](references/listview-layout-alignment-patterns.md)
- Patient Portal pattern (ListView with Cards, Appointments, Prescriptions)
- Appointments Dashboard (3x2 grid with filters)
- Monitoring Dashboard (3x3 grid with KPIs)
- Fixing common alignment issues (scrolling, borders, spacing)
- Responsive grid layouts

#### Quick Start Alignment
📄 **Read:** [references/listview-quick-start-alignment.md](references/listview-quick-start-alignment.md)
- Fast setup for common alignment patterns
- Common container setups
- Padding and margin guidelines

#### Performance & Virtualization
📄 **Read:** [references/listview-performance-virtualization.md](references/listview-performance-virtualization.md)
- Virtual scrolling for 1000+ items (enableVirtualization)
- refreshItemHeight() for dynamic heights
- Memory optimization tips
- Combining with pagination
- Performance best practices

#### API Reference
📄 **Read:** [references/listview-api-reference.md](references/listview-api-reference.md)
- Complete property documentation
- Method signatures and parameters
- Event handler arguments
- Default values for all properties
- Property type specifications

#### Accessibility & Events
📄 **Read:** [references/listview-accessibility-events.md](references/listview-accessibility-events.md)
- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader support
- ARIA attributes
- Event lifecycle (select, actionBegin, actionComplete, actionFailure, scroll)

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `dataSource` | Array/DataManager | `[]` | Data to display |
| `fields` | FieldSettingsModel | defaultMappedFields | Map data to fields |
| `template` | string/function/Vue | `null` | Custom item template |
| `headerTemplate` | string/function/Vue | `null` | Custom header template |
| `showCheckBox` | boolean | `false` | Show checkboxes |
| `checkBoxPosition` | 'Left'/'Right' | `'Left'` | Checkbox position |
| `sortOrder` | 'None'/'Ascending'/'Descending' | `'None'` | Data sort order |
| `enableVirtualization` | boolean | `false` | Virtual scrolling |
| `height` | number/string | `''` | List height |
| `width` | number/string | `''` | List width |
| `cssClass` | string | `''` | Custom CSS class |
| `enableRtl` | boolean | `false` | Right-to-left support |

### Common Patterns

#### Multiple Selection with Checkboxes

```vue
<template>
  <ListViewComponent
    :dataSource="items"
    :showCheckBox="true"
    :fields="fields"
  />
</template>

<script setup>
import { ListViewComponent } from '@syncfusion/ej2-vue-lists';

const items = [
  { id: '1', text: 'Item 1' },
  { id: '2', text: 'Item 2' }
];
const fields = { id: 'id', text: 'text', isChecked: 'checked' };
</script>
```

#### ListView in Card Container

```vue
<template>
  <div style="border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column;">
    <div style="padding: 16px; background-color: #f5f5f5; border-bottom: 1px solid #e0e0e0;">
      <h3 style="margin: 0;">Messages</h3>
    </div>
    <div style="flex: 1; overflow: auto; min-height: 0;">
      <ListViewComponent :dataSource="items" height="100%" width="100%" />
    </div>
  </div>
</template>
```

#### Add/Remove Items

```vue
<template>
  <ListViewComponent ref="listViewRef" :dataSource="items" />
  <button @click="addItem">Add</button>
</template>

<script setup>
import { ref } from 'vue';
import { ListViewComponent } from '@syncfusion/ej2-vue-lists';

const listViewRef = ref(null);
const items = ref([{ text: 'Item 1', id: 1 }]);

const addItem = () => {
  listViewRef.value?.addItem([{ text: 'New Item', id: Date.now() }]);
};

const removeItem = (item) => {
  listViewRef.value?.removeItem(item);
};
</script>
```

### Alignment Best Practices

- ✅ Always set explicit `height` on parent container when using flex layout
- ✅ Use `overflow: 'auto'` and `min-height: 0` on flex children for scrolling
- ✅ Use `flex-shrink: 0` on headers to prevent shrinking
- ✅ Use `gap` in templates instead of individual margins
- ✅ Set `width: '100%'` and `height: '100%'` on ListView to fill container
- ❌ Don't rely on default margins - they cause misalignment
- ❌ Don't skip flex container setup - ListView needs proper parent context

---

## Splitter

The Syncfusion Vue 3 **SplitterComponent** creates flexible, resizable multi-pane layouts. Each pane is defined with `<e-panes>` and `<e-pane>` child directives. Supports horizontal/vertical orientation, expand/collapse, nested splitters, custom content, and accessibility.

### Quick Start

```vue
<template>
  <SplitterComponent>
    <e-panes>
      <e-pane size="200px">
        <div>Left Panel</div>
      </e-pane>
      <e-pane size="300px">
        <div>Right Panel</div>
      </e-pane>
    </e-panes>
  </SplitterComponent>
</template>

<script setup>
import { SplitterComponent, PaneDirective, PanesDirective } from '@syncfusion/ej2-vue-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-vue-layouts/styles/tailwind3.css';
</script>
```

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/splitter-getting-started.md](references/splitter-getting-started.md)
- Package installation
- CSS imports and theme configuration
- Basic Splitter with `<e-panes>` / `<e-pane>` directives
- First working example

#### Properties and Configuration
📄 **Read:** [references/splitter-properties-and-configuration.md](references/splitter-properties-and-configuration.md)
- SplitterComponent properties (orientation, height, width, separatorSize)
- e-pane properties (size, min, max, collapsed, collapsible, resizable, content, cssClass)
- enablePersistence, enableHtmlSanitizer
- Common configuration patterns

#### Methods Reference
📄 **Read:** [references/splitter-methods-reference.md](references/splitter-methods-reference.md)
- addPane(pane) - Dynamically add new panes
- removePane(index) - Remove panes by index
- collapse(index) / expand(index) - Programmatically collapse/expand
- destroy() - Component cleanup
- Real-world examples

#### Events Reference
📄 **Read:** [references/splitter-events-reference.md](references/splitter-events-reference.md)
- created - Component initialization
- beforeCollapse / collapsed - Collapse events with cancellation
- beforeExpand / expanded - Expand events with data loading
- resizeStart / resizing / resizeStop - Resize lifecycle
- Event handling patterns

#### Pane Layout Configuration
📄 **Read:** [references/splitter-pane-layout-configuration.md](references/splitter-pane-layout-configuration.md)
- Horizontal and vertical layouts
- Multiple panes and nested splitters
- Pane properties and configuration
- Layout patterns for common use cases

#### Pane Sizing & Separation
📄 **Read:** [references/splitter-pane-sizing-and-separation.md](references/splitter-pane-sizing-and-separation.md)
- Fixed and percentage-based sizing (px, %)
- Min and max size constraints
- Separator styling and customization
- Dynamic size adjustments

#### Expand & Collapse
📄 **Read:** [references/splitter-expand-collapse-functionality.md](references/splitter-expand-collapse-functionality.md)
- Collapsed state initialization
- Button integration for expand/collapse
- User-driven vs. programmatic collapse
- Event handling patterns

#### Resize Behavior
📄 **Read:** [references/splitter-resize-behavior.md](references/splitter-resize-behavior.md)
- Resize events and lifecycle
- Preventing resize on specific panes
- Dynamic resize configuration
- Resize constraints and validation
- Event data and handling

#### Pane Content & Styling
📄 **Read:** [references/splitter-pane-content-and-styling.md](references/splitter-pane-content-and-styling.md)
- HTML content in panes
- Vue component content in panes
- CSS selector-based content
- Pane template usage
- Custom styling and classes

#### Accessibility & Globalization
📄 **Read:** [references/splitter-accessibility-and-globalization.md](references/splitter-accessibility-and-globalization.md)
- WCAG 2.1 compliance and keyboard navigation
- ARIA attributes (aria-label, aria-orientation, role="separator")
- RTL (Right-to-Left) support
- Internationalization (en, es, fr)
- Focus management

#### Style Customization
📄 **Read:** [references/splitter-style-customization.md](references/splitter-style-customization.md)
- CSS customization (.e-splitter-bar, .e-pane)
- Theme variables (--primary-color, --bg-primary)
- Gripper and separator styling
- Responsive design patterns
- Dark mode and theme switching

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `orientation` | 'Horizontal' / 'Vertical' | Layout direction |
| `size` (Pane) | string (px, %) | Pane width/height |
| `min` / `max` (Pane) | string | Min/max pane size |
| `collapsed` (Pane) | boolean | Initial collapsed state |
| `collapsible` (Pane) | boolean | Allow user to collapse |
| `resizable` (Pane) | boolean | Allow user to resize |

### Common Patterns

#### Two-Column Layout

```vue
<template>
  <SplitterComponent orientation="Horizontal">
    <e-panes>
      <e-pane size="25%"><div>Left</div></e-pane>
      <e-pane size="75%"><div>Main Content</div></e-pane>
    </e-panes>
  </SplitterComponent>
</template>
```

#### Vertical Split with Collapse

```vue
<template>
  <SplitterComponent orientation="Vertical">
    <e-panes>
      <e-pane size="50%" :collapsed="true"><div>Top</div></e-pane>
      <e-pane size="50%"><div>Bottom</div></e-pane>
    </e-panes>
  </SplitterComponent>
</template>
```

#### Three-Panel Dashboard

```vue
<template>
  <SplitterComponent orientation="Horizontal">
    <e-panes>
      <e-pane size="20%"><div>Sidebar</div></e-pane>
      <e-pane size="60%"><div>Main Content</div></e-pane>
      <e-pane size="20%"><div>Right Panel</div></e-pane>
    </e-panes>
  </SplitterComponent>
</template>
```

#### Nested Splitters

Combine horizontal and vertical splitters for complex layouts like code editors with file explorer, editor, and console panels.

---

## Timeline

The Syncfusion Vue 3 **TimelineComponent** displays events or steps in chronological order with visual indicators. Supports vertical/horizontal layouts, multiple alignment modes (Before, After, Alternate, AlternateReverse), customizable dots and connectors, templates, and events.

### Quick Start

```vue
<template>
  <div style="height: 350px;">
    <TimelineComponent>
      <e-items>
        <e-item content="Shipped" />
        <e-item content="Departed" />
        <e-item content="Arrived" />
        <e-item content="Out for Delivery" />
      </e-items>
    </TimelineComponent>
  </div>
</template>

<script setup>
import { TimelineComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-vue-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-vue-layouts/styles/tailwind3.css';
</script>
```

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/timeline-getting-started.md](references/timeline-getting-started.md)
- Installation via npm
- CSS imports and theme setup
- Basic TimelineComponent structure
- `<e-items>` / `<e-item>` vs. items array
- Container height requirement
- Running the application

#### Layout Configuration
📄 **Read:** [references/timeline-layout-configuration.md](references/timeline-layout-configuration.md)
- Orientation options (Vertical, Horizontal)
- Alignment modes (Before, After, Alternate, AlternateReverse)
- Content positioning strategies
- Choosing the right layout for your use case
- Globalization and persistence

#### Items and Content
📄 **Read:** [references/timeline-items-and-content.md](references/timeline-items-and-content.md)
- Items array property (data-driven)
- String content and multiline strings
- Template-based content with slots/props
- Opposite content configuration
- Dot customization (icons, images, text, colors, sizes)
- Disabling items and per-item CSS classes

#### Styling & Customization
📄 **Read:** [references/timeline-styling-and-customization.md](references/timeline-styling-and-customization.md)
- Connector styling (common and per-item)
- Dot color, size, shadow, outline, variants
- CSS custom properties (--dot-size, --dot-color, --connector-color)
- e-outline class usage
- Complete customization examples

#### Events and Callbacks
📄 **Read:** [references/timeline-events-and-callbacks.md](references/timeline-events-and-callbacks.md)
- created event when component renders
- beforeItemRender event for item customization
- TimelineRenderingEventArgs (item, itemIndex, element)
- Event handling patterns

#### Advanced Features
📄 **Read:** [references/timeline-advanced-features.md](references/timeline-advanced-features.md)
- template property for complete custom rendering
- Template context (item, itemIndex)
- reverse property for newest-first display
- Complex template patterns
- When to use templates vs. built-in properties

#### Accessibility
📄 **Read:** [references/timeline-accessibility.md](references/timeline-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- ARIA attributes and roles
- Keyboard navigation support
- RTL (Right-to-Left) language support
- Mobile device accessibility

### Key Props

| Prop | Type | Values | Purpose |
|------|------|--------|---------|
| `orientation` | string | `Vertical` (default), `Horizontal` | Layout direction |
| `align` | string | `Before`, `After`, `Alternate`, `AlternateReverse` | Content positioning |
| `reverse` | boolean | `true`, `false` | Reverse item order |
| `cssClass` | string | CSS class name | Global styling |
| `template` | function | Render function | Custom item rendering |
| `content` (item) | string/function | Text or template | Event text/content |
| `oppositeContent` (item) | string/function | Secondary content | Secondary content |
| `dotCss` (item) | string | CSS class | Dot styling |
| `disabled` (item) | boolean | `true`, `false` | Disable item |
| `cssClass` (item) | string | CSS class | Per-item styling |

### Common Patterns

#### Vertical Timeline with Before Alignment

```vue
<template>
  <TimelineComponent orientation="Vertical" align="Before">
    <e-items>
      <e-item content="Step 1" oppositeContent="Description" />
      <e-item content="Step 2" oppositeContent="Description" />
    </e-items>
  </TimelineComponent>
</template>
```

#### Horizontal Alternate Layout

```vue
<template>
  <TimelineComponent orientation="Horizontal" align="Alternate">
    <e-items>
      <e-item content="Event 1" oppositeContent="Date 1" />
      <e-item content="Event 2" oppositeContent="Date 2" />
    </e-items>
  </TimelineComponent>
</template>
```

#### Timeline with Custom Dots and Icons

```vue
<template>
  <TimelineComponent>
    <e-items>
      <e-item content="Shipped" dotCss="e-icons e-package" />
      <e-item content="Delivered" dotCss="e-icons e-check" cssClass="state-completed" />
    </e-items>
  </TimelineComponent>
</template>
```

#### Activity Feed with Reverse Order

```vue
<template>
  <TimelineComponent :reverse="true">
    <e-items>
      <e-item content="Latest activity" />
      <e-item content="Previous activity" />
    </e-items>
  </TimelineComponent>
</template>
```

---

## Shared Conventions

### Installation & Setup

All layout components (except Card CSS-only) require:
```bash
npm install @syncfusion/ej2-base @syncfusion/ej2-vue-layouts
```

CSS imports must precede component usage:
```vue
<script setup>
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-vue-layouts/styles/tailwind3.css';
</script>
```

### Component Pattern (Layouts: Dashboard, Splitter, Timeline)

```vue
<template>
  <Component id="my-component" orientation="Vertical">
    <e-items>
      <e-item content="Item 1" />
      <e-item content="Item 2" />
    </e-items>
  </Component>
</template>
```

### Refs & Imperative Methods

DashboardLayout, Splitter, and ListView support `ref()` for imperative control:
```vue
<script setup>
import { ref } from 'vue';

const componentRef = ref(null);

const callMethod = () => {
  componentRef.value?.methodName(args);
};
</script>

<template>
  <Component ref="componentRef" />
</template>
```

### Event Naming Convention

Syncfusion uses lowercase event names without `on` prefix:
- Vue standard: `@click`, `@change`
- Syncfusion: `@change`, `@select`, `@created`, `@dragStart`

### State Management

Use `ref()` or `reactive()` with the `change` or `select` event to keep state in sync:
```vue
<script setup>
import { ref } from 'vue';
const value = ref(null);
const handleChange = (e) => { value.value = e.value; };
</script>

<template>
  <Component :value="value" @change="handleChange" />
</template>
```

### RTL Support

All components support `:enableRtl="true"` for right-to-left languages.

### Persistence

All components support `:enablePersistence="true"` to save state across page reloads.

---

## Common Pitfalls

### CSS Not Applied
- Confirm CSS imports point to `node_modules/@syncfusion/ej2-vue-layouts/styles/` and load before component styles.
- Choose only one theme (e.g., tailwind3) to avoid conflicts.

### Vue State Mismatch
- Use the `v-model` or `value` prop and `@change` event to keep Vue state in sync. Do not rely on framework-specific bindings.
- For ListView, set state via the `@select` event handler.

### Container Height Required
- Timeline: container must have explicit `style="height: 350px;"`. Without it, items will not render.
- Splitter: parent container should have explicit height for proper rendering.
- ListView: set explicit height when used inside flex containers.

### Ref is Undefined
- Properly import and use `ref(null)`.
- Attach the ref to the component: `<Component ref="componentRef" />`.
- Access the instance via `componentRef.value` (not `componentRef.current`).

### Splitter Pane Content Not Showing
- Ensure each `<e-pane>` wraps content in a child element.
- Verify size is provided (px or %).

### Dashboard Panels Not Displaying
- Ensure all panels have required properties: `id`, `row`, `col`.
- Verify `panels` array is passed to the component.
- Check that panel `sizeX` and `sizeY` do not exceed `columns` count.

### Card Layout Misalignment
- Use `e-card-horizontal` AND `e-card-stacked` together for horizontal cards.
- For flex parents, set explicit height and use `overflow: auto` with `min-height: 0` on scrollable children.

### ListView Alignment Issues
- Wrap ListView in a flex container with `display: flex` and `flex-direction: column`.
- Set `width: '100%'` and `height: '100%'` on ListView to fill container.
- Use `gap` in templates instead of individual margins.

### TypeScript Errors
- Import types explicitly: `import { DashboardLayoutComponent, PanelModel } from '@syncfusion/ej2-vue-layouts'`.
- Use proper ref types: `ref<DashboardLayoutComponent | null>(null)`.

---

## Component Selection Guide

| Need | Use |
|------|-----|
| Display content in a structured card with header/image/buttons | **Card** |
| Build a customizable dashboard with draggable panels | **DashboardLayout** |
| Display a scrollable list of items with selection/filtering | **ListView** |
| Create resizable multi-pane layouts (split views) | **Splitter** |
| Show events in chronological order with visual indicators | **Timeline** |

---

**Next Steps:** Choose a reference file based on your specific component need, then implement your layout following the examples and patterns provided. The unified structure makes it easy to combine multiple layout components (e.g., Cards inside a Splitter, ListView inside a Card, Timeline items inside a DashboardLayout panel).
