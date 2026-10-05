---
name: syncfusion-vue-buttons
description: Comprehensive guide for implementing Syncfusion Vue 3 button components including Button, ButtonGroup, DropDownButton, Floating Action Button, ProgressButton, SplitButton, Speed Dial, Switch, RadioButton, and Chips. Use this when adding styled buttons, toggle behavior, icon support, grouped selections, dropdown action menus, programmatic control floating primary actions, expandable speed dial menus, compact interactive elements with avatars and drag-and-drop, or single/multiple selection capabilities to a Vue application.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Buttons"
---

# Syncfusion Vue 3 Buttons

> 📌 **Agent Notice:** `📄 Read:` links in Navigation Guide sections are reference pointers for passive file reading only. They do not imply automatic tool invocation, command execution, or action chaining.

---

## Button

The Syncfusion `ButtonComponent` is a graphical user interface element that triggers an action on click. It supports text, icons, or both, with extensive styling, accessibility, and behavioral options.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/button-getting-started.md](references/button-getting-started.md)
- Installation and package setup (@syncfusion/ej2-vue-buttons)
- CSS imports and theme configuration
- Rendering the first ButtonComponent
- Enabling ripple effects
- Basic click handling with @click event

#### Types and Styles
📄 **Read:** [references/button-types-and-styles.md](references/button-types-and-styles.md)
- Predefined color styles (primary, success, info, warning, danger, link)
- Flat, outline, round, and toggle button types
- HTML button types (submit, reset)
- Icon buttons (font icons, SVG)
- Icon positioning (left/right)
- Button sizes (small, normal)

#### How-To Patterns
📄 **Read:** [references/button-how-to.md](references/button-how-to.md)
- Create a block (full-width) button
- Create a rounded-corner button
- Add a navigation link to a button
- Customize button appearance with CSS
- Style native input and anchor elements as buttons
- Set the disabled state
- Enable right-to-left (RTL) support
- Add a tooltip on hover
- Implement a repeat button

#### Style and Appearance
📄 **Read:** [references/button-style-and-appearance.md](references/button-style-and-appearance.md)
- Available CSS classes and their purposes
- Overriding default styles
- Custom theme creation with Theme Studio

#### Accessibility
📄 **Read:** [references/button-accessibility.md](references/button-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA attributes
- Keyboard navigation
- Screen reader support

#### API Reference
📄 **Read:** [references/button-api.md](references/button-api.md)
- All properties, methods, and events
- Property types, defaults, and constraints

---

### Quick Start

```bash
# Install package
npm install @syncfusion/ej2-vue-buttons --save
npm install @syncfusion/ej2-material3-theme --save
```

```vue
<template>
  <ejs-button :content="content"></ejs-button>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
//Component registration
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  },
  data() {
    return {
        content: "Button"
    };
  }
}
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/button/index.css";
</style>
```

---

### Common Patterns

#### Styled Button
```vue
<template>
  <div>
    <ejs-button :content="'Primary'" :isPrimary="true"></ejs-button>
    <ejs-button :content="'Danger'" cssClass="e-danger"></ejs-button>
    <ejs-button :content="'Flat'" cssClass="e-flat"></ejs-button>
    <ejs-button :content="'Outline'" cssClass="e-outline"></ejs-button>
  </div>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  }
}
</script>
```

#### Icon Button
```vue
<template>
  <div>
    <ejs-button iconCss="e-icons e-save" :content="'Save'"></ejs-button>
    <ejs-button iconCss="e-icons e-delete" :content="'Delete'" iconPosition="Right"></ejs-button>
  </div>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  }
}
</script>
```

#### Toggle Button
```vue
<template>
  <div>
    <ejs-button :isToggle="true" cssClass="e-flat" :content="activeContent"></ejs-button>
  </div>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  },
  data: function() {
    return {
      activeContent: "Play"
    };
  },
  methods: {
    toggleActive: function() {
      this.activeContent = this.activeContent === 'Play' ? 'Pause' : 'Play';
    }
  }
}
</script>
```

#### Disabled Button
```vue
<template>
  <ejs-button :disabled="true" :content="'Disabled'"></ejs-button>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  }
}
</script>
```

#### Block (Full-Width) Button
```vue
<template>
  <ejs-button cssClass="e-block e-primary" :content="'Full Width'"></ejs-button>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  }
}
</script>
```

---

## ButtonGroup

The ButtonGroup is a pure CSS component that groups a series of buttons together in a horizontal (default) or vertical layout. It supports normal button behavior as well as radio-type (single selection) and checkbox-type (multiple selection) behaviors. Buttons can be nested with DropDownButton and SplitButton components.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/buttongroup-getting-started.md](references/buttongroup-getting-started.md)
- Installation and package setup
- Adding CSS references and theme imports
- Basic ButtonGroup implementation
- Running the application

