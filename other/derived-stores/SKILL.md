---
name: react/migration/derived-stores
description: >-
  Move shared React useMemo, hook/context derivations, and repeated render
  calculations to ReactStore selector definitions; route consumption to
  selector-lifecycle.
type: sub-skill
requires:
  - react/selectors
  - react/migration
triggers:
  - migrate React derived state
  - useMemo to selector
  - derived hook to selector
---
# React derived state migration

Shared React derivations move to `reactStore.createSelector(...)`. This leaf
maps old calculations to selector definitions; choose consumption and test APIs
using [Call-mode map](../../selector-lifecycle/SKILL.md#call-mode-map).

React sources include duplicated `useMemo`, derived custom-hook return values,
context selector helpers, and render-time calculations reused across components.

## Before: duplicated React derivation

```tsx
import * as React from "react";
import { useCartContext } from "./CartProvider";

export function CartSummary() {
  const { items, discountCode } = useCartContext();
  const subtotal = React.useMemo(() => items.reduce((sum, item) => sum + item.price, 0), [items]);
  const total = discountCode ? subtotal * 0.9 : subtotal;
  return <span>{total}</span>;
}
```

## After: Store-bound selectors

Migrate cart entity records to a `Collection<CartItem, "id">` in the `cart`
reducer's `collection` field. Materialize an array only as derived output with
`getItems`; do not preserve the legacy object array as canonical Redux state.
The shared Collection policy applies to React too; primitive arrays remain valid.

```ts
import { reactStore } from "../react-store";
import { getItems } from "@themislib/themis/utils/collections/collection-utils";

export const selectCartItems = reactStore.createSelector((state) => getItems(state.cart.collection));
export const selectDiscountCode = reactStore.createSelector((state) => state.cart.discountCode);
export const selectCartSubtotal = reactStore.createSelector((state) => {
  return selectCartItems.select(state).reduce((sum, item) => sum + item.price, 0);
});
export const selectCartTotal = reactStore.createSelector((state) => {
  const subtotal = selectCartSubtotal.select(state);
  return selectDiscountCode.select(state) ? subtotal * 0.9 : subtotal;
});
```

## Component and test consumption

The migrated read below is signal-aware. Apply
[React signal consumption guardrails](../../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails)
for `.value` tracking and any necessary plain-value fallback boundary.

```tsx
import { selectCartTotal } from "../store/cart/cart-selectors";

export function CartSummary() {
  const total = selectCartTotal();
  return <span>{total.value}</span>;
}
```

```ts
import { expect, it } from "vitest";
import { selectCartTotal } from "../store/cart/cart-selectors";
import { reactStore } from "../react-store";
import { createCollection } from "@themislib/themis/utils/collections/collection-utils";

it("selects the cart total from explicit state", () => {
  const disposeStore = reactStore.init();
  try {
    // Read state only after this test initializes its runtime; retain other domains.
    const mockState = {
      ...reactStore.state,
      cart: { collection: createCollection("id", [{ id: "a", price: 10 }]), discountCode: null },
    };
    expect(selectCartTotal.select(mockState)).toBe(10);
  } finally {
    disposeStore();
  }
});
```

Importing the test only registers it; initialization, state reads, and cleanup
happen inside the test callback. This test owns the configured Store runtime for
its duration, so do not run it concurrently with other tests using that instance.
The `.select(mockState)` call itself is pure and needs no live runtime if a test
supplies a complete state fixture instead of reading `reactStore.state`.

## Parameterized selectors

```ts
export const selectTodoById = reactStore.createSelector((state, id: string) => {
  return state.todos.byId[id];
});

export const selectTodoTitle = reactStore.createSelector((state, id: string) => {
  return selectTodoById.select(state, id)?.title ?? "Untitled";
});
```

## Rules

- One selector per shared derivation; keep selectors narrow and pure.
- Compose upstream selectors with `.select(state, ...args)` inside selector bodies.
- Verify migrated consumer boundaries using
  [Verification cues](../../selector-lifecycle/SKILL.md#verification-cues), not a
  migration-specific call-mode policy.
- Do not store selector outputs in reducers; reducers own base state only.
- Store entity records in Collections and derive arrays at the selector boundary;
  follow `../../../core/collections/SKILL.md`, not the legacy context shape.

## Bad: direct signal form inside selector composition

```ts
// BAD: selector callbacks must stay pure and synchronous against the provided state.
export const selectBadTotal = reactStore.createSelector(() => {
  return selectCartSubtotal().value;
});
```

## Cross-references

- `../../selectors/SKILL.md` — selector authoring and caching.
- `../../selector-lifecycle/SKILL.md` — direct signal, `.useValue`, `.select`, `.effect`, and `.withStore` choices.
- `../component-migration/SKILL.md` — component consumption after migration.