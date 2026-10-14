---
name: typescript
description: "TypeScript: strict compiler, ESM, generics, unions/discriminated unions, narrowing, promise hygiene, parse-dont-cast at boundaries. Types do not validate runtime."
---

# typescript

Strict types at compile time, runtime parsing at boundaries — types evaporate, validation doesn't.

## Activate when

- Writing, reviewing, or configuring TypeScript; type design, module, or async decisions.

## Do NOT activate for

- Runtime behavior of JS (see languages/javascript); framework specifics (see frameworks/*).

## Inspection

Check tsconfig strictness, module mode (ESM vs CJS), existing type patterns (unions, generics, zod schemas), and boundary casts (`as`, `any`, `@ts-ignore`).

## Decision rules

- `strict: true` minimum; `noUncheckedIndexedAccess` where index safety matters; ESM for new code.
- Model states as discriminated unions; narrow with guards, never with casts. `as` is allowed only with a comment proving safety; `any` only at a validated boundary being parsed immediately.
- Generics constrained to what call sites need; utility types over hand-rolled mappings; `unknown` in, validated types out (parse, don't cast — Zod or equivalent).
- Promises: no floating promises (lint it), explicit rejection paths, `Promise.allSettled` where partial failure is real.

## Procedure

1. Fix the strictness baseline first (no new `any`/casts without justification).
2. Type the domain with unions + narrowing; validate all external input at runtime.
3. Remove existing casts by parsing or restructuring; each removal covered by a test.
4. Verify: `tsc --noEmit` clean, lint clean, no `as`/`@ts-ignore` without justification comments, boundary tests green.

## Failure modes

- `as` laundering untrusted data; enums where unions fit; `any` creeping through generics; floating promises; strict off "temporarily" forever.

## Escalation

Version behavior questions → research/documentation-search with package.json version; monorepo layout → architecture/language-modularity.

## References

- Registry: `../../research/documentation-search/references/framework-registry.yaml` (typescript, zod, eslint).
- Related: `../javascript/`, `../../tooling/type-checking/`.
