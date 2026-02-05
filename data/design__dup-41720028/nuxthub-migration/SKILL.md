---
name: nuxthub-migration
description: Use when migrating NuxtHub projects or when user mentions NuxtHub Admin sunset, GitHub Actions deployment removal, self-hosting NuxtHub, or upgrading to v0.10/nightly. Covers v0.9.X self-hosting (stable) and v0.10/nightly multi-cloud.
---

# NuxtHub Migration

## When to Use

Activate this skill when:
- User mentions NuxtHub Admin deprecation or sunset (Dec 31, 2025)
- Project uses `.github/workflows/nuxthub.yml` or NuxtHub GitHub Action
- User wants to self-host NuxtHub on Cloudflare Workers
- User asks about migrating to v0.10 or nightly version
- Project has `NUXT_HUB_PROJECT_KEY` or `NUXT_HUB_PROJECT_DEPLOY_TOKEN` env vars

Two-phase migration. Phase 1 is stable and recommended. Phase 2 is multi-cloud.

## Phase 1: Self-Hosting (v0.9.X) - RECOMMENDED

Migrate from NuxtHub Admin / GitHub Actions to self-hosted Cloudflare Workers. No code changes required.

### 1.1 Remove GitHub Action Deployment

Delete `.github/workflows/nuxthub.yml` or any NuxtHub-specific GitHub Action. Workers CI (step 1.4) replaces this.

Remove deprecated env vars from CI/CD and `.env`:
- `NUXT_HUB_PROJECT_KEY`
- `NUXT_HUB_PROJECT_DEPLOY_TOKEN`

Also remove any GitHub Actions secrets related to NuxtHub deployment.

Check and clean up Cloudflare Worker secrets:
```bash
npx wrangler secret list --name <worker-name>
npx wrangler secret delete NUXT_HUB_PROJECT_DEPLOY_TOKEN --name <worker-name>
```

### 1.2 Get or Create Cloudflare Resources

NuxtHub Admin already created resources in your Cloudflare account. **Reuse them to preserve existing data.**

List existing resources:
```bash
npx wrangler d1 list              # Find existing D1 databases
npx wrangler kv namespace list    # Find existing KV namespaces
npx wrangler r2 bucket list       # Find existing R2 buckets
```

Look for resources named after your project. Use their IDs in wrangler.jsonc.

Only create new resources if none exist:
```bash
# D1 Database (if hub.database: true)
npx wrangler d1 create my-app-db

# KV Namespace (if hub.kv: true)
npx wrangler kv namespace create KV

# KV Namespace for cache (if hub.cache: true)
npx wrangler kv namespace create CACHE

# R2 Bucket (if hub.blob: true)
npx wrangler r2 bucket create my-app-bucket
```

### 1.3 Create wrangler.jsonc

Create `wrangler.jsonc` in project root. See `references/wrangler-templates.md` for full examples.

