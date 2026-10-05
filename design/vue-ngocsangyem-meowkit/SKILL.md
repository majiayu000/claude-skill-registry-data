---
name: mk:vue
version: 1.0.0
description: |
  Use when writing, reviewing, or refactoring Vue 3 code — components, composables,
  reactivity, Pinia state, Pinia Colada data-fetching, file-based routing, and forms.
  Targets Composition API + <script setup> + TypeScript. Auto-activates on .vue files.
  For deep best-practices review/recommendations or the full ordered workflow (built-in
  components, animations, performance pass), use mk:vue-best-practices.
allowed-tools:
  - Read
  - Grep
  - Glob
keywords:
  - vue
  - composition-api
  - script-setup
  - pinia
  - pinia-colada
  - composables
  - file-based-routing
  - definemodel
  - script-setup-macros
  - generic-components
  - vue-3-5
  - framework-specific
when_to_use: Use when writing/reviewing/refactoring Vue 3 (components, composables, reactivity, Pinia, Pinia Colada, routing). Auto-activates on .vue files. NOT for deep best-practices review/recommendations or the ordered best-practices workflow (see mk:vue-best-practices), generic TypeScript (see mk:typescript), React (see mk:react-patterns), or Angular (see mk:angular).
user-invocable: true
owner: utility
criticality: medium
status: active
runtime: claude-code
---

# Vue 3

Vue 3 patterns — Composition API + `<script setup lang="ts">`, Pinia, Pinia
Colada, file-based routing, and performance. Single entrypoint routing to focused references.

> Use `npx chub search vue` for relevant documentation packages within the Context Hub.

## When to Use

**Auto-activate on:** `.vue` files, Vue 3 Composition API, `<script setup>`, Pinia stores,
Pinia Colada queries/mutations, Vue Router file-based routes, composables.

**Explicit:** `/mk:vue [concern]`

**Deep best practices:** for a thorough best-practices **review/recommendations** pass or the
full ordered workflow — built-in components (Teleport/Suspense/KeepAlive/Transition),
animation techniques, optional features, and the performance pass — use `mk:vue-best-practices`.
This skill stays the everyday quick-reference.

**Do NOT invoke for:** deep best-practices review/workflow (use `mk:vue-best-practices`),
TypeScript fundamentals (use `mk:typescript`), React (use `mk:react-patterns`), Angular (use
`mk:angular`), visual design (use `mk:frontend-design`), testing (use `mk:testing` / `mk:qa`;
Vue test design/review → `mk:vue-testing-best-practices`).

## Core Rules (always apply)

Follow the repository's established conventions first. When it has no convention, use
these defaults; project requirements may override them. Everything else is in the references.

- **`<script setup lang="ts">` only** — never Options API, never `defineComponent()` wrapper.
- **`type` over `interface`** for defining object/prop shapes; keep types alongside the code.
- **Arrow functions for methods and callbacks.**
- **Named exports over default exports — except composables, which use `export default`.**
- **PascalCase component names, kebab-case file names** (`UserProfile` in
  `user-profile.vue`); composables are `camelCase` with `use` prefix (`useAuth`).
- **Name general → specific:** `SearchButtonClear.vue`, not `ClearSearchButton.vue`.
- **TailwindCSS classes, not manual CSS;** never hard-code colors — use the Tailwind color system.
- **Comments explain _why_, not _what_.**
- **`ref()` for primitives, `reactive()` only for complex objects;** `computed()` for derived state.
- **Never `v-html` with user-provided content** — XSS vector (see `mk:` security rules).

## Data Layer (conditional default)

When the project depends on `@pinia/colada`, it is the **preferred async/data-fetching layer**
— see `references/pinia-colada.md`. Otherwise use plain Pinia stores + composables for state.
Pinia stores hold global UI/app state; data fetching belongs in Pinia Colada when present.

## When to Read Each Reference

Read one level deep from this file. Read multiple when a task spans topics.

