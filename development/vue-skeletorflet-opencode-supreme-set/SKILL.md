---
name: vue
description: Vue.js Composition API, SFC structure, reactivity system, directives, router, Pinia state management, slots, and transitions. Use when building Vue components or applications.
---

## vue

Composition API is the standard for Vue 3 apps.

### Core Concepts
- Composition API: setup(), ref for primitives, reactive for objects, computed, watch
- SFC structure: <template>, <script setup>, <style scoped> per component
- Reactivity system: proxy-based tracking, automatic dependency collection

### Common Patterns
- v-if/v-else for conditional rendering, v-for with :key for lists
- v-model for two-way binding on form inputs and custom components
- Named and scoped slots for flexible component composition

### Best Practices
- Use <script setup> over Options API for new code
- Keep components small, one concern per component
- Use computed instead of method calls in template for caching

### Common Code Patterns
- watchEffect for running side effects that auto-track dependencies
- defineProps/defineEmits macro for typed component interfaces
- Scoped slots: pass data up via slot props for render flexibility
