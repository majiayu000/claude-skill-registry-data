---
name: vue-js-expert
description: Expert Vue.js 3 development assistance using Composition API, TypeScript, component architecture, state management with Pinia, reactivity patterns, and performance optimization. Use when building Vue 3 components, debugging reactivity issues, implementing composables, or architecting Vue applications.
metadata:
  category: "frontend"
  version: "1.0.0"
  framework: "vue3"
license: "MIT"
---

# Vue.js 3 Expert

## Overview

Expert guidance for Vue.js 3 development with deep expertise in the Composition API, TypeScript integration, component architecture, and modern Vue ecosystem tools. This skill provides best practices, patterns, and solutions for building scalable, maintainable Vue 3 applications.

## When to Use

Invoke this skill when you need help with:
- Building Vue 3 components using Composition API and `<script setup>`
- Debugging reactivity issues (ref, reactive, computed, watch)
- Architecting component hierarchies and data flow patterns
- Implementing composables and reusable logic
- State management with Pinia
- Vue Router integration with guards and dynamic imports
- Performance optimization (lazy loading, bundle optimization, shallow refs)
- TypeScript integration and type safety
- Testing Vue components with @testing-library/vue when possible
- Troubleshooting lifecycle problems and performance bottlenecks

## Core Development Standards

### Vue 3 Composition API (Required)

Always use Vue 3 Composition API and `<script setup>` syntax exclusively. Avoid Options API unless specifically requested.

**SFC Structure Order:**
```vue
<script setup lang="ts">
// Script content
</script>

<template>
  <!-- Template content -->
</template>

<style scoped>
/* Styles */
</style>
```

### Reactivity Patterns

**Prefer `ref` over `reactive`:**
- Use `ref` for scalar values and when you need fine-grained reactivity
- Use `shallowRef` for large or deeply nested data to avoid unnecessary deep observation
- For deep reactivity, use explicitly named `deepRef` instead of `ref` for clarity
- Import all Vue APIs directly from `"vue"`

**Example:**
```typescript
import { ref, shallowRef, computed } from 'vue'

// Scalar values
const count = ref(0)
const message = ref('')

// Large data structures
const largeDataset = shallowRef([/* thousands of items */])

// Computed values
const doubled = computed(() => count.value * 2)
```

### Component Props and Events

**Use `defineModel` for v-model bindings:**

Always use `defineModel<type>({ required, get, set, default })` to define allowed v-model bindings. This avoids manually defining `modelValue` prop and `update:modelValue` event.

**Example:**
```typescript
// Component with v-model
const modelValue = defineModel<string>({ required: true })

// Component with multiple v-models
const isOpen = defineModel<boolean>('open', { default: false })
const selectedId = defineModel<number>('selected')
```

### TypeScript Integration

Include proper TypeScript types and interfaces:

```typescript
interface User {
  id: number
  name: string
  email: string
}

interface Props {
  users: User[]
  pageSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  pageSize: 10
})
```

### Exports and Imports

**Always prefer named exports over default exports:**

```typescript
// Good - Named exports
export function useCounter() { /* ... */ }
export const UserCard = defineComponent({ /* ... */ })

// Avoid - Default exports
export default defineComponent({ /* ... */ })
```

### Code Comments

**Only add meaningful comments that explain WHY, not WHAT:**

```typescript
// Good - Explains why
// We use shallowRef here because the dataset contains 10k+ items
// and we only need to trigger updates when the array reference changes
const dataset = shallowRef(data)

// Avoid - Explains what (obvious from code)
// Create a ref for count
const count = ref(0)
```

## Component Architecture

### File Organization

Keep tests alongside the file they test:
```
src/
  components/
    ui/
      data-table.vue
      data-table.spec.ts
  composables/
    useAuth.ts
    useAuth.spec.ts
```

### Composables Pattern

Extract reusable logic into composables:

```typescript
// composables/useCounter.ts
export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initialValue

  return {
    count: readonly(count),
    increment,
    decrement,
    reset
  }
}
```

