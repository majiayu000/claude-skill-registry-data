---
name: supabase
description: Supabase — Postgres, Auth, Storage, Edge Functions, RLS, CLI.
---

# Supabase

## Detection Signals

A project uses Supabase when any of the following are present:

| Signal | Meaning |
|---|---|
| `supabase/` directory at project root | Supabase CLI project |
| `@supabase/supabase-js` in `package.json` | JS/TS client |
| `SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_URL` env var | Cloud or self-hosted instance |
| `supabase` service in `docker-compose.yml` | Self-hosted stack |
| `supabase/config.toml` | CLI configuration |
| `supabase/migrations/` directory | Database managed via CLI |

---

## Self-Hosted vs Cloud

| Aspect | Cloud | Self-Hosted |
|---|---|---|
| Auth service | GoTrue (managed) | GoTrue (Docker) |
| API Gateway | Kong (managed) | Kong (Docker, `kong.yml`) |
| Database | Managed Postgres | Your Postgres container |
| Realtime | Managed | Phoenix-based container |
| Storage | Managed S3-compatible | `storage-api` container |
| Edge Functions | Deno Deploy (managed) | `edge-runtime` container |
| Config | Dashboard + env vars | `supabase/config.toml` |
| Studio | `app.supabase.com` | `supabase-studio` container |

**Key difference**: in self-hosted, all services run in Docker. Changes to Kong routes, GoTrue config, and storage policies happen in config files — not a UI. Always check `docker-compose.yml` or `supabase/config.toml` for service config.

---

## Core Services

### Postgres

Supabase exposes Postgres directly (port 5432 by default). Connection via:
- **Direct**: standard connection string — use for migrations, scripts, admin tasks
- **Pooler (PgBouncer)**: for high-concurrency apps — `SUPABASE_DB_URL` with `?pgbouncer=true`
- **PostgREST**: auto-generated REST API from your schema — the default for app data access

PostgREST reads from the `public` schema by default. Expose only what needs to be public. Use schemas to namespace: `api`, `private`, `auth`.

```sql
-- Expose a table via PostgREST
grant select on public.products to anon;
grant all on public.orders to authenticated;
```

### Auth (GoTrue)

See `skills/integrations/gotrue/SKILL.md` for full detail.

Key points:
- GoTrue issues JWTs; your app must verify them
- User metadata: `raw_user_meta_data` (user-set) vs `raw_app_meta_data` (server-set)
- Custom claims go in `app_metadata` — only writable via service-role key or GoTrue hooks

### Storage

Bucket-based object storage with RLS policies.

```sql
-- Allow authenticated users to upload to their own folder
create policy "Users upload own files"
on storage.objects for insert
to authenticated
with check (bucket_id = 'avatars' and auth.uid()::text = (storage.foldername(name))[1]);
```

- Public buckets: files are accessible without auth
- Private buckets: require signed URLs or service-role access
- Max file size and allowed MIME types configured per bucket

### Edge Functions

Deno-based serverless functions deployed via CLI:

```bash
supabase functions new my-function
supabase functions serve            # local dev
supabase functions deploy my-function
```

Functions run with service-role privileges by default — be careful. Pass the JWT in the `Authorization` header and validate it if the function should be user-scoped.

### Realtime

See `skills/integrations/realtime/SKILL.md` for full detail.

---

## Row Level Security (RLS)

RLS is the **primary authorization layer** in Supabase. Always enable it on every table exposed via PostgREST.

```sql
-- Enable RLS
alter table orders enable row level security;

-- Users can only see their own orders
create policy "Users see own orders"
on orders for select
to authenticated
using (user_id = auth.uid());

-- Insert only for authenticated, auto-set user_id
create policy "Users create own orders"
on orders for insert
to authenticated
with check (user_id = auth.uid());
```

**Rules:**
- `using` clause — evaluated on SELECT, UPDATE, DELETE
- `with check` clause — evaluated on INSERT, UPDATE
- `auth.uid()` — returns the UUID of the authenticated user from the JWT
- `auth.role()` — returns `anon`, `authenticated`, or `service_role`
- Without a policy, no rows are returned (default deny)

**Service role key** bypasses RLS — never expose it to the client. Use only in server-side code (Edge Functions, backend services).

---

## Supabase CLI

```bash
supabase init                  # initialize project
supabase start                 # start local stack (Docker)
supabase stop                  # stop local stack
supabase db diff               # diff local vs remote schema
supabase db push               # push migrations to remote
supabase migration new <name>  # create new migration file
supabase gen types typescript  # generate TypeScript types from schema
supabase functions deploy      # deploy edge functions
supabase secrets set KEY=val   # set env secret for edge functions
```

Migrations live in `supabase/migrations/` as timestamped SQL files. Always use the CLI to generate and apply migrations — never edit migration files after they've been applied.

**After every schema change, regenerate the client types** (`supabase gen types typescript`) and commit them with the migration — stale generated types silently drift from the database and defeat type-safe queries.

---

## Environment Variables

| Variable | Usage |
|---|---|
| `SUPABASE_URL` | Base URL of your Supabase instance |
| `SUPABASE_ANON_KEY` | Public key — safe for client-side, respects RLS |
| `SUPABASE_SERVICE_ROLE_KEY` | Bypasses RLS — server-side only, never expose |
| `SUPABASE_JWT_SECRET` | Secret used to verify JWTs — server-side only |
| `DATABASE_URL` | Direct Postgres connection string |

---

## Client Initialization

```typescript
import { createClient } from '@supabase/supabase-js'

// Client-side (browser) — use anon key
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Server-side — use service role key only when RLS bypass is intentional
const adminSupabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)
```

---

## Common Patterns

**Data fetching with RLS**
```typescript
// RLS enforced — returns only rows the user can see
const { data, error } = await supabase
  .from('orders')
  .select('id, total, created_at')
  .order('created_at', { ascending: false })
```

**Typed queries (after `supabase gen types`)**
```typescript
import type { Database } from './database.types'
const supabase = createClient<Database>(url, key)
// now .from() is type-safe
```

**Server-side JWT verification**
```typescript
const { data: { user }, error } = await supabase.auth.getUser(jwt)
if (error || !user) throw new Error('Unauthorized')
```

---

## Common Pitfalls

- Using `service_role` key on the client — bypasses all RLS, massive security hole
- Forgetting to enable RLS on a new table — all rows become public via PostgREST
- Using `auth.uid()` in a migration context (outside a user request) — it returns null
- Not handling token refresh — JWTs expire; use `onAuthStateChange` on the client
- Direct Postgres connections in serverless functions — use PgBouncer URL instead to avoid connection exhaustion
