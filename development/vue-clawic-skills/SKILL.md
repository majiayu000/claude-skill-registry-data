---
name: Vue
slug: vue
version: 1.0.3
description: 'Builds, debugs, and reviews Vue 3 apps: reactivity, components, composables, Pinia state, Vue Router, forms, and performance. Use when the UI does not update after a state change, a reactive object loses reactivity on destructure or reassignment, .value is forgotten, a watcher never fires or loops ("Maximum recursive updates exceeded"), props or v-model stop syncing, a template ref is null, SSR reports a hydration mismatch, a route param change does not reload the component, Pinia warns "getActivePinia() was called but there was no active Pinia", the console shows "Failed to resolve component" or "Extraneous non-props attributes", a thrown error blanks the page, a long list or large object makes typing lag, a chart or map library breaks after being put in ref(), scoped styles do not reach a child, or when migrating Vue 2 Options API to Composition API and script setup. Not for Nuxt-specific SSR, routing, and data fetching (nuxt), Vite build configuration (vite), or React and Svelte (react, svelte).'
homepage: https://clawic.com/skills/vue
changelog: Display name shown correctly
metadata:
  clawdbot:
    emoji: 💚
    requires:
      bins:
      - node
    os:
    - linux
    - darwin
    - win32
    displayName: Vue
    configPaths:
    - ~/Clawic/data/vue/
    - ~/vue/
    - ~/clawic/vue/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/vue/
      - ~/vue/
      - ~/clawic/vue/
---

User preferences and memory live in `~/Clawic/data/vue/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/vue/` or `~/clawic/vue/`), move it to `~/Clawic/data/vue/`, and say in one line that you moved it and from where.

## When To Use

- Writing or reviewing Vue 3 components, composables, stores, and router configuration
- Debugging: state changes that never reach the DOM, watchers that loop or never fire, null template refs, hydration mismatches, memory leaks, a page that goes blank after an uncaught error
- Choosing between `ref` and `reactive`, computed and watch, props and provide/inject, Pinia and a plain composable
- Performance work: slow lists, laggy typing, oversized bundles, components that re-render on every keystroke
- Migrating Vue 2 / Options API code to Composition API and `<script setup>`
- Not for Nuxt's own layer (auto-imports, `useFetch`, server routes, `<ClientOnly>`) → `nuxt`; Vite plugin and build config → `vite`

## Quick Reference

| Situation | Play |
|---|---|
| State changes, DOM does not | Reactivity was lost or never established — walk the Reactivity Loss table below |
| Forgot `.value` and got a Ref object in a log | `.value` in script, auto-unwrapped in template — but NOT inside arrays or Map/Set (`arr[0].value`) |
| `state = {...}` stopped working | `reactive` cannot be reassigned; use `ref` and set `.value`, or `Object.assign(state, next)` |
| Destructuring killed reactivity | `toRefs(state)`, `storeToRefs(store)`, or pass `() => state.x` — props destructure is safe only on `vue >=3.5` |
| "Maximum recursive updates exceeded" | A watcher or computed mutates its own dependency → `debug.md` Infinite Loops |
| Watcher reads stale DOM | Default `flush: 'pre'` runs before render; use `flush: 'post'` or `await nextTick()` (rule 4) |
| Template ref is `null` | Refs bind at mount — read in `onMounted`, not in setup body (`components.md`) |
| Child does not receive updates through `v-model` | `:modelValue` + `@update:modelValue`, or `defineModel()` on `vue >=3.4` (`forms.md`) |
| Route param changes, component does not reload | Vue Router reuses the instance — `watch(() => route.params.id)` (`routing.md`) |
| Chart / map / editor library misbehaves in a `ref` | Deep proxy broke instance identity — `markRaw()` or `shallowRef()` (rule 6) |
| Typing lags, list of thousands re-renders | `shallowRef` + `v-memo` + virtualize above `virtualize_threshold` (`performance.md`) |
| Hydration mismatch after SSR | Non-deterministic render or invalid HTML nesting → `ssr.md` |
| Scoped style does not reach child markup | `:deep()` selector; `>>>` and `::v-deep` are the deprecated spellings (`sfc.md`) |
| `vue-tsc` errors that `tsc` never showed | `.vue` files only type-check through `vue-tsc` (`typescript.md`) |
| Test asserts before the DOM updates | `await nextTick()` / `await flushPromises()`; `trigger()` returns a promise (`testing.md`) |
| Vue 2 code, `$on` / filters / `.sync` gone | All removed in Vue 3 → `migration.md` |
| Page goes blank after a throw, one console error | Nothing catches errors by default — a setup-phase throw unmounts the subtree (`errors.md`) |
| Async component stuck on its loader, or `Failed to fetch dynamically imported module` | `timeout` + `errorComponent` + `onError` retry; a post-deploy chunk miss needs a guarded reload (`errors.md`) |
| Installing something app-wide: helper, component, directive, config | A plugin's `install(app)`; prefer `app.provide` over `globalProperties` (`plugins.md`) |
| Screen reader announces nothing after a route change | Focus stayed on the old page — move it to the new view's heading (`routing.md`) |
| Anything else | Reproduce in an isolated SFC with no props and no store, then add one input at a time until it breaks |