### Component Breakdown

For complex requirements:
1. Break down implementation into logical components and composables
2. Provide file structure recommendations
3. Include error handling and edge case considerations
4. Suggest testing strategies for the implemented features

## State Management

Use Pinia for state management appropriate to application scale:

```typescript
// stores/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => user.value !== null)

  async function login(credentials: Credentials) {
    // Implementation
  }

  return { user, isAuthenticated, login }
})
```

## Performance Optimization

- Use `shallowRef` for large data volumes to avoid deep reactivity overhead
- Implement lazy loading with dynamic imports: `() => import('./HeavyComponent.vue')`
- Optimize bundle size with proper code splitting
- Use `v-once` for static content that never changes
- Use `v-memo` for expensive list rendering

## Testing Standards

Write comprehensive tests using Testing Library for user-centric testing:

```typescript
import { render, screen } from '@testing-library/vue'
import { describe, it, expect } from 'vitest'
import userEvent from '@testing-library/user-event'
import MyComponent from './MyComponent.vue'

describe('MyComponent', () => {
  it('renders message to user', () => {
    render(MyComponent, {
      props: { message: 'Hello' }
    })
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const user = userEvent.setup()
    render(MyComponent)

    const button = screen.getByRole('button', { name: /click me/i })
    await user.click(button)

    expect(screen.getByText(/clicked/i)).toBeInTheDocument()
  })
})
```

## Bundled Resources

**references/** - Documentation loaded into context when needed
- `vueuse-guidelines.md` - VueUse development guidelines and best practices for Vue composables
- `vue-patterns.md` - Common Vue 3 patterns and anti-patterns

## Research & Documentation Strategy

When you need to reference documentation:

1. **First**: Try accessing the `llms.txt` file for quick reference
   - Example: `https://vuejs.org/llms.txt`

2. **Preferred**: Use Context7 MCP to get the latest documentation
   - For Vue.js core: `/vuejs/core`
   - For Pinia: `/vuejs/pinia`
   - For Vue Router: `/vuejs/router`

3. **Fallback**: Use WebFetch to get docs from official sources
   - Vue.js: https://vuejs.org/guide/
   - Pinia: https://pinia.vuejs.org/
   - Vue Router: https://router.vuejs.org/

4. **VueUse Patterns**: Reference `references/vueuse-guidelines.md` for composable best practices

**NEVER** hallucinate or guess URLs. Always verify examples and patterns from documentation before using.

## Examples

### Building a Reusable Component

```
User: "I need to create a reusable data table component with sorting and filtering capabilities"

Claude: I'll help you design and implement a Vue 3 data table component with proper Composition API patterns and TypeScript support.

[Provides implementation with:
- Proper TypeScript interfaces for props
- defineModel for v-model bindings
- Composables for sorting/filtering logic
- Performance optimizations with shallowRef
- Test examples]
```

### Debugging Reactivity Issues

```
User: "My computed property isn't updating when the reactive data changes"

Claude: Let me help diagnose this Vue 3 reactivity issue. Common causes include:
1. Using reactive() with destructuring
2. Accessing .value incorrectly
3. Mutating ref without .value

[Analyzes code and provides solution with explanation]
```

### Implementing Composables

```
User: "How do I create a composable for form validation?"

Claude: I'll create a reusable form validation composable following VueUse patterns.

[Provides implementation following:
- ref over reactive preference
- Proper TypeScript types
- Configurable options object
- Cleanup with tryOnScopeDispose]
```

## Progressive Disclosure

This skill is designed with three levels of information loading:

1. **Metadata** (~200 words) - Always in context (this frontmatter)
2. **SKILL.md** - Loaded when skill is triggered (this file)
3. **Bundled Resources** - Loaded as needed:
   - Load `references/vueuse-guidelines.md` when discussing composable patterns or VueUse
   - Load `references/vue-patterns.md` when discussing common patterns or anti-patterns

Keep core guidance concise. Reference bundled resources for detailed patterns and edge cases.
