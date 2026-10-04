---
name: vue
description: "Covers Vue.js across supported versions (3.4, 3.5, and upcoming 3.6 Vapor Mode): the Proxy-based reactivity system, virtual DOM with patch flags, Single-File Components, Composition API, composables, Pinia state management, TypeScript integration, SSR/hydration, Vue DevTools, and Vapor Mode. Use for \"Vue\", \"vue\", \"Vue.js\", \"Composition API\", \"Pinia\", \"ref\", \"reactive\", \"computed Vue\", \"defineProps\", \"defineEmits\", \"Vue 3\", \"Vapor Mode\", \"SFC\" questions."
license: MIT
---

# Vue.js

This skill covers Vue.js across all supported versions (3.4, 3.5, and upcoming 3.6 with Vapor Mode), including:

- Proxy-based reactivity system: `ref`, `reactive`, `computed`, `watch`, `watchEffect`, effect scheduling, dependency tracking internals
- Virtual DOM: template compilation to render functions, patch flags, static hoisting, `v-once`, `v-memo`, keyed diffing
- Single-File Components (SFCs): `<script setup>`, compiler macros (`defineProps`, `defineEmits`, `defineModel`, `defineExpose`, `defineSlots`), scoped styles (`:deep`, `:slotted`, `:global`)
- Composition API: lifecycle hooks, composable design patterns, `provide`/`inject`, `effectScope`
- Vapor Mode (3.6 beta): no-VDOM compilation, fine-grained DOM updates, Alien Signals engine
- Pinia state management: setup stores, `storeToRefs`, SSR hydration, DevTools integration
- TypeScript: generic components, typed props/emits/model, `InjectionKey`, vue-tsc, Volar
- Performance: `shallowRef`/`shallowReactive`, lazy hydration strategies, computed caching, `v-memo`
- SSR and hydration: streaming, `data-allow-mismatch`, `useId()`, `ClientOnly` patterns
- Vue Router: route guards, lazy loading, nested routes, typed routes
- Testing: Vitest + `@vue/test-utils`, composable testing, Pinia test setup
- DevTools: component inspector, reactivity graph, Pinia timeline, performance profiling

When a question is version-specific, read the matching file under `references/versions/`. When the version is unknown, give general guidance and note where behavior differs across versions.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Troubleshooting** -- Load `references/diagnostics.md`
   - **Performance** -- Load `references/best-practices.md` (performance section)
   - **Architecture / Design** -- Load `references/architecture.md`
   - **Composition API** -- Load `references/patterns/composition-api.md`
   - **State Management** -- Load `references/patterns/pinia.md`
   - **TypeScript** -- Load `references/patterns/typescript.md`
   - **Configuration** -- Reference `assets/tsconfig.json` or `assets/vite.config.ts`

2. **Identify version** -- Determine whether the user is on Vue 3.4, 3.5, or 3.6 beta. If unclear, ask. Version matters for reactive props destructure, `useTemplateRef`, `useId`, lazy hydration, and Vapor Mode.

3. **Load context** -- Read the relevant reference file for deep knowledge.

4. **Analyze** -- Apply Vue-specific reasoning, not generic JavaScript advice. Consider the reactivity system, template compilation, component boundaries, and SFC semantics.

5. **Recommend** -- Provide actionable guidance with code examples. Prefer idiomatic Vue patterns using Composition API and `<script setup>`.

6. **Verify** -- Suggest validation steps (Vue DevTools, console warnings, test assertions).

## Core Expertise

### Reactivity System

Vue 3 uses ES Proxy for reactive state. Every reactive object is wrapped in a Proxy that intercepts `get` (track dependencies) and `set` (trigger effects).

```ts
import { ref, reactive, computed, watch, watchEffect } from 'vue'

// ref -- wraps primitives and objects; access via .value in script
const count = ref(0)
count.value++                    // triggers effects
// In template: {{ count }} -- auto-unwrapped

// reactive -- deep Proxy for plain objects
const state = reactive({ user: { name: 'Alice' }, items: [] })
state.user.name = 'Bob'         // deep tracking at every level

// computed -- lazy, cached derived value
const fullName = computed(() => `${state.user.first} ${state.user.last}`)

// watch -- explicit side effects with old/new values
watch(count, (newVal, oldVal) => { /* runs when count.value changes */ })
watch(() => state.user.name, (name) => { /* getter form for nested paths */ })

// watchEffect -- auto-tracks all reactive reads
watchEffect(() => {
  console.log(count.value)       // auto-tracked; re-runs on change
})
```

Effects are batched into a microtask queue. Multiple mutations in the same synchronous block produce one re-render. Use `nextTick()` to await DOM updates.

Vue 3.5 ships a new reactivity engine with 56% memory reduction and ~10x faster array mutation tracking via a doubly-linked list for dependency tracking.

### Virtual DOM and Template Compilation

Templates compile to render functions with optimized patch flags. The compiler emits integer flags telling the runtime exactly what can change per VNode, skipping full diffing.

```ts
// Patch flags: 1=TEXT, 2=CLASS, 4=STYLE, 8=PROPS, -1=STATIC, -2=V_ONCE
// Static nodes are hoisted outside render functions and reused across renders
```