Depth on demand: `debug.md` symptom→cause chains · `reactivity.md` refs, watchers, effect scopes · `components.md` props, emits, slots, built-in components · `composables.md` reusable logic · `templates.md` directives and rendering · `sfc.md` script setup macros and scoped CSS · `state.md` Pinia, Vuex 4, provide/inject · `routing.md` Vue Router · `forms.md` inputs and validation · `errors.md` boundaries, the app error handler, failure states · `plugins.md` `app.use`, global config, registration · `performance.md` render and bundle cost · `ssr.md` hydration · `typescript.md` typing components · `testing.md` Test Utils, Vitest, Jest · `migration.md` Vue 2 to Vue 3 · `security.md` XSS and template injection.

## Core Rules

1. **Pass the source, not the value.** A watcher, computed, or composable receives a ref or a getter (`() => props.id`) — never the already-read value, which is a dead snapshot. Test: if deleting the arrow function still compiles, the reactivity is already gone. This single mistake explains most "my watcher never fires".
2. **`ref` by default; `reactive` only for a bounded object you never reassign.** `reactive` fails four ways — reassignment breaks it, destructuring breaks it, it rejects primitives, and its ref-unwrapping stops inside arrays and Map/Set. `ref` has one cost (`.value`) and no cliffs.
3. **`computed` derives, `watch` acts.** A computed is cached and must be pure: same dependencies in, same value out, zero side effects. The moment you need to fetch, write, or navigate, that is a watcher. A computed with a `fetch` inside runs an unpredictable number of times, because caching decides when it evaluates.
4. **Know the flush phase before you read the DOM.** Watchers default to `flush: 'pre'` (before the component re-renders), so DOM reads see the previous frame. Order: `sync` (immediately, on every mutation) → `pre` (batched, before render) → `post` (after DOM patch). Reading layout or measuring elements requires `post` or `await nextTick()`.
5. **Only what is registered synchronously in setup is cleaned up for you.** Effects, watchers, and lifecycle hooks created before the first `await` are bound to the component's scope and stopped at unmount. Anything created inside a timer, a promise callback, or after `await` leaks — keep the stop handle, or wrap the work in `effectScope()` and dispose it (`reactivity.md`).
6. **`markRaw` or `shallowRef` for every non-plain object.** Class instances (Chart.js, Leaflet, CodeMirror, WebSocket, IndexedDB handles, Web Audio nodes) put in `ref()`/`reactive()` get deep-proxied: the cost is proportional to the object graph, and `instanceof` plus `===` against the raw object start failing because the proxy is not the instance. Vue warns on components stored reactively; for library instances it stays silent and you get "the map went blank".
7. **`:key` is identity, not position.** `:key="index"` on a list that reorders, filters, or splices makes Vue reuse the wrong component instance: the DOM shows row 3's text with row 5's checkbox state. Use a stable ID; use the index only for a list that is append-only and never sorted.
8. **Gate every macro on the installed version.** `defineSlots` and generic components need `vue >=3.3`; `defineModel` needs `vue >=3.4`; `useTemplateRef`, `useId`, `onWatcherCleanup`, and reactive props destructure need `vue >=3.5`. Check `package.json` before recommending one — a macro that does not exist compiles to nothing and fails at runtime with an undefined identifier.

## Console Warnings

Vue's warnings name the cause precisely; treat each as a lookup, not a puzzle. (Production builds strip them — reproduce in dev.)

