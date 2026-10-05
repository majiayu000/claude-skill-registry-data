---
name: factory-data-pipelines
description: Data ingestion and pipeline conventions for projects that import CSVs, run simulations, or operate Python services alongside Next.js. Covers Papa Parse for CSV imports, JSONB envelope storage for time-series data, the three-entry-point Python service pattern (CLI / Cloud Run API / Pub/Sub), YAML config for service-level data, geopandas/shapely for geospatial work, and deployment via Cloud Run + ephemeral Neon DBs.
---

# Factory data pipelines

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Papa Parse / FastAPI / Cloud Run shape we use), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`.

## CSV ingestion — a script, not a framework

**Principle.** A one-shot CSV importer is a standalone script in `scripts/`; promote to a framework only when a second consumer appears.

**Why.** Premature job-framework adoption for a single CSV importer is paying the abstraction cost without the abstraction benefit. A standalone script with Papa Parse and a Drizzle transaction is grep-able, debuggable, runnable locally. Wrapping it in BullMQ / Inngest / a Cloud Run job buys nothing until there's a second importer that shares the wrapper.

**Recipe.**

```
scripts/
└── data_processing/
    ├── import-state-data.ts
    ├── simulations/
    │   └── import-simulation.ts
    └── vins/
        └── import-vins.ts
```

```ts
import Papa from 'papaparse';
import { db } from '@/db';
import { foo } from '@/db/schema';

const { data } = Papa.parse<FooRow>(csvText, { header: true, skipEmptyLines: true });

await db.transaction(async (tx) => {
  for (const row of data) {
    await tx.insert(foo).values({ /* ... */ }).onConflictDoUpdate({ /* ... */ });
  }
});
```

## Time-series / event storage — JSONB envelope

**Principle.** What drives queries gets a real column. What doesn't goes in a JSONB envelope. The schema inside JSONB can evolve without a migration.

**Why.** Time-series data and event streams have an outer schema (the row) and an inner schema (the payload). The outer schema needs to be queryable — filter by `fleetId`, sort by time, join across rows. The inner schema is consumed by application code that already speaks its types, doesn't need a SQL index, and may evolve faster than migrations can keep up. JSONB envelope splits these clean: columns for outer, JSONB for inner. The trap is querying inside JSONB at app speed — once you're doing that, the field has earned a column.

**Recipe.**

```ts
export const simulations = pgTable('simulations', {
  id: uuid('id').defaultRandom().primaryKey(),
  ...timestamps,
  // Structured columns for things that drive queries
  fleetId: uuid('fleet_id').references(() => fleets.id, { onDelete: 'cascade' }).notNull(),
  status: text('status').notNull(),
  // JSONB envelope for everything else
  metadata: jsonb('metadata').$type<SimulationMetadata>().notNull(),
  timeSeriesData: jsonb('time_series_data').$type<TimeSeriesPoint[]>().notNull(),
  chargingEvents: jsonb('charging_events').$type<ChargingEvent[]>().notNull(),
});
```

## YAML-driven service config

**Principle.** Service-level reference data (routes, vehicle specs, charger specs) lives in YAML, not code; env-overridable per environment.

**Why.** "Static" reference data is the part of the system the domain expert most wants to edit, and the part engineers least want to redeploy for. YAML in a config directory is the seam: the domain expert opens the file, edits a value, and the change ships through the same review process as code without code-thinking required. Env-driven base paths let prod, staging, and customer-specific overrides coexist.

**Recipe.**

```
models/<service>/
├── config/
│   ├── routes.yaml
│   ├── vehicles.yaml
│   └── chargers.yaml
└── src/
    └── services/
        └── data_service.py    # loads + validates + serves the config
```

JSON config overrides via env var or request payload.

## Three-entry-point pattern (Python services)

**Principle.** A Python service has three entry points sharing one core: CLI for local runs, FastAPI for HTTP, Pub/Sub handler for async jobs. The entry points are thin; the core does the work.

**Why.** The same simulation needs to run three ways: locally for development, synchronously for short jobs over HTTP, asynchronously for long jobs via queue. Three separate codebases means three places to fix every bug. One core with three entry points means the work is defined once; the wrappers only differ in I/O. Each entry point is a fifty-line file that calls the core.

**Recipe.**

```
models/<service>/
├── main.py              # CLI — local runs, ad-hoc invocations
├── main_api.py          # FastAPI — Cloud Run HTTP endpoint
├── main_pubsub.py       # Pub/Sub handler — async job processing
├── Dockerfile           # Pub/Sub variant
├── Dockerfile.api       # API variant
└── src/
    ├── simulation/
    │   └── simulation_runner.py   # the actual work; mode-aware
    └── services/                  # injected deps (Mapbox, weather, GCS, DB)
