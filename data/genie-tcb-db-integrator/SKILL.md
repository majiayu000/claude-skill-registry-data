---
name: genie-tcb-db-integrator
description: Integrate TCB (Tencent CloudBase) managed PostgreSQL database into web apps. Provides frontend SDK-first CRUD via PG REST API with Row Level Security (RLS), plus LLM-only scripts for DDL, migrations, and ad-hoc queries. Use this skill when the application needs database tables, persistent storage, or data queries.
_meta_type: sdk
---

# Genie TCB Database Integration (Serverless PostgreSQL)

Integrate TCB managed PostgreSQL into web apps using a **serverless-first** architecture: frontend JS SDK for CRUD (no backend needed), RLS for per-user data isolation, and LLM shell scripts for schema management.

## Architecture Overview

```
Priority 1 (PRIMARY): Frontend JS SDK + RLS
  app.rdb().from('items').select/insert/update/delete
  → TCB PG REST API (PostgREST-based)
  Security: RLS (anon / authenticated / auth.uid())
  No backend needed for standard CRUD.

Priority 2 (ADVANCED): RPC — Custom PostgreSQL Functions
  LLM creates function via tcb-pg-function.sh → frontend calls rpc() helper (HTTP)
  For complex queries, aggregations, multi-table operations.
  Function runs with caller's RLS permissions (or SECURITY DEFINER for elevated access).

Priority 3 (RESTRICTED): LLM Agent scripts
  tcb-pg-migrate.sh / tcb-pg-query.sh / tcb-pg-function.sh
  → auth-proxy → api-server → exec-pgsql
  For: DDL, RLS setup, function creation, ad-hoc analytics, debug.
  NEVER exposed via web app HTTP API endpoints.
```

## Prerequisites

- Frontend: React app with CloudBase JS SDK (`@cloudbase/js-sdk`)
- TCB Environment: Must be initialized first (see Setup)
- Auth (optional but recommended): `genie-tcb-auth-integrator` for user-scoped data

## MANDATORY: TCB Environment User Confirmation

**DO NOT run `ensure-cloudbase-env.sh` or any TCB setup without explicit user approval.**

Before ANY database work, you MUST follow this exact sequence:

1. **Check** if `/workspace/.env.tcb` exists:
   ```bash
   cat /workspace/.env.tcb 2>/dev/null
   ```
2. **If `.env.tcb` exists** and contains `CLOUDBASE_ENV_ID`: TCB is ready, proceed.
3. **If `.env.tcb` does NOT exist**: You MUST **STOP** and use `ask_followup_question` to ask the user:
   ```
   The project does not have a TCB (Tencent CloudBase) environment yet.
   This is required for database features (data storage, queries, RLS).

   Would you like to enable TCB database for this project?
   ```
   Options:
   - **Enable TCB Database** — Creates a TCB environment with managed PostgreSQL
   - **Skip** — Do not enable TCB database at this time

4. **ONLY if user explicitly selects "Enable TCB Database"**, run:
   ```bash
   bash /workspace/.genie/scripts/bash/ensure-cloudbase-env.sh --project-dir /workspace
   ```

5. If user selects "Skip", do NOT create the environment. Inform the user that database features require TCB and stop the database setup.

**NEVER assume the user wants TCB enabled. NEVER skip the confirmation step.**

> `ensure-cloudbase-env.sh` automatically installs `@cloudbase/js-sdk` — no need to install separately.

## Script Paths

**IMPORTANT**: Before calling any script, define these variables. All examples below use them.

```bash
# Define once at the start of any task
DB_SCRIPTS="/workspace/.codebuddy/skills/genie-tcb-db-integrator/scripts"
PROJECT_DIR="/workspace"
```

| Script | Variable | Purpose |
|--------|----------|---------|
| `$DB_SCRIPTS/tcb-pg-migrate.sh` | DDL | CREATE TABLE, ALTER, RLS policies, indexes |
| `$DB_SCRIPTS/tcb-pg-query.sh` | Query | Ad-hoc SQL, schema inspection (tables/columns/indexes/rls) |
| `$DB_SCRIPTS/tcb-pg-function.sh` | Functions | Create/list/show/grant/revoke/rename/drop functions |

If scripts are not found at the above path, try:
```bash
# Alternative: find the skill directory dynamically
DB_SCRIPTS=$(find /workspace -path "*genie-tcb-db-integrator/scripts" -type d 2>/dev/null | head -1)
```

---

## 1. Creating Tables (LLM Agent)

Always include: `id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY`, `user_id TEXT NOT NULL DEFAULT auth.uid()`, `created_at TIMESTAMPTZ DEFAULT now()`.

```bash
bash $DB_SCRIPTS/tcb-pg-migrate.sh \
  --project-dir $PROJECT_DIR \
  --sql "CREATE TABLE items (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id TEXT NOT NULL DEFAULT auth.uid(),
    title TEXT NOT NULL,
    content TEXT,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
  )"
```

**Table comment** (shown in Genie DB management page):
```bash
bash $DB_SCRIPTS/tcb-pg-migrate.sh \
  --project-dir $PROJECT_DIR \
  --sql "COMMENT ON TABLE items IS 'User content items with draft/publish workflow'"
```

