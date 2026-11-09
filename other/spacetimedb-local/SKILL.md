---
name: spacetimedb-local
description: Use when running a SpacetimeDB module locally.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
    hermes:
        tags: [spacetimedb, database, typescript, reducers, local-first, projection]
---

# SpacetimeDB Local Module

SpacetimeDB runs the schema _and_ the application logic (reducers) inside the database process, so a
write is queryable the moment it commits instead of after a refresh. This skill is the install →
init → schema → build → publish → verify path, plus the four traps that cost real time on the first
attempt.

## When to Use

- A project needs a local, live view of data that a file store already holds.
- Someone asks for event-driven tables, subscriptions or in-database logic on their own machine.
- A published module answers `failed to find database <name>-<suffix>`.

## Procedure

1. **Install the release binary, not the formula.** The Homebrew tap (`clockworklabs/tap`) can pin a
   version whose GitHub asset no longer exists, which fails as `curl: (22) … 404`; and
   `https://spacetimedb.com/install` serves the marketing page, so piping it to `sh` installs
   nothing.

    ```sh
    curl -sSL -o /tmp/spacetime.tar.gz \
      https://github.com/clockworklabs/SpacetimeDB/releases/download/<tag>/spacetime-aarch64-apple-darwin.tar.gz
    tar -xzf /tmp/spacetime.tar.gz -C ~/.local/bin
    chmod +x ~/.local/bin/spacetimedb-cli ~/.local/bin/spacetimedb-standalone
    ln -sf spacetimedb-cli ~/.local/bin/spacetime
    ```

    The tarball ships `spacetimedb-cli` and `spacetimedb-standalone`; `spacetime` is only a symlink
    you create. Pick the tag from
    `curl -s https://api.github.com/repos/clockworklabs/SpacetimeDB/releases/latest` and confirm
    with `spacetime --version`.

2. **Start the server on an explicit loopback address.** `spacetime start` defaults to port 3000 and
   prompts interactively when it is busy (an editor or dev server usually holds it), which reads as
   a hang.

    ```sh
    spacetime start --listen-addr 127.0.0.1:3010
    ```

    Bind loopback only: the module has no auth beyond the server's own identity handling. Verify
    with `lsof -nP -iTCP:3010 -sTCP:LISTEN`.

3. **Init the module inside the project, not beside it.**
   `spacetime init <name> --lang typescript --project-path <dir> --non-interactive --local` writes
   `spacetime.json` (module path) and `spacetime.local.json` (database name), then install the
   module's own deps in `<dir>/spacetimedb`.
4. **Write the schema, then let `build` be the typecheck.** `spacetime build` compiles the
   TypeScript module and reports schema errors; there is no separate `tsc` step to trust.
5. **Publish, then prove a write.**

    ```sh
    spacetime publish <db> --server http://127.0.0.1:<port> --module-path <dir> --yes
    spacetime call <db> <reducer> --server http://127.0.0.1:<port> <args…>
    spacetime sql <db> --server http://127.0.0.1:<port> "select … from <table>" --format json
    ```

    `--format json` is the machine-readable form; the default prints a padded table whose borders
    break naive parsing.

6. **Prove idempotency, not just success.** Call the same reducer twice with identical arguments and
   assert the row count did not move. Content-derived primary keys are what make that true (see
   below).

## Query and browse

There is no built-in web console - `curl http://127.0.0.1:<port>/` answers 404 - so the CLI is the
browser. Reach for `describe` before writing any query.

| Task                   | Command                                                                    |
| ---------------------- | -------------------------------------------------------------------------- |
| Schema, types, indexes | `spacetime describe <db> --server <URL>`                                   |
| One-shot query         | `spacetime sql <db> --server <URL> "select * from <table>"`                |
| Machine-readable rows  | the same plus `--format json`                                              |
| Interactive prompt     | `spacetime sql <db> --server <URL> --interactive`                          |
| Live tail              | `spacetime subscribe <db> --server <URL> "select * from <table>"`          |
| Typed client           | `spacetime generate --lang typescript --module-path <dir> --out-dir <dir>` |

Four limits of the query surface read as failures, not as syntax you can fix:

