---
name: vue-3-5
description: Write, review and port Vue 3.5 components and composables (vue@3.5.x, checked against 3.5.44). Covers reactive props destructure and the destructured-prop-passed-as-a-value trap, composables taking MaybeRefOrGetter with toValue() inside an effect, watch semantics (shallow ref watching, numeric deep, once, pause/resume, onWatcherCleanup before the first await, effectScope cleanup), defineModel (local mode without v-model, custom modifiers, factory defaults, never push into a model array), declared emits and listener fallthrough, $attrs, useTemplateRef, defineExpose, useId with app.config.idPrefix for SSR hydration, provide/inject, and testing with Vitest and @vue/test-utils. Use when code imports vue or has .vue files, when writing a composable, a v-model component or SSR code, when props do not update, hydration mismatches appear or events fire twice, and when porting Vue 2 idioms such as value/input v-model, .sync, $listeners, this.$set, filters or beforeDestroy.
license: MIT
---

# Vue 3.5

Vue 3.5 is the current minor (`vue@3.5.44`, November 2026; 3.6 is still a release candidate). Much
of the Vue code on the web and in training data is Vue 2 or Vue 3.0-3.3, and many of those idioms
still compile on 3.5 while doing nothing. Everything below was run against vue 3.5.44 with
@vitejs/plugin-vue 6, Vitest 5 and @vue/test-utils 2.5.

## 1. Know which Vue you are writing

```sh
npm ls vue @vue/compiler-sfc
```

The two versions must match: @vitejs/plugin-vue compiles with the project's `@vue/compiler-sfc`.

| Installed | Write |
| --- | --- |
| `vue@3.5.x` | `<script setup lang="ts">`, destructured props, `defineModel`, `useTemplateRef`, `useId`, `onWatcherCleanup` |
| `vue@3.4.x` | same, but destructured props are **not** reactive, and no `useTemplateRef`/`useId`/`onWatcherCleanup` |
| `vue@3.3.x` or older | no `defineModel` (3.4), no `toValue`/`MaybeRefOrGetter` before 3.3 |
| `vue@2.7` | Vue 2 semantics with a composition API backport; nothing in section 9 applies |

Vue 2 reached end of life on 2023-12-31. Options API components still work in Vue 3, but the Vue 2
instance API they lean on (`$listeners`, `$set`, `$on`, `$children`, `$scopedSlots`,
`beforeDestroy`) is gone. Section 9 lists what fails silently.

## 2. Props: reactive destructure and the value trap

In 3.5 the SFC compiler rewrites every use of a destructured prop to `__props.x`, so this is reactive
in templates, `computed`, `watchEffect` and watch getters:

```ts
const { city, units = 'metric', tags = [] } = defineProps<{
  city: string
  units?: 'metric' | 'imperial'
  tags?: string[]
}>()
const title = computed(() => `${city} (${units})`) // tracks both props
```

- Defaults use native syntax; object and array defaults are compiled into factories for you, so
  `tags = []` is not shared between instances. `withDefaults` is no longer needed.
- **Passing a destructured prop to a function passes its current value.** `useForecast(city)`
  compiles to `useForecast(__props.city)`: a plain string, frozen at setup time. No warning. Pass a
  getter: `useForecast(() => city)`. The same holds for `props.city`; use `() => props.city` or
  `toRef(props, 'city')`.
