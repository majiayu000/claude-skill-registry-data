---
name: svelte/migration/component-migration
description: >-
  Use when replacing Svelte store imports and template subscriptions with
  Themis selector readables and dispatch. Apply call-mode policy from
  svelte/selector-lifecycle.
type: sub-skill
requires:
  - svelte/component-integration
  - svelte/migration
triggers:
  - migrate component
  - replace store import
  - $foo$ in template
  - selector readable
---
# Migration — Components

> Replace Svelte store imports with `selectFoo()` readables and dispatch through
> the configured app `Store` instance. Templates stay reactive by
> reading the returned readable with `$selectorResult$`.

Apply `../../selector-lifecycle/SKILL.md` → **Call-mode map** when replacing
reads. This leaf owns the legacy-to-new consumer conversion, not a second
selector lifecycle policy.

## Examples

### 1. Before: component owns Svelte store imports and updates

```typescript
// migration/components/CounterPanel.before.ts
import { derived, writable } from "svelte/store";

export const count = writable(0);
export const doubled = derived(count, ($count) => $count * 2);

export function incrementLegacyCount() {
  count.update((value) => value + 1);
}
```

### 2. After: create selector readables once at component initialization

```typescript
// Inside the <script> of src/lib/components/CounterPanel.svelte
import { store } from "$lib/store/store";
import { increment } from "$lib/store/slices/counter/counter-slice";
import { selectCount, selectDoubled } from "$lib/store/slices/counter/counter-selectors";

const count$ = selectCount();
const doubled$ = selectDoubled();

function handleIncrement() {
  store.dispatch(increment());
}
```

### 3. Template-facing selector results keep markup simple

```typescript
// src/lib/store/slices/counter/counter-selectors.ts
import { store } from "$lib/store/store";

export const selectCounterVm = store.createSelector((state) => ({
  countLabel: `${state.counter.count} clicks`,
  doubledLabel: `${state.counter.count * 2} doubled`,
  canSubmit: state.counter.count > 0,
}));
```

### 4. Event handlers use `Store.state` plus `.select(...)` for one-shot reads

```typescript
// src/lib/components/SubmitCounter.svelte.ts
import { store } from "$lib/store/store";
import { submitCount } from "$lib/store/slices/counter/counter-slice";
import { selectCount } from "$lib/store/slices/counter/counter-selectors";

export function handleSubmit() {
  const count = selectCount.select(store.state);
  if (count > 0) {
    store.dispatch(submitCount(count));
  }
}
```

### 5. Event handlers dispatch through the configured Store instance

```typescript
// src/lib/components/UserMenu.svelte.ts
import { store } from "$lib/store/store";
import { logoutRequested, renameUser } from "$lib/store/slices/session/session-slice";

export function handleRename(name: string) {
  store.dispatch(renameUser(name.trim()));
}

export function handleLogout() {
  store.dispatch(logoutRequested());
}
```

### Callback lifecycle handoff

Do not move the readable call into a callback while converting a consumer.
Use `../../selector-lifecycle/SKILL.md` → **Call-mode map** and **Pitfalls** for
the one-shot replacement and subscription-ownership policy. Store-bound direct
selectors do not call `getContext()`; context helpers and `Store.init()` have
separate component-initialization requirements.

### 7. ❌ Bad: duplicate old-store ownership after Redux dispatch

```typescript
// ❌ BAD: updating both owners makes rollback and selector reads disagree.
type Writable<T> = { update(fn: (value: T) => T): void };
type Store = { dispatch(action: { type: string; payload?: unknown }): void };

declare const legacyCount: Writable<number>;
declare const store: Store;
declare function increment(): { type: "counter/increment" };

export function badDoubleWrite() {
  legacyCount.update((value) => value + 1);
  store.dispatch(increment());
}

export function goodSingleOwnerWrite() {
  store.dispatch(increment());
}
```

## Rollout Order Per Component

1. Replace each `import { foo } from "$lib/stores/..."` with imports from
   the new slice / selectors (`selectFoo`, action creators) and the configured
   app `store` instance.
2. At the top of the component script (init time), create one
   `const foo$ = selectFoo()` per consumed selector.
3. Replace every `$foo` template reference with `$foo$`.
4. Replace every `foo.set(...)` / `foo.update(...)` with
   `store.dispatch(setFoo(...))` / `store.dispatch(<action>(...))`.
5. Inside event handlers or async work that needs a one-shot read, use an
   existing initialized `Store` instance imported/captured outside the handler:
   `selectFoo.select(store.state)`.
6. Re-run the component's existing tests before handoff; VCS policy comes from
   the active task/repository instructions, per `../cleanup/SKILL.md` → **Workflow ownership**.

## Cross-References

- `../../component-integration/SKILL.md` → **Template and handler wiring** —
  Store dispatch and `$selectorResult$` templates
- `../../store/SKILL.md` → **Lifecycle rules** — Store initialization/disposal
- `../../selector-lifecycle/SKILL.md` — three call modes
  and component-init placement versus actual context-helper restrictions