#### Types and Styles
📄 **Read:** [references/buttongroup-types-and-styles.md](references/buttongroup-types-and-styles.md)
- Outline ButtonGroup (e-outline)
- Predefined color styles (e-primary, e-success, e-info, e-warning, e-danger)
- Mixing styles within a group

#### Selection and Nesting
📄 **Read:** [references/buttongroup-selection-and-nesting.md](references/buttongroup-selection-and-nesting.md)
- Single selection (radio type)
- Multiple selection (checkbox type)
- Setting initial selected state
- Nesting DropDownButton inside ButtonGroup
- Nesting SplitButton inside ButtonGroup

#### How-To Guide
📄 **Read:** [references/buttongroup-how-to.md](references/buttongroup-how-to.md)
- Add icons to buttons (icon-css)
- Rounded corners (e-round-corner)
- Disable individual or all buttons
- Enable ripple effect
- Enable RTL support
- Vertical orientation (e-vertical)
- Form submit with radio/checkbox ButtonGroup
- Initialize using CSS classes

#### Style and Appearance
📄 **Read:** [references/buttongroup-style-and-appearance.md](references/buttongroup-style-and-appearance.md)
- Available CSS classes for customization
- Overriding hover, focus, active states
- Theme Studio integration

#### Accessibility
📄 **Read:** [references/buttongroup-accessibility.md](references/buttongroup-accessibility.md)
- WCAG 2.2, Section 508 compliance
- Keyboard navigation shortcuts
- Screen reader support

---

### Quick Start

```vue
<template>
  <div class="e-btn-group">
    <ejs-button>HTML</ejs-button>
    <ejs-button>CSS</ejs-button>
    <ejs-button>Javascript</ejs-button>
  </div>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
//Component registration
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  },
  data() {
    return {
    };
  }
}
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/button-group/index.css";
</style>
```

---

### Common Patterns

#### Radio (single-select) ButtonGroup
```vue
<template>
  <div class="e-btn-group">
    <input type="radio" id="radioleft" name="align" value="left" />
    <label class="e-btn" for="radioleft">Left</label>
    <input type="radio" id="radiomiddle" name="align" value="middle" />
    <label class="e-btn" for="radiomiddle">Center</label>
    <input type="radio" id="radioright" name="align" value="right" />
    <label class="e-btn" for="radioright">Right</label>
  </div>
</template>

<script>
export default {
  name: "App"
}
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/button-group/index.css";
</style>
```

#### Checkbox (multi-select) ButtonGroup
```vue
<template>
  <div class="e-btn-group">
    <input type="checkbox" id="checkbold" name="font" value="bold" />
    <label class="e-btn" for="checkbold">Bold</label>
    <input type="checkbox" id="checkitalic" name="font" value="italic" />
    <label class="e-btn" for="checkitalic">Italic</label>
    <input type="checkbox" id="checkline" name="font" value="underline" />
    <label class="e-btn" for="checkline">Underline</label>
  </div>
</template>

<script>
export default {
  name: "App"
}
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/button-group/index.css";
</style>
```