- **No `GROUP BY`.** `select visibility, count(*) … group by visibility` answers `400 Bad Request`.
  `count(*)` on its own works; every breakdown is a client-side count over
  `select <column> from <table>`.
- **A subscription takes a table, not a projection.** `select id, author from post` is rejected with
  `Column projections are not supported in subscriptions; Subscriptions must return a table type` -
  subscribe to `select * from <table>` and filter in the client.
- **Columns are snake_case at the SQL surface.** A module declares `firstSeenAt` and `postCount`,
  but `describe` and `sql` expose `first_seen_at` and `post_count`; the camelCase spelling fails as
  an unknown column, which reads like a missing field rather than a naming convention.
- **`--no-config` decides how the positionals are read.** In a module directory holding
  `spacetime.json` and `spacetime.local.json` the CLI merges the configured database into the
  argument list, so every positional shifts one slot:
  `spacetime describe --server <URL> <db> tables belief` answers
  `Error: Invalid describe arguments.`, `spacetime describe --server <URL> <db>` answers
  `Error: Invalid entity_type '<db>'. Expected one of: env, procedures, reducers, routes, tables, types, views.`,
  and `spacetime sql --server <URL> <db> "select id from capability"` answers
  `sql parser error: Expected an SQL statement, found: t at Line: 1, Column 1` because the database
  name is read as the statement. Pass `--no-config` to every `describe`, `sql` and `call` aimed at a
  throwaway database, and the arguments mean what they say.

## Reading rows from a program

The CLI is for a person. A command that needs rows talks to the same endpoint the CLI does:

```
POST <URL>/v1/database/<identity>/sql
Authorization: Bearer <token>
content-type: text/plain

SELECT * FROM post
```

The statement is the **raw body**, not JSON - posting `{"query":"…"}` answers
`sql parser error: Expected an SQL statement, found: { at Line: 1, Column 1`, which reads like a
broken query rather than a wrong envelope. The answer is a JSON **array of statement results**, one
per statement, each shaped:

```json
{
	"schema": {
		"elements": [{ "name": { "some": "first_seen_at" }, "algebraic_type": { "String": [] } }]
	},
	"rows": [["2026-11-01T22:44:56.379Z", 1, true]]
}
```

`rows` are positional and aligned to `schema.elements`, so a reader maps names to values itself and
camelCases the snake_case names back. Load every table a command needs in one `Promise.all` and
assemble the nested shapes in memory: a query per record turns one round trip into two hundred.

## Splitting the module: generated schema, hand-written reducers

A field list is derived; behaviour is not. Emitting the `table(...)` declarations into
`src/Schema.ts` and keeping the reducers in `src/index.ts` lets one declaration own the columns
while the reducers stay readable.

- The **entry file must export the schema as default**: `import { spacetimedb } from "./Schema";`
  then `export default spacetimedb;`. Lifecycle hooks and reducers are `spacetimedb.reducer(...)`
  off that value, so `ctx.db.<table>` keeps its row types without re-declaring anything.
- **Imports inside the module package carry no `.ts` extension.** The module's own `tsconfig.json`
  uses `moduleResolution: "bundler"` without `allowImportingTsExtensions`, so `from "./Schema.ts"`
  fails with
  `TS5097: An import path can only end with a '.ts' extension when 'allowImportingTsExtensions' is enabled`.
  Write `from "./Schema"` there even when the surrounding repository spells `.ts` everywhere else.
- Give each table its database name explicitly - `table({ name: "post", public: true }, {…})` - so
  the published table name is a decision rather than whatever the variable happens to be called.
- **A helper is a sibling module, not an export of the entry.** The entry file's named exports are
  reserved for values registered with SpacetimeDB - reducers, lifecycle hooks, views - so an
  ordinary function exported from there is at best ignored and at worst read as a module export. Put
  the helper in `src/<Name>.ts`, import it with the same extensionless spelling
  (`from "./Catalog"`), and the bundler resolves it exactly as it resolves `./Schema`.
- **`spacetime build` typechecks every file the package `tsconfig.json` includes** (`./**/*`), not
  only what the entry reaches. A probe placed in the package is typechecked with the module, which
  is what catches the probe's own mistakes - `ctx.db.<table>.id.find` answers `Row | null`, and
  spreading it without a null check fails the build. The price is that
  `import { test } from "node:test"` reports `TS2591: Cannot find name 'node:test'`, because the
  module carries no `@types/node`; put a `// @ts-expect-error` directive above each `node:` import.
  An `exclude` for the probe directory in the module tsconfig also makes the build green, and gives
  the typecheck up: prefer the directives.

