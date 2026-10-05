---
name: skmtc-architecture
version: 0.1.1
description: |
  Understand what SKMTC is, how its engine works, and the
  architectural invariants — for agents building or extending
  infrastructure *around* SKMTC rather than authoring generators or
  running the CLI. Covers the three-phase pipeline, the host/Worker
  boundary, cross-generator coordination, the manifest, the
  attribution / gen-maps (provenance) subsystem, the package graph,
  the dependency substrate, and the design decisions that make SKMTC
  behave unlike a typical codegen tool.

  Use this skill when the user asks "what is SKMTC", "how does the
  SKMTC engine work", "explain the SKMTC architecture", or is
  building platform infrastructure around SKMTC — a hosted generate
  API, a schema or generator registry, tracing or provenance
  tooling, a web app or SaaS that wraps the engine, or
  platform-level CI integration. This skill is the system mental
  model. It does NOT cover authoring generators (→ skmtc-generator),
  running CLI commands (→ skmtc-cli), or diagnosing broken runs
  (→ skmtc-debug).
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  internal: true
---

# SKMTC architecture

This skill is the **system mental model** for agents building
infrastructure around SKMTC — a hosted generation service, a schema
or generator registry, provenance and tracing tooling, a web app
that wraps the engine. It explains *what SKMTC is, how it works, and
why it behaves the way it does* — deeply enough to reason about and
extend, without the generator-authoring or CLI-operating detail the
sibling skills carry.

SKMTC is **counter-intuitive on purpose**. Most of what generic
codegen and generic backend-infra training data would suggest is
actively wrong here. The fastest way to make a bad architectural
proposal is to extrapolate from another tool. Read §1 and §11 before
proposing anything.

## 1. The five facts that override default LLM intuitions

These override what training-data priors suggest about codegen
tools. They apply across every SKMTC interaction; an infra builder
needs facts 1, 2 and 5 most.

1. **No plugin registry, no dependency graph, no topological sort.**
   Cross-generator coordination is a `Map` cache keyed by
   `(identifier.name, exportPath)`. Generator execution order does
   not affect output.

2. **Render does not run Prettier or Biome.** No formatter runs
   inside `@skmtc/core`. Generated output is unformatted by design;
   consumers format separately.

3. **Generator source code is the customization surface.** Stock
   generators have *deliberately* hardcoded export paths and peer
   imports. To customize beyond enrichments: clone the generator and
   edit it. There are no config flags for paths or output shape.

4. **`OasSchema` is a union type, not a class hierarchy.** Sibling
   classes (`OasObject`, `OasArray`, `OasString`, …) each
   independently implement `.isRef()` returning `false`. `OasRef` is
   a *sibling* with `.isRef()` returning `true`. There is no
   `BaseSchema`.

5. **Every generation run is from cold.** One Deno Worker is spawned
   per `generate`, runs Parse → Generate → Render once, posts the
   result back, and is terminated. No warm pool, no cross-run cache,
   no incremental rebuild. `toArtifacts` is a pure function of
   `(document, settings, generators)`. Determinism is chosen over
   speed deliberately — **caching belongs outside the engine**, keyed
   on input hashes.

## 2. What SKMTC is

