---
name: syncfusion-vue-common
description: Common utilities and features for Syncfusion Vue components. Use this skill when the user needs to implement animations, drag-and-drop, state persistence, RTL support, localization, globalization, security, templates, and advanced features for Syncfusion Vue components.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Common Features"
---

# Common Features in Syncfusion Vue Components

Syncfusion Vue components include comprehensive common utilities and features that enhance user experience, ensure cross-cultural support, and provide foundational capabilities across all components. This skill covers installation setup, animations, globalization, state management, and security considerations for building robust Vue applications.

## Table of Contents

- [Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Features](#common-features)

---

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Vue 3 setup (Composition API, Options API)
- Vue 2 setup (Vue CLI, SCSS configuration)
- Nuxt 3 integration and configuration
- Quasar framework setup
- Vitest testing configuration

---

### Globalization

📄 **Read:** [references/globalization.md](references/globalization.md)
- Right-to-left (RTL) support for Arabic, Hebrew, Persian languages
- Localization (l10n) for multi-language support
- Internationalization (i18n) with CLDR data
- Number and currency formatting
- Date and time formatting

---

### Advanced Features & Utilities

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation effects (FadeIn, ZoomOut, SlideUp, etc.)
- Animation timing (duration, delay, global settings)
- Drag-and-drop interactions (Draggable, Droppable)
- Template customization
- State persistence with enablePersistence
- Security best practices and HTML sanitization

---

## Quick Start

### Install Syncfusion Vue component package and theme package

```bash
# Install a Syncfusion component package
npm install @syncfusion/ej2-vue-calendars@latest @syncfusion/ej2-material-theme@latest --save

# Install multiple packages
npm install @syncfusion/ej2-vue-grids@latest @syncfusion/ej2-vue-charts@latest @syncfusion/ej2-material-theme@latest --save
```

> **Note:** The `@syncfusion/ej2-base` package is a dependency for all Syncfusion components and will be automatically installed when you install any Syncfusion Vue package. You don't need to explicitly add it to your `package.json` file.

### Register License Key

**Step 1:** Set the environment variable:

```bash
# Windows
setx SYNCFUSION_LICENSE "Your_License_Key_Here"

# Mac/Linux
export SYNCFUSION_LICENSE='Your_License_Key_Here'
```

**Step 2:** Activate the license using NPX command:

```bash
npx syncfusion-license activate
```

> **Note:** For alternative license registration methods, kindly refer to the [Syncfusion license key registration documentation](https://ej2.syncfusion.com/vue/documentation/licensing/license-key-registration).

### Basic Component Setup

```vue
<template>
  <div class="app-container">
    <ejs-grid :dataSource="data" :allowPaging="true">
      <e-columns>
        <e-column field='OrderID' width='100'></e-column>
        <e-column field='CustomerID' width='100'></e-column>
        <e-column field='Freight' width='100' format='C2'></e-column>
      </e-columns>
    </ejs-grid>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { GridComponent as EjsGrid, ColumnsDirective as EColumns, ColumnDirective as EColumn, Page } from '@syncfusion/ej2-vue-grids';

const data = ref([
  { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
  { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 }
]);

// Provide services
provide('grid', [Page]);
</script>

<style>
/* Import theme CSS */
@import "../node_modules/@syncfusion/ej2-material-theme/styles/grid/index.css";
</style>
```

---

## Common Features

### Enable State Persistence

```vue
<template>
  <ejs-grid id="persistGrid" :dataSource="data" :enablePersistence="true"></ejs-grid>
</template>

<script>
import { GridComponent } from '@syncfusion/ej2-vue-grids';

export default {
  components: { 'ejs-grid': GridComponent },
  data() {
    return {
      data: [{ OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 }]
    };
  }
};
</script>
```

### Enable RTL Support

```vue
<template>
  <ejs-grid :dataSource="data" :enableRtl="true"></ejs-grid>
</template>

<script>
import { GridComponent } from '@syncfusion/ej2-vue-grids';
import { enableRtl } from '@syncfusion/ej2-base';

export default {
  components: { 'ejs-grid': GridComponent },
  data() {
    return { data: [{ OrderID: 10248 }] };
  },
  mounted() {
    enableRtl(true);
  }
};
</script>
```

### Add Animation Effects

```vue
<template>
  <div>
    <button @click="animateElement">Animate</button>
    <div ref="element">Animated Element</div>
  </div>
</template>

<script>
import { Animation } from '@syncfusion/ej2-base';

export default {
  data() {
    return { animation: null };
  },
  mounted() {
    this.animation = new Animation({ duration: 5000 });
  },
  methods: {
    animateElement() {
      this.animation.animate(this.$refs.element, { name: 'FadeOut' });
    }
  }
};
</script>
```

### Implement Drag-and-Drop

```vue
<template>
  <div>
    <div ref="draggable">Drag me</div>
    <div ref="droppable">Drop here</div>
  </div>
</template>

<script>
import { Draggable, Droppable } from '@syncfusion/ej2-base';

export default {
  mounted() {
    new Draggable(this.$refs.draggable, { clone: false });
    new Droppable(this.$refs.droppable);
  }
};
</script>
```