## Running the module's own code under node

`spacetimedb/server` and `spacetimedb/server/test-utils` import `spacetime:sys@2.x`, virtual modules
the host injects and node cannot resolve, so importing the module's sources directly fails with
`ERR_UNSUPPORTED_ESM_URL_SCHEME: Received protocol 'spacetime:'`. A resolve hook that points every
`spacetime:sys@*` specifier at a stub module, and appends `.ts` to an extensionless relative
specifier, is enough to load both the module and the SDK's test harness under plain node. Write that
hook once, beside the probe, and run the probe through it:

```sh
node --import ./Register.mjs <probe>.ts
```

Nothing in the tree runs such a file, so it is a probe rather than a gate: it is hand-run, and a
regression in the module passes review unless someone runs it. Two states read as green and are not:

- **No install.** The module is deliberately not a member of `pnpm-workspace.yaml`, so neither the
  root `pnpm install` nor `pnpm --filter` reaches it. A plain `pnpm install` run inside the module
  directory is worse than nothing - it resolves the root workspace, installs there, and exits 0 with
  the module still uninstalled. The remedy is
  `cd Maintain/Spacetime/spacetimedb && pnpm install --ignore-workspace`.
- **No test file.** `node --test` on an empty match exits 0, so a renamed or deleted file passes
  silently. Read the runner's reported test count before reading its exit code.

`createModuleTestHarness(schema, {})` then gives a real reducer context:
`withReducerTx(auth, ctx => …)` runs one transaction and rolls it back when the body throws,
`harness.clock.set(...)` moves the clock, and `ctx.timestamp.toISOString()` carries microseconds.

Traps in that harness:

- **The clock starts at the Unix epoch.** A fixture dated 2026 is never expired by a test that
  advances a few minutes, so a liveness check silently passes for the wrong reason. Pin the base
  timestamp first (`Timestamp.fromDate(new Date(...))` plus an offset) and assert the context's own
  `toISOString()` once.
- **The harness does not run `init`.** A fresh `createModuleTestHarness(...)` datastore holds zero
  rows in every table `init` seeds - the `capability` declarations among them - so a test that binds
  against the deployment's own list is refused by an empty catalog and looks like a broken reducer.
  Seed the rows a case needs through `withReducerTx` (`ctx.db.capability.insert(...)`), and keep
  fixture ids rather than the deployed ones: a case about an id that is _not_ declared must not
  start passing the day someone declares it.
- **Reading `harness.db` inside an open transaction traps the wasm backend** with `unreachable`.
  Read through `ctx.db` inside the transaction and through `harness.db` after it returns.
- **`JSON.stringify` cannot carry a `bigint` column**, so "the table is byte-for-byte unchanged"
  needs a snapshot that maps `fence` through `String(...)` first.
- **`console.log` is swallowed once the module is imported.** `spacetimedb/server` installs its own
  console (`node_modules/spacetimedb/src/server/polyfills.ts` does `globalThis.console = console`),
  and every method on it writes through `spacetime:sys`, which the hook's stub module answers with a
  recording no-op. A case that logs its evidence with `console.log` prints nothing and looks like
  one that never ran. Use `t.diagnostic(...)` for text the runner reports, or `process.stdout.write`
  for text a script reads back.
- **The harness freezes its `DbView`, so a Proxy cannot inject a fault.** V8 refuses a `get` trap
  that answers a frozen, non-configurable data property with anything but the real value:
  `'get' on proxy: property 'belief' is a read-only and non-configurable data property on the proxy target but the proxy did not return its actual value`.
  That TypeError arrives inside the transaction, where `withReducerTx` rolls back and rethrows it,
  so a test asserting only `assert.throws(…)` passes for the wrong reason - it caught the invariant,
  not the injected fault. Build the faulted context one layer at a time with
  `Object.create(<real accessor>, { <member>: { value: … } })`, and count the writes the reducer
  attempted (`deletes`, `inserts`) so a reducer that returns early cannot make the test vacuous.