**IMPORTANT**: `exec-pgsql` does NOT support multiple SQL statements in one call. Each statement must be a separate invocation.

---

## 2. RLS — Row Level Security (LLM Agent)

RLS controls who can read/write which rows at the database level. After enabling RLS, all operations not explicitly allowed by policies are **denied by default**.

### Enable RLS

```bash
bash $DB_SCRIPTS/tcb-pg-migrate.sh \
  --project-dir $PROJECT_DIR \
  --sql "ALTER TABLE items ENABLE ROW LEVEL SECURITY"
```

### Roles

| Role | Description |
|------|-------------|
| `anon` | Unauthenticated users (accessKey only, no login) |
| `authenticated` | Logged-in users (access_token from TCB Auth) |

### Key function: `auth.uid()`

Returns the current user's identity. Use in policies to enforce data ownership.

### Policy syntax

```sql
-- For SELECT, UPDATE, DELETE:
CREATE POLICY name ON table FOR operation TO role USING (condition);

-- For INSERT (and UPDATE write-check):
CREATE POLICY name ON table FOR INSERT TO role WITH CHECK (condition);
```

**IMPORTANT**: Use `DROP POLICY IF EXISTS name ON table` before `CREATE POLICY` — PostgreSQL has no `CREATE POLICY IF NOT EXISTS`.

### RLS Pattern 1: Read all, modify own data

**Use case**: User comments, public profiles

```bash
# Everyone can read all data
...tcb-pg-migrate.sh --sql "CREATE POLICY select_all ON items FOR SELECT TO authenticated USING (true)"
# Only owner can insert (user_id auto-bound)
...tcb-pg-migrate.sh --sql "CREATE POLICY insert_own ON items FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid())"
# Only owner can update own data
...tcb-pg-migrate.sh --sql "CREATE POLICY update_own ON items FOR UPDATE TO authenticated USING (user_id = auth.uid())"
# Only owner can delete own data
...tcb-pg-migrate.sh --sql "CREATE POLICY delete_own ON items FOR DELETE TO authenticated USING (user_id = auth.uid())"
```

### RLS Pattern 2: Owner-only (private data)

**Use case**: User settings, order management

```bash
...tcb-pg-migrate.sh --sql "CREATE POLICY select_own ON items FOR SELECT TO authenticated USING (user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY insert_own ON items FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY update_own ON items FOR UPDATE TO authenticated USING (user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY delete_own ON items FOR DELETE TO authenticated USING (user_id = auth.uid())"
```

### RLS Pattern 3: Public read (including anonymous)

**Use case**: Announcements, help docs

```bash
...tcb-pg-migrate.sh --sql "CREATE POLICY select_anon ON items FOR SELECT TO anon, authenticated USING (true)"
```

### RLS Pattern 4: Read all, no modification

**Use case**: Product catalog, system config

```bash
...tcb-pg-migrate.sh --sql "CREATE POLICY select_all ON items FOR SELECT TO authenticated USING (true)"
# No INSERT/UPDATE/DELETE policies → all writes denied by default
```

### RLS Pattern 5: Published + own drafts

**Use case**: Blog articles, product listings

```bash
...tcb-pg-migrate.sh --sql "CREATE POLICY select_published_or_own ON items FOR SELECT TO authenticated USING (status = 'published' OR user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY insert_own ON items FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY update_own ON items FOR UPDATE TO authenticated USING (user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY delete_own ON items FOR DELETE TO authenticated USING (user_id = auth.uid())"
```

### RLS Pattern 6: Team shared data

**Use case**: Multi-tenant, team collaboration

```bash
...tcb-pg-migrate.sh --sql "CREATE POLICY select_team ON items FOR SELECT TO authenticated USING (team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid()))"
...tcb-pg-migrate.sh --sql "CREATE POLICY insert_team ON items FOR INSERT TO authenticated WITH CHECK (team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid()))"
...tcb-pg-migrate.sh --sql "CREATE POLICY update_team ON items FOR UPDATE TO authenticated USING (team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid()))"
...tcb-pg-migrate.sh --sql "CREATE POLICY delete_team ON items FOR DELETE TO authenticated USING (team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid()))"
```

### RLS Pattern 7: Insert only, no modification

**Use case**: Feedback, audit logs

```bash
...tcb-pg-migrate.sh --sql "CREATE POLICY select_own ON items FOR SELECT TO authenticated USING (user_id = auth.uid())"
...tcb-pg-migrate.sh --sql "CREATE POLICY insert_own ON items FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid())"
# No UPDATE/DELETE policies → data cannot be modified after submission
```

### RLS Pattern 8: No permissions (server-only)

**Use case**: Internal logs, admin data

```bash
# Enable RLS but create NO policies → all client operations denied
...tcb-pg-migrate.sh --sql "ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY"
# Data only accessible via LLM scripts (admin role) or cloud functions
```

### Best Practice: DEFAULT auth.uid() + WITH CHECK

