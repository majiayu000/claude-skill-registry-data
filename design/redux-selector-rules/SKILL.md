---
name: redux-selector-rules
description: "Redux Toolkit selector rules against re-renders, recalculation warnings, and render loops. Use when writing useSelector/useAppSelector or createSelector, deriving state in a connected component, or seeing 'Selector returned a different result when called with the same parameters'."
---

# Redux Selector Rules

Prevent the most common Redux performance bugs: unnecessary re-renders, Reselect `inputStabilityCheck` warnings, and render loops on startup.

## Core Mechanic

`useSelector` / `useAppSelector` uses **strict `===` reference equality**. After every dispatched action, it re-runs the selector. If the return value is a **new reference**, the component re-renders — even if the data is identical.

- **Primitives** (string, number, boolean): Safe — `===` compares by value.
- **Objects and arrays**: Dangerous — `[] !== []` and `{} !== {}` are always `true`. Any selector returning a new object/array reference on every call forces a re-render on every dispatch.

---

## The Rules

### Rule 1: Never use default values in selectors

This is the #1 source of bugs. `?? null`, `?? []`, `?? {}`, `?? ""` create a **new value every invocation** when the source is `undefined`. This causes infinite re-render loops on startup and triggers Reselect stability warnings.

```ts
// ❌ WRONG — new reference every call when record is undefined
export const selectAgentMessages = createSelector(
  [selectAgentById],
  (record) => record?.messages ?? [],
);

// ✅ CORRECT — return as-is, including undefined
export const selectAgentMessages = createSelector(
  [selectAgentById],
  (record) => record?.messages,
);
```

### Rule 2: Never double-default in the component

If the selector returns the raw value, do not add a default in the component. Same new-reference problem, different location.

```ts
// ❌ WRONG — ?? [] creates a new array ref every render
const messages = useAppSelector(state => selectAgentMessages(state, id)) ?? [];

// ✅ CORRECT — handle undefined at the render boundary
const messages = useAppSelector(state => selectAgentMessages(state, id));
if (!messages) return <MessagesSkeleton />;
```

### Rule 3: Handle undefined at the render boundary

The component handles missing data — not the selector. In priority order:

1. **`next/dynamic` + skeleton** — component doesn't load until data exists. Reduces bundle size, eliminates wasted renders, prevents layout shift when the skeleton matches the component dimensions exactly.
2. **Early return with skeleton** — `if (!data) return <Skeleton />;`
3. **Conditional render** — `{data && <Component data={data} />}`

```tsx
// ✅ GOLD STANDARD — lazy load, show skeleton until data exists
const AgentPanel = dynamic(() => import('./AgentPanel'), {
  loading: () => <AgentSkeleton />,
});

const agent = useAppSelector(state => selectAgentById(state, id));
if (!agent) return <AgentSkeleton />;
return <AgentPanel agent={agent} />;
```

**Skeleton design rule**: Skeletons must be pixel-identical in dimensions to the loaded component. A skeleton that shifts layout on load is worse than no skeleton.

### Rule 4: Input selectors extract, result functions transform

Reselect's `inputStabilityCheck` runs input selectors twice in dev mode. An input selector returning a different reference on the second call triggers a warning.

```ts
// ❌ WRONG — filter in input creates new ref every call
const selectCompleted = createSelector(
  [state => state.todos.filter(t => t.completed)],
  (completed) => completed.length,
);

// ✅ CORRECT — extract in input, transform in result
const selectCompleted = createSelector(
  [state => state.todos],
  (todos) => todos.filter(t => t.completed).length,
);
```

**Input selectors:** plain lookups only — `state => state.some.slice`.  
**Result function:** all `.filter()`, `.map()`, `.reduce()`, aggregation, and derivation.

### Rule 5: Never pass `state => state` as an input selector

Root state reference changes on every action. This forces recalculation on every dispatch.

### Rule 6: Multiple primitives > one object

```ts
// ❌ WRONG — new object every call
const { name, status } = useAppSelector(state => ({
  name: state.agent.name,
  status: state.agent.status,
}));

// ✅ CORRECT — two stable primitive selectors
const name = useAppSelector(state => state.agent.name);
const status = useAppSelector(state => state.agent.status);
```

If an object is unavoidable, pass `shallowEqual` as the second argument to `useAppSelector`. But prefer separate calls for primitives.

### Rule 7: Parameterized selectors need factory functions when shared across components

`createSelector` has a cache size of 1. Multiple components calling the same selector with different arguments break memoization.

```ts
// ✅ Factory — each component instance gets its own memoized selector
const makeSelectAgentById = () =>
  createSelector(
    [state => state.agents.entities, (_state, id: string) => id],
    (entities, id) => entities[id],
  );

// In component
const selectAgent = useMemo(makeSelectAgentById, []);
const agent = useAppSelector(state => selectAgent(state, agentId));
```

---

## Refactoring Selectors: Full Codebase Sweep Required

