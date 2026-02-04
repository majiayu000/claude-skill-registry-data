---
name: vuejs
description: Expert knowledge for working with VueJS, the preferred frontend framework we use along with Vite as a bundler
---

# VueJS

[VueJS](https://vuejs.org/) is the preferred frontend framework we use along with [Vite](https://vite.dev/) as a bundler.

## Core Principles

- Applications should stay current with Vue 3
- **Always use Composition API** (never Options API)
- **Default to `<script setup>`** syntax over plain `<script>` blocks
- Strong TypeScript integration is expected
- Use [VueUse](./vueuse.md) for common composable patterns
- Use [Vite](./vite.md) as the standard bundler
- Styling / CSS
  - Use the [Unocss](./unocss.md) framework over Tailwind CSS
  - Use both **flex** and **grid** layouts but prefer **grid** in cases where both are appropriate.

---

## Composition API Overview

The Composition API organizes component logic by feature rather than by option type. It enables better code reuse through composables and provides superior TypeScript support.

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Reactive state
const count = ref(0)

// Computed property
const doubled = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <button @click="increment">Count: {{ count }} (doubled: {{ doubled }})</button>
</template>
```

---

## Script Setup

`<script setup>` is syntactic sugar that provides:

- Less boilerplate code
- Better runtime performance (template compiles in same scope)
- Superior TypeScript type inference
- Automatic exposure of top-level bindings to template

### Compiler Macros

These macros are globally available in `<script setup>` without imports:

#### defineProps

```typescript
// Runtime declaration
const props = defineProps({
  title: { type: String, required: true },
  count: { type: Number, default: 0 }
})

// Type-based declaration (preferred)
const props = defineProps<{
  title: string
  count?: number
}>()

// With defaults (type-based)
const props = withDefaults(defineProps<{
  title: string
  count?: number
}>(), {
  count: 0
})

// Destructuring with defaults (3.5+)
const { title, count = 0 } = defineProps<{
  title: string
  count?: number
}>()
```

#### defineEmits

```typescript
// Runtime declaration
const emit = defineEmits(['update', 'delete'])

// Type-based declaration (preferred)
const emit = defineEmits<{
  update: [id: number, value: string]
  delete: [id: number]
}>()

// Usage
emit('update', 1, 'new value')
```

#### defineModel

Creates two-way binding props for `v-model`:

```typescript
// Default model (v-model)
const modelValue = defineModel<string>()
modelValue.value = 'hello' // emits 'update:modelValue'

// Named model (v-model:count)
const count = defineModel<number>('count', { default: 0 })

// With options
const title = defineModel<string>('title', {
  required: true,
  default: 'Untitled'
})
```

#### defineExpose

Explicitly expose properties to parent components via template refs:

```typescript
const internalState = ref(0)
const publicMethod = () => { /* ... */ }

// Only publicMethod is accessible via ref
defineExpose({
  publicMethod
})
```

#### defineOptions

Declare component options (Vue 3.3+):

```typescript
defineOptions({
  inheritAttrs: false,
  name: 'CustomComponent'
})
```

#### defineSlots

Type slot props (Vue 3.3+):

```typescript
const slots = defineSlots<{
  default(props: { item: Item }): any
  header(): any
}>()
```

### Accessing Slots and Attrs

```typescript
import { useSlots, useAttrs } from 'vue'

const slots = useSlots()
const attrs = useAttrs()
```

### Top-Level Await

Async operations are supported (requires `<Suspense>` wrapper):

```vue
<script setup>
const data = await fetch('/api/data').then(r => r.json())
</script>
```

---

## Reactivity System

### ref()

Wraps values in a reactive container. **Preferred for most cases.**

```typescript
import { ref } from 'vue'

const count = ref(0)
const user = ref<User | null>(null)

// Access/modify via .value
count.value++
user.value = { name: 'Ken' }

// Auto-unwraps in templates
// <template>{{ count }}</template> - no .value needed
```

**Advantages:**

- Works with primitives and objects
- Can be passed to functions while retaining reactivity
- Explicit `.value` makes reactivity visible

### reactive()

Makes objects deeply reactive without wrapping:

```typescript
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  user: { name: 'Ken' }
})

// Direct property access
state.count++
state.user.name = 'Kenneth'
```

**Limitations (prefer `ref()` instead):**

- Only works with objects, not primitives
- Cannot replace entire object: `state = { ... }` breaks reactivity
- Destructuring loses reactivity: `const { count } = state` is not reactive

### computed()

Creates cached derived values:

```typescript
import { ref, computed } from 'vue'

const firstName = ref('Ken')
const lastName = ref('Snyder')

