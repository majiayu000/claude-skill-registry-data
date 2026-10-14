---
name: 05-appkit-lakebase-wiring
description: >
  Wire a Lakebase PostgreSQL backend into an existing AppKit project. Covers database
  schema design from a PRD, idempotent DDL, Express API routes with mock fallback,
  React data hooks, and local testing. PRD-independent patterns that apply to any
  AppKit + Lakebase app. Use after registering the Lakebase plugin via
  04-appkit-plugin-add. Triggers on "wire lakebase", "lakebase backend", "CRUD API",
  "lakebase tables", "DDL", "database schema design", "useLakebaseData",
  "mock fallback", "ConnectionStatus", "replace mock data", "connect frontend to
  backend", "API-backed data", "replace static data with database".
license: Apache-2.0
compatibility: Requires Lakebase plugin registered via 04-appkit-plugin-add, Node.js v22+, Databricks CLI >= 0.295.0
allowed-tools: Bash(databricks:*) Bash(npm:*) Bash(curl:*) Bash(node:*) Read
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Wiring is source editing (server.ts DDL/routes, hooks) — client-agnostic. DDL runs **server-side** on
  first deploy under the app's Service Principal (Deploy-First Pattern), so the SP owns the schema/tables on
  both clients — never run DDL locally. IDE: `npm run build` gates locally, then `databricks apps deploy
  --profile $PROFILE`. Genie Code: local `npm run build` gates are an IDE convenience (no local npm) — skip
  them and let the platform build server-side; deploy via `runDatabricksCli` (omit `--profile`) or the SDK
  fallback in `03-appkit-deploy`. Verify via browser `ConnectionStatus` / `apps logs` or the OAuth-session test.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: apps
  role: lakebase-wiring
  standalone: false
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills/databricks-lakebase"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-lakebase/SKILL.md"
      relationship: "extended"
      last_synced: "2026-04-27"
      sync_commit: "manifest-v2-2026-04-22"
    - name: "databricks-agent-skills/databricks-apps"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-apps/SKILL.md"
      relationship: "extended"
      last_synced: "2026-04-27"
      sync_commit: "manifest-v2-2026-04-22"
---

# Wire Lakebase Backend into AppKit

Design a database schema from a PRD, build Express API routes with mock fallback, wire the React frontend to live data, and verify locally.

## When to Use

- Wiring a Lakebase PostgreSQL backend into an AppKit app that already has the plugin registered
- Designing database tables from a PRD or feature spec
- Building CRUD API routes with `server.extend()`
- Replacing static mock data with API-backed data fetching
- Adding a health endpoint and ConnectionStatus indicator

**Not for registering the plugin.** Use `04-appkit-plugin-add` to install and configure the Lakebase plugin first.
**Not for deploying.** Use `03-appkit-deploy` after wiring is complete.

---

## Before You Begin

**Prerequisites — verify these before proceeding:**

1. The Lakebase plugin is registered in `server/server.ts` (via `04-appkit-plugin-add`)
2. Bundle resources (`postgres_project`/`postgres_branch`/`postgres_endpoint`) are declared in `databricks.yml`
3. `app.yaml` has `LAKEBASE_ENDPOINT` with `valueFrom: postgres` and `DB_SCHEMA` as a static env var
4. `DB_SCHEMA` is set to a user-scoped name derived from `$APP_NAME` (hyphens → underscores, e.g., `jane_d_booking_app`)
5. `npm run build` passes with the Lakebase plugin imported

**Upstream docs (always check for latest):**

```bash
npx @databricks/appkit docs "lakebase"
```

> **Build system note:** AppKit uses `tsdown` with `unbundle: true` for server compilation. Each `.ts` file in `server/` gets its own `.js` output, and relative imports between them are preserved. You can safely split `server/server.ts` into multiple files (e.g., `server/mock-data.ts`, `server/mappers.ts`) — they will resolve correctly at runtime. The entry point remains `server/server.ts`.

### Working in Genie Code (client routing)

