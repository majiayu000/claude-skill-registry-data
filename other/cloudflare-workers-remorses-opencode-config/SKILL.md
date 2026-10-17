---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: cloudflare-workers
description: >
  Cloudflare Workers and Durable Objects conventions for TypeScript projects.
  Covers wrangler.jsonc configuration, type-safe env via `wrangler types` and
  `import { env } from 'cloudflare:workers'`, secrets.required for typed secrets,
  custom_domain for routing, preview/production environments, deploy scripts,
  Durable Objects with SQLite, Spiceflow as the web framework with Vite,
  WebSocket close codes on Durable Objects (1006 isolate kill, always reconnect),
  and Durable Object OOM detection (exceededMemory vs scriptThrewException,
  clientDisconnected, responseStreamDisconnected) plus heap profiling.
  ALWAYS load this skill when a project uses wrangler, Cloudflare Workers,
  Durable Objects, or deploys to Cloudflare. Load it before writing any
  wrangler config, worker code, deploy scripts, or Durable Object WebSocket clients.
  Load durable-object-memory.md when counting OOMs, splitting DO invocation
  errors, taking heap snapshots, or reducing isolate RSS.
---

# Cloudflare Workers

Conventions for Cloudflare Workers and Durable Objects in TypeScript projects.

## Framework: Spiceflow with Vite + @cloudflare/vite-plugin

Always use Spiceflow as the web framework for Workers. Load the `spiceflow` skill first — it has the full API reference and conventions.

```ts
// vite.config.ts
import { cloudflare } from '@cloudflare/vite-plugin'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import spiceflow from 'spiceflow/vite'

export default defineConfig({
  plugins: [
    react(),
    spiceflow({ entry: './src/app.tsx' }),
    cloudflare({
      viteEnvironment: {
        name: 'rsc',
        childEnvironments: ['ssr'],
      },
    }),
  ],
})
```

Entry file is always `src/app.tsx` — uses JSX for `.page()` routes. The entry file also exports the Cloudflare Worker `default` fetch handler and any DO class re-exports. **No separate `worker.ts` file** — the app.tsx IS the worker entry.

```jsonc
// wrangler.jsonc — main points to your app entry file
{
  "main": "./src/app.tsx"
}
```

```tsx
// src/app.tsx — export DO classes and default fetch handler alongside the app
import { Spiceflow } from 'spiceflow'
import { env } from 'cloudflare:workers'

export { MyStore } from './my-store.ts'

export const app = new Spiceflow()
  .page('/', async () => <h1>Home</h1>)
  // ... routes

// Access env via `import { env } from 'cloudflare:workers'` anywhere — no need
// for .state('env') or threading env through handle(). The import works in any
// file, not just the fetch handler.
export default {
  async fetch(request: Request): Promise<Response> {
    return app.handle(request)
  },
} satisfies ExportedHandler<Env>
```

## Background tasks with `waitUntil`

All background promises (fire-and-forget work like analytics, logging, cache writes, webhook processing) MUST use `waitUntil`. Never do `void somePromise()` or `somePromise().catch(...)` directly; the Workers runtime kills the isolate as soon as the response is sent, so untracked promises are silently dropped.

**Inside a spiceflow route or middleware**, use `waitUntil` from the handler context:

```ts
export const app = new Spiceflow().route({
  method: 'POST',
  path: '/webhook',
  async handler({ request, waitUntil }) {
    const payload = await request.json()
    waitUntil(processWebhookInBackground(payload))
    return { ok: true }
  },
})
```

**Outside a route** (e.g. inside a Durable Object, a utility function, or the top-level fetch handler), import `waitUntil` from `cloudflare:workers`:

```ts
import { waitUntil } from 'cloudflare:workers'

async function doSomething() {
  waitUntil(trackEvent('something_happened'))
}
```

## Configuration: wrangler.jsonc

Always use `wrangler.jsonc` (not `wrangler.toml`). Newer features are exclusive to the JSON format.

### compatibility_date: ALWAYS use today's date

**MUST:** Always set `compatibility_date` to today's date minus 30 days (we can't use today's date directly because the wrangler version used should also released after that day or it will show an error) when creating a new worker or updating an existing one. Old dates disable newer runtime features like `WeakRef`, `FinalizationRegistry`, and other JS globals — causing cryptic "X is not defined" errors at runtime. There is no benefit to using an old date unless you are pinning behavior for a production worker you cannot test.

```jsonc
{
  // GOOD — use today's date (2026-04-14 or later)
  "compatibility_date": "2026-04-14",

  // BAD — disables WeakRef, FinalizationRegistry, and other modern APIs
  // "compatibility_date": "2025-01-01"
}
```

### Fetching your own domain: `global_fetch_strictly_public`

**A Worker on a custom domain cannot `fetch()` its own hostname by default.** A same-zone subrequest skips the Worker and goes to the (missing) origin, so it fails. `wrangler dev` hides this: it works locally and breaks only once deployed.