// Read-only computed
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// Writable computed (rare)
const fullNameWritable = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value: string) => {
    const [first, last] = value.split(' ')
    firstName.value = first
    lastName.value = last
  }
})
```

**Best practices:**

- Keep getters pure (no side effects, async, or DOM mutations)
- Computed values are cached until dependencies change
- Use methods when caching isn't beneficial

### watch()

Watches specific reactive sources:

```typescript
import { ref, watch } from 'vue'

const count = ref(0)
const user = ref<User | null>(null)

// Watch single ref
watch(count, (newValue, oldValue) => {
  console.log(`Count changed: ${oldValue} -> ${newValue}`)
})

// Watch multiple sources
watch([count, user], ([newCount, newUser], [oldCount, oldUser]) => {
  // ...
})

// Watch getter function
watch(
  () => user.value?.name,
  (newName) => console.log(`Name: ${newName}`)
)

// Options
watch(count, callback, {
  immediate: true,  // Run immediately on creation
  deep: true,       // Deep watch nested objects (use sparingly)
  once: true,       // Run only once (3.4+)
  flush: 'post'     // Run after DOM updates
})

// Stop watching
const stop = watch(count, callback)
stop() // Stop the watcher
```

### watchEffect()

Automatically tracks all reactive dependencies accessed during execution:

```typescript
import { ref, watchEffect } from 'vue'

const count = ref(0)
const name = ref('Ken')

// Automatically tracks count and name
watchEffect(() => {
  console.log(`Count: ${count.value}, Name: ${name.value}`)
})

// With cleanup
watchEffect((onCleanup) => {
  const controller = new AbortController()
  fetch('/api/data', { signal: controller.signal })

  onCleanup(() => controller.abort())
})
```

**When to use which:**

- `watch()`: When you need old/new values, or want explicit control over dependencies
- `watchEffect()`: When callback uses the same values it needs to watch

### nextTick()

Wait for DOM updates after state changes:

```typescript
import { ref, nextTick } from 'vue'

const count = ref(0)

async function increment() {
  count.value++
  await nextTick()
  // DOM is now updated
}
```

---

## Lifecycle Hooks

All hooks must be called synchronously during `setup()`:

```typescript
import {
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onErrorCaptured,
  onActivated,
  onDeactivated
} from 'vue'

// Most commonly used
onMounted(() => {
  // Component is mounted, DOM is available
  console.log('Mounted')
})

onUnmounted(() => {
  // Cleanup: remove event listeners, cancel timers
  console.log('Unmounted')
})

onUpdated(() => {
  // DOM has been updated after reactive state change
  console.log('Updated')
})

// Less common
onBeforeMount(() => { /* Before initial render */ })
onBeforeUpdate(() => { /* Before DOM update */ })
onBeforeUnmount(() => { /* Before unmounting */ })

// Error handling
onErrorCaptured((err, instance, info) => {
  console.error('Error captured:', err)
  return false // Prevent propagation
})

// Keep-alive specific
onActivated(() => { /* Component activated from cache */ })
onDeactivated(() => { /* Component deactivated to cache */ })
```

---

## Component Patterns

### Props

```typescript
// Type-based declaration (preferred)
interface Props {
  title: string
  count?: number
  items: Item[]
  onUpdate?: (value: string) => void
}

const props = defineProps<Props>()

// With defaults
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => []  // Factory function for objects/arrays
})

// Destructuring with defaults
const { title, count = 0 } = defineProps<Props>()
```

**One-way data flow:** Props flow down, events flow up. Never mutate props directly.

```typescript
// BAD - mutating prop
props.count++

// GOOD - emit event to parent
const emit = defineEmits<{ update: [count: number] }>()
emit('update', props.count + 1)
```

### Emits

```typescript
// Type-based declaration
const emit = defineEmits<{
  change: [id: number]
  update: [id: number, value: string]
  'update:modelValue': [value: string]
}>()

// Usage
emit('change', 1)
emit('update', 1, 'new value')
```

### Slots

**Parent component:**

```vue
<template>
  <MyComponent>
    <!-- Default slot -->
    <p>Default content</p>

    <!-- Named slot -->
    <template #header>
      <h1>Header</h1>
    </template>

    <!-- Scoped slot -->
    <template #item="{ item, index }">
      <li>{{ index }}: {{ item.name }}</li>
    </template>
  </MyComponent>
</template>
```

**Child component:**

```vue
<script setup lang="ts">
interface Item {
  name: string
}

defineSlots<{
  default(): any
  header(): any
  item(props: { item: Item; index: number }): any
}>()
</script>