```

`simulation_runner.py` is mode-aware (CLI vs Cloud) — structured log paths, GCS + DB integration. The three entry points are thin wrappers.

**Failure mode.** Sharing Pydantic models across the three entry points by copy-paste — the models drifted, deserialization broke at the Pub/Sub boundary, only visible when the queue replayed.

## FastAPI conventions

**Recipe only** — the principles (API key from header, OpenAPI off in prod, Pydantic for shapes, lifespan-managed DB engine, request ID for tracing) are encoded in the recipe itself.

- API-key dependency: `get_api_key()` reads from header, validates against env
- OpenAPI docs toggleable via env (off in prod)
- Pydantic models for all request/response shapes — never inline dicts
- Lifespan context manager for DB engine init/close
- Request logging middleware with trace ID propagated to response header

```py
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response
```

See `factory-observability.md` for the trace-ID propagation principle.

## Cloud Pub/Sub triggering from Next.js

**Recipe only** — env-driven credentials, JSON payload.

```ts
// src/server/cloud/cloudRun.ts
export async function triggerSimulationJob(payload: SimulationRequest) {
  const message = { ...payload, mode: 'db' /* or 'gcs' */ };
  return pubsub.topic(TOPIC).publishMessage({ json: message });
}
```

GCP credentials from env (JSON string or file path — use the env-driven helper, not hardcoded paths).

## Submit / poll / fetch — async over HTTP timeout

**Principle.** When a job exceeds HTTP timeout, split into three idempotent operations: submit returns a job ID, client polls status, fetches result separately.

**Why.** Long-running HTTP calls are fragile — the load balancer's timeout, the client's timeout, the proxy's timeout. Each adds a failure mode that doesn't recover. Submit/poll/fetch breaks the work into three short operations that each fit comfortably under any timeout. Each operation is idempotent (submit can dedupe; status is a read; fetch is a read), so retries are safe.

**Recipe.**

```ts
const { jobId } = await fleetsim.submit(payload);
const status = await fleetsim.pollStatus(jobId);  // until 'complete' | 'failed'
const result = await fleetsim.fetchResult(jobId);
```

Three endpoints, three idempotent operations. Never block the client on a single long-running HTTP call.

## Converter vs service split

**Principle.** Pure transformations live in `*-converter.ts` (client-safe, no I/O); orchestration lives in `*-service.ts` (server-only, may call multiple converters).

**Why.** Mixing pure transforms with I/O makes the transforms untestable without mocking and unusable on the client. Splitting them lets the same conversion function run in a browser preview and in the server-side service that talks to the world. The boundary is enforceable: a converter that imports `fetch` or a DB client is a converter that's blurred its line.

**Recipe.** Converter is the part you reuse in the client; service is the part that talks to the world.

## Geospatial — `geopandas + shapely` in one service file

**Recipe only** — route loading from GeoJSON, coordinate extraction from `LineString` / `MultiLineString` / `Polygon` belongs in a single `data_service.py`. Don't duplicate per consumer.

## Deployment

**Recipe only** — the principles (one service per entry-point variant; migrations in CI, not runtime; ephemeral Neon branch per PR) are stated in `factory-deployment.md` and `factory-data-layer.md`.

- **Web (Next.js):** Vercel
- **Python services:** Cloud Run, one service per Python entry-point variant (separate Dockerfiles, different startup commands)
- **DBs:** Neon for web (branch-per-PR via GitHub Actions); shared instance for backend services
- **GitHub Actions:** ephemeral Neon DB per PR; matrix-deploy web + each Python service to Cloud Run on merge

## Don't pre-build shared `libs/`

**Principle.** Don't scaffold a shared library before the second consumer exists; empty scaffolding is worse than no scaffolding.

**Why.** A `libs/py-libs/` directory with three modules and no callers signals "shared code lives here" without any actual shared code. New contributors put things there that aren't shared; the first real refactor has to untangle that misuse. Wait for the second consumer; extract then.

**Recipe.** First implementation lives in the consuming service. Second consumer is the trigger to extract. The third consumer confirms the extraction was right.

## Source patterns

Ford-analysis (CSV imports via Papa Parse, JSONB envelope, modular calculator engine, submit-poll-fetch async pattern, converter/service split), encode/monorepo (three-entry-point Python pattern, YAML config, FastAPI shape, Pub/Sub triggering, geopandas/shapely), cothon (request logging middleware, async SQLAlchemy with SoftDelete mixin).