**This is the most important section for refactors.** When you change a selector — especially removing a default value (`?? []`, `?? null`) or changing its return type — the type changes from `T` to `T | undefined`. **You must find and update every consumer before the refactor is complete.** Missing a single usage produces a runtime crash, not a build error.

### Mandatory refactor steps

1. **Search the entire codebase** for all usages of the selector name (e.g., `selectAgentMessages`).
2. **Update every component** — add an early return, skeleton, or guard before any property access or iteration.
3. **Check chained selectors** — if the selector is an input to another `createSelector`, the downstream result function now receives `T | undefined` and must handle it.
4. **Check non-component usages** — thunks, middleware, sagas, utils that call the selector also need undefined handling.
5. **Update the selector's TypeScript return type** so the compiler enforces the change.

```ts
// Before: selector returned [] — every consumer assumed array
// After: selector returns undefined

// ❌ CRASH — .map() on undefined
const items = messages.map(m => m.text);

// ✅ Guard first
if (!messages) return <Skeleton />;
const items = messages.map(m => m.text);
```

**A refactor is not complete until every consumer is updated.**

### Refactor as an upgrade opportunity

Every time you touch a selector's consumers, treat it as a chance to improve the component:

- Replace inline null guards with `next/dynamic` lazy loading
- Replace ad-hoc loading states with purpose-built skeleton components
- Ensure skeletons are dimensionally identical to prevent layout shift
- Split `useAppSelector` calls that return objects into separate primitive calls

---

---

## Fetch Status: The Authoritative Source for "What Data This Record Has"

Never infer data availability from field presence (e.g., checking `_loadedFields.has("messages")`). A field can arrive via any number of narrower fetches and will produce a false positive. The **thunk is the only code that knows exactly what it fetched** — so the thunk is where readiness is declared.

### The pattern

The slice holds a `_fetchStatus` string on every record. Thunks set it after a successful fetch. Selectors read it and return booleans for each UI use case.

```ts
// types.ts — fetch status levels in precedence order
type AgentFetchStatus =
  | "list"           // name, description, access metadata (card display)
  | "execution"      // + variableDefinitions, contextSlots
  | "customExecution"// + settings, tools, model
  | "full"           // full SELECT * (builder / editor)
  | "versionSnapshot"// full version snapshot (read-only)
```

The slice enforces one-directional precedence: status only upgrades, never downgrades. `full` will overwrite `execution`; `versionSnapshot` is the ceiling and cannot be overwritten by anything.

### One boolean selector per UI use case

Build on the existing `selectAgentFetchStatus` primitive. Each selector is a pure comparison — safe with `useAppSelector`.

```ts
// ✅ Card display — needs name + description
export const selectAgentReadyForDisplay = createSelector(
  [selectAgentFetchStatus],
  (status): boolean =>
    status === "list" || status === "full" || status === "versionSnapshot",
);

// ✅ Minimal execution — variableDefinitions + contextSlots
export const selectAgentReadyForExecution = createSelector(
  [selectAgentFetchStatus],
  (status): boolean =>
    status === "execution" || status === "customExecution" ||
    status === "full" || status === "versionSnapshot",
);

// ✅ Custom execution — adds settings, tools, model
export const selectAgentReadyForCustomExecution = createSelector(
  [selectAgentFetchStatus],
  (status): boolean =>
    status === "customExecution" || status === "full" || status === "versionSnapshot",
);

// ✅ Builder / editor — full SELECT * required
export const selectAgentReadyForBuilder = createSelector(
  [selectAgentFetchStatus],
  (status): boolean => status === "full" || status === "versionSnapshot",
);

// ✅ Version panel — snapshot only
export const selectAgentReadyForVersionDisplay = createSelector(
  [selectAgentFetchStatus],
  (status): boolean => status === "versionSnapshot",
);
```

### How the thunk sets it

```ts
// Partial fetch (list, execution, customExecution): dispatch the action explicitly
dispatch(setAgentFetchStatus({ id, status: "list" }));

// Full fetch: upsertAgent sets it automatically based on record.isVersion
dispatch(upsertAgent(dbRowToAgentDefinition(data)));
// → sets "full" for live agents, "versionSnapshot" for version records
```

### Using the boolean selector in a component

```tsx
// ✅ Gate the builder on the authoritative status — not field presence
const isReadyForBuilder = useAppSelector((state) =>
  selectAgentReadyForBuilder(state, agentId),
);

useEffect(() => {
  if (!isReadyForBuilder) dispatch(fetchFullAgent(agentId));
}, [agentId]);

if (!isReadyForBuilder) return <AgentBuilderSkeleton />;
```

### ❌ Never do this

```ts
// ❌ Field presence is not authoritative — messages could have arrived
// from a different, narrower fetch (e.g. a messages-only endpoint)
const isReady = record?._loadedFields.has("messages") ?? false;

// ❌ Local state duplicating what the slice already tracks
const [isLoading, setIsLoading] = useState(false);
dispatch(fetchFullAgent(id)).finally(() => setIsLoading(false));
```

