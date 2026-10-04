---
description: Create, update, or validate component-scoped utility functions and constants
argument-hint: create|update|validate ComponentName [details]
---

# Writing Utils and Constants Skill

You are a Nimbus utilities specialist. This skill helps you create, update, or
validate component-scoped pure helper functions in `utils/` and constants in
`constants/`.

## Critical Requirements

**Pure helper functions MUST NOT be inlined into the main component file
(`{component}.tsx`).** Every component-scoped utility lives in `utils/` with
its own file, its own spec, and is re-exported through a barrel.

Patterns enforced:

- One purpose per file; cohesive helpers merge into a single file when they
  share a meaningful name token, have a factory relationship, or form a direct
  dependency chain — see [File Organization](../../../docs/file-type-guidelines/utils-and-constants.md#file-organization)
  in `utils-and-constants.md` for the canonical rule
- Sibling `*.spec.ts` per util file (one source file = one spec file)
- `utils/index.ts` barrel re-exporting every util
- Pure functions only — no React, no JSX, no side effects
- JSDoc on every export
- `as const` for constants
- Don't mix promotable and component-coupled helpers in the same file

---

## Mode Detection

Parse the request to determine the operation:

- **create** — Generate new utility/constant files for a component
- **update** — Modify existing utilities or move inlined helpers into `utils/`
- **validate** — Check compliance with guidelines (**PRIMARY USE CASE**)

If no mode is specified, default to **validate**.

---

## Required Research (All Modes)

Before any operation, you MUST read in parallel:

1. **Utils and constants guidelines**:
   `docs/file-type-guidelines/utils-and-constants.md`
2. **Unit testing strategy**:
   `docs/file-type-guidelines/unit-testing.md`
3. **Existing patterns** (study at least one):
   - `packages/nimbus/src/components/combobox/utils/` — multi-file utils with
     specs (`filters.ts` + `filters.spec.ts`, `selection.ts` +
     `selection.spec.ts`, `collection.ts` + `collection.spec.ts`)
   - `packages/nimbus/src/components/inline-svg/utils/sanitize-svg.ts` — single
     util with sibling spec
   - `packages/nimbus/src/components/money-input/utils/` — utils plus an index
     barrel re-exporting multiple helpers

---

## File Structure

```
packages/nimbus/src/components/{component}/
├── {component}.tsx
├── utils/
│   ├── {kebab-name}.ts          # one purpose per file (see Merge Rule)
│   ├── {kebab-name}.spec.ts     # sibling unit test
│   └── index.ts                 # barrel re-export
├── constants/                   # only when constants are needed
│   ├── {kebab-name}.ts
│   └── index.ts
```

### Naming Convention

- File name is kebab-case of the function/constant: `getInitials` lives in
  `get-initials.ts`. `MAX_FILE_SIZE` lives in `max-file-size.ts` (or grouped
  by topic: `validation-limits.ts`).
- Spec file mirrors the source file with a `.spec.ts` suffix.

---

## Validate Mode

### Validation Checklist

Validate against these requirements. Each violation MUST be reported with the
specific file path and line number.

#### Category 1: Location & Inlining (3 items)

- [ ] **No inlined utils in main file**: `{component}.tsx` MUST NOT export pure
      helper functions. Detection: any `export function name(...)` or
      `export const name = (...) => ...` whose return value is not JSX is a
      utility and belongs in `utils/`.
- [ ] **Utils folder exists**: If the component has utilities, they live under
      `packages/nimbus/src/components/{component}/utils/`.
- [ ] **Constants folder exists** (if applicable): Constants live under
      `packages/nimbus/src/components/{component}/constants/`.

#### Category 2: File Organization (4 items)

- [ ] **One purpose per file**: A solo helper lives in its own
      `{kebab-name}.ts`. Cohesive helpers merge into a single file when
      (1) they share a meaningful name token (≥4 chars after dropping generic
      verbs and connectors), (2) one is a factory for another's signature, or
      (3) they form a direct dependency chain. Merged files are named for the
      shared token (agent-noun pluralized: `filters.ts`, `validators.ts`).
      Banned: `helpers.ts`, `utils.ts`, `misc.ts`, or naming a merged file
      after a single export. Promotable and component-coupled helpers do not
      belong in the same file. See
      [File Organization](../../../docs/file-type-guidelines/utils-and-constants.md#file-organization)
      in `utils-and-constants.md` for the full rule.
- [ ] **Kebab-case filename**: File name matches the function/topic name in
      kebab-case.
- [ ] **Index barrel**: `utils/index.ts` re-exports every util:
      `export { getInitials } from "./get-initials";`
- [ ] **Constants index barrel** (if applicable): `constants/index.ts`
      re-exports every constant.

#### Category 3: Purity (4 items)

- [ ] **No React imports**: Util files MUST NOT import React, hooks, or any
      `react-aria` modules. If you need React, it's a hook — move it to
      `hooks/` instead.
- [ ] **No JSX**: Util files MUST NOT return JSX. Files containing JSX are
      components, not utilities.
- [ ] **No side effects at module level**: Top-level statements must be
      `import`, `export`, type definitions, or `const` declarations. No
      mutation, no I/O, no DOM access at module scope.
- [ ] **Deterministic**: Pure functions — same input always yields same
      output, no reliance on `Date.now()`, `Math.random()`, or external state
      (unless explicitly passed as a parameter).

#### Category 4: Documentation (2 items)

- [ ] **JSDoc on every export**: Each exported function/constant has a JSDoc
      block explaining purpose, parameter contracts, and any non-obvious
      behavior (e.g. codepoint safety, locale handling).
- [ ] **No "WHAT" comments**: JSDoc explains WHY/contracts. Don't restate the
      function signature in prose.

#### Category 5: Type Safety (3 items)

- [ ] **Explicit parameter types**: All parameters typed (TypeScript may
      infer; the export signature should still be explicit).
- [ ] **`as const` for constants**: Constants use `as const` assertions for
      narrowest types.
- [ ] **No `any`**: No `any` types without an inline comment justifying the
      use.

#### Category 6: Testing (4 items)

- [ ] **Sibling spec exists**: Every `{name}.ts` has a sibling
      `{name}.spec.ts` (Vitest, JSDOM).
- [ ] **Edge case coverage**: Tests cover empty/undefined/null inputs,
      boundary values, and codepoint-sensitive cases (emoji surrogate pairs,
      CJK, RTL) where applicable.
- [ ] **Imports from sibling**: Spec imports the unit under test from
      `./{name}`, NOT from a barrel or the main component file.
- [ ] **Tests pass**: `pnpm test:dev packages/nimbus/src/components/{component}/utils/`
      reports 0 failures.

### Total Validation Items: 20 across 6 categories

---

## Validation Report Format

```markdown
## Utils & Constants Validation: {ComponentName}

### Status: [✅ PASS | ❌ FAIL | ⚠️ WARNING]

### Files Reviewed

- Utils dir: `packages/nimbus/src/components/{component}/utils/`
- Constants dir: `packages/nimbus/src/components/{component}/constants/` (if
  applicable)
- Main file scanned for inlined helpers:
  `packages/nimbus/src/components/{component}/{component}.tsx`

---

### ✅ Compliant (X/20)

[Per category breakdown]

---

### ❌ Violations (MUST FIX)

- **`{file}:{line}`**: [violation description]
  - **Guideline**: [reference to utils-and-constants.md section or this
    skill's checklist]
  - **Fix**: [how to resolve, including target file path]

---

### ⚠️ Warnings (SHOULD FIX)

[Same format as violations]

---

### Next Steps

1. Fix all ❌ violations first
2. Run tests: `pnpm test:dev packages/nimbus/src/components/{component}/utils/`
3. Re-validate: `writing-utils-and-constants validate {ComponentName}`
```

---

## Merge Rule Reference

The canonical merge rule — three criteria (shared meaningful name token /
factory relationship / direct dependency), file-naming formula, coupling
constraint, scope-agnostic application, promotion guidance, no reverse-merge,
forward-applied scope, and barrel-stability contract — lives in
[`docs/file-type-guidelines/utils-and-constants.md` → File Organization](../../../docs/file-type-guidelines/utils-and-constants.md#file-organization).
That document is the source of truth. Load it before applying the rule (it is
already in the [Required Research](#required-research-all-modes) list above).

One-line summary for quick reference: **merge into a single family file when
helpers share a meaningful name token (≥4 chars after dropping generic verbs
and connectors), when one is a factory for another's signature, or when one
directly depends on the other. Otherwise solo files. Banned filenames:
`helpers.ts`, `utils.ts`, `misc.ts`.**

---

## Procedure: Adding a Helper to `utils/`

When adding a new helper:

1. **List existing files** in the folder, with their exports.
2. **Tokenize the new helper's name** (camelCase boundary).
3. **For each existing helper**, compute shared content tokens:
   - Drop connectors (`By`, `For`, `From`, `To`, `With`) and generic verbs
     (`get`, `is`, `has`, `set`, `add`, `do`, `make`, `build`, `create`,
     `extract`, `find`, `try`)
   - Require ≥4 chars
4. **Check each merge criterion** (shared token / factory relationship /
   direct dependency) against each existing helper.
5. **If any criterion fires**, merge into a single file named per the
   file-naming rule. The PR that adds the connecting helper does the rename
   and barrel update — not punted as follow-up.
6. **Update the sibling `*.spec.ts`** the same way (one source file = one
   spec file).
7. **Update `utils/index.ts`** barrel.
8. **Search the component** for any deep imports of renamed files and update
   them.

The PR that adds a connecting helper performs the rename and barrel update —
not punted as follow-up. See
[Scope, Promotion, and Degenerate States](../../../docs/file-type-guidelines/utils-and-constants.md#scope-promotion-and-degenerate-states)
in the docs for promotion semantics, no-reverse-merge, forward-applied scope,
and barrel-stability constraints.

---

## Create Mode

### Process

1. Identify the helpers to extract (from a feature spec or from inlined code
   in `{component}.tsx`).
2. For each helper:
   - Create `utils/{kebab-name}.ts` with the function and JSDoc.
   - Create `utils/{kebab-name}.spec.ts` with edge-case coverage.
3. Create or update `utils/index.ts` to re-export every helper.
4. If constants are needed, mirror the same structure under `constants/`.
5. Update `{component}.tsx` to import from `./utils` (and `./constants`).
6. Run `pnpm test:dev packages/nimbus/src/components/{component}/utils/` to
   verify.

### Util File Template

```typescript
/**
 * {One-paragraph WHY: contract, edge cases, non-obvious behavior.}
 */
export function {functionName}({params}): {ReturnType} {
  // implementation
}
```

### Spec File Template

```typescript
import { describe, it, expect } from "vitest";
import { {functionName} } from "./{kebab-name}";

describe("{functionName}", () => {
  it("{primary contract description}", () => {
    expect({functionName}({inputs})).toBe({expected});
  });

  it("handles {edge case}", () => {
    expect({functionName}({edge inputs})).toBe({expected});
  });

  // ...edge cases: empty, undefined, boundary, codepoint, etc.
});
```

### Constant File Template

```typescript
/**
 * {One-paragraph WHY: where this is used, why this value.}
 */
export const { CONSTANT_NAME } = { value } as const;
```

---

## Update Mode

### Common Scenarios

#### Scenario 1: Move inlined helpers out of main component

**Trigger**: Validate mode flagged `export function ...` in `{component}.tsx`.

**Steps**:

1. For each inlined helper, create `utils/{kebab-name}.ts` and copy the
   function + JSDoc.
2. If a `{component}.spec.tsx` exists with describe blocks for these
   functions, split each describe block into its own
   `utils/{kebab-name}.spec.ts` and update the import path to
   `./{kebab-name}`.
3. Create or update `utils/index.ts` with re-exports.
4. Update `{component}.tsx` to `import { ... } from "./utils";` and remove
   the inlined definitions.
5. Delete the now-redundant `{component}.spec.tsx` (or trim it down to
   anything component-level that legitimately needs JSDOM).
6. Run `pnpm test:dev packages/nimbus/src/components/{component}/` to verify.
7. Run `pnpm --filter @commercetools/nimbus typecheck:dev` to verify.

#### Scenario 2: Add a new helper to an existing utils folder

**Steps**:

1. Create `utils/{new-name}.ts` and `utils/{new-name}.spec.ts`.
2. Add the re-export line to `utils/index.ts`.
3. Run tests.

---

## Error Recovery

### Error 1: "Can't import from barrel — circular dependency"

**Cause**: A util file imports from `@/components` or another barrel that
indirectly references the same component.

**Fix**: Utils should be self-contained. If a util needs a type from another
component, import directly from the implementation file:
`import type { Foo } from "../../button/button.types";`

### Error 2: "Spec file can't find function"

**Cause**: Spec imports from `./` (folder index) instead of the sibling file.

**Fix**: Specs MUST import from the sibling source file:
`import { getInitials } from "./get-initials";` (NOT from `./index`).

### Error 3: "JSX in utility file" / TypeScript error on JSX syntax

**Cause**: The "utility" actually returns React elements — it's a component
or a hook, not a util.

**Fix**: Move it to the appropriate location:

- Returns JSX → component file
- Uses React hooks but doesn't return JSX → `hooks/` folder, named
  `use-{name}.ts`

---

## Related Guidelines

- `docs/file-type-guidelines/utils-and-constants.md` — The canonical reference
- `docs/file-type-guidelines/hooks.md` — When to use hooks instead of utils
- `docs/file-type-guidelines/unit-testing.md` — Vitest conventions
- `docs/file-type-guidelines/main-component.md` — What stays in the main file

---

**Execute utils-and-constants operation for component specified in arguments**
