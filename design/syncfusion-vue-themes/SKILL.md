---
name: syncfusion-vue-themes
description: Use this skill when users need to apply themes, customize appearance, switch dark mode, use CSS variables, configure icons, or modify visual styling for Syncfusion Vue components. Covers icon library, size modes, and Theme Studio integration.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Theming and Appearance"
---

# Themes in Syncfusion Vue Components

Syncfusion Vue components provide comprehensive theming support with modern, customizable themes. This skill guides you through applying themes, customizing appearance, implementing dark mode, using CSS variables, managing icons, and creating custom themes for consistent, professional Vue applications.

## Table of Contents

- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Patterns](#common-patterns)

## Documentation and Navigation Guide

### Built-in Themes
📄 **Read:** [references/built-in-themes.md](references/built-in-themes.md)
- Available 10+ themes
- Applying themes via npm packages, CDN, or individual component styles
- Optimized (lite) CSS files for reduced bundle size

### Dark Mode Implementation
📄 **Read:** [references/dark-mode.md](references/dark-mode.md)
- Global dark mode with `e-dark-mode` class
- Per-component dark mode
- Runtime theme switching with checkboxes or toggle buttons

### CSS Variables Customization
📄 **Read:** [references/css-variables.md](references/css-variables.md)
- CSS variable structure for each theme (Material 3, Fluent 2, Bootstrap 5.3, Tailwind 3.4)
- Customizing primary, success, warning, danger, info colors
- Runtime color modification with JavaScript
- Theme-specific variable formats (RGB vs hex values)

### Icon Library
📄 **Read:** [references/icons.md](references/icons.md)
- Setting up the icon library (npm or CDN)
- Using icons with `e-icons` class
- Icon sizing (small, medium, large)
- Customizing icon color and appearance
- Available icon sets per theme

### Size Modes
📄 **Read:** [references/advanced-theming.md](references/advanced-theming.md)
- Normal vs touch (bigger) size modes
- Enabling size modes globally or per-component
- Runtime size mode switching

### Advanced Features
📄 **Read:** [references/advanced-theming.md](references/advanced-theming.md)
- Styled-components integration
- Font customization across all components
- Theme Studio for custom theme creation

### Migrating Styles from Component Packages to Theme Packages
📄 **Read:** [references/migration-styles.md](references/migration-styles.md)
- Migrate from component packages to theme packages
- SCSS & CSS Reference migration to theme packages
- Automatic dependency inclusion via index files

## Quick Start

### Install and Apply a Theme

**Step 1: Install Syncfusion Vue Package and theme package**

```bash
npm install @syncfusion/ej2-vue-buttons @syncfusion/ej2-tailwind3-theme@latest --save
```

**Step 2: Import Theme CSS**

**Option 1: Import from npm (Recommended)**

```css
/* src/App.vue - <style> section */
@import "../node_modules/@syncfusion/ej2-tailwind3-theme/styles/button/index.css";
```

**Option 2: Use CDN**

> **⚠️ Important:** The CDN version MUST match your installed npm package version to avoid style and rendering issues.

To find your installed version:

```bash
npm list @syncfusion/ej2-vue-buttons
```

Then use the matching CDN version:

```html
<!-- index.html -->
<!-- Replace {VERSION} with your installed package version (e.g., 28.1.33, 33.1.44) -->
<link href="https://cdn.syncfusion.com/ej2/{VERSION}/tailwind3.css" rel="stylesheet"/>

<!-- Example: If your package version is 33.1.44 -->
<link href="https://cdn.syncfusion.com/ej2/33.1.44/tailwind3.css" rel="stylesheet"/>
```

> **Note:** Using npm imports (Option 1) is recommended as it automatically keeps CSS and JavaScript versions in sync.

## Common Patterns

### Pattern 1: Apply Dark Mode Globally

```vue
<template>
  <div>
    <ejs-checkbox 
      label="Enable Dark Mode" 
      :checked="isDarkMode" 
      @change="handleDarkModeToggle"
    />
    <ejs-button cssClass="e-primary">Sample Button</ejs-button>
  </div>
</template>

<script>
import { CheckBoxComponent } from '@syncfusion/ej2-vue-buttons';
import { ButtonComponent } from '@syncfusion/ej2-vue-buttons';

export default {
  components: {
    'ejs-checkbox': CheckBoxComponent,
    'ejs-button': ButtonComponent
  },
  data() {
    return {
      isDarkMode: false
    };
  },
  methods: {
    handleDarkModeToggle(event) {
      this.isDarkMode = event.checked ?? false;
      
      if (this.isDarkMode) {
        document.body.classList.add('e-dark-mode');
      } else {
        document.body.classList.remove('e-dark-mode');
      }
    }
  }
};
</script>
```

### Pattern 2: Customize Primary Color with CSS Variables

**For Fluent 2 Theme:**

```vue
<style>
:root {
  --color-sf-primary: #ff6b35;  /* Custom orange */
}
</style>
```

**For Material 3 Theme (uses RGB values):**

```vue
<style>
:root {
  --color-sf-primary: 255, 107, 53;  /* RGB: Custom orange */
}
</style>
```

### Pattern 3: Enable Touch Mode Globally

```html
<!-- index.html -->
<body class="e-bigger">
  <div id="app"></div>
</body>
```

Or per-component:

```vue
<ejs-button cssClass="e-bigger">Touch-Friendly Button</ejs-button>
```

### Pattern 4: Use Optimized CSS for Faster Loading

```css
```vue
<style>
/* Lite version without bigger mode styles */
@import "@syncfusion/ej2-tailwind3-theme/styles/tailwind3-lite.css";
</style>
```

### Pattern 5: Use Icons from Syncfusion Library

**Install icons package:**

You can install either the icons package or the theme package:

```bash
npm install @syncfusion/ej2-icons@latest

/* or */

npm install @syncfusion/ej2-tailwind3-theme@latest
```

**Import icon styles:**

```css
/* Syncfusion theme package icon styles */
<style>
@import "../node_modules/@syncfusion/ej2-tailwind3-theme/styles/icons/tailwind3.css";
</style>

/* or */

/* Syncfusion components package icon styles */
<style>
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
</style>
```

**Use icons in components:**

```vue
<template>
  <span class="e-icons e-cut"></span>
  <span class="e-icons e-medium e-copy"></span>
  <span class="e-icons e-large e-paste"></span>
</template>
```
