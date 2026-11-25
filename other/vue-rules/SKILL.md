---
name: vue-rules
description: Standing rules for Vue and Nuxt code covering the Composition API, typed props and emits, reactivity pitfalls, composables, stores and server versus client rendering in Nuxt.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: rule
  category: conventions
  source: https://hermes-ide.com/prompts/vue-rules
  catalog: 2026.1014.1
---

# Vue and Nuxt rules

Apply these rules to files matching: `**/*.vue`, `composables/**`, `stores/**`, `server/**`, `nuxt.config.*`, `src/**/*.ts`.

When you write or change Vue or Nuxt code in this project:

**Know the project first**
- Check the Vue (and Nuxt, if present) version in `package.json` and follow the existing style. Some reactivity behaviour, such as whether destructured props stay reactive, depends on the version.

**Components**
- Write single-file components with `<script setup lang="ts">` and the Composition API. Do not add Options API components to a Composition API codebase.
- Declare props with type-based `defineProps<...>()` and defaults through the version's supported mechanism, and emits with typed `defineEmits<...>()`. Use `defineModel` for two-way binding where the version supports it, instead of hand-written prop and emit pairs.
- Never mutate a prop. Emit an event or use a local copy that is explicitly an initial value.
- Give every `v-for` a stable `:key` from the data. Do not put `v-if` and `v-for` on the same element; filter in a computed property or wrap in a `<template>`.

**Reactivity**
- Use `ref` for primitives and values you replace; use `reactive` only for objects you mutate in place and never reassign. Pick one style per file.
- Do not destructure a `reactive` object or a store directly; you lose reactivity. Use `toRefs` or `storeToRefs`.
- Derive values with `computed`, never with a `watch` that copies state into another ref. Use `watch` and `watchEffect` only for side effects, and clean up timers and listeners in `onUnmounted` or the watcher's cleanup.
- Do not store component instances, DOM nodes or large immutable data in deep reactive state; use `shallowRef` or `markRaw`.

**Composables**
- Put reusable stateful logic in composables named `useSomething` that accept refs or getters and return refs. A composable that adds listeners or timers removes them when the calling component unmounts.
- Keep composables free of component-specific DOM assumptions so they also run during server rendering.

**State and stores**
- Keep state local until two distant components need it, then use the project's store (Pinia in most projects). Stores hold state and actions, not UI concerns. Do not access a store at module top level outside a component or composable.

**Templates and security**
- Never bind untrusted content with `v-html`. Sanitise it with an allow-list sanitiser first, or render it as text.
- Use semantic elements, labelled form controls and real buttons for actions.

**Nuxt: server and client rendering**
- Fetch data during setup with `useFetch` or `useAsyncData` so it is fetched once on the server and reused on the client. Use `$fetch` directly only in event handlers and server code; calling it bare in setup fetches twice.
- Give `useAsyncData` a unique, stable key, and handle `pending` and `error` states in the template.
- Avoid hydration mismatches: no `Date.now()`, random values, `window`, `localStorage` or locale-dependent formatting in rendered output on the server. Wrap browser-only components in `<ClientOnly>` and guard browser code with `import.meta.client` or `onMounted`.
- Read configuration through `useRuntimeConfig()`. Only `public` runtime config reaches the browser; keep secrets in the private part and use them only in `server/` routes.
- Put backend endpoints in `server/api` and validate their input like any public API. Use route middleware for navigation guards, and remember client-side guards are not authorisation.

**Tests and checks**
- Test components with Vue Test Utils or Testing Library through user-visible behaviour, and composables as plain functions.
- Before finishing, run the type check (`vue-tsc` or `nuxi typecheck`), lint and tests, and load the page with server rendering to check for hydration warnings in the console.
