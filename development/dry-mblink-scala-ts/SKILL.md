---
name: dry
description: Preventing and removing repetitive code in scala-ts. Use when asked to deduplicate code, find repeated patterns, refactor for reuse, apply DRY principles, or extract shared logic.
---

# DRY

## Search before you write

Before writing a helper, search for an existing one — re-implementing is the most common DRY violation. Places to check first:

- `TsImports.Available` (`TsImports.scala`) — every io-ts/fp-ts/io-ts-types reference as a `Generated` or `CallableImport` (`imports.iotsReadonlyArrayC(...)`, `imports.fptsOption(...)`). Never write `"t.something"` as a bare string in the generator; add a helper here so the import travels with the reference.
- `TsGenerator` private helpers — `generateFields0`, `maybeWrapCodec`, `generateCodecTypeRef`/`generateValueTypeRef`/`generateCodecInstanceRef`, `typeArgsMixed`/`typeArgsFnParams`, `mkCodecName`/`mkValueName`, `intercalateMap`.
- `ReflectionUtils` — `Mirror` extraction for the macro.
- `CodecTest` and `tests/package.scala` — the shared test harness; a new suite supplies only types and expected output.

## Workflow

1. Grep for the key patterns (signatures, string fragments of generated code, `TsModel` matches).
2. Classify; refactor only knowledge duplication:

   | Classification | Action |
   | --- | --- |
   | Knowledge duplication (same rule, e.g. how a codec name is derived) | Extract a shared function |
   | Structural similarity (the four renderers matching on `TsModel`) | Leave alone — each match must stay exhaustive and independent |
   | Configuration duplication (same import location) | Put it in `TsImports.Config` / `Available` |
   | Type duplication | Extract a shared type |

3. Verify: `sbt Test/compile` and `sbt test`.

Thresholds: identical logic → abstract at 2 instances; structurally similar → wait for 3; in doubt, keep the duplication. Tests are DAMP: each suite's expected output is spelled out in full, even when it repeats another suite's. Don't over-parameterize: a helper taking several callbacks and flags is worse than the duplication.
