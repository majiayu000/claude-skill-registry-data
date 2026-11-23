---
name: functional-typescript
description: >
  Functional programming patterns for TypeScript and JavaScript: pure functions,
  immutability, composition, currying, higher-order functions, and Result and Option
  types. Applies the fp-ts rules when the codebase imports fp-ts. Trigger on "how do I
  avoid mutation", "how do I curry this", "how do I handle async errors without
  try-catch", or "make this more functional". For general typing questions use
  typescript-best-practices.
license: MIT
metadata:
  author: mshindi-labs
  version: "2.0.0"
---

# Functional TypeScript

Comprehensive guide to writing idiomatic functional TypeScript and JavaScript.
Contains 20 rules across 7 categories, grounded in
[_You Don't Know JS Yet_](https://github.com/getify/you-dont-know-js) by Kyle Simpson,
extended with TypeScript type system patterns.

## When to Apply

Reference these guidelines when:

- Writing new TypeScript or JavaScript functions
- Reviewing code for mutation, side effects, or imperative patterns
- Designing module APIs or encapsulated state
- Implementing data transformation pipelines
- Handling errors and nullable values without exceptions or null checks

## Rule Categories by Priority

| Priority | Category            | Impact                    | Prefix     |
| -------- | ------------------- | ------------------------- | ---------- |
| 1        | Core Principles     | CRITICAL                  | `core-`    |
| 2        | Immutability        | CRITICAL                  | `immut-`   |
| 3        | Closures & Scope    | HIGH                      | `closure-` |
| 4        | Function Patterns   | HIGH                      | `fn-`      |
| 5        | Module Pattern      | MEDIUM-HIGH               | `module-`  |
| 6        | TypeScript FP Types | MEDIUM                    | `types-`   |
| 7        | Code Style          | LOW-MEDIUM                | `style-`   |
| 8        | fp-ts Library       | HIGH (when fp-ts present) | `fp-ts-`   |

## Quick Reference

### 1. Core Principles (CRITICAL)

- `core-pure-functions` — return same output for same inputs; no side effects
- `core-side-effect-isolation` — functional core, imperative shell
- `core-referential-transparency` — inject `Date.now()`, `Math.random()`, and other hidden inputs

### 2. Immutability (CRITICAL)

- `immut-avoid-mutation` — never mutate arguments; use spread and map
- `immut-readonly-types` — annotate params with `Readonly<T>` and `readonly T[]`
- `immut-const-assertion` — use `as const` for literal types; prefer over `enum`
- `immut-spread-over-push` — use `toSorted`, `toReversed`, spread instead of `sort`, `push`, `splice`

### 3. Closures & Scope (HIGH)

- `closure-encapsulate-state` — closures for private state without classes
- `closure-loop-pitfall` — use `let` (not `var`) in loops; prefer array methods
- `closure-memoize` — memoize pure functions with closure-private cache

### 4. Function Patterns (HIGH)

- `fn-partial-application` — pre-fill arguments; return specialised functions
- `fn-currying` — one argument at a time; put config first, data last
- `fn-composition-pipe` — replace nested calls with `pipe`
- `fn-higher-order` — `map`/`filter`/`reduce` over imperative loops
- `fn-point-free` — pass function references directly; eliminate wrapper lambdas

### 5. Module Pattern (MEDIUM-HIGH)

- `module-iife-singleton` — IIFE for single-instance modules with private state
- `module-factory` — factory function for multiple independent instances
- `module-esm-private` — export functions not raw state; unexported = private

### 6. TypeScript FP Types (MEDIUM)

- `types-result` — `Result<T, E>` instead of throwing for expected errors
- `types-option` — `Option<T>` to make absence explicit
- `types-discriminated-union` — discriminated unions with exhaustiveness checking
- `types-type-guard` — reusable `x is T` predicates; use with `filter`
- `types-hof-generics` — type HOFs with generics; `Transform<A,B>`, `Predicate<T>`

### 7. Code Style (LOW-MEDIUM)

- `style-prefer-functions-over-classes` — factory functions avoid `this` binding bugs
- `style-naming-conventions` — verbs for functions, `is`/`has` for predicates, `make`/`create` for factories

### 8. fp-ts Library (HIGH — when `fp-ts` is present)

Apply when the codebase imports from `fp-ts/*`.

- `fp-ts-pipe-flow` — `pipe` for immediate transforms; `flow` for reusable functions
- `fp-ts-option-either` — `Option<T>` for absence; `Either<E, A>` for typed errors; accumulate all errors with `getApplicativeValidation`
- `fp-ts-taskeither` — `TaskEither<E, A>` for async; `tryCatch`, `chain`, `traverseArray`, `orElse`, `fold`
- `fp-ts-do-notation` — `Do + bind + apS + bindTo` for multi-step workflows; `bind` when step depends on prior values, `apS` when independent

## How to Use

Read individual rule files for detailed explanations and before/after examples:

```
rules/core-pure-functions.md
rules/immut-avoid-mutation.md
rules/fn-composition-pipe.md
rules/fp-ts-pipe-flow.md
rules/fp-ts-option-either.md
rules/fp-ts-taskeither.md
rules/fp-ts-do-notation.md
```

Each rule file contains:

- Impact level and description
- Incorrect code example with explanation
- Correct code example with explanation
- Real-world patterns and edge cases
- Reference link

## References

- `references/pragmatic-fp.md` — 80/20 guide: when to use FP, when to skip it, common refactors
- `references/fp-typescript-types.md` — TypeScript type system tools for FP
- `references/fp-ts-library.md` — fp-ts API cheat sheet (pipe/flow, Option, Either, TaskEither, Do, RTE)
- `references/closures-and-partial-application.md` — closures, currying, memoization
- `references/module-pattern.md` — IIFE, factory, ESM encapsulation

## Full Compiled Guide

For all rules expanded in one document: `AGENTS.md`
