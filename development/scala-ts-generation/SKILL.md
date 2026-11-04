---
name: scala-ts-generation
description: How scala-ts maps Scala types to TypeScript types and io-ts codecs — the parse/render pipeline, the full mapping table, naming, imports, and the footguns consumers hit. Use when changing generated output, adding support for a Scala type, or debugging why a consumer's generated file looks wrong.
---

# Scala → TypeScript generation

## Why it exists

One owner per fact: a shape is written once, in Scala, and generated into TypeScript, so server and client cannot disagree without one side failing to compile. Every Scala sum encodes (with circe's `_tag` discriminator) as a tagged union that TypeScript narrows and folds on directly. That only holds if the generated types are at least as precise as the Scala ones.

## Pipeline

`parse[A]` (macro, compile time, `TsParser`) → `TsModel` (data) → `generateAll` (`TsGenerator.generateTopLevel` per model) → `writeAll` (resolve imports per output file, `TypeSorter.sort`, write). `parseReference[A]` emits a reference only — the referenced type must be generated in some file passed to the same `writeAll`, or resolution throws `UnresolvedTsImportException` at run time.

## Mapping

| Scala | `TsModel` | Codec | Value type |
|---|---|---|---|
| `Byte`/`Short`/`Int`/`Long`/`Double`/`Float` | `Number` | `t.number` | `number` |
| `BigDecimal`/`BigInt` | `BigNumber` | configured `iotsBigNumber` (no default) | configured |
| `Boolean` | `Boolean` | `t.boolean` | `boolean` |
| `String` | `String` | `t.string` | `string` |
| `java.time.LocalDate`, joda `LocalDate` | `LocalDate` | configured `iotsLocalDate` (no default) | configured |
| `LocalDateTime`/`ZonedDateTime`/`Instant`, joda `DateTime` | `DateTime` | `DateFromISOString` (default) | `Date` |
| `java.util.UUID` | `UUID` | io-ts-types `UUID` | `UUID` |
| `io.circe.Json` | `Json` | `t.unknown` | `unknown` |
| `cats.Eval[A]` | `Eval` | as `A` | as `A` |
| `List`/`Vector`/`Seq`/`Chain` | `Array` | `t.readonlyArray` | `ReadonlyArray<A>` |
| `Set`/`SortedSet` | `Set` | `readonlySetFromArray(c, ord)` | `ReadonlySet<A>` |
| `NonEmptyList`/`NonEmptyVector`/`NonEmptyChain`, scalaz `NonEmptyList` | `NonEmptyArray` | `readonlyNonEmptyArray` | `RNEA.ReadonlyNonEmptyArray<A>` |
| `Option[A]` | `Option` | `optionFromNullable` | `O.Option<A>` |
| `Either`, scalaz `\/` | `Either` | io-ts-types `either` | `E.Either<L, R>` |
| cats `Ior`, scalaz `\&/` | `Ior` | configured `iotsThese` (no default) | `Th.These<L, R>` |
| `Map[String, V]` | `Map` | `t.record(t.string, v)` | `Record<string, V>` |
| `Map[K, V]` (other `K`) | `Map` | `readonlyMapFromEntries(k, ord, v)` | `ReadonlyMap<K, V>` |
| tuple | `Tuple` | `t.tuple([...])` | `[A, B]` |
| Scala 3 union `A \| B` (reference only) | `UnionTypeRef` | `t.union([...])` | `A \| B` |
| `case class` | `Interface` | `t.type({...})` | `{ ... }` |
| field-less, non-generic `case class` outside a union | `Interface` | `t.UnknownRecord` | `Record<string, unknown>` |
| `object` | `Object` | `t.type` of literal fields, plus a `const` of values | literal fields |
| sealed trait / `enum` | `Union` | `t.union([...])` | `A \| B` |
| type alias (non-generic) | `TypeAlias` | as the dealiased type, under the alias's name | |
| anything else | `Unknown` | an import of `<name>C` the consumer must provide | |

`Set` and non-`String`-keyed `Map` need an `Ord` for the element/key: built in for `string`/`number`/`boolean`, `Option`/array of those, and all-object unions (`xOrd`); otherwise supply one through `TsCustomOrd`, or generation fails with "`Ord` instance requested for … but not found".

## Naming

- Codec const: `decap(base) + "C"` (`Foo` → `fooC`; all-caps names keep their case). Codec type: `cap` of that (`FooC`). Value type: `Foo`.
- Unions: codec and codec type `FooCU`, value type `FooU`; plus `allFooC`, `allFooNames`, `FooName`, `FooMap<A>` (non-generic unions), `allFoo` (all-object unions) and `fooOrd` (all-object, non-generic unions).
- Cross-file imports are aliased `importedN_Name`; same-file references are rewritten back to the plain name during `resolve`.

## Consumer customization

- `TsImports.Config` — where each fp-ts/io-ts/io-ts-types reference comes from; `iotsBigNumber`, `iotsLocalDate` and `iotsThese` have no default and fail generation with "… import config value missing" if a type needs them.
- `TsCustomType` — replace generation for a type, matched on its fully-qualified name **string**. Renaming or moving the Scala type silently falls back to structural generation.
- `TsCustomOrd` — supply `Ord` instances by `TypeName`.

## Footguns

- **Run-time, not compile-time, failures.** Unregistered references (`UnresolvedTsImportException`), missing config (`sys.error`), missing `Ord`, and empty unions all fail when the consumer runs generation, not when it compiles.
- **Union types are references only.** `parse[A | B]` at the top level aborts compilation ("Union types are only supported as references").
- **Same type in two files.** `generateAll` de-duplicates per file by full type name, and `makeTypeToFile` keeps the last file seen; register each type in one file.
- **Output changes are breaking for every consumer.** Their generated files change on upgrade; describe the before/after TypeScript in the PR and bump `version` in `build.sbt` for a release.
