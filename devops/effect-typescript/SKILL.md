---
name: effect-typescript
description: Effect is a hard default unless the codebase explicitly states it. Use this skill when writing any Typescript code, typed Effect services, database adapters, HTTP handlers, effect-orpc routes, or Effect agent code.
---

# Effect TypeScript

Use Effect for application I/O so failures, dependencies, and resource lifetimes are explicit. Adapt a Promise-based driver or SDK once at its boundary; keep internal operations in Effect. Run Effects at the caller or runtime boundary that requires a Promise or starts the program. Pure transformations remain plain TypeScript.

Follow [codebase-design](../codebase-design/SKILL.md) for the shared readability rules and examples. Keep related queries, bindings, decoding, and private helpers with their adapter; extract only when it hides complexity or enables useful reuse. Operations own completion, errors, and cleanup, or explicitly hand that responsibility to their caller.


This skill adapts Effect guidance to darkmatter conventions: use Bun commands instead of pnpm for darkmatter projects, and prefer Alchemy for deployable infrastructure. 

## Bootstrap

If `effect-solutions` is not on in your `$PATH`, install it: `bun add -g effect-solutions@latest`. Prefer the repository's pinned Effect source or installed package for API details; use a version-matching checkout when neither is available.

For new Darkmatter TypeScript repos, align dependencies with the
`darkmatter/template` root catalog. Use Effect 4, `@effect/tsgo`,
`@effect/vitest`, `@effect/platform-bun`, and `effect-solutions`; prefer the
Effect agent APIs (`effect/unstable/ai`) before inventing agent loop contracts.

## Guidelines

- Refer to the best practices recommended by the `effect-solutions` CLI when writing effectful code.
- If you need more specific information, there's a local checkout of the effect source in the reference directory.

## When to use

- Meaningful I/O is involved and the work benefits from explicit failure, dependency, resource, retry, validation, or testing boundaries.
- The code already uses Effect and you are adding or reviewing Effect code.
- You are deciding whether a TypeScript/Bun feature should use Effect.
- The task involves external APIs, databases, queues, workers, CLIs, schedules, retries, config, secrets, structured logging, runtime validation, resource cleanup, or concurrent workflows.
- You need typed domain errors rather than unstructured thrown exceptions.
- You need swappable live/test implementations through services and Layers.
- You are deploying TypeScript infrastructure or workers and need Alchemy-aware conventions.

## When NOT to use

- A small one-off script can be obvious plain TypeScript: read one file, transform pure data, write one file, no retries, no injected dependencies, no long-lived resources. As requirements grow, adopt Effect where I/O needs it and extract coherent responsibilities. A line count alone does not justify scattering the implementation; retain configured limits with documented, targeted exceptions where needed.
- Pure functions, simple data mappers, UI-local state, or tiny glue code do not need Effect wrappers.
- A project has no Effect dependency and the feature does not benefit from typed errors, Layers, resource safety, retries, or observability.
- The team only needs a tactical fix in plain async code. Do not introduce Effect as a drive-by refactor.
- You cannot explain the service/layer/error/testing shape. Stop and design that first instead of sprinkling `Effect.runPromise` calls everywhere.

## Darkmatter Conventions

- Use Bun commands: `bun install`, `bun test`, `bun run <script>`, `bunx <tool>`.
- Translate upstream `pnpm` examples mechanically. Example: `pnpm test file.test.ts` becomes `bun test file.test.ts` when the project uses Bun test, or `bun run test file.test.ts` when test is a package script.
- Prefer Bun runtime packages where relevant, such as `@effect/platform-bun` and `BunRuntime.runMain` for Bun entrypoints.
- Prefer Alchemy for deployable infrastructure. Put infra in `alchemy.run.ts`, create resources with Alchemy, bind them to workers/services, and build up an `Alchemy.Stack`. Refer to the alchemy skill if writing alchemy code or adding new infra code.
- Prefer Postgres for application data. Use Kysely + `pg` for query-heavy TypeScript adapters, or Effect SQL Postgres when persistence is exposed as Effect services and Layers. D1/sqlite are exceptions for narrow edge-local state, demos, or an explicit project decision.
- Configuration comes from named config files (`config/<name>.json`) read through `Config`. There is no selector flag: an interactive run picks from a list (`Prompt.select`), a non-interactive run reads `APP_CONFIG` or fails listing the names. Env vars and flags are per-key overrides chained with `ConfigProvider.orElse`; secrets come from the `.sops.json` sibling via `effect-sops`. Do not design the setup of a program as a list of flags or env vars. See [ADR-0014](../../docs/adr/0014-named-config-files-over-flags-and-env.md).

## Typed RPC with effect-orpc