<template>
  <div>
    <header>
      <slot name="header" />
    </header>

    <main>
      <slot />  <!-- default slot -->
    </main>

    <ul>
      <li v-for="(item, index) in items" :key="item.id">
        <slot name="item" :item="item" :index="index" />
      </li>
    </ul>
  </div>
</template>
```

### Provide/Inject

Dependency injection for deeply nested components:

```typescript
// Parent component
import { provide, ref } from 'vue'
import type { InjectionKey } from 'vue'

// Type-safe injection key
const ThemeKey: InjectionKey<Ref<'light' | 'dark'>> = Symbol('theme')

const theme = ref<'light' | 'dark'>('light')

provide(ThemeKey, theme)

// Also provide mutation function
provide('setTheme', (newTheme: 'light' | 'dark') => {
  theme.value = newTheme
})
```

```typescript
// Child component (any depth)
import { inject } from 'vue'

const theme = inject(ThemeKey)  // Ref<'light' | 'dark'> | undefined
const theme = inject(ThemeKey, ref('light'))  // With default

const setTheme = inject<(theme: 'light' | 'dark') => void>('setTheme')
```

---

## TypeScript Integration

### Typing Refs

```typescript
import { ref, type Ref } from 'vue'

// Inferred
const count = ref(0)  // Ref<number>

// Explicit
const user = ref<User | null>(null)

// Complex types
interface State {
  items: Item[]
  loading: boolean
}
const state = ref<State>({ items: [], loading: false })
```

### Typing Reactive

```typescript
import { reactive } from 'vue'

interface State {
  count: number
  user: User | null
}

// Use interface annotation
const state: State = reactive({
  count: 0,
  user: null
})
```

### Typing Computed

```typescript
import { computed, type ComputedRef } from 'vue'

// Usually inferred
const doubled = computed(() => count.value * 2)  // ComputedRef<number>

// Explicit when needed
const user: ComputedRef<User | undefined> = computed(() =>
  users.value.find(u => u.id === selectedId.value)
)
```

### Typing Event Handlers

```typescript
function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  console.log(target.value)
}

function handleClick(event: MouseEvent) {
  console.log(event.clientX, event.clientY)
}
```

### Typing Template Refs

```typescript
import { ref, onMounted } from 'vue'

const inputRef = ref<HTMLInputElement | null>(null)
const componentRef = ref<InstanceType<typeof MyComponent> | null>(null)

onMounted(() => {
  inputRef.value?.focus()
  componentRef.value?.someMethod()
})
```

```vue
<template>
  <input ref="inputRef" />
  <MyComponent ref="componentRef" />
</template>
```

---

## Composables

Composables are functions that encapsulate and reuse stateful logic using Composition API.

### Naming Convention

Always prefix with `use`: `useMouse`, `useFetch`, `useAuth`

### Creating a Composable

```typescript
// composables/useMouse.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useMouse() {
  const x = ref(0)
  const y = ref(0)

  function update(event: MouseEvent) {
    x.value = event.pageX
    y.value = event.pageY
  }

  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  return { x, y }
}
```

```typescript
// Usage in component
import { useMouse } from '@/composables/useMouse'

const { x, y } = useMouse()
```

### Composable with Arguments

```typescript
// composables/useFetch.ts
import { ref, watchEffect, toValue, type MaybeRefOrGetter } from 'vue'

export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function fetchData() {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(toValue(url))
      data.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Unknown error')
    } finally {
      loading.value = false
    }
  }

  watchEffect(() => {
    fetchData()
  })

  return { data, error, loading, refetch: fetchData }
}
```

### Best Practices

1. **Return refs, not reactive objects** - Allows destructuring while maintaining reactivity
2. **Accept `MaybeRefOrGetter`** - Use `toValue()` to handle refs, getters, or plain values
3. **Clean up side effects** - Use `onUnmounted` or cleanup callbacks
4. **Call synchronously in setup** - Don't call composables inside callbacks or conditions

---

## Best Practices

### Prefer ref() over reactive()

```typescript
// Preferred
const count = ref(0)
const user = ref<User | null>(null)

// Avoid unless you have a specific reason
const state = reactive({ count: 0, user: null })
```

### Keep Computed Getters Pure

```typescript
// BAD
const doubled = computed(() => {
  fetch('/api/log')  // Side effect!
  return count.value * 2
})

// GOOD
const doubled = computed(() => count.value * 2)
```

### Use Descriptive Variable Names

```typescript
// BAD
const d = ref<User[]>([])

// GOOD
const users = ref<User[]>([])
const isLoading = ref(false)
const hasError = ref(false)
```

### Avoid Mutating Props

```typescript
// BAD
props.items.push(newItem)

