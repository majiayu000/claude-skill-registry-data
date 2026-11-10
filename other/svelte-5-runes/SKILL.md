---
name: svelte-5-runes
description: Write, review and migrate Svelte 5 code (svelte@5.x, checked against 5.57.3) with runes - $state, $derived, $effect, $props, $bindable - snippets, callback props, shared state in .svelte.ts modules and the mount/unmount/flushSync API. Covers the Svelte 3/4 habits that break or fail silently in Svelte 5 (export let, $:, on:click, createEventDispatcher, slots, $$restProps, new Component(), $set/$on/$destroy, writable stores), state syncing in $effect, missing $bindable, runes outside .svelte.ts files, Map/Set in $state, proxies rejected by structuredClone/postMessage, deferred onMount and bind:this after mount, and testing with Vitest and jsdom. Use when editing .svelte, .svelte.ts or .svelte.js files, when a project turns on runes mode or upgrades to Svelte 5, when replacing svelte/store with runes, when embedding Svelte components from plain JavaScript, or when a Svelte component stops updating.
license: MIT
---

# Svelte 5 runes

Svelte 5 is the current major (`svelte@5.57.3` as of November 2026). Most Svelte examples on the
web and in model training data are Svelte 3/4. Several Svelte 4 idioms still compile in Svelte 5,
or compile into something that runs and does the wrong thing. Everything below was checked against
svelte 5.57.3 by compiling and running it.

## 1. Know the version and the mode

```sh
node -p "require('svelte/package.json').version"   # or: npm ls svelte
```

Each component compiles in **runes mode** or **legacy mode**. A component is in runes mode if it
uses a rune, if it has `<svelte:options runes />`, or if the compiler option `runes` says so. The
`sv create` template forces runes for the whole project:

```js
// svelte.config.js
export default {
  compilerOptions: {
    runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true),
  },
}
```

In runes mode these are **compile errors**: `export let` (`legacy_export_invalid`), `$:`
(`legacy_reactive_statement_invalid`), `$$props`/`$$restProps` (`legacy_rest_props_invalid`),
`beforeUpdate`/`afterUpdate` (`runes_mode_invalid_import`), and `on:click` together with `onclick`
in one component (`mixed_event_handler_syntaxes`). `on:click`, `<slot>` and `<svelte:component>`
still compile with `*_deprecated` warnings. `createEventDispatcher` compiles without any warning,
but it does not call callback props (section 4).

Legacy components keep working without forced runes, and both kinds can be mixed per component. Port
a component completely; don't leave it half in each syntax.

SvelteKit 3.0 (October 2026) requires `svelte@^5.57.1`, `vite@^8` and
`@sveltejs/vite-plugin-svelte@^7`.

## 2. Svelte 4 habits and what they do in Svelte 5

The dangerous rows are the silent ones: the code compiles and runs, and the result is wrong.