| Warning | Real cause | Fix |
|---|---|---|
| `Failed to resolve component: X` | Not registered, or a case/typo mismatch between import and tag | Import in `<script setup>` (auto-registers), or check PascalCase vs kebab-case |
| `Extraneous non-props attributes ... could not be automatically inherited` | Component has multiple root nodes, so Vue cannot pick a fallthrough target | Single root, or `defineOptions({ inheritAttrs: false })` + explicit `v-bind="$attrs"` |
| `Maximum recursive updates exceeded` | An effect writes to state it also reads | Isolate the write behind a condition, or derive with `computed` (`debug.md`) |
| `Invalid watch source` | A plain value was passed where a ref/getter belongs | Wrap in `() => ...` (rule 1) |
| `Property "x" was accessed during render but is not defined` | Not returned from `setup()`, or typo; also fires when `<script setup>` and a plain `<script>` disagree | Return it, or declare it in `<script setup>` |
| `Hydration node mismatch` | Server HTML ≠ first client render | `ssr.md` — non-determinism or invalid nesting |
| `inject() can only be used inside setup()` | Called in a callback, after `await`, or in a plain module | Call synchronously at the top of setup and store the result |
| `Set operation on key "x" failed: target is readonly` | Mutating a prop or a `readonly()` proxy | Emit upward, or clone before editing |
| `Vue received a Component that was made a reactive object` | A component definition stored in `ref`/`reactive` | `shallowRef` for dynamic components; `markRaw` for anything class-like (rule 6) |
| `Component provided template option but runtime compilation is not supported` | Runtime-only build plus a string template | Move it to an SFC, or switch to the bundler build with the compiler (`security.md` — it needs `unsafe-eval`) |
| `"getActivePinia()" was called but there was no active Pinia` (Pinia <2.1 worded it `getActivePinia was called with no active Pinia`) | Store used before `app.use(pinia)`, or at module scope | Call the store inside setup or after install (`state.md`) |

## Reactivity Loss

Every "the UI doesn't update" bug is one row of this table. Diagnose by asking what you held onto: the source, or a value read from it.

| You wrote | What you hold | Write instead |
|---|---|---|
| `const { count } = reactive(state)` | A number, frozen at read time | `toRefs(state)`, or `state.count` at the point of use |
| `const { items } = useStore()` (Pinia) | A frozen snapshot of state; actions survive destructuring, state does not | `storeToRefs(store)` for state, plain destructure for actions |
| `state = { ...state, x: 1 }` on a `reactive` | A new unproxied object; the old proxy still feeds the DOM | `Object.assign(state, patch)`, or hold a `ref` and swap `.value` |
| `watch(props.id, ...)` | The current id, a primitive | `watch(() => props.id, ...)` |
| `const first = arr.value[0]` where items are refs | A ref (arrays do not unwrap) | `arr.value[0].value`, or store plain objects |
| `provide('user', user.value)` | A snapshot; injectors never update | `provide('user', user)` — provide the ref itself |
| `const cfg = toRaw(state)` then mutate `cfg` | The raw object; writes bypass tracking | Mutate the proxy; use `toRaw` only to hand data to a non-Vue library |
| `Object.freeze(data)` then `ref(data)` | Frozen data Vue cannot proxy — silently non-reactive | Freeze after rendering, or use `shallowRef` deliberately |
| `const { x } = defineProps()` on `vue <3.5` | A snapshot (the compiler transform only landed in 3.5) | `toRef(props, 'x')`, or upgrade and keep the destructure |

## Component Communication

Pick the narrowest mechanism that reaches the target; every step outward costs traceability.

| From → To | Mechanism | Breaks down when |
|---|---|---|
| Parent → child | Props (`defineProps`) | The chain is 3+ levels — prop drilling; move to provide/inject |
| Child → parent | Emits (`defineEmits`) | You need a return value; then it is a callback prop, not an event |
| Two-way on one value | `defineModel()` (`vue >=3.4`), else `modelValue` + `update:modelValue` | Multiple values — use named models (`v-model:title`) |
| Ancestor → deep descendant | `provide` / `inject` with an `InjectionKey` | Consumers outside that subtree, or you need writes from anywhere → store |
| Parent → child imperative call | Template ref + `defineExpose` | You are reaching in to read state you should have passed down |
| Slot content → slot owner | Scoped slot props | The content needs the owner's lifecycle, not just its data |
| Siblings / any-to-any | Pinia store | It is one screen's local concern — lift state to the common parent instead |
| Across routes | Route params for identity, store for payload | You are stuffing objects in query strings (`routing.md`) |
| Anything else | Pinia store, then narrow it once the shape is known | — |

## Output Gates

Before emitting a component, composable, or store, verify:

