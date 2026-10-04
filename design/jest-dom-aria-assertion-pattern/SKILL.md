---
name: jest-dom-aria-assertion-pattern
description: Use when a component test asserts on ARIA attributes and ESLint reports jest-dom/prefer-required or jest-dom/prefer-to-have-attribute, when toBeRequired() cannot distinguish native required from aria-required, or when mutants inside aria-describedby / aria-required computation survive DOM assertions.
---

# Jest-dom ARIA assertion pattern

## Profile keys consumed

- `make.lint_eslint`
- `make.lint_metrics`
- `make.test_unit_client`
- `make.test_mutation`
- `capabilities.mutation_testing`
- `architecture.source_root`

Run every check through the profile's `make` target map. Where one of those
keys maps to `null` the capability is absent — skip that step with a recorded
note rather than improvising a raw command, and skip the mutation-survivor half
of this skill with a note when `capabilities.mutation_testing` is `false`.

## Overview

`eslint-plugin-jest-dom` rewrites attribute assertions made on Testing Library query results, and
its rules push the same assertion back and forth for attributes on its banned list. Move the ARIA
emission logic into a pure helper module and assert on the object it returns; leave the DOM
assertions on role and structure.

## When to use

- A test asserts `toHaveAttribute('aria-required', 'true')` and the gate mapped by
  `make.lint_eslint` reports that `jest-dom/prefer-required` demands `toBeRequired()`, while a
  `getAttribute` rewrite trips `jest-dom/prefer-to-have-attribute`.
- The component computes an ARIA value (joining helper-text and caller-supplied `aria-describedby`
  ids, choosing `aria-invalid`), and a DOM matcher cannot pin which branch ran.
- Mutation survivors reported by the target mapped by `make.test_mutation` sit in ARIA-computing
  branches that render identically.
- `toBeRequired()` passes for both the native `required` attribute and `aria-required="true"`, so
  the test no longer proves which one the component emits.
- Not for: assertions about visible text, roles, or focus — those stay idiomatic DOM matchers.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the ESLint config behind `make.lint_eslint` registers `eslint-plugin-jest-dom`
  and applies `flat/recommended` across TypeScript sources; the helper must be instance methods on
  a class exported as a module singleton and its return type must live in a `types/` file (this
  shape's "no static methods or free functions" and "type-only files" conventions).
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — the ESLint config
  extends `plugin:jest-dom/recommended`; plain exported helper functions are allowed, so the
  module can stay a function module.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes —
  jest-dom `flat/recommended` is scoped to the test globs, and the pattern extends the
  per-component file split already in use (`theme.ts`, `types.ts`, `index.tsx`) — the same split
  this shape's component-structuring guidance covers.

## Core pattern

Put the emission logic in its own module beside the component, under the tree named by
`architecture.source_root`:

```ts
// <source root>/components/ui-input/aria.ts
export function inputAria(required: boolean | undefined): { 'aria-required'?: 'true' } {
  return required ? { 'aria-required': 'true' } : {};
}

export function describedBy(helperId?: string, callerId?: string): { 'aria-describedby'?: string } {
  const ids = [helperId, callerId].filter(Boolean);
  return ids.length > 0 ? { 'aria-describedby': ids.join(' ') } : {};
}
```

Assert on the returned object, not on an element — these assertions run in the client unit suite
mapped by `make.test_unit_client`:

```ts
expect(inputAria(true)).toEqual({ 'aria-required': 'true' });
expect(inputAria(false)).toEqual({});
expect(describedBy('helper-1', 'caller-2')).toEqual({ 'aria-describedby': 'helper-1 caller-2' });
```

The component spreads the result, so the DOM keeps the same contract:

```ts
<input {...inputAria(required)} {...describedBy(helperId, ariaDescribedBy)} />
```

In the React SPA shape the same helper is instance methods on a class exported as a module
singleton (`export default new InputAria();`), with its return type in a `types/` file; the
assertions are unchanged apart from the receiver.

## Why the lint loop stops

The jest-dom rules fire only when the `expect` argument is a Testing Library query node. An
assertion on a plain object returned by a helper is outside their scope, so neither rule rewrites it
and the ARIA contract is pinned exactly — including the "attribute is absent" case, which
`toBeRequired()` and `toHaveAttribute` express only indirectly. The helper is also cheap to cover
without rendering, which keeps per-function complexity under the metrics policy enforced by the
target mapped by `make.lint_metrics`.

## Common mistakes

- Silencing one rule to satisfy the other — every repository shape forbids inline lint suppression;
  move the assertion off the DOM node instead.
- Leaving the DOM test out entirely — still assert the element renders with the right role, so a
  helper that is computed but never spread fails.
- Returning `{ 'aria-required': undefined }` rather than omitting the key — a `toEqual` assertion
  then cannot tell "absent" from "explicitly undefined"; omit the key.
- In the React SPA shape, shipping the helper as exported free functions or declaring its return
  type in the logic file — move it to instance methods on a singleton class and put the type in a
  `types/` file.