| Svelte 4 habit | Svelte 5 | If you keep the habit |
| --- | --- | --- |
| `export let value` | `let { value } = $props()` | compile error in runes mode |
| `export let value` + parent `bind:value` | `let { value = $bindable() } = $props()` | **silent**: the child updates, the parent's variable never does |
| `$: doubled = n * 2` | `const doubled = $derived(n * 2)` | compile error in runes mode |
| `$: doubled = n * 2` ported as `const doubled = n * 2` | `$derived` | **stale**: computed once (`state_referenced_locally` warning) |
| `$: { total = sum(items) }` ported to `$effect(() => { total = sum(items) })` | `$derived` / `$derived.by` | **stale reads** until the next flush; `effect_orphan` outside components |
| `$derived(() => expr)` | `$derived(expr)` or `$derived.by(() => …)` | **the value is the function**; the template prints its source |
| `createEventDispatcher` + `dispatch('publish', x)` | callback prop `onpublish(x)` | **callback props are never called** |
| parent `on:publish={(e) => f(e.detail)}` | `onpublish={(x) => f(x)}` | no `.detail`; payload is the argument |
| `on:click`, `on:submit\|preventDefault` | `onclick`, `event.preventDefault()` in the handler | deprecated; modifiers don't exist on `onclick` |
| `<slot />`, `<slot name="row" {item} />`, `let:item` | `children` / named snippet props, `{@render row(item)}` | slot content can't be passed to a component that uses `{@render}` |
| `{...$$restProps}` | `let { a, ...rest } = $props()` then `{...rest}` | compile error in runes mode |
| `let set = new Set(); set.add(x); set = set` | `new SvelteSet()` or reassign a new `Set` | **`$state(new Set())`/`Map`/`Date` mutations don't update** |
| plain `let` in a `.js`/`.ts` store module | `$state` in a `.svelte.ts` module | `$state` in plain `.ts` throws `rune_outside_svelte` |
| `export let count` in a module, reassigned | export an object, a class instance or getters | `state_invalid_export` compile error |
| `writable`/`derived` + `get(store)` | class with `$state`/`$derived` fields | stores still work; `$store` syntax only inside components |
| `new App({ target, props })` | `mount(App, { target, props })` | `component_api_invalid_new` at runtime |
| `app.$set({ x })` | mount with a `$state` props object and assign to it | `component_api_changed`; a plain props object never updates |
| `app.$on('publish', cb)` | pass `onpublish: cb` in props | `events` option exists but is deprecated |
| `app.$destroy()` | `unmount(app)` | `component_api_changed` |
| relying on `onMount` having run after `new App()` | `flushSync()` after `mount()` | **`onMount`, `$effect` and `bind:this` have not run yet** |
| `beforeUpdate`/`afterUpdate` | `$effect.pre` / `$effect` (+ `tick`) | compile error in runes mode |
| `<svelte:component this={C} />` | `<C />` (dynamic by default) | deprecated |
| `{@const x = …}` | `{const x = …}` declaration tags (5.56+) | still works, considered legacy |
| `use:action` | `{@attach fn}` (5.29+) | still works; attachments re-run on state changes |
| `class:active={on}` | `class={['btn', { active: on }]}` (5.16+) | still works |

More before/after code, grep patterns and what `sv migrate svelte-5` does and doesn't convert:
[the migration reference](references/migration-svelte-4.md).

## 3. Props

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte'
  import type { HTMLInputAttributes } from 'svelte/elements'

  interface Props extends Omit<HTMLInputAttributes, 'value'> {
    value?: number
    step?: number
    onvaluechange?: (value: number) => void
    label?: Snippet<[number]>
  }

  let { value = $bindable(0), step = 1, onvaluechange, label, ...rest }: Props = $props()
  const uid = $props.id() // stable per instance, consistent between SSR and hydration (5.20+)
</script>
```

- Props are read through accessors: anything computed from a prop must be `$derived`, or it keeps
  the first value.
- **`$bindable()` is opt-in.** Without it, `<Child bind:value={x}>` still compiles and the child can
  reassign its local copy, but `x` in the parent never changes. In 5.57.3 nothing throws.
- With `$bindable(fallback)`, a parent that binds must pass a value that is not `undefined`.
- Reassigning a prop gives the child a local override until the parent passes a new value.
  **Don't mutate props you don't own**: a non-bindable fallback (`items = []`) is not reactive, and
  mutating a parent's `$state` proxy works but warns `ownership_invalid_mutation`. Reassign
  (`items = [...items, x]`), use `$bindable`, or call back to the parent.
- A non-reactive value can *look* reactive: Svelte groups several template expressions into one
  effect, so a stale value repaints when an unrelated value in the same effect changes. Test the
  value on its own.
- `children` is reserved for the default content; don't declare another prop with that name.

## 4. Events are callback props

```svelte
<!-- Stepper.svelte -->
<script lang="ts">
  let { value = $bindable(0), onvaluechange }: { value?: number; onvaluechange?: (v: number) => void } = $props()
  function set(next: number) {
    value = next
    onvaluechange?.(next) // a plain value, not a CustomEvent
  }
