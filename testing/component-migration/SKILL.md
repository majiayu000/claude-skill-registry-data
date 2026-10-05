---
name: react/migration/component-migration
description: >-
  Plan React JSX/TSX and custom-hook migration to ReactStore selectors and
  Store-first dispatch. Map consumers and rollout order; defer call modes to
  selector-lifecycle.
type: sub-skill
requires:
  - react/component-integration
  - react/selector-lifecycle
  - react/migration
triggers:
  - migrate React component
  - replace React state import
  - selector .useValue component migration
---
# React component migration

Replace old React state/context/custom-hook reads with `ReactStore` selectors,
prefer signal-aware consumers, and dispatch through the configured store.

Choose render, hook, handler, and test entry points using
[Call-mode map](../../selector-lifecycle/SKILL.md#call-mode-map). Apply
[React signal consumption guardrails](../../selector-lifecycle/SKILL.md#react-signal-consumption-guardrails)
to the `.value` reads in the migrated example, including React tracking.

## Before: context/custom hook consumption

```tsx
import { useCartContext } from "./CartProvider";

export function CartButton({ id }: { id: string }) {
  const { items, addItem, removeItem } = useCartContext();
  const item = items.find((candidate) => candidate.id === id);
  return <button onClick={() => item ? removeItem(id) : addItem(id)}>{item ? "Remove" : "Add"}</button>;
}
```

## After: direct selector signal plus Store dispatch

```tsx
import { reactStore } from "../store/react-store";
import { addItem, removeItem } from "../store/cart/cart-slice";
import { selectCartItemById } from "../store/cart/cart-selectors";

export function CartButton({ id }: { id: string }) {
  const item = selectCartItemById(id);
  return (
    <button onClick={() => reactStore.dispatch(item.value ? removeItem(id) : addItem(id))}>
      {item.value ? "Remove" : "Add"}
    </button>
  );
}
```

## Custom hook migration

Record which existing hook contracts can become signal-aware and which must
keep plain values. Follow [Call-mode map](../../selector-lifecycle/SKILL.md#call-mode-map)
and [Fallback hook/plain-value read](../../selector-lifecycle/SKILL.md#fallback-hookplain-value-read)
instead of maintaining a second hook-consumption recipe here.

## Handler one-shot reads

Move old context snapshots to the configured store without introducing a render
subscription. Use [Handler and test one-shot reads](../../selector-lifecycle/SKILL.md#handler-and-test-one-shot-reads)
for the implementation and hook-boundary restrictions.

## Rollout order per component

1. Replace old state/context/custom-hook imports with the new slice actions, selectors, and configured `reactStore` instance.
2. Map each read boundary using [Call-mode map](../../selector-lifecycle/SKILL.md#call-mode-map).
3. Replace writes with `reactStore.dispatch(actionCreator(...))`.
4. Verify both render consumers and one-shot handlers against the lifecycle examples above.
5. Preserve local-state decisions from [Decision framework](../assessment/SKILL.md#decision-framework).
6. Remove obsolete providers/hooks only after all consumers migrate.

## Bad: calling `.useValue` in an event handler

Moving a custom-hook read into an event handler can violate React hook rules.
Check [Pitfalls](../../selector-lifecycle/SKILL.md#pitfalls) before replacing the
old consumer; do not carry its render-only call mode into callbacks.

## Bad: duplicate old and new owners

```tsx
// BAD: writing context state and ReactStore state makes ownership ambiguous.
function badAdd(id: string) {
  legacyCartContext.addItem(id);
  reactStore.dispatch(addItem(id));
}
```

## Cross-references

- `../../component-integration/SKILL.md` — React app bootstrap and dispatch rules.
- `../../selector-lifecycle/SKILL.md` — call-mode guardrails.
- `../cleanup/SKILL.md` — removing obsolete providers/hooks after migration.