This hits libraries that call their own server over HTTP, e.g. better-auth `requireMcpAuth` fetching `/api/auth/jwks` ("Jwks failed: <none>"). Add the flag so the subrequest goes out to the public internet and back into the Worker:

```jsonc
{
  // requireMcpAuth fetches this Worker's own /api/auth/jwks
  "compatibility_flags": ["nodejs_compat", "global_fetch_strictly_public"]
}
```

Add it to every environment that overrides `compatibility_flags`. When the code is yours, call the handler in process instead (`app.handle(request)` or a service binding); use the flag when a dependency does the fetch.

### TCP sockets cannot reach Cloudflare IPs

**`connect()` from `cloudflare:sockets` fails for any host behind Cloudflare** (claude.ai, most SaaS, trycloudflare tunnels). Use `fetch` for HTTP. Do not hand-roll HTTP over a pinned-IP socket for SSRF safety: Worker subrequests already leave from Cloudflare's edge, which cannot reach private networks. `wrangler dev` uses your machine's network, so this also breaks only after deploy. https://developers.cloudflare.com/workers/runtime-apis/tcp-sockets/

**Test outbound calls on a deployed preview**, with `wrangler tail --env preview` open: both traps above pass locally.

## Type-safe environment

### Generate types with `wrangler types`

`wrangler types` generates a `worker-configuration.d.ts` file with a typed `Env` interface derived from your `wrangler.jsonc` bindings. This replaces `@cloudflare/workers-types` entirely.

```bash
# Add to package.json scripts
"types": "wrangler types"
```

**After generating types:**
1. **Uninstall** `@cloudflare/workers-types` — it conflicts with generated runtime types
2. **Install** `@types/node` if using `nodejs_compat`
3. **Include** `worker-configuration.d.ts` in tsconfig:

```json
{
  "compilerOptions": {
    "types": []
  },
  "include": ["src", "worker-configuration.d.ts"]
}
```

4. **Rerun** `wrangler types` every time you change `wrangler.jsonc`

### NEVER define custom Env types

The generated `worker-configuration.d.ts` declares a global `Env` interface. Never create your own `Env` type or interface. All bindings, vars, and secrets are available on `Env` automatically.

```ts
// BAD — never do this
export interface Env {
  MY_KV: KVNamespace
  API_KEY: string
}

// GOOD — Env is global from worker-configuration.d.ts
// Just use it directly in your code
export class MyDO extends DurableObject<Env> { ... }

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) { ... }
} satisfies ExportedHandler<Env>
```

### Importing common types

The generated types include all Cloudflare runtime types. Import only from `cloudflare:workers` for Worker-specific classes:

```ts
// DurableObject base class
import { DurableObject } from 'cloudflare:workers'

// For accessing env from anywhere (not just fetch handler)
import { env } from 'cloudflare:workers'
```

All other types are available globally from the generated file — `DurableObjectState`, `DurableObjectStorage`, `KVNamespace`, `ExecutionContext`, `ExportedHandler`, `DurableObjectNamespace`, `DurableObjectStub`, etc. No imports needed.

```ts
import { env } from 'cloudflare:workers'

// Access env from the cloudflare:workers import — no function params needed.
// Note: wrangler generates DurableObjectNamespace without a generic param,
// so do NOT annotate the return type with DurableObjectStub<MyDO> — just
// let TypeScript infer it. Fix with env.d.ts augmentation (see below).
function getStub() {
  const id = env.MY_STORE.idFromName('main')
  return env.MY_STORE.get(id)
}

export default {
  async fetch(request: Request): Promise<Response> {
    const stub = getStub()
    // Call named RPC methods — do NOT use stub.fetch()
    return stub.handleRequest(request)
  },
} satisfies ExportedHandler<Env>
```

### Avoid overriding fetch() on Durable Objects

Prefer **named RPC methods** over overriding `fetch()` on DOs. RPC methods are type-safe, self-documenting, and avoid the legacy fetch-based routing pattern.

```ts
// GOOD — named RPC methods
export class MyStore extends DurableObject<Env> {
  async handleRequest(request: Request): Promise<Response> { ... }
  async hranaHandler(request: Request): Promise<Response> { ... }
  async restore(timestamp: number) { ... }
}

// BAD — overriding fetch()
export class MyStore extends DurableObject<Env> {
  async fetch(request: Request): Promise<Response> { ... }
}
```

The worker calls `stub.handleRequest(request)` or `stub.hranaHandler(request)` directly — clear what each method does, and TypeScript checks the call.

### Fixing DurableObjectNamespace generics

`wrangler types` generates `DurableObjectNamespace` without the generic type param, so the stub type is `DurableObjectStub<undefined>` — RPC methods are invisible. Interface augmentation doesn't work because the existing property type wins in the intersection.

Fix with a typed helper that casts the stub return:

```ts
// src/get-stub.ts
import { env } from 'cloudflare:workers'
import type { MyStore } from './my-store.ts'

export function getStub() {
  const id = env.MY_STORE.idFromName('main')
  return env.MY_STORE.get(id) as DurableObjectStub<MyStore>
}
```

