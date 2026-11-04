---
name: compiler-driven-verification
description: Step-by-step CDD implementation workflow for scala-ts — change the type first, follow compiler errors, pin generated output, verify. The equivalent of TDD here. Use when implementing features or making code changes.
---

# Compiler-Driven Verification

The execution loop for CDD (philosophy: `cdd`; Scala toolkit: `scala-type-safety`). Change the type, follow compiler errors, fix semantically, pin the output, verify:

| Step | Command / mechanism |
|---|---|
| Type check + lint | `sbt Test/compile` (`-Werror`, so every warning is fatal) |
| Exhaustiveness | `match` over a sealed trait/`enum` listing every case, enforced by `-Ycheck-all-patmat` |
| Generated output | golden expected strings in `src/test/scala/scalats/tests/*Test.scala` |
| Generated output type-checks and round-trips | `sbt test` (needs `cd tests && yarn` once) |
| Never silence with | `.asInstanceOf`, catch-all `case _`, `@nowarn` |

## Workflow

1. **Read the current model** — `TsModel` cases, the `TsParser.parse` branch that produces them, and each `TsGenerator` renderer (`generateCodecType`, `generateValueType`, `generateCodecInstance`, `generateValueInstance`) that consumes them.
2. **Change the type first.** Add or change the `TsModel` case (or a private ADT in the generator), then `sbt Test/compile` and follow every error.
3. **Write the expected TypeScript first.** Add or update the golden string in a `CodecTest` suite, run `sbt 'testOnly scalats.tests.<Suite>'`, and confirm it fails showing the old output.
4. **Implement** until the golden test and the ts-node round-trip pass.
5. **Full verification** per `verification-before-completion`.

## Pitfalls

| Pitfall | Correct approach |
|---------|-----------------|
| Golden test passes but the TS doesn't type-check | Only files imported by the suite's `decode-encode.ts` are type-checked; make the decode-encode type reference the new output |
| `-Werror` on unused/value-discard | Remove the binding or consume the value; don't suppress |
| Changing one renderer only | Codec type, value type and codec instance must agree; `satisfies t.Type<X, unknown>` in the output catches a mismatch only when ts-node compiles it |
| Macro change compiles but output is wrong | Macros expand in the test sources; `sbt Test/compile` recompiles them — inspect the failing golden diff |
