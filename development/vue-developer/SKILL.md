---
name: vue-developer
description: Vue 3 + Nuxt 3 development. Composition API, script setup, TypeScript, Pinia, Vue Router, SSR patterns.
stacks:
  - vue
  - nuxt
packages:
  - vue
  - nuxt
  - pinia
  - vuedraggable
  - "@tiptap/vue-3"
  - vue-chartjs
tags:
  - vue
  - nuxt
  - frontend
  - spa
user-invocable: false
references: references/REFERENCE.md
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Building Vue 3 components or Nuxt 3 applications
- Implementing state management with Pinia or routing with Vue Router
- Working with SSR, server routes, or middleware in Nuxt 3
- Debugging reactivity, composables, or TypeScript typing in Vue projects

## Do not use this skill when

- The task is unrelated to Vue or Nuxt
- You need React, Svelte, or another frontend framework

## Purpose

Expert Vue 3 + Nuxt 3 developer. Deep knowledge of the Composition API with `<script setup>`, TypeScript integration, Pinia state management, Vue Router, and Nuxt 3 conventions including auto-imports, data fetching, server routes, and middleware.

## Capabilities

### Vue 3 Core: Script Setup

Always use `<script setup lang="ts">` — it is the recommended syntax for Vue 3 SFCs. It automatically exposes top-level bindings to the template and has better TypeScript support than Options API.

### Reactivity APIs

Use `ref()` for primitives and single values (access with `.value`). Use `reactive()` for plain objects where you want property access without `.value`. Use `computed()` for derived state — it is cached and read-only by default, must be pure. Use `watch()` for side effects with access to old and new values. Use `watchEffect()` for auto-tracking side effects when you don't need the previous value. Use `shallowRef()` for large objects where deep reactivity is expensive. Use `toRefs()` when destructuring a reactive object while preserving reactivity.

Prefer `ref()` over `reactive()` for consistency — it works with primitives and complex values, and `.value` access is explicit. Never destructure a `reactive()` object directly — use `toRefs()` or `storeToRefs()` for Pinia stores.

### Props and Emits

Define props with `defineProps<{ title: string; count?: number }>()`. Use `withDefaults(defineProps<...>(), { count: 0 })` for default values. Define emits with `defineEmits<{ change: [id: number]; update: [value: string] }>()`. Use `defineModel<string>()` for v-model bindings (Vue 3.4+).

### Slots

Type slots with `defineSlots<{ header(props: { title: string }): any; default(): any }>()`. Access slotted content in parent with named templates: `<template #header="{ title }">`. Render slot content in child with `<slot name="header" :title="pageTitle" />`.

### Provide and Inject

Create typed injection keys with `InjectionKey<Type>` from Vue. Use `provide(key, value)` in the providing component. Use `inject(key)` in consumer components — this returns `Type | undefined`. Pass a default value as the second argument to get `Type` without undefined.

### Composables

Composables are the primary code reuse pattern. Name them with `use` prefix in PascalCase (`useCounter`, `useFetch`). Return reactive refs, not unwrapped values. Accept `MaybeRefOrGetter<T>` arguments for reactivity compatibility and use `toValue()` to unwrap them. Handle cleanup in `onUnmounted` or return a cleanup function. Composables must be called synchronously in `setup()` scope — never conditionally.

### Pinia State Management

Use Setup Store syntax (function-based). Define state as refs, getters as computed values, and actions as async functions inside the store definition. Return all state, getters, and actions from the function. Destructure with `storeToRefs(store)` to preserve reactivity. Never mutate store state directly from components — use actions. One store per domain entity.

### Vue Router

Define routes with lazy-loaded components using `() => import('./pages/Page.vue')`. Pass route params as props with `props: true`. Add auth metadata to `meta` and check in `router.beforeEach()`. In components, use `useRoute()` for reactive params and `useRouter()` for programmatic navigation. Access params reactively via `computed(() => route.params.id as string)`.

### Nuxt 3

Nuxt 3 auto-imports Vue APIs (`ref`, `computed`, `watch`, `onMounted`), Nuxt composables (`useFetch`, `useAsyncData`, `useRoute`, `useRouter`, `useState`), all components from `components/`, and all composables from `composables/`. No manual imports needed for these.

Data fetching: `useFetch('/api/path')` for convenience API calls with caching. `useAsyncData('unique-key', () => $fetch(...))` when you need a custom fetching function — always provide a unique key for deduplication. `useLazyFetch` or `{ lazy: true }` for non-critical data that should not block navigation. Use `$fetch` for event-triggered requests (click handlers, form submissions). Call `refresh()` to refetch without a full page reload.

Server routes live in `server/api/`. File name determines the HTTP method: `posts.get.ts`, `posts.post.ts`, `posts/[id].get.ts`. Use `getQuery(event)` for query params, `readBody(event)` for request bodies, `getRouterParam(event, 'id')` for path params.

Middleware in `middleware/` runs on route navigation. Define with `defineNuxtRouteMiddleware()` and redirect with `return navigateTo('/path')`. Apply per-page with `definePageMeta({ middleware: 'auth' })`.

Runtime config: server-only secrets go under `runtimeConfig` (read as `config.secretKey`), public values under `runtimeConfig.public` (read as `config.public.apiBase`). Environment variables map automatically: `NUXT_SECRET_KEY` → `runtimeConfig.secretKey`.

## Behavioral Traits

- Always uses Composition API with `<script setup lang="ts">`, never Options API
- Always uses `storeToRefs()` when destructuring Pinia store state
- Always uses lazy imports for route components (`() => import(...)`)
- Types props and emits with generic syntax, never runtime validators alone
- Uses `computed()` for derived state instead of watchers that assign to refs

## Important Constraints

- NEVER use Options API — always Composition API with `<script setup>`
- NEVER use `this` inside `<script setup>` — it does not exist
- NEVER mutate props — emit events or use `defineModel()`
- NEVER use index as `:key` in `v-for` — use unique IDs
- NEVER destructure `reactive()` directly without `toRefs()` — loses reactivity
- NEVER mix Pinia Options syntax and Setup syntax in the same project
- ALWAYS use `() => import()` for route components — no static imports in routes

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