All the **code** in this skill — DDL, routes, hooks, mappers — is written into the project the same way on both clients. The DDL is intentionally executed **server-side on first deploy** (the "Deploy-First Pattern" in Step 1d), so it is already client-agnostic. Only the **local build/test gates** differ:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `npm run build` gates (Steps 2g, 3c2, 4a, 4b) — "**You MUST run `npm run build`**" | **IDE-only** convenience — there is no local Node toolchain on Genie Code. Skip them; the platform runs the same build **server-side** on deploy, and TypeScript/import errors surface in `databricks apps logs <name>`. Wire the code, then deploy and read the logs. |
| `npm run dev` | not available on Genie Code (and blocked pre-deploy anyway — `lakebase()` needs platform-injected env) — verify on the deployed app instead |
| `npx @databricks/appkit docs "lakebase"` | npx absent (P9) — WebFetch https://databricks.github.io/appkit/docs/plugins/lakebase |
| `databricks … --profile $PROFILE` | run via `runDatabricksCli`, **omit `--profile`** (pre-authenticated) |
| local `curl … -H "Authorization: Bearer …"` health test | browser `ConnectionStatus` + `apps logs`, **or** the 3-hop OAuth `requests.Session()` test (see Quick Reference note and `03-appkit-deploy`) |

Paths are relative to `apps_lakebase/$APP_NAME` — on Genie Code that resolves inside your git-cloned workshop project (`artifact_root`), never the read-only `.assistant/skills` copy and never `/tmp`. The `apps validate` skip and the health-test routing are already flagged inline at Steps 4a2 and Quick Reference. See `skills/genie-code-environment` for the full manifest.

---

## Decision Defaults

When multiple approaches are valid, use these defaults. Override only if the PRD demands it.

| Decision | Default | Rationale |
|----------|---------|-----------|
| Where does mock data live? | `server/mock-data.ts` — server owns all fallback data | Client and server are separate builds; cannot import across the boundary |
| Single server file or split? | **Split when `server.ts` exceeds 300 lines.** Extract mappers to `server/mappers.ts`. Count lines after writing: `wc -l server/server.ts`. | `tsdown unbundle: true` preserves relative imports between server files (see note above) |
| Numeric PK or text PK? | Use `text` PK if the frontend already uses formatted IDs (e.g., `"lst-001"`) everywhere; otherwise `bigint identity` | Avoids a format-conversion layer that touches every route and mapper |
| N+1 queries or JOINs? | Application-side joins for <50 rows; SQL JOINs for larger datasets | Simpler code; performance is irrelevant at seed-data scale |
| Client-side or server-side validation? (promos, discounts) | Keep client-side for MVP; migrate to server in a follow-up | Reduces scope of this step |
| Dynamically generated data (available dates, time slots)? | Generate in the mapper function, not a database table | Avoids seeding hundreds of ephemeral rows |
| Mock fallback data format? | camelCase (matching API response after mappers) | Catch block returns data in the same shape as the live path |
| Seed data: parameterized inserts or raw SQL? | **Parameterized (`$1, $2`) iterating over MOCK_* arrays** for all tables when mock-data.ts exists. Raw SQL only when no mock array exists and data is purely numeric. | Single source of truth; type-safe; avoids escaping bugs |

---

## Step 1: Design the Database Schema

Derive your database schema from the PRD. This step produces DDL and seed data in `server/server.ts`.

### 1a. Identify Entities from the PRD

Read the PRD and extract:

- **Entities** — each major noun becomes a table (e.g., `bookings`, `listings`, `users`)
- **Attributes** — each property becomes a column
- **Relationships** — identify 1:N (FK) and M:N (junction table) relationships
- **Data types** — map PRD fields to PostgreSQL types using the conventions below

### 1b. PostgreSQL Type Conventions

For normalization rules, naming conventions, and additional type guidance, see [references/database-design-guide.md](references/database-design-guide.md).

| PRD Concept | PostgreSQL Type | Why |
|-------------|----------------|-----|
| Unique ID | `bigint generated always as identity primary key` | SQL-standard, future-proof (not `serial`) |
| Short text (name, email, status) | `text` | Same performance as `varchar(n)`, no artificial limit |
| Constrained text (status enum) | `text` + `CHECK` constraint | `CHECK (status IN ('pending','confirmed','cancelled'))` |
| Money / price | `numeric(10,2)` | Exact decimal arithmetic (not `float`) |
| Timestamp | `timestamptz default now()` | Always timezone-aware (not `timestamp`) |
| Date only | `date` | Calendar dates without time component |
| Boolean flag | `boolean default false` | 1 byte (not `varchar`) |
| Foreign key | `bigint references other_table(id)` | Always add an index on FK columns |

