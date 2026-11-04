---
name: cdd
description: Compiler Driven Development methodology for scala-ts — Scala 3 generator code and the TypeScript/io-ts it emits. Use when writing, editing, or refactoring code to maximize compile-time correctness guarantees. Guides type-level modeling, exhaustive handling, and lint-as-compiler.
---

# Compiler Driven Development (CDD)

Push correctness from runtime to compile time by encoding invariants in types. In this repo that applies twice: to the Scala that does the generating (`TsParser`, `TsModel`, `TsGenerator`), and to the TypeScript it emits, which its consumers type-check under `strict`. Scala toolkit: `scala-type-safety`. Step-by-step loop: `compiler-driven-verification`. Output shapes: `scala-ts-generation`, `io-ts`.

Enforcement order: **types** → **lint** (scalac `-Werror` with sbt-tpolecat's flags, `-Ycheck-all-patmat`) → **tests** (golden output + ts-node round-trip) → runtime checks only where data enters.

## Construct map (Scala ↔ generated TS)

| Principle | Scala (this repo) | Generated TypeScript |
|---|---|---|
| Absent value | `Option[A]` (no `null`) | `O.Option<A>` via `optionFromNullable` |
| Fallible result | `Either[E, A]`; generation-time failure is `sys.error` / `report.errorAndAbort` with the type name | `E.Either<L, R>` via io-ts-types `either` |
| Closed set of cases | sealed trait / `enum` (`TsModel`) | `_tag` union: `t.union([...])`, `XU`, `XCU` |
| Exhaustiveness | `-Ycheck-all-patmat` + `-Werror` on a `match` that lists every case | consumers' `switch` on `_tag` narrows because every member carries a literal `_tag` |
| No unsafe casts | no new `asInstanceOf`/`isInstanceOf` | output never needs `as`; codecs end in `satisfies t.Type<X, unknown>` |
| Immutability | immutable collections, no `var` | `ReadonlyArray`, `ReadonlySet`, `ReadonlyMap`, `ReadonlyNonEmptyArray`, `t.readonly` |
| Boundary validation | the macro reads the type once, into `TsModel` | io-ts `decode` at the consumer's edge |

## Core principles

1. **Make illegal states unrepresentable** — a sealed ADT over a record of flags; a new distinction in the generator is a new `TsModel` case or a private ADT, not a `Boolean` parameter.
2. **Parse, don't validate** — `TsParser` turns a Scala type into a `TsModel` once; the generator never re-inspects Scala types or re-parses strings it generated.
3. **The compiler is the refactoring guide** — change the type first, follow the errors; each fix must be semantically complete, never a silencer.
4. **Verify type-system claims with the compiler, not memory.** For a claim about Scala, write a scratch test and compile it (`sbt Test/compile`). For a claim about TypeScript or io-ts, put the code in `tests/output/scratch.ts` and run `cd tests && yarn --silent ts-node output/scratch.ts` (strict type-check), then delete it.
5. **Generated output must not be weaker than the Scala type.** No `{}`, `any`, or mutable collections in emitted types; a field-less shape still gets a precise type.

## Workflow

1. **Define or change the type** (a `TsModel` case, a field, a private ADT).
2. **Follow compiler errors** — `sbt Test/compile`.
3. **Fix each error correctly** — no `asInstanceOf`, no `case _ =>` over a sealed type, no `@nowarn`.
4. **Pin the output** — update or add the golden expectation in the matching `CodecTest` suite.
5. **Verify** per `verification-before-completion`.

## Anti-patterns

- `case _ =>` over `TsModel` → list every case (the compiler then flags new variants).
- `asInstanceOf` to reach a runtime value → capture a typed conversion function in `TsParser` (like `TsModel.Array.toList`).
- Silently emitting looser TypeScript for an unsupported shape → fail generation with the type name.
- A `Boolean` mode parameter that callers can swap → a two-case ADT.
- `var` or mutable builders → fold / `foldMap` / `|+|` on `Generated`.