Import and call `getStub()` instead of accessing `env.MY_STORE` directly.

## Secrets

### Declare secrets in wrangler.jsonc

Use `secrets.required` to declare secrets. This makes `wrangler types` generate typed `string` properties on `Env`, and `wrangler deploy` validates they are set.

```jsonc
{
  "secrets": {
    "required": ["API_KEY", "DB_PASSWORD", "AUTH_SECRET"]
  }
}
```

After adding secrets, rerun `wrangler types`. The generated `Env` will include:

```ts
interface Env {
  API_KEY: string;
  DB_PASSWORD: string;
  AUTH_SECRET: string;
  // ... other bindings
}
```

### Local development: use Doppler, not `.env`

Do **not** use checked-in `.env` files for Worker local development in this workspace. Use Doppler to inject local env vars and secrets into `wrangler dev` / `vite dev` instead.

Wrangler local dev now loads local dev vars from `.env` files or the process environment, so `doppler run` works fine for local Worker runtime bindings. Keep `secrets.required` in `wrangler.jsonc` so local dev only loads the keys the Worker actually expects.

```bash
# Local wrangler dev
doppler run -c development -- wrangler dev

# Local vite dev against preview env
CLOUDFLARE_ENV=preview doppler run -c preview -- vite dev

# Preview build + deploy
CLOUDFLARE_ENV=preview doppler run -c preview -- vite build && wrangler deploy --env preview
```

Add **`CLOUDFLARE_INCLUDE_PROCESS_ENV=true`** to your Doppler config so wrangler automatically picks up all Doppler-injected env vars as Worker bindings during local dev. Without it, `doppler run` populates `process.env` but wrangler ignores those values. Sigillo (`sigillo run`) sets this automatically; Doppler requires it to be added manually.

Rules:

- **Prefer Doppler over `.env` / `.dev.vars`** for local development.
- **Put shell env vars before `doppler run`, never after.**
- **Add `CLOUDFLARE_INCLUDE_PROCESS_ENV=true`** in Doppler so wrangler sees the injected env vars.
- Read runtime values from `import { env } from 'cloudflare:workers'`, not `process.env`, even though `process.env` may be populated under `nodejs_compat`.

### Upload secrets from Doppler to Cloudflare

Cloudflare Workers store their own deployed secret values. Local `doppler run` is only for local development — it does **not** upload secrets to Cloudflare. Sync them explicitly with `wrangler secret bulk`.

```json
{
  "scripts": {
    "secrets:preview": "doppler run -c preview --mount .env.preview --mount-format env -- wrangler secret bulk --env preview .env.preview",
    "secrets:prod": "doppler run -c production --mount .env.prod --mount-format env -- wrangler secret bulk .env.prod"
  }
}
```

Run these whenever Worker secrets change:

```bash
pnpm secrets:preview
pnpm secrets:prod
```

Do **not** loop over `wrangler secret put` one key at a time. It is interactive and hangs in scripts. Always use `wrangler secret bulk`.

### First deploy: secrets chicken-and-egg

`wrangler secret bulk` and `wrangler secret put` require the worker to already have at least one deployed version. But `wrangler deploy` with `secrets.required` refuses to deploy if secrets aren't set yet. This creates a chicken-and-egg problem on first deploy.

**Fix:** use `--secrets-file` on the first deploy. This flag passes secrets inline during deploy, creating the worker and setting secrets in one shot. No need to temporarily remove `secrets.required`.

Use `sigillo run --mount` to write secrets to a temp file that only exists while the command runs. The `--mount-format env` flag writes a `KEY=value` file that `--secrets-file` expects:

```bash
# Preview — sigillo mounts secrets as a temp .env file, wrangler reads it
sigillo run -c preview \
  --mount /tmp/pw-secrets.env --mount-format env \
  -- wrangler deploy --env preview --secrets-file /tmp/pw-secrets.env

# Production
sigillo run -c prod \
  --mount /tmp/pw-secrets.env --mount-format env \
  -- wrangler deploy --secrets-file /tmp/pw-secrets.env
```

The mounted file is created before the command starts and cleaned up after it exits. Secrets never stay on disk.

For the full build + deploy chain, combine `--mount` with `--command` so vite build and wrangler deploy share the same sigillo session:

```bash
CLOUDFLARE_ENV=preview sigillo run -c preview \
  --mount /tmp/pw-secrets.env --mount-format env \
  --command 'vite build && wrangler deploy --env preview --secrets-file /tmp/pw-secrets.env'
```

After the first deploy, subsequent deploys work normally because the worker and its secrets already exist. `wrangler secret bulk` also works from this point on for updating secrets.

### Production / preview secret values

```bash
# Set for production
wrangler secret put API_KEY
wrangler secret put API_KEY --env preview
```

Prefer the bulk upload scripts above over manual `secret put` commands.

## KV operations: always use `--remote`

**`wrangler kv` commands default to local storage**, not the deployed remote KV. If you `kv key list`, `kv key get`, or `kv key put` without `--remote`, you're reading/writing to a local SQLite file that the deployed worker never sees. This causes confusing debugging sessions where writes appear to succeed but data seems missing.