</script>
<button onclick={() => set(value - 1)}>−</button>
<button onclick={() => set(value + 1)}>+</button>
```

- `createEventDispatcher` is deprecated. Its dispatch only reaches listeners added with `on:` on
  the component or with `mount(…, { events })`; a parent that passes an `onpublish` prop is never
  called.
- No modifiers: call `event.preventDefault()`/`stopPropagation()` in the handler. Capture phase is
  `onclickcapture`. Passive/non-passive listeners need `addEventListener` (or `on()` from
  `svelte/events`) inside an attachment or action.
- One handler per event: combine them in one function. With spreads, put local handlers after
  `{...rest}` and call `rest.onclick?.(e)` yourself.
- `onclick`, `oninput`, `onkeydown` and other common events are delegated to the app root. Calling
  `stopPropagation()` in a native listener between the element and the root hides the event from
  Svelte handlers. Dispatch synthetic events with `bubbles: true`.
- Window/document listeners: `<svelte:window onkeydown={…} />`, not `addEventListener` in
  `onMount`; Svelte removes them on unmount.

## 5. `$derived` first, `$effect` last

- `$derived(expr)` is lazy and always current: reading it right after a state change returns the
  new value, inside or outside components, without any flush.
- `$derived.by(() => { … })` for multi-statement logic. `let { a, b } = $derived(obj)` keeps every
  name reactive.
- Deriveds are writable since 5.25 (optimistic UI): assigning overrides the value until a
  dependency changes. Declare with `const` when overriding must be impossible.
- `$effect` runs **after** the DOM updates, in a microtask, and only in the browser. Using it to
  copy state into other state gives one stale read per change, extra renders, and loops.
- `$effect` must run inside a component or an `$effect.root`. A class that calls `$effect` in its
  constructor throws `effect_orphan` when it is created in plain code, a test, or at module scope
  (an exported singleton fails at import time).
- Effects are for side effects: DOM work, third-party widgets, subscriptions, analytics, writing to
  storage. Return a teardown function. Dependencies are what the effect read synchronously the last
  time it ran; reads after `await` or in callbacks are not tracked. `untrack(() => …)` opts out.
- `$effect.pre` replaces `beforeUpdate`. `getAbortSignal()` (5.35+) gives a signal that aborts when
  the current derived or effect re-runs or is destroyed.
- Two-way relations: function bindings `bind:value={() => left, (v) => (spent = total - v)}`
  instead of two effects writing each other.

## 6. `$state`: proxies, classes and built-ins

- `$state({...})` and `$state([...])` are deep proxies of **plain objects and arrays only**. Pushing,
  splicing and assigning properties all update.
- **`Map`, `Set`, `Date`, `URL` and class instances are not proxied.** `$state(new Set())` and
  `.add()` change nothing on screen. Use `SvelteMap`, `SvelteSet`, `SvelteDate`, `SvelteURL`,
  `SvelteURLSearchParams` from `svelte/reactivity` (they don't need `$state`), or reassign a new
  instance. `SvelteMap#getOrInsert`/`getOrInsertComputed` exist since 5.57.
- Classes: declare reactive fields with `$state`/`$derived` (fields or first assignment in the
  constructor since 5.31). Those fields become non-enumerable accessors, so
  **`JSON.stringify(instance)` gives `{}`** and `{ ...instance }` leaves them out. Add `toJSON()` or
  serialise the fields. Use arrow-function methods if they are passed as event handlers (`this`).
- `$state.raw(value)` is not proxied: only reassignment updates. Good for large API responses.
- **Proxies are not structured-cloneable.** `structuredClone` and everything built on it
  (`postMessage`, IndexedDB, `history.pushState` state) throw `DataCloneError` on `$state` objects. Pass `$state.snapshot(value)`
  (respects `toJSON`), or map to fresh plain objects. `$state.snapshot` is a rune too, so in a plain
  `.ts` file copy the data out (`list.map((x) => ({ ...x }))`) or call a method of the
  `.svelte.ts` module. `JSON.stringify` reads through proxies and is fine.
- Destructuring or passing a primitive copies the current value: `const { count } = counter` and
  `useThing(count)` are snapshots. Pass the object, a getter, or a function.

## 7. Shared state in `.svelte.ts` modules

Runes work only in `.svelte`, `.svelte.js` and `.svelte.ts` files. Moving state out of a component
means renaming the module and updating its importers.

