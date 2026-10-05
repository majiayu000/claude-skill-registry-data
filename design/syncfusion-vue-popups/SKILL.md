---
name: syncfusion-vue-popups
description: Comprehensive guide for implementing Syncfusion Vue popup components including Dialog, ToolTip. Use this when building modal/modeless dialogs, confirmation popups, forms in dialogs, draggable windows, popovers, tooltips, and overlaid content with custom positioning, animations, WCAG 2.2 accessibility, forms integration, and event handling in Vue applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Layout"
---

# Syncfusion Vue Popups Component

## Implementing Syncfusion Vue Dialog Component

The DialogComponent displays content in a floating window with support for modal and modeless modes, custom positioning, dragging, resizing, animations, templating, and comprehensive accessibility features.

### Component Overview

**DialogComponent Features:**
- **Modal/Modeless modes**: Control parent interaction blocking
- **9 preset positions + custom X/Y**: Flexible placement
- **Dragging**: Header-based drag and drop (allowDragging)
- **Resizing**: Diagonal resize grip (enableResize)
- **Templating**: Custom header, content, footer
- **Animations**: 16 effects (Fade, Zoom, Flip, Slide, FadeZoom, etc.)
- **Buttons**: Built-in action buttons with click handlers
- **Events**: open, close, beforeOpen, beforeClose, drag, dragStart, dragStop, resize events
- **Keyboard Navigation**: Tab, Escape (closeOnEscape), Enter
- **WCAG 2.2 Accessibility**: ARIA roles, focus management
- **Localization**: 20+ locales via locale property
- **RTL Support**: Right-to-left rendering

### Documentation & Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/dialog-getting-started.md)
- Installation (`@syncfusion/ej2-vue-popups`)
- CSS/theme imports (material, bootstrap, tailwind)
- Basic DialogComponent template structure
- Using refs (template refs) to control dialogs
- Composition API patterns with reactive state
- Initial visibility with visible prop

#### Modal vs Modeless
📄 **Read:** [references/modal-vs-modeless.md](references/dialog-modal-vs-modeless.md)
- isModal boolean property (true/false)
- Modal overlay behavior and parent blocking
- Modeless floating behavior
- Focus management differences
- When to choose each mode
- Side-by-side comparisons

#### Positioning and Dragging
📄 **Read:** [references/positioning-and-dragging.md](references/dialog-positioning-and-dragging.md)
- position object (X: 'center'|'left'|'right'|number, Y: 'top'|'center'|'bottom'|number)
- 9 preset position combinations
- Custom pixel-based positioning
- allowDragging boolean property
- enableResize and resizeHandles configuration
- Target element constraints with target prop

#### Templates and Content
📄 **Read:** [references/templates-and-content.md](references/dialog-templates-and-content.md)
- content property (string, HTML, template)
- header property (text or template)
- footerTemplate (custom footer template)
- Dynamic content updates with computed
- HTML sanitization (enableHtmlSanitizer)
- Styling content and edge cases

#### Buttons and Actions
📄 **Read:** [references/buttons-and-actions.md](references/dialog-buttons-and-actions.md)
- buttons array with ButtonPropsModel[]
- ButtonPropsModel structure (buttonModel, click, isFlat, type)
- buttonModel properties (content, isPrimary, cssClass)
- Click event handlers with methods
- Styling buttons with cssClass
- Button types (Button, Submit, Reset)

#### Animation Effects
📄 **Read:** [references/animation-effects.md](references/dialog-animation-effects.md)
- AnimationSettingsModel (effect, duration, delay)
- 16 animation effects (Fade, FadeZoom, FlipLeftDown, FlipLeftUp, etc.)
- Duration in milliseconds
- Delay before animation starts
- Disable animations (effect: 'None')
- Performance considerations