Use `effect-orpc` when a service needs typed RPC procedures, a generated or
shared oRPC client contract, Effect service injection, and typed Effect errors.
Use raw Effect `HttpRouter` or Hono when the route is simple HTTP, a webhook,
static content, streaming/SSE, or a framework adapter where an RPC contract
would add ceremony without a client-facing type contract.

When adding `effect-orpc`, pin the Effect 4 build in the catalog:

```json
{
  "workspaces": {
    "catalog": {
      "effect-orpc": "1.0.0-effect-v4.8",
      "@orpc/server": "^1.13.0",
      "@orpc/client": "^1.13.0",
      "@orpc/contract": "^1.13.0",
      "@orpc/shared": "^1.13.0"
    }
  }
}
```

Do not install `effect-orpc@latest`; npm `latest` is the Effect 3 line
(`0.5.0`). The `effect-v4` dist-tag currently resolves to
`1.0.0-effect-v4.8`, whose peers require Effect 4
(`effect >=4.0.0-beta.98`) and the oRPC packages above.

Prefer these upstream shapes:

- Build procedures from `eos.provide(AppLayer)` or `makeEffectORPC(runtime)`.
  Use a caller-owned `ManagedRuntime` when a scoped layer should be acquired
  once and disposed during application shutdown, such as a Postgres pool,
  telemetry SDK, or shared cache.
- Write handlers and Effect middleware with `.effect(function* (...) { ... })`
  and generator `.use(function* ({ next }) { return yield* next(...) })` so
  service requirements, spans, cancellation, and errors stay in Effect.
- Model HTTP errors with `ORPCTaggedError` and pass those classes to
  `.errors(...)` / `eoc.errors(...)`; do not duplicate the same error contract
  as unrelated thrown exceptions and response schemas.
- Use `implementEffect(contract, layerOrRuntime)` when a repo is contract-first
  and already owns an oRPC contract. Contract leaves keep the declared input,
  output, and error surface while adding `.effect(...)` handlers.
- Import `effect-orpc/node` only when Node `AsyncLocalStorage` is needed to
  preserve FiberRefs across native oRPC middleware or framework boundaries.
  Use `withFiberContext(() => next())` when request-local FiberRef state is
  created outside the oRPC pipeline and must be visible inside handlers.

## Package layout reference

See [effect-package-map.md](effect-package-map.md) for domain ownership, public package entries, adapters, workflows, tests, and runtime boundaries. It describes responsibilities rather than prescribing a file for each function or Effect export.

## Upstream Reference

Use `reference/effect` or `effect-solutions` CLI when you need current Effect source or examples instead of relying on memory:
- `reference/effect/AGENTS.md` — upstream repository rules, including pnpm validation commands, generated barrels, changesets, and `it.effect` conventions.
- `reference/effect/packages/effect/` — core library source and tests.
- `reference/effect/packages/platform-bun/` and `reference/effect/packages/platform-node/` — runtime/platform examples.
- `reference/effect/packages/vitest/` — Effect-aware Vitest helpers.

If the submodule is missing in a fresh checkout, initialize it before using local references:

```bash
git submodule update --init skills/effect-typescript/reference/effect
```

For darkmatter application work, treat the submodule as read-only and translate upstream pnpm commands to the repo's package manager. For direct upstream Effect contributions, follow `reference/effect/AGENTS.md` exactly; do not apply darkmatter Bun defaults inside the upstream repo.

## JSON Encoding & Decoding

Use `Schema.fromJsonString` to parse JSON strings and validate them with your schema in one step. This combines `JSON.parse` + schema decoding in one step, and `JSON.stringify` + schema encoding for the reverse:

```typescript
import { Effect, Schema } from "effect"

const Row = Schema.Literals(["A", "B", "C", "D", "E", "F", "G", "H"])
const Column = Schema.Literals(["1", "2", "3", "4", "5", "6", "7", "8"])

class Position extends Schema.Class<Position>("Position")({
  row: Row,
  column: Column,
}) {}

class Move extends Schema.Class<Move>("Move")({
  from: Position,
  to: Position,
}) {}

// fromJsonString combines JSON.parse + schema decoding
// MoveFromJson is a schema that takes a JSON string and returns a Move
const MoveFromJson = Schema.fromJsonString(Move)

const program = Effect.gen(function* () {
  // Parse and validate JSON string in one step
  // Use MoveFromJson (not Move) to decode from JSON string
  const jsonString = '{"from":{"row":"A","column":"1"},"to":{"row":"B","column":"2"}}'
  const move = yield* Schema.decodeUnknownEffect(MoveFromJson)(jsonString)

  yield* Effect.log("Decoded move", move)

  // Encode to JSON string in one step (typed as string)
  // Use MoveFromJson (not Move) to encode to JSON string
  const json = yield* Schema.encodeEffect(MoveFromJson)(move)
  return json
})
```