> SKMTC is a code generator. It takes one **OpenAPI v3** document or
> one **GraphQL SDL** schema and produces
> **source files** — types, runtime validators, query hooks, forms,
> mocks, server routes — all derived from that one schema, in one
> run, all consistent with each other. The output is committed to the
> consumer's repository like any other source code; there is **zero
> SKMTC runtime** in the consumer's bundle. The engine is
> **language-blind** (core 0.8.0+): a generator declares its target
> language by importing its projection-base factories and snippet
> base from a `@skmtc/lang-*` package — the import graph alone
> carries the language; entries have no `lang` field. TypeScript
> (`@skmtc/lang-typescript`) and Kotlin (`@skmtc/lang-kotlin`, proven
> by `gen-kotlin` DTOs + `gen-kotlin-spring` controllers) are the
> production languages; other `lang-*` packages (C#, …) are the
> roadmap.

The crucial reframing for an infrastructure builder: **SKMTC is an
engine with several thin hosts, not a CLI.** The CLI is one host.
The mental decomposition:

| Layer | Package | Role |
|---|---|---|
| **Engine** | `@skmtc/core` | The three-phase pipeline. Entry point: `core/run/toArtifacts.ts`. |
| **Worker host** | `@skmtc/worker` | Wraps the engine in a Deno Worker `postMessage` handler. |
| **CLI host** | `@skmtc/cli` | Local developer surface: scaffold, install, bundle, generate, watch. |
| **HTTP host** | `@skmtc/server` | Hono app — the hosted "Sandbox API". `POST /artifacts`. |
| **MCP host** | `@skmtc/mcp` | Model Context Protocol server surface. |
| **Schema normalizer** | `@skmtc/convert`, `@skmtc/openapi-down-convert` | Swagger 2 / OAS 3.1 → OAS 3.0. Runs *before* the engine. |
| **Generators** | `@skmtc/gen-*` | The actual codegen logic, distributed as JSR packages. |

Every host does the same thing: get a schema, call `toArtifacts`,
do something with `{ artifacts, manifest }`. **A SaaS is just
another host of the same engine.**

## 3. What you get — the benefits

- **Multi-artifact coherence.** One schema yields N artifact types
  (types + validators + hooks + forms + mocks + routes) that
  reference each other correctly. Add a field, regenerate, every
  artifact updates consistently.
- **Output is committed source code.** Reviewable in `git diff`,
  grep-able, refactorable. No runtime library, no peer-dependency
  package at deploy time. Schema/output drift is visible in version
  control.
- **Determinism.** Same inputs → byte-identical output. No hidden
  state, no order dependence, no warm-cache effects.
- **Idempotency by construction.** Generators coordinate by
  memoization, not by a dependency graph — so they can be written,
  tested, and reasoned about in isolation, and order never matters.
- **Clone-to-customize.** Generators are owned source code, not
  opaque configured dependencies (the shadcn/ui model).
- **Lenient input, strict diagnostics.** One malformed schema does
  not kill the run; it is logged and its dependents pruned. The
  `manifest.json` is an exhaustive record even when output is
  partial.
- **OAS and GraphQL through one engine.** The GraphQL pipeline reuses
  the same DSL, the same renderer, the same manifest.

## 4. When to use SKMTC — and when not to

| Verdict | Situation |
|---|---|
| **Strong fit** | An OpenAPI v3 or GraphQL schema is the contract; you need *multiple* artifact types from it; you want generated code committed to the repo. |
| **Overkill** | You only need types (`openapi-typescript`); you only need a typed fetch client (`@hey-api/openapi-ts`); schemas are dynamic at runtime (use a runtime renderer). |
| **Wrong tool** | Can't run Deno *and* won't use the hosted Sandbox API; you need production output in a language with no `@skmtc/lang-*` package yet (today that is everything except TypeScript — use `openapi-generator`). |

SKMTC's closest peer is `kubb` — multi-target, TypeScript-native.
The distinguishing bet is the **customization model**: clones (source
you own) over plugins (configured packages), plus **coordination by
name** (memoization) over explicit composition. Full landscape:
[`explanation/comparison-to-other-tools.md`](../../explanation/comparison-to-other-tools.md).

## 5. How it works — the pipeline

A generation run is a one-way pipeline of three phases, each
producing an immutable artifact the next consumes:

```
        ┌─────────────── HOST PROCESS ───────────────┐
        │  bootstrap · fetch schema · OAS pre-parse   │
        └──────────────────────┬──────────────────────┘
                               │  postMessage(GENERATE)
        ┌──────────────────────▼──────────────────────┐
        │        DENO WORKER  (sandboxed)             │
        │   PARSE  ─▶  GENERATE  ─▶  RENDER            │
        │   model     files map      { path: text }   │
        │   +issues   (in memory)    artifacts        │
        └──────────────────────┬──────────────────────┘
                               │  postMessage(RESULT)
        ┌──────────────────────▼──────────────────────┐
        │  HOST: write files to disk · write manifest │
        └─────────────────────────────────────────────┘
```

- **Parse** — schema → typed object model (`OasDocument` /
  `GqlDocument`). Lenient: a per-item parser that throws becomes a
  `ParseIssue`; `removeErroredItems` then prunes one hop of `$ref`
  consumers of any failed component. Generate can trust every
  surviving item.
- **Generate** — walk the configured generators over the parsed
  document, producing an in-memory `Map<path, File>`. Generators
  produce output via side effects (`register` / `insert*`), never by
  return value. Memoized **Drivers** dedupe and coordinate (§6).
- **Render** — serialize each `File` to a string by joining
  re-exports, imports, and definitions. **No formatter runs.** Output
  is `Record<path, content>`.

Each phase boundary is an immutable hand-off — the next phase reads,
never mutates. Detail:
[`concepts/the-three-phases.md`](../../concepts/the-three-phases.md).

### The host / Worker boundary

The engine physically runs in a **Deno Worker** spawned by the host,
one per run (fact 5). The boundary is `postMessage`, which uses the
structured-clone algorithm — and that shapes a real asymmetry:

- **OAS is parsed host-side.** A plain `OpenAPIV3.Document` is JSON —
  it survives structured clone. The host normalizes Swagger 2 / OAS
  3.1 to 3.0 via `@skmtc/convert`, then posts the plain document.
- **GraphQL is parsed Worker-side.** A parsed `GqlDocument` has class
  instances with cyclic back-references — structured clone strips
  methods and prototypes. So the host posts the raw SDL **string**
  and the Worker parses it.

The Worker boundary is also the **security boundary**. The Worker is
spawned with Deno permissions `read: true, write: true, env: true,
net: false, run: false`. Generator code (third-party JSR packages or
team-edited clones) cannot make network calls or spawn subprocesses.
It is a *soft sandbox* — it limits the blast radius of a buggy or
compromised generator, not a determined attacker. Schema fetching
happens host-side, before the Worker exists. Detail:
[`concepts/the-worker-runtime.md`](../../concepts/the-worker-runtime.md),
[`explanation/security-model.md`](../../explanation/security-model.md).

### The engine entry point

Every host calls one function:

```ts
toArtifacts({
  traceId, spanId, startAt,          // run correlation
  document,                          // SkmtcDocumentInput (oas | gql)
  settings,                          // ClientSettings (basePath, enrichments, skip, include)
  toGeneratorConfigMap,              // () => the registered generators
  stackTrail,                        // position/trace stack
  silent,
  attribution                        // optional — turns on gen-maps (§8)
}): { artifacts: Record<string,string>; manifest: ManifestContent;
      sidecars?; generationMap? }
```

It is pure with respect to its inputs and does no I/O of its own
beyond reading. `core/run/toArtifacts.ts`, `worker/mod.ts`, and
`server/src/createServer.ts` are three independent callers of it —
study them as the templates for a fourth.

## 6. How it works — cross-generator coordination

This is the single most counter-intuitive piece. There is **no
dependency graph and no topological sort.** Coordination is
**memoization**:

- A generator that needs a peer's output calls
  `this.insertOperation(PeerProjection, op)` (or `insertModel` /
  `insertNormalizedModel`).
- A **Driver** (`OasOperationDriver`, `GqlOperationDriver`,
  `ModelDriver`) computes a cache key `(identifier.name, exportPath)`
  — both pure functions of `(operation, enrichments, variant, options)`
  via the peer's static methods. `options` is typed data the caller
  passes on the insert; a peer that uses it folds it into the name.
- **Cache hit** → the existing `Definition` is reused, after an
  integrity check (generator key, class, and the caller's options — a
  hit built with different options throws). **Miss** → the
  peer's Projection is constructed (which may recurse), wrapped in a
  `Definition`, registered, and its import stitched into the calling
  file.

Because the key is a pure function of inputs, whichever generator
asks first triggers construction and everyone after gets a cache
hit — so the output `Map<path, File>` is **identical regardless of
generator order**. A `generatorKey` integrity check throws
`"Registered definition mismatch"` if two different
generator-and-input pairs collide on one cache key.

**Why this matters for infra:** order-independence means there is
nothing to schedule or sequence. Determinism means the *correct
caching layer is outside the engine* — cache the whole
`{ artifacts, manifest }` result keyed on a hash of
`(schema, settings, bundle)`. Never try to cache *inside* a run.
Detail:
[`concepts/cross-generator-coordination.md`](../../concepts/cross-generator-coordination.md).

## 7. The DSL in one screen

You do not need to author generators to build infrastructure, but
you should recognize the vocabulary (defer authoring to
`skmtc-generator`):

- A **generator** is a JSR package exporting an *entry* built with
  `toOasOperationEntry` / `toGqlOperationEntry` / `toModelEntry`.
  Entries are pure pipeline config — no `lang` field; the generator
  declares its target language by importing its projection bases
  from a `@skmtc/lang-*` package, and the engine's Drivers read it
  off the projection class's inherited static.
- The entry's `transform` hook runs once per matched operation/model
  and produces output by calling `register` / `insert*` — its return
  value is discarded.
- A **Projection** is a *named, file-scope* artifact (`export const
  X = …`), wrapped in a `Definition`, cached by `(name, exportPath)`,
  reachable by other generators. A **Snippet** is an *anonymous*
  fragment embedded into a Projection's body via template-literal
  interpolation.
- Templates are TypeScript template literals inside classes — not
  `.hbs`/`.mustache` files. Composition is by `${...}` interpolation
  of anything `Stringable`. (Generators are *authored* in
  TypeScript/Deno regardless of the target language they emit.)

**Vocabulary discipline:** in SKMTC prose use `register`, `insert`,
`render`. Avoid *emit*, *dispatch*, *stitch* — they map to no
exported surface. See
[`reference/glossary.md`](../../reference/glossary.md#skmtc-vocabulary--load-bearing-terms).

## 8. The manifest — the run contract and tracing

Every run writes a `manifest.json` (to
`.skmtc/<project>/.settings/manifest.json` for the CLI host;
returned in-band for the HTTP host). It is the **canonical record of
a run** — written *always, even on failure*. The terminal output is
a summary; the manifest is the full story.

```ts
type ManifestContent = {
  deploymentId: string      // the run; from DENO_DEPLOYMENT_ID or a timestamp
  traceId: string           // OpenTelemetry-shaped correlation key
  spanId: string            // sub-span within the run
  region?: string           // set only for hosted (Deno Deploy) runs
  files:    Record<path, { lines, characters, destinationPath }>
  results:  ResultsItem     // nested tree of per-(generator × item) outcomes
  previews, mappings        // optional UI metadata (per-Definition source descriptors)
  parseIssues: ParseIssue[] // every Parse-phase diagnostic
  startAt, endAt: number    // unix ms; endAt - startAt = worker wall time
}
```

What an infra builder must internalize:

- **Tracing is built in.** `traceId` / `spanId` are
  OpenTelemetry-shaped. The `StackTrail` carries them as its root
  frames, and the `results` tree is keyed by stack-trail strings —
  so an outcome is addressable as
  `traceId → spanId → generate → generatorId → item`. `deploymentId`
  and `region` come from Deno Deploy env vars on the hosted path.
  Wire these straight into an observability backend.
- **Exit / status derives from `parseIssues`, not from throws.** The
  CLI returns exit 1 iff any `parseIssue.level === 'error'`. The
  engine *fails open* — a bad schema does not throw, it logs. Your
  HTTP host must compute status from `manifest.parseIssues`, not from
  a `try/catch` around `toArtifacts`.
- **`results` outcomes:** `success` means "the transform ran without
  throwing" — **not** "produced output". `notSupported` is normal (a
  generator that doesn't apply to an item). `skipped` is filter
  exclusion. Diagnose "no output" via the `files` map, not `results`.
- **No history.** The on-disk manifest is overwritten every run. If
  you want run history, **persist each manifest yourself** — it is
  already the right per-run telemetry payload.

Detail: [`concepts/the-manifest.md`](../../concepts/the-manifest.md),
[`reference/manifest-format.md`](../../reference/manifest-format.md).

## 9. Provenance — the attribution / gen-maps subsystem

`core/anchors/` is the **provenance layer**. Capture is always on;
**emission is opt-in**: pass `attribution: { postPass: {...} }` to
`toArtifacts` (the engine-level `AttributionState` has no `enabled`
field — the `client.json#settings.anchors.enabled` switch is the
user-facing toggle). When emission is on, the run produces two extra
artifact types alongside the code:

- **Sidecar** (`<file>.skm.json`) — one per generated file. A
  pooled, position-indexed map: byte ranges in the rendered file →
  **attribution tuples** `{ genId, srcPtr, variant, defName }`, plus
  generator version and source registry. It is a *source map for
  provenance* — it answers "which generator, which schema location,
  which variant produced *this span* of code?". `srcPtr` is a schema
  pointer like `oas:#/components/schemas/User`.
- **Generation map** (`_map.ndjson`) — a project-level, per-Definition
  **reverse-query index**: "which files came from refName `User`?",
  "which files did `gen-zod` produce?". Wholly rewritten each run.

Both live under `.skmtc/<project>/.maps/` (gitignored by default).
Mechanism: `SnippetBase` instrumentation caches each producer's
rendered text; a post-pass walks the producer tree and AST-resolves
byte spans to landmarks. The AST parser (`oxc-parser`) does not
bundle into a Worker, so **inside the Worker** landmark names come
from `Definition` identifiers and a host-side post-pass can fill AST
detail later.

A lighter, always-on channel exists too: the manifest's `previews`
and `mappings` pair a per-Definition module with a **source
descriptor** (`{ generatorId, operationPath, operationMethod }` etc.)
— enough for a UI to say "this form was generated from `POST
/contacts`".

**If you are building provenance or "trace generated code back to
its schema" tooling, build on this subsystem** (`Sidecar`,
`GenerationMapEntry`, `AttributionState` — exported from
`@skmtc/core/Anchors`). Do not reinvent it.

Full treatment — the four-stage mechanism, the Sidecar v2 format,
the worker-side parser omission, the `doctor` checks:
[`attribution-and-gen-maps.md`](attribution-and-gen-maps.md).

## 10. The package graph and dependencies

### The `@skmtc/*` packages

```
@skmtc/openapi-down-convert   (OAS 3.1 → 3.0, vendored fork)
        ▲
@skmtc/convert                (Swagger 2 / 3.1 → 3.0; YAML/JSON parse)
        ▲
@skmtc/core ◀───────────────── the engine; depended on by everything
        ▲   ▲   ▲   ▲
        │   │   │   └── @skmtc/gen-*   (generators; + peer generators)
        │   │   └────── @skmtc/server  (Hono HTTP host)
        │   └────────── @skmtc/worker  (Deno Worker host)
        └────────────── @skmtc/cli ──▶ @skmtc/mcp (MCP host wraps the CLI)
```

`cli` also depends on `convert` and `worker`. Exact versions live in
each package's `deno.json` — treat that as canonical, not this skill.

### The substrate

SKMTC's design principle "build on the substrate, don't rebuild it"
means **Deno is the platform**:

- `deno bundle` is the bundler — it compiles a project's `worker.ts`
  into `bundle.js`.
- `new Worker(...)` with `deno.permissions` is the sandbox.
- **JSR** is the package registry. Generators and packages are
  *ordinary JSR packages* — there is no bespoke registry layer (that
  was explicitly rejected). Two registries are in play: `jsr.io`
  (public) and `jsr.skmtc.dev` (the SKMTC private registry).
- The hosted Sandbox API runs on **Deno Deploy** (hence
  `DENO_DEPLOYMENT_ID` / `DENO_REGION` flowing into the manifest).

The project is **Deno-locked**, and that is an accepted trade. The
*generated output*, however, runs anywhere TypeScript runs.

### Key third-party dependencies

| Dependency | Used for |
|---|---|
| `valibot` | Runtime validation of the manifest, settings, parse issues, generator configs, and sidecars. Each schema is paired with a TS type via an unread `_driftCheck` binding — **do not delete those**. |
| `graphql` | GraphQL SDL parsing (Worker-side). |
| `oxc-parser` | AST parsing for the attribution post-pass (chosen over `tsc` because `tsc` won't bundle into a Worker). |
| `openapi-types` | Type definitions for OpenAPI documents. |
| `hono` | The `@skmtc/server` HTTP framework. |
| `@modelcontextprotocol/sdk` | The `@skmtc/mcp` server. |
| `swagger2openapi` | Swagger 2.0 → OpenAPI 3.0 conversion inside `@skmtc/convert`. |
| `@cliffy/command`, `ink`, `react` | CLI command parsing and terminal UI. |

**Version-pin discipline:** published `@skmtc/*` packages declare
their `@skmtc/*` dependencies as **caret ranges** (`^0.29.0`; on 0.x a
caret admits patch releases only), so packages released a patch apart
resolve one copy of `@skmtc/core`. The release cascade moves each lower
bound forward when a dependency releases. The project's `deno.json`
keeps an **exact** `@skmtc/core` pin, written from the lower bound of
the CLI's range, and the generated `worker.ts` imports `@skmtc/core`,
so that pin is the one version every range settles on. `skmtc doctor`
checks that it matches the CLI's.
Lower bounds *can* lag between packages; always read `deno.json`.

## 11. Building infrastructure around SKMTC

The user's context: a **GitHub-like SaaS** for hosting APIs and
generators, running them, and supporting tracing and provenance.
Here is how the engine's concepts map onto that platform — and where
the engine stops and your platform code begins.

### The integration map

| Platform concern | What the engine gives you | What you build |
|---|---|---|
| **Hosting APIs (schemas)** | A schema enters `toArtifacts` as `SkmtcDocumentInput` — `{ type:'oas', value: OpenAPIV3.Document }` or `{ type:'gql', value: sdlString }`. `@skmtc/convert` normalizes Swagger 2 / OAS 3.1 to 3.0 *before* the engine. | Schema storage, versioning, ingest validation, the normalize-on-ingest-or-on-run decision. |
| **Hosting generators** | Generators are ordinary JSR packages (`@skmtc/gen-*`). `jsr.skmtc.dev` is already a JSR-compatible private registry. | A registry UX; discovery, search, featured ranking; the publish pipeline. |
| **Running generators** | A run needs a **bundle** — `worker.ts` (templated from the import map) compiled to `bundle.js`. `toArtifacts` then executes it. Three reference hosts exist: local Worker (CLI), Hono `POST /artifacts` (`@skmtc/server`), the Worker message protocol (`@skmtc/worker`). | The run service: validate → convert → `toArtifacts` → return/store `{ artifacts, manifest }`. Bundle build & cache. Execution pooling if you need throughput. |
| **Tracing** | `traceId` / `spanId` / `deploymentId` / `region` already populate the manifest and `StackTrail`; the `results` tree is trace-addressable. | Shipping them to an observability backend; cross-run dashboards. |
| **Provenance** | The attribution / gen-maps subsystem (§8): `sidecars` + `generationMap`, opt-in via `attribution`. | Persisting and serving them; a viewer that maps generated code ↔ schema ↔ generator version. |

### `@skmtc/server` is the seed of the SaaS

`server/src/createServer.ts` is ~150 lines: a Hono app with
`POST /artifacts` (validate a discriminated body → convert →
`toArtifacts` → `{ artifacts, manifest }`), `GET /generators`, and
`POST /to-v3-json`. A production run service is this pattern with
auth, tenancy, persistence, and bundle management added around it.
The MCP host already calls a deployed instance of this server.

### Where the engine stops — build these at the platform layer

The engine deliberately does **schema in → artifacts out** and
nothing else. It has **no notion of**:

- **Users, identity, auth, multi-tenancy.** A SKMTC "project" is a
  *generator configuration*, **not a tenant**. Tenancy is entirely
  yours to build.
- **Persistence or run history.** `toArtifacts` returns a value; the
  on-disk `manifest.json` is overwritten every run.
- **Result caching.** Determinism makes this safe and easy — cache
  `{ artifacts, manifest }` by a hash of `(schema, settings, bundle)`
  — but it is *your* layer, never the engine's.
- **A warm execution pool, rate limiting, quotas, streaming.** Fact
  5: one cold Worker per run. Pool at the *container/process* level
  if you need throughput; never share a context across runs.
- **A plugin / hook API.** There isn't one and it is a rejected
  design. Extension happens by cloning generators or by writing a
  new host — not by hooking the engine.

## 12. Counter-intuitive facts for infrastructure builders

Beyond the five facts in §1. Left column = a reflex from generic
backend / platform training data; right column = SKMTC reality.

| Infra reflex | SKMTC reality |
|---|---|
| Keep a warm worker pool for throughput | One Worker per run, spawned cold, terminated after `RESULT`. Determinism depends on fresh contexts. Pool *containers*, not engine contexts. |
| Do incremental builds — only regenerate changed operations | There are none. Every run is whole-document and from cold. Cache the *whole result* by input hash instead. |
| Retry a failed run | Runs are deterministic — a retry reproduces the same failure exactly. Fix the input; don't retry. |
| Wrap `toArtifacts` in try/catch and 500 on throw | It fails *open* — a bad schema logs a `ParseIssue`, it does not throw. Derive status from `manifest.parseIssues`, not from exceptions. |
| Stream artifacts for large outputs | The Worker batch-`postMessage`s the whole result. No streaming protocol; structured clone handles typical sizes. |
| Format the output before returning it | Output is unformatted *by design*. Formatting is the consumer's separate step. |
| Let generators fetch schemas / templates at run time | The Worker has `net: false`. Everything a generator needs must already be in its inputs. Fetching is host-side, pre-engine. |
| The on-disk `manifest.json` is the run record | It is overwritten every run. Persist each manifest yourself for history. |
| Add an engine plugin/hook API for the platform | Rejected design. Extend by cloning generators or adding a host. |
| A "project" is a tenant / a customer | A project is a *generator configuration*. It is not a unit of tenancy, identity, or billing. |
| Generated code needs the SKMTC runtime at deploy time | Zero runtime. Output is plain committed source; the engine never ships to the consumer's bundle. |

## 13. Boundaries with other skills

- **skmtc-generator** — authoring and editing generators (Projections,
  Snippets, the DSL, customization seams). Load when *writing
  generator code*.
- **skmtc-cli** — running the CLI, configuring `client.json`,
  enrichments, skip/include. Load when *operating* SKMTC.
- **skmtc-debug** — diagnosing broken runs (no output, wrong output,
  errors). Verify-first stance. Load when *something is broken*.
- **skmtc-retro** — end-of-session reflection / friction capture.
- **This skill (skmtc-architecture)** — the system mental model for
  reasoning about and building infrastructure *around* the engine.

If the question is *how the system works* or *how to build a service
around it*, this skill. If it is *how to write a generator*, *how to
run a command*, or *why a run is broken*, hand off.

## 14. Cross-references

**Concepts** —
[`the-three-phases.md`](../../concepts/the-three-phases.md) ·
[`the-worker-runtime.md`](../../concepts/the-worker-runtime.md) ·
[`the-manifest.md`](../../concepts/the-manifest.md) ·
[`stack-trail.md` (reference)](../../reference/api/stack-trail.md) ·
[`cross-generator-coordination.md`](../../concepts/cross-generator-coordination.md) ·
[`generators-as-packages.md`](../../concepts/generators-as-packages.md) ·
[`attribution-and-gen-maps.md`](attribution-and-gen-maps.md)

**Explanation** —
[`design-philosophy.md`](../../explanation/design-philosophy.md) ·
[`security-model.md`](../../explanation/security-model.md) ·
[`comparison-to-other-tools.md`](../../explanation/comparison-to-other-tools.md) ·
[`status-and-roadmap.md`](../../explanation/status-and-roadmap.md)

**Reference** —
[`glossary.md`](../../reference/glossary.md) ·
[`manifest-format.md`](../../reference/manifest-format.md) ·
[`llms.md`](../../llms.md) (consolidated operational reference)

**Source landmarks** — `core/run/toArtifacts.ts` (engine entry) ·
`worker/mod.ts` (Worker host) · `server/src/createServer.ts` (HTTP
host) · `core/context/` (the three context classes) · `core/anchors/`
(attribution / gen-maps).