```ts
// playlist.svelte.ts
export class Playlist {
  songs = $state<Song[]>([])
  durationSec = $derived(this.songs.reduce((s, t) => s + t.durationSec, 0))
  constructor(initial: Song[] = []) {
    this.songs = initial
  }
  add(song: Song) {
    this.songs.push(song)
  }
  clear() {
    this.songs = []
  }
}
export const playlist = new Playlist()
```

- You can export `$state` only if the binding is never reassigned (`export const settings = $state({…})`
  and mutate its properties). `export let n = $state(0)` plus `n += 1` is the compile error
  `state_invalid_export`; exporting a `$derived` is `derived_invalid_export`. Export a class
  instance, an object, or getter functions.
- Replacing stores: methods mutate state, `$derived` fields replace `derived()`, and plain code reads
  `playlist.durationSec` directly instead of `get(store)`. `$store` auto-subscription only works in
  components (`store_invalid_subscription_module` in modules). Bridge with `fromStore`/`toStore`
  from `svelte/store` while both exist.
- Persisting: write to storage in the mutating methods, or own an effect explicitly with
  `$effect.root(() => { $effect(() => persist(JSON.stringify(this.songs))) })` and keep its cleanup.
- Module state is shared by every request during SSR. For per-user state, put the instance in
  context: `const [getPlaylist, setPlaylist] = createContext<Playlist>()` (5.40+; 5.57 also returns
  a third `has` function).

Patterns for stores, persistence, context and external subscriptions (`createSubscriber`,
`MediaQuery`): [the shared state reference](references/shared-state.md).

## 8. Snippets instead of slots

```svelte
<!-- DataTable.svelte -->
<script lang="ts" generics="Row">
  import type { Snippet } from 'svelte'
  let { rows, row, empty, children }: {
    rows: Row[]
    row: Snippet<[Row, number]>
    empty?: Snippet
    children?: Snippet
  } = $props()
</script>
{@render children?.()}
{#each rows as r, i (i)}{@render row(r, i)}{:else}{@render empty?.()}{/each}
```

```svelte
<DataTable rows={songs}>
  <h2>Songs</h2>
  {#snippet row(song, i)}<p>{i + 1}. {song.title}</p>{/snippet}
  {#snippet empty()}<p>No songs</p>{/snippet}
</DataTable>
```

- Content between the tags becomes `children`; `{#snippet name()}` inside the tags becomes the prop
  `name`. Slot props become snippet parameters. Fallback content is an `{#if snippet}` / `{:else}`.
- Don't name a loop variable like a snippet prop: `{#each items as row}` shadows a `row` snippet.
- Top-level snippets can be referenced in `<script>` and passed as props (`row={myRow}`).
- In tests, build snippets with harness `.svelte` files, or `createRawSnippet` from `svelte`.

## 9. Mounting from plain JavaScript

```ts
// chart-api.ts: a plain API around a component
import { flushSync, mount, unmount } from 'svelte'
import Chart from './Chart.svelte'
import { chartProps } from './chart-props.svelte.ts' // export const chartProps = (p) => { const s = $state(p); return s }

export function mountChart(target: HTMLElement, options: { series: number[]; onpoint?: (i: number) => void }) {
  const props = chartProps({ series: options.series, onpoint: options.onpoint })
  const app = mount(Chart, { target, props, intro: false })
  flushSync() // run onMount, $effect and bind:this now, like Svelte 4's constructor did
  return {
    setSeries: (series: number[]) => void (props.series = series), // replaces $set
    highlight: (i: number) => app.highlight(i), // exports come back from mount()
    destroy: () => void unmount(app), // replaces $destroy; removes <svelte:window> listeners too
  }
}
```

