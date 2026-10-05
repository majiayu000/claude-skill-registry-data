---
name: beautyline-lib-and-tests
description: >-
  Placement of helpers, queries, serializers, and Vitest tests under
  src/lib for Beautyline. Use when adding business logic, API helpers,
  course/product/equipment queries, constants, or unit tests beside modules.
---

# Beautyline: lib layer and tests

## Role of `src/lib/`

- **Pure/domain logic**, query helpers, slug rules, serializers to public JSON shapes (`public-course`, `public-product`, `display-text`, token-like constants (`course-types`, `product-brands`).
- Prefer **thin** route handlers and page loaders that delegate to **`@/lib/...`** for heavy logic rather than embedding long logic in `page.tsx`.

## Naming and cohesion

- **One concern per file** where feasible (matching existing granular modules).
- Stable constants and enums used across admin and storefront live here when not tied to a single component.

## Tests

- **Vitest**: `npm test` / `npm run test:watch`.
- Place **`*.test.ts`** or **`*.test.tsx`** **next to** the module under test (existing example: `src/lib/auth.test.ts`).
- Expand tests for non-trivial new `lib` behavior (serialization edge cases, auth utilities, deterministic queries) rather than skipping tests for complex additions.

## Imports

- Consumers import from **`@/lib/<module>`** — keep public exports at the bottom of modules clear (named exports preferred for tree-shaking and grep-ability).
