---
name: react/migration/assessment
description: >-
  Assess ReactStore adoption: inventory React state, context/hooks, external stores,
  derivations, effects, and consumers; distinguish shared/persistent/async state
  from component-local UI.
type: sub-skill
requires:
  - react
  - react/migration
  - core/core-policy
triggers:
  - audit React state
  - classify React state
  - React migration inventory
---
# React migration assessment

Before editing, inventory current React state ownership and decide what moves to `ReactStore` versus what stays local.

## Identify React state owners

Search for state and effect patterns in React files:

- `useState`, `useReducer`, and reducer-like custom hooks.
- Context providers and `useContext` consumers.
- Shared custom hooks that return mutable state, setters, or derived values.
- External stores, event emitters, browser storage, or subscription wrappers.
- `useMemo`/derived values reused across components.
- `useEffect` blocks with fetches, timers, storage, subscriptions, or IPC.

## Decision framework

Classify each inventoried React owner using
[When to use Redux vs component-local state](../../../core/core-policy/SKILL.md#when-to-use-redux-vs-component-local-state).
For effects and shared derivations, apply
[Setup — core rules](../../../core/core-policy/SKILL.md#setup--core-rules).
This leaf owns React-pattern inventory and evidence, not a separate placement
policy. Record the matched policy criterion and all consumers, including
services/non-component code; do not infer ownership from the hook name alone.

## Assessment output

Produce evidence that downstream migration leaves can consume:

```ts
type ReactStatePattern = "useState" | "useReducer" | "context" | "custom-hook" | "external-store" | "useMemo" | "useEffect";
type ReactMigrationVerdict = "reactstore" | "local";

type ReactStateInventoryRecord = {
  owner: string;
  patterns: ReactStatePattern[];
  stateFields: string[];
  derivedValues: string[];
  sideEffects: string[];
  consumers: string[];
  policyReason: string;
  verdict: ReactMigrationVerdict;
  nextSkills: string[];
};

export const cartInventory: ReactStateInventoryRecord = {
  owner: "src/cart/CartProvider.tsx",
  patterns: ["context", "useReducer", "useMemo", "useEffect"],
  stateFields: ["items", "couponCode"],
  derivedValues: ["itemCount", "subtotal"],
  sideEffects: ["localStorage sync"],
  consumers: ["CartSummary.tsx", "HeaderCartButton.tsx"],
  policyReason: "Shared business state with persisted storage synchronization",
  verdict: "reactstore",
  nextSkills: ["setup", "writable-stores", "derived-stores", "side-effects", "component-migration"],
};
```

## Bad assessment example

```ts
// BAD: a single button's hover state should remain local React state.
export const hoverInventory = {
  owner: "src/products/ProductCard.tsx",
  stateFields: ["isHovered"],
  consumers: ["ProductCard.tsx"],
  verdict: "reactstore",
};
```

## Downstream routing

- Mutable shared state → `../writable-stores/SKILL.md`.
- Shared derivations → `../derived-stores/SKILL.md`.
- Shared async/persistent effects → `../side-effects/SKILL.md`.
- JSX/TSX consumers → `../component-migration/SKILL.md`.
- Old owners/import paths → `../cleanup/SKILL.md`.