- `mount` and `hydrate` render the markup synchronously but **defer effects**: `onMount`, `$effect`,
  attachments, actions and `bind:this` assignments run at the next flush. An exported method that
  uses a `bind:this` element throws if it is called before that. Call `flushSync()` (or
  `flushSync(() => mount(…))`, which returns the callback's result) when callers rely on effects
  having run.
- Props are read lazily from the object you pass. A plain object is read once; a `$state` object,
  or an object with getters over `$state`, updates the component in place. Don't unmount and mount
  again to change props: that throws away local state, typed input and focus.
- `mount` plays intro transitions by default (`intro: true`); `new Component()` did not. Pass
  `intro: false` to keep the old behaviour. In jsdom an intro throws `element.animate is not a function`.
- `unmount(app, { outro: true })` returns a promise that resolves after outros.
- `render(App, { props })` from `svelte/server` replaces `App.render()`; it returns `{ head, body }`.
- `svelte/legacy` (`createClassComponent`, `asClassComponent`) and `compatibility.componentApi: 4`
  are stopgaps for code you don't control, not a migration.

## 10. Testing with Vitest

```ts
// vitest.config.ts (Vitest prefers it over vite.config.ts)
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [svelte()],
  resolve: { conditions: ['browser'] },
  test: { environment: 'jsdom' },
})
```

- The `browser` condition makes `svelte` resolve its client build; without it `mount` throws
  `lifecycle_function_unavailable`.
- Mount, act, then `flushSync()` before asserting the DOM. Runes are allowed in test files named
  `*.svelte.test.ts`: `const props = $state({ … })`, mount with it, change it, flush, assert.
- Code that creates effects outside components needs `$effect.root` in the test, and its cleanup.
- Test pure state modules without a component: values from `$derived` must be correct right after
  each call.

Details, harness components, `createRawSnippet` and jsdom gaps: [the testing reference](references/testing.md).

## 11. Porting a component or module

1. Check the version and whether runes are forced (section 1). Run the tests and svelte-check
   (usually `npm test` and `npm run check`) first so you know the starting point.
2. Props: `export let` to `$props()`. Mark every prop a parent binds to with `$bindable`. Search
   callers for `bind:<prop>`.
3. `$:` to `$derived` (most of them) or `$effect` (real side effects only).
4. Events: `createEventDispatcher` to callback props; update every caller from `on:x={(e) => …e.detail}`
   to `onx={(v) => …}`. DOM `on:` to `on` attributes with explicit `preventDefault`.
5. Slots to snippets; update callers' `slot="…"`/`let:` to `{#snippet}`.
6. Stores to `.svelte.ts` classes or objects where state is shared; keep values `$derived`.
7. `new Component`/`$set`/`$on`/`$destroy` to `mount`/`$state` props/callbacks/`unmount`, with
   `flushSync()` where callers expect a ready component.
8. Grep for leftovers (single quotes, so the shell leaves `$` alone):
   `rg -n 'export let|\$:|on:[a-z]|createEventDispatcher|<slot|let:|\$\$(rest)?props|\.\$(on|set|destroy)\(|new [A-Z][A-Za-z]*\(\{ *target' src`
9. Prove behaviour: bound parents update, callbacks receive plain values, derived values follow
   prop changes, snapshots survive `structuredClone`, and code that runs outside components still
   reads current values.

## 12. Anti-patterns

| Don't | Do |
| --- | --- |
| `$effect(() => { total = a + b })` | `const total = $derived(a + b)` |
| `$effect` in a class constructor | `$derived` fields; `$effect.root` if an effect is really needed |
| `let { value } = $props()` for a bound prop | `let { value = $bindable() } = $props()` |
| `dispatch('valuechange', v)` | `onvaluechange?.(v)` |
| `$state(new Map())` | `new SvelteMap()` |
| `postMessage(state)` / `structuredClone(state)` | `$state.snapshot(state)` |
| `JSON.stringify(classInstance)` | `toJSON()` or serialise the `$state` fields |
| runes in `store.ts` | `store.svelte.ts` |
| `mount(...)` then immediately read what `onMount` set | `flushSync()` after `mount` |
| remount to change props | `$state` props object |
| `{@render children()}` when children is optional | `{@render children?.()}` |

## References

- [Migration details and grep patterns](references/migration-svelte-4.md)
- [Shared state: classes, modules, stores, context, persistence](references/shared-state.md)
- [Testing Svelte 5 with Vitest and jsdom](references/testing.md)
- [Sources checked](references/sources.md)
