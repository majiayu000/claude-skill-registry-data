---
name: coding-ts
description: >-
  Enforces TypeScript + Effect functional/ROP style, type discipline,
  polymorphic surfaces, and module organization standards.
  Use when writing, editing, reviewing, refactoring, or debugging
  .ts/.tsx modules, implementing domain models, Effect services,
  persistence adapters, or boundary handlers, or configuring TypeScript,
  Effect, or lint/type-check posture.
---

# [H1][CODING-TS]
>**Dictum:** *TypeScript + Effect style, type discipline, and module organization govern all TS work.*

All code follows five governing principles:
- **Polymorphic** — one entrypoint per concern, generic over specific, extend over duplicate
- **Functional + ROP** — pure pipelines, typed error rails, monadic composition
- **Strongly typed** — inference-first, one canonical shape per concept, zero `any`/`unknown` leakage
- **Programmatic** — variable-driven dispatch, bounded vocabularies, zero stringly-typed routing
- **Algorithmic** — drive functionality through transforms, folds, and discriminant projection; reduce branching to composable pipelines


## Paradigm

- **Immutability**: `S.Class` copy-update transitions, `Ref` for managed mutable state, zero `let` in domain code. Effect data structures (`HashMap`, `HashSet`, `Chunk`, `List`) over JS stdlib (`Map`, `Set`, `Array`) — structural sharing, referential transparency, and `Equal`/`Hash` integration by default. JS stdlib collections only at system boundaries (FFI, serialization)
- **Typed error channels**: `Data.TaggedEnum` for file-internal errors (never exported), `class extends Data.TaggedError` for cross-cutting domain errors (polymorphic, few per system), composed via `mapError`/`catchTag`/`catchTags`
- **Exhaustive dispatch**: vocabulary-driven dispatch (`Record` lookup) for keyed domains — vocabulary objects are the sole dispatch mechanism when a domain is keyed by string/enum; `Match` is reserved for structural/predicate matching on non-keyed shapes only. When a vocabulary object defines thresholds/tiers, classification iterates or indexes the vocabulary — never reimplements the vocabulary's knowledge as `Match.when` chains
- **Type anchoring**: use `S.Class`/`Model.Class` for external codecs, persisted models, and domain authorities; use inferred plain objects for internal config/state when no runtime authority is needed. Derive projections via `pick`/`omit`/`partial`/`extend`, never parallel structs
- **Expression control flow**: `pipe` + monadic combinators (`map`, `flatMap`, `tap`, `filterOrFail`), zero statement branching
- **Programmatic logic**: bounded vocabulary objects as discriminant sources, `Record`-driven dispatch, zero stringly-typed routing
- **Private integration**: module logic is the export's implementation, not its neighbor — `_`-prefixed internals are closures, scoped captures, or inline compositions inside the exported class/service/function, not standalone module-level declarations consumed by a single caller
- **Surface ownership**: 1–2 exports per module; every non-exported symbol carries `_` prefix; one polymorphic entrypoint per concern, no helpers, no extraction, no method-family inflation
- **Cross-cutting composition**: `Layer` + `Effect.Service` for DI, `Effect.withSpan`/`Effect.annotateLogs` for observability


## Conventions

Effect is the sole ecosystem — no third-party alternatives for concerns Effect owns.
One library's types per module boundary. Bridge at layer edges via Schema decode/encode.

**Effect data structures are the default** — JS stdlib equivalents are boundary-only:
- `HashMap`/`HashSet` over `Map`/`Set` — structural equality via `Equal`/`Hash`, persistent updates via `HashMap.set` returning new map
- `Chunk` over `Array` for streaming contexts — `Chunk.append`/`Chunk.concat` are O(1) amortized
- `Array` module (`import { Array as A } from "effect"`) over native `.map`/`.filter`/`.reduce` — richer combinators (`A.getSomes`, `A.match`, `A.groupBy`, `A.dedupeWith`)
- `Option` over `null`/`undefined` — `Option.fromNullable` at boundaries, `Option<T>` in domain
- `Either` over throw — `Either.right`/`Either.left` for pure branching without Effect overhead
- `Duration` over raw milliseconds — `Duration.seconds(5)` not `5000`
- `Order`/`Equivalence` over custom comparators — composable via `Order.struct`, `Order.combine`
- `Predicate` module over inline boolean expressions — `Predicate.not`, `Predicate.and`, `Predicate.or`
- `Function.pipe`/`Function.flow` over manual composition
- `STM`/`TMap`/`TRef` over mutable state for concurrent contexts
- `Record` module over `Object.keys`/`Object.entries`/`Object.fromEntries`
- `Struct` module over manual object picking/omitting