#### Vertical ButtonGroup
```vue
<template>
  <div class="e-btn-group e-vertical">
    <ejs-button>HTML</ejs-button>
    <ejs-button>CSS</ejs-button>
    <ejs-button>Javascript</ejs-button>
  </div>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';
export default {
  name: "App",
  components: {
    "ejs-button": ButtonComponent
  }
}
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/button-group/index.css";
</style>
```

---

### Key Props

| Prop / Class | Component | Description |
|---|---|---|
| `css-class` | `ButtonComponent` | Apply style classes (e-outline, e-primary, e-success, e-info, e-warning, e-danger) |
| `icon-css` | `ButtonComponent` | CSS class(es) for button icon |
| `:disabled` | `ButtonComponent` | Disables the button |
| `is-primary` | `ButtonComponent` | Marks button as primary |
| `e-btn-group` | container div | Required wrapper class for ButtonGroup |
| `e-outline` | container div + buttons | Outline style for the group |
| `e-round-corner` | container div | Rounded corners for the group |
| `e-vertical` | container div | Vertical layout |
| `e-rtl` | container div | Right-to-left layout |

---

## DropDownButton

The Syncfusion `DropDownButtonComponent` renders a button that toggles a contextual popup menu with a list of action items. It supports icons, separators, templates, animations, accessibility, and extensive customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/dropdownbutton-getting-started.md](references/dropdownbutton-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Rendering the first DropDownButtonComponent
- Binding data source with :items
- Minimal working example

#### Popup Items and Navigation
📄 **Read:** [references/dropdownbutton-popup-items.md](references/dropdownbutton-popup-items.md)
- Adding icons to popup items with icon-css
- Navigation URLs via url on items
- Separators to group popup items
- Item templates with before-item-render
- Popup (target) templates
- Underline characters in item text

#### Icons and Layout
📄 **Read:** [references/dropdownbutton-icons-and-layout.md](references/dropdownbutton-icons-and-layout.md)
- Button icons with icon-css and icon-position
- Icon-only buttons with e-caret-hide
- Sprite image icons
- Vertical button layout with e-vertical
- Customizing icon size and button width

#### Appearance and Styling
📄 **Read:** [references/dropdownbutton-appearance-and-styling.md](references/dropdownbutton-appearance-and-styling.md)
- CSS class overrides (color styles, sizes, states)
- Rounded corners with e-round-corner
- Hide dropdown arrow with e-caret-hide
- Popup width with popup-width
- Theme Studio customization
- Animation settings for popup open/close

#### Events and Interactivity
📄 **Read:** [references/dropdownbutton-events-and-interactivity.md](references/dropdownbutton-events-and-interactivity.md)
- Handling @select event on item click
- @before-open / @before-close for dynamic caret icon
- @open event for custom popup positioning
- Disabling the button with :disabled
- RTL support with enable-rtl
- Opening a dialog on item select
- Dynamic add-items / remove-items methods
- toggle() method for programmatic open/close

#### Item Template
📄 **Read:** [references/dropdownbutton-item-template.md](references/dropdownbutton-item-template.md)
- item-template property for custom item rendering
- Rendering links, icons, and rich content inside items

#### ListView Integration
📄 **Read:** [references/dropdownbutton-listview-integration.md](references/dropdownbutton-listview-integration.md)
- Using target property with a ListView element
- Grouped popup items with category headers

#### Accessibility
📄 **Read:** [references/dropdownbutton-accessibility.md](references/dropdownbutton-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes (role, aria-haspopup, aria-expanded)
- Keyboard navigation shortcuts
- Screen reader support

#### API Reference
📄 **Read:** [references/dropdownbutton-api.md](references/dropdownbutton-api.md)
- All properties with types and defaults
- All events with argument interfaces
- All methods with return types
- Type definitions and interfaces

---

### Quick Start

```vue
<template>
  <ejs-dropdownbutton :items='items'>Clipboard</ejs-dropdownbutton>
</template>

<script>
import { DropDownButtonComponent } from "@syncfusion/ej2-vue-splitbuttons";
export default {
  name: "App",
  components: { "ejs-dropdownbutton": DropDownButtonComponent },
  data () {
    return {
      items:[ { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' } ]
    };
  }
}
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/drop-down-button/index.css";
</style>
```

---

## Floating Action Button

The Syncfusion Vue `FabComponent` is a circular button that floats above the UI and represents the primary action in an application. It supports flexible positioning, icon + text content, predefined styles, full accessibility compliance, and CSS customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/floating-action-button-getting-started.md](references/floating-action-button-getting-started.md)
- Installing @syncfusion/ej2-vue-buttons
- CSS theme imports for Tailwind3
- Minimal FabComponent setup
- Using target to position relative to a container
- Handling the click event

#### Icons and Content
📄 **Read:** [references/floating-action-button-icons.md](references/floating-action-button-icons.md)
- icon-css prop for icon-only FAB
- content prop for text label
- icon-position for icon-left vs icon-right layout
- Combined icon + text examples

#### Positions
📄 **Read:** [references/floating-action-button-positions.md](references/floating-action-button-positions.md)
- position prop with all nine predefined values (TopLeft → BottomRight)
- target prop to scope FAB to a container
- Custom CSS position using css-class

#### Styles and Appearance
📄 **Read:** [references/floating-action-button-styles.md](references/floating-action-button-styles.md)
- Predefined css-class values: e-primary, e-outline, e-info, e-success, e-warning, e-danger
- CSS class override reference table
- Show text on hover with CSS transition
- Outline color customization

#### Events
📄 **Read:** [references/floating-action-button-events.md](references/floating-action-button-events.md)
- @click event for click handling
- @created event for post-render initialization

#### Accessibility
📄 **Read:** [references/floating-action-button-accessibility.md](references/floating-action-button-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes (aria-label, aria-disabled, role="button")
- Keyboard navigation (Enter, Space, Tab, Escape)
- RTL support via enable-rtl
- Screen reader support

#### API Reference
📄 **Read:** [references/floating-action-button-api.md](references/floating-action-button-api.md)
- All properties, methods, and events with types and defaults

---

## ProgressButton

The `ProgressButtonComponent` provides a button that visualizes the progression of a background operation — complete with an animated spinner, background progress bar fill, and content/style hooks at every stage.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/progressbutton-getting-started.md](references/progressbutton-getting-started.md)
- Installation and CSS imports
- Basic ProgressButtonComponent rendering
- Enabling progress mode

#### Spinner and Progress
📄 **Read:** [references/progressbutton-spinner-and-progress.md](references/progressbutton-spinner-and-progress.md)
- Spinner position/size/template
- Progress bar configuration
- Animations and step control
- Start/stop methods

#### Style and Appearance
📄 **Read:** [references/progressbutton-style-and-appearance.md](references/progressbutton-style-and-appearance.md)
- CSS classes and theming
- Theme Studio integration

#### Accessibility
📄 **Read:** [references/progressbutton-accessibility.md](references/progressbutton-accessibility.md)
- ARIA attributes and keyboard navigation
- Screen-reader compliance

#### How-To Guides
📄 **Read:** [references/progressbutton-how-to-enable-progress-in-button.md](references/progressbutton-how-to-enable-progress-in-button.md)
📄 **Read:** [references/progressbutton-how-to-hide-spinner.md](references/progressbutton-how-to-hide-spinner.md)
📄 **Read:** [references/progressbutton-how-to-customize-progress-using-cssclass.md](references/progressbutton-how-to-customize-progress-using-cssclass.md)
📄 **Read:** [references/progressbutton-how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md](references/progressbutton-how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md)
📄 **Read:** [references/progressbutton-how-to-trace-events-of-progress-button.md](references/progressbutton-how-to-trace-events-of-progress-button.md)

#### API Reference
📄 **Read:** [references/progressbutton-api.md](references/progressbutton-api.md)
- All properties, methods, and events

---

## RadioButton

A graphical UI element that lets users select exactly one option from a group. Supports checked/unchecked states, label positioning, small size, form integration, RTL, disabled state, and full CSS customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/radiobutton-getting-started.md](references/radiobutton-getting-started.md)
- Package installation and CSS import
- Basic RadioButtonComponent rendering
- Grouping radio buttons with name prop
- Enabling ripple effect

