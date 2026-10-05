---
name: ha:lit-render-audit
description: "Inspect ha-frontend Lit component reactive properties/state for unnecessary re-renders — per-hass work not gated on the relevant change, over-broad @state, whole-hass params, heavy objects in @property, missing hasChanged, memory bloat. Use when a component re-renders too often or memory grows."
effort: medium
argument-hint: path/to/component.ts
allowed-tools: Read, Grep, Glob, Bash
---

# Lit Render Audit (ha-frontend)

Analyze ha-frontend Lit component reactive properties and state for render
efficiency, clarity, and best practices. Maps to the frontend strong defaults
**FS1** (gate derived work on the relevant change), **FS2** (correct
memoization), **FS3** (`@state` vs `@property`), **FS10** (narrow the `hass`
object), and **FS15** (memory discipline). Each finding cites its law + PR.

## Iron Laws - Never Violate These

1. **Gate derived work on the *relevant* change** - `changedProps.has(...)`, `shouldUpdate`, or `memoizeOne` on narrowed inputs; never run per-`hass`-update work for unrelated state changes. **FS1** - "This fires on every `hass` change which is way to often" (MindFreeze, [PR 28672](https://github.com/home-assistant/frontend/pull/28672#discussion_r2882169715))
2. **Use `repeat()` with stable keys for lists** - Never render large lists directly with `.map()` and no key; virtualize truly large ones with `@lit-labs/virtualizer`
3. **`@state()` for internal reactive fields, `@property` only for public API** - `@property`/`@state` only for values that actually affect `render()`; anything async-assigned or `_`-prefixed is `@state`. **FS3** - "this shouldn't be a property. make it a boolean `@state`" (wendevlin, [PR 27020](https://github.com/home-assistant/frontend/pull/27020#discussion_r2381811816))
4. **Provide a custom `hasChanged` for heavy objects/arrays** - Don't let default reference equality trigger (or suppress) re-renders incorrectly
5. **Initialize every reactive property with a default** - Never access a property/state field that might be `undefined`
6. **NEVER modify components or code during audit** - this is a read-only diagnostic; report findings only

## Quick Audit Commands

### Extract All Reactive Fields

Use Grep to find all `@property(` and `@state(` declarations in the target component file.

### Find Per-`hass` Work Not Gated (FS1)

Use Grep to find `willUpdate`/`updated`/`shouldUpdate` bodies and check each does derived work only inside a `changedProps.has(...)` guard. Flag any `willUpdate`/`updated` that runs work unconditionally on every `hass` change.

### Find Whole-`hass` Params (FS10)

Use Grep to find helper/child signatures taking the full `hass` object where a slice (`HomeAssistant["states"]`, `localize`) would do. Docs still show monolithic `hass`; 2026 reviews push narrowing — flag as an FS10 finding, not a hard block.

### Find Large Data Patterns

Use Grep to find large data patterns: arrays/objects stored in state (`@state\(\).*:.*\[\]`, `@state\(\).*Array`) and heavy object properties (`@property\(.*\).*:.*(object|\{)`) in the target file.

## Audit Checklist

### 1. Render-Thrash Issues

| Pattern | Problem | Solution |
|---------|---------|----------|
| Work in `willUpdate`/`updated` with no `changedProps.has` guard | Runs on every `hass` (i.e. every state) change | Gate on the relevant change (FS1) |
| `@property() items: Item[]` passed from parent | Re-renders on every parent update (new array reference) | Add custom `hasChanged`, or memoize upstream |
| Object/array/schema built inside `render()` | Creates a new reference each render, defeats child memoization | Hoist to a module const or `memoizeOne` (F2) |
| `@state() data: BigObject` never read in `render()` | Unnecessary re-render on every write | Move to a plain class field (FS3) |
| `.map(...)` rendering a list without `repeat()` | Key-less diff discards and rebuilds DOM nodes | Use `repeat()` from `lit/directives/repeat` |
| Unbounded list rendered directly | Memory + layout cost grows with data | `@lit-labs/virtualizer`'s `<lit-virtualizer>` |

### 2. Memoization Correctness (FS2)

Flag memoized functions that:

- read `this.*` inside the body instead of taking it as an argument
- omit an input (commonly `localize`) from the argument list
- receive a freshly-built object (`Object.values(...)`, an inline literal) as an arg, defeating the cache

"`Object.values` generates a new object each time and defeats the memoization" (MindFreeze, [PR 29636](https://github.com/home-assistant/frontend/pull/29636#discussion_r3481369292)).

```ts
// GOOD: every input passed explicitly, including localize
private _rows = memoizeOne(
  (states: HomeAssistant["states"], localize: LocalizeFunc) => /* … */
);
```

### 3. Missing or Incorrect hasChanged

Should define a custom `hasChanged`:

- Properties holding arrays/objects compared by reference
- Properties where shallow reference equality causes unnecessary re-renders
- Properties where a deep/id-based comparison catches real content changes

```ts
@property({
  attribute: false,
  hasChanged: (value: Item[], oldValue: Item[]) =>
    value.length !== oldValue?.length ||
    value.some((v, i) => v.id !== oldValue[i]?.id),
})
public items: Item[] = [];
```

### 4. Unused / Over-Broad State (FS3)

Search for `@state()`/`@property()` fields defined but never used in `render()`
or a derivation. `_`-prefixed `@property` fields should be `@state`; public
`@property` fields never set from outside should be `@state`.

Use Grep to extract all `@state()`/`@property()` field names, then use Grep to find all `this\.\w+` references inside `render()`/`willUpdate`. Compare to find unused reactive fields (these should be plain class fields).

### 5. Missing Initialization

```ts
// BAD: this._items might be undefined
protected render() {
  return html`${this._items.map((item) => html`<li>${item.name}</li>`)}`;
}

// GOOD: initialize with a default
@state() private _items: Item[] = [];
```

### 6. Leaked Listeners, Subscriptions, and Timers (FS15)

- Event listeners added in `connectedCallback()` must be removed in `disconnectedCallback()`
- Subscriptions (`hass.connection.subscribe*`, `src/data` collections, reactive controllers) must be torn down in `disconnectedCallback()` (returned `UnsubscribeFunc` called)
- `setInterval`/`setTimeout` handles must be cleared in `disconnectedCallback()`
- Module-level `Map` caches must be capped or use `WeakMap` - "there is no cap on it. It can run out of memory" (balloob, [PR 52657](https://github.com/home-assistant/frontend/pull/52657#discussion_r3414893248))

## Render-Cost / Memory Estimation

For each reactive field, estimate retained memory and re-render cost:

| Data Held | Approx Size | Concern Level |
|-----------|-------------|----------------|
| number / boolean | ~8 bytes | Low |
| string (100 chars) | ~200 bytes | Low |
| array of 100 plain objects in `@state` | ~10-50 KB; full re-render on any mutation | Medium |
| array of 1000+ items rendered without `repeat()`/virtualizer | ~100-500 KB + full DOM diff per update | High |
| whole `hass` object passed to a child/helper | re-renders the child on every state change | High - narrow the slice (FS10) |
| Blob / ArrayBuffer / image data in `@state` | Varies | Critical - store a file id / object URL, not the data |
| heavy object `@property` with no `hasChanged` | size varies | Medium-High - re-renders on every parent update |

## Usage

Run `/ha:lit-render-audit path/to/component.ts` to generate a reactive-property
inventory with render-cost estimates and optimization recommendations.
