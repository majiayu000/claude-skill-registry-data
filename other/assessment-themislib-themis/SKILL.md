---
name: svelte/migration/assessment
description: >-
  Start Svelte-to-Themis migrations by inventorying stores/runes and
  consumers, classifying state, derivations, and effects, and deciding shared
  Redux versus component-local state.
type: sub-skill
requires:
  - svelte
  - svelte/migration
  - core/core-policy
triggers:
  - audit stores
  - classify store
  - migration inventory
  - shared or local
---
# Migration — Assessment Phase

> Before writing any code, inventory the current state management and decide what moves to Redux.

## 1. Identify All Stores

Use repository searches such as `find src/ -name "*.store.svelte.ts" -o -name "*.store.ts"`, `grep -rn "writable\|readable\|derived" src/ --include="*.ts" --include="*.svelte"`, and `grep -rn '\$state\|\$derived' src/ --include="*.store.svelte.ts"`. Record results as structured assessment evidence so downstream skills can consume them.

## 2. Classify Each Store

For each store file, determine:

1. **What state does it hold?** List all `writable()`, `$state`, or reactive fields
2. **What derived values exist?** List all `derived()`, `$derived`, getters
3. **What side effects exist?** localStorage, fetch, event listeners, timers, IPC
4. **Who consumes it?** Which components import and use this store?
5. **Is it shared or local?** Used by multiple components, or just one?

## Decision Framework

Apply `../../../core/core-policy/SKILL.md` → **Setup — core rules** to each
field/effect, not just the file's syntax. Redux owns shared/domain state, including
persisted or externally synchronized business state. Purely visual, ephemeral,
instance-local fields stay local. A timer or `await` alone does not make UI state
domain-owned; DOM-local focus, scroll, measurement, and widget lifecycle stay in
the component. Record the owner, consumers, persistence needs, and cancellation
lifetime before choosing a migration leaf. If that evidence is unclear, resolve
the ownership question rather than defaulting every local field/effect to Redux.

## Output of the Assessment

Produce a per-store table so you can order the migration (simplest / most isolated slice first — see `../SKILL.md` for the recommended order and `../setup/SKILL.md` for the bootstrap that must be done before the first slice):

| Store file | State fields | Derived | Side effects | Consumers | Verdict |
| --- | --- | --- | --- | --- | --- |
| cart.store.svelte.ts | items, total | count | localStorage sync | Cart, Header, Checkout | Redux |
| tooltip.store.svelte.ts | open | — | — | Tooltip only | Local |

Downstream skills consume this table:

- `../writable-stores/SKILL.md` — for shared/domain `writable` / `$state` fields
- `../derived-stores/SKILL.md` — for shared/domain `derived` / `$derived` values
- `../side-effects/SKILL.md` → **Effect ownership boundary** — for domain effects, not DOM-local lifecycle
- `../component-migration/SKILL.md` — for the migrated consumers column
- `../cleanup/SKILL.md` — to confirm deletion order only after a replacement owner is verified

## Examples in This Skill

- Added: assessment record type; shared writable verdict; component-local verdict; derived selector candidate; side-effect saga candidate; bad local-UI overmigration verdict.
- Retained: none (this assessment skill previously had no JS/TS examples).

## Assessment Examples

### 1. Capture inventory as structured evidence

```typescript
type StorePrimitive = "writable" | "readable" | "derived" | "$state" | "$derived" | "$effect";
type MigrationVerdict = "redux" | "local";

type StoreInventoryRecord = {
  file: string;
  primitives: StorePrimitive[];
  stateFields: string[];
  derivedValues: string[];
  sideEffects: string[];
  consumers: string[];
  verdict: MigrationVerdict;
  nextSkills: string[];
};

const cartInventory: StoreInventoryRecord = {
  file: "src/lib/stores/cart.store.svelte.ts",
  primitives: ["writable", "derived", "$effect"],
  stateFields: ["items"],
  derivedValues: ["total", "itemCount"],
  sideEffects: ["localStorage sync"],
  consumers: ["Cart.svelte", "Header.svelte", "Checkout.svelte"],
  verdict: "redux",
  nextSkills: ["writable-stores", "derived-stores", "side-effects", "component-migration"],
};
```

### Classify shared writable state as Redux-owned

```typescript
// Evidence for a verdict made using core policy, not a replacement classifier.
export const cartVerdict = {
  consumers: ["Cart.svelte", "Header.svelte"],
  persists: true,
  businessLogic: true,
  verdict: "redux",
  reason: "Shared checkout domain state persisted across navigation",
};
```

### 3. Keep ephemeral component state local

```typescript
type LocalStateFinding = {
  file: string;
  field: string;
  reason: "single-component" | "ephemeral-ui";
  replacement: "component-local-state";
};

export const tooltipFinding: LocalStateFinding = {
  file: "src/lib/stores/tooltip.store.svelte.ts",
  field: "open",
  reason: "ephemeral-ui",
  replacement: "component-local-state",
};
```

### 4. Route derived values to selector migration

```typescript
type DerivedFinding = {
  source: string;
  dependencies: string[];
  targetSelector: string;
  composeWithSelect: boolean;
};

export const cartTotalFinding: DerivedFinding = {
  source: "derived(items, ($items) => sumCart($items))",
  dependencies: ["items"],
  targetSelector: "selectCartTotal",
  composeWithSelect: true,
};
```

### 5. Route side effects to saga migration

```typescript
type SideEffectFinding = {
  sourceFile: string;
  effect: "fetch" | "timer" | "subscription" | "storage" | "ipc";
  triggerAction: string;
  targetSaga: string;
};

export const persistenceFinding: SideEffectFinding = {
  sourceFile: "src/lib/stores/cart.store.svelte.ts",
  effect: "storage",
  triggerAction: "cart/setItems",
  targetSaga: "cartSaga",
};
```

### 6. ❌ Bad: migrate single-component UI state to Redux

```typescript
// ❌ BAD: hover state belongs in the component, not in a Redux slice.
type BadAssessmentRecord = {
  file: string;
  stateFields: string[];
  consumers: string[];
  verdict: "redux" | "local";
};

export const badHoverAssessment: BadAssessmentRecord = {
  file: "src/lib/stores/card-hover.store.svelte.ts",
  stateFields: ["isHovered"],
  consumers: ["ProductCard.svelte"],
  verdict: "redux",
};
```

## Cases Covered

| Case | Example |
| --- | --- |
| Inventory shape for downstream skills | Capture inventory as structured evidence |
| Shared/persisted/business state | Classify shared writable state as Redux-owned |
| Local-only UI state | Keep ephemeral component state local |
| Derived values | Route derived values to selector migration |
| Effects/subscriptions/storage | Route side effects to saga migration |
| Incorrect overmigration | Bad: migrate single-component UI state to Redux |