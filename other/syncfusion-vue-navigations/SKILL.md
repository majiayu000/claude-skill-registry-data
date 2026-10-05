---
name: syncfusion-vue-navigations
description: Guides Syncfusion Vue 3 navigation components such as AppBar, Accordion, Breadcrumb, Sidebar, and Tabs. Use this when building responsive menus, tabbed layouts, and step-based workflows with Vue 3 Composition API.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation Components"
---

# Syncfusion Vue 3 Navigation Components

> 📌 **Agent Notice:** `📄 Read:` links in Navigation Guide sections are reference pointers for passive file reading only. They do not imply automatic tool invocation, command execution, or action chaining.

---

## Overview

This consolidated skill provides comprehensive guidance for implementing **11 Syncfusion Vue 3 navigation components** that work together to build complete navigation ecosystems. Whether you're building single navigation features or complex multi-level navigation systems, this skill covers all components, patterns, accessibility requirements, and best practices.

### Components Included

| Component | Purpose | Best For |
|-----------|---------|----------|
| **AppBar** | Top/bottom navigation header | Application chrome, branding, action buttons |
| **Accordion** | Expandable/collapsible content panels | FAQs, settings panels, content organization |
| **Breadcrumb** | Hierarchical location indicator | Site navigation trails, file paths |
| **Carousel** | Rotating content/image display | Image galleries, testimonials, product showcases |
| **ContextMenu** | Right-click popup menu | File operations, data grid actions |
| **Menu** | Hierarchical dropdown navigation | Application menus, navigation bars |
| **Sidebar** | Side-slide navigation panel | Responsive menus, drawer navigation |
| **Tabs** | Tab-based content switching | Multi-view layouts, wizard steps |
| **Toolbar** | Command/button bar | Editing tools, action groups |
| **TreeView** | Hierarchical node display | File explorers, organizational charts |
| **Stepper** | Step-by-step workflow guide | Wizards, checkout flows, onboarding |

---

## Quick Component Selector

**Need to build...**