### 1c. Schema Naming

Use `DB_SCHEMA` (from env var) as the PostgreSQL schema for all objects:

```sql
CREATE SCHEMA IF NOT EXISTS ${DB_SCHEMA};
CREATE TABLE IF NOT EXISTS ${DB_SCHEMA}.bookings ( ... );
```

This prevents collisions when multiple apps share a Lakebase database. All DDL, queries, and grants must use `${DB_SCHEMA}` consistently.

> **`DB_SCHEMA` is a SINGLE Postgres schema name — never a dotted UC FQN.** It must be one identifier (hyphens → underscores, e.g. `jane_d_booking_app`); a `catalog.schema` Unity Catalog FQN with a `.` is **not** a valid Postgres schema and quoting it as one silently breaks GRANTs and `search_path`. For a **read-only app over already-synced tables** (the activation reverse-ETL track), do not trust the `DB_SCHEMA` template literal at all — the schema NAME the sync actually landed (from `information_schema` introspection / `reverse_etl.md`) is authoritative; use the introspected value everywhere and reject a dotted one.

### 1d. Write Idempotent DDL

All DDL runs on every app startup. It must be safe to execute repeatedly.

```typescript
const AppKit = await createApp({
  plugins: [server(), lakebase()],
});

const DB_SCHEMA = process.env.DB_SCHEMA || "app";

await AppKit.lakebase.query(`CREATE SCHEMA IF NOT EXISTS ${DB_SCHEMA}`);
await AppKit.lakebase.query(`
  CREATE TABLE IF NOT EXISTS ${DB_SCHEMA}.orders (
    id bigint generated always as identity primary key,
    customer_name text not null,
    amount numeric(10, 2) not null,
    status text default 'pending' check (status in ('pending', 'confirmed', 'cancelled')),
    created_at timestamptz default now()
  )
`);
```

**Index foreign key and frequently filtered columns:**

```typescript
await AppKit.lakebase.query(`
  CREATE INDEX IF NOT EXISTS idx_orders_status
  ON ${DB_SCHEMA}.orders (status)
`);
```

