---
name: skmtc-generator
version: 0.14.0
description: >
  Author and edit Skmtc generators — packages that project an OpenAPI
  domain model into application code. Method: clone the nearest stock
  generator, then apply the engine rules imitation can't teach. Assumes
  zero prior Skmtc knowledge. Use when asked to "write a skmtc
  generator", "author/clone/customize gen-x", "add a field type",
  "change export paths", "add enrichment options", or when editing
  generator source. ALWAYS pair with the target language's skill
  (skmtc-lang-typescript).
metadata:
  describes:
    '@skmtc/core': '0.29'
---

# Authoring Skmtc generators

## 1. What Skmtc is

Skmtc derives application code from an OpenAPI document treated as a
domain model. A **stack** of **generators** (small, opinionated,
cloneable packages) is run by a deterministic engine that sweeps every
subject of the schema — each **model** (component schema, by `refName`)
and each **operation** (`path` + `method`) — through each generator.
Outputs are regenerated wholesale every run: never hand-edit generated
files; customize the generator. Generators compose: a React-Query
generator reuses the Zod generator's schemas through the engine's cache.

## 2. The method: start from a stock generator

Generator source code is the customization surface: stock generators
hardcode their export paths and peer imports on purpose, so the fastest
reliable route to a correct generator is imitation of a published one —
clone the structure, swap the target syntax. Pick the nearest exemplar:

| Need | Clone |
|---|---|
| model → validator/schema value | load **skmtc-model** and copy its engine-tested skeleton (fill-in slots; gen-zod is its pattern source) |
| model → type declaration | `@skmtc/gen-typescript` |
| operation → client hook/SDK/form, consuming a model generator | load **skmtc-operation** (decomposition + peer-consumption rules; gen-tanstack-query-fetch-zod is its canonical instance) |
| many subjects → one shared file (accumulator) | `@skmtc/gen-msw`, `@skmtc/gen-express` |
| Kotlin | `@skmtc/gen-kotlin-jackson` (current lang-kotlin API; the older gen-kotlin-* were retired) |

Fetch source from JSR: `https://jsr.io/@skmtc/<name>/meta.json` → pick
version → fetch files (or `deno doc jsr:@skmtc/<name>`). Keep the
package convention as cloned, with one exception: declare `@skmtc/*`
dependencies as caret ranges (`^x.y.z`), even where the clone source
pins them exactly — an exact core pin puts a second copy of core in the
bundle as soon as the project pins a different core:

```
gen-x/  deno.json (name @scope/gen-*, caret-range @skmtc/* pins (^x.y.z),
        lint plugin jsr:@skmtc/lint-plugin)
        mod.ts            → re-exports + `export { entry as default }`
        src/mod.ts        → the entry: toModelEntry / toOasOperationEntry
        src/base.ts       → identity statics via the lang base factory
        src/enrichments.ts→ enrichment schema (emptyEnrichmentSchema opt-out)
        src/XProjection.ts→ constructor builds the value tree
        src/<router>.ts   → schema-type → snippet dispatch
```

What you adapt: the identity policy in `base.ts` (names, export paths,
identifier kind) and the router's per-type snippets (your target
syntax). What you keep: everything else — the shape is the point.

## 3. The one law: your code never writes output text

Three phases: parse → **generate** (your code runs here) → render
(`toString()` runs once per file, only here). During generate the output
does not exist; your generator builds **object trees** the engine can
walk, attribute, deduplicate, and settle imports from.

**The trap**: template strings full of target syntax
(`` `export const ${name} = ...` ``) compile, render — and silently break
imports (never settled into the header), reuse (text is invisible to the
cache → duplicates), composition (peers can't reference text), and
provenance. Lint rules `skmtc/no-template-imports` and
`skmtc/no-adhoc-tostring` catch the worst mechanically; keep them wired.

**Litmus, applied at the keystroke**: target-language punctuation inside
a string that will be STORED on an object → stop, build the object.
Strings are legitimate as *leaves*: identifier names, export paths,
module specifiers, literals, a cached peer *name*, and final syntax
assembled **inside a `toString()` body** from already-structured fields.
Prefer composing even render-time syntax inside `toString()` over helper
functions that return strings — helpers drift.

## 4. What imitation can't teach: the engine rules

- **Identity before construction.** `toIdentifierName` / `toIdentifierType`
  / `toExportPath` are statics computed from `(subject, enrichments,
  variant)` WITHOUT constructing the projection. This is the invariant
  everything rests on: cheap cache probes, and peers knowing where your
  artifact *will* live. Never make a name depend on construction.
- **Coordination is memoization.** No plugin registry, no dependency
  graph, no topological sort — the cache is the file map, keyed
  `(identifier.name, exportPath)`, and every producer creates its own
  dependencies. Generator order does not affect output; never propose
  ordering, priorities, or a pre-generation pass. On a peer reference the Driver probes
  `findDefinition`; hit → reuse (constructor never runs) + auto-stitched
  import; miss → construct recursively. So: never hardcode a peer's name
  or path — insert and read the result, minding the two return shapes:
  `insertModel(Peer, refName)` returns an **Inserted handle** (name via
  `.toName()`, definition via `.definition`), while
  `insertNormalizedModel(Peer, { schema, fallbackName })` returns the
  **definition itself** (name via `.identifier.name`). Never hand-write
  peer imports; never import a peer's naming helpers (ask
  `context.toModelContentSettings` if you need identity without
  materializing). Key collision under different generators throws
  `Registered definition mismatch`.
