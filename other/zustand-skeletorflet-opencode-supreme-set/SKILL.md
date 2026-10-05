---
name: zustand
description: Zustand — lightweight state management with stores, selectors, middleware, slices pattern.
---

## zustand

### Stores & Actions
- `create((set, get) => ({ count: 0, inc: () => set((s) => ({ count: s.count + 1 })) }))` — define store.
- `set` for partial state merges; `get()` for current state inside actions.
- `set({ count: 5 }, true)` — replace entire state instead of shallow merge.

### Selectors
- `useStore((s) => s.count)` — subscribe with selector; re-renders only on change.
- `useStore.getState()` / `useStore.setState(...)` — read/write outside React.
- `subscribe((state) => console.log(state))` — listener for non-React contexts.
- `subscribe((s) => s.count, (count) => ...)` — selector-based subscription (v4+).

### Middleware
- `persist` — `persist(store, { name: 'key', storage: createJSONStorage(() => localStorage) })`.
- `immer` — `immer((state) => { state.items.push(newItem) })` — mutable-style updates.
- `devtools` — `devtools(store, { name: 'StoreName' })` — Redux DevTools integration.
- `subscribeWithSelector` — enables selector-specific subscriptions.

### Slices Pattern
- Compose stores: `create((...a) => ({ ...createUserSlice(...a), ...createCartSlice(...a) }))`.
- Each slice receives `set`, `get` — no cross-slice coupling.
- `useBoundStore` — re-export composed store with typed selectors.

### Computed Values
- Derive state in selectors: `useStore((s) => s.items.filter((i) => i.active))`.
- Use `subscribeWithSelector` + local computation for memoized derivations.
- Middleware `combine` or manual `get()` in actions for computed side effects.