- **A rolled-back write looks exactly like a write that never happened.** `withReducerTx` aborts a
  throwing call, so "the table is byte-for-byte unchanged after a refusal" is true even when the
  reducer wrote first and refused second - a before/after snapshot cannot show that validation
  preceded the write, and a mutation that moves the guard below the insert leaves every such test
  green. Count the writes instead, by spreading a context whose one table overrides `insert`
  (spread, not a Proxy - see above): assert `0` on the refused call **and** `1` on the accepted one,
  because a counter that never observes anything reports zero for every input and proves the same
  thing as a broken one.
- **A green probe is not evidence until a guard has been broken.** Copy the package to a scratch
  directory (`node_modules` symlinked, so the bare `spacetimedb` specifier still resolves), negate
  one guard in the copy, and require the run to fail on exactly the case that names that rule: a
  mutation caught by an unrelated case proves nothing, and one caught by nothing means the assertion
  describes the code rather than testing it.

## A deadline is text, and the text has a ceiling

Every deadline column in this module is a `t.string()`, written as `ctx.timestamp.toISOString()` -
microseconds, a `Z`, a four-digit year. Three facts about that format decide what a reducer may
write:

- **Past year 9999 the renderer switches format instead of failing.**
  `new Timestamp(253_402_300_799_999_999n + 1n).toISOString()` answers
  `"+010000-01-01T00:00:00.000000Z"`, which nothing that expects four digits reads back. A row
  holding one is unreadable, and it also sorts _before_ every current stamp (`+` is below `2`), so
  `expiresAt > now` calls that grant already expired: the claim that wrote it granted nothing, the
  resource looks free, and a second claim takes it at once. Bound a computed deadline at
  `STAMP_CEILING` (`src/Catalog.ts`) and refuse past it.
- **`Number.MAX_SAFE_INTEGER * 1000` is not that bound.**
  `new Timestamp(9_007_199_254_740_991_999n)` throws `RangeError: Invalid time value`, while a
  smaller value still renders the extended format; a guard written against `MAX_SAFE_INTEGER` lets
  both through. Check the stamp ceiling.
- **A negative instant does not render as one.** `new Timestamp(-1n).toISOString()` answers
  `"1970-01-01T00:00:00.000001Z"` - a microsecond _after_ the epoch - so arithmetic that can go
  negative is refused, never rendered.

`Date` is the wrong parser in both directions: it carries milliseconds, so `new Date(text)` drops
the three digits that separate two deadlines inside one millisecond, and `Date.UTC` rolls
`2026-02-30` into March rather than rejecting it. Parse the fields, compare them back, and re-render
through `Timestamp` (`microsOf` / `stampOf` in `src/Catalog.ts`).

## Schema rules that keep it replayable

- **Derived ids, never auto-increment.** `.autoInc()` in the TypeScript schema API still requires
  the `id` field on `insert`, so an auto-inc column does not save you a key. Build the key from the
  content instead - `<postId>:<source>:<at>`, `<at>:<kind>:<subject>` - and look the row up by key
  before inserting. A replay then writes nothing rather than duplicating history.