> **Deploy-First Pattern:** DDL is written in `server.ts` so the Service Principal executes it on first deploy and becomes the owner of the schema, tables, and sequences. This is critical — if you run DDL locally first, your personal identity owns the objects and the SP cannot access them after deployment. The workshop sequence (wire code locally with mock fallback, then deploy so SP creates objects) follows this pattern. Reference: [AppKit Lakebase docs - Local development](https://databricks.github.io/appkit/docs/plugins/lakebase#local-development)

### 1e. Seed Data (Count-Check Pattern)

Use a count-check pattern for idempotent seeding. Do NOT use `ON CONFLICT DO NOTHING` — it fails to prevent duplicates with `identity`/`serial` PKs that auto-generate new IDs on every insert.

```typescript
const seedCheck = await AppKit.lakebase.query(
  `SELECT count(*) AS cnt FROM ${DB_SCHEMA}.orders`
);
if (parseInt(seedCheck.rows[0].cnt) === 0) {
  await AppKit.lakebase.query(`
    INSERT INTO ${DB_SCHEMA}.orders (customer_name, amount, status) VALUES
      ('Alice', 99.99, 'confirmed'),
      ('Bob', 45.00, 'pending'),
      ('Carol', 72.50, 'confirmed')
  `);
  console.log("[Lakebase] Seed data inserted");
}
```

> **Apostrophe escaping:** If seed data contains apostrophes (e.g., `chef's kitchen`), use double single quotes in raw SQL: `'chef''s kitchen'`. Alternatively, use parameterized inserts (`$1, $2`) which handle escaping automatically — see the Decision Defaults table.

For multi-table seed patterns with foreign keys, see [references/multi-table-example.md](references/multi-table-example.md).

### 1f. Mock Data Strategy

When the app already has a client-side `mockData.ts` with static arrays, use this migration pattern:

1. **Create `server/mock-data.ts`** with the same data in camelCase format (matching what mappers would produce from DB rows). Export typed arrays.
2. **Import into `server/server.ts`** for use in catch-block fallbacks and as the source for seed SQL generation.
3. **Keep `client/src/data/mockData.ts`** for type definitions, UI constants (filter options, property type lists), and utility functions. Remove the data arrays once all pages use `useLakebaseData`.
4. **Pages switch from** `import { LISTINGS } from '../data/mockData'` **to** `useLakebaseData<Listing>('/api/listings')` — the server returns mock fallback data when Lakebase is unavailable, so the client never needs its own copy of the data.

File ownership after wiring:

| File | Contains | Does NOT contain |
|------|----------|------------------|
| `server/mock-data.ts` | All data arrays (listings, bookings, etc.) in camelCase | Type definitions, UI constants |
| `client/src/data/mockData.ts` | Type interfaces, filter-option constants, utility functions | Data arrays (deleted after migration) |
| `server/server.ts` | DDL, seed logic, routes importing from `mock-data.ts` | Inline mock data objects |

> **This table is prescriptive.** `server/mock-data.ts` must NOT define TypeScript interfaces — those belong exclusively in `client/src/data/mockData.ts`. The server file exports data arrays only and imports types from the client when feasible, or uses `Record<string, unknown>` parameter types with explicit return-type annotations. Duplicating interfaces causes type drift (e.g., server `status: string` vs. client `status: "confirmed" | "cancelled"`).

---

## Step 2: Build API Routes

AppKit Lakebase is **server-side only** — there are no frontend hooks like `useAnalyticsQuery`. Use `server.extend()` to add Express routes.

> **Note:** The upstream [databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) Lakebase reference uses tRPC for server-side CRUD. This skill uses `server.extend()` with Express routes for explicit control over request/response handling, which is simpler for workshop purposes. Both patterns are valid AppKit approaches. If the scaffold generated tRPC boilerplate (from `--features lakebase`), either pattern works — use whichever is already in your codebase.

### 2a. Server Setup Pattern

Register custom routes inside the `onPluginsReady` callback. It runs after the plugins initialize but **before** the `server()` plugin starts listening — exactly the window where `appkit.server.extend()` must attach Express routes. Move the Step 1 DDL and the Step 1e seed inside this same callback (before the `extend` call) so the schema exists before the server accepts traffic. Do **NOT** pass `autoStart: false` and do **NOT** call `AppKit.server.start()` yourself:

```typescript
import { createApp, server, lakebase } from "@databricks/appkit";

const DB_SCHEMA = process.env.DB_SCHEMA || "app";

await createApp({
  plugins: [server(), lakebase()],
  async onPluginsReady(appkit) {
    // DDL + seed (from Step 1) — run before the server accepts traffic
    await appkit.lakebase.query(`CREATE SCHEMA IF NOT EXISTS ${DB_SCHEMA}`);
    // ... CREATE TABLE / INDEX + count-check seed ...

    appkit.server.extend((app) => {
      // Register routes here (Steps 2b-2d)
    });
  },
});
```

> **`npm run dev` will NOT work until after the first deploy.** The `lakebase()` plugin throws `ConfigurationError` during `createApp()` when `LAKEBASE_ENDPOINT` and `PGHOST` are not set. These env vars are injected by the platform after the Lakebase project is provisioned (first deploy). Use **`npm run build` only** for local validation at this step — it type-checks and bundles without executing the code. Runtime testing with `npm run dev` is available after deployment creates the Lakebase project and you populate `.env` with connection details (see the **Deploy and E2E Test** step, Step 7).

> **Gotcha — register routes in `onPluginsReady`, never call `server.start()` manually.** The `server()` plugin owns the HTTP listener. Passing `autoStart: false` and then calling `AppKit.server.start()` yourself is the stale pattern — it double-`listen()`s (the plugin still binds the port) and the app crashes on boot (`EADDRINUSE`). The supported shape is the `onPluginsReady(appkit)` hook on `createApp`: it fires after plugins init but before the listener binds, so `appkit.server.extend(...)` routes are attached in time. The `server()` plugin also auto-adds `/health` — do not register it yourself. Reference: [developer docs — AppKit `createApp` (`onPluginsReady` hook)](https://developers.databricks.com/appkit).

> **Gotcha — Do NOT annotate `app` with `: any` or `: Express`.** AppKit's AST-grep linter blocks `any` annotations (`no-as-any` rule), and importing `Express` from the `express` module causes TS2345 (type mismatch with AppKit's internal type). Leave `app` untyped in `server.extend((app) => { ... })` — TypeScript infers the correct type from the callback signature. For route handler parameters, import and use `Request` and `Response` types from `express`.

### 2b. Response Contract

Every data endpoint must return this shape:

```typescript
{ data: T[], source: "live" | "mock" }
```

- `source: "live"` — data came from Lakebase
- `source: "mock"` — Lakebase unavailable, returning fallback data

### 2c. CRUD Route Pattern (with Mock Fallback)

Every route follows try/catch with mock fallback:

```typescript
import type { Request, Response } from "express";

app.get("/api/orders", async (req: Request, res: Response) => {
  try {
    const result = await AppKit.lakebase.query(
      `SELECT * FROM ${DB_SCHEMA}.orders ORDER BY created_at DESC`
    );
    console.log(`[Lakebase] /api/orders returned ${result.rows.length} rows`);
    res.json({ data: result.rows, source: "live" });
  } catch (err) {
    console.warn(`[Lakebase] /api/orders fallback: ${err}`);
    res.json({
      data: [{ id: 1, customer_name: "Demo", amount: 99.99, status: "mock" }],
      source: "mock",
    });
  }
});
```

**For parameterized queries**, use `$1`, `$2` placeholders (not string interpolation):

```typescript
app.get("/api/orders/:id", async (req, res) => {
  try {
    const result = await AppKit.lakebase.query(
      `SELECT * FROM ${DB_SCHEMA}.orders WHERE id = $1`,
      [req.params.id]
    );
    res.json({ data: result.rows, source: "live" });
  } catch (err) {
    res.json({ data: [], source: "mock" });
  }
});
```

### 2d. Health Endpoint

Always include a health endpoint:

```typescript
app.get("/api/health/lakebase", async (req, res) => {
  try {
    await AppKit.lakebase.query("SELECT 1");
    res.json({ status: "connected", source: "live" });
  } catch (err) {
    res.json({ status: "disconnected", error: String(err), source: "mock" });
  }
});
```

### 2e. POST/PUT Routes (skip if your app only has GET endpoints)

If your app has POST or PUT routes, add JSON body parsing. Express is bundled inside AppKit — access it exclusively via the `app` parameter in `server.extend()`:

```typescript
AppKit.server.extend((app) => {
  app.use((req, _res, next) => {
    if (req.headers["content-type"]?.includes("application/json") && !req.body) {
      let raw = "";
      req.on("data", (chunk) => { raw += chunk; });
      req.on("end", () => {
        try { req.body = JSON.parse(raw); } catch { req.body = {}; }
        next();
      });
    } else { next(); }
  });

  // POST routes ...
});
```

> **Gotcha — `import express`:** Do not `import express` or `require("express")` just for `express.json()`. It creates a redundant copy alongside AppKit's bundled version and may cause version conflicts. Use the inline parser above instead.

### 2f. Connection Resilience (optional)

AppKit's Lakebase plugin handles OAuth token rotation and caching automatically. Configure pool settings only if you need additional resilience:

```typescript
await createApp({
  plugins: [
    lakebase({
      pool: {
        max: 10,
        connectionTimeoutMillis: 5000,
        idleTimeoutMillis: 30000,
      },
    }),
  ],
});
```

---

## Step 2g: Build Gate

**You MUST run `npm run build` and fix all errors before proceeding to Step 3.** Backend build errors found after frontend wiring are much harder to diagnose. This gate catches them early.

**Line count check:** After build passes, run `wc -l server/server.ts`. If >300 lines, extract mapper functions to `server/mappers.ts` and re-run build before proceeding.

---

## Step 3: Wire Frontend

Replace all static mock data arrays in React components with API-backed data fetching.

### 3a. `useLakebaseData` Hook

**You MUST read [references/frontend-patterns.md](references/frontend-patterns.md) and copy the `useLakebaseData` hook into `client/src/hooks/useLakebaseData.ts`.** This hook replaces `useState`/`useEffect`/`fetch` boilerplate with a reusable pattern that returns `{ data, source, error }`.

Usage: `const { data, source, error } = useLakebaseData<Order>("/api/orders");`

### 3b. `ConnectionStatus` Component

**You MUST read [references/frontend-patterns.md](references/frontend-patterns.md) and copy the `ConnectionStatus` component.** Place it at the top of every page that fetches data. Pass a `context` string describing the data (e.g., `context="orders"`).

### 3c. Replace Static Mock Data

- Replace all static `data` arrays with `useLakebaseData` hook calls
- For AppKit chart components (`BarChart`, `AreaChart`, `DonutChart`, `DataTable`), use the `data` prop with fetched results

> **Gotcha — `queryKey` requires the analytics plugin.** Do NOT use `queryKey` on chart components. Use the `data` prop with fetched results from `useLakebaseData` instead.

### 3c2. Intermediate Build Gate

**After rewiring every 2-3 page files, run `npm run build` (or `npx tsc --noEmit`).** Do not rewrite all pages in a single pass.

When removing a static data import (e.g., `import { LISTINGS } from '../data/mockData'`), audit every other import in the same file. Symbols like `MapPin`, `User`, or helper functions may have only been used alongside the removed data source. If a page previously showed data from `PARENT_ARRAY.find()` (e.g., a property image on a booking page), the rewrite must either fetch that data via API or explicitly acknowledge the removal.

> **Rule: removing a data import may orphan UI elements that depended on it.** Check imports and visual output after each batch. See [references/multi-table-example.md](references/multi-table-example.md) "Cross-Entity Enrichment" for the API pattern.

### 3d. Defensive Data Handling

**You MUST read the "Defensive Data Handling" section in [references/frontend-patterns.md](references/frontend-patterns.md).** Key rules: coerce DECIMAL with `Number()`, format DATE with `.toISOString().slice(0,10)`, write mapper functions for snake_case-to-camelCase.

> **Gotcha — DECIMAL columns are returned as strings** by `node-pg`. `"73" + "51"` produces `"7351"` (concatenation, not addition). Always coerce with `Number()` in mapper functions.

> **Gotcha — DATE columns are returned as JS Date objects.** `String(date)` produces `"Fri May 15 2026..."`. Use `.toISOString().slice(0, 10)` for `YYYY-MM-DD` format.

### 3e. TypeScript Interfaces for Chart Compatibility

**You MUST add `[key: string]: unknown` index signatures** to all interfaces passed to AppKit chart `data` props. See [references/frontend-patterns.md](references/frontend-patterns.md) for the pattern.

### 3f. Post-Wiring Cleanup (optional but recommended)

After all pages are wired to API calls:

1. **Rename `mockData.ts`** to better reflect its new role:
   - Move type interfaces to `client/src/data/types.ts`
   - Move utility functions and constants to `client/src/data/constants.ts`
   - Delete the original `mockData.ts` (or keep it as a re-export if too many imports to update)

2. **Import server mapper return types from the client types:**
   ```typescript
   import type { Listing } from "../shared/types";
   function mapListingRow(row: any): Listing { ... }
   ```
   This ensures server mapper output matches client expectations at compile time. If a `shared/` directory is not feasible, at minimum annotate mapper return types to match the client interface names.

The field-name mismatch class of bugs (e.g., `image` vs `imageUrl`) is eliminated when mapper functions declare their return type explicitly.

---

## Step 4: Build Gate and Local Test

### 4a. Build Gate

```bash
cd apps_lakebase/$APP_NAME
npm run build   # Must pass with zero errors
```

Fix TypeScript, ESM, or import errors now. Each deploy cycle takes 3-5 minutes — catching errors locally saves significant time.

### 4a2. Validate (optional but recommended)

Run the full AppKit validator to catch issues that `npm run build` alone misses — TypeScript strict mode errors (e.g., `app` parameter implicitly `any`), smoke test selector regressions, and resource binding problems:

```bash
databricks apps validate --profile $PROFILE
```

If the smoke test fails because of default selectors ("Minimal Databricks App", "hello world"), update `tests/smoke.spec.ts` heading and text assertions to match your app's actual content. See [testing.md](https://github.com/databricks/databricks-agent-skills/blob/main/skills/databricks-apps/references/testing.md).

> **Client note — Genie Code:** `databricks apps validate` is **hard-blocked** via `runDatabricksCli`. Skip it and rely on the **server-side build logs** after deploy; see `03-appkit-deploy` Step 1 (Client note).

### 4b. Local Validation (Build Only)

> **Do NOT run `npm run dev` at this step.** The `lakebase()` plugin throws `ConfigurationError` when `LAKEBASE_ENDPOINT` and `PGHOST` are not set. These env vars are provisioned by the platform on first deploy. `npm run build` is sufficient — it validates all TypeScript, imports, and bundling without executing the code.

```bash
cd apps_lakebase/$APP_NAME
npm run build   # Must pass with zero errors
```

Runtime testing (`npm run dev`, `curl` endpoints, UI verification) happens **after deployment** in the **Deploy and E2E Test** step. After that deploy creates the Lakebase project and you configure `.env` with connection details, `npm run dev` works locally with live data.

### 4c. What to Verify at This Step

Since `npm run dev` is not available, verify these through `npm run build` output:

- Zero TypeScript errors (catches incorrect types, missing imports)
- All `@databricks/lakebase` and `@databricks/appkit` imports resolve
- DDL strings, route handlers, and mapper functions compile
- Mock fallback data arrays match the expected API response shape

---

## Gotchas (Summary)

Detailed callouts are embedded inline at the relevant step. This table is a compact reference validated by three independent agent runs.

| Gotcha | Fix | Step |
|--------|-----|------|
| `ON CONFLICT DO NOTHING` with identity PKs | Count-check seed pattern | 1e |
| `import express` / `require("express")` | Use `server.extend((app))` + inline parser | 2e |
| Manual `AppKit.server.start()` / `autoStart: false` | Register routes in `onPluginsReady(appkit)` + `appkit.server.extend(...)`; let `server()` own the listener (manual start double-binds → `EADDRINUSE`) | 2a |
| `lakebase()` crashes without env vars (`LAKEBASE_ENDPOINT`, `PGHOST`) | Expected before first deploy. Use `npm run build` only; `npm run dev` works after deploy + `.env` setup | 2a |
| DECIMAL columns → strings | `Number()` in mappers | 3d |
| DATE columns → Date objects | `.toISOString().slice(0,10)` | 3d |
| `queryKey` on chart components | Use `data` prop instead | 3c |
| `npm run dev` crashes without Lakebase env vars | Use `npm run build` only before first deploy | 4b |
| Old `postgres:` resource format | Use `postgres_project`/`postgres_branch`/`postgres_endpoint` | Prerequisites |
| Stale endpoint hostname in `.env` | Re-fetch: `databricks postgres get-endpoint ...` | Prerequisites |
| AppKit AST-grep linter blocks `as any` and `as unknown as T` | Avoid type assertions; use proper type imports or leave parameters untyped for inference. `databricks apps validate` runs these rules but `npm run build` does not | 2a |
| SP permission errors on deploy | Verify bundle resource bindings in `databricks.yml` | Prerequisites |

---

## Quick Reference

| Task | Command / Pattern |
|------|------------------|
| Check live Lakebase docs | `npx @databricks/appkit docs "lakebase"` |
| Derive schema name | `DB_SCHEMA=$(echo "$APP_NAME" \| tr '-' '_')` |
| Build gate | `npm run build` (must pass with zero errors) |
| Test health endpoint (after deploy) | `curl -s "$APP_URL/api/health/lakebase" -H "Authorization: Bearer $TOKEN" \| jq .` (IDE only — see note) |

> **Client note — Genie Code:** a plain `curl … -H "Authorization: Bearer $TOKEN"` does **not** work (`auth token` hard-blocked; raw Bearer rejected by AppKit's OAuth gate → 401). Two working paths: **(1) browser** — open the app URL and read the `ConnectionStatus` indicator (live/mock), plus `databricks apps logs <name>` for `[Lakebase]` query lines; **(2) programmatic** — hit `/api/health/lakebase` via the **3-hop OAuth `requests.Session()` pattern** in `03-appkit-deploy` "Testing Deployed App APIs" (Client note).

---

## See Also

- Upstream platform skills: [`databricks-lakebase`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-lakebase) and [`databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) (both tracked in `upstream_sources`).
- AppKit Lakebase plugin docs: [databricks.github.io/appkit/docs/plugins/lakebase](https://databricks.github.io/appkit/docs/plugins/lakebase)

