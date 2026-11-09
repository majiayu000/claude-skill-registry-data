---
name: vue-expert
description: Vue 3 Composition API, reactivity system, Pinia state management, Nuxt 3, Vue Router, component design patterns, and migration from Options API.
---

# Vue Expert

Deep technical reference for senior Vue developers building production applications with Vue 3. Covers the Composition API in depth, Vue's reactivity system internals, component design patterns, Pinia state management, Vue Router advanced usage, Nuxt 3 full-stack patterns, testing strategies, and migration paths from Vue 2 and the Options API. Every section includes working code, rationale, and anti-patterns to avoid.

## Table of Contents

- [Composition API](#composition-api)
- [Reactivity System](#reactivity-system)
- [Component Patterns](#component-patterns)
- [Pinia State Management](#pinia-state-management)
- [Vue Router](#vue-router)
- [Nuxt 3](#nuxt-3)
- [Testing](#testing)
- [Migration and Performance](#migration-and-performance)

---

## Composition API

### setup() and Script Setup

`<script setup>` is the recommended syntax. It compiles the entire `<script>` block into the component's `setup()` function, reducing boilerplate and improving runtime performance through compile-time optimizations.

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { User } from '@/types'

const props = defineProps<{ userId: string }>()
const emit = defineEmits<{ (e: 'update', user: User): void }>()

const user = ref<User | null>(null)
const displayName = computed(() => user.value?.name ?? 'Anonymous')

onMounted(async () => {
  user.value = await fetchUser(props.userId)
})
</script>
```

When you need to declare component options like `inheritAttrs` or a custom name, use a separate plain `<script>` block alongside `<script setup>`.

```vue
<script lang="ts">
export default { name: 'UserProfile', inheritAttrs: false }
</script>

<script setup lang="ts">
// setup logic here
</script>
```

### ref vs reactive

`ref()` wraps any value (primitives, objects, arrays) in a reactive container accessed via `.value`. `reactive()` creates a deeply reactive proxy of an object but cannot hold primitives and loses reactivity if destructured.

```typescript
import { ref, reactive } from 'vue'

// ref: works with any type, requires .value in script
const count = ref(0)
count.value++

const user = ref<User | null>(null)
user.value = { name: 'Alice', age: 30 }

// reactive: object-only, no .value needed, but cannot reassign root
const state = reactive({ items: [] as string[], loading: false })
state.loading = true
state.items.push('new item')

// DANGER: reassigning a reactive object breaks reactivity
// state = { items: [], loading: false }  // reactivity lost
```

Prefer `ref()` as the default. It works uniformly with primitives and objects, is explicit about reactivity (`.value`), and avoids the destructuring trap of `reactive()`.

### computed

Computed refs are cached and only re-evaluate when their reactive dependencies change.

```typescript
import { ref, computed } from 'vue'

const items = ref<Product[]>([])
const search = ref('')

// Read-only computed
const filtered = computed(() =>
  items.value.filter(item =>
    item.name.toLowerCase().includes(search.value.toLowerCase())
  )
)

// Writable computed
const selectedIds = ref<Set<string>>(new Set())
const allSelected = computed({
  get: () => selectedIds.value.size === items.value.length,
  set: (val: boolean) => {
    selectedIds.value = val
      ? new Set(items.value.map(i => i.id))
      : new Set()
  },
})
```

### watch and watchEffect

`watch` tracks specific sources and provides old/new values. `watchEffect` automatically tracks every reactive dependency accessed during execution.

```typescript
import { ref, watch, watchEffect } from 'vue'

const userId = ref('u-1')
const userData = ref<User | null>(null)

// watch: explicit source, lazy by default
watch(userId, async (newId, oldId) => {
  console.log(`Changed from ${oldId} to ${newId}`)
  userData.value = await fetchUser(newId)
}, { immediate: true })

// watch multiple sources
watch([userId, () => route.query.tab], ([id, tab]) => {
  loadContent(id, tab as string)
})

// watchEffect: auto-tracks dependencies, runs immediately
const stop = watchEffect(async (onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())

  const data = await fetch(`/api/v1/users/${userId.value}`, {
    signal: controller.signal,
  })
  userData.value = await data.json()
})

// Stop the watcher manually when needed
stop()
```

### Composables

Composables are functions that encapsulate and reuse stateful logic using Composition API. They are the Vue equivalent of React's custom hooks.

```typescript
// composables/useFetch.ts
import { ref, watchEffect, type Ref } from 'vue'

interface UseFetchReturn<T> {
  data: Ref<T | null>
  error: Ref<string | null>
  loading: Ref<boolean>
}

export function useFetch<T>(url: Ref<string> | string): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>
  const error = ref<string | null>(null)
  const loading = ref(false)

  watchEffect(async (onCleanup) => {
    const controller = new AbortController()
    onCleanup(() => controller.abort())

    loading.value = true
    error.value = null

    try {
      const urlValue = typeof url === 'string' ? url : url.value
      const response = await fetch(urlValue, { signal: controller.signal })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      data.value = await response.json()
    } catch (e) {
      if (e instanceof Error && e.name !== 'AbortError') {
        error.value = e.message
      }
    } finally {
      loading.value = false
    }
  })

  return { data, error, loading }
}
```

```vue
<script setup lang="ts">
import { useFetch } from '@/composables/useFetch'

const { data: users, loading, error } = useFetch<User[]>('/api/v1/users')
</script>
```

### Lifecycle Hooks

All Options API lifecycle hooks have Composition API equivalents prefixed with `on`.

| Options API | Composition API | When |
|---|---|---|
| `beforeCreate` / `created` | `setup()` itself | Reactive data initialized |
| `beforeMount` | `onBeforeMount` | Before first DOM render |
| `mounted` | `onMounted` | DOM is available |
| `beforeUpdate` | `onBeforeUpdate` | Before reactive DOM update |
| `updated` | `onUpdated` | After reactive DOM update |
| `beforeUnmount` | `onBeforeUnmount` | Before teardown |
| `unmounted` | `onUnmounted` | After teardown |
| `errorCaptured` | `onErrorCaptured` | Error from descendant |
| `activated` | `onActivated` | `<KeepAlive>` re-activated |
| `deactivated` | `onDeactivated` | `<KeepAlive>` deactivated |

### Anti-patterns

- Using `reactive()` for everything and then destructuring it -- reactivity is silently lost. Use `ref()` or wrap destructured values with `toRefs()`.
- Accessing `.value` inside templates -- Vue auto-unwraps refs in templates, so `{{ count }}` is correct, not `{{ count.value }}`.
- Putting side effects inside `computed()` -- computed should be pure. Use `watch` or `watchEffect` for side effects.
- Creating composables that rely on component context but are called outside `setup()` -- lifecycle hooks and inject only work within setup.

---

## Reactivity System

### How Reactivity Works

Vue 3 uses ES `Proxy` objects (replacing Vue 2's `Object.defineProperty`) to intercept get/set operations. When a reactive property is read inside a running effect (render function, computed, watcher), Vue tracks the dependency. When the property changes, Vue triggers all effects that depend on it.

```
ref(0)  -->  Proxy { value: 0 }
                |
         get .value --> track(effect)
         set .value --> trigger(effects)
```

This proxy-based system has key advantages over Vue 2: it detects property additions/deletions, array index mutations, and Map/Set operations without special helper methods.

### shallowRef and shallowReactive

Use shallow variants when you have large objects where deep reactivity tracking is wasteful. Only the top-level `.value` assignment (for `shallowRef`) or top-level property changes (for `shallowReactive`) trigger updates.

```typescript
import { shallowRef, triggerRef } from 'vue'

const largeList = shallowRef<DataRow[]>([])

// This does NOT trigger reactivity (mutating inner array)
largeList.value.push({ id: '1', value: 42 })

// Option 1: reassign .value to trigger
largeList.value = [...largeList.value, { id: '2', value: 99 }]

// Option 2: mutate then manually trigger
largeList.value.push({ id: '3', value: 77 })
triggerRef(largeList)
```

### toRef and toRefs

Convert reactive object properties into individual refs that maintain the reactive connection.

```typescript
import { reactive, toRef, toRefs } from 'vue'

const state = reactive({ name: 'Alice', age: 30 })

// Single property
const nameRef = toRef(state, 'name')
nameRef.value = 'Bob' // state.name is now 'Bob'

// All properties -- essential for destructuring without losing reactivity
const { name, age } = toRefs(state)
name.value = 'Charlie' // state.name is now 'Charlie'
```

The most common use is destructuring props in composables:

```typescript
export function useUserSearch(props: { query: string; limit: number }) {
  const { query, limit } = toRefs(props)
  // query and limit are now reactive refs
}
```

### Reactivity Transform (Deprecated)

The Reactivity Transform (`$ref`, `$computed`, `$toRef`) was an experimental compile-time feature that removed the need for `.value`. It was deprecated in Vue 3.3 and removed in Vue 3.4. Do not use it in new code. If migrating, replace `$ref(0)` with `ref(0)` and add `.value` access.

### markRaw and toRaw

Opt objects out of reactivity entirely when they should never be observed (class instances, third-party library objects, immutable data).

```typescript
import { markRaw, reactive, toRaw } from 'vue'

import { Chart } from 'chart.js'

const state = reactive({
  chartInstance: markRaw(new Chart(/* ... */)),
  data: [1, 2, 3],
})

// toRaw: get the original object behind a reactive proxy
const raw = toRaw(state) // plain object, no proxy
```

### Reactivity Gotchas

| Gotcha | Explanation | Fix |
|---|---|---|
| Destructuring `reactive()` | Extracts plain values, loses reactivity | Use `toRefs()` or use `ref()` instead |
| Replacing a `reactive` root | `state = newObj` breaks the proxy | Mutate properties: `Object.assign(state, newObj)` |
| Adding properties to `reactive` | Works in Vue 3 (Proxy), but not Vue 2 | No fix needed in Vue 3 |
| Non-primitive ref in template | Auto-unwrapped, no `.value` needed | Just use `{{ myRef }}` |
| Async gap in watchEffect | Dependencies accessed after `await` are not tracked | Access all reactive deps before the first `await` |

### Anti-patterns

- Wrapping everything in `reactive()` when `ref()` is simpler and safer for primitives.
- Calling `triggerRef()` frequently instead of designing state updates as immutable replacements.
- Forgetting that `watchEffect` only tracks dependencies accessed synchronously during execution -- anything read after an `await` is invisible to the tracker.
- Using `markRaw` on data that should be reactive -- typically a sign of premature optimization.

---

## Component Patterns

### Props and Emits with TypeScript

Vue 3.3+ supports type-only props/emits declarations with defaults.

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items: string[]
  variant?: 'primary' | 'secondary'
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  variant: 'primary',
})

const emit = defineEmits<{
  (e: 'update', value: string): void
  (e: 'delete', id: string): void
}>()

// Vue 3.3+ shorthand emit syntax
const emit2 = defineEmits<{
  update: [value: string]
  delete: [id: string]
}>()
</script>
```

### v-model on Components

Vue 3 supports multiple v-model bindings on a single component. Each maps to a `modelValue`-style prop and `update:` event.

```vue
<!-- Parent -->
<UserForm v-model:name="userName" v-model:email="userEmail" />

<!-- UserForm.vue -->
<script setup lang="ts">
const name = defineModel<string>('name', { required: true })
const email = defineModel<string>('email', { required: true })
</script>

<template>
  <input :value="name" @input="name = ($event.target as HTMLInputElement).value" />
  <input :value="email" @input="email = ($event.target as HTMLInputElement).value" />
</template>
```

`defineModel()` (Vue 3.4+) creates a ref that automatically syncs with the parent's v-model. This replaces the manual `defineProps` + `defineEmits` pattern.

### Slots: Named, Scoped, and Dynamic

```vue
<!-- BaseLayout.vue -->
<template>
  <header><slot name="header" /></header>
  <main><slot /></main>
  <footer><slot name="footer" :year="currentYear" /></footer>
</template>

<!-- Parent usage -->
<BaseLayout>
  <template #header>
    <h1>Dashboard</h1>
  </template>

  <p>Main content goes in the default slot</p>

  <template #footer="{ year }">
    <span>&copy; {{ year }}</span>
  </template>
</BaseLayout>
```

Dynamic slot names allow programmatic slot selection:

```vue
<template v-for="section in sections" :key="section.id">
  <slot :name="section.slotName" :data="section.data" />
</template>
```

### Renderless Components with Scoped Slots

Renderless components encapsulate logic without prescribing UI. They expose state and methods through scoped slots.

```vue
<!-- MouseTracker.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const x = ref(0)
const y = ref(0)

function update(event: MouseEvent) {
  x.value = event.pageX
  y.value = event.pageY
}

onMounted(() => window.addEventListener('mousemove', update))
onUnmounted(() => window.removeEventListener('mousemove', update))
</script>

<template>
  <slot :x="x" :y="y" />
</template>

<!-- Usage -->
<MouseTracker v-slot="{ x, y }">
  <p>Mouse is at {{ x }}, {{ y }}</p>
</MouseTracker>
```

### provide / inject

Dependency injection for deeply nested components. Avoids prop drilling.

```typescript
// types/injection-keys.ts
import type { InjectionKey, Ref } from 'vue'

export const ThemeKey: InjectionKey<Ref<'light' | 'dark'>> = Symbol('theme')
export const ApiClientKey: InjectionKey<ApiClient> = Symbol('api-client')
```

```vue
<!-- Provider (ancestor) -->
<script setup lang="ts">
import { provide, ref } from 'vue'
import { ThemeKey } from '@/types/injection-keys'

const theme = ref<'light' | 'dark'>('light')
provide(ThemeKey, theme)
</script>
```

```vue
<!-- Consumer (any descendant) -->
<script setup lang="ts">
import { inject } from 'vue'
import { ThemeKey } from '@/types/injection-keys'

const theme = inject(ThemeKey)
// type: Ref<'light' | 'dark'> | undefined

// With default value (removes undefined from type)
const theme2 = inject(ThemeKey, ref('light'))
</script>
```

### Async Components and Suspense

Lazy-load components with loading and error states.

```typescript
import { defineAsyncComponent } from 'vue'

const AsyncDashboard = defineAsyncComponent({
  loader: () => import('./Dashboard.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,      // ms before showing loading component
  timeout: 10000,  // ms before showing error component
})
```

`<Suspense>` (experimental) provides a declarative way to handle async dependencies in a component subtree:

```vue
<template>
  <Suspense>
    <template #default>
      <AsyncDashboard />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>
```

Components with async `setup()` are automatically Suspense-compatible:

```vue
<script setup lang="ts">
const data = await fetchDashboardData() // top-level await makes this async
</script>
```

### Anti-patterns

- Deeply nesting `provide/inject` without typed injection keys -- leads to `unknown` types and missing dependency errors at runtime.
- Using `Suspense` in production without an error boundary -- if the async component fails, the entire subtree disappears.
- Defining emit names as strings without TypeScript definitions -- prevents type checking of emitted payloads.
- Creating "god components" that mix layout, logic, and data fetching -- extract composables for logic and use slots for flexible layouts.

---

## Pinia State Management

### Defining Stores

Pinia supports two syntaxes: Options stores and Setup stores. Setup stores align with the Composition API and offer more flexibility.

```typescript
// stores/useAuthStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Setup store (recommended)
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const displayName = computed(() => user.value?.name ?? 'Guest')

  async function login(credentials: LoginPayload) {
    const response = await api.post('/api/v1/auth/login', credentials)
    token.value = response.data.token
    user.value = response.data.user
  }

  function logout() {
    token.value = null
    user.value = null
  }

  return { user, token, isAuthenticated, displayName, login, logout }
})
```

```typescript
// Options store syntax (familiar for Vuex users)
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0, lastUpdated: null as Date | null }),
  getters: {
    doubleCount: (state) => state.count * 2,
    isPositive(): boolean { return this.count > 0 },
  },
  actions: {
    increment() {
      this.count++
      this.lastUpdated = new Date()
    },
    async fetchCount() {
      const data = await api.get('/api/v1/counter')
      this.count = data.count
    },
  },
})
```

### Using Stores in Components

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/useAuthStore'

const authStore = useAuthStore()

// Destructure reactive state with storeToRefs (preserves reactivity)
const { user, isAuthenticated } = storeToRefs(authStore)

// Actions can be destructured directly (they are plain functions)
const { login, logout } = authStore
</script>
```

### Plugins

Pinia plugins extend every store with additional behavior.

```typescript
// plugins/piniaLogger.ts
import type { PiniaPlugin } from 'pinia'

export const piniaLogger: PiniaPlugin = ({ store }) => {
  store.$onAction(({ name, args, after, onError }) => {
    console.log(`[${store.$id}] Action: ${name}`, args)

    after((result) => {
      console.log(`[${store.$id}] Action ${name} completed`, result)
    })

    onError((error) => {
      console.error(`[${store.$id}] Action ${name} failed`, error)
    })
  })
}

// main.ts
const pinia = createPinia()
pinia.use(piniaLogger)
```

### Composing Stores

Stores can use other stores. Import and call the store function inside actions or getters.

```typescript
export const useCartStore = defineStore('cart', () => {
  const authStore = useAuthStore()
  const items = ref<CartItem[]>([])

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.qty, 0)
  )

  async function checkout() {
    if (!authStore.isAuthenticated) {
      throw new Error('Must be logged in to checkout')
    }
    await api.post('/api/v1/orders', {
      items: items.value,
      userId: authStore.user!.id,
    })
    items.value = []
  }

  return { items, total, checkout }
})
```

### SSR Hydration

When using Pinia with SSR (Nuxt 3), the server serializes store state into the HTML payload. The client hydrates it automatically. For non-serializable state, use `skipHydrate`:

```typescript
import { skipHydrate } from 'pinia'

export const useWebSocketStore = defineStore('ws', () => {
  const socket = ref(skipHydrate(null as WebSocket | null))
  const messages = ref<Message[]>([])

  return { socket, messages }
})
```

### Anti-patterns

- Destructuring state directly from a store (`const { count } = store`) -- loses reactivity. Use `storeToRefs()` for state and getters.
- Putting everything in a single store -- split by domain (auth, cart, ui, notifications) for maintainability and code splitting.
- Mutating state outside actions in production -- enable strict mode (`pinia.use(strictMode)` or Nuxt devtools) to catch direct mutations during development.
- Using Pinia for server/cache state that TanStack Query or `useFetch` handles better -- Pinia is for client-side application state.

---

## Vue Router

### Route Definitions with TypeScript

```typescript
// router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('@/pages/Home.vue') },
      { path: 'about', name: 'about', component: () => import('@/pages/About.vue') },
    ],
  },
  {
    path: '/users/:id',
    name: 'user-profile',
    component: () => import('@/pages/UserProfile.vue'),
    props: true, // passes :id as a prop
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, roles: ['admin'] },
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('@/pages/admin/Dashboard.vue') },
      { path: 'users', name: 'admin-users', component: () => import('@/pages/admin/Users.vue') },
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/pages/NotFound.vue') },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
})

