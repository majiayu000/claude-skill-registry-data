---
name: react/migration/writable-stores
description: >-
  Move shared React useState/useReducer, context, custom-hook, or external-store
  state to actions and reducers; preserve local-state verdicts.
type: sub-skill
requires:
  - core/actions
  - core/reducers
  - core/core-policy
  - core/state-serialization
  - react/migration
triggers:
  - migrate React local state
  - useState to slice
  - context state to reducer
---
# React mutable state migration

Shared mutable React state maps to slice state, actions, and reducers only after
classification with [When to use Redux vs component-local state](../../../core/core-policy/SKILL.md#when-to-use-redux-vs-component-local-state).
Keep the assessment's local-state verdicts; this leaf owns the React migration
mapping, not the core state/action/reducer contracts.

React source patterns include `useState`, `useReducer`, context provider state,
custom hook state, and external mutable stores.

## Before: shared React context state

```tsx
import * as React from "react";

type CounterContextValue = { count: number; increment(): void; setUsername(name: string): void };
export const CounterContext = React.createContext<CounterContextValue | null>(null);

export function CounterProvider({ children }: { children: React.ReactNode }) {
  const [count, setCount] = React.useState(0);
  const [username, setUsername] = React.useState("");
  const increment = () => setCount((value) => value + 1);
  return <CounterContext.Provider value={{ count, increment, setUsername }}>{children}</CounterContext.Provider>;
}
```

## After: slice state, actions, reducer

| React source in the example | Migrated owner |
| --- | --- |
| Provider `count` and `username` state | Canonical fields in the counter slice |
| `setCount` / `setUsername` setters | Named actions carrying the new primitive value |
| Functional `increment` setter | Event action handled by the counter reducer |
| Context consumers | Store-bound selectors plus configured Store dispatch |

Implement the mapped actions using [Examples](../../../core/actions/SKILL.md#examples)
(no-payload events and tuple payloads), and implement the reducer using
[Examples](../../../core/reducers/SKILL.md#examples) (handler chaining and
same-reference no-ops). Do not create migration-local copies of those APIs.
Then migrate JSX/TSX consumers with
[After: direct selector signal plus Store dispatch](../component-migration/SKILL.md#after-direct-selector-signal-plus-store-dispatch).

## Core implementation contracts

- State placement is decided by [When to use Redux vs component-local state](../../../core/core-policy/SKILL.md#when-to-use-redux-vs-component-local-state).
- Pure immutable transitions and no-op identity follow [Do](../../../core/reducers/SKILL.md#do)
  and [Don't](../../../core/reducers/SKILL.md#dont); components dispatch rather than owning the transition.
- Every migrated field, including nested values and objects previously held by
  React providers, must meet [Do](../../../core/state-serialization/SKILL.md#do)
  and the complete [Don't](../../../core/state-serialization/SKILL.md#dont)
  serialization exclusions. Do not substitute a shorter migration-specific list.
- Add/update serialization tests for initial state and changed reducer paths
  according to [Verification cues](../../../core/state-serialization/SKILL.md#verification-cues)
  and [JSON round-trip regression test](../../../core/state-serialization/SKILL.md#json-round-trip-regression-test).
  Verify reducer transitions and no-op identity with
  [Verification cues](../../../core/reducers/SKILL.md#verification-cues).

## Component-local state remains local

```tsx
import * as React from "react";

export function ProductCard() {
  const [isHovered, setHovered] = React.useState(false);
  return <article onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)} />;
}
```

## Bad: reducer side effect

Do not carry a provider's persistence into its replacement reducer. The forbidden
operations remain in [Don't](../../../core/reducers/SKILL.md#dont); migrate that
work separately via [Conversion recipes](../side-effects/SKILL.md#conversion-recipes).

## Cross-references

- `../../../core/actions/SKILL.md` — action creators.
- `../../../core/reducers/SKILL.md` — reducer patterns.
- `../../../core/state-serialization/SKILL.md` — serializable state rules.