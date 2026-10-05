---
name: svelte/migration/cleanup
description: >-
  Use after migrating a Svelte store to remove old .store.svelte.ts files,
  check residual references, verify the migrated slice, or roll back a
  regression.
type: sub-skill
requires:
  - svelte/migration
triggers:
  - delete old store
  - verify no references
  - migration rollback
  - migration cleanup
---
# Migration — Cleanup and Rollback

> Final step of `../SKILL.md` → **Recommended Order**, plus the rollback recipe. Run this once per slice, only after the new slice passes tests and the UI flows have been verified.

## Remove Old Store Files

Delete the old store file only after tests and UI checks pass. Verify zero references with targeted searches such as `grep -rn "{old-store}.store" src/` and `grep -rn "from.*stores/{old-store}" src/`; both must return no results.

Do not replace the deleted store with a barrel, re-export, or proxy module that keeps the old import path alive. After a migration or refactor, the old module path must be removed, inlined into the new owner, or explicitly kept as a compatibility shim.

## Pass-Through Wrapper Guard

Check every old path touched by the migration, not only the `.store.svelte.ts` file. Thin wrappers include:

- `export { ... } from "new/path"` or `export * from "new/path"`
- imports from the new file followed by identical exports
- functions/classes whose only behavior is calling the new implementation

Intentional shims must be rare and documented next to the shim with:

1. The compatibility consumer or release window that still imports the old path
2. The sunset/removal condition
3. The new import path callers should use

Verifier output must say either “no pass-through wrappers” or list each documented compatibility shim and its removal condition.

## Rollback Strategy

Keep migrations in small, independently verifiable technical increments. Retain
the old store until the replacement is verified, and preserve a recoverable
baseline through the active workflow before deleting it. Follow **Workflow
ownership** below for any branch, commit, PR, or history operation.

## Workflow ownership

Branching, commits, PR sizing, and rollback commands are governed by the active
user/task/repository instructions. This skill does not require a branch, commit,
or PR per store and does not authorize destructive history changes. Technical
rollback scope remains the complete migrated owner and its consumers.

### Reverting a migration

When rollback is authorized, restore the old store and affected consumers from the approved baseline; remove the replacement slice, matching reducer constructor entry, and matching `store.runSaga(sagaFn)` startup call as one technical unit. Re-run affected tests and UI checks so there is only one active owner.

### Minimizing risk

- **Run all existing tests** after each store migration
- **Manually test affected UI flows** before handoff
- **Keep technical increments small**; use **Workflow ownership** for VCS policy
- **Verify zero references** to the old store before deleting it: `grep -rn "{old-store}" src/ --include="*.ts" --include="*.svelte"`

## Final Checklist Per Slice

- [ ] Reducer registered in the configured Store constructor map
- [ ] Any app saga explicitly started with owned cancellation, per `../../store/SKILL.md` → **App saga lifetime**
- [ ] All consuming components updated (see `../component-migration/SKILL.md`)
- [ ] All tests pass
- [ ] Manual UI verification done on affected flows
- [ ] Old `.store.svelte.ts` file deleted
- [ ] `grep` confirms zero references to the old store path
- [ ] Old module paths checked for one-line re-export/proxy/delegate leftovers
- [ ] Any remaining compatibility shim documents the reason and sunset/removal condition
- [ ] Handoff identifies the migrated slice and follows **Workflow ownership**

## Cleanup Examples

### Document a temporary compatibility shim

```typescript
/**
 * Compatibility shim for plugin-cart@2.x until that plugin releases its
 * cart selector migration. Remove after plugin-cart >= 3.0 is required.
 * New callers must import from "$lib/store/slices/cart/cart-selectors".
 */
export { selectCartTotal } from "$lib/store/slices/cart/cart-selectors";
```

### Record per-slice cleanup evidence

Record actual search queries/results, consumer import replacements, tests, UI
flows, and wrapper/shim findings together. This example is a report shape, not
proof of a run: only delete when tests/UI pass and old-path searches are empty.
If `Header.svelte` or `Checkout.svelte` still imports the old store, deletion is
unsafe regardless of whether the replacement itself passes tests.

```typescript
export const cartCleanupReport = {
  slice: "cart",
  removedStoreFiles: ["src/lib/stores/cart.store.svelte.ts"],
  searches: [
    { query: "cart.store.svelte", matches: [] },
    { query: "from.*stores/cart", matches: [] },
  ],
  importReplacements: [{
    consumer: "src/routes/cart/CartSummary.svelte",
    removedImport: "$lib/stores/cart.store.svelte",
    addedImports: [
      "$lib/store/slices/cart/cart-selectors",
      "$lib/store/slices/cart/cart-slice",
      "$lib/store/store",
    ],
  }],
  passThroughWrappers: [],
  documentedShims: [],
  verification: ["cart reducer tests", "cart saga tests", "cart checkout manual flow"],
};
```