#### Label and Size
📄 **Read:** [references/radiobutton-label-and-size.md](references/radiobutton-label-and-size.md)
- Adding captions with the label property
- Positioning labels before/after with label-position
- Applying small size with css-class="e-small"

#### Features and State
📄 **Read:** [references/radiobutton-features-and-state.md](references/radiobutton-features-and-state.md)
- Setting checked/unchecked state
- Disabling a RadioButton
- Grouping and form submission with name and value
- RTL layout
- Handling state change via change event

#### Style and Appearance
📄 **Read:** [references/radiobutton-style-and-appearance.md](references/radiobutton-style-and-appearance.md)
- Overriding default CSS classes
- Creating semantic color variants
- Using css-class for custom styles
- Theme Studio integration

#### Accessibility
📄 **Read:** [references/radiobutton-accessibility.md](references/radiobutton-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation shortcuts
- Screen reader support

#### API Reference
📄 **Read:** [references/radiobutton-api.md](references/radiobutton-api.md)
- All properties, methods, and events

---

## Speed Dial

The `SpeedDialComponent` is a floating action button (FAB) that reveals a set of contextual action items when clicked or hovered. It supports Linear and Radial display modes, flexible positioning, templates, animations, modal overlay, and full accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/speeddial-getting-started.md](references/speeddial-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Rendering the first SpeedDialComponent
- Basic items configuration
- Target element setup

#### Items Configuration
📄 **Read:** [references/speeddial-items.md](references/speeddial-items.md)
- SpeedDialItemModel fields (text, icon-css, id, title, disabled)
- Icon only, text only, icon with text combinations
- Disabling individual items
- Animation effects (Fade, Zoom, etc.)

#### Display Modes
📄 **Read:** [references/speeddial-display-modes.md](references/speeddial-display-modes.md)
- Linear mode (default) and direction values (Up, Down, Left, Right, Auto)
- Radial mode overview and usage

#### Radial Menu
📄 **Read:** [references/speeddial-radial-menu.md](references/speeddial-radial-menu.md)
- Setting mode to Radial
- radialSettings configuration
- startAngle and endAngle
- offset to control item distance

#### Positions and Visibility
📄 **Read:** [references/speeddial-positions.md](references/speeddial-positions.md)
- Position values (TopLeft, TopCenter, TopRight, etc.)
- Target element relative positioning
- opensOnHover for hover-based open behavior
- Programmatic show() and hide() methods

#### Styles and Appearance
📄 **Read:** [references/speeddial-styles.md](references/speeddial-styles.md)
- openIconCss and closeIconCss for button icons
- content property for text button
- Predefined css-class values
- Custom CSS overrides

#### Events
📄 **Read:** [references/speeddial-events.md](references/speeddial-events.md)
- clicked, @created, @before-open, @open, @before-close, @close events
- Event argument types
- Cancel pattern for beforeOpen and beforeClose

#### Templates
📄 **Read:** [references/speeddial-template.md](references/speeddial-template.md)
- item-template for custom item rendering
- popup-template for full popup customization

#### Modal
📄 **Read:** [references/speeddial-modal.md](references/speeddial-modal.md)
- Enabling modal overlay
- Interaction blocking behavior
- Close on backdrop click

#### Accessibility
📄 **Read:** [references/speeddial-accessibility.md](references/speeddial-accessibility.md)
- WCAG 2.2, Section 508 compliance
- Keyboard navigation shortcuts
- Screen reader support

#### API Reference
📄 **Read:** [references/speeddial-api.md](references/speeddial-api.md)
- All properties, methods, and events

---

## SplitButton

A button that displays a primary action and a dropdown menu of secondary actions.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/splitbutton-getting-started.md](references/splitbutton-getting-started.md)
- Installation and package setup
- Basic SplitButton implementation
- CSS imports and themes
- First working example