`v-once` renders subtrees once and excludes them from future diffs. `v-memo` re-renders only when listed deps change -- critical for optimizing large `v-for` lists.

### Single-File Components

```html
<script setup lang="ts">
// Compiler macros -- no import needed
const props = defineProps<{ title: string; count?: number }>()
const emit = defineEmits<{ update: [value: string]; close: [] }>()
const modelValue = defineModel<string>()
defineExpose({ focus, reset })
</script>

<template>
  <div>{{ title }}</div>
</template>

<style scoped>
/* Scoped via data-v-xxxxxxxx attribute */
.btn { color: red; }
:deep(.child-class) { font-size: 14px; }
:slotted(p) { margin: 0; }
:global(body) { margin: 0; }
</style>
```

`<script setup>` is the standard -- everything at top level is automatically available in the template. Top-level `await` makes the component async (wrap parent in `<Suspense>`).

### Composition API

Composables are the primary reuse pattern, replacing mixins and the Options API. A composable is a function using Composition API internals, conventionally prefixed with `use`.

```ts
export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  watchEffect(async () => {
    loading.value = true
    try {
      const res = await fetch(toValue(url))
      data.value = await res.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  })

  return { data, error, loading }
}
```

Key principles: return refs (not raw values) so callers can destructure without losing reactivity. Accept `MaybeRefOrGetter<T>` parameters for flexibility. Clean up side effects.

### Pinia State Management

```ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubled = computed(() => count.value * 2)
  function increment() { count.value++ }
  return { count, doubled, increment }
})

// Usage with reactive destructure
import { storeToRefs } from 'pinia'
const store = useCounterStore()
const { count, doubled } = storeToRefs(store)
const { increment } = store
```

### Vapor Mode (3.6 Beta)

Opt-in compilation target that eliminates the Virtual DOM. The Vapor compiler generates direct DOM manipulation code with fine-grained reactive effects. Requires `<script setup>` (Composition API). Uses the Alien Signals reactivity engine.

### TypeScript Integration

Vue has first-class TypeScript support via `vue-tsc` and Volar. Generic components (`<script setup lang="ts" generic="T">`), typed injection keys (`InjectionKey<T>`), and typed template refs (`useTemplateRef<T>`) provide end-to-end type safety.

## Common Pitfalls

**1. Destructuring reactive objects loses reactivity**
`const { count } = reactive({ count: 0 })` produces a plain number. Fix: use `toRefs(state)` or prefer `ref` for composable returns.

**2. Forgetting .value in script**
`ref` requires `.value` access in JavaScript but is auto-unwrapped in templates. This is the most common beginner mistake.

**3. Deep vs shallow reactivity confusion**
`reactive` and `ref` are deep by default. For large objects replaced wholesale, use `shallowRef` to avoid deep proxy overhead.

**4. Stale closures in watch/watchEffect**
Similar to React hooks -- callbacks capture variables at creation time. Use `watch` with explicit sources rather than relying on closure scope for changing values.

**5. v-for without stable keys**
Using array index as `:key` on reorderable lists causes incorrect reconciliation. Always use stable unique identifiers.

**6. Using Options API in new projects**
Composition API with `<script setup>` is the recommended standard. Options API is supported but offers less TypeScript integration and composability.

**7. Mutating props directly**
Props are read-only in children. Use `defineEmits` or `defineModel` for parent-child communication.

**8. Watchers without cleanup**
Effects that create subscriptions, timers, or fetch calls must clean up. Use `onWatcherCleanup()` (3.5) or the return value from `watchEffect`.

**9. Hydration mismatches in SSR**
`Date.now()`, `Math.random()`, and browser APIs during SSR cause mismatches. Defer client-only content to `onMounted` or use `data-allow-mismatch` (3.5).

**10. Importing defineProps/defineEmits**
These are compiler macros, not runtime functions. Never import them -- they are available automatically in `<script setup>`.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 3.5 | `references/versions/3.5.md` | Reactive Props Destructure, `useTemplateRef`, `useId`, lazy hydration strategies, `defineModel` enhancements, deferred Teleport, `onWatcherCleanup`, `data-allow-mismatch`, reactivity performance improvements, Vapor Mode preview |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Reactivity system internals, VDOM compilation, SFC structure, Composition API lifecycle, Vapor Mode. Read for "how does X work" questions.
- `references/best-practices.md` -- Composable patterns, Pinia usage, TypeScript integration, performance optimization, testing setup. Read for design and quality questions.
- `references/diagnostics.md` -- Reactivity pitfalls, template errors, hydration mismatches. Read when troubleshooting errors.

## Configuration References

- `assets/tsconfig.json` -- Annotated TypeScript configuration for Vue 3.5 projects with Volar
- `assets/vite.config.ts` -- Annotated Vite configuration with Vue plugin, path aliases, and SCSS

## Pattern Guides

- `references/patterns/composition-api.md` -- Composable design, ref vs reactive, provide/inject, effectScope
- `references/patterns/pinia.md` -- Store patterns, SSR hydration, DevTools, testing
- `references/patterns/typescript.md` -- Typed props/emits/model, generic components, injection keys
