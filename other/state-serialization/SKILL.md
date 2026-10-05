---
name: core/state-serialization
description: >-
  Use when checking Redux state for structured-clone compatibility or
  replacing non-serializable values such as Date, Map, Set, and Error.
type: sub-skill
requires:
  - core
triggers:
  - serializable state
  - structured clone
  - no date in state
---
# State Serialization

> Operational checklist for reducer state shape. Full rationale and examples: `@themislib/themis/docs/REDUCERS.md` → State Serialization Rules. Reducer API: `@themislib/themis/utils/store/create-reducer`; canonical checklist: [Do](#do) and [Don't](#dont).

## Use when

- Adding or changing reducer state, initial state, persisted state, or action payloads that become state.
- Reviewing helpers that introduce dates, errors, maps/sets, class instances, functions, promises, or browser APIs.

## Do

- Keep Redux state JSON-shaped: primitives, arrays, and plain objects.
- Store timestamps as `number` milliseconds or ISO strings; generate them in action creators or sagas, not reducers.
- Store entity sets/maps as `Record<string, T>`, `string[]`, or `Collection<T, K>`.
- Store errors as plain data such as `{ message: string; stack?: string }`.
- Add or update serialization tests for new reducer state: stringify/parse should round-trip the state.

## Don't

- Do not store `Date`, `Map`, `Set`, `WeakMap`, `WeakSet`, `RegExp`, `Promise`, `Function`, class instances, `Error`, or `Symbol` values.
- Do not call `Date.now()`, `Math.random()`, or ID generators inside reducer handlers; pass generated values in the action payload.
- Do not hide non-serializable objects inside collections or nested state fields.

## Examples

### Plain JSON-shaped state

```ts
type Todo = { id: string; title: string; completed: boolean };
type TodosState = {
  ids: string[];
  byId: Record<string, Todo>;
  loading: boolean;
  selectedId: string | null;
};
```

### Store timestamps as numbers or ISO strings

```ts
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

const markSynced = createAction("todos/markSynced", (syncedAtMs: number, syncedAtIso: string) => ({ syncedAtMs, syncedAtIso }));

export const reducer = createReducer({ syncedAtMs: 0, syncedAtIso: "" }).with(markSynced, (state, { payload }) => ({
  ...state,
  syncedAtMs: payload.syncedAtMs,
  syncedAtIso: payload.syncedAtIso,
}));
```

### Serialize errors before storing them

```ts
type SerializableError = { message: string; stack?: string };

function toSerializableError(error: unknown): SerializableError {
  if (error instanceof Error) return { message: error.message, stack: error.stack };
  return { message: String(error) };
}

const failedState = { error: toSerializableError(new Error("network failed")) };
```

### Use records or collections instead of Map and Set

```ts
import { type Collection, createCollection } from "@themislib/themis/utils/collections/collection-utils";

type Todo = { id: string; title: string };
type TodosState = {
  todos: Collection<Todo, "id">;
  selectedById: Record<string, true>;
};

const initialState: TodosState = { todos: createCollection<Todo, "id">("id"), selectedById: {} };
```

### JSON round-trip regression test

```ts
import { describe, expect, it } from "vitest";

const todosReducer = {
  initialState: { ids: [] as string[], byId: {} as Record<string, { id: string; title: string }> },
};

describe("todos state serialization", () => {
  it("round-trips through JSON", () => {
    const state = todosReducer.initialState;
    expect(JSON.parse(JSON.stringify(state))).toEqual(state);
  });
});
```

### ❌ Bad: non-serializable state and reducer-created values

```ts
import { createAction } from "@themislib/themis/utils/store/create-action";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

// BAD: Date, Map, Set, Promise, class instances, and Error do not belong in Redux state.
type Todo = { id: string; title: string };
type TodosState = { updatedAt: Date; byId: Map<string, Todo>; selectedIds: Set<string>; error?: Error };
const initialState: TodosState = { updatedAt: new Date(0), byId: new Map(), selectedIds: new Set() };
const markTouched = createAction("todos/markTouched");

export const reducer = createReducer<TodosState>(initialState).with(markTouched, (state) => ({
  ...state,
  updatedAt: new Date(),
  error: new Error("changed"),
}));
```

## Implementation cues

- If a value needs behavior, store its data in Redux and run behavior in a saga/service.
- If a value is derived from state, keep it out of state and expose it through selectors.
- If a collection-like field grows beyond a simple primitive list, prefer `Collection<T, K>` and the collection helpers.

## Verification cues

- Reducer tests cover initial state and changed paths with `JSON.stringify`/`JSON.parse` round-trips.
- Search new state types for forbidden constructors and browser objects before handoff.
- Run the repository's skill/example validation when documentation examples changed.

## See also

- `@themislib/themis/docs/REDUCERS.md` — human reference for serialization rules and examples.
- `core/reducers/SKILL.md` — reducer purity and same-reference no-op behavior.
- `core/collections/SKILL.md` — serializable normalized entity storage.
- `core/state-integrity/SKILL.md` — derived values and canonical ownership.