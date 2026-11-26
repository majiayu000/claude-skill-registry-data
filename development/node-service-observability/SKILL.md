---
name: node-service-observability
description: "Use when adding logs, traces or APM to a Node service."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [observability, logging, opentelemetry, apm, node, sveltekit]
    related_skills: [studio-workflows, kernel-ops-ship, studio-dashboard]
---

# Node service observability

Order of work is fixed: **structured logs → tracing → one real request as proof.** Each step is
useful alone, and the third is the only thing that distinguishes "configured" from "working".

## When to Use

- A service has `console.log` scattered through it and no way to answer "what failed, for which
  request, how slow".
- Wiring APM (New Relic, Datadog, Honeycomb) into an existing Node/SvelteKit app.
- Making per-operation cost, latency or status queryable instead of prose in a log file.
- An agent or SDK is already in `package.json` but nothing shows up at the vendor.

## 1. Structured logs

One JSON object per line, so a forwarder, `jq` and a terminal all read the same thing:

```js
{"ts":"…","level":"info","event":"boot.env","file":"/Users/…/.app.env","found":true,"keys":["API_KEY"]}
```

- `event` is a dotted verb naming the thing that happened (`boot.env`, `write_failed`,
  `duplicate_event`) — not a sentence. Grepping one event is then a query.
- One `LOG_LEVEL` filter; `warn`/`error` to stderr, the rest to stdout.
- **Never log a value that is a secret.** Report the key's _name_, and whether it was found. A single
  `KEY=…` line lives in the aggregator forever, and it is the log that outlives the credential.
- Telemetry never breaks work: wrap the emit in `try/catch`, log the failure, and let the request
  succeed. A request that succeeded must not 500 because the logger threw.

## 2. Tracing starts before the app, never inside it

```bash
node --import ./otel.mjs build/index.js     # not: import the SDK from app code
```

- In SvelteKit, `instrumentation.server.ts` is **not** the place to initialise an SDK: it is
  evaluated inside Vite's SSR module graph, after app modules load, and in dev it runs inside the
  dev server's own instrumentation context.
- **Do not add `@opentelemetry/api` as a direct dependency of the app.** In a pnpm workspace it
  re-resolves the framework's peer set (the SvelteKit package path gains an `_@opentelemetry+api@…`
  segment), and dev SSR then dies inside `push_element` with `Cannot read properties of null (reading
  'function')` — a crash that looks like a Svelte bug and is a dependency-graph bug. Reach the SDK's
  own copy instead:

  ```js
  const requireFromSdk = createRequire(import.meta.resolve("@opentelemetry/sdk-node"));
  const { trace } = requireFromSdk("@opentelemetry/api");
  globalThis.__tracer = trace.getTracer("service-name");
  ```

  App code uses `globalThis.__tracer` if present and no-ops if not, so dev (no SDK) and production
  (SDK preloaded) share one code path.

- **A built server does not get the bundler's dotenv handling.** The preload loads the personal env
  file and then the repo `.env` itself; otherwise the first DB or storage call fails with a path that
  "does not exist" on a server that boots fine.
- **The OTLP endpoint follows the key region**, not a guess: an `eu01…` license key exports to
  `https://otlp.eu01.nr-data.net:4318` with the key in an `api-key` header.

### Vendor agent or OTLP path

Some vendor agents patch Node internals (`diagnostics_channel`, bundled `undici`). On a modern Node +
Vite stack that can recurse and abort the process in the agent's own bootstrap, before your code
runs — a runtime mismatch, not an app bug. Boot the built server with the agent and read the first 20
lines of stderr; if it aborts, disable the vendor's internal-patching instrumentation, and if it
still aborts use the standards-based OTLP exporter instead (Node SDK + OTLP trace exporter + HTTP
instrumentation). It needs no Node patching and lands in the same place.

## 3. Put the expensive operation on a span

Attributes beat log parsing: tool, operation, model, `cost_usd`, `cost_source`, units, tokens,
latency, status, project id. One span per model call makes "spend and latency by operation" a query
instead of a grep. Cost semantics (reported vs estimated vs unpriced) belong to the ledger — see the studio ledger in studio-workflows (`studio-core/LEDGER.md`).

## 4. Prove it with one real request

```bash
node --import ./otel.mjs build/index.js &
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:PORT/
grep -oE '"event":"otel\.[a-z_]+"' /tmp/server.log | sort -u
```

- Expect the boot lines (`otel.started`, `otel.tracer_ready`), a 200, and no `"level":"error"`.
- **Know which runtime actually served the request before blaming the tracing.** A package-manager
  wrapper can spawn a different Node than the one it runs under (a second Node earlier in `PATH`),
  and a native module built for the other ABI fails at `require` time — the symptom is a 500 with a
  `NODE_MODULE_VERSION` mismatch, or a bare "directory does not exist" from the database, never a
  telemetry error. Put `process.version` in the boot log and launch with the interpreter you intend
  (`PATH=<that node>/bin:$PATH pnpm dev`); a green traceless request on the wrong runtime reads
  exactly like a broken agent.
