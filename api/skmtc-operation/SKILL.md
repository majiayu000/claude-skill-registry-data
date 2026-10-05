---
name: skmtc-operation
version: 0.1.2
description: >
  The operation-generator shape for Skmtc: one definition per (path,
  method), for any output family — client hooks, SDK methods, forms,
  route stubs, docs. Output varies wildly; the DECOMPOSITION of the
  operation and the peer-consumption rules do not. Core teaching:
  every schema that appears in your output is a reference to a model
  generator's definition, obtained through the insert machinery —
  never rendered text. Use when authoring or editing a generator whose
  subject is operations ("write a gen for API clients/hooks/routes",
  "generate an SDK/form per endpoint"). Covers the projection shape
  only — accumulators (many operations → one file) are out of scope.
  Load ALONGSIDE skmtc-generator and the emitted language's skill.
metadata:
  describes:
    '@skmtc/core': '0.29'
---

# Operation generators: decompose the operation, reference the models

An **operation generator** turns each operation — subject `(path,
method)` — into one definition in one file. Unlike models, there is no
single output shape: a TanStack hook, a Kotlin SDK method, a form
component, and a doc page look nothing alike. What they share is the
**decomposition**: every one of them is assembled from the same
subject-derived pieces plus references to model generators' artifacts.
Author the composition; never re-derive the pieces.

## 1. The method

Clone the nearest stock generator **by output family** (there is no
fill-in skeleton for this shape yet):

| Output family | Clone |
|---|---|
| client call / hook, consuming a model generator | `@skmtc/gen-tanstack-query-fetch-zod` — the canonical instance |
| per-operation UI (forms), variant-aware | `@skmtc/gen-shadcn-form` |
| many operations appended into ONE file | that is an **accumulator** — out of scope here; see skmtc-generator §4 and clone `gen-msw`/`gen-express` |

The clone gives you the anatomy (same package convention as models:
entry / base / projection / value snippets). This skill carries the
rules the clone can't show you.

## 2. The subject API — read, never re-parse

Every piece of the operation comes from the engine's `OasOperation`,
by name. Re-spelling any of them (parsing the path yourself, guessing
a response shape) breaks the moment the schema evolves.

- **Name**: derive from **method + path** via core's
  `toEndpointName(operation)` (post→Create, put→Update...), then apply
  your policy (`use` prefix, `Fn` suffix). **Never `operationId`** —
  author-controlled, absent in many specs, unstable across emitters.
- **Filter**: `isSupported({ operation })` in the entry config — claim
  only what you can render (e.g. mutations require
  `operation.toRequestBody(({ schema }) => schema)` to exist). An
  unfiltered entry constructs subjects it can't handle and fails them
  one by one.
- **Inputs**: `operation.toParams(['path'])` / `['query']` /
  `['header']` for individual parameters;
  `operation.toParametersObject()` for all of them as ONE object
  schema — the form you hand to a model generator (§3).
- **Request body**: `operation.toRequestBody(({ schema }) => schema)`.
- **Response**: `operation.toSuccessResponse()?.resolve().toSchema()
  ?? OasVoid.empty()` — selection and void-fallback in one idiom.
- **Request line**: `operation.path` and `operation.method` are stored
  facts; the target-syntax path template (`/users/${id}` vs
  `"/users/{id}"`) is RENDER-time work done by your lang layer's
  path-template helper inside a `toString()` body.
- **Grouping**: `operation.tags`.

## 3. The operation law: schemas in your output are peer references

An operation's params object, request body, and response are schemas —
and rendering a schema is a MODEL generator's job. The single worst
operation-generator failure is rendering one inline: it compiles, then
duplicates the model, drifts from the canonical definition, and its
imports never settle.

Inline (unnamed) schemas go through the projection's
`insertNormalizedModel`, with a fallback name derived from **your own
settings identifier** so variants stay distinct automatically:

```ts
const args = this.insertNormalizedModel(PeerProjection, {
  schema: operation.toParametersObject(),
  fallbackName: `${capitalize(settings.identifier.name)}Args`
})

const response = this.insertNormalizedModel(PeerProjection, {
  schema: operation.toSuccessResponse()?.resolve().toSchema() ?? OasVoid.empty(),
  fallbackName: `${decapitalize(settings.identifier.name)}Response`
})
this.responseName = response.identifier.name   // the NAME is yours; the definition is theirs
```

Named `$ref` schemas go through `insertModel(Peer, refName)` (name via
`.toName()`). Either way: the peer renders the schema ONCE at its own
path, your file's import is stitched by the engine, and only the
identifier lands in your tree. Import peer projections through their
package alias (`@skmtc/gen-zod`), never by relative path.