// GOOD
emit('add-item', newItem)
```

### Type Everything

```typescript
// BAD
const props = defineProps(['title', 'count'])

// GOOD
const props = defineProps<{
  title: string
  count?: number
}>()
```

### Co-locate Related Logic

```typescript
// Group related state, computed, and methods together
// Feature 1: User management
const user = ref<User | null>(null)
const isLoggedIn = computed(() => user.value !== null)
async function login(credentials: Credentials) { /* ... */ }
async function logout() { /* ... */ }

// Feature 2: Theme
const theme = ref<'light' | 'dark'>('light')
const isDarkMode = computed(() => theme.value === 'dark')
function toggleTheme() { /* ... */ }
```

---

## Common Patterns

### Async Component Loading

```typescript
import { defineAsyncComponent } from 'vue'

const AsyncModal = defineAsyncComponent(() =>
  import('./components/Modal.vue')
)

const AsyncModalWithOptions = defineAsyncComponent({
  loader: () => import('./components/Modal.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,
  timeout: 3000
})
```

### v-model with Components

```vue
<!-- Parent -->
<CustomInput v-model="searchQuery" />
<CustomInput v-model:title="title" v-model:content="content" />
```

```vue
<!-- CustomInput.vue -->
<script setup lang="ts">
const model = defineModel<string>({ required: true })
</script>

<template>
  <input :value="model" @input="model = ($event.target as HTMLInputElement).value" />
</template>
```

### Conditional Rendering

```vue
<template>
  <!-- v-if for conditional rendering (removes from DOM) -->
  <div v-if="isLoading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <div v-else>{{ data }}</div>

  <!-- v-show for frequent toggling (CSS display: none) -->
  <div v-show="isVisible">Toggleable content</div>
</template>
```

### List Rendering

```vue
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>

  <!-- With index -->
  <li v-for="(item, index) in items" :key="item.id">
    {{ index }}: {{ item.name }}
  </li>

  <!-- Object iteration -->
  <div v-for="(value, key, index) in object" :key="key">
    {{ key }}: {{ value }}
  </div>
</template>
```

### Event Handling

```vue
<template>
  <!-- Method handler -->
  <button @click="handleClick">Click</button>

  <!-- Inline handler -->
  <button @click="count++">Increment</button>

  <!-- With event -->
  <button @click="handleClick($event)">Click</button>

  <!-- Modifiers -->
  <button @click.stop="handleClick">Stop propagation</button>
  <button @click.prevent="handleSubmit">Prevent default</button>
  <input @keyup.enter="submit" />
  <input @keyup.ctrl.enter="submitWithCtrl" />
</template>
```

### Form Handling

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue'

const form = reactive({
  email: '',
  password: '',
  remember: false
})

const errors = ref<Record<string, string>>({})

async function handleSubmit() {
  errors.value = {}

  if (!form.email) {
    errors.value.email = 'Email is required'
  }

  if (Object.keys(errors.value).length === 0) {
    await submitForm(form)
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="form.email" type="email" />
    <span v-if="errors.email">{{ errors.email }}</span>

    <input v-model="form.password" type="password" />

    <label>
      <input v-model="form.remember" type="checkbox" />
      Remember me
    </label>

    <button type="submit">Submit</button>
  </form>
</template>
```

---

## Related Resources

### Core Tools

- [VueUse Composables](./vueuse.md) - Collection of essential Vue composition utilities
- [Vite Configuration](./vite.md) - Bundler configuration for Vue projects

### TypeScript & Language Tooling

- [Volar / Vue Language Tools](./volar.md) - IDE support, TypeScript integration, and language server
- [vue-tsc](./vue-tsc.md) - Command-line type checking for Vue SFCs

### Styling

- [UnoCSS](./unocss.md) - Instant on-demand Atomic CSS engine (Tailwind-compatible)

### UI Components

- [UI Component Libraries](./ui-libraries.md) - Comprehensive guide to Vue 3 UI ecosystem:
  - Full suites (Vuetify, PrimeVue, Quasar, Naive UI)
  - Headless libraries (Headless UI, Inspira UI)
  - Specialized: tables, charts, forms, date pickers, editors

### Data Visualization

- [Chart.js](./chartjs.md) - Flexible charting library with Vue 3 integration via vue-chartjs

### Build Plugins

- [UnPlugins](./unplugin.md) - Essential Vue build plugins:
  - unplugin-vue-router - File-based routing with TypeScript
  - unplugin-vue-components - Auto-import components
  - unplugin-vue-macros - Extended compiler macros
  - unplugin-auto-import - Auto-import APIs

### Static Site Generation

- [Vite SSG](./vite-ssg.md) - Static site generation for Vue 3 on Vite