```bash
# BAD — reads/writes local storage only
wrangler kv key list --namespace-id abc123
wrangler kv key get --namespace-id abc123 "my-key"
wrangler kv key put --namespace-id abc123 "my-key" "value"

# GOOD — reads/writes the actual deployed KV
wrangler kv key list --namespace-id abc123 --remote
wrangler kv key get --namespace-id abc123 "my-key" --remote
wrangler kv key put --namespace-id abc123 "my-key" "value" --remote
```

When debugging whether a Worker's KV writes are persisting, always use `--remote` on the verification commands. The Worker itself always writes to the remote KV; only the wrangler CLI defaults to local.

### KV consistency model

- **`KV.get()`** is strongly consistent in the datacenter that wrote the key. Cross-datacenter reads are eventually consistent (up to 60s).
- **`KV.list()`** is always eventually consistent, even in the same datacenter. Recently written keys may not appear for several seconds.
- Use `KV.getWithMetadata(key)` (checking `value !== null`) instead of `KV.list()` when verifying that specific keys exist after writing them.

## Dynamic workers with LOADER

See ./dynamic-workers.md

## CORS for static assets

Cloudflare Workers Static Assets are served by the CDN **before** Worker code runs. CORS headers set in Worker code don't apply to static files. This breaks cross-origin `<canvas>` image drawing, `@font-face` loading, and `fetch()` reads from other origins.

Fix: create a `public/_headers` file (Vite copies it to the build output, which becomes `assets.directory`):

```
/*
  Access-Control-Allow-Origin: *
```