#### Types and Styles
📄 **Read:** [references/splitbutton-types-and-styles.md](references/splitbutton-types-and-styles.md)
- Button styles (primary, success, info, warning, danger, link)
- Button types (flat, outline, round)
- Icon positioning (left, right, top, bottom)
- Size variations

#### Features
📄 **Read:** [references/splitbutton-features.md](references/splitbutton-features.md)
- Dropdown menu items
- Icon and text combinations
- Disabled state
- Event handling
- Dynamic item manipulation

#### API Reference
📄 **Read:** [references/splitbutton-api-reference.md](references/splitbutton-api-reference.md)
- Complete properties documentation
- Methods and their usage
- Event handlers and callbacks

#### Customization
📄 **Read:** [references/splitbutton-customization.md](references/splitbutton-customization.md)
- Custom CSS classes
- Theming and color schemes
- Custom icons and fonts
- Responsive design

#### Accessibility
📄 **Read:** [references/splitbutton-accessibility.md](references/splitbutton-accessibility.md)
- WCAG 2.1 compliance
- Keyboard navigation patterns
- ARIA attributes

---

## Switch

A graphical toggle control that switches between checked (on) and unchecked (off) states. Supports text labels, size variants, disabled state, form submission, RTL, programmatic control, and full CSS customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/switch-getting-started.md](references/switch-getting-started.md)
- Package installation and npm setup
- CSS theme imports
- Basic SwitchComponent rendering
- Checked state initialization

