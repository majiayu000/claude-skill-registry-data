---
name: prisma-composer-core-concepts
metadata:
  library: "@prisma/composer"
  library_version: "0.20.0"
  version: 2026.9.1
description: >-
  Use when deploying or managing an app that uses Prisma Composer
  (`@prisma/composer`): wiring its services and Modules, running it locally,
  testing composed services, or standing up / tearing down an environment.
  Triggers on "prisma composer", "@prisma/composer", "prisma app", the
  `prisma-composer` CLI, `compute()`, `module()`, `contract()`,
  `service.load()`, `mockService`, `bootstrapService`.
---

# Prisma Composer core concepts

A **Prisma App** is a tree of typed declarations composed in TypeScript and
handed to the `prisma-composer` CLI. This file covers structures,
hierarchies, relationships, and workflows: the concepts you cannot observe
from the code or the CLI's help output. It is not a CLI reference; discover
any individual command and its flags with `--help`. Commands named here
belong to the `prisma-composer` CLI itself; a host CLI that embeds Composer
may not carry every verb, so confirm a command exists via `--help` rather
than inferring it. The Prisma platform moves fast, so treat this file as the
stable conceptual core and find current, fuller documentation at
<https://www.prisma.io/docs>. For working code, read `examples/` in the
prisma/composer repo.

Two principles govern everything and are binding
(`docs/design/01-principles/`):

1. **Your code never reads its environment.** Dependencies, configuration,
   credentials, and the port all arrive through the service node, typed.
   `process.env` is never the answer.
2. **Composer never bundles or transforms your code.** You build with your own
   bundler; the framework assembles the built output by deterministic steps
   and hands it to the configured deploy target.

## Declarations are data

Everything you author is a declaration: plain data describing a piece of the
app, executing nothing when imported. Three node kinds exist:

| Kind | Declared with | Purpose |
| --- | --- | --- |
| Service | `compute()` | A running unit of your code; atomic, Composer sees only its ports |
| Resource | `rawPostgres()`, `bucket()` | A stateful managed dependency |
| Module | `module()` | A grouping boundary; runs no code of its own, exposes typed ports |

Nodes connect through **ports**: `deps` declares what a node requires,
`expose` declares what it offers. Wiring happens in a Module's builder via
`provision()`, and the root Module, handed to the CLI, is the App:

```ts
// module.ts
import { module } from '@prisma/composer';

export default module('store', ({ provision }) => {
  const catalog = provision(catalogModule);
  provision(storefrontService, { deps: { catalog: catalog.rpc } });
});
```

Because ports are typed, **the compiler verifies every wire**. A dependency
wired to the wrong producer, a missing RPC handler, a literal input value of
the wrong shape: all of it fails `tsc`, not the deploy. Env-bound input is
the exception: those values exist only at deploy, so secret-binding
mismatches and missing platform variables surface as early deploy-time
refusals instead (see Two channels below). Typecheck, then build, then
deploy; don't use the cloud to find out whether the wiring is correct.

Composer itself is target-agnostic: `@prisma/composer` carries authoring,
testing, and the CLI, coupled to no platform. A deploy target is an extension
registered in the deploy config; `@prisma/composer-prisma-cloud` is the
Prisma Cloud target and the one this skill's deploy sections assume. Its
root exports `compute`, `rawPostgres`, `bucket`, `envSecret`, and
`envParam`; the ORM vocabulary (`postgres`, `dataContract`) lives under the
`/orm` subpath, alongside the shared `/cron`, `/storage`, `/streams`,
`/auth`, and `/email` modules. These are the only two Composer packages a
basic Prisma Cloud app needs, and nothing installs them for you: a fresh
project starts with neither, so add both as dependencies first. An
extension adds its own `prisma-composer-*` package alongside them. Compose
an existing Module before implementing a capability yourself; wiring one in
is a couple of lines.