#### Localization and Accessibility
📄 **Read:** [references/localization-and-accessibility.md](references/dialog-localization-and-accessibility.md)
- locale property for culture/language
- WCAG 2.2 compliance
- Keyboard navigation (Tab, Enter, Escape)
- closeOnEscape behavior control
- ARIA roles and attributes
- Screen reader support
- RTL support with enableRtl
- Focus management patterns

#### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/dialog-advanced-patterns.md)
- Events: open, close, beforeOpen, beforeClose, drag, dragStart, dragStop, resizeStart, resizeStop, resizing
- Nested and stacked dialogs
- Forms with validation
- AJAX content loading
- Prevent close logic (beforeClose event)
- Full-screen dialogs
- HTML sanitization and security
- CSS classes and z-index management
- Enable persistence (enablePersistence)
- Common edge cases and troubleshooting

#### API Reference (Complete)
📄 **Read:** [references/api-reference.md](references/dialog-api-reference.md)
- All 24 DialogModel properties with types and defaults
- All 11 events with event arguments
- Methods: show(), hide(), refresh(), destroy()
- ButtonPropsModel structure (buttonModel, click, isFlat, type)
- AnimationSettingsModel with all 16 effects
- Types and enumerations
- Quick reference patterns

### Quick Start Example

> **⚠️ Dependency Alignment:** All `@syncfusion/ej2-*` packages must be on the **same major version** to avoid peer-dependency conflicts and supply-chain mismatches. Install them together:
> ```
> npm install @syncfusion/ej2-vue-popups @syncfusion/ej2-base @syncfusion/ej2-buttons
> ```

**Basic Dialog:**

```vue
<template>
  <div id="target">
    <ejs-dialog
      target='#target'
      content="This is dialog content"
      width="300px"
    >
    </ejs-dialog>
  </div>
</template>

<script>
import { DialogComponent } from '@syncfusion/ej2-vue-popups';

export default {
  name: "App",
  components: {
    'ejs-dialog': DialogComponent
  }
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/dialog/index.css";

#target {
    height: 100%;
    min-height: 200px;
}
</style>
```

### Common Patterns

#### Pattern 1: Confirmation Dialog
Delete action with confirmation buttons:
```vue
<script setup>
const buttons = [
  {
    buttonModel: { content: 'Delete', cssClass: 'e-flat e-danger', isPrimary: true },
    click: () => { performDelete(); dialogRef.value?.hide?.(); }
  },
  {
    buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
    click: () => dialogRef.value?.hide?.()
  }
];
</script>
```

#### Pattern 2: Form Dialog
Dialog with form inputs and validation:
```vue
<DialogComponent header="Edit Profile" :buttons="buttons" :isModal="true" width="500px">
  <div style="padding: 16px">
    <input type="text" placeholder="Name" class="form-control" />
    <input type="email" placeholder="Email" class="form-control" />
    <textarea placeholder="Bio" class="form-control"></textarea>
  </div>
</DialogComponent>
```

#### Pattern 3: Centered Dialog
Position dialog in center of screen:
```vue
<DialogComponent
  header="Alert"
  :position="{ X: 'center', Y: 'center' }"
  :isModal="true"
  showCloseIcon
  width="350px"
>
  This dialog is centered on the screen.
</DialogComponent>
```

#### Pattern 4: Draggable Floating Panel
Non-modal, draggable properties panel:
```vue
<DialogComponent
  header="Properties"
  :isModal="false"
  :allowDragging="true"
  :position="{ X: 200, Y: 150 }"
  width="300px"
  :enableResize="true"
  :resizeHandles="['All']"
  showCloseIcon
>
  Drag me around! I don't block the page.
</DialogComponent>
```

#### Pattern 5: Animated Dialog
Dialog with Zoom animation:
```vue
<DialogComponent
  header="Welcome"
  :animationSettings="{ effect: 'Zoom', duration: 400, delay: 0 }"
  :isModal="true"
  :position="{ X: 'center', Y: 'center' }"
  width="400px"
>
  This dialog zooms in smoothly!
</DialogComponent>
```