export default router
```

### Navigation Guards

Guards run in order: global `beforeEach` -> per-route `beforeEnter` -> in-component `beforeRouteEnter` -> global `afterEach`.

```typescript
// Global guard: authentication check
router.beforeEach(async (to, from) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.roles) {
    const hasRole = (to.meta.roles as string[]).some(
      role => authStore.user?.roles.includes(role)
    )
    if (!hasRole) return { name: 'forbidden' }
  }
})

// Per-route guard
{
  path: '/checkout',
  component: () => import('@/pages/Checkout.vue'),
  beforeEnter: (to) => {
    const cart = useCartStore()
    if (cart.items.length === 0) return { name: 'shop' }
  },
}
```

### Composable-Based Navigation

```vue
<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Reactive route params
const userId = computed(() => route.params.id as string)

// Programmatic navigation
async function handleSave() {
  await saveUser()
  router.push({ name: 'user-profile', params: { id: userId.value } })
}

// Replace current history entry
router.replace({ query: { ...route.query, page: '2' } })
</script>
```

### Dynamic Routes

Add or remove routes at runtime for plugin systems or feature flags.

```typescript
// Add route dynamically
const removeRoute = router.addRoute({
  path: '/experiments/:slug',
  name: 'experiment',
  component: () => import('@/pages/Experiment.vue'),
})