---

## Quick Reference

| Return type | Safe? | Fix |
|---|---|---|
| Primitive | ✅ | None |
| Existing object ref from state | ✅ | None |
| `.filter()` / `.map()` result | ❌ new array | Wrap in `createSelector` |
| `?? []` / `?? {}` / `?? null` | ❌ new ref when undefined | Remove default, guard in component |
| `{ a: state.a, b: state.b }` | ❌ new object | Separate `useAppSelector` calls or `shallowEqual` |

## Debugging

If you see *"Selector returned a different result when called with the same parameters"*:

1. Check for `??`, `||`, or default values in the selector — remove them.
2. Check for `.filter()`, `.map()`, or object construction in input selectors — move to result function.
3. Use `selector.recomputations()` and `selector.dependencyRecomputations()` to trace what's recalculating.

---

## Real-World Example: Replacing a Hook with Selectors

### The Anti-Pattern: a hook that manages "derived display state"

A common mistake is reaching for `useState` + `useEffect` when all you need is a selector. This hook existed to pick the best available title for an agent execution instance:

```ts
// ❌ WRONG — useEffect/useState for pure state derivation
export function useAnimatedTitle(instanceId: string) {
  const resolvedTitle = useInstanceTitle(instanceId);   // another hook
  const conversationTitle = useAppSelector(selectConversationTitle(instanceId));

  const [displayTitle, setDisplayTitle] = useState(resolvedTitle ?? "Agent");
  const prevRef = useRef<string | null>(null);

  useEffect(() => {
    if (conversationTitle && conversationTitle !== prevRef.current) {
      prevRef.current = conversationTitle;
      setDisplayTitle(conversationTitle);
    }
  }, [conversationTitle]);

  useEffect(() => {
    if (!conversationTitle && resolvedTitle) {
      setDisplayTitle(resolvedTitle);
    }
  }, [resolvedTitle, conversationTitle]);

  return displayTitle;
}
```

Problems:
- Two `useEffect` calls managing state that is already in Redux
- `useRef` tracking a "previous value" that Redux already tracks
- Every dispatch causes the outer selector to run, then maybe triggers a state update, causing a second render
- `resolvedTitle ?? "Agent"` in `useState` initial value: if `resolvedTitle` is undefined on first render, `displayTitle` starts as `"Agent"` and stays there until the next effect fires — a stale render

### The Correct Pattern: tiered inline selectors

The same logic as a set of plain selectors — all primitive reads, no new references, single render per change:

```ts
// ✅ Tier 1 — agent name only (string | undefined)
export const selectInstanceAgentName =
  (instanceId: string) =>
  (state: RootState): string | undefined => {
    const agentId = state.executionInstances.byInstanceId[instanceId]?.agentId;
    if (!agentId) return undefined;
    return state.agentDefinition.agents?.[agentId]?.name || undefined;
  };

// ✅ Tier 2 — shortcut label → agent name → undefined
export const selectInstanceTitle =
  (instanceId: string) =>
  (state: RootState): string | undefined => {
    const instance = state.executionInstances.byInstanceId[instanceId];
    if (!instance) return undefined;
    if (instance.shortcutId) {
      const label = state.agentShortcut?.[instance.shortcutId]?.label;
      if (label) return label;
    }
    if (instance.agentId) {
      const name = state.agentDefinition.agents?.[instance.agentId]?.name;
      if (name) return name;
    }
    return undefined;
  };

// ✅ Tier 3 — conversationTitle → shortcutLabel → agentName → "Agent"
// Always returns a string. Use for title bars that must never be empty.
export const selectInstanceDisplayTitle =
  (instanceId: string) =>
  (state: RootState): string => {
    const conversationTitle =
      state.instanceConversationHistory.byInstanceId[instanceId]?.title;
    if (conversationTitle) return conversationTitle;

    const instance = state.executionInstances.byInstanceId[instanceId];
    if (!instance) return "Agent";

    if (instance.shortcutId) {
      const label = state.agentShortcut?.[instance.shortcutId]?.label;
      if (label) return label;
    }
    if (instance.agentId) {
      const name = state.agentDefinition.agents?.[instance.agentId]?.name;
      if (name) return name;
    }
    return "Agent";
  };
```

**Why this works:**
- Each read is a primitive string — `===` comparison catches all changes
- The `"Agent"` fallback is a string literal, not a new reference — it's always `=== "Agent"`
- No `useState`, no `useEffect`, no `useRef` — zero extra renders
- Each tier is independently usable: pre-execution UI calls Tier 1 (agent name only), title bars call Tier 3

**In the component:**

```tsx
// Before — hook with hidden re-render complexity
const { displayTitle } = useAnimatedTitle(instanceId);

// After — one selector call, one render per value change
const displayTitle = useAppSelector(selectInstanceDisplayTitle(instanceId));
```
