---
name: skmtc-lang-kotlin
version: 0.11.0
description: >
  The Kotlin target-language layer for Skmtc generators
  (@skmtc/lang-kotlin): base factories, KtSnippet, the seven entity
  kinds, packages-from-paths imports, the head+value render model,
  KtAnnotation and the composition classes, sanitization and
  @SerialName placement, plus the current-API worked example (the
  shipped gen-kotlin-* packages are API-stale — do not copy their call
  shapes). Use ALONGSIDE skmtc-generator whenever a generator emits
  Kotlin. Headings mirror skmtc-lang-typescript.
metadata:
  internal: true
---

# The Kotlin layer (@skmtc/lang-kotlin)

Read `skmtc-generator` first.

> **Drift warning.** The API of record is the workspace
> `skmtc/deno/lang-kotlin` and its tests. The shipped `gen-kotlin-*`
> generators predate the 0.9.11 flattening: they call
> `new KtAnnotation('Name', [args])` positionally and import
> `isKtAnnotated`/`isKtSupertyped` (no longer exported; supertype
> clauses now render inline in the value). Clone their **structure**
> only; take call shapes from THIS skill's example (§8), which is pinned
> byte-for-byte against the engine by
> `lang-kotlin/src/skill-example.test.ts`.

## 1. Declaring the language

Same pattern as TypeScript — the import graph declares it. Two
factories: `toKtModelProjectionBase`, `toKtOasOperationProjectionBase`;
snippets extend `KtSnippet`.

```ts
export const KtModelBase = toKtModelProjectionBase<EnrichmentSchema>({
  id: denoJson.name,
  toEnrichmentSchema,
  toIdentifierName({ refName, enrichments }) {
    return enrichments?.subject?.name ?? capitalize(camelCase(refName))
  },
  // Kotlin's identifier KIND depends on schema shape → may read context
  // (runs only on cache-miss; the NAME stays pure):
  toIdentifierType(refName, context) {
    return { type: toShape(context, peekSchema(context, refName)) }
  },
  toExportPath({ refName, enrichments }) {
    const name = enrichments?.subject?.name ?? capitalize(camelCase(refName))
    return `@/${enrichments.generator.basePackage.replaceAll('.', '/')}/${name}.generated.kt`
  }
})
```

The export path's directory segments ARE the Kotlin package (§4). Make
`basePackage` a **required generator-scope enrichment** with no default;
validate segments with `isKtIdentifierName` + `ktHardKeywords`. Put the
shape dispatch (object+props → `data-class`; string+enums →
`enum-class`; qualifying discriminated union → `sealed-interface`; else
`typealias`) in ONE deterministic function read by both
`toIdentifierType` and the constructor, so kind and value can't disagree.

## 2. Register shapes — Kotlin differences

Same three shapes as TS (projection own-file / `registerInto` / snippet
with required `destinationPath`), plus `defineAndRegister` (no cache
check; no `noExport` — visibility is the identifier's fact: pass
`exported: false` to the factory). Compile-time differences: **no
`reExports` field** (Kotlin has none) and **no `type` tag on imports**
(no type-only imports). `custom` renders above the `package` directive.

## 3. Identifier kinds

Kotlin output has seven entity kinds (`KtEntityType`): `class`,
`data-class`, `enum-class`, `interface`, `sealed-interface`,
`typealias`, `val` —
factories `createClass`, `createDataClass`, `createEnumClass`,
`createInterface`, `createSealedInterface`, `createTypeAlias`,
`createValue` (only `createValue` takes `typeName`; `exported: false`
renders `private `). Deferred kinds (`object`, `fun`, `var`) make
`toKtEntityType` throw — deliberately loud. Kind does NOT affect import
form. The engine's `type` is an opaque string: `isKtEntityType` narrows
it to the vocabulary above, and `isKtIdentifier` narrows a neutral
`IdentifierBase` back to `KtIdentifier`.

## 4. Emitted-import rules

- **Packages from paths**: `@/com/example/api/User.generated.kt` →
  `package com.example.api`. Segments are validated, never sanitized —
  a keyword or invalid segment **throws** (fix the path policy).
- One `import pkg.Name` per symbol (no brace grouping), `as` aliases,
  rendered **sorted** (determinism, not style).
- **Same-package suppression is central**: register imports
  unconditionally; `KtFile` drops same-package ones at render.
- Importing from the default package throws (root-level artifact
  referenced from a packaged one = path-policy bug).