// Remove it later
removeRoute()

// Or remove by name
router.removeRoute('experiment')
```

### Typed Route Meta

Augment the `RouteMeta` interface to get type safety on `route.meta`.

```typescript
// router/types.ts
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    roles?: string[]
    title?: string
    transition?: string
  }
}
```

### Anti-patterns

- Using string paths everywhere instead of named routes -- breaks when paths change.
- Fetching data in `beforeEach` global guards -- slows every navigation. Use per-route guards or in-component data fetching.
- Not lazy-loading route components -- ships the entire app in one bundle.
- Ignoring the `scrollBehavior` option -- users expect scroll position to restore on back navigation.

---

## Nuxt 3

### Auto-Imports

Nuxt 3 auto-imports Vue APIs, composables, and utilities. No manual import statements needed for `ref`, `computed`, `useState`, `useFetch`, `navigateTo`, or any composable in the `composables/` directory.

```vue
<!-- No imports needed -->
<script setup lang="ts">
const count = ref(0)
const doubled = computed(() => count.value * 2)
const { data: users } = await useFetch('/api/v1/users')
</script>
```

Custom composables placed in `composables/` are auto-imported by filename:

```
composables/
  useAuth.ts        --> useAuth() available everywhere
  useFormatDate.ts  --> useFormatDate() available everywhere