Within the entry graph (everything reachable from `module.ts`), write
relative imports with explicit `.ts` extensions (`./service.ts`, with
`allowImportingTsExtensions` in tsconfig): that form resolves everywhere.
The `prisma-composer` CLI also maps `./service.js` and extensionless
`./service` to the `.ts` source, but other hosts may not.

## The service node is the only doorway

Your runtime code receives everything from the service declaration it
imports:

1. `service.load()`: dependencies (typed RPC clients, database bindings).
2. `service.input()`: the whole input as one schema-validated object;
   credentials in it are redacting `SecretString` boxes.
3. `service.port()`: the reserved port to bind (default 3000).

A service declaration is pure data; the server entry is what your build
produces and the platform boots:

```ts
// service.ts
export default compute({
  name: 'auth',
  deps: { db: rawPostgres() },
  build: node({ module: import.meta.url, entry: '../dist/server.mjs' }),
  expose: { rpc: authContract },
});

// server.ts
const { db } = service.load(); // { url }: you construct your own client
const handler = serve(service, {
  rpc: { verify: async ({ token }) => ({ ok: token.length > 0 }) },
});
Bun.serve({ port: service.port(), hostname: '0.0.0.0', fetch: handler });
```

The consumer declares `deps: { auth: rpc(authContract) }` and gets a typed
client back from `load()`.

## Two channels: dependencies and input

| The value is… | Declare | Provide | Read |
| --- | --- | --- | --- |
| produced by another node | `deps: { db: rawPostgres() }` | wire at `provision()` | `load()` |
| anything else (config or credential) | one field of the `input` schema | bind at `provision()`: literal, `envParam()`, or `envSecret()` | `input()` |