#### Features
📄 **Read:** [references/switch-features.md](references/switch-features.md)
- on-label / off-label text labels
- disabled property
- name and value for form submission
- css-class for custom styling
- enable-rtl for right-to-left support

#### Events and Methods
📄 **Read:** [references/switch-events-and-methods.md](references/switch-events-and-methods.md)
- @change event and ChangeEventArgs
- @before-change event to cancel state transitions
- @created lifecycle event
- toggle() method for programmatic state control

#### How-To
📄 **Read:** [references/switch-how-to.md](references/switch-how-to.md)
- Change switch size (small vs default)
- Prevent state change
- Set text labels
- Enable RTL layout
- Programmatic toggle

#### Style and Appearance
📄 **Read:** [references/switch-style-and-appearance.md](references/switch-style-and-appearance.md)
- CSS class reference table
- Customizing bar and handle shape
- Small size variant
- Theme Studio

#### API Reference
📄 **Read:** [references/switch-api.md](references/switch-api.md)
- All properties with types and defaults
- All methods and events

---

## Chips

The `ChipListComponent` renders compact, interactive elements representing inputs, attributes, or actions. Supports single/multiple selection, deletion, drag-and-drop, avatars, icons, templates, and rich styling.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/chips-getting-started.md](references/chips-getting-started.md)
- Installation and package setup
- CSS/theme imports
- Rendering a basic chip or chip list
- Running the application

#### Types and Selection
📄 **Read:** [references/chips-types-and-selection.md](references/chips-types-and-selection.md)
- Four chip types: Input, Choice, Filter, Action
- Single selection vs. multiple selection
- Deletable chips
- Pre-selecting chips

#### Customization
📄 **Read:** [references/chips-customization.md](references/chips-customization.md)
- Predefined styles
- Leading icon and avatar image
- Custom chip template
- htmlAttributes for custom HTML attributes