Always use `DEFAULT auth.uid()` on `user_id` column AND `WITH CHECK (user_id = auth.uid())` on INSERT policy. This double protection:
- `DEFAULT`: auto-fills user_id so client doesn't need to pass it
- `WITH CHECK`: prevents malicious clients from forging another user's user_id

---

## 3. Frontend SDK — CRUD Operations

The frontend uses CloudBase JS SDK `app.rdb()` for all data operations. Under the hood, the SDK calls the TCB PG REST API (`https://{envId}.api.tcloudbasegateway.com/v1/rdb/rest/{table}`) with the user's access_token. RLS enforces security at the database level.

### SDK Setup

```typescript
// src/lib/database.ts — copy from skill lib/database.ts
import cloudbase from '@cloudbase/js-sdk'

const app = cloudbase.init({
  env: import.meta.env.VITE_CLOUDBASE_ENV_ID,
  region: import.meta.env.VITE_CLOUDBASE_REGION || 'ap-shanghai',
  accessKey: import.meta.env.VITE_CLOUDBASE_PUBLISH_KEY,
})

// IMPORTANT: must pass { database: 'public' } to use the public schema
// Without this, SDK uses envId as schema name → "Invalid schema" error
export const db = app.rdb({ database: 'public' })
export const auth = app.auth()
export default app
```

### SELECT — Query data

```typescript
// Basic query with filters + order + limit
const { data, error } = await db
  .from('items')
  .select('id, title, created_at')
  .eq('status', 'published')
  .order('created_at', { ascending: false })
  .limit(20)

// Select specific columns only
const { data } = await db.from('items').select('id, title, status')

// Single record (returns object, not array)
const { data } = await db.from('items').select('*').eq('id', 42).single()

// Maybe single (returns null if not found, no error)
const { data } = await db.from('items').select('*').eq('id', 42).maybeSingle()

// Pagination with total count
const from = (page - 1) * pageSize
const to = from + pageSize - 1
const { data, count } = await db
  .from('items')
  .select('*', { count: 'exact' })
  .order('created_at', { ascending: false })
  .range(from, to)

// Count only (no data returned)
const { count } = await db.from('items').select('*', { count: 'exact', head: true })

// Multiple filters (AND)
const { data } = await db
  .from('items')
  .select('*')
  .gte('created_at', '2024-01-01')
  .ilike('title', '%search%')
  .in('status', ['published', 'featured'])
  .neq('user_id', 'some-id')

// OR conditions
const { data } = await db
  .from('items')
  .select('*')
  .or('status.eq.published,status.eq.featured')

// NULL check
const { data } = await db.from('items').select('*').is('deleted_at', null)

// NOT NULL
const { data } = await db.from('items').select('*').not('deleted_at', 'is', null)

// Multi-column match (shorthand for multiple .eq())
const { data } = await db.from('items').select('*').match({ status: 'published', lang: 'en' })

// Foreign key join
const { data } = await db.from('items').select(`
  id, title, created_at,
  category:categories(id, name)
`).eq('status', 'published')

// Nested join
const { data } = await db.from('categories').select(`
  name,
  items(title, user:users(name, email))
`)

// Full-text search
const { data } = await db
  .from('items')
  .select('*')
  .textSearch('content', 'search query', { type: 'websearch', config: 'simple' })

// Array/JSONB contains
const { data } = await db.from('items').select('*').contains('tags', ['tech', 'ai'])
const { data } = await db.from('items').select('*').containedBy('tags', ['tech', 'ai', 'web'])
```

### INSERT — Create data

```typescript
// Single insert (user_id auto-filled by DEFAULT auth.uid())
// NOTE: Do NOT chain .select() after .insert() — TCB PG REST API does not support
// Prefer: return=representation, which causes 406 error.
const { error } = await db
  .from('items')
  .insert({ title: 'New Item', content: 'Hello', status: 'draft' })

// Batch insert
const { error } = await db.from('items').insert([
  { title: 'Item A', content: 'Content A' },
  { title: 'Item B', content: 'Content B' },
])

// Upsert — update on conflict (merge duplicates)
const { error } = await db
  .from('items')
  .upsert({ id: 42, title: 'Updated or Created', content: '...' })

// Upsert — ignore on conflict
const { error } = await db
  .from('items')
  .upsert({ id: 42, title: 'Skip if exists' }, { ignoreDuplicates: true })
```

### UPDATE — Modify data

```typescript
// Update by ID (RLS enforces owner-only)
const { error } = await db
  .from('items')
  .update({ title: 'Updated Title', status: 'published' })
  .eq('id', 42)

// Batch update by condition
const { error } = await db
  .from('items')
  .update({ status: 'archived' })
  .eq('status', 'draft')
  .lt('created_at', '2024-01-01')
```

### DELETE — Remove data

```typescript
// Delete by ID (RLS enforces owner-only)
const { error } = await db.from('items').delete().eq('id', 42)

// Batch delete by condition
const { error } = await db
  .from('items')
  .delete()
  .eq('status', 'archived')
  .lt('created_at', '2023-01-01')
```

### Filter operators reference

