---
name: rule-frontend-utils
description: MANDATORY when editing files matching ["frontend/src/utils/**/*.ts", "frontend/src/utils/**/*.tsx", "frontend/src/**/*.ts", "frontend/src/**/*.tsx"]. Frontend utility conventions for the Simpler Grants frontend — when to extract a utility vs inline, file/function naming, pure-function expectations, edge-runtime safety, and testing requirements. Grounded in frontend/src/utils/.
---

# Frontend Utils Rules

## When to Extract vs Inline

INLINE a helper when it's used **once** and its meaning is obvious in context.

EXTRACT to `frontend/src/utils/` when any of:
- Used in 2+ files
- Contains non-trivial logic worth unit-testing
- Encapsulates a tricky edge case
- Crosses a feature boundary

> Per `frontend/src/utils/README.md`: **"avoid files that contain or support only a single function."** Group related helpers in a shared file (`dateUtil.ts`, `generalUtils.ts`) rather than creating one-file-per-function. Standalone files like `getFormData.ts` exist only when the function is substantial and self-contained.

Component-only helpers (e.g., a formatter used by exactly one component) stay in the component file or a sibling `Component.utils.ts`.

## Where Utilities Live

- `frontend/src/utils/` is the canonical home.
- USE a **domain subfolder** (`applyForm/`, `attachment/`, `opportunity/`, `search/`, `fileUtils/`) when there are multiple related files for a slice.
- USE a **flat grouped file** at the root of `utils/` (`dateUtil.ts`, `generalUtils.ts`, `analyticsUtil.ts`, `apiUtils.ts`) for cross-cutting helpers.
- **`testing/`** holds shared test helpers, NOT the tests themselves.
- **`middlewareSafeUtils.ts`** is the only place for helpers that must be importable from Next.js middleware / edge runtime — see the "Runtime Safety" section.

## File Naming

- Grouped helpers: `<topic>Util.ts` or `<topic>Utils.ts` — `dateUtil.ts`, `apiUtils.ts`, `generalUtils.ts`, `analyticsUtil.ts`.
- Single-purpose action files (only when the function is large enough to stand alone): `verbNoun.ts` — `getFormData.ts`, `getRoutes.ts`, `formHasAttachment.ts`, `formatRoleName.ts`.
- Tests: colocated `*.test.ts` next to the utility.
- DO NOT introduce `index.ts` barrels in `utils/`.

## Function Naming

ALWAYS use **camelCase**, verb-led, descriptive names:
- `formatCurrency`, `getFormData`, `isExternalLink`, `encodeText`, `splitMarkup`, `saveBlobToFile`

Prefixes:
- Booleans: `is*`, `has*`, `should*`, `can*`
- Getters: `get*`
- Formatters: `format*`
- Parsers: `parse*`
- Mappers: `to*` / `from*`

AVOID vague names: `helper`, `doStuff`, `handle`.

## Exports

- **Named exports only** — `export const fn = …` or `export function fn(…)`. NEVER `export default`.
- One concept per export. DO NOT bundle a kitchen-sink object.
- USE `import type { … }` for type-only imports.

```ts
import type { PaginationInfo } from "src/types/apiResponseTypes";

export function formatCurrency(amount: number): string { /* … */ }
export const isExternalLink = (href: string): boolean => /* … */;
```

## Pure Function Expectations

DEFAULT to pure:
- No I/O, no DOM access
- No `Date.now()` / `Math.random()` baked in — inject them as parameters
- No module-level mutable state

When impurity is required (DOM mutation, network, storage, downloads), MAKE it obvious in the name (`saveBlobToFile`) and isolate it in its own function — NEVER mix pure and impure logic in one helper.

Side-effecting helpers MUST be safe to call multiple times, or DOCUMENT that they aren't.

DO NOT throw for control flow. Throw only on truly exceptional/malformed input (see `splitMarkup`'s defensive parsing for the canonical pattern).

## Runtime Safety (Next.js)

Anything imported by middleware, `instrumentation.ts`, or edge routes MUST live in **`middlewareSafeUtils.ts`**:
- No Node-only APIs (`fs`, `path`)
- No `process.env` access patterns that break at the edge
- No large dependencies

Server-only helpers should NOT import from client-only modules and vice versa. If a helper is server-only, mark it with `import "server-only"` at the top.

DO NOT import React from `utils/` files unless the helper genuinely returns JSX (rare — prefer a component).

## Dependencies

- Lodash is acceptable when it meaningfully simplifies code (matching existing usage). PREFER native ES methods when equivalent.
- DO NOT pull in heavy date libs — `dateUtil.ts` is the single source of truth for date helpers; extend it rather than importing a new lib.
- NO new top-level dependencies just for a utility — discuss first.

## Testing Requirements

**Every utility in `frontend/src/utils/` MUST have a colocated `*.test.ts`** (matches the existing `formDataToJson.test.ts` pattern).

Tests MUST cover:
- Happy path
- Empty / zero / null inputs
- Boundary conditions
- Any explicit `throw` cases

Pure functions should be tested **without mocks**. Impure helpers should isolate side effects behind a thin seam so the pure core is testable.

USE shared helpers from `frontend/src/utils/testing/` rather than reinventing fixtures.

## Anti-Patterns

- One-function files (violates the README rule)
- `default` exports
- Mixing pure and impure logic in one function
- Module-level mutable state
- Using `any` — use `unknown` and narrow
- Importing Node-only APIs into anything that might run at the edge
- Reaching into React internals or component state from a utility
- Untested utilities

---

## Related Rules

- **`frontend-types.mdc`** — type organization and naming for shared types consumed by utils
- **`frontend-components.mdc`** — when a "utility" is really a component
- **`frontend-services.mdc`** — service-layer boundary for network/data fetching
- **`frontend-tests.mdc`** — testing conventions and shared fixtures

## Specialist Validation

**Simple changes (add a function to an existing grouped file, extend a formatter):** No specialist needed.

**Moderate changes (new grouped utility file, new domain subfolder):** Invoke `codebase-conventions-reviewer`.

**Complex changes (new edge-runtime helper, refactoring `middlewareSafeUtils.ts`, introducing a new dependency):** Invoke in parallel:
- `architecture-strategist` — validate placement and runtime boundaries
- `kieran-typescript-reviewer` — TypeScript quality review
- `performance-oracle` — bundle and edge-runtime impact
