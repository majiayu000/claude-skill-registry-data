---
name: react/migration
description: >-
  Adopt ReactStore by migrating shared React state/context/hooks, external stores,
  useMemo derivations, and useEffect side effects to selectors, actions, reducers,
  and sagas.
type: lifecycle
requires:
  - react
  - core/core-policy
sources:
  - ./assessment/SKILL.md
  - ./setup/SKILL.md
  - ./writable-stores/SKILL.md
  - ./derived-stores/SKILL.md
  - ./side-effects/SKILL.md
  - ./component-migration/SKILL.md
  - ./cleanup/SKILL.md
triggers:
  - React migration
  - migrate React state
  - replace React context state
  - migrate useEffect side effect
  - ReactStore adoption
---
# React migration — React state/context/effects to ReactStore

Use this index when a React app is adopting `themis` and the current
state owner is `useState`, `useReducer`, React context, custom hooks, external
stores, component `useMemo` derivations, or `useEffect` side effects.

## React migration policy

Apply [When to use Redux vs component-local state](../../core/core-policy/SKILL.md#when-to-use-redux-vs-component-local-state)
to each React owner, and [Setup — core rules](../../core/core-policy/SKILL.md#setup--core-rules)
to derived-state and effect ownership. These are the canonical placement rules;
this index owns migration sequencing, not a separate state policy. Record the
React-specific evidence with [Decision framework](./assessment/SKILL.md#decision-framework).

Migrate one state owner/slice at a time, keeping the app on `ReactStore`.
Signal-first reads and necessary plain-value fallbacks follow
[Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map), including handler,
test, composition, and saga boundaries.

## React migration leaf routes

| Route | Use when |
| --- | --- |
| `./assessment/SKILL.md` | Inventory shared React local state, context/hooks, external stores, derivations, effects, and consumers. |
| `./setup/SKILL.md` | Confirm migration readiness against canonical installation and React runtime owners; not greenfield bootstrap instructions. |
| `./writable-stores/SKILL.md` | Move shared mutable React state into actions, reducers, and serializable slice state. |
| `./derived-stores/SKILL.md` | Move shared derivations to `ReactStore` selectors and test them with `.select`. |
| `./side-effects/SKILL.md` | Move shared, persistent, or async effects to sagas. |
| `./component-migration/SKILL.md` | Migrate JSX/TSX consumption to direct selector signals and Store dispatch. |
| `./cleanup/SKILL.md` | Remove old state owners/import paths and document shims or rollback steps. |

## Recommended order

1. `./assessment/SKILL.md` — inventory React state owners, derivations, effects, and
   consumers; classify shared vs component-local.
2. `./setup/SKILL.md` — complete the [Adoption checkpoint](./setup/SKILL.md#adoption-checkpoint).
   For first-time installation/family choice, start at
   [Store-family decision gate](../../setup/SKILL.md#store-family-decision-gate);
   for runtime mechanics use [Create and configure ReactStore](../component-integration/SKILL.md#create-and-configure-reactstore).
3. `./writable-stores/SKILL.md` — move shared mutable React state to serializable slice
   state, actions, and pure reducers.
4. `./derived-stores/SKILL.md` — move shared derivations to selectors and test them.
5. `./side-effects/SKILL.md` — migrate effects selected by core policy.
6. `./component-migration/SKILL.md` — replace consumers using the canonical
   [Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map) and Store-first dispatch.
7. `./cleanup/SKILL.md` — remove old providers/hooks/state owner modules after verification.

## Quick reference

| React source pattern | ReactStore target |
| --- | --- |
| Shared `useState` / `useReducer` state | Slice initial state + actions + reducer |
| Context provider that stores business state | `ReactStore` reducer map + selectors/actions |
| Custom hook exposing shared mutable state | [Custom hook migration](./component-migration/SKILL.md#custom-hook-migration) + action dispatch |
| External mutable store subscription | Reducer state + saga/channel integration as needed |
| Repeated `useMemo`/derived hook value | `reactStore.createSelector(...)` |
| `useEffect` business fetch/timer/storage sync | [Conversion recipes](./side-effects/SKILL.md#conversion-recipes) after policy classification |
| Render/handler/test/composition read | [Call-mode map](../selector-lifecycle/SKILL.md#call-mode-map) |

## Orchestration example

```ts
type ReactMigrationStep =
  | "setup"
  | "writable-stores"
  | "derived-stores"
  | "side-effects"
  | "component-migration"
  | "cleanup";

type ReactStateAssessment = {
  owner: string;
  verdict: "reactstore" | "local";
  patterns: Array<"useState" | "useReducer" | "context" | "useMemo" | "useEffect">;
  consumers: string[];
};

const cartAssessment: ReactStateAssessment = {
  owner: "src/cart/CartProvider.tsx",
  verdict: "reactstore",
  patterns: ["context", "useReducer", "useMemo", "useEffect"],
  consumers: ["CartSummary.tsx", "HeaderCartButton.tsx", "Checkout.tsx"],
};

const nextSteps: ReactMigrationStep[] = cartAssessment.verdict === "reactstore"
  ? ["setup", "writable-stores", "derived-stores", "side-effects", "component-migration", "cleanup"]
  : ["cleanup"];
```

## Verification cues

- React examples import `ReactStore` from `@themislib/themis/react-store` and keep
  selectors Store-bound.
- Consumer migration passes [Verification cues](../selector-lifecycle/SKILL.md#verification-cues).
- Runtime readiness passes [Verification cues](./setup/SKILL.md#verification-cues),
  including saga startup at the React app owner.
- React migration instructions keep state ownership, selector consumption, and
  side-effect ownership explicit at each step.