When the peer declares caller options, the trailing argument is
required and typed by the peer:
`this.insertModel(Peer, refName, { options: { suffix: 'Input' } })` —
a fresh object per insertion; a peer that declares none refuses the
key. On `insertNormalizedModel` the options reach the `$ref` branch
only: the inline branch constructs no projection, so put whatever
distinguishes the call into `fallbackName`.

What the insert gives you — the name, the placement (normalized models
co-locate at YOUR export path via the base wrapper), the declaration
form — **is the convention**. If it does not match what you want, do
not fight it by driving the peer's machinery yourself: fabricating a
refName to key the peer's identity statics, calling its
`toExportPath`/`toIdentifierName` directly, or reading fields off its
returned value beyond the definition and its name are all the same
mistake — a reimplementation of the engine that passes every automated
check and breaks on the next peer or engine change. Those are the TWO
DOORS of skmtc-generator §4; when neither door fits, do not settle
for a degraded render — research how other code generators handle the
same edge case (the lang skill's notes, retired in-house generators in
git history, OpenAPI Generator's inline-model hoisting). The usual
answer is a synthesized named declaration, reached through the peer's
exported API or your own lang package's `defineAndRegister`. If the
known solution needs machinery the engine lacks, name the gap in your
summary and raise it — never silently ship the degraded form.

## 4. Dispatch and composition

Models route on schema type; operations route on **operation kind** —
method, response shape, body presence — at the top of the projection:

```ts
this.client = match(operation)
  .with({ method: 'get' }, () => isListResponse(operation)
    ? new PaginatedQuery({ context, operation, settings })
    : new Query({ context, operation, settings }))
  .otherwise(() => new Mutation({ context, operation, settings }))
```

Each kind is its own snippet class taking `(context, operation,
settings)` (`OasOperationProjectionConstructorArgs`), storing snippets
and peer names in its constructor, and composing target syntax ONLY in
`toString()`. Runtime-library imports (`useQuery`, a client class)
register in the constructor. The litmus from skmtc-generator
applies with one addition: if you are about to write a schema's
target-syntax by hand — a field list, a validator call, a type body —
stop; that is a peer insert.

## 5. Variants

`transform({ context, operation, variant })` — pass `variant` through:
`context.insertOperation({ projection, operation, variant })`.
Dropping it constructs every variant as `'main'` and dies on the
second with `Registered definition mismatch`. Names fold the variant
via `withVariant` in the base; anything you derive from
`settings.identifier.name` (incl. §3 fallback names) inherits it for
free — one reason never to hand-compose those names.

## 6. Enrichments

Same three-scope umbrella as models; the subject key for operations is
`[path][method]` (plus variant where variants exist). Opt-out stays
`toEnrichmentSchema = () => emptyEnrichmentSchema`.

## 7. Verify

Generation is sub-second — run after every change. Operation-specific
reading order: (1) your artifact's **import header** — every consumed
model must appear as an import of the peer's file (missing = a string
swallowed a schema); (2) the peer's files — each consumed schema
defined exactly ONCE, named as expected (an `Args`/`Response`
explosion or a `...2` suffix means fallback names collided or weren't
identifier-derived); (3) unsupported operations absent, not errored.

## 8. Operation pitfalls

| Symptom | Fix |
|---|---|
| Names change when the spec author edits `operationId` | Derive from method+path via `toEndpointName` |
| Response/body/params rendered inline in your file | §3 — insert into a model peer; only the name lands in your tree |
| Peer model duplicated per operation | `fallbackName` not derived from `settings.identifier.name`, or peer referenced by hand-written name |
| `Registered definition mismatch` on the second variant | Thread `variant` into `insertOperation` |
| `Registered definition mismatch` naming `Cached options` | The peer's name ignores options its output depends on — fix the peer's `toIdentifierName`, not your call |
| Run fails on operations you never meant to handle | Missing/loose `isSupported` |
| Path renders with wrong interpolation | Path template belongs to the lang layer, at render — never build it into a stored string |
| Peer import points into another package's source tree | Import via the `@skmtc/*` package alias |
| A helper builds a `#/components/schemas/...` string, or calls a peer's identity statics | Reimplemented insert machinery — two doors only (skmtc-generator §4) |
| Peer's rendered value looks wrong in declaration position | Lang-level type-vs-declaration gap — see the lang skill's known-gap notes, don't pluck the peer's internals |

## 9. Boundaries

Engine rules (the one law, memoization, the two insert return shapes,
enrichment umbrellas) live in **skmtc-generator** — read it first.
Everything concrete about the emitted language — the
`to<Lang>OasOperationProjectionBase` factory, parameter-list and
path-template helpers, import forms — lives in the lang skill
(`skmtc-lang-typescript`). The model side
of the seam (how the peer you insert into actually renders schemas) is
**skmtc-model**. Accumulator generators — many subjects appending
into one shared definition via the `findDefinition ??
defineAndRegister` idiom — are a different shape, deliberately not
covered here.