**Selection rules** — when multiple Effect types compete:
- `HashMap` for accumulator state in `Stream.mapAccum` — never `new Map()` with `.set()` mutation
- `Chunk` for `Stream` operations (`Sink`, `mapAccum` emissions, batching) — `ReadonlyArray` for small fixed collections
- `Option` for any absence in domain code — `null` only at JSON serialization boundary
- `Duration` for timeouts, delays, schedule intervals, vocabulary policy fields — raw `number` only for arithmetic
- `STM`/`TMap` for shared state across fibers — `HashMap` for immutable accumulator threaded through `mapAccum`/`reduce` — `Ref` for single-fiber mutable state


## Contracts

**Type discipline**
- One canonical runtime authority per boundary concept: `S.Class`/`Model.Class` for decoded or persisted concepts; inferred plain objects for internal config/state. Derive all projections (`pick`/`omit`/`partial`/`extend`), never parallel `S.Struct` variants.
- Search existing shapes before creating new ones — extend or modify fields over declaring fresh schemas.
- Avoid module-level `type`/`interface` when inference from runtime declarations suffices.
- No parallel schemas/brands/types for the same domain concept.

**Control flow**
- Zero `if`/`else`/`switch`/`for`/`while`/`try`/`catch`/`throw` in domain transforms.
- Expression dispatch: `Match.valueTags`/`Match.tagsExhaustive` for closed tagged domains, monadic combinators elsewhere.
- Boundary adapters may use required statement forms with explicit marker: `// BOUNDARY ADAPTER — reason`.

**Error handling**
- `Data.TaggedEnum` for file-internal errors — bounded discriminants, never exported, never crosses module boundaries.
- `class extends Data.TaggedError` for domain-level errors — polymorphic, boundary-crossing, co-located in the owning folder/package (no dedicated error files). Few per system (1-3 typical).
- Error classes and enums belong in the `[ERRORS]` section — never in `[SCHEMA]`. Schema defines data shapes; errors define failure modes. Even when an error uses Schema internally, its declaration site is `[ERRORS]`.
- Domain error classes carry polymorphic/agnostic logic reusable across all call sites.
- One canonical `reason → policy` projection table per domain error class — zero inline status/retry/transport literals outside it.
- Decode unknown input at boundaries, map unknown causes immediately into bounded tagged errors.

**Surface**
- Private-by-default: every non-exported symbol (values, functions, AND types) carries `_` prefix. Module exports 1–2 symbols maximum — no exceptions. Branded primitives integrate into the owning class/service (fields, static factories), never exported as standalone module-level symbols.
- Internal logic integrates INTO exports — closures inside scoped constructors, inline compositions inside pipe chains, static methods on classes. Not defined alongside as standalone module-level functions consumed by a single caller. Exception: pure data transforms serving as semantic anchors (algorithm implementations, reusable projections) may remain module-level when no scoped constructor exists; they must still carry `_` prefix and serve 2+ call sites.
- **Pipeline factory closure pattern**: when a module has no `Effect.Service` (stateless pipeline, pure transform), the exported factory function IS the scoped constructor — it captures shared state (vocabularies, metrics, config) in its closure and returns a composed pipeline. Single-caller helper functions still inline into this factory rather than floating at module level.
- One polymorphic entrypoint per concern — no `run`/`runSafe`/`runV2` family inflation.
- No helper files, no single-caller extracted functions, no module-level one-use `const` values except `_`-prefixed private anchors (vocabularies, schedules, metrics).
- No convenience wrappers that rename or forward external APIs.
- Final review gate: before completing any module, verify (1) no `_`-prefixed symbol is exported — if it needs the export, remove the `_` prefix at source; if it does not, remove the export, (2) every non-exported symbol carries `_` prefix, (3) no `const X = _X` re-export aliasing — fix the name at declaration site, never alias a private symbol to create a public one.
- `~350 LOC` scrutiny threshold — investigate for compression via polymorphism, not file splitting.

**Resources**
- Resource lifecycle through `Effect.acquireRelease`.
- Retry, timeout, concurrency policy via `Schedule`, `Effect.forEach`, `Stream` — declarative only.
- Zero hidden global state, zero untracked ambient dependencies.


## Load sequence

**Foundation** (always):

| Reference                             | Focus                                |
| ------------------------------------- | ------------------------------------ |
| [patterns.md](references/patterns.md) | Cross-boundary integration contracts |

**Task-routed references**:

