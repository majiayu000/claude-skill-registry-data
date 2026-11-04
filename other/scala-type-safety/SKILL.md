---
name: scala-type-safety
description: The Scala 3 type-safety toolkit and compiler-flag rules for scala-ts — choosing a type-level tool, exhaustiveness, the @nowarn policy, macro-specific rules, and what the compiler does not check here. Use when writing, reviewing or designing any Scala code in this repo.
---

# Scala type safety (CDD toolkit)

Every idiom here exists to move a class of bug from runtime (or review) to the compiler. When a change is hard to express with these, the model is wrong — change the types first, then follow the errors (`cdd`, `compiler-driven-verification`).

## Compiler flags are the lint layer

`sbt-tpolecat` (in its default CI mode) sets `-Werror`, `-Ycheck-all-patmat`, `-Wvalue-discard`, `-Wnonunit-statement` and `-Wunused:{implicits,explicits,imports,locals,params,patvars,privates}`; see them with `sbt 'show scalacOptions'`. There is no scalafmt or scalafix. Every warning is a build failure — fix the code, never suppress it.

## Choosing a type-level tool

| Need | Tool | What it rules out |
|---|---|---|
| A closed set of cases | sealed trait / `enum` (`TsModel`, `TsImport`, `TsImport.Location`) | Stringly-typed states; missing cases in matches |
| A mode switch | a two-case ADT | A swapped `Boolean` argument that compiles silently |
| Two values of one base type must not mix | `opaque type` with its own companion | Passing one kind of name where another goes |
| Construction must be validated | `opaque type` / private constructor + smart constructor returning `Option`/`Either` | Unvalidated values existing at all |
| A literal must be valid | `inline` + `compiletime.error`, or `report.errorAndAbort` in a macro | Bad input reaching generation |
| A type-level parameter without a value | a proxy type param (`TypeParam["A1"]`) | Inference drifting |
| An erased runtime value must be read | capture a typed conversion at parse time (`TsModel.Array.toList: Any => List[Any]`) | Casts scattered through the generator |

## Exhaustiveness

- `-Ycheck-all-patmat` + `-Werror` make a non-exhaustive match on a sealed type a build error — but only if the match lists cases. A wildcard `case _ =>` is **not** checked and swallows new variants. List every case; a wildcard is acceptable only when the scrutinee is genuinely open (strings, ints, arbitrary `Any` values).
- A union of case types (`TsModel.Object | TsModel.Interface`) is matched exhaustively the same way.

## `@nowarn` policy

- Never add `@nowarn` to silence a real warning.
- The one standing use is `@annotation.nowarn("msg=match may not be exhaustive")` on quote-pattern type matches (`tpe.asType match { case '[t] => ... }`) inside the macro, which are exhaustive but cannot be proven so.
- A parameter that exists only for its type (evidence or a proxy) is unused by definition; prefer a memberless marker type (exempt from the warning) over `@nowarn`.

## Macro rules (`TsParser`, `ReflectionUtils`)

- Abort with `report.errorAndAbort` and a message naming the type when a shape is unsupported at compile time; use `sys.error` only for failures that can only be detected when generating.
- Keep the macro producing data (`Expr[TsModel]`), never TypeScript text — rendering belongs to `TsGenerator`.
- Top-level vs reference parsing (`top`) decides whether a definition is produced; parse referenced types with `top = false` so each type is defined once.

## Instances: least power, no ambient defaults

- Make the compiler force a decision. Don't let a default parameter or "no instance in scope" mean "do nothing".
- Take a `using` parameter only when there is more than one meaningful instance (`TsCustomType`, `TsCustomOrd`, `TsImports.Available` are the consumer's choices).

## Things the compiler does not check here

- **Golden output.** Only the tests pin the generated text; a renderer change compiles regardless of what it emits.
- **Generated TS type-correctness.** Only the ts-node round-trip checks it, and only for files the suite's `decode-encode.ts` imports.
- **Scala JSON vs generated codecs.** The round-trip tests use circe with the `_tag` discriminator; a consumer with different encoders is not checked.
- **Name-string matching.** `TsCustomType` matches fully-qualified names as strings.
- **Run-time failures in generation** — unresolved imports, missing config, missing `Ord` (`scala-ts-generation` → Footguns).
- **Wildcard matches**, `sys.error`, and `asInstanceOf` on `Any` values are invisible to the compiler — review rejects new ones.

## Preferred vs legacy (don't copy the legacy)

| Prefer | Legacy still present |
|---|---|
| `given`/`using`, `extension` | `implicit def liftString` and `implicit B: Monoid[B]` in `TsGenerator` |
| explicit cases over a sealed type | `case _ =>` in `recordCodecType`/`recordValueType`/`recordCodecInstance`/`generateTopLevel` |
| a typed conversion captured in `TsParser` | `asInstanceOf` on values inside `generateValueInstance` |
