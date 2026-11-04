---
name: add-api-route
description: >-
  Add a Hono API route to Greenhouse: core route under apps/api/src/routes (endpoint comment block,
  chained new Hono<AppEnv>(), guards, db services, one line in mountRoutes) or a plugin route under
  plugins/<id>/api (defineExtension routes on /api/ext/<id>, or a dataSource instead of hand-written
  CRUD), then tests. Use for: add an endpoint / API / route, 加个接口, 新增 API, 加条路由, 写个
  endpoint. Red lines: chain the definition (statement-style drops it from AppType), no any in a
  response, never reorder mountRoutes, plugins import only @greenhouse/api/extension-kit.
---

# Add an API route

Source of truth: apps/api/src/AGENTS.md (routes, security, uploads) and EXTENDING.md (plugin routes and data sources). This skill is the order of work; on conflict those files win.

## Decide first
- Core or plugin: core owns identity, conversations, models, tools/runs, MCP/connectors, automations, Files, notifications, settings, plugin host and admin; everything else is a plugin under plugins/<id>/.
- Table-backed plugin entity: declare a dataSource instead of hand-written CRUD; the host generates guarded `/api/ext/<plugin>/entities/<entity>` REST with scopes, field policy and audit.
- Missing db service: do add-db-table first.
- Access level: internal (team + super), super only, or a feature flag; core feature flags are empty, flags come from plugins.

## Core route
- One resource per file: apps/api/src/routes/<resource>.ts, starting with an endpoint comment block (method, path, purpose per line).
- Chain the definition; statement-style `x.get(...)` drops endpoints from AppType, and factories never declare a `: Hono` return type.
```typescript
/**
 * Widgets — /api/widgets
 * GET  /api/widgets      list the caller's widgets
 * POST /api/widgets      create one
 */
import { Hono } from 'hono';
import { getDb } from '@greenhouse/db';
import { getAuthUser } from '../auth/middleware.js';
import type { AppEnv } from '../app-env.js';

const widgetRoutes = new Hono<AppEnv>()
  .get('/', async (c) => {
    const user = getAuthUser(c);
    return c.json({ widgets: await getDb().widgets.listByUser(user.id) });
  })
  .post('/', async (c) => {
    /* validate with zod, write through the service */
  });
export default widgetRoutes;
```
- Responses never contain `any`: one `any` field collapses the inferred response to never; give raw SQL rows a shape first.
- Mount it with one `.route('/api/<resource>', routes)` in mountRoutes() (apps/api/src/index.ts); its order has security meaning (OAuth first, public callbacks before wildcard role guards). Never reorder.
- `export type AppType` in index.ts is the typed route contract; keep it compiling instead of adding parallel types.
- Public paths go only through PUBLIC_PATHS / isPublicPath (auth/middleware.ts), each with a reason; /api/mcp… and /api/gateway… are owned prefixes.

## Guards
- Import from ../auth/middleware.js: requireSuper(), requireInternal(), requireRole('team', 'super'), requireFeature('<flag>'); read the caller with getAuthUser(c).
- `/api/x/*` does not match the bare `/api/x`: guard both, mount writes on a sub-path, or put `.use('*', requireInternal())` inside the router (search, refs, people, activity do).
- Feature checks in code use userHasFeature, never a raw user_features read; UI hiding never replaces a route check.

## Plugin route
- In plugins/<id>/api: `routes: [{ path: '/api/ext/<id>', app, guards: [requireFeature('<id>')] }]` inside defineExtension; the host applies guards to the path and its `/*` (mountExtensionRoutes in apps/api/src/plugin-host/boot.ts).
- Reference: plugins/example/api/routes.ts and plugins/example/api/index.ts.
- Import only @greenhouse/api/extension-kit (getDb, getExtensionServices, getAuthUser, guards, AppEnv, humanActor, recordWrite, notify, logger …), shared types and own files.
- New routes use /api/ext/<id>; official packages keep their legacy prefixes; aliases cannot replace core routes.
- Protected writes go through the platform runtime (runtime.dispatch) or recordWrite; do not build a parallel permission or audit path.
- Writes reject unknown, immutable or forbidden fields atomically, even for super; ids and storage timestamps are never caller input.
- Callback or webhook exceptions go in publicPaths with a reason; throttling in rateLimits.
- Plugin routes are not part of AppType.

## Implementation rules
- Data only through `getDb().<domain>.<method>()` (plugins: their service bag); no SQL in routes.
- Log with `logger.info/warn/error` (@greenhouse/utils/logger); console.* only in cli/.
- Model-bound user input passes sanitizeForPrompt() (security/security.ts).
- Rate limits use checkRateLimit (security/security.ts); client IPs come only from security/request-ip.ts.
- Uploads verify MIME with validateMagicBytes() and store only through storage/uploads.ts.
- Never fetch a model-supplied URL directly: fetchPublicImage() / fetchPublicPage() (security/network.ts).
- Errors are `{ error: '<words>' }`, name the next step and quote interpolated values: `(ID: "${id}")`.
- Writes record the acting user; paid calls go through usage/metering.ts.
- A client that starts calling the new endpoint raises MOBILE_API_LEVEL (routes/bootstrap.ts) with the client's MOBILE_API.

## Tests
- Route and permission tests: tests/api/ or apps/api/src/routes/__tests__/; real-DB cases are `*.db.test.ts` (transaction rolled back per test).
- Plugin route tests sit beside the plugin (plugins/<id>/api/__tests__/); cover enabled and disabled, denials and field rejection.
- Auth, isolation and escalation cases go to tests/e2e/*.e2e.test.ts (`pnpm test:e2e:ci`, real HTTP against a dead LLM endpoint).
- Build fixtures from returned ids; never assume fixed ids.

## Gate
```bash
pnpm typecheck
pnpm lint
TEST_DATABASE_URL=<loopback test db> pnpm test
DATABASE_URL=<loopback e2e db> pnpm test:e2e:ci   # when auth, permissions or isolation changed
```

## Checklist
- [ ] Core vs plugin decided; data source considered for plugin CRUD
- [ ] Endpoint comment block; chained definition; no `: Hono` annotation; no any in responses
- [ ] Guards right, bare path covered; public path registered with a reason if any
- [ ] Mounted in mountRoutes() without reordering (core) or via defineExtension routes (plugin)
- [ ] Services, logger, sanitizeForPrompt, rate limit and network helpers used
- [ ] Error text names the next step and quotes values
- [ ] Tests at the right layer; gate green
