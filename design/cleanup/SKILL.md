---
name: react/migration/cleanup
description: >-
  Clean up or roll back React migrations: remove old state owners, providers,
  hooks, adapters, wrappers, and stale imports; document temporary shims.
type: sub-skill
requires:
  - react/migration
triggers:
  - React migration cleanup
  - delete old React state owner
  - React migration rollback
---
# React migration cleanup and rollback

Run cleanup once each migrated React state owner/slice passes tests and affected UI flows have been verified. Remove old providers, custom hooks, context modules, external-store adapters, and pass-through wrappers unless they are explicitly documented compatibility shims.

React cleanup targets React state owner modules such as providers, hooks, context
files, and old external store adapters.

## Remove old owners and imports

Verify zero references with targeted searches for the old owner path, provider, hook names, and context names. Examples:

- `grep -rn "CartProvider" src/ --include="*.ts" --include="*.tsx"`
- `grep -rn "useCartContext" src/ --include="*.ts" --include="*.tsx"`
- `grep -rn "from .*cart-context" src/ --include="*.ts" --include="*.tsx"`

Do not leave a one-line re-export or delegate-only wrapper that keeps the old module path alive. Remove it, inline it, or document it as a temporary shim with a sunset condition.

## Cleanup evidence

```ts
type ReactCleanupEvidence = {
  migratedSlice: string;
  removedOwners: string[];
  remainingOldPathMatches: string[];
  passThroughWrappers: string[];
  documentedShims: Array<{ path: string; removalCondition: string }>;
  verification: string[];
};

export const cartCleanupEvidence: ReactCleanupEvidence = {
  migratedSlice: "cart",
  removedOwners: ["src/cart/CartProvider.tsx", "src/cart/useCartContext.ts"],
  remainingOldPathMatches: [],
  passThroughWrappers: [],
  documentedShims: [],
  verification: ["cart reducer tests", "cart saga tests", "cart component tests"],
};
```

## Compatibility shim requirements

```ts
/**
 * Compatibility shim for plugin-cart@2.x until plugin-cart >= 3.0 is required.
 * New callers must import from "../store/cart/cart-selectors".
 */
export { selectCartTotal } from "../store/cart/cart-selectors";
```

Every shim must state the compatibility consumer, the removal condition, and the new import path. Verifier output should say either “no pass-through wrappers” or list each documented shim.

## Rollback recipe

If the migrated slice regresses:

1. Restore the old provider/hook/context files from git history.
2. Remove the new reducer map entry from the `ReactStore` constructor.
3. Remove the matching `reactStore.runSaga(sagaFn)` startup call.
4. Restore affected component imports.
5. Re-run tests for the restored React path.

## Final checklist per slice

- [ ] Reducer registered in the ReactStore reducer map.
- [ ] App saga started after `reactStore.init()` when the slice has side effects.
- [ ] Components/custom hooks use direct selector signals first; any
  `.useValue(...args)` reads are documented as necessary plain-value fallbacks.
- [ ] Handlers/tests use `.select(reactStore.state, ...args)`.
- [ ] Old providers/hooks/context/external-store adapters removed or documented as compatibility shims.
- [ ] Targeted searches confirm zero stale imports.
- [ ] Tests and affected UI checks pass.

## Bad: deleting while consumers still import old context

```ts
// BAD: consumersStillImportingOldPath must be empty before deleting the provider.
export const badCleanupPlan = {
  oldOwnerPath: "src/cart/CartProvider.tsx",
  consumersStillImportingOldPath: ["HeaderCartButton.tsx", "Checkout.tsx"],
  deleteOldOwnerNow: true,
};
```