- **Two composition shapes.** Projection (one definition per subject —
  entry calls `insertModel`/`insertOperation`) and accumulator (many
  subjects append into one definition — entry does
  `context.findDefinition(...) ?? defineAndRegister(context, {...})`
  then mutates the container value; the sanctioned exception to "no
  methods beyond constructor and toString"). `defineAndRegister` is a
  **lang-package free function** (import it from your lang package) —
  there is no `context.defineAndRegister`; that API was deleted.
- **Peers have exactly two doors**: the insert machinery, or an API the
  peer package explicitly exports. Never call another generator's
  identity statics (`toIdentifierName`/`toExportPath`/`toEnrichments`)
  yourself, and never fabricate a refName — `toRefName` on a string you
  built points at a schema that does not exist, and attribution,
  enrichment routing, and recursion tracking are all keyed by REAL
  refNames; the fabrication survives only until something resolves it.
  If the sanctioned call cannot express what you need, do NOT settle
  for a degraded render — a widened type (`Map<String, Any?>` for a
  known shape) is capitulation, not a solution. Treat the situation as
  a solved problem you haven't found yet: research how other code
  generators handle this exact edge case — the stock lineup, retired
  in-house generators (git history is a design archive), and mature
  external tools (OpenAPI Generator, Fabrikt). The answer is almost
  always to SYNTHESIZE a named declaration and reference it by name
  (`findDefinition` probe + your lang package's `defineAndRegister`).
  The synthesized NAME derives from the schema's own `stackTrail` — a
  pure function from position to name, computed at the point of need
  (`components/schemas/Order/properties/metadata` → `OrderMetadata`;
  an operation-rooted trail reuses `toMethodVerb` naming →
  `CreateApiOrdersBody`). Never thread a naming hint as a parameter:
  position-derived names are deterministic, collision-free (distinct
  positions → distinct trails), and reach EVERY construction path —
  including values built through `insertNormalizedModel`'s contract,
  which cannot pass a hint. Two rules: anchor on the document landmarks
  (`components`/`paths`), never absolute indices — the trail's head
  carries per-run tracing frames (`trace-*`/`span-*`/`parse`); and
  throw on an unrecognized or empty trail rather than invent a name
  (the engine isolates the throw to that subject). Worked example:
  `toSynthesizedName.ts` in the kotlin-debug rig's gen-kotlin-jackson
  (verified end-to-end 2026-08-04, compiler-clean).
  Only when the known solution needs machinery the engine genuinely
  lacks have you found an ENGINE GAP — name it in your summary and
  raise it; never silently ship the degraded form as if it were the
  answer. Never re-create engine machinery inside a generator — a
  faithful-looking counterfeit passes every automated check and breaks,
  far from the cause, on the next engine change.
- **When in doubt, make it a producer.** The cost asymmetry is one-way:
  a producer that never needed to be one costs a few lines; a string
  that later needed to be a producer severs the chain for everything
  built on it. Assume your value will be built upon.
- **The variant axis fans out at the engine, not the generator.** One
  subject can produce N definitions via named variants declared in
  enrichments; `'main'` is always present. Thread the variant:
  `transform({ context, operation, variant })` →
  pass `variant` through to `insertOperation`, and fold it into names
  with `withVariant`. Dropping it collides every variant onto `'main'`.
- **Enrichments are the settings your generator needs that the
  document cannot supply; the consumer provides them; options are
  the caller's.** Declare them as a valibot three-scope umbrella
  (`subject`/`generator`/`stack`) in `enrichments.ts` — that schema is
  the whole contract the consumer's `client.json` can fill; the
  opt-out is
  `export const toEnrichmentSchema = () => emptyEnrichmentSchema` — a
  FUNCTION returning the schema, required in both the entry config and
  the base-factory config. Read via
  `this.settings.enrichments.subject?...`; the run-constant scopes
  (`client.json` keys `[id]._generator` and `._stack`, umbrella
  members `generator` and `stack` — no underscore in generator code)
  are read outside a projection with `toGeneratorEnrichment` /
  `toStackEnrichment`. Declare every scope you read: a scope left
  `v.undefined()` rejects any value at its key (so `_stack` needs
  every generator in the run to declare `stack`; check each
  generator's `enrichments.ts` — most stock ones declare `subject` only).
  A wrong-typed value fails that item only; keys the schema drops and
  routing paths nothing read land on `manifest.enrichmentWarnings`.
  Options come from the CALLING generator, on the insert:
  `this.insertModel(Peer, refName, { options: { suffix: 'Input' } })`.
  A projection declares its options type on its base factory (the
  veneer's second type parameter: `toTsModelProjectionBase<E, Options>`);
  the Driver hands them to `toIdentifierName` / `toExportPath` and the
  constructor, and the instance stores them as `this.options`. Options
  are identity: fold them into `toIdentifierName` whenever the output
  depends on them, or a second insertion with different options throws
  `Registered definition mismatch`. The call surface follows the
  declaration — `{ options }` is required when the peer declares
  options and a type error when it does not; declare `T | undefined`
  to make it optional. Pass a fresh object per insertion. Module state
  is never a channel: it breaks determinism.
- **Naming**: models from `refName` casing (core's `camelCase`,
  `capitalize`, `decapitalize`); operations from **method + path** via
  core's `toEndpointName` (post→Create, put→Update). **Never**
  `operationId` — spec-author-controlled; no stock generator reads it.
- **Registration at construction; `toString()` is a prototype method**
  reading precomputed fields (an arrow-function `toString` field breaks
  provenance wrapping). Errors are isolated per subject — a throw kills
  one artifact, not the run.

## 5. Verify against the run

**Never guess a signature.** Skmtc has almost no training-data presence;
your recalled API shapes are unreliable. Exact signatures for core
contracts (`Oas*` classes, `Inserted`, `ContentSettings`,
`TypeSystemArgs`, entry configs) are one command away:
`deno doc jsr:@skmtc/core@<pinned-version> <SymbolName>` — read it
instead of guessing, and instead of casting around a type error. In
particular `OasSchema` is a union type, not a class hierarchy: every
variant implements `.isRef()` returning `false`, and `OasRef` is a
sibling with `.isRef()` returning `true`.

Render does not run Prettier or Biome — no formatter runs inside the
engine, so read the raw output as the generator produced it and format
as a post-generation step.

Generation is sub-second — run it after every meaningful change. Read in
order: (1) manifest — expected definitions at expected paths? parse
issues? per-item errors? (2) one golden artifact — **import header
first** (missing import = a string swallowed a snippet), then the body;
(3) `deno lint`; (4) if you consume a peer: their definition exists once
and your file imports it. Never "fix" missing output by concatenating
the text into a template.

## 6. Pitfalls

| Symptom | Fix |
|---|---|
| Import missing / appears mid-file | Declare via `register`, never in templates |
| Duplicate definitions of a shared model | Reference peers via `insertModel`, not by name |
| `Registered definition mismatch` | Thread `variant`; or two generators claim one (name, path) |
| `Registered definition mismatch` naming `Cached options` | The peer's output depends on its options but its name ignores them — fold options into `toIdentifierName` |
| Peer output name wrong | Read `.identifier.name` off the insert result |
| Works once, breaks on recursion/refs | Build tree in constructor; refs via the ref snippet/Driver |
| Enrichment ignored | Umbrella routing key mismatch — check warnings |
| Output edits vanish | You edited generated files; customize the generator |
| Router misroutes custom values | `schema.type === 'custom'` is a real dispatch case — presence-test with `'readOnly' in schema`-style guards, not type equality |
| `null` slips through an optional guard | `!== undefined` lets `null` pass on Nullable generics — check both |
| `insertResult.identifier` is a type error | You have an `Inserted` handle (from `insertModel`) — use `.toName()`/`.definition`; only `insertNormalizedModel` returns the definition |
| `` toRefName(`...${name}`) `` anywhere | Fabricated ref — go through a peer's two doors, never its statics |
| Reading fields off a peer's value beyond the definition/name | Coupled to the peer's PRIVATE snippet shape — it will change silently |

## 7. The lang layer

The engine is language-blind; the import graph declares the language —
a generator imports its projection-base factories and snippet base from
its language package, and the Drivers read the language off the
projection class. Everything concrete — base-factory names, snippet
classes, File/Import/Definition, identifier factories, emitted-language
import rules, sanitization — lives in that package and its skill.
Load `skmtc-lang-typescript` before writing code (the Kotlin layer has
its own skill, not yet published). Lang skill wins on language
specifics; this skill wins on engine semantics. Two SHAPE skills carry the per-shape guidance — load the
one matching your subject: `skmtc-model` (fill-in skeleton, model
edge cases: refs, recursion, visibility) or `skmtc-operation`
(operation decomposition, peer-consumption rules). Shape-specific
guidance lives there, not here.

Scope note: this skill covers **OpenAPI input**. GraphQL SDL input
exists (`toGqlOperationEntry`, subject routing by
`[rootKind][fieldName]`) and the engine rules here apply to it
unchanged, but the GraphQL specifics — the entry, the enrichment
routing, the companion base factories — are not covered here.
