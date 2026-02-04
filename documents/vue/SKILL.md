---
name: vue
description: Use when working with Vue.js 3 projects - provides patterns for Composition API, reactivity, components, and best practices from official Vue.js documentation
---

# Vue.js 3

## Overview

Vue.js 3 is a progressive JavaScript framework for building user interfaces. **Core principle:** Use Composition API with `<script setup>`, leverage composables for reusable logic, and follow one-way data flow.

**Official Documentation:** https://vuejs.org

## When to Use

- Building Vue.js 3 applications or components
- Working with reactive state and composables
- Need Vue.js patterns and best practices

**When NOT to use:**
- Vue 2 projects (different API)
- Other frameworks (React, Angular, Svelte)

## Quick Reference

| Pattern | Use Case | Syntax |
|---------|----------|--------|
| `ref()` | Primitives, reassignment | `const count = ref(0)` |
| `reactive()` | Objects only | `const state = reactive({ count: 0 })` |
| `computed()` | Derived state | `const double = computed(() => count.value * 2)` |
| `watch()` | Specific sources | `watch(source, callback)` |
| `watchEffect()` | Auto-track deps | `watchEffect(() => {...})` |
| Composables | Reusable logic | `const { x, y } = useMouse()` |

**For complete API reference:** See @reference.md

## Essential Patterns

### Component Structure

Use `<script setup>` for modern Vue components:

```vue
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>

<template>
  <button @click="increment">Count: {{ count }}</button>
  <p>Doubled: {{ doubled }}</p>
</template>

<style scoped>
button { font-weight: bold; }
</style>
```

**More examples:** See @examples.md for 20+ official examples

### Reactivity

**Use `ref()` for:**
- Primitives (string, number, boolean)
- When you need to replace entire value
- Destructuring-friendly code

**Use `reactive()` for:**
- Objects/arrays only
- When you never replace the object

```javascript
// ✅ ref() for primitives
const count = ref(0)
count.value++ // Need .value in script

// ✅ reactive() for objects
const state = reactive({ count: 0 })
state.count++ // Direct access

// ⚠️ Don't destructure reactive()
const { count } = state // Loses reactivity!
```

### Props and Events

```vue
<script setup>
// Props with validation
defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0
  }
})

// Emits
const emit = defineEmits(['update', 'delete'])

function handleUpdate(value) {
  emit('update', value)
}
</script>
```

**Never mutate props** - always emit events instead.

### Composables

Reusable stateful logic following conventions:

```javascript
// composables/useMouse.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useMouse() {
  const x = ref(0)
  const y = ref(0)

  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  return { x, y }
}
```

**Composable conventions:**
- Name starts with "use"
- Return refs (not reactive objects)
- Clean up in `onUnmounted()`
- Call synchronously in setup

**Official guide:** https://vuejs.org/guide/reusability/composables.html

### Watchers

```javascript
// watch() - explicit sources
watch(count, (newVal, oldVal) => {
  console.log(`${oldVal} → ${newVal}`)
})

// watchEffect() - auto-track dependencies
watchEffect(() => {
  console.log('Count:', count.value)
})
```

## Best Practices

1. **Use `ref()` for primitives**
   ```javascript
   const count = ref(0) // ✅
   let count = 0 // ❌ Not reactive
   ```

2. **Use `computed()` for derived state**
   ```javascript
   const doubled = computed(() => count.value * 2) // ✅ Cached
   const doubled = count.value * 2 // ❌ Recalculates every render
   ```

3. **Never mutate props**
   ```javascript
   emit('update:count', props.count + 1) // ✅
   props.count++ // ❌
   ```

4. **Use `<script setup>` for cleaner code**
   - Automatic component registration
   - Less boilerplate
   - Better TypeScript inference

5. **Extract shared logic to composables**
   - Don't repeat stateful logic
   - Follow composable conventions
   - Clean up side effects

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Destructuring `reactive()` | Use `toRefs()` or `ref()` |
| Forgetting `.value` in script | Refs need `.value` outside templates |
| Mutating props | Emit events instead |
| `reactive()` for primitives | Use `ref()` |
| Not cleaning up | Use `onUnmounted()` |
| Conditional composable calls | Always call at top level |

## Resources

### Examples
**See @examples.md** for 20+ official Vue.js examples:
- Basic examples (Hello World, Forms, Components)
- Practical examples (Fetching Data, Markdown Editor)
- Advanced examples (CRUD, Tree View, Transitions)

**Live examples:** https://vuejs.org/examples/

### API Reference
**See @reference.md** for complete API documentation with links to:
- Reactivity Core (ref, reactive, computed, watch)
- Lifecycle Hooks (onMounted, onUnmounted, etc.)
- Component APIs (defineProps, defineEmits)
- Built-in Components (Transition, KeepAlive, Teleport)
- Template Directives (v-if, v-for, v-model)

**Full API:** https://vuejs.org/api/

### Official Guides
- **Introduction:** https://vuejs.org/guide/introduction.html
- **Quick Start:** https://vuejs.org/guide/quick-start.html
- **Composables:** https://vuejs.org/guide/reusability/composables.html
- **TypeScript:** https://vuejs.org/guide/typescript/overview.html

### Tools
- **Vue Playground:** https://play.vuejs.org/
- **Vue Router:** https://router.vuejs.org/
- **Pinia (State):** https://pinia.vuejs.org/
- **Vite (Build):** https://vitejs.dev/

## Red Flags

- Using Options API for new code → Use Composition API
- Mutating props → Emit events
- Deep watching everything → Watch specific sources
- Not using composables → Extract shared logic
- Ignoring TypeScript → Better DX with types