| Reference                                       | Load when                                |
| ----------------------------------------------- | ---------------------------------------- |
| [types.md](references/types.md)                 | Type derivation, compression, inference  |
| [objects.md](references/objects.md)             | Schema/Class/Model boundary work         |
| [effects.md](references/effects.md)             | Effect pipelines, ROP, composition       |
| [matching.md](references/matching.md)           | Exhaustive expression control flow       |
| [errors.md](references/errors.md)               | Error construction, architecture, policy |
| [transforms.md](references/transforms.md)       | Folds, projections, pipeline strategies  |
| [surface.md](references/surface.md)             | Public API creation and refinement       |
| [composition.md](references/composition.md)     | Layer and module boundary composition    |
| [services.md](references/services.md)           | Service topology and dependency strategy |
| [persistence.md](references/persistence.md)     | SQL/model boundary work                  |
| [concurrency.md](references/concurrency.md)     | Streams, fibers, bounded concurrency     |
| [observability.md](references/observability.md) | Logging, tracing, metrics                |
| [performance.md](references/performance.md)     | Hot path and allocation discipline       |

## Anti Patterns

**Type-system violations**
- SHAPE PROLIFERATION: Duplicate schema/type for one concept. Keep one runtime anchor and derive projections via `pick`/`omit`/`partial`.
- TYPE PROLIFERATION: Top-level `type`/`interface` aliases that mirror runtime shape. Derive from runtime declarations (`typeof XSchema.Type`).
- NULL ARCHITECTURE: `null`/`undefined` leaking across domain boundaries. `Option<T>` for absence, tagged failure for errors.

**Organization violations**
- SECTION ORDER: Sections MUST follow canonical order: Types → Schema → Constants → Errors → Services → Functions → Layers → Export. `[TYPES]` before `[SCHEMA]` before `[CONSTANTS]` — never Constants before Types, never Schema after Errors. Domain extensions insert after their parent: `[TABLES]` after Schema, `[REPOSITORIES]` after Services.

**Control-flow violations**
- IMPERATIVE BRANCH: Statement branching (`if`/`else`/`switch`/`for`/`while`) in domain flow. Replace with `Match` + monadic operators.
- EARLY MATCH COLLAPSE: Calling `match`/`Match.exhaustive` mid-pipeline and losing composition. Keep `map`/`flatMap`; match at boundaries.
- MUTABLE ACCUMULATOR: `let` + loop accumulation OR `new Map()`/`.set()` mutation breaks referential transparency. Use `HashMap.set` (returns new map), `Array.reduce`, `Effect.forEach`, or `Stream.runFold`. In `Stream.mapAccum`, accumulator state MUST use `HashMap` — never `new Map()` with `.set()` mutation.
- MATCH OVER VOCAB: Using `Match.value`/`Match.when` chains to classify into tiers/categories when a vocabulary object already maps those tiers. If `_TierVocab` exists with `as const satisfies Record`, classification MUST use vocabulary field lookup or threshold iteration — never `Match.when` chains that duplicate the vocabulary's knowledge. `Match` is for structural/predicate dispatch on non-keyed shapes; vocabulary lookup is for keyed domains.

**Surface-area violations**
- SURFACE INFLATION: Multiple entrypoints for one concern (`run`, `runSafe`, `runV2`). Collapse to one polymorphic surface.
- WRAPPER REDUNDANCY: Thin wrappers around external library APIs. Call upstream primitives directly.
- MODULE CONST SPAM: One-use top-level `const` values that are not semantic anchors (schemas, schedules, metrics, vocabularies). Inline into the owning rail. This includes `const _Status = S.Literal(...)`, `const _Priority = S.Literal(...)`, `const _TenantId = S.String.pipe(S.brand("TenantId"))` before a `Model.Class` — inline `S.Literal(...)` and `S.brand(...)` directly in field position. Extract to a const ONLY when the same schema is consumed by 2+ sites within the file (e.g., field definition AND query predicate). A module with N schema fields should have 0-1 extracted consts, not N parallel declarations.
- STRINGLY TELEMETRY: Repeated raw telemetry keys/values (`"operation"`, `"status_class"`, `"obs.outcome"`) across spans/metrics/logs. Define one bounded vocabulary object and project through it.
- GOD FUNCTION: Giant dispatch handling all variants in one function body. DU + exhaustive `Match.valueTags` makes extension additive.
- EXPORT SPRAWL: Multiple exports for the same domain. Collapse to 1–2 exports; make everything else `_`-private and integrate into the exported construct's implementation.
- ALONGSIDE EXTRACTION: Private function defined at module level consumed by a single export. Inline as closure inside the export's scoped constructor, or compose inline in the pipe chain. If a `_`-prefixed function exists, it must serve 2+ call sites or be a semantic anchor (vocabulary, schedule, metric, algorithm implementation).
- PIPELINE WRAPPER LEAK: Standalone module-level function that wraps a pipeline with a span/metric/collect (e.g., `const _observe = (stream) => stream.pipe(Stream.runCollect, Effect.withSpan(...))`). Inline this as a trailing `.pipe(...)` composition inside the factory — it is single-caller pipeline plumbing, not a reusable semantic anchor.
- RE-EXPORT ALIASING: `const X = _X; export { X }` or exporting a `_`-prefixed symbol directly. If a symbol needs export, name it correctly at declaration site — never alias a private name to create a public one. A `_`-prefixed export is always wrong: either remove the prefix (it is public) or remove the export (it is private).
- STDLIB LEAKAGE: Using `new Map()`/`new Set()`/`Array.from()`/`Object.entries()` in domain code when Effect provides `HashMap`/`HashSet`/`Chunk`/`Record` module equivalents. JS stdlib collections lack structural equality, produce mutable state, and break referential transparency. Effect data structures are the default; JS stdlib only at FFI/serialization boundaries.