#### Pattern 6: Custom Footer Template
Custom footer instead of buttons:
```vue
<DialogComponent
  header="Custom Footer"
  :isModal="true"
>
  <template #footer>
    <div style="padding: 12px; text-align: right">
      <button class="e-control e-btn e-primary" style="margin-right: 8px">
        Save
      </button>
      <button class="e-control e-btn">Cancel</button>
    </div>
  </template>
  Dialog content with custom footer.
</DialogComponent>
```

#### Pattern 7: Nested Dialogs
Parent dialog containing child dialog:
```vue
<DialogComponent header="Parent" :isModal="true" width="400px">
  <button @click="showChild" class="e-control e-btn">
    Open Child Dialog
  </button>
  
  <DialogComponent
    ref="childDialogRef"
    header="Child"
    :isModal="true"
    width="300px"
    :visible="false"
  >
    Nested dialog content
  </DialogComponent>
</DialogComponent>
```

### Key Props (DialogModel)

| Prop | Type | Description | Default | When to Use |
|------|------|-------------|---------|------------|
| `isModal` | boolean | Enable modal mode (blocks parent interaction) | false | Confirmations, alerts, critical actions |
| `visible` | boolean | Initial visibility state | false | Control initial dialog display |
| `header` | string | Dialog header/title | - | Every dialog needs a title |
| `content` | string \| HTML | Dialog body content | - | Main dialog information |
| `buttons` | ButtonPropsModel[] | Action buttons in footer | - | For OK/Cancel, action confirmations |
| `footerTemplate` | Template | Custom footer content | - | When buttons prop doesn't fit |
| `showCloseIcon` | boolean | Show close button in header | false | Allow users to dismiss |
| `position` | PositionData | X/Y positioning (center, top, etc.) | { X: 'center', Y: 'center' } | Custom placement |
| `allowDragging` | boolean | Enable drag functionality | false | Movable dialogs, floating panels |
| `enableResize` | boolean | Enable resize with grip | false | Resizable dialogs |
| `resizeHandles` | ResizeDirections[] | Which edges/corners resize | ['All'] | Control resize behavior |
| `width` | string \| number | Dialog width | '330px' | Control dialog size |
| `height` | string \| number | Dialog height | 'auto' | Control dialog size |
| `minHeight` | string \| number | Minimum height | - | Prevent too-small resize |
| `animationSettings` | AnimationSettingsModel | Animation effect/duration/delay | - | Smooth open/close transitions |
| `closeOnEscape` | boolean | Close on Escape key press | true | Keyboard navigation |
| `target` | string (selector) | Container element | document.body | Modal positioning |
| `enableHtmlSanitizer` | boolean | Sanitize HTML content | true | Security (prevent XSS) |
| `cssClass` | string | Custom CSS classes | - | Styling and theming |
| `enableRtl` | boolean | Right-to-left rendering | false | RTL languages |
| `locale` | string | Culture/language code | 'en-US' | Localization |
| `zIndex` | number | Stack order | - | Manage overlapping dialogs |
| `enablePersistence` | boolean | Persist state on reload | false | Remember size/position |

### Common Use Cases

1. **Confirmation Dialogs** - Confirm delete, submit, or critical actions before proceeding
2. **Alert/Info Popups** - Display system messages, warnings, or notifications
3. **Form Dialogs** - Edit profiles, settings, or create new records in modal forms
4. **Input Prompts** - Collect user input for specific actions (e.g., "Enter file name")
5. **Properties Panels** - Draggable, non-modal panels for settings or properties
6. **Multi-Step Workflows** - Nested dialogs for step-by-step processes
7. **Loading/Processing** - Show progress indicators or loading states
8. **Help/Documentation** - Contextual help, tips, or tutorial overlays
9. **Image Galleries** - Lightbox dialogs for images or media previews
10. **Settings/Preferences** - Organize application settings in tabbed dialogs

---