| Method | SQL | Example |
|--------|-----|---------|
| `.eq(col, val)` | `=` | `.eq('status', 'published')` |
| `.neq(col, val)` | `!=` | `.neq('status', 'draft')` |
| `.gt(col, val)` | `>` | `.gt('price', 100)` |
| `.gte(col, val)` | `>=` | `.gte('created_at', '2024-01-01')` |
| `.lt(col, val)` | `<` | `.lt('price', 50)` |
| `.lte(col, val)` | `<=` | `.lte('age', 18)` |
| `.like(col, pat)` | `LIKE` | `.like('title', '%cloud%')` |
| `.ilike(col, pat)` | `ILIKE` | `.ilike('title', '%cloud%')` (case-insensitive) |
| `.is(col, val)` | `IS` | `.is('deleted_at', null)` |
| `.in(col, arr)` | `IN` | `.in('id', [1, 2, 3])` |
| `.contains(col, val)` | `@>` | `.contains('tags', ['tech'])` |
| `.containedBy(col, val)` | `<@` | `.containedBy('tags', ['a','b','c'])` |
| `.overlaps(col, val)` | `&&` | `.overlaps('tags', ['tech'])` |
| `.not(col, op, val)` | `NOT` | `.not('status', 'eq', 'deleted')` |
| `.or(filters)` | `OR` | `.or('status.eq.published,featured.eq.true')` |
| `.match(obj)` | multi `=` | `.match({ status: 'published', lang: 'en' })` |
| `.textSearch(col, q)` | `@@` | `.textSearch('content', 'query')` |

### Modifier methods

| Method | Description | Example |
|--------|-------------|---------|
| `.order(col, opts)` | Sort results | `.order('created_at', { ascending: false })` |
| `.limit(n)` | Limit row count | `.limit(20)` |
| `.range(from, to)` | Pagination (0-based inclusive) | `.range(0, 19)` |
| `.single()` | Return single object (error if != 1 row) | `.eq('id', 42).single()` |
| `.maybeSingle()` | Return object or null (error if > 1 row) | `.eq('id', 42).maybeSingle()` |
| `.select(cols, opts)` | Column selection + count | `.select('*', { count: 'exact' })` |

---

## 4. Frontend RPC — Custom PostgreSQL Functions

For complex queries (aggregations, multi-table joins, custom logic), LLM creates PostgreSQL functions, then frontend calls them via the `rpc()` helper from `database.ts`.

> **IMPORTANT:** `@cloudbase/js-sdk@3.x` does NOT have a `db.rpc()` method. The `rpc()` helper calls the TCB PG REST API (`/v1/rdb/rest/rpc/{function}`) directly via HTTP. Do NOT use `db.rpc()` — it will throw `TypeError: db.rpc is not a function`.

### Function volatility types

| Type | Description | GET support |
|------|-------------|-------------|
| `VOLATILE` | Can modify DB, different results each call (default) | No |
| `STABLE` | Read-only within a statement, can read DB | Yes |
| `IMMUTABLE` | Always same result for same input, no DB access | Yes |

### Creating functions (LLM Agent)

Use `tcb-pg-function.sh create`:

```bash
# Search function (read-only, STABLE)
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace create \
  --name search_items --args "keyword text" --returns "SETOF items" \
  --language sql --volatility STABLE \
  --comment "Search items by keyword (case-insensitive)" \
  --body "SELECT * FROM items WHERE title ILIKE '%' || keyword || '%';"

# Stats function returning JSON
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace create \
  --name get_item_stats --returns json --language sql --volatility STABLE \
  --comment "Get aggregate statistics of all items" \
  --body "SELECT json_build_object('total', COUNT(*), 'latest', MAX(created_at)) FROM items;"

# Simple calculation (IMMUTABLE)
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace create \
  --name add_numbers --args "a integer, b integer" --returns integer \
  --language sql --volatility IMMUTABLE \
  --body "SELECT a + b;"

# plpgsql function with defaults
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace create \
  --name get_recent_items --args "days_ago integer DEFAULT 30, max_results integer DEFAULT 10" \
  --returns "SETOF items" --language plpgsql --volatility STABLE \
  --comment "Get recently created items within N days" \
  --body "RETURN QUERY SELECT * FROM items WHERE created_at >= NOW() - (days_ago || ' days')::interval ORDER BY created_at DESC LIMIT max_results;"

# SECURITY DEFINER function (bypasses RLS — use with caution)
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace create \
  --name get_global_stats --returns json --language sql --volatility STABLE \
  --security-definer \
  --comment "Global stats across all users (admin only)" \
  --body "SELECT json_build_object('total_users', COUNT(DISTINCT user_id), 'total_items', COUNT(*)) FROM items;"
```

Script `create` options:
| Option | Required | Description |
|--------|----------|-------------|
| `--name` | Yes | Function name |
| `--body` | Yes | Function body SQL |
| `--args` | No | Arguments (e.g., `"keyword text, limit_num integer"`) |
| `--returns` | No | Return type (default: `void`). Use `SETOF table` for table results |
| `--language` | No | `sql` (default) or `plpgsql` |
| `--volatility` | No | `IMMUTABLE`, `STABLE`, or `VOLATILE` |
| `--comment` | No | Function description (shown in Genie DB management) |
| `--security-definer` | No | Run with creator's permissions (bypasses RLS) |