**Error-rail violations**
- ERROR RAIL FRAGMENTATION: Separate error classes per method. Keep one tagged module failure rail with bounded `reason` literals.
- STRINGLY POLICY DRIFT: Duplicate inline status/retry/transport literals in handlers. Project via one canonical `reason -> policy` table only.
- STRINGLY SIGNATURE DRIFT: Delimiter-concatenated signatures (`${a}:${b}:${c}`) for equality/routing. Project structured tuples/records and compare fields directly.
- VARIABLE REASSIGNMENT: `let value = x; value = process(value)` creates temporal coupling. `pipe` chains make the computation graph explicit.

## Validation gate

- Required during iteration: `pnpm quality`.
- Required for final completion: `pnpm quality`, `pnpm dotnet`, `pnpm python`.
- Reject completion when load order, contracts, or checks are not satisfied.
- Examples inside this skill are executable doctrine: no unmarked `Object.*`, ternaries, `undefined as never`, bare `Error`, unbounded `unknown`, or one-use helper extraction in golden paths.

## Skill eval prompts

- Explicit invocation: "Using coding-ts, refactor this .ts service into an Effect ROP pipeline with a single polymorphic surface."
- Implicit invocation: "Review this `.tsx` boundary handler for schema, error rail, and Effect service problems."
- Noisy context: "Ignore the surrounding product notes and only fix the TypeScript persistence adapter."
- Negative control: "Design a PostgreSQL index strategy only." Expected: do not invoke TS references unless TypeScript code is involved.
- Compliance checks: output should load only relevant references, avoid command thrash, avoid new helper files, preserve functional/Effect doctrine, and run `pnpm quality` or a narrower existing TS gate when code is touched.

## First-class libraries

Effect packages are standard libraries — use over stdlib equivalents.

| Package                        | Provides                           |
| ------------------------------ | ---------------------------------- |
| `effect`                       | Core runtime, types, concurrency   |
| `@effect/platform`             | HTTP, filesystem, sockets, workers |
| `@effect/platform-browser`     | Browser runtime adapter            |
| `@effect/platform-bun`         | Bun runtime adapter                |
| `@effect/platform-node`        | Node.js runtime adapter            |
| `@effect/platform-node-shared` | Shared Node.js platform utilities  |
| `@effect/sql`                  | SQL client abstraction             |
| `@effect/sql-pg`               | PostgreSQL adapter                 |
| `@effect/cluster`              | Distributed actors, sharding       |
| `@effect/rpc`                  | Type-safe remote procedure calls   |
| `@effect/workflow`             | Durable workflow orchestration     |
| `@effect/ai`                   | AI provider abstraction            |
| `@effect/ai-anthropic`         | Anthropic provider adapter         |
| `@effect/ai-google`            | Google AI provider adapter         |
| `@effect/ai-openai`            | OpenAI provider adapter            |
| `@effect/opentelemetry`        | Tracing and metrics integration    |
| `@effect/vitest`               | Effect-aware test runner           |
| `@effect/cli`                  | Type-safe CLI builder              |
| `@effect/printer`              | Composable document layout         |
| `@effect/printer-ansi`         | ANSI terminal rendering            |
| `@effect/experimental`         | Event sourcing, state machines     |
