---
name: svelte/selector-lifecycle
description: >-
  Use when choosing selector call modes in Svelte components, handlers,
  callbacks, composition, or sagas, dispatching through Store, or fixing
  lifecycle_outside_component and selector-shape errors.
type: sub-skill
requires:
  - svelte
  - svelte/selectors
triggers:
  - Svelte selector call mode
  - Svelte outside component crash
  - Svelte select in handler
---
# Selector Lifecycle — call-mode guardrails

> Canonical call-site checklist for avoiding `lifecycle_outside_component`. Human reference and examples: `@themislib/themis/docs/SELECTORS.md` → Using Selectors and Selector Lifecycle Rules. Authoring/cache contracts: `../selectors/SKILL.md` → **Selector caching**. Store setup: `../store/SKILL.md` → **Lifecycle rules**.

## Use when

- Selecting values from components, event handlers, callbacks, tests, sagas, or other selectors.
- Debugging `lifecycle_outside_component` crashes.
- Moving selector reads across component initialization boundaries.

Use this lifecycle for apps that chose the Svelte Store family.

## Call-mode map

| Context | Correct call | Why |
| --- | --- | --- |
| Component init/top-level `<script>` | `const value$ = selectFoo(args)` | Returns a Store-bound readable; recommended placement for subscription ownership. |
| Template | Use the captured readable as `$value$` | Captures once at component init and renders the value, not the readable object. |
| Event handler/callback/async/test | `selectFoo.select(state, args)` | No Svelte context required. |
| Saga | `yield* selectFoo.effect(args)` | Emits the package's typed saga select effect. |
| Selector composition | `otherSelector.select(state, args)` | Reuses state already in scope. |
| Non-context readable | `selectFoo.withStore(store)(args)` | Binds explicitly to an initialized Store; the subscriber owns unsubscribe cleanup. |

Direct `selectFoo()` already binds to the creating Store and does not call
`getContext()`. Component-init placement is app policy, not an enforced runtime
restriction on these reads. Services may consume an already-initialized Store's
readable if they own unsubscribe cleanup; `.withStore(store)` selects an explicit
Store, not a context workaround. Fresh Svelte `store.init()` and context helpers
have different restrictions; see `../store/SKILL.md` → **Lifecycle rules** and
**Svelte component lifecycle helpers**.

## Do

- Capture selector readables during component initialization and dispatch through the configured Store instance.
- Use `.select(store.state, ...)` with the existing initialized `Store` instance captured outside the handler for one-shot reads when no state argument is already available.
- Use `.effect()` in sagas instead of passing selector objects to `select`; use selector-channel helpers with plain args when a saga needs to respond to selector value changes.
- Use `.select(state)` when composing selectors or testing them.

## Don't

- Do not use `selectFoo()` after `await`, in handlers/callbacks or pure selector tests for one-shot reads; use `.select(state)` instead. Deliberate adapter subscription tests/services need an initialized Store and explicit cleanup. Never call the readable form inside another selector.
- Do not use `get(selectFoo())` for a one-shot handler read; prefer `.select(store.state)` without creating a subscription.
- Do not import standalone dispatch helpers; use `store.dispatch(action)` on the configured Store instance.
- Do not pass the selector object itself to saga `select`; use `.effect()` or `.select` intentionally.
- Do not make selector-channel effects call or subscribe to direct Svelte readables;
  they read the Redux store from saga context and use the `.select`/`.effect`
  selector shape.

## Examples

### 1. Capture selector readables during component initialization

```ts
import { store as appStore } from "$lib/store";

const item$ = selectItem(itemId);
const canSave$ = selectCanSaveItem(itemId);

function onSave() {
  const item = selectItem.select(appStore.state, itemId);
  if (item) appStore.dispatch(saveItem(item));
}
```

### 2. Derive template-facing values from captured readables

```ts
import { derived } from "svelte/store";

const item$ = selectItem(itemId);
const itemTitle$ = derived(item$, (item) => item?.title ?? "Untitled");
```

### 3. Use .select after await or inside callbacks

```ts
import { store as appStore } from "$lib/store";

async function onArchive(itemId: string) {
  await confirmArchiveDialog(itemId);
  const item = selectItem.select(appStore.state, itemId);
  if (item?.status !== "archived") appStore.dispatch(archiveItem(itemId));
}
```

### 4. Use .effect inside sagas instead of passing selector objects to select

```ts
import { put } from "typed-redux-saga";

function* saveCurrentItemWorker() {
  const itemId = yield* selectCurrentItemId.effect();
  if (itemId) yield* put(saveItem(itemId));
}
```

### Composition handoff

Composition uses `.select(state)` on the state already in scope. For the actual
selector definitions, use `../selectors/SKILL.md` → **Compose selectors with .select(state), not readable calls**;
do not create a readable subscription inside a selector callback.

### Bind explicitly with .withStore when no Svelte context is available

```ts
import type { store as appStore } from "$lib/store";

export function createItemReadable(store: typeof appStore, itemId: string) {
  return selectItem.withStore(store)(itemId);
}
```

The supplied Store must already be initialized. If you subscribe manually,
retain and call the unsubscribe function when the owner ends; component `$value$`
bindings handle their own subscription cleanup.

### 7. ❌ Bad: creating readables after component initialization

```ts
// BAD: creates an unowned subscription for what should be a one-shot read.
async function onSaveLater(itemId: string) {
  await queueMicrotaskPromise();
  const item$ = selectItem(itemId);
  item$.subscribe((item) => store.dispatch(saveItem(item)));
}

async function onSaveLaterSafely(itemId: string) {
  await queueMicrotaskPromise();
  const item = selectItem.select(store.state, itemId);
  if (item) store.dispatch(saveItem(item));
}
```

## Pitfalls

- Direct selectors require a live initialized Store, not Svelte `getContext()`. Keep readables at component init for clear ownership, and use `.select` for one-shot work. A `lifecycle_outside_component` error points to context helpers or Svelte Store initialization, not the Store-bound selector itself. Dispatch also uses the configured Store without a context helper.
- A selector readable call in a template expression still violates lifecycle guidance even though the same Store + selector + args reuse the cached readable; capture it once at component init and render the captured `$value$`. Cache behavior is owned by `../selectors/SKILL.md` → **Selector caching**.
- `.select(state)` returns a value; `selectFoo()` returns a readable. Mixing them often produces wrong-shape bugs before it crashes.

## Verification cues

- Component changes show selector readables captured at top-level initialization and Store dispatch used in handlers.
- Pure selector tests use `.select(mockState, ...)`; adapter lifecycle tests may subscribe deliberately with valid initialization and teardown.
- Saga tests cover `.effect()` paths or named selector calls rather than inline `select((state) => ...)` lambdas.

## See also

- `@themislib/themis/docs/SELECTORS.md` — examples for each selector call form.
- `../selectors/SKILL.md` — selector authoring and composition.
- `../component-integration/SKILL.md` — component store/dispatch wiring.
- `../../core/selector-channels/SKILL.md` — selector reads from sagas.
- `../../core/wait-for/SKILL.md` — saga waiting on selector predicates.