### Calling functions from frontend

Use the `rpc()` helper exported from `database.ts` (calls PG REST API directly via HTTP):

```typescript
import { rpc } from '@/lib/database'

// Basic call with parameters
const result = await rpc('add_numbers', { a: 1, b: 2 })
// → 3

// Function returning table rows — filter/order/limit via options
const items = await rpc('search_items', { keyword: 'hello' }, {
  select: 'id,title',
  order: 'created_at.desc',
  limit: 10,
})

// Stats function returning JSON
const stats = await rpc('get_item_stats')
// → { total: 42, latest: '2026-04-23T...' }

// No parameters
const data = await rpc('get_item_stats')
```

`rpc()` function signature:
```typescript
rpc<T>(functionName: string, params?: Record<string, any>, options?: {
  select?: string    // Column selection on result: 'id,title'
  order?: string     // Sort: 'created_at.desc'
  limit?: number     // Max rows
  offset?: number    // Skip rows
}) → Promise<T>
```

> **Do NOT use `db.rpc()`** — `@cloudbase/js-sdk@3.x` does not have this method. Always use the `rpc()` helper.

### Function permissions — Execute & Security

Function permissions have two dimensions:

**1. EXECUTE permission — who can call the function**

By default, `PUBLIC` (everyone including anonymous) can call any function. Use `REVOKE` + `GRANT` to restrict:

```bash
# Revoke from everyone, then grant only to authenticated users
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace revoke --name search_items --args "keyword text" --role PUBLIC

bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace grant --name search_items --args "keyword text" --role authenticated

# Grant to both anon and authenticated (public-readable function)
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace grant --name get_public_info --role anon

bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace grant --name get_public_info --role authenticated
```

| Execute permission | Who can call | Use case |
|-------------------|-------------|----------|
| `PUBLIC` (default) | Anyone (anon + authenticated) | Public stats, info |
| `authenticated` only | Logged-in users | User-specific operations |
| `anon, authenticated` | Explicitly both | Same as PUBLIC but explicit |

**2. Security mode — whose permissions apply inside the function**

| Mode | SQL inside function runs as | RLS behavior | Use case |
|------|---------------------------|-------------|----------|
| `SECURITY INVOKER` (default) | Caller's role (anon/authenticated) | RLS enforced, `auth.uid()` = caller | User data queries |
| `SECURITY DEFINER` | Function creator's role (admin) | **Bypasses RLS**, sees all data | Global stats, leaderboards |

```bash
# Change a function to SECURITY DEFINER
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace set-definer --name get_leaderboard --args "top_n integer"

# Change back to SECURITY INVOKER
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace set-invoker --name get_leaderboard --args "top_n integer"
```

**3. Query and manage functions**

```bash
# List all functions with permissions
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace list

# Show details for a specific function
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace show --name search_items

# Drop a function
bash $DB_SCRIPTS/tcb-pg-function.sh \
  --project-dir /workspace drop --name old_function
```

**4. Common permission patterns**

| Pattern | Execute | Security | Example |
|---------|---------|----------|---------|
| Public read, RLS enforced | `PUBLIC` | `INVOKER` | `get_published_items()` |
| Authenticated only, RLS enforced | `authenticated` | `INVOKER` | `search_my_items(keyword)` |
| Public leaderboard, bypass RLS | `PUBLIC` | `DEFINER` | `get_leaderboard(top_n)` |
| Admin stats, bypass RLS, login required | `authenticated` | `DEFINER` | `get_admin_stats()` |
| Internal only, no client access | revoke from all | `INVOKER` | Helper functions |

**WARNING**: `SECURITY DEFINER` bypasses RLS — only use for functions that genuinely need cross-user data access. Always restrict EXECUTE to the minimum required roles. Validate inputs to prevent data leakage.

### Supported parameter types

| Type | JS Example |
|------|------------|
| `integer` | `{ id: 1 }` |
| `text` / `varchar` | `{ name: 'test' }` |
| `boolean` | `{ active: true }` |
| `json` / `jsonb` | `{ data: { key: 'value' } }` |
| `integer[]` | `{ ids: [1, 2, 3] }` |
| `text[]` | `{ names: ['a', 'b'] }` |

---

## 5. HTTP REST API Reference

The PG REST API follows PostgREST protocol. Base URL: `https://{envId}.api.tcloudbasegateway.com/v1/rdb/rest/`.

All requests require `Authorization: Bearer <access_token>`.

### Query (GET)

```
GET /v1/rdb/rest/{table}?select={cols}&{filter}&order={col.asc|desc}&limit={n}&offset={n}
```

Filter syntax: `column=operator.value` (e.g., `status=eq.published`, `price=gt.100`, `name=ilike.*search*`)

Operators: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like`, `ilike`, `is`, `in`, `not`, `or`, `cs` (contains), `cd` (contained by), `ov` (overlaps)

Headers:
- `Prefer: count=exact` — include total count in `Content-Range` header

### Insert (POST)

```
POST /v1/rdb/rest/{table}
Content-Type: application/json
Prefer: return=representation