#### Drag and Drop
📄 **Read:** [references/chips-drag-and-drop.md](references/chips-drag-and-drop.md)
- Enabling drag and drop
- Restricting drag area
- Drag events
- Cross-container drag and drop

#### Style
📄 **Read:** [references/chips-style.md](references/chips-style.md)
- CSS overrides for chip styling
- Outline chip styling
- Selected chip customization
- Size customization

#### Accessibility
📄 **Read:** [references/chips-accessibility.md](references/chips-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- Keyboard navigation
- RTL support

#### API Reference
📄 **Read:** [references/chips-api.md](references/chips-api.md)
- All properties, methods, and events

---

## Common Vue 2 Patterns Across All Components

### Reactive State (data property)
```vue
<script>
export default {
  name: "App",
  data: function() {
    return {
      isActive: false,
      config: {
        disabled: false,
        cssClass: 'e-primary'
      }
    };
  }
};
</script>
```

### Event Handling
```vue
<template>
  <ejs-button @click="handleClick" @created="onCreated"></ejs-button>
</template>

<script>
export default {
  name: "App",
  methods: {
    handleClick: function(args) {
      console.log('Button clicked', args);
    },
    onCreated: function() {
      console.log('Component created');
    }
  }
};
</script>
```

### Template Refs for Method Calls
```vue
<template>
  <ejs-button ref="btnRef"></ejs-button>
</template>

<script>
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';

export default {
  name: "App",
  components: {
    'ejs-button': ButtonComponent
  },
  methods: {
    callMethod: function() {
      if (this.$refs.btnRef) {
        this.$refs.btnRef.click();
      }
    }
  }
};
</script>
```

### Computed Properties
```vue
<template>
  <ejs-button :disabled="isLoading"></ejs-button>
</template>

<script>
export default {
  name: "App",
  data: function() {
    return {
      status: 'pending'
    };
  },
  computed: {
    isLoading: function() {
      return this.status === 'pending';
    }
  }
};
</script>
```

### Component Props Binding
```vue
<template>
  <ejs-dropdownbutton :items="menuItems" :disabled="isDisabled"></ejs-dropdownbutton>
</template>

<script>
import { DropDownButtonComponent } from '@syncfusion/ej2-vue-buttons';

export default {
  name: "App",
  components: {
    'ejs-dropdownbutton': DropDownButtonComponent
  },
  data: function() {
    return {
      menuItems: [
        { text: 'Cut' },
        { text: 'Copy' }
      ],
      isDisabled: false
    };
  }
};

const isDisabled = ref(false);
</script>
```

---

## Next Steps

1. **Start with Button** → Read [references/button-getting-started.md](references/button-getting-started.md)
2. **Explore Button Group** → Read [references/buttongroup-getting-started.md](references/buttongroup-getting-started.md)
3. **Advanced Components** → Choose from DropdownButton, FloatingActionButton, ProgressButton, RadioButton, SpeedDial, SplitButton, Switch, or Chips
4. **API Reference** → Consult component-specific API documentation for detailed properties and methods
5. **Accessibility** → Review accessibility guides for WCAG compliance and screen reader support

---

## Key Takeaways

- **Vue 3 Composition API**: Use `ref()` for state, `computed()` for derived values, and template refs for method calls
- **Reactive Props**: Prefix prop names with `:` for v-bind binding (`:disabled`, `:items`, etc.)
- **Event Binding**: Use `@event-name` syntax (e.g., `@click`, `@select`, `@before-open`)
- **Kebab-Case Props**: Vue uses kebab-case for HTML attributes (icon-css, css-class, etc.)
- **CSS Imports**: Import Syncfusion base and component CSS in your main app
- **Component Refs**: Use `ref="varName"` to access component methods in `<script setup>`
- **Package**: Install `@syncfusion/ej2-vue-buttons` and related splitbuttons/popups packages
