---
name: io-ts
description: The io-ts codec shapes scala-ts generates and the rules they must satisfy. Use when changing generated codecs or types, adding a new mapping, or checking that generated TypeScript decodes what the Scala side encodes.
---

# io-ts in scala-ts

Standard io-ts (`t.type`/`t.union`/`t.literal`/`new t.Type`, `t.TypeOf`) is assumed knowledge. This covers the shapes this library emits and the rules they follow. The test harness pins io-ts `2.2.20`, fp-ts `2.16.0` and TypeScript `5.1.3` (`tests/package.json`); consumers may run newer versions.

## The triple every definition emits

```ts
export type FooC = t.TypeC<{ int: t.NumberC }>;               // codec type  (generateCodecType)
export type Foo = { int: number };                             // value type  (generateValueType)
export const fooC: FooC = t.type({ int: t.number }) satisfies t.Type<Foo, unknown>;  // codec (generateCodecInstance)
```

- The `satisfies t.Type<Foo, unknown>` clause is the check that the three agree; keep it on every new top-level codec.
- The codec type is exported by name (not left as `typeof fooC`) so consumers and other generated files can refer to it.
- Generic types become codec functions: `export const fooC = <A1 extends t.Mixed>(A1: A1) => t.type({...}) satisfies t.Type<Foo<t.TypeOf<A1>>, unknown>`.

## Wire format

The codecs decode what circe encodes with a `_tag` discriminator (BondLink's global circe configuration; the tests use `CirceConfig(discriminator = Some("_tag"))`):

- Union members carry `_tag: t.literal("Name")`; singleton `object`s travel as `{ _tag }` only, and a `t.Type` re-attaches their constant fields on decode.
- `Option` → `optionFromNullable` (null/absent ↔ `O.none`); `Either`/`Ior` → `{ _tag: "Left", left }` / `{ _tag: "Both", left, right }` shapes via io-ts-types `either` and a configured `These` codec.
- `Map[String, V]` → `t.record`; other keys → `readonlyMapFromEntries` (a list of pairs on the wire) with an `Ord` for the key.

## Rules for generated output

- Types must not resolve to `{}`, `object` or `any`; `unknown` only where the Scala side is genuinely untyped (`io.circe.Json`, and the open record a field-less case class decodes: `t.UnknownRecord`, which accepts any non-array object just as `t.type({})` would, without typing it as `{}`).
- Immutable values get readonly types: `ReadonlyArray`, `ReadonlySet`, `ReadonlyMap`, `ReadonlyNonEmptyArray`, `t.readonly(...)`.
- Every reference goes through `TsImports.Available` so its import is emitted; never hard-code `t.` / `E.` / `O.` text without the matching import.
- A codec change that alters what decodes is a breaking change for consumers' runtime data, not only their types — check the round-trip tests and say so in the PR.

## Verifying a TS claim

Put the snippet in `tests/output/scratch.ts` and run `cd tests && yarn --silent ts-node output/scratch.ts` — ts-node type-checks under `strict: true` before running. Delete the file afterwards.