- **Append-only stays append-only.** Update the mutable entity (a post's metrics) in place; append
  an observation row for every scrape that saw it.
- **Keep one gate field.** A `visibility` (`shadow | public | hidden`) is the only thing that
  decides what a downstream exporter may publish.
- **Opaque payloads beat migrations.** Store event payloads as a JSON string so a new event shape
  needs no schema change.

## The module is a projection, never the source of truth

Keep the files (or the existing store) authoritative and treat the database as rebuildable. An
exporter reads the database and writes the same files a static site already consumes - the site
build must never connect to the database, or a static/CI build acquires a live service dependency.

## A refusal is a read

A reducer returns nothing, so its error message is the only channel it has - and the caller reading
it was refused, which means it is by definition not entitled to what it was refused for. Two
refusals in this module named a value out of a private table before anyone noticed:

- `reveal` answered `admission-refused: <audience> holds no live lease on catalog:latency`, naming
  `property.resource` - a column of a private table, and the one value `claim` needs to make itself
  entitled. It now names the property and not the resource.
- `claim` answered `lease-held: <resource> is held by <holder hex> under fence 1 until <stamp>`,
  naming `lease.holder` - another sender's identity, from a private table. It now says
  `held by another identity` and keeps the fence and the deadline.

The rule the two instances give: name the fact the caller must act on - the property, the fence, the
deadline - and never the value it would have to read a private table to learn. Keep the diagnostic
while dropping the identity; a refusal that says only "denied" makes the caller guess what to do
next, which is its own defect.

## Pitfalls

- **`failed to find database <name>-<suffix>` is a config mismatch, not a missing database.**
  `spacetime init` writes a generated name into `spacetime.local.json` that does not match what
  `publish` created; every `sql` and `call` then resolves the wrong name. Fix the file to the
  published name, and confirm the truth with `spacetime list --server <URL>`.
- **An option-typed reducer argument is a sum type, in both directions.** A bare string for a
  `t.string().optional()` parameter fails with `invalid type: string …, expected sum type`, and
  `null` is accepted but means _none_ - so a value sent as `null` succeeds with the field silently
  dropped. The wire shape is `{"some":"<value>"}` for a value and `null` for none; check the
  parameter index the error names.
- **A reducer's argument list is positional on the CLI, optional arguments included.** Omitting an
  optional one fails with `invalid length <n>, expected reducer args for <name> with <m> elements`,
  so it has to be passed explicitly as `null`. `spacetime describe <db> reducers --server <URL>`
  prints the wire signature with the optional argument still in place - read the arity there rather
  than from the TypeScript, where `optional()` reads like a shorter call.
- **A reducer cannot share a table's name.** A reducer named `probe` declares an argument object
  typed `Probe`, and a module holding both fails to publish with
  `name 'Probe' is used for multiple types`. `spacetime build` passes regardless, because the
  collision is in the module registry rather than the TypeScript. Name the reducer for the act
  (`reveal`, not `probe`) and prove registration with `spacetime describe <db> reducers` and
  `... views`, which is also the only check that a view's name and return type reached the engine.
- **A result's option column is a tagged pair, and the tags run the other way.** `select` returns
  `[0, "<value>"]` for a value and `[1, []]` for none. Decoding `0` as none turns every optional
  column into `null` with no error anywhere: the rows still arrive, the counts still match, and the
  only symptom is a field that quietly lost its content. Assert one known non-null value survives a
  write → read round trip before trusting a reader that maps these.
- **A program calls a reducer over HTTP, not through the CLI.** The CLI's own transport is
  `POST <URL>/v1/database/<identity>/call/<reducer>` with `Authorization: Bearer <token>` and a JSON
  **array** of positional arguments (not an object keyed by name), answering `200` with an empty
  body. The token is the `spacetimedb_token` line in `~/.config/spacetime/cli.toml`; the identity is
  `GET <URL>/v1/database/<name>` -> `database_identity.__identity__` with the `0x` prefix stripped,
  which equals the identity `spacetime list` prints. Resolve it once per run rather than hardcoding
  a hex string. A wrong argument shape answers `400 invalid arguments for reducer <name>: [<index>]`
    - the index is the whole diagnosis.
- **`spacetime sql` positional order is `[DATABASE] <QUERY>`** and the server flag is `-s/--server`;
  a name that resolves locally in one command can still resolve from `spacetime.local.json` in
  another, so read the error's database name before editing anything.
- **A projection lags its source silently.** Nothing errors when the file store gains rows the
  database has never seen: a push that ran before the last scrape leaves `select count(*)` smaller
  than the store's own count, and a push that sends only entities leaves the derived tables
  (observations, events) empty. When asked whether the data "is in the database", count both layers
  and report the difference -
  `spacetime sql <db> -s <URL> "select count(*) as n from <table>" --format json` against
  `ls <store>/<Entity> | wc -l` - instead of answering from the schema. A push command's own
  `--dry-run` count is the third number worth quoting.
- **A publish is an upload, not a migration.** Adding a column to an existing table is refused
  without a default annotation:
  `Adding a column <name> to table <table> requires a default value annotation`, then
  `Aborting because publishing would require manual migration or deletion of data and --delete-data was not specified`.
  The refusal is structural rather than a backfill question - `t.string().optional()` is refused
  exactly like `t.string()`, and a table holding zero rows is refused the same way, so an empty
  table is not a way around it. Two honest routes: `--delete-data` on a database whose rows are
  rebuildable, or `t.string().default(<value>)` when some value really is the default for rows
  written before the column existed. A default chosen only to dodge the flag writes a fact that
  never happened - a receipt stamped with a generation nobody bound - so prefer `--delete-data` and
  say so. Either way, publish to a fresh database name while iterating.
- **Do not run the server as a long foreground command.** It never exits; start it in the background
  and health-check with `lsof` or a `spacetime list` call.

## Claim → test

| Claim                                      | Test                                                                                                                                                                          |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CLI installed                              | `spacetime --version` prints the release tag                                                                                                                                  |
| Server up                                  | `lsof -nP -iTCP:<port> -sTCP:LISTEN` shows `spacetime`                                                                                                                        |
| Module compiles                            | `spacetime build` → `Build finished successfully.`                                                                                                                            |
| Database published                         | `spacetime list --server http://127.0.0.1:<port>` shows the name                                                                                                              |
| Reducer writes                             | `spacetime call …` then `spacetime sql … "select count(*) from <table>"`                                                                                                      |
| Replay is idempotent                       | a second identical `call` leaves `count(*)` unchanged                                                                                                                         |
| Optional argument round-trips              | send `{"some":"<value>"}` for the optional argument, then `select <column> from <table>` shows the value rather than `(none = ())`                                            |
| Config matches reality                     | the name in `spacetime.local.json` equals the row in `spacetime list`                                                                                                         |
| Schema is discoverable                     | `spacetime describe <db> --server <URL>` lists tables, columns and indexes                                                                                                    |
| Aggregation is client-side                 | `select count(*) from <table> --format json` works; the same query with `group by` returns 400                                                                                |
| A program reads rows                       | `POST <URL>/v1/database/<identity>/sql` with a raw `SELECT` body returns `[{schema, rows}]`                                                                                   |
| An optional column survives                | write `{"some":"<value>"}`, then read `[0,"<value>"]` back - `[1,[]]` means the value was lost                                                                                |
| Generated schema, hand reducers            | `spacetime build` passes with `src/Schema.ts` imported as `"./Schema"` (no extension)                                                                                         |
| A helper module bundles                    | a reducer that imports `from "./Catalog"` builds, and the reducer's name appears in `dist/bundle.js`                                                                          |
| A probe typechecks with the module         | `spacetime build` stays green with the probe in the tsconfig include and a `// @ts-expect-error` above each `node:` import                                                    |
| The module loads under node                | `node --import ./Register.mjs` imports `src/Schema.ts` and `createModuleTestHarness` without `ERR_UNSUPPORTED_ESM_URL_SCHEME`                                                 |
| A stale fence writes nothing               | a renewal presenting the fence a takeover superseded throws `stale-fence`, and the `lease` table is byte-for-byte unchanged                                                   |
| A derived row survives a mid-write failure | the delete and the insert of one derived row sit in one transaction: a throw after the insert, and one before it, both leave the prior row byte-identical                     |
| A refusal precedes the write               | a counted context reports 0 inserts for the refused call and 1 for the accepted one                                                                                           |
| A stamp round-trips                        | `stampOf(microsOf(s)) === s` for a `ctx.timestamp.toISOString()` value                                                                                                        |
| An added column is publishable             | publishing a module whose table gains a column over the previous database either succeeds, or fails with `requires a default value annotation` - it never drops rows silently |
| A deadline past year 9999 is refused       | a reducer given a duration that would cross `STAMP_CEILING` throws; no row holds a `+NNNNNN-…` deadline                                                                       |
| A grant is live the moment it is made      | every granted claim satisfies `state === held && expiresAt > acquiredAt` at the claim's own clock, for a one-microsecond lease and a year-long one                            |
| A refusal discloses nothing                | two identities, one resource: the `lease-held` refusal matches `/held by another identity/`, carries no 64-character hex, and still names the fence and the deadline          |
| A generation row is never rewritten        | no `src/` file calls an `update` or `delete` on `generation`, and `bind`'s single append is followed by its own `requireCoherentGeneration` re-check                          |
| A table `init` seeds starts empty in tests | a fresh harness iterates zero `capability` rows, so every case seeds the ids it needs and a bind against them appends one row                                                 |
