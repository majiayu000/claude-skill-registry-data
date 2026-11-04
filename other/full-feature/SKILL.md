---
name: full-feature
description: >-
  Orchestrate an end-to-end Greenhouse feature: requirements → core vs plugin decision → DB →
  shared types → API → universal client → Agent tools → tests → gate → docs → local acceptance.
  Superset of add-db-table, add-api-route, add-client-screen, add-agent-tool, add-agent-profile and
  quality-gate. Use for: build a complete feature / end to end / from table to page / full feature,
  做个完整功能, 端到端实现, 从表到页面都要, 做个插件. Red lines: core never imports or names a
  plugin, decide core vs plugin before writing code, the full gate before handoff.
---

# End-to-end feature

This skill only orders the work and makes the decisions; each layer's rules live in its sub-skill and module docs (copying them here would drift).

| Layer | Sub-skill | Source of truth |
|---|---|---|
| Database | add-db-table | packages/db/src/AGENTS.md |
| API | add-api-route | apps/api/src/AGENTS.md |
| Client UI | add-client-screen | apps/client/AGENTS.md, apps/client/DESIGN.md |
| Agent tool | add-agent-tool | apps/api/src/tools/define.ts |
| Agent profile | add-agent-profile | apps/api/src/profiles/AGENTS.md |
| Plugin package | — | EXTENDING.md, plugins/example |
| Gate | quality-gate | root AGENTS.md |

## Phase 0: questions before code
1. Data: which tables and columns; FK inside one domain or a logical link across domains?
2. API: which endpoints; internal, super only or behind a plugin feature flag?
3. Client: a place, an object sheet/inspector, a dialog, an Admin section, or a declarative plugin page?
4. Agent: must the model call it; through chat only, or also /api/agent and /api/mcp?
5. Permissions: who reads, who writes; which feature point or capability carries it?
- Non-trivial cross-cutting work gets a spec first: local-only docs/specs/YYYYMMDD-<name>.md with status, decisions, acceptance criteria and an index entry.
- Reuse before adding: a second implementation of the same job needs its reason in the relevant AGENTS.md.