Cloudflare reads `_headers` and applies the rules to all static asset responses. The file itself is not served. See [Cloudflare headers docs](https://developers.cloudflare.com/workers/static-assets/headers/).

## Importing non-JS files as text

For things like `.txt`, `.md`, and `.sql`, tell Wrangler/Vite to import them as text with `rules`, then add a TypeScript declaration file. Do **not** silence the import with `// @ts-expect-error`.

```jsonc
{
  "rules": [
    { "type": "Text", "globs": ["**/*.sql"], "fallthrough": true },
    { "type": "Text", "globs": ["**/*.md", "**/*.txt"], "fallthrough": true }
  ]
}
```

```ts
// src/import-text.d.ts
declare module '*.sql' {
  const content: string
  export default content
}

declare module '*.md' {
  const content: string
  export default content
}

declare module '*.txt' {
  const content: string
  export default content
}
```

```ts
import schemaSql from './schema.sql'
import promptMd from './prompt.md'
import fixtureTxt from './fixture.txt'
```

Use a real `declare module` file so TypeScript understands the import shape. Never paper over missing module types with `@ts-expect-error`.

## Routing: prefer custom_domain when you actually need routing

Do **not** add `routes` / `custom_domain` entries just because a project uses Spiceflow, Vite, or `@cloudflare/vite-plugin`. Spiceflow does not need wrangler routing rules to run, build, or deploy, and Vite does not need them either.

Only add `routes` when you are intentionally binding a real hostname to the worker. If you do need that, prefer `custom_domain` instead of path-based `routes`. Custom domains work without needing a proxied A/AAAA DNS record first — Cloudflare creates it automatically.

```jsonc
{
  // GOOD — custom_domain, no DNS setup needed
  "routes": [
    { "pattern": "api.example.com", "custom_domain": true },
    { "pattern": "api.preview.example.com", "custom_domain": true, "zone_name": "example.com" }
  ]

  // BAD — requires pre-existing proxied DNS record
  // "routes": [
  //   { "pattern": "api.example.com/*", "zone_name": "example.com" }
  // ]
}
```

Use `routes` (non-custom_domain) only when you need path-based routing (`example.com/api/*`) on a domain that already has another worker or Pages project on the root.

If a Worker has no named environments and uses only `*.workers.dev`, leave
`routes` out entirely. A named preview environment is different: `routes` is
an inherited Wrangler property. If production defines routes and preview
should use workers.dev, preview must override them with `"routes": []`.

## Environments: preview and production

Every project has two environments. Preview is the default for development and testing.

### wrangler.jsonc structure

**Critical: bindings are NOT inherited by environments.** Wrangler environments do not inherit `durable_objects`, `kv_namespaces`, `secrets`, `r2_buckets`, etc. from the top level. You MUST duplicate all bindings in both top-level (production) and `env.preview`. If you don't, `wrangler types` generates optional (`?`) types for bindings that only exist in one environment, causing `possibly undefined` errors everywhere.

Keep binding names, Durable Object classes, secret names, and migration shapes
consistent so generated `Env` types stay stable. Environment values, routes,
and physical resource identifiers should differ where isolation requires it.

**Routes behave in the opposite way: they ARE inherited.** If top-level
production owns `app.example.com` and `env.preview` omits `routes`, then
`wrangler deploy --env preview` attempts to reassign that production domain to
the preview Worker. Wrangler prints a warning before doing this. Treat that
warning as a deployment blocker, never as informational output.

Use one of these explicit preview configurations:

```jsonc
// workers.dev preview — disable inherited production routes
"routes": []

// dedicated preview hostname
"routes": [
  { "pattern": "app.preview.example.com", "custom_domain": true }
]
```

If preview accidentally takes a production domain, add the correct preview
`routes`, redeploy preview, then redeploy production so it reclaims its domain.

```jsonc
{
  "name": "my-worker",
  "compatibility_date": "2026-04-14",
  "compatibility_flags": ["nodejs_compat"],
  "main": "./src/app.tsx",

  // ── Production (top-level) ──────────────────────────────────
  "durable_objects": {
    "bindings": [{ "name": "MY_STORE", "class_name": "MyStore" }]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["MyStore"] }
  ],
  "vars": {
    "APP_URL": "https://app.example.com"
  },
  "secrets": {
    "required": ["API_KEY", "AUTH_SECRET"]
  },
  // Optional: only add this when you want a custom hostname.
  "routes": [
    { "pattern": "app.example.com", "custom_domain": true }
  ],

  // ── Preview ─────────────────────────────────────────────────
  // Must duplicate ALL bindings, secrets, migrations
  "env": {
    "preview": {
      "name": "my-worker-preview",
      "durable_objects": {
        "bindings": [{ "name": "MY_STORE", "class_name": "MyStore" }]
      },
      "migrations": [
        { "tag": "v1", "new_sqlite_classes": ["MyStore"] }
      ],
      "vars": {
        "APP_URL": "https://app.preview.example.com"
      },
      "secrets": {
        "required": ["API_KEY", "AUTH_SECRET"]
      },
      // Use [] for workers.dev, or list a distinct preview hostname.
      "routes": []
    }
  }
}
```

Preview bindings must also point at **isolated resources**. Create separate KV
namespaces, R2 buckets, and D1 databases instead of copying production IDs or
bucket names into `env.preview`. Matching binding names keep `Env` types stable;
different resource identifiers keep preview tests away from production data.

### Deploy scripts

The `@cloudflare/vite-plugin` resolves and flattens your `wrangler.jsonc` at **build time** and writes it into `dist/rsc/wrangler.json`. Set `CLOUDFLARE_ENV` during `vite build` so the plugin resolves the correct environment section:

`wrangler deploy` deploys **one environment at a time**. It does **not** deploy every configured `env.*` block. With no `--env` flag, Wrangler deploys the top-level/default config (usually production). Use `wrangler deploy --env preview` or another explicit env name when targeting a non-production environment.

> **IMPORTANT: Cloudflare D1 does NOT auto-apply migrations on deploy.** If you deploy new worker code that references columns or tables from a pending migration, the worker will crash with "no such table" or "no such column" errors. Always run D1 migrations before deploying. Bake them into the deploy scripts so they can't be skipped.

> **Always deploy preview first, then production.** D1 migrations can fail (bad SQL, constraint violations on existing data) and there is no automatic rollback. Running against preview first catches these failures safely. If the preview migration or deploy fails, **stop**. Do not continue to production.

For projects using D1, bake migrations into the deploy chain. The remote migration scripts print a unix timestamp before running so you can restore via D1 time travel if something goes wrong:

```json
{
  "scripts": {
    "deploy": "pnpm db:migrate:preview && tsc && CLOUDFLARE_ENV=preview vite build && wrangler deploy --env preview",
    "deploy:prod": "pnpm db:migrate:prod && tsc && vite build && wrangler deploy"
  }
}
```

If a migration corrupts data, use the printed timestamp to restore:

```bash
wrangler d1 time-travel restore DB --timestamp=<unix_timestamp>
wrangler d1 time-travel restore DB --timestamp=<unix_timestamp> --env preview
```

For projects without D1 (no migrations needed):

```json
{
  "scripts": {
    "deploy": "tsc && CLOUDFLARE_ENV=preview vite build && wrangler deploy --env preview",
    "deploy:prod": "tsc && vite build && wrangler deploy"
  }
}
```

- `pnpm run deploy` → migrates + builds for preview env, deploys to **preview** (safe default)
- `pnpm run deploy:prod` → migrates + builds for production, deploys to **production**

Always include `run` for package scripts. `pnpm deploy` is pnpm's own built-in
deployment command and does not reliably invoke a `"deploy"` script.

**Preview is the default deploy target.** This prevents accidental production deploys. Production deploys should be deliberate.

Deployment sequence for D1 projects:

```bash
# 1. Deploy preview (migration + build + deploy)
pnpm run deploy

# 2. Verify preview works (load the page, hit health endpoint, check logs)

# 3. Deploy production
pnpm run deploy:prod
```

### Secrets per environment

Secrets are set per environment. Set them separately:

```bash
# Preview
wrangler secret put API_KEY --env preview

# Production
wrangler secret put API_KEY
```

### Using preview for integration tests

Preview environments are useful for tests that depend on Cloudflare infrastructure (Durable Objects, KV, R2, etc.) which can't be fully emulated locally.

```ts
// test/integration.test.ts
import { describe, test, expect } from 'vitest'

const PREVIEW_URL = 'https://app.preview.example.com'

describe('integration', () => {
  test('health check', async () => {
    const res = await fetch(`${PREVIEW_URL}/health`)
    expect(res.status).toBe(200)
    const body = await res.json()
    expect(body).toEqual({ ok: true })
  })

  test('auth flow redirects to provider', async () => {
    const res = await fetch(`${PREVIEW_URL}/api/auth/sign-in/social?provider=sigillo`, {
      redirect: 'manual',
    })
    expect(res.status).toBe(302)
    expect(res.headers.get('location')).toContain('auth.sigillo.dev')
  })
})
```

Deploy to preview first, then run tests against it:

```bash
pnpm run deploy && pnpm vitest --run test/integration.test.ts
```

## Testing with Vitest inside workerd

Tests run **inside the real workerd runtime** via `@cloudflare/vitest-pool-workers`. This means `env`, `waitUntil`, D1, KV, R2, Durable Objects — all Cloudflare APIs work in tests without mocks. Miniflare simulates every binding locally as in-memory state; no real Cloudflare infrastructure is needed.

### vite.config.ts setup

The key pattern: swap between `cloudflareTest()` (tests) and `cloudflare()` (dev/build) based on `process.env.VITEST`. Both can live in the same `vite.config.ts`.

```ts
// vite.config.ts
import path from 'node:path'
import { cloudflare } from '@cloudflare/vite-plugin'
import { cloudflareTest, readD1Migrations } from '@cloudflare/vitest-pool-workers'
import spiceflow from 'spiceflow/vite'
import { defineConfig } from 'vite'

export default defineConfig(async () => {
  // readD1Migrations runs on the Node.js side before workerd starts.
  // Passes SQL file contents to miniflare as TEST_MIGRATIONS so the
  // setup file can apply them inside workerd.
  const migrations = await readD1Migrations(path.join(__dirname, 'migrations')).catch(() => [])

  return {
    plugins: [
      process.env.VITEST
        ? cloudflareTest({
            wrangler: { configPath: './wrangler.jsonc' },
            miniflare: {
              // TEST_MIGRATIONS is a test-only binding — not in wrangler.jsonc
              bindings: { TEST_MIGRATIONS: migrations },
            },
          })
        : cloudflare({
            viteEnvironment: { name: 'rsc', childEnvironments: ['ssr'] },
          }),
      spiceflow({ entry: './src/main.tsx' }),
    ],
    test: {
      setupFiles: ['./src/apply-migrations.ts'],
    },
  }
})
```

If you have no D1, omit `readD1Migrations` and the `miniflare.bindings` option entirely.

### Applying D1 migrations before tests

Create a setup file that runs inside workerd before each test file:

```ts
// src/apply-migrations.ts
import { applyD1Migrations } from 'cloudflare:test'
import { env } from 'cloudflare:workers'

// Idempotent — tracks applied migrations, safe to call multiple times.
await applyD1Migrations(env.DB, env.TEST_MIGRATIONS)
```

Add `TEST_MIGRATIONS` to your type declarations so `env.TEST_MIGRATIONS` is typed:

```ts
// src/env.d.ts
declare namespace Cloudflare {
  interface Env {
    TEST_MIGRATIONS: D1Migration[]
  }
}

interface D1Migration {
  name: string
  queries: string[]
}
```

### Storage isolation model

**All storage** (D1, KV, R2, Durable Objects) follows the same isolation model:

- **Per test file** — each file gets a fresh storage snapshot; writes are invisible to other files
- **Shared within a file** — tests within the same file see each other's writes
- **Automatic reset** — workerd uses an on-disk SQLite snapshot stack: "pushes" a fresh snapshot at file start, "pops" it at file end, discarding all writes

This means setup files like `apply-migrations.ts` run once per test file, applying migrations to a fresh in-memory DB each time.

**Durable Objects** follow the same per-file isolation. DO instances created in one file don't exist in another. `listDurableObjectIds(namespace)` only returns IDs created within the current file's storage context.

```
pnpm test
│
├─ users.test.ts                   ├─ posts.test.ts
│   Fresh D1 + fresh DO storage        Fresh D1 + fresh DO storage
│   ├─ setup: apply migrations          ├─ setup: apply migrations
│   ├─ test 1 writes D1/DO              ├─ test 1 writes D1/DO
│   └─ test 2 sees test 1's state       └─ test 2 sees test 1's state
│   (file ends → all state discarded)  (file ends → all state discarded)
│
│   Files run concurrently. Each sees only its own storage.
```

**If you need per-test isolation within a file:** clean up manually in `beforeEach`/`afterEach` (e.g. `DELETE FROM table` or `env.KV.delete(key)`).

**If you need shared state across files** (e.g. integration tests with accumulated data): run with `--max-workers=1 --no-isolate`.

**WebSockets + Durable Objects** don't work with per-file isolation. Use `--max-workers=1 --no-isolate` as a workaround.

### Key test APIs

**From `cloudflare:workers`:**

| Import | Purpose |
|---|---|
| `env` | All bindings from `wrangler.jsonc` — typed via `Cloudflare.Env` |
| `waitUntil` | Register background promises (same as `ctx.waitUntil`) |
| `exports` | Access `exports.default.fetch()` to hit the Worker handler directly |

**From `cloudflare:test`:**

| Import | Purpose |
|---|---|
| `applyD1Migrations(db, migrations)` | Apply SQL migration files to a D1 binding |
| `runInDurableObject(stub, callback)` | Run a callback inside a DO instance — inspect state, call methods |
| `runDurableObjectAlarm(stub)` | Immediately fire a scheduled DO alarm |
| `listDurableObjectIds(namespace)` | List all DO IDs created in the current file's storage context |
| `createExecutionContext()` | Create a `ctx` object for passing to raw worker handlers |
| `waitOnExecutionContext(ctx)` | Wait for all `ctx.waitUntil()` promises to settle |

For the full reference including Queues, Workflows, and Scheduled handlers, see [Cloudflare Workers Vitest test APIs](https://developers.cloudflare.com/workers/testing/vitest-integration/test-apis/).

## WebSocket close codes on Durable Objects

See ./websocket-close-codes.md

**1006** means the isolate died with no Close frame (OOM, CPU, throw, deploy). Always reopen the WebSocket. Hibernation does not drop sockets; shutdown does. 1006 does not prove an OOM.

## Durable Object memory and OOMs

See ./durable-object-memory.md

The isolate heap limit is **128 MB**. The only production OOM signal is invocation status **`exceededMemory`**. Split other errors by status first: `scriptThrewException`, `clientDisconnected`, `responseStreamDisconnected`. Then group stored exceptions by `$metadata.errorTemplate`. Profano is for CPU profiles, not heap snapshots.

## Durable Objects with SQLite

See the `drizzle` skill for full schema and migration conventions. Key wrangler config:

```jsonc
{
  "rules": [
    { "type": "Text", "globs": ["**/*.sql"], "fallthrough": true }
  ],
  "durable_objects": {
    "bindings": [
      { "name": "MY_STORE", "class_name": "MyStore" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["MyStore"] }
  ]
}
```

The `rules` entry is required for drizzle DO migrations — imports `.sql` files as text.

### Usage counter pattern (exact billing / rate limiting)

For exact per-entity counters (API call tracking, usage-based billing, hard rate limits), use a Durable Object with SQLite storage. Each entity (project, user, org) gets its own DO instance via `idFromName()`, so counters are isolated and increments are atomic SQL statements with no read-modify-write races.

**Full implementation:** copy `./usage-counter-do.ts` (bundled with this skill) into your project. No external dependencies.

Usage is stored as append-only event rows with timestamps, so you can query any time window (current billing month, last 7 days, all time). Totals are derived by summing rows.

```ts
import { env } from 'cloudflare:workers'
import type { UsageCounter } from './usage-counter-do.ts'

function getUsageStub(projectId: string) {
  const id = env.USAGE_COUNTER.idFromName(projectId)
  return env.USAGE_COUNTER.get(id) as DurableObjectStub<UsageCounter>
}

// Record usage events
await getUsageStub('proj_123').record('api-calls')
await getUsageStub('proj_123').record('tokens', 1500)

// Query totals for a billing window
const monthStart = new Date('2026-07-01').getTime()
const apiCalls = await getUsageStub('proj_123').getTotalSince('api-calls', monthStart)
const breakdown = await getUsageStub('proj_123').getBreakdownSince(monthStart)

// Prune old events to keep storage small
const threeMonthsAgo = Date.now() - 90 * 24 * 60 * 60 * 1000
await getUsageStub('proj_123').pruneOlderThan(threeMonthsAgo)
```

The DO hibernates after 10s of inactivity, so each write only costs the few ms of execution time. At $0.15/million requests and negligible duration, this is much cheaper than KV ($5/million writes) and fully atomic unlike KV's eventually-consistent read-modify-write.

For **approximate** usage tracking (dashboards, analytics), use Analytics Engine instead. It handles sampling and high cardinality but doesn't give exact counts.

## Memoizing slow operations with the Cache API

Workers run globally on 300+ datacenters, but your database (D1, Postgres, etc.) lives in one region. Cross-region reads can be 50-200ms. Use the Cache API (`caches.default`) to memoize slow lookups at the edge so repeated reads from the same datacenter are ~1-5ms.

Each datacenter has its own independent cache. No cross-datacenter replication. First request to a datacenter is always a miss, subsequent requests are fast. This is ideal for data that changes rarely (auth checks, config, org membership, environment lookups).

The `memoize()` utility wraps any async function. Args are superjson-serialized and SHA-256 hashed into cache keys. Supports stale-while-revalidate: within the SWR window, stale values return immediately while a background refresh runs via `waitUntil()`. Cache keys include the spiceflow deployment id so stale entries from old builds are never served.

**Requires a custom domain.** Does NOT work on `*.workers.dev`.

**Full implementation:** copy `./worker-memoize.ts` (bundled with this skill) into your project as `lib/memoize.ts`. Dependencies: `superjson`, `cloudflare:workers`, `spiceflow`.

**Usage example — memoize auth and config lookups:**

```ts
import { memoize } from './lib/memoize.ts'

// Defaults: 5 min fresh TTL, 10 min stale-while-revalidate

// Org membership check — called on every request, changes rarely
const lookupOrgMember = memoize({
  namespace: 'org-member',
  fn: async (userId: string, orgId: string) => {
    const db = getDb()
    const member = await db.query.orgMember.findFirst({ where: { userId, orgId } })
    if (!member) return null // null = not cached
    return { role: member.role }
  },
})

// Project ownership — never changes
const getOrgIdForProject = memoize({
  namespace: 'project-org',
  fn: async (projectId: string) => {
    const db = getDb()
    const row = await db.query.project.findFirst({
      where: { id: projectId },
      columns: { orgId: true },
    })
    return row?.orgId ?? null // null = not cached
  },
})
```

**null, undefined, and Error results are never cached.** This prevents caching "not found" or "unauthorized" responses that would lock users out until the TTL expires. Memoized functions that indicate absence or failure MUST return null/undefined or throw. If a background SWR refresh returns null/Error, the stale cache entry is evicted so the next request hits the database.

**What to memoize vs skip:**

| Memoize | Skip |
|---|---|
| Auth/membership checks | Session validation (BetterAuth has its own cookieCache) |
| Org/project ownership lookups | Secrets (change frequently, stale = security risk) |
| OAuth client id by hostname | Encryption keys (CPU, not I/O) |
| Environment resolution (id/slug) | Write operations |

## Redirect chains multiply database latency

Every 302 hop is a full worker invocation: middleware, auth, and database reads run again. With D1 at 50-200ms per cross-region read, a two-hop chain doubles or triples time-to-content.

**Resolver routes** (e.g. `/dashboard` that resolves the user's tenant and redirects to `/org/:id/...`) exist only as stable entry points for external links where the final URL can't be known upfront: docs, emails, CLI error messages, OAuth `callbackURL`. Internal code must never redirect to a resolver; compute the final URL and redirect there in one hop.

```
/login (signed in) ──► /dashboard ──► /org/:id/posts     two hops, queries run twice
/login (signed in) ──► /org/:id/posts                    one hop
```

Audit the usual chain sources: "already signed in" bounces on login pages, stale-resource bounces in loaders, logo/home links pointing at the resolver, and signed-out pages linking to authed resolvers (which chain into `/login`).

## Remote bindings can crash the vite dev worker

With bindings like `send_email` set to `remote: true`, the dev worker sometimes dies with `Error: internal error; reference = ...` and the port stops accepting connections. This is a known flaky behavior. Restart the tuistory dev session; nothing is wrong with the code.

## Firing the cron handler locally

`@cloudflare/vite-plugin` exposes the `scheduled()` handler at a special path. Invoke it with:

```bash
curl -X POST "http://localhost:<port>/cdn-cgi/handler/scheduled?cron=*/5+*+*+*+*"
```

Replace `<port>` with your dev server port and the cron expression with the one you want to test.

## Always typecheck before building

**Always run `tsc` before `vite build`** in build and deploy scripts. Vite does not typecheck; it only transpiles. Without `tsc`, type errors slip through to production silently. The `build` script should be `tsc && vite build`, and deploy scripts should include `tsc &&` before the `vite build` step.

## package.json scripts

Standard scripts for a Worker package (with D1):

`CI=1` on every `wrangler d1 migrations apply`: without it, apply asks Y/n and blocks `pnpm dev` and deploy scripts.

```json
{
  "scripts": {
    "dev": "pnpm db:migrate:local && vite dev",
    "build": "tsc && vite build",
    "typecheck": "tsc",
    "types": "wrangler types",
    "db:migrate:local": "CI=1 wrangler d1 migrations apply DB --local",
    "db:migrate:prod": "echo \"D1 pre-migration timestamp: $(date +%s)\" && CI=1 wrangler d1 migrations apply DB --remote",
    "db:migrate:preview": "echo \"D1 pre-migration timestamp: $(date +%s)\" && CI=1 wrangler d1 migrations apply DB --remote --env preview",
    "deploy": "pnpm db:migrate:preview && tsc && CLOUDFLARE_ENV=preview vite build && wrangler deploy --env preview",
    "deploy:prod": "pnpm db:migrate:prod && tsc && vite build && wrangler deploy"
  }
}
```

Standard scripts for a Worker package (without D1):

```json
{
  "scripts": {
    "dev": "vite dev",
    "build": "tsc && vite build",
    "typecheck": "tsc",
    "types": "wrangler types",
    "deploy": "tsc && CLOUDFLARE_ENV=preview vite build && wrangler deploy --env preview",
    "deploy:prod": "tsc && vite build && wrangler deploy"
  }
}
```
