---
name: core/debugging
description: >-
  Use when inspecting Store state through window.svelteRedux.reduxContext or
  Store.initDevTool(), or diagnosing reducer reference equality.
type: sub-skill
library: themis
requires:
  - core
sources:
  - "@themislib/themis/svelte-store"
  - package-internal devtools registration
triggers:
  - svelteRedux api
  - reduxContext inspect
  - reducer reference equality
---
# Debugging — `window.svelteRedux` and inspection

> Runtime debugging hooks are registered by `Store.initDevTool()` after
> `Store.init()`. No localStorage-gated reference-check middleware or debug
> toggle is wired.

## 1. `window.svelteRedux` — console API

After `store.initDevTool()` runs in a browser, Store-owned devtools registration
attaches a `svelteRedux` object to `window` where supported. The
debugging-relevant field is:

```typescript
window.svelteRedux = {
  reduxContext: Store instance | Store instance[],
};
```

`reduxContext` stores the public `Store` instance, not the internal Redux store
context. Use the `Store.state` and `Store.dispatch` APIs from the console.

### 1.1 Inspect state from the console

```js
// Current state snapshot (plain object)
window.svelteRedux.reduxContext.state;

// Dispatch an action manually (useful when a button is broken)
window.svelteRedux.reduxContext.dispatch({ type: "my/action", payload: [...] });
```

### 1.2 Multiple-store detection

Devtools registration treats the first Store as the canonical one. If a second
Store is exposed before cleaning up the previous devtools registration,
`registerGlobalDevTools` reports `"Multiple Redux stores initialized:"` with the
list. Diagnose the exposed registrations and their lifetime owners; the warning
is not an init-call counter. `init()` alone does not register devtools, and
repeating `init()` on an already-initialized instance is a no-op. Remove stale
registrations or consolidate accidental duplicate owners onto one `Store`.

## 2. Reference-equality diagnostics

No runtime debug toggle is wired for reducer reference checks. Keep no-op reducer
contracts in tests instead:

```js
expect(reducer(initialState, noOpAction)).toBe(initialState);
```

## 3. Setup — minimum working inspection

After a store exists and devtools are registered:

```js
// 1. App code runs store.init(), then store.initDevTool().
// 2. Open DevTools.
// 3. Inspect state.
window.svelteRedux.reduxContext.state;
```

## 4. Core patterns

### 4.1 Diagnose a selector that won't update

1. Reproduce the action and inspect the state snapshot from
   `window.svelteRedux.reduxContext.state`.
2. If the slice didn't change → reducer missed the case. Check the action
   type namespace (`sliceName/actionName`).
3. If the slice changed but your selector didn't fire → selector
   memoization key didn't change; inspect what `.select(state)` returns
   from the console.

### 4.2 Diagnose "multiple stores initialized"

Check the log for `"Multiple Redux stores initialized:"`, then inspect the
registered `reduxContext` instances and where each calls `initDevTool()`.
Typical causes are overlapping root lifetimes, hot-reload/test code retaining a
registration, or intentionally exposing another Store before unregistering the
first. The warning does not prove that repeated `init()` is the cause.

Retain and call the disposer returned by `initDevTool()` when inspection ends;
`Store.dispose()` also cleans up that Store's registration and initialized
runtime. Do not dispose a live Store owned elsewhere just to hide the warning.

### 4.3 Confirm state is serializable

Use reducer tests or console inspection to verify state remains plain and
JSON-shaped after the suspected action. See
`core/state-serialization` for the allowed and forbidden
state shapes.

### 4.4 Check reducers that break reference equality

Write reducer tests for no-op paths and assert the incoming `state` reference
is returned unchanged. Runtime devtools inspection does not emit reducer
reference warnings.

## 5. Common Mistakes

### Expecting runtime debugging to diagnose reducer drift

**Mechanism:** `window.svelteRedux` exposes Store inspection only; it does not
install a reducer-reference checker.

```js
// ❌ WRONG — expects browser debugging to enforce reducer contracts
window.svelteRedux.reduxContext.state;

// ✅ CORRECT
expect(reducer(initialState, noOpAction)).toBe(initialState);
```

*Public facade: `@themislib/themis/svelte-store`; devtools registration is package-internal implementation context.*

### Expecting `reduxContext` to always be an object

**Mechanism:** overlapping devtools registrations can make `reduxContext` an
**array** of Store instances. Reading an array's `.state` returns `undefined`;
subsequent state access may then throw. Cleanup can leave an empty or one-element
array, and no registration can mean no context at all. Inspect every remaining
registration rather than silently picking the first one:

```js
// Console-only diagnostic, not application Store selection.
const ctx = window.svelteRedux?.reduxContext;
const stores = ctx ? (Array.isArray(ctx) ? ctx : [ctx]) : [];
const states = stores.map((store) => store.state);
// Inspect each owner; remove stale registrations at their owning boundary.
```

*Source: Store-owned runtime context handling.*

### Using initialized store access for debug reads

**Mechanism:** `store.state` and `store.dispatch` are only available after
the app's `Store.init()` completes. In application code, pass or import the
same initialized `Store` instance. In the browser console, use
`window.svelteRedux.reduxContext` only after devtools registration exposes it.

```js
// ✅ Application code after Store.init()
store.dispatch(action);
const state = store.state;

// ✅ Browser console diagnostic
window.svelteRedux.reduxContext.dispatch(action);
```

*Public API: `@themislib/themis/svelte-store` (`Store.state`, `Store.dispatch`).*

## 6. See also

- Selected Store family lifecycle skill — initialization/disposal ownership and
  overlapping lifetimes that can leave multiple devtools registrations.
- `core/reducers` — the same-reference on no-op contract
  that reducer tests should enforce.
- `core/state-serialization` — the serializability rule
  reducers and tests should preserve.
- `core/testing` — assertions that mirror reducer and
  serialization contracts in unit tests.