## The key decision: core or plugin
- Core owns identity/permissions, conversations/Agents, models/budgets/gateway, tools/runs/audit, MCP/connectors, automations, Files, notifications/push, settings/branding, plugin host, administration and CLI.
- Anything optional, private, experimental or deployment-specific is a plugin package under plugins/<id>/; core consumes active registries and never imports a plugin or branches on its id.
- Package layout (copy plugins/example):
```text
plugins/<id>/
  package.json         "greenhouse": { "id", "sdk": 2, "api": "./api/index.ts" }, exports ./manifest and ./api
  manifest.ts          pure data: id, name, version (from package.json), sdk, core range, client_min, surfaces, dependsOn, features, ui
  api/index.ts         default defineExtension({ ...manifest, tools, routes, dataSources, featureFlags, featurePoints, migrations, services, … })
  api/schema.ts        owned tables (kit column helpers)
  migrations/          NNNN_name.sql lane (+ drizzle.config.ts at the package root when it has tables)
  ui/                  optional trusted static frontend for an embed page
  README.md AGENTS.md db-schema.md
```
- Add the path to `plugins` and the id to `extensions.enabled` in greenhouse.config.ts (GREENHOUSE_EXTENSIONS overrides at boot), then `pnpm plugins:sync`; compiled lists need a rebuild, enablement a restart.
- Plugin code imports only @greenhouse/api/extension-kit, @greenhouse/types/*, @greenhouse/crud, @greenhouse/ui*, own files and declared dependencies; `pnpm lint` enforces it.
- Manifest titles and labels are `{ en, zh }`; client glue copy goes in the client catalogs (plugin Admin sections under admin.ext.<id>).
- A missing hook is added to the contract only with a real consumer, Example coverage and seam tests (plugins/example/api/__tests__/seam.test.ts); never a per-plugin case in core.
- Client side: declarative pages (entity-list, entity-detail, settings-form, embed) need no client code; native pages and plugin Admin sections need glue in apps/client/src/plugins/<id>/ (add-client-screen).

## Phase 1: database → add-db-table
- Core: schema + _columns helpers + ids prefix → service → provider.ts → `pnpm drizzle-kit generate` at the root → review → `DATABASE_URL=<own db> pnpm db:migrate` → db-schema.md.
- Plugin: api/schema.ts → service bag → reviewed NNNN_name.sql lane file → plugins/<id>/db-schema.md.
- Persistent databases migrate, never push.

## Phase 2: shared types
- Server-shared protocol types go in packages/types/src (imported as @greenhouse/types/<module>); helpers come from packages/utils first.
- The client cannot import @greenhouse/*: copy what it needs into apps/client/src/shared (VENDORED verbatim files are parity-tested; greenhouse-types.ts is the hand-kept subset).

## Phase 3: API → add-api-route
- Core: chained `new Hono<AppEnv>()` → guards → services → one line in mountRoutes() without reordering.
- Plugin: a dataSource for table-backed entities (generated guarded REST, tools, search, export), hand-written routes on /api/ext/<id> only for real operations.
- A client that needs the endpoint raises MOBILE_API with the server's MOBILE_API_LEVEL.

## Phase 4: client → add-client-screen
- Pick the surface from DESIGN.md, build from the kit, open objects through openObject, write en + zh, keep logic React-free and tested.
- Run typecheck and lint inside apps/client; root checks skip it.

## Phase 5: Agent integration (when needed) → add-agent-tool
- defineTool with meta beside the implementation → CORE_TOOL_MODULES or the plugin's tools → surface → exactly one grant path.
- Profiles usually need no change: built-in YAML uses `tools: []`; prompts never restate tool rules.

## Phase 6: tests
| Layer | File name | Where |
|---|---|---|
| Unit / contract | `*.test.ts(x)` | beside the logic, tests/api, tests/utils, apps/client (React-free) |
| DB, rolled back | `*.db.test.ts` | tests/db, tests/api, plugins/<id>/api/__tests__ |
| DB, committed | `*.db-commit.test.ts` | only for cross-connection, DDL or locks; header `@db-commit-reason` |
| HTTP security | `*.e2e.test.ts` | tests/e2e (`pnpm test:e2e:ci`) |
| Browser | `*.e2e.ts` | tests/client-e2e (`pnpm test:e2e:client`) |
- Create members with tests/helpers/internal-user.ts; build fixtures from returned ids; assert only rows the test created.
- Plugins also test enabled and disabled, denials, scopes and field masks, write allowlists and audit.

## Phase 7: gate → quality-gate
```bash
pnpm typecheck && pnpm lint && TEST_DATABASE_URL=<loopback test db> pnpm test
```
- Plus the surface gates: test:e2e:ci, plugins:sync --check, test:core, client checks, test:e2e:client, app:build.

## Phase 8: docs
- Schema → db-schema.md (core or plugin); conventions → the nearest AGENTS.md; behavior people see → README.md.
- Plugin contract changes → EXTENDING.md + plugins/example + seam tests; a plugin's behavior → its README.md.
- Deletions update docs too and cascade to orphaned code, copy, routes, nav entries and tests.

## Local acceptance
```bash
pnpm dev                # client web on :3100, API on :3000
pnpm run-dev up         # or: Postgres + API + client web with logs in .run-dev/logs/
pnpm seed               # example dataset into an empty database
```
- Worktrees get their own database (greenhouse_wt_<slug>); never migrate the main database from a worktree, and let run-dev pick ports instead of killing processes.
- Look at wide (1440) and phone (390) widths, light and dark; native UI in a dev client.

## Checklist
- [ ] Phase 0 answered; core vs plugin decided; reuse reasons recorded
- [ ] DB: schema, service, migration or lane file, db-schema.md
- [ ] Types in packages/types; client copies vendored
- [ ] API: chained, guarded, mounted (core) or declared (plugin)
- [ ] Client: right surface, kit, en + zh, React-free tests
- [ ] Agent tool (if any): defineTool, registered, surface, one grant path
- [ ] Tests at every layer touched; gate green
- [ ] AGENTS.md / README / EXTENDING.md updated