- `watch(city, ...)` and `toRef(city)` are compile errors ("is a destructured prop and should not
  be passed directly to watch()"). Write `watch(() => city, ...)`.
- Destructured props are readonly; assigning to one is a compile error. Copy into a `ref` if the
  component needs local state seeded from a prop, or use `defineModel`.
- `defineModel()` options are hoisted out of `setup()`, so `defineModel({ default: city })` is a
  compile error (since 3.5.44): use `default: (props) => props.city`.
- Same rules for `provide`: `provide(UnitsKey, units)` provides a frozen string. Provide
  `computed(() => units)` or `toRef(() => units)`.

## 3. Composables

```ts
import { type MaybeRefOrGetter, onWatcherCleanup, ref, shallowRef, toValue, watch } from 'vue'

export function useForecast(city: MaybeRefOrGetter<string>, { refreshMs = 60_000 } = {}) {
  const data = shallowRef<Forecast | null>(null)
  const error = shallowRef<unknown>(null)
  const loading = ref(false)

  watch(
    () => toValue(city), // read inside the getter so refs, getters and computeds are tracked
    (name) => {
      const controller = new AbortController()
      const load = async () => {
        loading.value = true
        try {
          const result = await getForecast(name, { signal: controller.signal })
          if (!controller.signal.aborted) [data.value, error.value] = [result, null]
        } catch (err) {
          if (!controller.signal.aborted) error.value = err
        } finally {
          if (!controller.signal.aborted) loading.value = false
        }
      }
      data.value = null
      void load()
      const timer = setInterval(load, refreshMs)
      // Synchronous, before any await. Runs when `city` changes and when the scope stops.
      onWatcherCleanup(() => {
        controller.abort()
        clearInterval(timer)
      })
    },
    { immediate: true },
  )
  return { data, error, loading } // refs, so callers can destructure
}
```

Rules:

1. Accept `MaybeRefOrGetter<T>` and call `toValue()` **inside** a `watch` getter, `watchEffect` or
   `computed`. Calling `toValue(city)` once at the top of the composable reads it once.
2. Return an object of refs, not a `reactive()`: callers destructure it.
3. Clean up with `onWatcherCleanup` (3.5), the `onCleanup` callback argument, or `onScopeDispose`.
   Not `onUnmounted`: Pinia setup stores and code run inside `effectScope()` have no component
   instance, so lifecycle hooks warn and never run there. Watchers created synchronously in a scope
   are stopped with it, and stopping runs their pending cleanup.
4. `onWatcherCleanup` must run during the synchronous part of the callback. After an `await` it
   warns "no active watcher" and the cleanup is never registered (no abort, timer leaks). The
   `onCleanup` argument (`watch(src, (v, old, onCleanup) => …)`) has no such limit.
5. Guard async results: an aborted or superseded request must not write state. Check the signal
   (or a local `cancelled` flag set in cleanup) after every `await`.
6. Create watchers synchronously in `setup()` or the composable. A watcher created after an
   `await` is not owned by the component and must be stopped by hand.

`toRef(() => x)` gives a readonly ref from a getter (3.3+); `toRefs(reactiveObj)` keeps the
properties of a `reactive` reactive after destructuring.

## 4. Watchers

| Source | Fires on |
| --- | --- |
| `watch(someRef, cb)` | `.value` replaced. **Not** on `someRef.value.push()` |
| `watch(someRef, cb, { deep: true })` | any nested change |
| `watch(reactiveObj, cb)` | any nested change (implicitly deep) |
| `watch(() => state.items, cb)` | `state.items` replaced; not on `push` unless `deep` |
| `watch(() => state.nested, cb, { deep: 1 })` | changes up to one level inside (3.5) |
| `watch([a, () => b.value], cb)` | either source changes; `cb([newA, newB], [oldA, oldB])` |

- `{ immediate: true }` runs the callback synchronously inside `watch()`. `{ once: true }` (3.4)
  stops after the first run.
- Callbacks are batched and run before the component update (`flush: 'pre'`), also outside
  components: after `x.value = 1`, the callback runs on the next microtask, so tests `await nextTick()`.
  `flush: 'post'` sees the updated DOM; `flush: 'sync'` runs on every mutation (avoid on arrays).
- `watch()` returns a handle: `stop()`, and since 3.5 `pause()` / `resume()`. A change while paused
  fires once on `resume()`.
- `shallowRef` only tracks `.value`; after `list.value.push(x)` call `triggerRef(list)` or
  assign a new array. Prefer assigning.

More (watchEffect tracking across `await`, `getCurrentWatcher`, `effectScope` recipes) in
[the reactivity reference](references/reactivity-and-watchers.md).

## 5. v-model on components: defineModel

```ts
// <ChipEditor v-model="chips" /> and <ChipEditor v-model.uppercase="codes" />
const [chips, modifiers] = defineModel<readonly string[], 'uppercase'>({ default: () => [] })

function add(raw: string) {
  const chip = modifiers.uppercase ? raw.trim().toUpperCase() : raw.trim()
  if (chip && !chips.value.includes(chip)) chips.value = [...chips.value, chip] // new array
}
```

- `defineModel()` declares the `modelValue` prop and the `update:modelValue` emit;
  `defineModel('title')` pairs with `v-model:title` (the Vue 3 replacement for `.sync`). Parents
  using `:value` + `@input` (Vue 2) bind nothing.
- **Local mode.** When the parent does not pass both the prop and its `onUpdate:` listener (no
  `v-model`, or only `@update:model-value`), assigning `model.value` updates a local value **and**
  emits. With a manual `modelValue` prop + `emit`, such a component renders nothing new, because
  the prop never changes.
- **Never mutate a model in place.** `chips.value.push(x)` or `splice` writes into the parent's
  array without emitting: it throws on frozen or readonly state, does not re-render when the array
  is not reactive, and with a non-factory default it writes into a default shared by every
  instance. Always assign a new array or object.
- Array or object defaults must be factories: `{ default: () => [] }`. `defineModel` does not
  wrap them for you (destructured props do).
- Modifiers: `v-model.foo` arrives as `modifiers.foo` (or the `modelModifiers` / `titleModifiers`
  prop without `defineModel`). Built-in `.trim` and `.number` are applied by Vue to string payloads
  of `update:*` events automatically; custom ones are yours, usually in the `set` transform:
  `defineModel({ set: (v) => (modifiers.lowercase ? v.toLowerCase() : v) })`.
- A `default` on a model the parent leaves `undefined` desynchronises: the child shows the default,
  the parent holds `undefined`. Prefer `required: true` or a parent-side initial value.

Details, the manual equivalent and edge cases in
[the components reference](references/components-and-v-model.md).

## 6. Events and attributes

- **Declare every event you emit** (`defineEmits` or `emits`). An undeclared event's listener is a
  fallthrough attribute, so `@click` on a component that emits `click` from a root `<button>` runs
  **twice** per click (native listener plus the emit). Vue 2's `.native` modifier is gone.
- `$attrs` holds every undeclared attribute **and listener**, including `class` and `style`.
  `$listeners` no longer exists. With `inheritAttrs: false` (`defineOptions({ inheritAttrs: false })`),
  `v-bind="$attrs"` on an inner element moves class, style and listeners there.
- Type emits with the tuple syntax: `defineEmits<{ change: [id: number]; close: [] }>()`.
- Component events do not bubble. Listen on the component that emits them, or use provide/inject.

## 7. Template refs, exposure and ids

- `const field = useTemplateRef<HTMLInputElement>('field')` with `<input ref="field">` (3.5). The old
  `const field = ref(null)` named like the ref attribute still works.
- Inside `v-for`, the ref holds an **array**, and its order is not guaranteed to match the source.
- `<script setup>` components are closed: a parent ref sees nothing unless the child calls
  `defineExpose({ focus })`.
- **SSR-stable ids: `useId()`.** Module-level counters, `Math.random()`, `crypto.randomUUID()` and
  `getCurrentInstance().uid` produce different ids on the server (a long-lived process that has
  rendered other requests) and in the browser, so hydration logs attribute mismatches. Attribute
  mismatches are never patched: the DOM keeps the server's ids while client code uses its own.
  `useId()` derives ids from the component tree: stable across requests, concurrent renders and
  hydration, unique per instance. Call it in `setup`, not inside `computed`.
- `useId()` is unique per app. Two apps on one page (a header widget and the main app) both start at
  `v-0`: set `app.config.idPrefix` in the app factory used by both server and client. On 3.5.44 the
  id is `${idPrefix}-${n}` (the docs still show a colon separator, which changed in 3.5.3).
- For content that legitimately differs (timestamps, `Date.now()`), mark the element with
  `data-allow-mismatch="text"` (or `attribute`, `children`, `class`, `style`) instead of silencing
  all warnings.

## 8. provide/inject

```ts
export const UnitsKey: InjectionKey<Readonly<Ref<Units>>> = Symbol('units')

// provider: a ref or computed, never `.value` or a destructured prop
const units = ref<Units>('metric')
provide(UnitsKey, readonly(units))

// consumer: third argument `true` treats the default as a factory
const current = inject(UnitsKey, () => readonly(ref<Units>('metric')), true)
```

`app.provide(key, value)` makes something available to every component of that app, which is how to
give each app its own instance of shared state. Since 3.5.25 `provide()` after mount warns.

## 9. Vue 2 and early Vue 3 habits

| Habit | Vue 3.5 | If you keep it |
| --- | --- | --- |
| `props: ['value']` + `$emit('input')` | `defineModel()` / `modelValue` + `update:modelValue` | `v-model` binds nothing |
| `:title.sync="t"` | `v-model:title="t"` | **silently one-way**: `.sync` is dropped, `update:title` goes nowhere |
| `this.value.push(x)` on a prop | emit a new array | mutates parent state, no event, throws on frozen data |
| `v-on="$listeners"` | `v-bind="$attrs"` | `$listeners` is `undefined` |
| `@click.native` | plain `@click` (falls through to the root unless the child declares `click`) | modifier silently dropped |
| emitting without `emits` | declare it | listener runs twice for native event names |
| `this.$set(obj, k, v)`, `Vue.set` | `obj[k] = v` | `TypeError` |
| `this.$on/$off/$once` event bus | callback props, provide/inject or a tiny emitter | `TypeError` |
| `beforeDestroy` / `destroyed` | `beforeUnmount` / `unmounted` | **silently never called** (leaks) |
| `{{ price \| currency }}` filters | a function or computed: `{{ currency(price) }}` | **compiles as bitwise OR**, renders a number |
| `v-if` and `v-for` on one element | `v-if` now runs first: wrap with `<template v-for>` or filter in a computed | `TypeError` on the loop variable |
| `<template v-for>` with keys on children | key on the `<template>` | compile error |
| `$children`, `$scopedSlots` | template refs; `$slots` (functions) | `undefined` |
| `v-enter` / `v-leave` transition classes | `v-enter-from` / `v-leave-from` | the start state is never applied, no animation |
| `const { x } = defineProps()` "is not reactive" (3.4) | reactive in 3.5; still wrap in a getter when passing it on | stale reasoning, extra code |
| `const el = ref(null)` matched by name | `useTemplateRef('name')` | still works |
| `Math.random()` ids | `useId()` | hydration mismatches |

Port behaviour, not just syntax: after porting, check events fire once, `class` lands on the
right element, cleanup hooks run, and transitions still play. Full list in
[the Vue 2 and early Vue 3 reference](references/vue-2-and-early-3-habits.md).

## 10. Testing with Vitest and @vue/test-utils 2

```sh
./node_modules/.bin/vitest run
./node_modules/.bin/vue-tsc --noEmit
```

Vitest runs Vue's development build, so `[Vue warn]` messages and hydration details are visible.
vue-tsc checks types only: a destructured prop passed as a value type-checks fine.

- `mount(Comp, { props, slots, attrs, global: { provide, plugins, stubs } })`. Vue 2-era
  `propsData`, `scopedSlots`, `wrapper.destroy()` and `createLocalVue` are gone (`unmount()`).
- v-model round trip without a parent:
  `mount(Comp, { props: { modelValue: x, 'onUpdate:modelValue': (v) => wrapper.setProps({ modelValue: v }) } })`.
  Test local mode separately by mounting with only the listener.
- `await wrapper.setProps(...)`, `await trigger(...)`, then `await flushPromises()` for async work.
- Composables: run them inside `effectScope()` and call `scope.stop()` to assert cleanup; for
  lifecycle-dependent ones, mount a tiny host component.
- Fake timers: `vi.useFakeTimers()` and `await vi.advanceTimersByTimeAsync(ms)`, which also flushes
  promise callbacks between timers.
- Hydration: `renderToString(createSSRApp(App))`, put the HTML in a container, mount a second
  `createSSRApp(App)` on it with `app.config.warnHandler` collecting warnings, and assert there are
  none. Render twice first to catch module-level counters.

More recipes in [the testing reference](references/testing.md).

## 11. Anti-patterns

| Don't | Do |
| --- | --- |
| `useThing(city)` with a destructured prop | `useThing(() => city)` |
| `const v = toValue(src)` at the top of a composable | `toValue(src)` inside `watch`/`computed` |
| `onWatcherCleanup` after `await` | register it first, or use the `onCleanup` argument |
| `onUnmounted` in a reusable composable | `onScopeDispose` or watcher cleanup |
| `model.value.push(x)` | `model.value = [...model.value, x]` |
| `defineModel({ default: [] })` | `defineModel({ default: () => [] })` |
| manual `modelValue` prop for a component also used without v-model | `defineModel` (local mode) |
| emitting `click` without declaring it | `defineEmits<{ click: [] }>()` |
| `let n = 0` id counters, `Math.random()` ids | `useId()`, plus `app.config.idPrefix` per app |
| `watch(listRef, cb)` expecting `push` to fire | `{ deep: true }`, or replace the array |
| `provide(key, props.x)` | `provide(key, toRef(() => props.x))` |

## References

- [Reactivity, watchers, effect scopes and composables](references/reactivity-and-watchers.md)
- [Components: props, defineModel, emits, attrs, slots, refs, ids and SSR](references/components-and-v-model.md)
- [Vue 2 and early Vue 3 habits, with what each one does on 3.5](references/vue-2-and-early-3-habits.md)
- [Testing with Vitest, @vue/test-utils and SSR hydration](references/testing.md)
- [Sources checked](references/sources.md)