{"title": "New Item", "content": "..."}
```

Batch: send JSON array `[{...}, {...}]`.

Upsert: add `Prefer: resolution=merge-duplicates` (ON CONFLICT DO UPDATE) or `resolution=ignore-duplicates` (ON CONFLICT DO NOTHING).

### Update (PATCH)

```
PATCH /v1/rdb/rest/{table}?{filter}
Content-Type: application/json
Prefer: return=representation

{"title": "Updated"}
```

**WHERE condition is mandatory** — returns 400 without filter.

### Delete (DELETE)

```
DELETE /v1/rdb/rest/{table}?{filter}
Prefer: return=representation
```

**WHERE condition is mandatory** — returns 400 without filter.

### RPC (POST)

```
POST /v1/rdb/rest/rpc/{function_name}
Content-Type: application/json

{"param1": "value1", "param2": "value2"}
```

GET (for IMMUTABLE/STABLE functions): `GET /v1/rdb/rest/rpc/{function_name}?param1=value1`

Chain filters on result: `POST /v1/rdb/rest/rpc/search_items?select=title&order=created_at.desc&limit=5`

### Error codes

| Code | HTTP | Description |
|------|------|-------------|
| `INVALID_PARAM` | 400 | Invalid request parameters |
| `INVALID_REQUEST` | 400 | Missing WHERE, SQL error, etc. |
| `PERMISSION_DENIED` | 401 | Authentication failed |
| `PERMISSION_DENIED` | 403 | RLS policy denied |
| `RESOURCE_NOT_FOUND` | 404 | Table not found |
| `DATABASE_23505` | 409 | Unique constraint violation |
| `SYS_ERR` | 500 | Internal error |

---

## 6. LLM Query Script (Analytics / Debug)

For ad-hoc queries during LLM conversation (NOT for web app use):

```bash
bash $DB_SCRIPTS/tcb-pg-query.sh \
  --project-dir $PROJECT_DIR \
  --sql "SELECT COUNT(*) FROM items WHERE created_at >= CURRENT_DATE"

bash $DB_SCRIPTS/tcb-pg-query.sh \
  --project-dir $PROJECT_DIR \
  --sql "SELECT status, COUNT(*) as cnt FROM items GROUP BY status ORDER BY cnt DESC"
```

---

## 7. Error Handling

```typescript
const { error } = await db.from('items').insert({ title: 'Test' })
if (error) {
  switch (error.code) {
    case 'PERMISSION_DENIED':
      // 401: Need login / 403: RLS denied
      break
    case 'DATABASE_23505':
      // Unique constraint violation
      break
    case 'RESOURCE_NOT_FOUND':
      // Table doesn't exist
      break
    default:
      console.error(error.message)
  }
}
```

---

## 8. Scripts Reference

All scripts are located at `$DB_SCRIPTS` (see "Script Paths" section above) and require `--project-dir /workspace`.

### tcb-pg-migrate.sh — DDL & RLS

Execute a single DDL/DML SQL statement (CREATE TABLE, ALTER TABLE, RLS policies, indexes, etc.):

```bash
# Create a table
bash .../scripts/tcb-pg-migrate.sh --project-dir /workspace \
  --sql "CREATE TABLE items (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id TEXT NOT NULL DEFAULT auth.uid(),
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
  )"

# Enable RLS
bash .../scripts/tcb-pg-migrate.sh --project-dir /workspace \
  --sql "ALTER TABLE items ENABLE ROW LEVEL SECURITY"

# Create RLS policy
bash .../scripts/tcb-pg-migrate.sh --project-dir /workspace \
  --sql "CREATE POLICY select_own ON items FOR SELECT TO authenticated USING (user_id = auth.uid())"

# Add table comment
bash .../scripts/tcb-pg-migrate.sh --project-dir /workspace \
  --sql "COMMENT ON TABLE items IS 'User content items'"

# Add column
bash .../scripts/tcb-pg-migrate.sh --project-dir /workspace \
  --sql "ALTER TABLE items ADD COLUMN status TEXT DEFAULT 'draft'"

# Create index
bash .../scripts/tcb-pg-migrate.sh --project-dir /workspace \
  --sql "CREATE INDEX idx_items_user_id ON items(user_id)"
```

### tcb-pg-query.sh — Ad-hoc queries & schema inspection

Execute SQL or use built-in shortcuts (LLM conversation only):

```bash
QUERY="$DB_SCRIPTS/tcb-pg-query.sh"

# === Built-in shortcuts ===
# List all tables
bash $QUERY --project-dir /workspace tables

# Show columns for a table
bash $QUERY --project-dir /workspace columns --table items

# Show indexes
bash $QUERY --project-dir /workspace indexes --table items

# Show RLS policies (one table or all)
bash $QUERY --project-dir /workspace rls --table items
bash $QUERY --project-dir /workspace rls

# Count rows
bash $QUERY --project-dir /workspace count --table items

# Sample data (default 10 rows)
bash $QUERY --project-dir /workspace sample --table items --limit 5