- **Top/bottom action bar?** → [AppBar](#appbar-section)
- **Expandable content sections?** → [Accordion](#accordion-section)
- **Breadcrumb trail?** → [Breadcrumb](#breadcrumb-section)
- **Image/content carousel?** → [Carousel](#carousel-section)
- **Right-click menu?** → [ContextMenu](#contextmenu-section)
- **Dropdown menus?** → [Menu](#menu-section)
- **Slide-out drawer?** → [Sidebar](#sidebar-section)
- **Tabbed interface?** → [Tabs](#tabs-section)
- **Toolbar with buttons?** → [Toolbar](#toolbar-section)
- **File/tree hierarchy?** → [TreeView](#treeview-section)
- **Multi-step wizard?** → [Stepper](#stepper-section)

---

## AppBar

**Purpose:** Create responsive navigation headers and toolbars at the top or bottom of your application.

**When to Use:**
- Application header/chrome with branding
- Navigation buttons and action buttons
- Sticky navigation that stays visible while scrolling
- Responsive toolbars that adapt to screen size
- Dark/light/primary color modes

**Key Props:**
- `colorMode` - Light, Dark, Primary, Inherit
- `mode` - Regular, Prominent, Dense
- `position` - Top, Bottom
- `isSticky` - Stick to viewport while scrolling

**Documentation:**
- 📄 **Read:** [references/appbar-getting-started.md](references/appbar-getting-started.md) - Installation and setup
- 📄 **Read:** [references/appbar-positioning-and-layout.md](references/appbar-positioning-and-layout.md) - Layout and positioning
- 📄 **Read:** [references/appbar-size-and-color-modes.md](references/appbar-size-and-color-modes.md) - Styling modes
- 📄 **Read:** [references/appbar-design-patterns.md](references/appbar-design-patterns.md) - Integration patterns
- 📄 **Read:** [references/appbar-styling-and-accessibility.md](references/appbar-styling-and-accessibility.md) - Accessibility
- 📄 **Read:** [references/appbar-api-reference.md](references/appbar-api-reference.md) - Complete API

**Quick Example:**
```vue
<template>
  <ejs-appbar color-mode="Primary">
    <button class="e-btn e-inherit e-icon-btn">
      <span class="e-icons e-menu"></span>
    </button>
    <span>My App</span>
    <div class="e-appbar-spacer"></div>
    <button class="e-btn e-inherit">Login</button>
  </ejs-appbar>
</template>

<script setup>
import { AppBarComponent } from "@syncfusion/ej2-vue-navigations";
</script>
```

---

## Accordion

**Purpose:** Display collapsible content panels for organizing information into expandable sections.

**When to Use:**
- FAQ sections with question/answer pairs
- Settings panels with collapsible options
- Multi-step forms
- Content organization
- Navigation with expandable items

**Key Props:**
- `expandMode` - Single, Multiple
- `expandedIndices` - Initially expanded items
- `animation` - Configure expand/collapse animations
- `dataSource` - Bind accordion items to data

**Documentation:**
- 📄 **Read:** [references/accordion-getting-started.md](references/accordion-getting-started.md) - Installation and setup
- 📄 **Read:** [references/accordion-expand-modes.md](references/accordion-expand-modes.md) - Single vs Multiple mode
- 📄 **Read:** [references/accordion-animation-effects.md](references/accordion-animation-effects.md) - Animations
- 📄 **Read:** [references/accordion-content-loading.md](references/accordion-content-loading.md) - Dynamic content
- 📄 **Read:** [references/accordion-events-lifecycle.md](references/accordion-events-lifecycle.md) - Events
- 📄 **Read:** [references/accordion-styling-customization.md](references/accordion-styling-customization.md) - Styling
- 📄 **Read:** [references/accordion-advanced-features.md](references/accordion-advanced-features.md) - Advanced patterns

**Quick Example:**
```vue
<template>
  <ejs-accordion :expandMode="'Multiple'">
    <e-accordion-items>
      <e-accordion-item header="Question 1" content="Answer 1" />
      <e-accordion-item header="Question 2" content="Answer 2" />
    </e-accordion-items>
  </ejs-accordion>
</template>

<script setup>
import { AccordionComponent, AccordionItemsDirective, AccordionItemDirective } from '@syncfusion/ej2-vue-navigations';
</script>
```

---

## Breadcrumb

**Purpose:** Display hierarchical navigation path showing user's current location.

**When to Use:**
- Website breadcrumb trails
- File path display
- Navigation history
- Multi-level category display
- Link-based navigation

**Key Props:**
- `items` - Array of breadcrumb items with text and URLs
- `enableNavigation` - Enable/disable click navigation
- `maxItems` - Maximum items before overflow
- `overflowMode` - Menu, Collapsed, Scroll, etc.

**Documentation:**
- 📄 **Read:** [references/breadcrumb-getting-started.md](references/breadcrumb-getting-started.md) - Installation and setup
- 📄 **Read:** [references/breadcrumb-navigation-and-routing.md](references/breadcrumb-navigation-and-routing.md) - Navigation patterns
- 📄 **Read:** [references/breadcrumb-customization.md](references/breadcrumb-customization.md) - Customization
- 📄 **Read:** [references/breadcrumb-icon-integration-data-binding.md](references/breadcrumb-icon-integration-data-binding.md) - Icons and data
- 📄 **Read:** [references/breadcrumb-accessibility.md](references/breadcrumb-accessibility.md) - Accessibility
- 📄 **Read:** [references/breadcrumb-api-properties-and-events.md](references/breadcrumb-api-properties-and-events.md) - Complete API

**Quick Example:**
```vue
<template>
  <ejs-breadcrumb :items="items"></ejs-breadcrumb>
</template>

<script setup>
import { ref } from 'vue';
import { BreadcrumbComponent } from '@syncfusion/ej2-vue-navigations';

const items = ref([
  { text: 'Home', url: '/' },
  { text: 'Products', url: '/products' },
  { text: 'Electronics', url: '/products/electronics' }
]);
</script>
```

---

## Carousel

**Purpose:** Display rotating/sliding content such as images, testimonials, or product showcases.

**When to Use:**
- Image galleries with auto-play
- Product carousels
- Testimonial sliders
- Content rotators
- Image presentations

**Key Props:**
- `selectedIndex` - Currently active slide
- `itemsPerSlide` - Items visible at once
- `autoPlay` - Auto-rotate slides
- `showNavigators` - Previous/next buttons
- `showIndicators` - Slide indicators

**Documentation:**
- 📄 **Read:** [references/carousel-getting-started.md](references/carousel-getting-started.md) - Installation and setup
- 📄 **Read:** [references/carousel-populating-items.md](references/carousel-populating-items.md) - Add slide content
- 📄 **Read:** [references/carousel-navigators-and-indicators.md](references/carousel-navigators-and-indicators.md) - Navigation controls
- 📄 **Read:** [references/carousel-animations-and-transitions.md](references/carousel-animations-and-transitions.md) - Transitions
- 📄 **Read:** [references/carousel-styling-and-appearance.md](references/carousel-styling-and-appearance.md) - Styling
- 📄 **Read:** [references/carousel-accessibility.md](references/carousel-accessibility.md) - Accessibility

**Quick Example:**
```vue
<template>
  <ejs-carousel :selectedIndex="0">
    <e-carousel-items>
      <e-carousel-item>
        <img src="image1.jpg" />
      </e-carousel-item>
      <e-carousel-item>
        <img src="image2.jpg" />
      </e-carousel-item>
    </e-carousel-items>
  </ejs-carousel>
</template>

<script setup>
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from '@syncfusion/ej2-vue-navigations';
</script>
```

---

## ContextMenu

**Purpose:** Display popup menus triggered by right-click or context actions.

**When to Use:**
- Right-click context menus
- File explorer operations
- Data grid row actions
- Custom action menus
- Mobile touch-hold menus

**Key Props:**
- `items` - Menu items with nested structure
- `target` - Element selector to attach menu to
- `enableHtmlSanitizer` - Security for user content
- `enableRtl` - Right-to-left support

**Documentation:**
- 📄 **Read:** [references/contextmenu-getting-started.md](references/contextmenu-getting-started.md) - Installation and setup
- 📄 **Read:** [references/contextmenu-menu-items-and-data-binding.md](references/contextmenu-menu-items-and-data-binding.md) - Menu structure
- 📄 **Read:** [references/contextmenu-events-and-interaction.md](references/contextmenu-events-and-interaction.md) - Events
- 📄 **Read:** [references/contextmenu-templates-and-customization.md](references/contextmenu-templates-and-customization.md) - Templates
- 📄 **Read:** [references/contextmenu-advanced-features.md](references/contextmenu-advanced-features.md) - Advanced patterns
- 📄 **Read:** [references/contextmenu-use-cases-and-patterns.md](references/contextmenu-use-cases-and-patterns.md) - Real-world patterns

**Quick Example:**
```vue
<template>
  <div id="target" @contextmenu.prevent>
    Right-click here
  </div>
  <ejs-contextmenu :items="menuItems" target="#target"></ejs-contextmenu>
</template>

<script setup>
import { ref } from 'vue';
import { ContextMenuComponent } from '@syncfusion/ej2-vue-navigations';

const menuItems = ref([
  { text: 'Cut' },
  { text: 'Copy' },
  { text: 'Paste' }
]);
</script>
```

---

## Menu

**Purpose:** Create hierarchical dropdown menus for navigation and selection.

**When to Use:**
- Application menus (File, Edit, Help)
- Navigation bars
- Dropdown menus
- Submenu hierarchies
- Hamburger/mobile menus

**Key Props:**
- `items` - Menu items with hierarchical structure
- `hamburgerMode` - Mobile-friendly mode
- `enableScrolling` - Scrollable menus
- `orientation` - Horizontal or Vertical

**Documentation:**
- 📄 **Read:** [references/menu-getting-started.md](references/menu-getting-started.md) - Installation and setup
- 📄 **Read:** [references/menu-properties-and-configuration.md](references/menu-properties-and-configuration.md) - Configuration
- 📄 **Read:** [references/menu-data-binding.md](references/menu-data-binding.md) - Data sources
- 📄 **Read:** [references/menu-menu-items-customization.md](references/menu-menu-items-customization.md) - Dynamic items
- 📄 **Read:** [references/menu-events-and-callbacks.md](references/menu-events-and-callbacks.md) - Events
- 📄 **Read:** [references/menu-styling-and-appearance.md](references/menu-styling-and-appearance.md) - Styling
- 📄 **Read:** [references/menu-hamburger-mode.md](references/menu-hamburger-mode.md) - Mobile mode
- 📄 **Read:** [references/menu-methods-api.md](references/menu-methods-api.md) - Methods

**Quick Example:**
```vue
<template>
  <ejs-menu :items="menuItems"></ejs-menu>
</template>

<script setup>
import { ref } from 'vue';
import { MenuComponent } from '@syncfusion/ej2-vue-navigations';

const menuItems = ref([
  {
    text: 'File',
    items: [
      { text: 'New' },
      { text: 'Open' },
      { text: 'Save' }
    ]
  }
]);
</script>
```

---

## Sidebar

**Purpose:** Create slide-out side navigation panels.

**When to Use:**
- Mobile-responsive navigation
- Drawer menus
- Side panel navigation
- Dashboard sidebars
- Content organization sidebars

**Key Props:**
- `type` - Over, Push, Slide, Auto
- `width` - Sidebar width
- `enableGestures` - Touch/swipe support
- `isOpen` - Open/closed state

**Documentation:**
- 📄 **Read:** [references/sidebar-getting-started.md](references/sidebar-getting-started.md) - Installation and setup
- 📄 **Read:** [references/sidebar-opening-closing.md](references/sidebar-opening-closing.md) - Open/close patterns
- 📄 **Read:** [references/sidebar-sidebar-positioning.md](references/sidebar-sidebar-positioning.md) - Positioning
- 📄 **Read:** [references/sidebar-content-integration.md](references/sidebar-content-integration.md) - Content integration
- 📄 **Read:** [references/sidebar-styling-customization.md](references/sidebar-styling-customization.md) - Styling
- 📄 **Read:** [references/sidebar-accessibility.md](references/sidebar-accessibility.md) - Accessibility
- 📄 **Read:** [references/sidebar-events-reference.md](references/sidebar-events-reference.md) - Events

**Quick Example:**
```vue
<template>
  <ejs-sidebar width="250px" type="Over" :isOpen="isOpen" @change="toggleSidebar">
    <ul>
      <li><a href="#home">Home</a></li>
      <li><a href="#about">About</a></li>
    </ul>
  </ejs-sidebar>
  <button @click="toggleSidebar">☰ Menu</button>
</template>

<script setup>
import { ref } from 'vue';
import { SidebarComponent } from '@syncfusion/ej2-vue-navigations';

const isOpen = ref(false);
const toggleSidebar = () => { isOpen.value = !isOpen.value; };
</script>
```

---

## Tabs

**Purpose:** Organize content into tabbed sections.

**When to Use:**
- Multi-view interfaces
- Tabbed content organization
- Step-by-step wizards
- Settings panels
- Responsive content switching

**Key Props:**
- `headerPlacement` - Top, Bottom, Left, Right
- `selectedItem` - Active tab index
- `allowDragAndDrop` - Reorderable tabs
- `heightAdjustMode` - Auto, Content, Fill

**Documentation:**
- 📄 **Read:** [references/tabs-getting-started.md](references/tabs-getting-started.md) - Installation and setup
- 📄 **Read:** [references/tabs-populating-items.md](references/tabs-populating-items.md) - Tab content
- 📄 **Read:** [references/tabs-header-styling.md](references/tabs-header-styling.md) - Header styling
- 📄 **Read:** [references/tabs-orientation-overflow.md](references/tabs-orientation-overflow.md) - Orientation and overflow
- 📄 **Read:** [references/tabs-drag-drop-reordering.md](references/tabs-drag-drop-reordering.md) - Drag and drop
- 📄 **Read:** [references/tabs-accessibility-localization.md](references/tabs-accessibility-localization.md) - Accessibility

**Quick Example:**
```vue
<template>
  <ejs-tab>
    <e-tab-items>
      <e-tab-item :header="{ text: 'Tab 1' }">
        <template #content>Content 1</template>
      </e-tab-item>
      <e-tab-item :header="{ text: 'Tab 2' }">
        <template #content>Content 2</template>
      </e-tab-item>
    </e-tab-items>
  </ejs-tab>
</template>

<script setup>
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-vue-navigations';
</script>
```

---

## Toolbar

**Purpose:** Create command bars with buttons, separators, and input components.

**When to Use:**
- Text editor toolbars
- File operation commands
- Format/styling buttons
- Application command bars
- Tool buttons with icons

**Key Props:**
- `items` - Button, Separator, Input types
- `overflowMode` - Scrollable, Popup, MultiRow, Extended
- `width` - Toolbar width
- `allowKeyboard` - Keyboard navigation

**Documentation:**
- 📄 **Read:** [references/toolbar-getting-started.md](references/toolbar-getting-started.md) - Installation and setup
- 📄 **Read:** [references/toolbar-item-configuration.md](references/toolbar-item-configuration.md) - Item types
- 📄 **Read:** [references/toolbar-responsive-modes.md](references/toolbar-responsive-modes.md) - Overflow modes
- 📄 **Read:** [references/toolbar-accessibility.md](references/toolbar-accessibility.md) - Accessibility
- 📄 **Read:** [references/toolbar-styling-customization.md](references/toolbar-styling-customization.md) - Styling
- 📄 **Read:** [references/toolbar-advanced-features.md](references/toolbar-advanced-features.md) - Templates and components

**Quick Example:**
```vue
<template>
  <ejs-toolbar>
    <e-items>
      <e-item text="Cut"></e-item>
      <e-item text="Copy"></e-item>
      <e-item type="Separator"></e-item>
      <e-item text="Bold"></e-item>
    </e-items>
  </ejs-toolbar>
</template>

<script setup>
import { ToolbarComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-vue-navigations';
</script>
```

---

## TreeView

**Purpose:** Display hierarchical data in a tree structure with nodes.

**When to Use:**
- File explorers
- Organizational charts
- Category/product hierarchies
- Navigation trees
- Data hierarchies with selection

**Key Props:**
- `fields` - Data field mappings
- `allowMultiSelection` - Single/multi-select
- `allowDragAndDrop` - Reorderable nodes
- `showCheckBox` - Checkbox selection

**Documentation:**
- 📄 **Read:** [references/treeview-getting-started.md](references/treeview-getting-started.md) - Installation and setup
- 📄 **Read:** [references/treeview-data-binding.md](references/treeview-data-binding.md) - Data sources
- 📄 **Read:** [references/treeview-templates-and-rendering.md](references/treeview-templates-and-rendering.md) - Custom templates
- 📄 **Read:** [references/treeview-node-operations.md](references/treeview-node-operations.md) - CRUD operations
- 📄 **Read:** [references/treeview-selection-and-checking.md](references/treeview-selection-and-checking.md) - Selection modes
- 📄 **Read:** [references/treeview-drag-drop-and-reordering.md](references/treeview-drag-drop-and-reordering.md) - Drag and drop
- 📄 **Read:** [references/treeview-filtering-and-searching.md](references/treeview-filtering-and-searching.md) - Filtering
- 📄 **Read:** [references/treeview-keyboard-and-accessibility.md](references/treeview-keyboard-and-accessibility.md) - Accessibility

**Quick Example:**
```vue
<template>
  <ejs-treeview 
    :fields="{ dataSource: data, id: 'id', text: 'name', parentID: 'pid' }"
    :allowMultiSelection="true"
  ></ejs-treeview>
</template>

<script setup>
import { ref } from 'vue';
import { TreeViewComponent } from '@syncfusion/ej2-vue-navigations';

const data = ref([
  { id: 1, name: 'Parent', pid: null },
  { id: 2, name: 'Child 1', pid: 1 },
  { id: 3, name: 'Child 2', pid: 1 }
]);
</script>
```

---

## Stepper

**Purpose:** Guide users through multi-step processes or workflows.

**When to Use:**
- Checkout wizards
- Registration flows
- Setup wizards
- Multi-step forms
- Onboarding processes

**Key Props:**
- `steps` - Array of step definitions
- `activeStep` - Currently active step
- `orientation` - Horizontal or Vertical
- `stepType` - Default, Label, Indicator

**Documentation:**
- 📄 **Read:** [references/stepper-getting-started.md](references/stepper-getting-started.md) - Installation and setup
- 📄 **Read:** [references/stepper-steps-and-configuration.md](references/stepper-steps-and-configuration.md) - Step configuration
- 📄 **Read:** [references/stepper-orientations-and-types.md](references/stepper-orientations-and-types.md) - Layout options
- 📄 **Read:** [references/stepper-events-and-interactions.md](references/stepper-events-and-interactions.md) - Events
- 📄 **Read:** [references/stepper-linear-flow-and-validation.md](references/stepper-linear-flow-and-validation.md) - Validation
- 📄 **Read:** [references/stepper-animation-template-tooltip.md](references/stepper-animation-template-tooltip.md) - Customization
- 📄 **Read:** [references/stepper-methods-and-advanced.md](references/stepper-methods-and-advanced.md) - Advanced patterns

**Quick Example:**
```vue
<template>
  <ejs-stepper :steps="steps" :activeStep="activeStep"></ejs-stepper>
</template>

<script setup>
import { ref } from 'vue';
import { StepperComponent } from '@syncfusion/ej2-vue-navigations';

const steps = ref([
  { text: 'Step 1' },
  { text: 'Step 2' },
  { text: 'Step 3' }
]);
const activeStep = ref(0);
</script>
```

---

## Common Vue 3 Patterns Across All Components

### Reactive State Management
```vue
<script setup>
import { ref, reactive } from 'vue';

// Simple reactive value
const selectedIndex = ref(0);

// Complex object state
const config = reactive({
  enabled: true,
  cssClass: 'e-primary',
  animation: { duration: 300 }
});
</script>
```

### Event Handling
```vue
<template>
  <ejs-component @select="handleSelect" @created="onCreated" />
</template>

<script setup>
const handleSelect = (args) => {
  console.log('Selected:', args.index);
};

const onCreated = () => {
  console.log('Component initialized');
};
</script>
```

### Template Refs for Method Calls
```vue
<template>
  <button @click="callMethod">Action</button>
  <ejs-component ref="componentRef" />
</template>

<script setup>
import { ref } from 'vue';

const componentRef = ref(null);

const callMethod = () => {
  componentRef.value?.methodName?.();
};
</script>
```

### Computed Properties for Derived State
```vue
<template>
  <ejs-component :disabled="isLoading" />
</template>

<script setup>
import { ref, computed } from 'vue';

const status = ref('idle');

const isLoading = computed(() => status.value === 'loading');
</script>
```

---

## Installation and Setup

### Install All Required Packages

```bash
npm install @syncfusion/ej2-vue-navigations @syncfusion/ej2-base
npm install @syncfusion/ej2-vue-buttons    # For AppBar content
npm install @syncfusion/ej2-vue-popups    # For menus/dropdowns
```

### CSS Imports (Pick a theme)

```javascript
// In main.ts or component
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-vue-navigations/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';

// Available themes: tailwind3.css, bootstrap5.css, material.css, fluent.css
```

---

## Accessibility Across All Components

- **WCAG 2.2 Level AA** compliance
- **Keyboard Navigation:** Arrow keys, Tab, Enter, Escape
- **ARIA Attributes:** Proper roles and labels
- **Screen Reader Support:** Full compatibility
- **RTL Support:** Right-to-left language support
- **Color Contrast:** Meets accessibility standards
- **Focus Management:** Clear focus indicators

---

## Next Steps

1. **Choose your component** from the component selector above
2. **Read the Getting Started** reference for basic setup
3. **Explore specific features** using the documentation links
4. **Review examples** for your use case
5. **Check Accessibility** guide for WCAG compliance
6. **Consult API Reference** for complete property/event documentation

---

## Related Resources

- [Syncfusion Vue Documentation](https://ej2.syncfusion.com/vue/)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [WCAG 2.2 Standards](https://www.w3.org/WAI/WCAG22/quickref/)
- [Accessibility Testing](https://www.webAIM.org/)

````