Minimal example with database:
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-app",
  "main": "dist/server/index.mjs",
  "assets": { "directory": "dist/public" },
  "compatibility_date": "2025-12-01",
  "compatibility_flags": ["nodejs_compat"],
  "d1_databases": [{ "binding": "DB", "database_name": "my-app-db", "database_id": "<from-wrangler-output>" }]
}
```

> **Note**: Nuxt cloudflare-module preset outputs to `dist/`, not `.output/`.

Required binding names:
| Feature | Binding | Type |
|---------|---------|------|
| Database | `DB` | D1 |
| KV | `KV` | KV Namespace |
| Cache | `CACHE` | KV Namespace |
| Blob | `BLOB` | R2 Bucket |

### 1.4 Set Up Workers Builds CI/CD

Ensure `nuxt.config.ts` uses the `cloudflare_module` preset:
```ts
nitro: { preset: 'cloudflare_module' }
```

In Cloudflare Dashboard:
1. Workers & Pages → Create → Import from Git
2. Connect GitHub/GitLab repository
3. Configure build settings (**both fields required**):
   - **Build command**: `pnpm build` (or `npm run build`)
   - **Deploy command**: `npx wrangler deploy`
4. Add environment variables (e.g., secrets, API keys)

> **Common mistake**: Only setting deploy command. Build must run first to generate `.output/`.

### 1.5 Configure Environment Variables (Optional)

For advanced features (blob presigned URLs, cache DevTools, AI):

```bash
NUXT_HUB_CLOUDFLARE_ACCOUNT_ID=<account-id>
NUXT_HUB_CLOUDFLARE_API_TOKEN=<token-with-appropriate-permissions>
# Feature-specific (as needed):
NUXT_HUB_CLOUDFLARE_BUCKET_ID=<bucket-id>
NUXT_HUB_CLOUDFLARE_CACHE_NAMESPACE_ID=<namespace-id>
```

### 1.6 Test Remote Development

```bash
npx nuxt dev --remote
```

### Phase 1 Checklist

- [ ] Delete `.github/workflows/nuxthub.yml`
- [ ] Remove `NUXT_HUB_PROJECT_KEY` and `NUXT_HUB_PROJECT_DEPLOY_TOKEN` env vars
- [ ] Clean up old Worker secrets (`wrangler secret list/delete`)
- [ ] Get existing or create new Cloudflare resources (D1, KV, R2 as needed)
- [ ] Create `wrangler.jsonc` with bindings
- [ ] Set `nitro.preset: 'cloudflare_module'` in nuxt.config.ts
- [ ] Connect repo to Cloudflare Workers Builds
- [ ] Test with `npx nuxt dev --remote`

No code changes required. Keep `hub.database: true`, `server/database/`, `hubDatabase()`, and `@nuxthub/core`.

---

## Phase 2: v0.10/Nightly - MULTI-CLOUD

Multi-cloud support (Cloudflare, Vercel, Deno, Netlify). Breaking changes from v0.9.X.

### 2.1 Update Package

```bash
pnpm remove @nuxthub/core
pnpm add @nuxthub/core-nightly
```

### 2.2 Update nuxt.config.ts

**Before (v0.9.X):**
```ts
hub: { database: true, kv: true, blob: true, cache: true }
```

**After (v0.10):**
```ts
hub: { db: 'sqlite', kv: true, blob: true, cache: true }
```

Key change: `database: true` → `db: '<dialect>'` (`sqlite` | `postgresql` | `mysql`)

### 2.3 Rename Database Directory

```bash
mv server/database server/db
```

Update imports: `~/server/database/` → `~/server/db/`

Migrations generated via `npx nuxt db generate` go to `server/db/migrations/{dialect}/`.

### 2.4 Migrate Database API (hubDatabase → Drizzle)

**Before:**
```ts
const db = hubDatabase()
const users = await db.prepare('SELECT * FROM users').all()
```

**After:**
```ts
import { db, schema } from 'hub:db'
// Note: db and schema are auto-imported on server-side
const users = await db.select().from(schema.users)
```

### 2.5 Migrate KV API (hubKV → kv)

**Before:**
```ts
import { hubKV } from '#hub/server'
await hubKV().set('vue', { year: 2014 })
await hubKV().get('vue')
await hubKV().has('vue')
await hubKV().del('vue')
await hubKV().keys('vue:')
await hubKV().clear('vue:')
```

**After:**
```ts
import { kv } from 'hub:kv'
// Note: kv is auto-imported on server-side
await kv.set('vue', { year: 2014 })
await kv.get('vue')
await kv.has('vue')
await kv.del('vue')
await kv.keys('vue:')
await kv.clear('vue:')
```

Key change: `hubKV()` function call → `kv` direct object. Same methods, different access pattern.

### 2.6 Migrate Blob API (hubBlob → blob)

**Before:**
```ts
const blob = hubBlob()
await blob.put('file.txt', body, { contentType: 'text/plain' })
await blob.get('file.txt')
await blob.list({ prefix: 'uploads/' })
await blob.del('file.txt')
await blob.serve(event, 'file.txt')
```

**After:**
```ts
import { blob } from 'hub:blob'
// Note: blob is auto-imported on server-side
await blob.put('file.txt', body, { contentType: 'text/plain' })
await blob.get('file.txt')
await blob.list({ prefix: 'uploads/' })
await blob.del('file.txt')
await blob.serve(event, 'file.txt')
```

Key change: `hubBlob()` function call → `blob` direct object. Same methods, different access pattern.

### 2.7 New Import Pattern (Summary)

v0.10 uses virtual module imports. All are auto-imported on server-side:

```ts
import { db, schema } from 'hub:db'   // Database
import { kv } from 'hub:kv'           // KV Storage
import { blob } from 'hub:blob'       // Blob Storage
```

### 2.8 CLI Commands

```bash
npx nuxt db generate              # Generate migrations from schema
npx nuxt db migrate               # Apply migrations
npx nuxt db mark-as-migrated [NAME]  # Mark migration as applied without running
npx nuxt db drop <TABLE>          # Drop a table
npx nuxt db sql [QUERY]           # Execute SQL query
npx nuxt db sql < dump.sql        # Execute SQL from file

