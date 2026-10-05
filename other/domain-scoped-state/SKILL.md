---
name: core/domain-scoped-state
description: >-
  Use createDomainScopedHelpers when reading, writing, or clearing Redux state
  keyed by workspace, project, or tenant in byDomainId.
type: sub-skill
library: themis
requires:
  - core
  - core/reducers
sources:
  - "@themislib/themis/utils/store/domain-scoped"
  - ../SKILL.md
triggers:
  - domain-scoped state
  - scoped helpers
  - byDomainId shape
  - workspace state
---
# Domain-Scoped State — `createDomainScopedHelpers`

Use for state partitioned by workspace, project, tenant, or session id.
The helpers preserve immutable updates and no-op identity; they do not schedule
cleanup automatically. Call `clearDomainState` when a domain is removed.

## Shape

Import `createDomainScopedHelpers` from
`@themislib/themis/utils/store/domain-scoped`. Its state constraint is:

```typescript
type DomainScopedState<T> = {
  byDomainId: Record<string, T>;
};
```

Key guarantees:

- `getDomainState(state, id)` returns the stored value or the shared `emptyState`
  fallback for a missing/nullish value; do not mutate that fallback.
- `setDomainState(state, id, value)` compares the actual stored value, not the
  fallback, using shallow equality. An equal replacement returns the original
  state, map, and domain references. Changed nested references count as changes,
  even if their contents are equal.
- A changed set creates a new state and `byDomainId`, stores the supplied value,
  and preserves unrelated domains/fields. Setting a missing id to a non-null
  empty-state object still creates the entry.
- `clearDomainState(state, id)` preserves state identity for an absent id;
  otherwise it removes that entry immutably.

These guarantees come from the helper itself, not `createReducer` normalization.
Implementation evidence: `src/utils/store/domain-scoped.ts`; executable contract:
`src/utils/store/create-reducer.test.ts` (`createDomainScopedHelpers` cases).

## 2. Setup — minimum working slice

```typescript
// workspace-items-types.ts
import type { Collection } from "@themislib/themis/utils/collections/collection-utils";

export type WorkspaceItemsState = {
  items: Collection<Item, "id">;
  loadedAt: number;
};

export type State = {
  byDomainId: Record<string, WorkspaceItemsState>;
};
```

```typescript
// workspace-items-slice.ts
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";
import { createCollection } from "@themislib/themis/utils/collections/collection-utils";
import { createDomainScopedHelpers } from "@themislib/themis/utils/store/domain-scoped";
import type { State, WorkspaceItemsState, Item } from "./workspace-items-types";

const emptyState: WorkspaceItemsState = {
  items: createCollection<Item, "id">("id"),
  loadedAt: 0,
};

const { getDomainState, setDomainState, clearDomainState } =
  createDomainScopedHelpers(emptyState);

const initialState: State = { byDomainId: {} };

export const setItems    = createAction<[id: string, items: Item[]]>("workspaceItems/setItems");
export const clearDomain = createAction<[id: string]>("workspaceItems/clearDomain");

export const workspaceItemsReducer = createReducer<State>(initialState)
  .with(setItems, (state, { payload: [id, items] }) =>
    setDomainState(state, id, {
      ...getDomainState(state, id),
      items: createCollection<Item, "id">("id", items),
      loadedAt: 0, // store a timestamp you dispatch in, not Date.now here
    })
  )
  .with(clearDomain, (state, { payload: [id] }) => clearDomainState(state, id));
```

Notes:

- Pass the domain id as the **first** tuple element so saga code can key subscriptions by it.
- Use `getDomainState(state, id)` inside reducer handlers to read the current per-domain slice safely (falls back to `emptyState` for unknown ids).
- `clearDomainState` is the right tool for logout / workspace-change cleanup.

## 3. Core patterns

### 3.1 Reading the current-domain slice in a selector

```typescript
// workspace-items-selectors.ts
import { store } from "$lib/store/store";
import { getItems } from "@themislib/themis/utils/collections/collection-utils";
import { selectCurrentWorkspaceId } from "../workspaces/workspaces-selectors";

export const selectWorkspaceItems = store.createSelector((state) => {
  const id = selectCurrentWorkspaceId.select(state);
  return id ? state.workspaceItems.byDomainId[id]?.items : undefined;
});

// Array form for templates
export const selectWorkspaceItemList = store.createSelector((state) => {
  const items = selectWorkspaceItems.select(state);
  return items ? getItems(items) : [];
});
```

### 3.2 Updating inside an existing per-domain slice

Combine `getDomainState` + spread + `setDomainState`:

```typescript
.with(addItem, (state, { payload: [id, item] }) => {
  const current = getDomainState(state, id);
  return setDomainState(state, id, {
    ...current,
    items: addItemCollection(current.items, item),
  });
})
```

### 3.3 Clearing a domain on logout / workspace-change

```typescript
.with(leftWorkspace, (state, { payload: [id] }) =>
  clearDomainState(state, id)
);
```

Because `clearDomainState` returns the same reference if the id was absent, selectors keyed on unrelated domains won't re-emit.

## 4. Common Mistakes

- Do not hand-roll nested setters that omit the safe read fallback or no-op
  checks; use the guarantees in [Shape](#shape).
- Keep `emptyState` serializable: use collections and numeric timestamps, not
  `Date`, `Map`, `Set`, or class instances. See
  [State Serialization — Do](../state-serialization/SKILL.md#do) and
  [Don't](../state-serialization/SKILL.md#dont).
- Keep the key named `byDomainId`; `byId`/`byWorkspaceId` do not satisfy the
  helper's state constraint.

## 5. When to use

- State must be partitioned by a stable id (workspace / project / tenant / session).
- You need explicit cleanup on domain removal (`clearDomainState`).
- You want reads to gracefully fall back to a known empty shape.

If every consumer shares a single domain (no multi-tenant / multi-workspace concept), a plain slice is simpler — reach for `createDomainScopedHelpers` only when the domain id is part of the key.

## 6. See also

- `core/reducers` — pure-update rules, `createReducer` builder.
- `core/state-serialization` — why `emptyState` must be structured-cloneable.
- `core/collections` — the usual shape of per-domain data.