## 5. Render model: head + value

Assignment kinds (`typealias`, `val`): `<head> = <value>`. Declaration
kinds: `<head><value>` — the value renders everything after the name:
parameter list (parens included), inline ` : Parent` clauses, ` { … }`
bodies; an empty value yields the bodyless idiom
(`sealed interface Animal`).

Two things ride on value-carried protocols (the neutral Lang signature
has no slot for them): `KtAnnotated` (`annotations: KtAnnotation[]`,
strict — string look-alikes are silently dropped) and `KtDocumented`
(`description`, guard `isKtDocumented`, rendered as KDoc above the
annotations). **The mirroring gotcha**: the Driver wraps the
PROJECTION as the definition's value, so mirror both onto the projection
— canon is **reference assignment in the constructor**
(`this.annotations = this.value.annotations` — one array, two names;
never copy) — or class-level annotations and KDoc silently vanish.

## 6. Composition classes (current API)

- `KtParameterList(parameters)` — parens included; each
  `{ name, type: Stringable, nullable?, defaultValue?, annotations?,
  visibility? }` renders as an indented `val`, annotations one per line.
- `KtPrimaryConstructor({ parameters, modifiers? })` — modifiers force
  the explicit `constructor` keyword.
- `KtFunctionSignature({ name, parameters, returnType?, annotations?,
  body? })` — abstract by default, expression body only.
- `KtAnnotation({ context, name, args?, target?, packageName?,
  destinationPath })` — a **registering leaf**: with `packageName` it
  registers its own import (register unconditionally; suppression
  handles same-package). `args` are pre-quoted (`['"user_id"']`,
  `['Foo::class']`). `target` is the use-site target
  (`KtAnnotationTarget`: `field`/`get`/`set`/…) rendered as
  `@field:JsonAnySetter` — the imported symbol stays the bare `name`.
  Needed on a constructor `val`, which is parameter/property/field/
  getter at once: Jackson's catch-all pair is `@field:JsonAnySetter` +
  `@get:JsonAnyGetter`, and without targets both annotations land on
  the parameter, where Jackson never looks. (Shipped in lang-kotlin
  0.10.0, 2026-08-04 — pre-`target` versions cannot express use-site
  targets at all.)
- `withDescription(value, { description })` — KDoc.

## 7. Sanitization and @SerialName