# All commands support:
--cwd <dir>       # Run in different directory
--dotenv <file>   # Use different .env file
-v, --verbose     # Verbose output
```

### 2.9 Provider-Specific Setup (Non-Cloudflare)

#### Database Providers

**PostgreSQL:**
```bash
pnpm add drizzle-orm drizzle-kit postgres @electric-sql/pglite
```
- Uses PGlite locally if no env vars set
- Uses postgres-js if `DATABASE_URL`, `POSTGRES_URL`, or `POSTGRESQL_URL` set

**MySQL:**
```bash
pnpm add drizzle-orm drizzle-kit mysql2
```
- Requires `DATABASE_URL` or `MYSQL_URL` env var

**SQLite (Turso):**
```bash
pnpm add drizzle-orm drizzle-kit @libsql/client
```
- Uses libsql locally at `.data/db/sqlite.db`
- Uses Turso if `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` set

#### KV Providers

| Provider | Package | Env Vars |
|----------|---------|----------|
| Upstash | `@upstash/redis` | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` |
| Redis | `ioredis` | `REDIS_URL` |
| Cloudflare KV | - | `KV` binding in wrangler.jsonc |
| Deno KV | - | Auto on Deno Deploy |
| Vercel | - | `KV_REST_API_URL`, `KV_REST_API_TOKEN` |

#### Blob Providers

| Provider | Package | Config |
|----------|---------|--------|
| Vercel Blob | `@vercel/blob` | Dashboard setup |
| Cloudflare R2 | - | `BLOB` binding in wrangler.jsonc |
| S3 | `aws4fetch` | `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_BUCKET`, `S3_REGION` |
| Netlify Blobs | `@netlify/blobs` | `NETLIFY_BLOB_STORE_NAME` |

### 2.10 Database Hooks (For Nuxt Modules)

```ts
// Extend schema
nuxt.hook('hub:db:schema:extend', async ({ dialect, paths }) => {
  paths.push(await resolvePath(`./schema/pages.${dialect}`))
})

// Add migration directories
nuxt.hook('hub:db:migrations:dirs', (dirs) => {
  dirs.push(resolve('./db-migrations'))
})

// Post-migration queries (must be idempotent)
nuxt.hook('hub:db:queries:paths', (paths, dialect) => {
  paths.push(resolve(`./db-queries/seed.${dialect}.sql`))
})
```

### 2.11 Schema Files

Schema can be in multiple locations:
- `server/db/schema.ts`
- `server/db/schema.{dialect}.ts`
- `server/db/schema/*.ts`
- `server/db/schema/*.{dialect}.ts`

Generated schema at `.nuxt/hub/db/schema.mjs`.

### Deprecated Features (v0.10)

Cloudflare-specific features removed:
- `hubAI()` - Use AI SDK with Workers AI Provider
- `hubBrowser()` - Puppeteer
- `hubVectorize()` - Vectorize
- `hubAutoRAG()` - AutoRAG

### Phase 2 Checklist

- [ ] Complete Phase 1 first
- [ ] Replace `@nuxthub/core` with `@nuxthub/core-nightly`
- [ ] Change `hub.database: true` to `hub.db: 'sqlite'` (or other dialect)
- [ ] Rename `server/database/` to `server/db/`
- [ ] Update imports from `~/server/database/` to `~/server/db/`
- [ ] Migrate `hubDatabase()` → `db` from `hub:db`
- [ ] Migrate `hubKV()` → `kv` from `hub:kv`
- [ ] Migrate `hubBlob()` → `blob` from `hub:blob`
- [ ] Update table references: `tables.X` → `schema.X`
- [ ] Run `npx nuxt db generate` to generate migrations
- [ ] Test all database, KV, and blob operations

---

## Quick Reference

| Aspect | v0.9.X (Phase 1) | v0.10/Nightly (Phase 2) |
|--------|------------------|-------------------------|
| Package | `@nuxthub/core` | `@nuxthub/core-nightly` |
| Database config | `hub.database: true` | `hub.db: 'sqlite'` |
| Directory | `server/database/` | `server/db/` |
| DB access | `hubDatabase()` | `db` from `hub:db` |
| Schema access | N/A | `schema` from `hub:db` |
| KV access | `hubKV()` | `kv` from `hub:kv` |
| Blob access | `hubBlob()` | `blob` from `hub:blob` |
| Migrations | Manual SQL | `npx nuxt db generate` |
| Cloud support | Cloudflare only | Multi-cloud |

## Resources

- [Self-hosting changelog](https://hub.nuxt.com/changelog/self-hosting-first)
- [Deploy docs](https://hub.nuxt.com/docs/getting-started/deploy)
- [v0.10 Installation](https://hub.nuxt.com/docs/getting-started/installation)
- [v0.10 Database](https://hub.nuxt.com/docs/features/database)
- [v0.10 KV](https://hub.nuxt.com/docs/features/kv)
- [v0.10 Blob](https://hub.nuxt.com/docs/features/blob)
- [Legacy v0.9 docs](https://legacy.hub.nuxt.com)
- `references/wrangler-templates.md` - Cloudflare wrangler.jsonc templates
