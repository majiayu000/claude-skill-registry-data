---
name: barrel-export-validation-testing
description: >-
  Use when writing or repairing a test that guards a public barrel — an index that re-exports
  components and their prop types — and the guard parses export lines with a regex, checks names
  with a loose "ends with Props" filter, or relies on runtime key inspection that cannot see
  type-only exports. Also when a type leaked to or vanished from a package public surface unnoticed.
---

# Barrel export validation testing

## Profile keys consumed

- `make.test_unit_client`
- `make.lint_deps`
- `architecture.source_root`
- `architecture.modules`

## Overview

A barrel guard that parses only some re-export forms passes vacuously: a type written in a form the
parser does not recognise is invisible to it, and `Object.keys` on the imported module cannot see
type-only exports at all. Make the parser's blind spot an assertion, and bind the type surface at
compile time so the type checker catches what text parsing cannot.

## When to use

- A public barrel is the package's contract and nothing fails when an export is dropped or added.
- A guard's regex covers `export { … } from` and `export type { … } from` but the file may also
  contain `export type * from`, `export * from`, or an inline `export { type Foo } from`.
- Component prop types are validated by a loose suffix check rather than against the directory name.
- Not for: enforcing which module may import which — that is a dependency-cruiser boundary rule,
  run through the target mapped by `make.lint_deps` (skip with a recorded note when it maps to
  `null`).

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — module and feature barrels exist (one `index.ts` per entry in
  `architecture.modules` under `architecture.source_root`) and dependency-cruiser rules such as
  `no-module-internal-imports` guard the boundary, but there is no export-contract test; the
  patterns below are what such a test would need.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the shared
  components barrel under `architecture.source_root` is a value-only barrel with no export-contract
  test.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — a unit
  test (`tests/unit/export-contract-integrity.test.ts`, run through the target mapped by
  `make.test_unit_client`) guards the components barrel against a checked-in register and applies
  every pattern below.

## Pattern one — assert the parser's residue

Define a regex for exactly the forms the guard understands, then strip every match from the file and
assert that no `export` line remains. An unrecognised form now fails loudly instead of slipping
past.

```ts
const BARREL_REEXPORT = /export\s+(?:type\s+)?\{[^}]*\}\s*from\s*'[^']+';/g;

const unparsed = barrel
  .replace(BARREL_REEXPORT, '')
  .split('\n')
  .map((line) => line.trim())
  .filter((line) => line.startsWith('export'));

expect(unparsed).toEqual([]);
```

Add a second assertion that no value re-export smuggles types through an inline specifier: collect
the names inside every `export { … } from` statement and assert none starts with `type`.

## Pattern two — bind the surface at compile time

Import every public name from the barrel and reference each in a tuple type. Dropping an
`export type` then breaks the type check, which a runtime key sweep can never do.

```ts
type Named<T> = T;
type PublicTypeSurface = [Named<UiCardListProps>, Named<HeadingLevel>];
```

## Pattern three — derive names, do not sniff them

Compute the expected props type from the directory slug (`ui-card-list` → `UiCardListProps`) and
require it in both the register row and the barrel's type re-exports for that module. A loose "some
exported name ends with `Props`" filter passes on a typo.

Modules that genuinely publish no such name (token modules that export theme values, a wrapper that
publishes a generic component type) go in a small keyed exemption map whose value is the reason, and
a further test asserts every exemption key is documented in the register.

## Pattern four — assert the negative

The contract has two halves, and a guard that only checks presence covers one of them. Keep a named
list of types that appear solely in an internal child signature and assert none of them shows up in
the barrel's type re-exports, so a helper type cannot drift onto the published surface the way a
missing one drops off it.

## Common mistakes

- Widening the regex to swallow a surprising line instead of adding the form as its own case — the
  residue test then covers less than it appears to.
- Listing an exemption without a stated reason, so the next maintainer cannot tell intent from
  drift.
- Checking only that a name is in the register, not that it reached the barrel; the register is the
  claim and the barrel is the delivery, so assert both.
- Relaxing an assertion to make a red guard green — strengthen the parser or record the exemption.