| Task involves                                                          | Read                                   |
| ---------------------------------------------------------------------- | -------------------------------------- |
| Components, props/emits, slots, `defineModel`, naming, templates       | `references/components.md`             |
| Composables (`use*`), shared reactive logic                            | `references/composables.md`            |
| `ref`/`reactive`/`computed`/`watch`, `toRefs`, performance             | `references/reactivity-performance.md` |
| Global state with Pinia setup stores, `storeToRefs`                    | `references/state-pinia.md`            |
| Pinia Colada core: keys, `defineQueryOptions`, `useQuery`, mutations   | `references/pinia-colada.md`           |
| Optimistic updates, infinite/paginated queries, SSR, cancellation      | `references/pinia-colada-advanced.md`  |
| Pinia Colada plugins (retry, delay, auto-refetch, persister, hooks)    | `references/pinia-colada-plugins.md`   |
| Direct cache access: `getQueryData`/`setQueryData`/`invalidateQueries` | `references/pinia-colada-cache.md`     |
| File-based routing, route groups, params, `definePage`, typed router   | `references/routing-pages.md`          |
| Project stack, structure, commands, conventions, docs research         | `references/project-standards.md`      |
| 3.4/3.5 core APIs: `useId`, `nextTick`, flush timing, `watch` once/deep, `onWatcherCleanup` | `references/core-new-apis.md`          |
| `<script setup>` compiler macros — `defineOptions`, `withDefaults`, generic components       | `references/script-setup-macros.md`    |
| Advanced reactivity: `effectScope`, `customRef`, `triggerRef`, `markRaw`, `shallowReadonly`  | `references/advanced-patterns.md`      |

## Gotchas

- **Destructuring `reactive()` loses reactivity** — `const { count } = reactive({ count: 0 })`
  makes `count` a plain number; keep the reactive object intact, or use `toRefs()`, or `ref()`.
- **`storeToRefs()` required when destructuring Pinia state** — `const { user } = useAuthStore()`
  gives a non-reactive snapshot; use `const { user } = storeToRefs(useAuthStore())`. Methods
  are destructured directly from the store (not through `storeToRefs`).
- **Parent `ref` access needs `defineExpose()`** — `childRef.value.method()` returns `undefined`
  unless the child `<script setup>` explicitly `defineExpose({ method })`.
- **Use `:slotted()` not `:deep()` for slotted content** — slot content comes from the parent
  scope, so `:deep(.child-class)` in a scoped style block does not match it; use `:slotted(.child-class)`.
- **`watchEffect` cleanup race on fast re-renders** — register cleanup to cancel async work:
  `watchEffect((onCleanup) => { onCleanup(() => controller.abort()) })`, or a fast prop change
  starts a second effect before the first resolves and writes stale state.
- **Pinia store not hydrated in SSR** — calling `useMyStore()` outside a component setup context
  (e.g. a top-level module) creates an instance disconnected from the SSR app; call stores inside
  `setup()` or pass the `pinia` instance explicitly: `useMyStore(pinia)`.
- **Query keys must depend on ALL variables used in the query function** — a key that omits a
  variable serves stale cached data when that variable changes (Pinia Colada).
- **Dynamic query keys need a getter, not a plain value** — pass `key: () => [...]` so the key
  re-evaluates reactively; a plain array snapshot never updates.
- **Prefer `refresh()` over `refetch()`** — `refresh()` reuses in-flight requests and respects
  `staleTime`; `refetch()` always forces a new fetch.
- **Avoid `index.vue` route files** — use a named group like `pages/(home).vue` for a meaningful
  route name.
- **Use explicit route param names** — `userId` not `id`, `postSlug` not `slug`, for type-safe,
  self-documenting routes.
- **Watching a destructured prop needs a getter** — `const { count } = defineProps()` stays reactive
  in templates, but `watch(count, ...)` watches a snapshot; use `watch(() => count, ...)`
  (`references/core-new-apis.md`).
- **`onWatcherCleanup()` must be called synchronously** — invoking it after an `await` throws, since
  the active-watcher context is gone; use the `onCleanup` callback param for post-await cancellation
  (`references/core-new-apis.md`).

## Anti-Patterns

| Don't                              | Do Instead                       |
| ---------------------------------- | -------------------------------- |
| Options API (`data()`, `methods:`) | Composition API `<script setup>` |
| `this.$store` / Vuex               | Pinia with setup store syntax    |
| Direct store state destructuring   | `storeToRefs(useMyStore())`      |
| `v-html` with dynamic content      | `v-text` or sanitized rendering  |
| `reactive()` for primitives        | `ref()` for primitives           |
| Watchers when computed works       | `computed()` for derived state   |
| Global event bus                   | `provide/inject` or Pinia        |
| `defineComponent()` wrapper        | `<script setup>` directly        |

## Workflow Integration

Auto-activates during Build when a Vue project is detected (`.vue` files, `vue` in
`package.json`). Loaded by the `developer` agent alongside `mk:typescript`.