`sanitizePropertyName(name)`: plain → unchanged; hard keyword or invalid
→ **backticked**; JVM-unescapable characters → **throws** ("rename +
@SerialName"). Renames are NOT its job — serialization annotations
handle wire-name mismatches, and the two compose: decide the annotation
by comparing the *unescaped* chosen name with the wire key
(`` `object` `` needs no @SerialName; `user_id`→`userId` does). Only the
28 hard keywords escape; soft/modifier keywords (`value`, `data`,
`sealed`) are legal identifiers. Canonical pairing:
`sanitizePropertyName(camelCase(key))`.

## 8. Worked example — kotlinx data class (current API, engine-pinned)

Per-property loop inside the data-class value snippet:

```ts
const propertyName = sanitizePropertyName(camelCase(key))
const annotations: KtAnnotation[] = []
if (propertyName.replaceAll('`', '') !== key) {
  annotations.push(new KtAnnotation({
    context, destinationPath,
    name: 'SerialName', packageName: 'kotlinx.serialization', args: [`"${key}"`]
  }))
}
parameters.push({
  name: propertyName,
  type: value,                     // the SNIPPET — never `${value}`
  defaultValue: isRequired ? undefined : 'null',
  annotations
})
// this.parameterList = new KtParameterList(parameters)
// class-level: this.annotations = [new KtAnnotation({ context,
//   destinationPath, name: 'Serializable', packageName: 'kotlinx.serialization' })]
// projection mirrors by REFERENCE: this.annotations = this.value.annotations
```

Renders (verified byte-for-byte through the engine):

```kotlin
package com.example.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class User(
    @SerialName("user_id")
    val userId: String,
    val name: String,
    val email: String? = null
)
```

The type expression is the **single owner** of `?`; the parameter layer
only adds `= null`. Passing `` `${value}` `` instead of the snippet
strands its registered imports and synthesized siblings — the file
breaks far from the cause. Serialization flavor is confined to the value
files (data class / enum entries / sealed interface): a Jackson/Moshi
sibling generator swaps annotation construction there only.

## 8b. Normalized models — KNOWN ENGINE GAP (verified 2026-08-03)

The head+value model means a Kotlin value renders differently in TYPE
position (`Map<String, Any?>`) and DECLARATION position (a parameter
list). Core's generic `insertNormalizedModel` glues the identifier
head to the value's type-position `toString()` — which for an inline
OBJECT schema renders invalid Kotlin: `data class XMap<String, Any?>`.
The engine gap is real, but the SOLUTION does not wait for it —
every mature Kotlin generator solves inline objects the same way:

- **Named `$ref` schemas are unaffected** — `insertModel` and the ref
  path work correctly.
- An inline NON-object schema normalizes fine as a `typealias`-shaped
  value.
- **An inline object is SYNTHESIZED as a named sibling declaration**
  and referenced by name — the retired gen-kotlin-kotlinx pattern
  (`KtObjectValue`, skmtc-generators history at `2c24a65`) rebuilt
  WITHOUT its naming-hint threading: the name derives from the
  schema's own `stackTrail` (`toSynthesizedName.ts` in
  gen-kotlin-jackson — anchor on the `components`/`paths` landmark
  frames, never absolute indices; classification is POSITIONAL:
  `properties` consumes the following frame as a literal key, so a
  property named `properties`/`schema`/`items` can never be mistaken
  for trail structure), so every construction path — including peers
  arriving through `insertNormalizedModel` — lands on the same name
  with NO parameter added to the router contract. Names are NOT
  collision-free: claim via the document-wide registry
  (`claimSynthesizedName`, gen-kotlin-jackson `synthesizedNames.ts`)
  BEFORE declaring — it throws per-item when the name collides with a
  component-derived class name (Kotlin's redeclaration scope is the
  PACKAGE, not the file) or with a different position's claim
  (camelCase-convergent keys), and returns reuse for a same-position
  re-walk. On `'declare'`, `defineAndRegister` the sibling and render
  only the NAME. Type position then always holds a name or a map —
  never property structure. This is also how OpenAPI Generator solves it
  (inline schemas hoisted to named components before generation).
  Widening a known shape to `Map<String, Any?>` is capitulation, not
  a solution — it discards the type the schema gave you. Inline
  string enums synthesize the same way (`enum class` sibling).
- Never fabricate a refName or drive the peer's identity statics to
  force a declaration into existence — that is the two-doors rule
  (skmtc-generator §4), and the result couples you to the peer's
  private snippet shape.

## 8c. Discriminated unions — sealed interfaces (shipped 2026-08-04)

Kotlin has no union type; a QUALIFYING discriminated union becomes a
`sealed interface` (gen-kotlin-jackson is the worked example; ancestry:
the retired kotlinx machinery at skmtc-generators `2c24a65`, stale call
shapes). Predicate (`shape.ts isSealedUnion`, part of the shape
dispatch): discriminated, ≥2 members, every member a `$ref` to an
object-with-properties, and every member keeps ≥1 parameter AFTER
discriminator omission. Everything else renders the honest wire type
(`JsonNode` for Jackson), never `Any`.

- **The inversion scan.** OpenAPI points parent → member; Kotlin
  declares member → parent (`data class Dog(...) : Pet`). Memoization
  makes build order arbitrary, so membership must be known BEFORE any
  construction: one document-wide scan over `components.schemas`,
  memoized per document via `WeakMap`, mapping member refName → claims.
  Claims store the parent's real `RefName`; the consumer derives the
  display name via `context.toModelContentSettings` — never a copy of
  the naming policy, never a fabricated refName.
- **Parent side**: an empty-body value (`toString()` returns `''` →
  the bodyless idiom) carrying `@JsonTypeInfo(use = NAME, include =
  PROPERTY, property = "<discriminator>")` + `@JsonSubTypes(Type(value
  = Dog::class, name = "dog"), …)` via the `KtAnnotated` protocol —
  mirror `annotations` AND `description` on the projection by
  reference. Each subtype entry holds the walked member ref SNIPPET,
  so member models build and imports stitch through the normal chain.
  Tags: `discriminator.mapping` key pointing at the member, else the
  member's refName (the OpenAPI default).
- **Member side**: inline ` : Pet` supertype clause rendered by the
  parameter-list value (after the parens), and the discriminator
  property OMITTED — filtered BEFORE the property walk, or its enum
  schema synthesizes a spurious sibling. Same package by the
  export-path policy satisfies Kotlin's sealed same-package rule.
- **Jackson vs kotlinx flavor**: tags are parent-side
  (`@JsonSubTypes`), so members carry no tag annotation and one member
  may hold different tags under different parents (the kotlinx
  one-`@SerialName`-per-class conflict rule does not apply).
- **Runtime gotcha (probed)**: a raw `writeValueAsString(list)` erases
  the element type and silently DROPS the tags; concrete roots,
  `writerFor(type)`, and full-generic types all write them — Spring
  MVC uses the typed path, so real consumers are fine. Test round-trips
  with a typed writer.
- `allOf`-composed members (the spec's canonical idiom: shared fields
  on a base, members compose via `allOf`) qualify WITHOUT special
  handling — core resolves `allOf` at parse time (`mergeIntersection`),
  so the member peeks as a flat object and the base's fields flatten
  into each data class (verified through the pipeline 2026-08-04).
  Flattening is the right Kotlin target: the sealed interface is the
  polymorphism seam, not class inheritance.
- **Inline unions (stage 2, shipped)**: a qualifying union ANYWHERE —
  component property, operation body/response/header/parameter —
  synthesizes its sealed parent under its stackTrail name (combinator
  frames `oneOf`/`anyOf`/`allOf` are structural and elided; a
  `parameters/<index>` position resolves to the parameter NAME via a
  WeakMap document scan — the trail itself cannot carry names, it
  doubles as a JSON Pointer where `parameters` is an array) into the
  MODELS package (`toModelExportPath` — ONE placement policy for EVERY
  synthesized declaration; caller's-file placement breaks
  `'reuse'`-across-files for cross-package peers). The scan deep-walks
  components AND operations AND webhooks (headers and the `content`
  alternative included); synthesized claims carry the union NODE so
  `ensureSealedParent` lets WHOEVER needs the name first declare it via
  the claim registry. Derivability is ONE shared non-throwing probe
  (`toSynthesizedNameOrNull`) across scan/render/members — underivable
  roots degrade consistently to pre-synthesis behavior; the object/enum
  sites deliberately keep the THROWING derivation (no honest fallback
  exists for structure). One member may implement several sealed
  parents (parent-side tags).
- Not yet built: undiscriminated unions (stage 3 —
  enrichment-asserted hints / Jackson `Id.DEDUCTION`) and the INVERTED
  swagger-style pattern (discriminator on the base, no `oneOf`,
  membership implied by `allOf` back-references — no union node exists,
  so no sealed interface).

## 9. Kotlin pitfalls

| Symptom | Fix |
|---|---|
| `@Serializable`/KDoc missing | Mirror `annotations`/`description` getters on the projection |
| Annotation silently dropped | Real `KtAnnotation` instances, not strings |
| `segment 'x' is not a valid package name part` | Fix the export-path policy — packages validate, never sanitize |
| Import mid-file / duplicated | `register` / annotation `packageName`, never templates |
| `String??` | Type expression owns the single `?` |
| `Unknown Kotlin entity type` | Use the seven Kotlin factories, not TS kinds |
| Empty `data class` throws | Shape dispatch must route empty objects to `typealias` |
| TDZ crash at module load | Break base↔router↔projection cycles with a leaf module (`peekSchema` pattern) |
| Nondeterministic output | No module state; config via enrichments; memoize document scans in `WeakMap` |
| `data class X` glued to `Map<String, Any?>` | The normalized-insert type/declaration gap — §8b, don't hack around it |
| Union renders `Any`/`JsonNode` where a sealed type was expected | Qualifying predicate failed — check discriminator presence, all-ref members, per-member surviving parameters (§8c) |
| Member missing ` : Parent` / spurious discriminator enum sibling | Membership scan not consulted before construction, or omission applied after the property walk (§8c) |
| Sealed round-trip loses the wire tag at runtime | Jackson root-list type erasure — serialize via a typed writer; generated code is correct (§8c) |

<!-- api-appendix:begin — GENERATED, do not edit by hand -->

## Appendix — generated API reference

The full `deno doc` surface for the packages this skill covers lives
in [`appendix.md`](appendix.md), in this skill's directory —
generated from framework source — signatures and field docs only.
It is **authoritative**: when the prose above does
not carry the exact constructor or field shape you need, Read (or
grep) `appendix.md` instead of diving into package source. Do not
guess signatures. For a symbol not listed there,
`deno doc <file> <Symbol>` against the framework source beats
grepping it.

<!-- api-appendix:end -->