# === Custom SQL ===
bash $QUERY --project-dir /workspace \
  --sql "SELECT status, COUNT(*) as cnt FROM items GROUP BY status ORDER BY cnt DESC"

bash $QUERY --project-dir /workspace \
  --sql "SELECT * FROM items WHERE created_at >= NOW() - INTERVAL '7 days' LIMIT 20"
```

### tcb-pg-function.sh — Create & manage functions

Unified script for all function operations:

```bash
SCRIPT="$DB_SCRIPTS/tcb-pg-function.sh"

# === CREATE ===
# Simple SQL function
bash $SCRIPT --project-dir /workspace create \
  --name add_numbers --args "a integer, b integer" --returns integer \
  --language sql --volatility IMMUTABLE --body "SELECT a + b;"

# Search function returning table rows
bash $SCRIPT --project-dir /workspace create \
  --name search_items --args "keyword text" --returns "SETOF items" \
  --language sql --volatility STABLE \
  --comment "Search items by keyword" \
  --body "SELECT * FROM items WHERE title ILIKE '%' || keyword || '%';"

# Stats function returning JSON
bash $SCRIPT --project-dir /workspace create \
  --name get_stats --returns json --language sql --volatility STABLE \
  --comment "Aggregate statistics" \
  --body "SELECT json_build_object('total', COUNT(*), 'latest', MAX(created_at)) FROM items;"

# plpgsql function with default params
bash $SCRIPT --project-dir /workspace create \
  --name get_recent --args "days integer DEFAULT 30, limit_n integer DEFAULT 10" \
  --returns "SETOF items" --language plpgsql --volatility STABLE \
  --body "RETURN QUERY SELECT * FROM items WHERE created_at >= NOW() - (days || ' days')::interval ORDER BY created_at DESC LIMIT limit_n;"

# SECURITY DEFINER function (bypasses RLS)
bash $SCRIPT --project-dir /workspace create \
  --name get_leaderboard --args "top_n integer DEFAULT 10" \
  --returns "SETOF items" --language sql --volatility STABLE \
  --security-definer --comment "Top N leaderboard (bypasses RLS)" \
  --body "SELECT * FROM items ORDER BY score DESC LIMIT top_n;"

# === LIST all functions ===
bash $SCRIPT --project-dir /workspace list

# === SHOW details for one function ===
bash $SCRIPT --project-dir /workspace show --name search_items

# === GRANT execute permission ===
bash $SCRIPT --project-dir /workspace grant --name search_items --args "keyword text" --role authenticated
bash $SCRIPT --project-dir /workspace grant --name get_stats --role anon

# === REVOKE execute permission ===
bash $SCRIPT --project-dir /workspace revoke --name search_items --args "keyword text" --role PUBLIC

# === CHANGE security mode ===
bash $SCRIPT --project-dir /workspace set-definer --name get_leaderboard --args "top_n integer"
bash $SCRIPT --project-dir /workspace set-invoker --name get_leaderboard --args "top_n integer"

# === DROP a function ===
bash $SCRIPT --project-dir /workspace drop --name old_function
bash $SCRIPT --project-dir /workspace drop --name old_function --args "param1 text"

# === RENAME a function ===
bash $SCRIPT --project-dir /workspace rename --name old_name --new-name new_name

# === UPDATE comment ===
bash $SCRIPT --project-dir /workspace comment --name search_items --comment "Updated description"

# === VIEW source code only ===
bash $SCRIPT --project-dir /workspace source --name search_items
```

All `tcb-pg-function.sh` actions:
| Action | Required options | Description |
|--------|-----------------|-------------|
| `create` | `--name`, `--body` | Create or replace a function |
| `list` | (none) | List all user functions with permissions |
| `show` | `--name` | Show full details (args, returns, security, ACL, source) |
| `source` | `--name` | Show function source code only |
| `grant` | `--name`, `--role` | Grant EXECUTE to a role |
| `revoke` | `--name`, `--role` | Revoke EXECUTE from a role |
| `set-definer` | `--name` | Change to SECURITY DEFINER (bypasses RLS) |
| `set-invoker` | `--name` | Change to SECURITY INVOKER (RLS enforced) |
| `rename` | `--name`, `--new-name` | Rename a function |
| `comment` | `--name`, `--comment` | Update function description |
| `drop` | `--name` | Drop a function |

All `tcb-pg-query.sh` actions:
| Action | Required options | Description |
|--------|-----------------|-------------|
| `--sql "..."` | (none) | Execute custom SQL |
| `tables` | (none) | List all tables with comments and column counts |
| `columns` | `--table` | Show columns, types, defaults, nullable, comments |
| `indexes` | `--table` | Show indexes and their definitions |
| `rls` | `--table` (optional) | Show RLS policies (for one table or all) |
| `count` | `--table` | Count rows in a table |
| `sample` | `--table`, `--limit` (optional) | Sample rows (default 10) |

---

---

## TCB SDK Known Limitations

**1. `app.rdb()` must pass `{ database: 'public' }`**

The CloudBase JS SDK defaults to using the envId as the PostgREST schema name. Since TCB managed PostgreSQL uses the `public` schema, you MUST pass `{ database: 'public' }`:

```typescript
// CORRECT
export const db = app.rdb({ database: 'public' })