```

### File-Based Routing

Nuxt generates routes from the `pages/` directory structure.

```
pages/
  index.vue              --> /
  about.vue              --> /about
  users/
    index.vue            --> /users
    [id].vue             --> /users/:id
  posts/
    [...slug].vue        --> /posts/* (catch-all)
  admin/
    [[dashboard]].vue    --> /admin, /admin/dashboard (optional param)
```

### Server Routes (API Routes)

Full-stack API endpoints live in `server/api/` and `server/routes/`.

```typescript
// server/api/users/[id].get.ts
import { defineEventHandler, getRouterParam, createError } from 'h3'

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  const user = await db.user.findUnique({ where: { id } })

  if (!user) {
    throw createError({ statusCode: 404, message: 'User not found' })
  }

  return user
})
```

```typescript
// server/api/users/index.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody<{ name: string; email: string }>(event)
  const user = await db.user.create({ data: body })
  return user
})
```

### useFetch and useAsyncData

`useFetch` is a convenience wrapper around `useAsyncData` + `$fetch`. It deduplicates requests during SSR and auto-serializes data for hydration.

```vue
<script setup lang="ts">
// Basic usage -- runs on server during SSR, hydrates on client
const { data: users, pending, error, refresh } = await useFetch<User[]>('/api/v1/users')

// With query params and watch
const page = ref(1)
const { data: posts } = await useFetch('/api/v1/posts', {
  query: { page, limit: 20 },
  watch: [page], // re-fetches when page changes
})

// useAsyncData for custom async logic
const { data: stats } = await useAsyncData('dashboard-stats', () => {
  return Promise.all([
    $fetch('/api/v1/stats/revenue'),
    $fetch('/api/v1/stats/users'),
  ])
})

// Client-only fetch (skip SSR)
const { data: notifications } = await useFetch('/api/v1/notifications', {
  server: false,
})
</script>
```

### Middleware

Nuxt middleware runs before navigating to a route. Place files in `middleware/`.

```typescript
// middleware/auth.ts (named middleware -- applied per-page)
export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated.value) {
    return navigateTo('/login', { redirectCode: 301 })
  }
})
```

```vue
<!-- pages/dashboard.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  layout: 'admin',
})
</script>
```

Global middleware runs on every route -- suffix the filename with `.global`:

```typescript
// middleware/analytics.global.ts
export default defineNuxtRouteMiddleware((to) => {
  trackPageView(to.fullPath)
})
```

### Modules and Runtime Config

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt', '@nuxt/image', '@vueuse/nuxt'],

  runtimeConfig: {
    // Server-only (not exposed to client)
    databaseUrl: process.env.DATABASE_URL,
    jwtSecret: process.env.JWT_SECRET,

    // Exposed to client
    public: {
      apiBase: process.env.API_BASE || '/api/v1',
      appName: 'My App',
    },
  },
})
```

```vue
<script setup lang="ts">
const config = useRuntimeConfig()
// In client code: only config.public.* is available
const apiBase = config.public.apiBase
</script>
```

### Deployment

Nuxt 3 uses Nitro as its server engine, supporting multiple deployment presets.

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    preset: 'node-server',     // Node.js (default)
    // preset: 'vercel',       // Vercel
    // preset: 'cloudflare',   // Cloudflare Workers
    // preset: 'netlify',      // Netlify
    // preset: 'static',       // Static site generation
  },
})
```

### Anti-patterns

- Using `$fetch` directly in components instead of `useFetch` -- causes duplicate requests (server + client) during SSR.
- Putting secrets in `runtimeConfig.public` -- anything under `public` is shipped to the client. Use root-level `runtimeConfig` for secrets.
- Creating API routes that bypass Nuxt's server middleware -- use `server/middleware/` for cross-cutting concerns like auth validation.
- Ignoring the `key` option on `useFetch` when the same endpoint is called with different params -- causes cache collisions.

---

## Testing

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./test/setup.ts'],
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
```

### Component Testing with Vue Test Utils

```typescript
// components/__tests__/TodoList.spec.ts
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import TodoList from '../TodoList.vue'

describe('TodoList', () => {
  it('renders todo items', () => {
    const wrapper = mount(TodoList, {
      props: {
        items: [
          { id: '1', text: 'Write tests', done: false },
          { id: '2', text: 'Ship feature', done: true },
        ],
      },
    })

    const items = wrapper.findAll('[data-testid="todo-item"]')
    expect(items).toHaveLength(2)
    expect(items[0].text()).toContain('Write tests')
  })

  it('emits remove event when delete is clicked', async () => {
    const wrapper = mount(TodoList, {
      props: {
        items: [{ id: '1', text: 'Test item', done: false }],
      },
    })

    await wrapper.find('[data-testid="delete-btn"]').trigger('click')

    expect(wrapper.emitted('remove')).toBeTruthy()
    expect(wrapper.emitted('remove')![0]).toEqual(['1'])
  })

  it('applies completed class to done items', () => {
    const wrapper = mount(TodoList, {
      props: {
        items: [{ id: '1', text: 'Done task', done: true }],
      },
    })

    expect(wrapper.find('[data-testid="todo-item"]').classes()).toContain('completed')
  })
})
```

### Testing with Plugins and Global Dependencies

```typescript
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createI18n } from 'vue-i18n'
import UserProfile from '../UserProfile.vue'

function mountWithPlugins(component: any, options = {}) {
  return mount(component, {
    global: {
      plugins: [
        createTestingPinia({
          initialState: { auth: { user: { name: 'Test User' } } },
          createSpy: vi.fn,
        }),
        createI18n({ locale: 'en', messages: { en: { greeting: 'Hello' } } }),
      ],
      stubs: {
        RouterLink: true,
        teleport: true,
      },
    },
    ...options,
  })
}

it('displays user name from store', () => {
  const wrapper = mountWithPlugins(UserProfile)
  expect(wrapper.text()).toContain('Test User')
})
```

### Testing Composables

```typescript
// composables/__tests__/useCounter.spec.ts
import { describe, it, expect } from 'vitest'
import { useCounter } from '../useCounter'

describe('useCounter', () => {
  it('increments and decrements', () => {
    const { count, increment, decrement } = useCounter(10)

    expect(count.value).toBe(10)

    increment()
    expect(count.value).toBe(11)

    decrement()
    expect(count.value).toBe(10)
  })
})
```

For composables that require a component context (using `provide/inject`, lifecycle hooks, or `getCurrentInstance`), wrap them in a test component:

```typescript
import { mount } from '@vue/test-utils'
import { defineComponent, h } from 'vue'
import { useAuth } from '../useAuth'

function withSetup<T>(composable: () => T) {
  let result!: T
  const TestComponent = defineComponent({
    setup() {
      result = composable()
      return () => h('div')
    },
  })
  const wrapper = mount(TestComponent)
  return { result, wrapper }
}

it('provides authentication state', () => {
  const { result } = withSetup(() => useAuth())
  expect(result.isAuthenticated.value).toBe(false)
})
```

### Snapshot Testing

Use sparingly for stable, presentational components.

```typescript
it('matches snapshot', () => {
  const wrapper = mount(AppBadge, {
    props: { label: 'New', variant: 'success' },
  })
  expect(wrapper.html()).toMatchSnapshot()
})
```

### Anti-patterns

- Testing implementation details (internal ref values, private methods) instead of rendered output and emitted events.
- Mounting the entire app tree for unit tests -- use `shallowMount` or stub heavy children.
- Not using `@pinia/testing` -- testing with a real Pinia store makes tests depend on global state.
- Skipping `await nextTick()` or `await flushPromises()` after state changes -- assertions run before the DOM updates.
- Over-relying on snapshot tests -- they break on every markup change and rarely catch logic bugs.

---

## Migration and Performance

### Options API to Composition API Migration

Migrate incrementally. Both APIs work in the same component during transition.

| Options API | Composition API Equivalent |
|---|---|
| `data()` | `ref()` / `reactive()` |
| `computed: {}` | `computed()` |
| `methods: {}` | Plain functions |
| `watch: {}` | `watch()` / `watchEffect()` |
| `mounted()` etc. | `onMounted()` etc. |
| `this.$emit()` | `emit()` from `defineEmits` |
| `mixins` | Composables |
| `provide / inject` | `provide()` / `inject()` |

Step-by-step migration for a single component:

```vue
<!-- BEFORE: Options API -->
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: { userId: { type: String, required: true } },
  data() {
    return { user: null as User | null, loading: false }
  },
  computed: {
    displayName(): string {
      return this.user?.name ?? 'Unknown'
    },
  },
  watch: {
    userId: {
      immediate: true,
      async handler(newId: string) {
        this.loading = true
        this.user = await fetchUser(newId)
        this.loading = false
      },
    },
  },
})
</script>
```

```vue
<!-- AFTER: Composition API -->
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{ userId: string }>()

const user = ref<User | null>(null)
const loading = ref(false)

const displayName = computed(() => user.value?.name ?? 'Unknown')

watch(() => props.userId, async (newId) => {
  loading.value = true
  user.value = await fetchUser(newId)
  loading.value = false
}, { immediate: true })
</script>
```

### Mixin to Composable Migration

```typescript
// BEFORE: mixin (Options API)
export const paginationMixin = {
  data() {
    return { page: 1, pageSize: 20, total: 0 }
  },
  computed: {
    totalPages() { return Math.ceil(this.total / this.pageSize) },
  },
  methods: {
    nextPage() { if (this.page < this.totalPages) this.page++ },
    prevPage() { if (this.page > 1) this.page-- },
  },
}

// AFTER: composable (Composition API)
export function usePagination(pageSize = 20) {
  const page = ref(1)
  const total = ref(0)

  const totalPages = computed(() => Math.ceil(total.value / pageSize))
  function nextPage() { if (page.value < totalPages.value) page.value++ }
  function prevPage() { if (page.value > 1) page.value-- }

  return { page, total, totalPages, pageSize, nextPage, prevPage }
}
```

### Vue 2 to Vue 3 Migration

Key breaking changes to address:

| Vue 2 | Vue 3 | Action |
|---|---|---|
| `new Vue()` | `createApp()` | Replace global Vue instance |
| `Vue.component()` | `app.component()` | Scope to app instance |
| `Vue.directive()` | `app.directive()` | Scope to app instance |
| `Vue.filter()` | Removed | Use computed or methods |
| `$on`, `$off`, `$once` | Removed | Use external event bus (mitt) |
| `Vue.set()`, `Vue.delete()` | Not needed | Proxy handles additions/deletions |
| `.sync` modifier | `v-model:propName` | Update template syntax |
| `.native` modifier | Removed | All events are native by default |
| `$children` | Removed | Use refs or provide/inject |
| `$listeners` | Merged into `$attrs` | Update attribute forwarding |

Use the official migration build (`@vue/compat`) for gradual migration:

```typescript
// vue.config.js or vite.config.ts
export default {
  resolve: {
    alias: {
      vue: '@vue/compat',
    },
  },
}
```

### Performance Optimization

#### Virtual Scrolling for Large Lists

```vue
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core'

const { list, containerProps, wrapperProps } = useVirtualList(
  allItems, // ref with thousands of items
  { itemHeight: 48, overscan: 10 }
)
</script>

<template>
  <div v-bind="containerProps" style="height: 600px; overflow-y: auto">
    <div v-bind="wrapperProps">
      <div v-for="{ data, index } in list" :key="index" style="height: 48px">
        {{ data.name }}
      </div>
    </div>
  </div>
</template>
```

#### v-once, v-memo, and Computed Caching

```vue
<template>
  <!-- v-once: render once, never update -->
  <footer v-once>
    <p>&copy; {{ year }} Company Inc.</p>
  </footer>

  <!-- v-memo: skip re-render unless dependencies change -->
  <div v-for="item in list" :key="item.id" v-memo="[item.id, item.selected]">
    <ExpensiveComponent :item="item" />
  </div>
</template>
```

#### KeepAlive for Route Caching

```vue
<template>
  <RouterView v-slot="{ Component }">
    <KeepAlive :include="['DashboardPage', 'SettingsPage']" :max="5">
      <component :is="Component" />
    </KeepAlive>
  </RouterView>
</template>
```

#### Bundle Size Analysis

```bash
# Vite
npx vite-bundle-visualizer

# Nuxt
npx nuxi analyze
```

#### Tree Shaking

Vue 3 is fully tree-shakable. Unused features (Transition, KeepAlive, Teleport, Suspense) are eliminated from production builds when not imported. Third-party libraries should be evaluated for tree-shaking support.

```typescript
// Named imports enable tree shaking
import { ref, computed, watch } from 'vue'

// Avoid importing entire libraries
// BAD:  import _ from 'lodash'
// GOOD: import debounce from 'lodash-es/debounce'
```

### Anti-patterns

- Migrating an entire codebase at once -- convert one component at a time, starting with leaf components.
- Using `@vue/compat` permanently -- it adds bundle size and hides deprecation warnings. Treat it as a temporary bridge.
- Adding `v-memo` everywhere -- it has overhead and only helps when re-renders are measurably expensive.
- Ignoring `defineAsyncComponent` for heavy components -- eager loading everything defeats code splitting.
- Not profiling before optimizing -- use Vue DevTools performance tab to identify actual bottlenecks.