The service declares its whole incoming configuration, plain values and
credentials together, as **one [Standard Schema](https://standardschema.dev)**
(arktype is the house choice). A credential is a field typed as
`secretString()` from `@prisma/composer/arktype`; conditional legality ("no
stripe key unless billing is on") is an ordinary schema union. The binding at
`provision()` mirrors the schema's shape; `envSecret('NAME')` names the
platform variable and never carries the value.

Rules that bite:

1. **Secretness is enforced by validation.** A literal bound where the schema
   expects `SecretString` fails the deploy; `envSecret` bound to a plain
   string field fails the same way.
2. **`envParam` values arrive as raw strings**; bind them to string fields.
   The stage's platform variable is the store; the deploying shell only seeds
   a missing name (and the deploy fails early, naming the variable, when both
   lack it). Changing the platform value needs a redeploy.
3. **Absence is the schema's call.** An env-bound field whose variable is
   unset or empty resolves to *key omitted*, which is legal only if the
   schema allows it (optional field, union arm). The deploy report prints the
   serialized input document (secrets ride as `{"$secret":"VAR"}` pointers)
   and every key that resolved absent.
4. **The reserved `port` is outside the schema.** Read it through
   `service.port()`, never `process.env`. The framework also exports `PORT`
   for Next.js standalone, which binds it itself.
5. **A Module forwards a secret need without learning the platform name.**
   Declare `secrets: { signingKey: secret() }` on the Module boundary and
   pass the forwarded ref as a binding leaf; the parent binds the real
   source.
6. `input.apiKey.expose()` is the only way to a secret's value; the box
   redacts everywhere else (logs, JSON, errors).

## Contracts and RPC

A contract is the typed interface through which services communicate. It
lives with the service that owns it, typed by any Standard Schema validator,
and both provider (`serve()`, exhaustive over the contract's methods at
compile time) and consumer (`rpc(contract)`) reference the same value. Calls
travel as RPC over HTTP. Two behaviours are provisioned for you and must not
be reimplemented:

1. **Service keys.** At deploy, Composer mints a distinct unguessable key per
   consumer→provider binding; `serve()` returns `401` to anything else before
   the handler runs. Nothing in your code declares it. Consequences: don't
   build your own service-to-service auth, and don't `curl` a deployed
   `/rpc/<method>` to check it works. An unwired caller always gets `401`,
   which looks like a broken deploy and isn't. Debug through a consumer, or
   locally, where nothing is enforced. Keys are per binding (one leaking
   can't impersonate another consumer), service-scoped (any valid key
   reaches every method; split services to gate separately), rotated only by
   removing the binding or destroying the stack and redeploying, and stored
   in deploy-owned `COMPOSER_*` variables you never hand-edit.
2. **Idempotency and retries.** Every generated-client call carries an
   `Idempotency-Key`; dropped calls retry with backoff, and `serve()` runs
   one call per key, replaying the completed answer to late retries. Every
   method is therefore safely retryable and no contract declares anything
   about it (there is no "is this idempotent" flag; don't invent one). A
   handler may take an optional third argument `(input, deps, ctx)` and read
   `ctx.idempotencyKey` (`string | undefined`) if it needs exactly-once
   beyond one instance's memory; most don't. Locally and in tests nothing is
   provisioned, so `serve()` passes every call through: never supply a key
   in test inputs.

## Builds are yours

You build, the framework assembles. For a plain server process, `entry` must
point at a single self-contained ESM file: everything inlined except runtime
built-ins (`bun`, `bun:*`, `node:*`). Deploy copies that one file and never
ships `node_modules`, so anything left un-inlined fails at boot, not at
deploy. Rules that bite:

1. **Two services in one package means two separate builds**, one per entry.
   A single multi-entry build splits shared code into a chunk neither output
   contains.
2. **A directory build uses `dir` + `entry`** (`dir` relative to the service
   module, `entry` a file inside `dir`; `../` is an error). The tree is
   copied verbatim, so the server must resolve siblings against
   `import.meta.url`, not the working directory. The tree must contain no
   symlinks: the packager rejects them, names the link, and assembly fails.
3. **Next.js**: `next build` with `output: 'standalone'` is the whole build;
   `nextjs({ module, appDir })` names the app root. Any page or action that
   calls `load()` needs `export const dynamic = 'force-dynamic'`, because
   the runtime environment doesn't exist at build time and Next ignores
   runtime env for prerendered routes.
4. **Always build before `deploy` or `dev`.** Neither builds for you.

Deploy configuration lives in `prisma-composer.config.ts` (or `.mts`, `.mjs`,
`.js`; nearest ancestor of the entry wins, `.ts` first within a directory).
It registers extensions (`prismaCloud()`, `nodeBuild()`, `nextjsBuild()` when
the app has a Next.js service) and the deploy-state backend
(`prismaState()`). It is read by the CLI's operations (deploy, destroy, and
dev; a `dev` run without one refuses, naming the missing file) and never
imported by app code.

## Databases and migrations

Two kinds of Postgres dependency:

1. **`rawPostgres()`**: the binding is `{ url }` and the app owns its client.
2. **`postgres(...)`**: a Prisma-ORM-typed database. The binding is
   `{ url, client }` (ADR-0040): the raw connection URL plus the typed
   client Composer constructs from your data contract, lazily on first
   access, so queries go through `binding.client` and are compile-time
   checked. Both `postgres` and `dataContract` import from
   `@prisma/composer-prisma-cloud/orm`, not the package root. One
   `dataContract`-wrapped value (emitted from `contract.prisma` by
   `prisma contract emit`) is referenced by both the dependency end
   (`deps: { db: postgres(catalogData) }`) and the resource end, which also
   names the `prisma.config.ts` path so the deploy's migration step can
   reload the emitted `contract.json` and find `migrations/`.

**Deploys are replay-only**: they apply the migrations committed under
`migrations/` and never create schema themselves. Every schema change,
including the first schema of a new database, follows one loop:

1. Edit `contract.prisma`.
2. `prisma contract emit` regenerates `contract.json` + `contract.d.ts`.
3. `prisma migration plan --name <slug>` authors the migration (on an empty
   graph this authors the baseline).
4. Commit `migrations/` with the change, then deploy. A fresh database
   replays the whole path from empty.

If no authored path reaches the target contract, deploy (and `dev` against a
stale local database) refuses with `MIGRATION_PATH_NOT_FOUND`; its message
lists the two ways out: author the missing migration, or, when iterating
against a local
database only, `prisma db update`. The tracked migration resource persists only
compact contract identity in deploy state; if the emitted contract artifact
named by `prisma.config.ts` is missing, unreadable, or no longer matches the
declared `dataContract(...)` value, deploy fails before touching the database.
Never skip step 3 before a deploy. See `examples/store/modules/catalog` for the
complete pattern.

## Deploy model: converge, don't script

Deploy compares the declared topology against recorded deploy state and
applies only the difference. Re-deploying with nothing changed is a no-op;
removing a node removes its deployed resource. The Prisma Cloud target
requires exactly two environment variables: `PRISMA_SERVICE_TOKEN` and
`PRISMA_WORKSPACE_ID`. There is no interactive login.

**Stages.** A stage is an environment name chosen on the command line at
deploy time, never written in the topology. The identical graph deploys
everywhere. On the Prisma Cloud target, a Prisma App is one Project and a
stage is a Branch of it, with its own running services, its own empty
database, its own configuration. A stage name must be a valid git ref name;
an invalid name is a hard error.

**Destroy** always requires an explicit target: a bare destroy is an error,
and naming a stage and production together is too. Destroying a stage
deletes its Branch after removing its resources. Destroying production
removes only the resources inside the production Branch, never the Branch
itself directly; once the Project is empty it is deleted too, and that
deletion takes the production Branch with it. A Project still holding
another stage's resources is kept. Destroy never creates anything:
destroying a
never-deployed stage fails rather than standing one up.

**The engine underneath is alchemy.** Convergence is executed by
[alchemy](https://alchemy.run), a third-party infrastructure-as-code engine
that arrives as an ordinary, exactly-pinned npm dependency of
`@prisma/composer` (2.0.0-beta.74 at this library version). Your code never
imports or configures it; consult alchemy's own docs for the engine itself.
What matters operationally:

Alchemy is resolved from the nearest `node_modules/.bin`, including hoisted
ancestor directories. Windows resolves `alchemy.exe`, then `alchemy.cmd`,
then the extensionless shim; POSIX resolves `alchemy`. No global Alchemy
installation is needed.

1. Deploy and destroy write the pipeline's results to a generated, gitignored
   stack file at `.prisma-composer/alchemy.run.ts`, then run the alchemy CLI
   against it as a child process; `dev` does the same at
   `.prisma-composer/dev/alchemy.run.ts` with local providers. The file
   carries the computed values as literals but reads credentials via
   `fromEnv()`, so nothing sensitive lands on disk, and it is regenerated
   every run: output, not configuration, never edited.
2. Failures are bisectable through that file. A failing deploy names its
   path; running `alchemy deploy .prisma-composer/alchemy.run.ts` directly
   separates "the framework computed the wrong thing" from "the engine or
   platform rejected the right thing". An engine failure surfaces as
   `DEPLOY.ENGINE_FAILED` carrying the exit code and that reproduce command;
   the child's live output streams to the terminal either way.
3. Destroy evaluates the same stack program as deploy, and evaluating it
   packages the assembled bundles, so **an app must be built before it can
   be torn down**.
4. alchemy is why the `effect` pin exists: it resolves the `effect`
   constellation, and a hoisted newer `effect` halts every command (failure
   mode 1 below).

**The deploy report** ends with the app's own topology: authored names, the
platform resource each became, and public URLs. Read ids out of it rather
than hunting in the Console. A URL appears only where the address is
genuinely public: a service prints one, a database never does, and a
node whose product is secret material reports no resource line at all.

**Connection contract refusals.** A connection declares the values it needs
by name; a producer that omits one fails the deploy, naming the edge, the
param, and what the producer did supply:

```text
Connection input "auth.db" declares param "url", but its producer "db" did not
supply it — the producer's outputs carry [host].
```

This is a deploy-time refusal, not a broken deploy, and it can appear on an
app whose code didn't change (the gap used to pass silently as `undefined`
and crash the consumer at boot). Fix whichever end is wrong; don't mark the
param `optional` unless absent really is legal. Only reachable if you
authored the connection or an extension on one side.

**Driving deploys from code.** `@prisma/composer/control` exposes typed
`deploy`, `destroy`, `dev`, and `log` returning structured results. Failures
come back as `{ ok: false, failure }` with a dotted `failure.code` from a
closed registry (e.g. `ASSEMBLE.BUILD_FAILED`, `DEPLOY.ENGINE_FAILED`,
`DEPS.EFFECT_VERSION_CONFLICT`); branch on the code, not the message. A
non-structured rejection out of an operation is a bug in composer, not an
expected failure.

## Local development

The `dev` command runs the whole app on this machine, wired as it deploys,
against local emulators. No cloud credentials are needed or read. Concepts
that surprise:

1. It runs the same pipeline as deploy, so **build first**, exactly like
   deploy. It watches built output and restarts a service when its build
   changes.
2. Ctrl-C stops the app's processes but leaves local databases, buckets, and
   their data up: the next `dev` is a warm start. Starting clean, wiping
   this app's local instances and data first, is an explicit opt-in flag.
3. `dev` does not print service logs; `log` is a separate, read-only command
   that follows the already-running app's merged logs. It never builds,
   provisions, starts, or stops anything.
4. An unset secret doesn't block a local run: it becomes a placeholder plus a
   warning, and only the code path that spends it fails, at the external
   service it calls.
5. Windows isn't supported yet.

## Testing is an environment seam

A test is just another environment: one where you decide what `load()` and
`input()` return, never by editing the code under test.

| You want to… | Use | From |
| --- | --- | --- |
| Test a page / action / handler in isolation | `mockService` | `@prisma/composer/testing` |
| Run the real boot + request path against a fake dependency | `bootstrapService` | `@prisma/composer-prisma-cloud/testing` |

`mockService` returns a copy of the service whose `load()` yields your
doubles (type-checked against the declared deps) and whose `input()` yields
the object passed under the reserved `input` key (required exactly when the
service declares an input schema; handed over as-is, not validated). Wiring
the module substitution is your runner's job (`vi.mock` in Vitest,
`mock.module` in bun test).

`bootstrapService` boots the service's real built entry in-process against a
config you choose; drive it over real HTTP. Gotchas:

1. `service.port` must be concrete: the entry self-listens, and no
   OS-assigned port is reported back.
2. There is no `close()`; run each integration-test file in its own process
   (bun test does).
3. Next.js services take a third argument, a boot thunk, resolved with
   `standaloneServerPath` from `@prisma/composer/nextjs/control`.
4. A service with an input schema takes `input` in the config, a binding
   exactly like `provision()`'s, run through the real serialize/read path.

A dependency's type is its contract, so any value of that shape is a valid
double: a bare object, the real client over an in-memory handler, or a real
local server. Ship a dependency's fake from its own package as a `/fake`
entry point, outside `src/`, so the fake and the real service share one
contract.

## Building blocks and extensions

First-party Modules ship inside `@prisma/composer-prisma-cloud` and
provision exactly like your own:

| Import | What it provisions | Exposes |
| --- | --- | --- |
| `cron` from `/cron` | An always-on scheduler (it holds Compute's keep-awake guard) firing your schedule at your runner service; `input` on `cron()` binds the runner's input schema | nothing |
| `storage` from `/storage` | An S3-backed blob store (own Postgres + minted credentials) | `store` |
| `streams` from `/streams` | Durable append-only event streams over a `store` | `streams` |
| `auth` from `/auth` | Signup, login, sessions, and JWT verification (Better Auth in one service, own database) | `api`, `session`, `admin` |
| `email` from `/email` | Transactional email with a stored outbox (own service and database) | `send`, `outbox` |

`bucket()` (imported alongside `rawPostgres`) is a raw S3-compatible bucket:
the dependency end receives `{ url, bucket, accessKeyId, secretAccessKey }`,
shape-compatible with `/storage`'s `s3()` dependency, so a service wired to
`s3()` can be rewired to a `bucket` resource unchanged.

An extension (a package bringing its own Modules, resources, or deploy
target) is published on npm as `prisma-composer-*`. The ecosystem is new:
today the blocks above plus your own Modules are the whole set, so verify a
`prisma-composer-*` package exists on npm before reaching for it.

## Failure modes quick reference

1. **Every `prisma-composer` command halts at start-up on an `effect`
   version conflict** (`Dependency conflict: alchemy resolves effect@...`).
   The app, or one of its dependencies, pins a different `effect` and the
   package manager hoisted it over Composer's pin. Match the app's own
   `effect` to `@prisma/composer`'s exact pin, or force it with
   `"overrides": { "effect": "<pin>" }` in the app's `package.json` (yarn:
   `resolutions`; pnpm: `pnpm.overrides`), then reinstall. A plain Composer
   app never hits this: the public packages pin every `effect`-family
   package alchemy would float.
2. **A deployed `/rpc/<method>` returns `401` to anything but a wired
   peer.** Not a broken deploy; see Contracts above.
3. **Scale-to-zero closes idle database connections.** A persistent client
   crashes into a 502 restart loop unless the pool is small and
   reconnect-friendly (`new SQL({ url, max: 1, idleTimeout: 10 })` for Bun)
   and the process logs `uncaughtException`/`unhandledRejection` instead of
   dying. Under `dev` watch-restarts against the local emulator, add
   `prepare: false` as well: restarted processes collide on
   prepared-statement names in the emulator's shared session.
4. **Cold starts reset service-to-service connections.** A call into a
   scaled-to-zero service can get `ECONNRESET`; retry it.
5. **Bind `0.0.0.0`, not loopback.** The platform routes external HTTP to
   the VM; a loopback-only listener is unreachable.
6. **The ingress buffers streaming responses.** An open SSE tail delivers
   nothing and times out at 60s; don't build on streamed HTTP responses.
7. **Naming rules fail at load, not typecheck.** Provision ids and declared
   node names must be ASCII letters and digits only (`[A-Za-z0-9]`): they
   derive config keys and address segments, so a hyphenated name like
   `my-db` passes `tsc` and then fails the load. The root module's name is
   exempt. A provision id shorter than 3 characters is rejected by the
   platform (name the database `'database'`, not `'db'`), and a service
   whose name equals its enclosing Module's reads as `auth.auth` unless
   given an explicit `id`.
8. **`MIGRATION_PATH_NOT_FOUND`**: see Databases above; author the missing
   migration, don't skip the plan step.
9. **Date/time columns hand back `Temporal.*` values on read.** Bun and
   stock Node ship no global `Temporal`, so a service with `DateTime`
   contract columns compiles and deploys, then fails on the first timestamp
   read. Provide the global at the server entry
   (`import 'temporal-polyfill/global'`) or use string column types.

## What Composer doesn't do yet

Name the gap instead of inventing an API:

1. **No interactive auth in the `prisma-composer` CLI.** Its deploys
   authenticate only via a static
   `PRISMA_SERVICE_TOKEN`; there is no `login` flow.
2. **No in-memory contract bindings.** A dependency can't yet be wired to a
   co-located handler without HTTP; use `bootstrapService` with a loopback
   fake.
3. **RPC over HTTP is the only contract kind.** No gRPC, WebSocket, or
   streaming contracts.

For anything else missing, check `examples/`, `docs/design/10-domains/`, and
`docs/design/90-decisions/` in the prisma/composer repo, then file an issue
there rather than guessing.