// WRONG — causes "Invalid schema: gn-xxxxx" error
export const db = app.rdb()
```

**2. Do NOT chain `.select()` after `.insert()` or `.upsert()`**

TCB PG REST API does not support the `Prefer: return=representation` header, which the SDK sends when `.select()` is chained after a write operation. This causes a **406 Not Acceptable** error.

```typescript
// CORRECT
const { error } = await db.from('items').insert({ title: 'New' })

// WRONG — returns 406 error on TCB
const { data } = await db.from('items').insert({ title: 'New' }).select()
```

If you need the inserted row data, query it separately after insert:
```typescript
const { error } = await db.from('items').insert({ title: 'New' })
if (!error) {
  const { data } = await db.from('items').select('*').order('id', { ascending: false }).limit(1).single()
}
```

**3. Anonymous session auto-creation**

CloudBase JS SDK automatically creates an anonymous session when initialized with `accessKey`. This means `auth.getUser()` may return a user object with `provider: 'anonymous'` even when the user has not explicitly logged in. The `genie-tcb-auth-integrator` auth-context.tsx handles this by filtering anonymous users.

If you write custom auth checks, always filter:
```typescript
const { data } = await auth.getUser()
const user = data?.user
if (!user || !user.email || user.app_metadata?.provider === 'anonymous') {
  // Not a real logged-in user
}
```

**4. Do NOT pass `null` values in `.insert()`**

Omit fields instead of passing `null` to let PostgreSQL use column defaults (e.g., `DEFAULT auth.uid()` for user_id, `DEFAULT now()` for created_at):

```typescript
// CORRECT — omit user_id, let DEFAULT auth.uid() fill it
const { error } = await db.from('items').insert({ title: 'New', content: 'Hello' })

// WRONG — explicit null overrides the DEFAULT
const { error } = await db.from('items').insert({ title: 'New', user_id: null })
```

**5. `db.rpc()` does NOT exist in `@cloudbase/js-sdk@3.x`**

The SDK only supports table-level CRUD (`from/select/insert/update/delete`). To call PostgreSQL functions (RPC), use the `rpc()` helper exported from `database.ts`, which calls the PG REST API endpoint directly via HTTP:

```typescript
// CORRECT — use the rpc() helper
import { rpc } from '@/lib/database'
const result = await rpc('add_numbers', { a: 1, b: 2 })

// WRONG — db.rpc is not a function in @cloudbase/js-sdk@3.x
const { data } = await db.rpc('add_numbers', { a: 1, b: 2 }) // TypeError!
```

---

## MANDATORY: Dangerous SQL User Confirmation

**Before executing any high-risk SQL, you MUST show the SQL to the user and get explicit confirmation via `ask_followup_question`.**

High-risk SQL includes:
- `DROP TABLE` / `DROP FUNCTION` — permanently deletes data or functions
- `TRUNCATE` — deletes all rows without recovery
- `DELETE` without WHERE clause — deletes all rows
- `ALTER TABLE DROP COLUMN` — permanently removes a column and its data
- `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` on a table with existing data — may lock out access
- `REVOKE ALL` on functions or tables — may break running applications
- `SECURITY DEFINER` functions — bypasses RLS, potential data leakage
- Any SQL that modifies or deletes **existing** user data

**Safe SQL (no confirmation needed):**
- `CREATE TABLE` / `CREATE FUNCTION` — creates new objects
- `CREATE POLICY` / `DROP POLICY IF EXISTS` — RLS policy management
- `ALTER TABLE ADD COLUMN` — adds a column (no data loss)
- `COMMENT ON` — adds descriptions
- `CREATE INDEX` — improves performance
- `INSERT` — adds data
- Read-only queries (`SELECT`, `SHOW`, etc.)

**Confirmation flow:**
```
LLM identifies high-risk SQL
  ↓
STOP and use ask_followup_question:
  "I need to execute the following SQL which will [describe impact]:
   
   [show the exact SQL]
   
   This operation is irreversible. Proceed?"
   
   Options: Execute / Cancel
  ↓
ONLY if user selects "Execute", run the script
```

---

## Key Rules

1. **Frontend SDK is the primary path** — use `app.rdb()` for all web app CRUD
2. **Never expose raw SQL via web app API** — auth-proxy `/pg/query` is LLM-only
3. **Always enable RLS** on every table — it's the security boundary
4. **Always include `user_id TEXT DEFAULT auth.uid()`** for user-scoped tables
5. **One SQL statement per script call** — `exec-pgsql` doesn't support batching
6. **Use `DROP POLICY IF EXISTS` before `CREATE POLICY`** — no `IF NOT EXISTS` for policies
7. **RPC functions respect RLS** by default — use `SECURITY DEFINER` only when necessary
8. **TCB environment is shared** with `genie-tcb-auth-integrator` — no separate setup needed
9. **Dangerous SQL requires user confirmation** — see "Dangerous SQL User Confirmation" section above