**Next:** Choose a reference based on what you need to implement. All references include working code examples, best practices, and troubleshooting guidance.

## Implementing Syncfusion Vue Predefined Dialog Component

### Table of Contents
- [Key Concept](#key-concept)
- [Quick Start](#quick-start)
- [Documentation Guide](#documentation-guide)
- [Common Patterns](#common-patterns)

### Key Concept

Syncfusion Predefined Dialogs in Vue are opened
imperatively via the **`DialogUtility`** utility class:

| Dialog Type | Method |
|---|---|
| Alert | `DialogUtility.alert({ ... })` |
| Confirm | `DialogUtility.confirm({ ... })` |
| Prompt (input) | `DialogUtility.confirm({ content: '<input .../>', ... })` |

**Import:** `import { DialogUtility } from '@syncfusion/ej2-vue-popups';`

---

### Quick Start

```vue
<template>
  <div id="app">
    <button class="e-btn" @click="showAlert">Show Alert</button>
  </div>
</template>

<script>
import { DialogUtility } from '@syncfusion/ej2-vue-popups';

export default {
  name: "App",
  methods: {
    showAlert: function() {
      DialogUtility.alert({
        title: 'Low Battery',
        width: '250px',
        content: '10% of battery remaining'
      });
    }
  }
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/dialog/index.css";
</style>
```

---

### Documentation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/predefineddialog-getting-started.md)
- Installation (`@syncfusion/ej2-vue-popups`)
- CSS imports
- Alert, Confirm, and Prompt minimal examples
- Setup with app.mount()

#### Animation
📄 **Read:** [references/animation.md](references/predefineddialog-animation.md)
- `animationSettings` property with `effect`, `duration`, `delay`
- Alert / Confirm / Prompt animation examples

#### Draggable
📄 **Read:** [references/draggable.md](references/predefineddialog-draggable.md)
- `isDraggable` boolean property
- Alert / Confirm / Prompt drag examples

#### Position
📄 **Read:** [references/position.md](references/predefineddialog-position.md)
- `position` property: `{ X, Y }` — `left|center|right` / `top|center|bottom` or numeric offset
- Alert / Confirm / Prompt position examples

#### Dimension
📄 **Read:** [references/dimension.md](references/predefineddialog-dimension.md)
- `width` and `height` properties
- `cssClass` for max-width / min-width constraints
- Alert / Confirm / Prompt dimension examples

#### Customization
📄 **Read:** [references/customization.md](references/predefineddialog-customization.md)
- `okButton` / `cancelButton` — custom `text`, `icon`, `click` handler
- `showCloseIcon` and `closeOnEscape`
- Custom `content` for prompt dialogs

#### API Reference
📄 **Read:** [references/api.md](references/predefineddialog-api.md)
- Full `DialogUtility.alert()` / `confirm()` option properties
- All supported fields: `title`, `content`, `width`, `height`, `position`, `animationSettings`, `isDraggable`, `okButton`, `cancelButton`, `showCloseIcon`, `closeOnEscape`, `cssClass`

---

### Common Patterns

**Alert with OK callback:**
```vue
<script setup>
const dialogObj = DialogUtility.alert({
  title: 'Info',
  content: 'Operation complete.',
  okButton: { click: () => { dialogObj.hide(); } }
});
</script>
```

**Confirm with Yes / No:**
```vue
<script setup>
const dialogObj = DialogUtility.confirm({
  title: 'Delete?',
  content: 'Are you sure?',
  width: '300px',
  okButton: { text: 'Yes', click: () => { dialogObj.hide(); /* do delete */ } },
  cancelButton: { text: 'No', click: () => { dialogObj.hide(); } }
});
</script>
```

**Prompt (input capture):**
```vue
<script setup>
const dialogObj = DialogUtility.confirm({
  title: 'Enter Name',
  content: '<p>Your name:</p><input id="nameInput" class="e-input" placeholder="Type here..." />',
  width: '300px',
  okButton: {
    text: 'Submit',
    click: () => {
      const val = (document.getElementById('nameInput') as HTMLInputElement).value;
      dialogObj.hide();
    }
  },
  cancelButton: { click: () => dialogObj.hide() }
});
</script>
```

## Implementing Syncfusion Vue Tooltip

A comprehensive skill for implementing the Syncfusion Vue `TooltipComponent` — covering setup, content strategies, positioning, open modes, animation, customization, accessibility, and advanced how-to patterns.

**Package:** `@syncfusion/ej2-vue-popups`  
**Import:** `import { TooltipComponent } from '@syncfusion/ej2-vue-popups';`

## Quick Start

```bash
npm install @syncfusion/ej2-vue-popups --save
npm install @syncfusion/ej2-material3-theme --save
```

```vue
<template>
  <div id="app">
    <div id="container">
      <ejs-tooltip content="Tooltip content" target="#target">
        <button id="target">Show Tooltip</button>
      </ejs-tooltip>
    </div>
  </div>
</template>

<script>
import { TooltipComponent } from "@syncfusion/ej2-vue-popups";

export default {
  name: "App",
  components: {
    "ejs-tooltip": TooltipComponent
  }
};
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/tooltip/index.css";
</style>
```

## Navigation Guide

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/tooltip-getting-started.md)
- Installation and CSS imports
- Basic tooltip on a single element
- Tooltip on multiple targets within a container (`target` prop)
- Using `title` attribute as fallback content
- Running the application

### Content
📄 **Read:** [references/content.md](references/tooltip-content.md)
- Plain string content
- Template content (slot)
- Dynamic content loaded via Fetch/Ajax (`beforeRender` event)
- HTML content (iframe, embedded elements)
- Updating content programmatically with ref

### Positioning
📄 **Read:** [references/position.md](references/tooltip-position.md)
- 12 static positions (`TopLeft`, `TopCenter`, `TopRight`, `BottomLeft`, `BottomCenter`, `BottomRight`, `LeftTop`, `LeftCenter`, `LeftBottom`, `RightTop`, `RightCenter`, `RightBottom`)
- Tip pointer show/hide (`showTipPointer`) and positioning (`tipPointerPosition`: Auto, Start, Middle, End)
- Dynamic positioning with `refresh()` method (draggable targets)
- Mouse trailing (`mouseTrail`)
- Offset values (`offsetX`, `offsetY`)
- Collision handling (auto-flip behavior, `windowCollision`)

### Open Modes
📄 **Read:** [references/open-mode.md](references/tooltip-open-mode.md)
- `Auto`, `Hover`, `Click`, `Focus`, `Custom` modes via `opensOn`
- Combining multiple modes (`opensOn="Hover Click"`)
- Sticky mode (`isSticky`) — close button appears
- Open/close delay (`openDelay`, `closeDelay`)
- Custom open mode with `open()` and `close()` methods
- Mobile behavior (tap-and-hold)

### Animation
📄 **Read:** [references/animation.md](references/tooltip-animation.md)
- `animation` property (open/close `AnimationModel`)
- All 15 available animation effects (FadeIn, ZoomIn, FlipX/Y, etc.)
- Custom duration and delay
- Animating via `open()` and `close()` methods programmatically
- Transition effect using `beforeRender` + CSS transitions

### Customization
📄 **Read:** [references/customization.md](references/tooltip-customization.md)
- `cssClass` for custom themes and styles
- Tip pointer size, background, and border customization
- Full tooltip appearance (background, opacity, font)
- Curved tip and bubble tip arrow patterns
- Dimension control (`width`, `height`) and scroll mode
- RTL support (`enableRtl`)

### How-To Patterns
📄 **Read:** [references/how-to.md](references/tooltip-how-to.md)
- Tooltip on multiple targets (dynamic content per target)
- Tooltip on disabled elements
- Enabling/disabling tooltip with `destroy()` and `render()`
- Displaying tooltip on SVG and Canvas elements
- Embedding iframes or HTML elements in tooltip content
- Custom open modes (double-click, right-click)

### Accessibility
📄 **Read:** [references/accessibility.md](references/tooltip-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes (`role="tooltip"`, `aria-describedby`, `aria-hidden`)
- Keyboard shortcuts (Escape, Tab)
- Screen reader behavior

### API Reference
📄 **Read:** [references/api.md](references/tooltip-api.md)
- All properties, methods, and events with types and defaults
- `TooltipAnimationSettings`, `TooltipEventArgs` types
- `Position` and `TipPointerPosition` enum values

## Common Patterns

### Tooltip on a Button
```vue
<TooltipComponent content="Submit the form" position="TopCenter">
  <button class="e-btn e-primary">Submit</button>
</TooltipComponent>
```

### Multi-Target Tooltip in a Container
```vue
<!-- Single TooltipComponent handles all .e-info targets; 
     each uses its own `title` attribute as content -->
<TooltipComponent target=".e-info" position="RightCenter">
  <form>
    <input class="e-info" type="text" title="Enter your name" />
    <input class="e-info" type="email" title="Enter a valid email" />
  </form>
</TooltipComponent>
```

### Click-Triggered Sticky Tooltip
```vue
<TooltipComponent
  content="Click the × to close me"
  opensOn="Click"
  :isSticky="true"
  position="BottomCenter"
>
  <button class="e-btn">Click Me</button>
</TooltipComponent>
```

### Programmatic Open/Close
```vue
<template>
  <TooltipComponent
    ref="tooltipRef"
    content="Tooltip opened programmatically"
    opensOn="Custom"
  >
    <button
      ref="target"
      class="e-btn"
      @click="toggleTooltip"
    >
      Toggle Tooltip
    </button>
  </TooltipComponent>
</template>

<script setup>
import { ref } from 'vue';
import { TooltipComponent } from '@syncfusion/ej2-vue-popups';

const tooltipRef = ref(null);
const target = ref(null);

const toggleTooltip = () => {
  if (target.value?.getAttribute('data-tooltip-id')) {
    tooltipRef.value?.close?.();
  } else {
    tooltipRef.value?.open?.(target.value);
  }
};
</script>
```

### Mouse-Trailing Tooltip
```vue
<TooltipComponent
  content="Following your mouse!"
  :mouseTrail="true"
  :showTipPointer="false"
>
  <div style="width: 200px; height: 100px; background: #eee">
    Hover over me
  </div>
</TooltipComponent>
```

## Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `content` | `string \| HTMLElement \| Function` | — | Tooltip text, HTML, or template |
| `target` | `string` | — | CSS selector for multi-target mode |
| `position` | `Position` | `'TopCenter'` | 12 placement values |
| `opensOn` | `string` | `'Auto'` | Hover / Click / Focus / Custom |
| `isSticky` | `boolean` | `false` | Keep visible until user closes |
| `mouseTrail` | `boolean` | `false` | Follow mouse cursor |
| `showTipPointer` | `boolean` | `true` | Show/hide arrow tip |
| `tipPointerPosition` | `TipPointerPosition` | `'Auto'` | Auto / Start / Middle / End |
| `openDelay` | `number` | `0` | ms delay before opening |
| `closeDelay` | `number` | `0` | ms delay before closing |
| `offsetX` / `offsetY` | `number` | `0` | Distance from target (px) |
| `width` / `height` | `string \| number` | `'auto'` | Tooltip dimensions |
| `cssClass` | `string` | `null` | Custom CSS class |
| `animation` | `AnimationModel` | FadeIn/FadeOut 150ms | Open/close animation |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enableHtmlSanitizer` | `boolean` | `true` | Sanitize HTML content |
| `container` | `string \| HTMLElement` | `body` | Popup append target |
| `windowCollision` | `boolean` | `false` | Collision vs viewport |