- Every reactive source crossing a function boundary is a ref or a getter, never a read value?
- Each `v-for` has a stable identity `:key`, and no `v-if` on the same element?
- Watchers and listeners created outside synchronous setup have a stop handle or an `effectScope`?
- Props treated as read-only; every mutation routed through an emit or a model?
- Any class instance or third-party object wrapped in `markRaw`/`shallowRef`?
- Every macro used exists in the project's Vue version (rule 8)?
- No user-controlled string reaching `v-html`, `:is`, or `:href` (`security.md`)?
- Every async region has a loading, an error, and an empty state, and something above it catches a throw (`errors.md`)?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/vue/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| vue_version | 3.2 \| 3.3 \| 3.4 \| 3.5 \| later | 3.5 | Gates which macros and APIs get recommended (rule 8) and which workarounds appear in examples; 3.2 is the supported floor (`sfc.md`), and `later` means assume everything through 3.5 and check the release notes before using a newer API |
| api_style | script-setup \| setup-function \| options | script-setup | Shapes every code sample and the `migration.md` target style |
| language | ts \| js | ts | Whether examples carry type annotations and whether `typescript.md` guidance is volunteered |
| state_library | pinia \| vuex \| none | pinia | Selects the store patterns in `state.md`; `vuex` switches to its Vuex 4 section (`useStore`, commit/dispatch, namespaced paths); `none` routes shared state to composables and provide/inject |
| rendering_mode | spa \| ssr \| ssg | spa | Turns on SSR-safety review (module-scope state, browser APIs, hydration) from `ssr.md` |
| virtualize_threshold | number (rows) | 200 | Row count above which `performance.md` recommends virtual scrolling instead of `v-memo` |
| test_runner | vitest \| jest \| none | vitest | Shapes the setup and mocking examples in `testing.md`; `jest` swaps `vi.*` for `jest.*` and adds the transform and `transformIgnorePatterns` config that Vitest does not need |

Preference areas to record as the user reveals them:

- **conventions** — `ref` vs `reactive` house style, component and composable naming, SFC block order, feature-folder vs type-folder layout
- **tooling** — build tool, package manager, UI kit, validation and i18n libraries, whether VueUse is welcome or the project prefers hand-rolled composables
- **safety posture** — `v-html` policy, whether to run codemods without confirmation, how loudly to flag missing keys and unbounded watchers
- **output format** — whether components ship with a test, how much explanation accompanies code, comment density
- **platform** — browser support target, CSP strictness (which decides runtime-only vs compiler build), SSR host

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `v-if` and `v-for` on the same element | In Vue 3 `v-if` evaluates first and cannot see the loop variable — "Property 'item' is not defined" (the opposite of Vue 2's precedence) | `<template v-for>` wrapping the `v-if`, or filter in a `computed` |
| `v-html` with anything a user typed | Vue escapes mustaches but never `v-html` — this is the XSS door | Render as text, or sanitize server-side (`security.md`) |
| `watch(obj, ...)` on a reactive object | Vue forces `deep: true` and the callback gets the same object as old and new value | Watch a getter of the field you care about |
| `deep: true` on a large tree | Traversal cost is proportional to the node count, on every mutation | Watch specific getters, or `deep: 2` on `vue >=3.5` |
| Mutating a prop object because "it works" | It does mutate — same reference — but the parent has no record and DevTools shows no source | `defineModel()` or an explicit emit |
| `async setup()` without `<Suspense>` | The component never resolves and renders nothing, silently | Sync setup + a loading ref, or an explicit `<Suspense>` boundary |
| Registering a listener in `onMounted` with no `onUnmounted` | Survives the component; every remount adds another | Pair them, or use a composable that owns the cleanup |
| Module-scope `const state = reactive({})` in SSR | The module is shared across requests — one user's data leaks into another's page | State factory per request (`ssr.md`) |
| `KeepAlive` without `max` | Every visited view stays in memory for the session | `<KeepAlive :max="10">` and `onActivated` for refresh |
| Index as `:key` on a sortable list | Instance reuse mixes rendered content with stale local state | Stable ID (rule 7) |

## Where Experts Disagree

- **`ref` everywhere vs `reactive` for objects.** The `ref`-only camp wins on consistency and on never hitting the reassignment cliff; the `reactive` camp wins on template and script ergonomics for a form-shaped object. Default: `ref`, with `reactive` allowed for an object that is created once and mutated in place. Do not mix styles inside one module.
- **Pinia store vs a shared composable.** A composable holding module-scope refs is a global store with no devtools, no SSR safety, and no plugin surface. Reach for it only for a singleton with no server rendering; anything crossing routes or touched by more than two features belongs in a store (`state.md`).
- **Options API is legacy.** It is supported indefinitely and still the fastest onboarding for a large team; Composition API's real payoff is logic extraction and typing. Boundary: mixins and cross-cutting logic mean migrate; a stable CRUD screen in Options API is not technical debt.
- **VueUse vs hand-rolled composables.** Depending on a 200-utility library for `useLocalStorage` is a genuine cost; reimplementing `useIntersectionObserver` correctly (SSR guard, cleanup, ref-or-value input) is a bigger one. Split on whether the utility touches a browser API lifecycle.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/vue (install if the user confirms):
- `nuxt` — Nuxt's SSR, file routing, data fetching, and server layer
- `vite` — build, dev server, and bundle configuration
- `typescript` — type-system design beyond component typing
- `javascript` — language-level semantics (async, coercion, closures)
- `playwright` — end-to-end tests that a component test cannot cover

## Feedback

- If useful, star it: https://clawic.com/skills/vue
- Latest version: https://clawic.com/skills/vue

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/vue.