- Say what you proved and what you did not: "exported without error" is not "visible in the vendor
  UI". Do not claim the second without looking at it.
- Dev is usually logs-only on purpose; state that when handing over, or someone concludes tracing is
  broken because `pnpm dev` shows nothing.

## 5. Performance benchmarking

See `references/perf-benchmarking.md` for the JSONL baseline pattern, p50/p95/p99 computation, and comparison over time.

## 6. Batch job step logging (JSONL)

For long-running batch jobs (sleep jobs, migrations, ETL), log each step as a JSONL line with timing:

```typescript
interface StepLog { ts: string; event: string; step?: string; duration_ms?: number; result?: any; }

private logPath: string | null = null;
private logStep(entry: Record<string, any>) {
  if (!this.logPath) return;
  const line = JSON.stringify({ ts: nowUtc(), ...entry }) + '\n';
  fs.appendFileSync(this.logPath, line);
}

// In run():
this.logStep({ event: 'job_start', job_id: jobId, trigger, started_at: startedAt });
this.logStep({ event: 'step_start', step: 'dedup', detail: 'Starting dedup sweep...' });
const start = Date.now();
steps['dedup'] = await this.dedupSweep();
this.logStep({ event: 'step_complete', step: 'dedup', duration_ms: Date.now() - start, result: steps['dedup'] });
this.logStep({ event: 'job_complete', job_id: jobId, status: 'completed', steps, metrics });
```

**Pattern:**

- Clear the log file at job start (`fs.writeFileSync(logPath, '')`)
- Each line is one JSON object with `ts`, `event`, and event-specific fields
- Events: `job_start`, `step_start`, `step_complete`, `metrics`, `job_complete`, `job_failed`
- Include `duration_ms` on step_complete for timing analysis
- On failure, log `job_failed` with the error message and partial steps
- Make logPath optional (null = no logging) so the job works without a log file

**Pitfall:** Use `fs.appendFileSync` (not async) for log writes — the job is already sequential and sync writes prevent interleaving. If the job crashes mid-step, the log will show the last completed step, making debugging straightforward.

**A JSONL step log is the right answer only while nothing queries it.** The moment a reader appears — a
dashboard panel, a totals-per-day question, a join against another table — or the lines start repeating an
entity key and "latest line wins" is implemented by reading the tail, the file has become a table you have
not migrated. Move it, keeping the payload as a JSON column so readers keep the same objects. Recipe:
`references/sqlite-journal.md`.

## 7. When the file becomes a journal

For a local service that accumulates its own history, one SQLite file queried through Kysely beats any
number of log files. Rules that decide whether it works:

- **One migration runner, recorded in the database.** Kysely's migrator over `node:sqlite`, migrations in
  TypeScript, `kysely_migration` as the ledger. Ad-hoc `CREATE TABLE IF NOT EXISTS` in modules is a second
  schema owner and drifts the moment a column changes.
- **The first migration adopts, it does not create.** `create table if not exists` plus `pragma_table_info`
  before every `alter table … add column`; verify against a copy of the real database, not only a fresh file.
- **Do not add a native SQLite binding for convenience.** better-sqlite3 and libsql need a prebuilt binary;
  a service that starts under launchd after an upgrade must not depend on one matching. Kysely exposes its
  SQLite adapter/compiler/introspector, so only the driver is yours.
- **Decide reader vs writer from `statement.columns()`, never from the SQL prefix** — otherwise
  `insert … returning` runs as a write and loses its rows.
- **Write path:** `PRAGMA busy_timeout`, `synchronous=NORMAL`, `journal_mode=WAL` on open, because several
  processes share the file. Retention and best-effort writes are design decisions, not operations: prune by
  owner, and let a locked database degrade to the text log instead of failing the work.
- **A log the service writes and never reads is the failure this section exists to prevent.** Before adding
  a new file output, ask which code will query it; if the answer is "none", it is a text log with a schema
  nobody can enforce.

## Pitfalls

- **A tracer that throws must not take the request with it.** No-op when absent, `try/catch` when
  present, and never `await` telemetry on the request path.
- **A config file and a no-config flag fight each other.** If you add a vendor config file, stop
  forcing the no-config env var in the preload, or the file is silently ignored.
- `references/perf-benchmarking.md` — p50/p95/p99 latency baselines in JSONL, store size tracking, comparison over time
- `references/sqlite-journal.md` — moving an append-only log into SQLite: Kysely over node:sqlite, adopting an existing file, schema shape, tests
- **Skip native build extras on a fresh agent.** Optional native addons (metrics, fn-inspect) need a
  matching ABI and turn a working install into a rebuild loop; decline them and keep the pure-JS path
  until there is a reason.
- **Don't initialise the SDK in two places.** The preload owns startup; app code only consumes the
  tracer. Two initialisers produce double spans and a shutdown race.
