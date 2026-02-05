---
name: vue-components
description: Apply when creating or modifying Vue components, using BaseCard, ColorPicker, Toast, or composables. Covers component architecture, module structure, and Vue 3 Composition API patterns.
---

# Vue 3 Component Architecture

## Project Structure

```
src/
├── components/
│   ├── common/           # Shared components (BaseCard, ColorPicker, Toast)
│   └── [module-name]/    # Feature modules (cards + admin components)
├── composables/          # Reusable Vue composition functions
├── services/            # API services and utilities
└── types/              # TypeScript definitions
```

## BaseCard Pattern

All dashboard cards extend BaseCard for consistency:

```vue
<template>
  <BaseCard
    title="Your Card Title"
    :loading="loading"
    :error="error"
  >
    <!-- Your content here -->
  </BaseCard>
</template>

<script setup lang="ts">
import BaseCard from '../common/BaseCard.vue'
import { ref } from 'vue'

const loading = ref(false)
const error = ref<string | null>(null)
</script>
```

## Available Components

- **BaseCard**: Base component for dashboard cards with consistent styling
- **ColorPicker**: ChurchTools-compatible color picker with 4-column grid, round swatches, v-model support
- **Toast**: Notification system with 4 types (success, error, warning, info), auto-dismiss, smooth animations

## Available Composables

- `useToast`: Toast notification management
- `useTableSearch`: Table search functionality
- `useTableSorting`: Table sorting with custom comparators
- `useTableResize`: Responsive table handling

## Component Usage Example

```vue
<template>
  <BaseCard title="My Extension" :loading="loading" :error="error">
    <p>Extension content here</p>
    <ColorPicker v-model="selectedColor" />
    <button @click="showSuccess" type="button">Show Toast</button>
  </BaseCard>
  <Toast />
</template>

<script setup lang="ts">
import BaseCard from './components/common/BaseCard.vue'
import ColorPicker from './components/common/ColorPicker.vue'
import Toast from './components/common/Toast.vue'
import { useToast } from './composables/useToast'

const { showToast } = useToast()
const showSuccess = () => showToast('Success!', 'Operation completed', 'success')
</script>
```

## Module Structure

Each feature module has:
- `[ModuleName]Card.vue` - Dashboard card component
- `[ModuleName]Admin.vue` - Admin/CRUD component

## Code Style

- Use Vue 3 Composition API with `<script setup>`
- Use TypeScript strictly
- Import BaseCard from `../common/BaseCard.vue` (relative paths)
- Always use `type="button"` on buttons to prevent form submission
