---
name: drizzle-orm-d1
description: Type-safe ORM for Cloudflare D1 using Drizzle. Use when building D1 schemas, writing type-safe queries, generating migrations with Drizzle Kit, defining relations, using db.batch, or hitting D1_ERROR, BEGIN TRANSACTION failures, foreign key constraints, env.DB undefined, or schema inference issues.
---

# Drizzle ORM for Cloudflare D1

## Quick Start (10 Minutes)

### 1. Install Drizzle

```bash
bun add drizzle-orm
bun add -D drizzle-kit
```

### 2. Configure Drizzle Kit

`drizzle.config.ts` at the project root:

```ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/server/db/schema",
  out: "./src/server/db/migrations",
  dialect: "sqlite",
});
```

No `driver`, no `dbCredentials`. Drizzle Kit only generates SQL files. Wrangler applies them.

### 3. Define Schema

`src/server/db/schema/users.ts`:

```ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";
import { relations } from "drizzle-orm";
import { posts } from "./posts";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  email: text("email").notNull().unique(),
  name: text("name").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date())
    .notNull(),
});

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));
```

`src/server/db/schema/posts.ts`:

```ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";
import { relations } from "drizzle-orm";
import { users } from "./users";

export const posts = sqliteTable("posts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  title: text("title").notNull(),
  content: text("content").notNull(),
  authorId: integer("author_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
});

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}));
```

`src/server/db/schema/index.ts` re-exports everything (tables AND `*Relations`):

```ts
export * from "./users";
export * from "./posts";
```

`src/server/db/client.ts`:

```ts
import { drizzle } from "drizzle-orm/d1";
import * as schema from "./schema";

export function createDb(d1: D1Database) {
  return drizzle(d1, { schema });
}

export type DB = ReturnType<typeof createDb>;
```

The barrel re-export is mandatory: `client.ts` does `import * as schema from "./schema"` and passes it to `drizzle`, and the relational query API can only see relations exported there.

### 4. Generate & Apply Migrations (local)

```bash
bun run db:generate        # drizzle-kit generate → SQL in ./src/server/db/migrations
bun run db:migrate:local   # apply to local D1
```

Remote is a deliberate, separate step: `bun run db:migrate:remote`, then `bun run deploy` — the scripts bake in the production env selection (see [MIGRATIONS.md](MIGRATIONS.md)); never run raw wrangler `--remote`/`deploy`.

### 5. Query in Worker

```ts
import { createDb } from "./server/db/client";
import { users } from "./server/db/schema";
import { eq } from "drizzle-orm";

export default {
  async fetch(req: Request, env: { DB: D1Database }) {
    const db = createDb(env.DB);
    const list = await db.select().from(users).all();
    return Response.json(list);
  },
};
```

Helpers downstream take `db: DB`, never a raw `D1Database`.

---

## Critical Rules

### Always Do

| Rule | Why |
|------|-----|
| Use `dialect: "sqlite"` only in `drizzle.config.ts` | Drizzle Kit's job is generating SQL; wrangler owns the database |
| Point `schema` at a directory | Multi-file schema with `index.ts` barrel is the project convention |
| Re-export every `*Relations` from `schema/index.ts` | Otherwise the relational query API silently can't see them |
| Go through `createDb(env.DB)` | Schema wiring stays in one place; the `DB` type flows to callers |
| Use `bunx drizzle-kit generate` | Never write SQL by hand |
| Match the surrounding table's timestamp style (see SCHEMA-PATTERNS) | Auth tables use ISO text; product tables use epoch-ms integers — do not mix or migrate |
| Use `.$defaultFn(() => ...)` for dynamic defaults | `.default()` is for literal SQL defaults |
| Use `db.batch([...])` for transactions | D1 does not support SQL `BEGIN`/`COMMIT` |
| Build `.where()` from condition operators (`eq`, `ne`, `gt/gte/lt/lte`, `and`, `or`, `not`, `like`, `inArray`, `isNull`, `isNotNull`, `between`, `exists` — all from `drizzle-orm`), not raw ``sql`...` `` templates | Composable, typo-safe, and typed against the column; reserve ``sql`...` `` for what operators can't express (aggregates, `CASE WHEN`, `COLLATE`, datetime math) |
| Chunk multi-row inserts via `insertInChunks` (`src/server/lib/d1-insert.ts`) | D1 caps bound params at **100** per statement |
| Test migrations with `--local` before commit | Catches schema drift before CI does |
| Read every generated migration before applying | Table rebuilds break on FK'd tables: D1 no-ops drizzle-kit's `PRAGMA foreign_keys=OFF`, so the drop either rolls back at COMMIT or cascades child rows away. See [ERRORS.md](ERRORS.md) #14 |
| Verify rebuild migrations on a *populated* local DB | An empty DB passes any rebuild; production won't |
| Declare `onDelete` on every new FK | D1 always enforces FKs; default `no action` fails deletes |

### Never Do

| Rule | Why |
|------|-----|
| Add `driver` or `dbCredentials` to `drizzle.config.ts` | We do not use the HTTP driver; wrangler is the only applier |
| Run raw `wrangler d1 migrations apply DB --remote` or raw `wrangler deploy` | Without the production env selection they target the top-level (dev) config. Use `bun run db:migrate:remote` (bakes in `--env production`) and `bun run deploy` (bakes in `CLOUDFLARE_ENV=production`), migrate before deploy |
| Use `drizzle-kit push` against any D1 | Bypasses migrations, no audit trail, no rollback |
| Use SQL `BEGIN TRANSACTION` or `db.transaction()` | Not supported on D1; use `db.batch` |
| Pass a raw `D1Database` to query helpers | Loses schema wiring; relational queries break |
| Commit credentials in any config file | Use Cloudflare secrets and env vars |

---

## D1 Limits & Quirks

| Limit | Value |
|-------|-------|
| Bound parameters per statement | **100** (drives insert chunking) |
| Columns per table | 100 |
| String/BLOB value size | 2 MB |
| SQL statement length | 100 KB |
| Queries per Worker invocation | 1000 (paid) / 50 (free) |
| Concurrent D1 connections per Worker | 6 |
| Max query duration | 30 s |
| Database size | 10 GB (paid) / 500 MB (free) |

Quirks: FKs are always enforced — `PRAGMA foreign_keys` is blocked, only `PRAGMA defer_foreign_keys` works (see [MIGRATIONS.md](MIGRATIONS.md)). Other PRAGMAs are restricted to `table_list`/`table_info`/`table_xinfo`. D1 is single-threaded (one query at a time, backed by a Durable Object). No BigInt — values beyond JS's 53-bit safe-integer range lose precision. FTS5 virtual tables work but block `wrangler d1 export`.

---

## Top 5 Critical Errors

| # | Error | Solution |
|---|-------|----------|
| 1 | `D1_ERROR: Cannot use BEGIN TRANSACTION` | Use `db.batch([...])` instead of `db.transaction()` |
| 2 | `FOREIGN KEY constraint failed` | Define cascading: `.references(() => users.id, { onDelete: "cascade" })` |
| 3 | `env.DB is undefined` | The `binding` in `wrangler.jsonc` `d1_databases` must equal the property name (`DB`) |
| 4 | `db.query.X` is `undefined` or relation missing in result | Re-export `*Relations` from `schema/index.ts` and pass `{ schema }` to `drizzle(...)` |
| 5 | `Type instantiation is excessively deep and possibly infinite` | Annotate with `InferSelectModel<typeof users>` instead of letting TS infer |

**See**: [ERRORS.md](ERRORS.md) for the full catalog with code samples.

---

## Common Patterns Summary

| Pattern | Use Case | Reference |
|---------|----------|-----------|
| **CRUD operations** | Basic database operations | [QUERIES.md](QUERIES.md) (CRUD section) |
| **Relations & joins** | Manual joins and relational query API | [QUERIES.md](QUERIES.md) (Joins, Relational query API) |
| **Batch operations** | Atomic multi-statement work (D1 batch API) | [QUERIES.md](QUERIES.md) (Transactions: db.batch) |
| **Schema design** | Naming, indexes, soft deletes, UUIDs, enums | [SCHEMA-PATTERNS.md](SCHEMA-PATTERNS.md) |
| **Prepared statements** | Hot paths reusing the same query shape | [QUERIES.md](QUERIES.md) (Prepared statements) |

---

## Configuration Summary

| File | Purpose | Reference |
|------|---------|-----------|
| `drizzle.config.ts` | Drizzle Kit configuration (dialect-only) | This SKILL.md, Quick Start step 2 |
| `wrangler.jsonc` | D1 binding + `migrations_dir` | [MIGRATIONS.md](MIGRATIONS.md) (Wrangler binding) |
| `src/server/db/client.ts` | `createDb` factory + `DB` type | This SKILL.md, Quick Start step 3 |
| `src/server/db/schema/index.ts` | Barrel re-export feeding the relational query API | This SKILL.md, Quick Start step 3 |
| `package.json` | bun scripts for migrations | [MIGRATIONS.md](MIGRATIONS.md) (bun scripts) |

**bun scripts:**

```json
{
  "db:generate": "drizzle-kit generate",
  "db:migrate:local": "wrangler d1 migrations apply DB --local",
  "db:migrate:remote": "wrangler d1 migrations apply DB --remote --env production",
  "db:seed": "wrangler d1 execute DB --local --file=./src/server/db/seed.sql"
}
```

`--env production` on the remote script is load-bearing — the top-level `wrangler.jsonc` config is dev-only; production bindings live under `env.production`.

---

## Migration Workflow

| Step | Command | Notes |
|------|---------|-------|
| 1. Edit schema | Edit files in `src/server/db/schema/` | Add the table, re-export from `index.ts` |
| 2. Generate | `bun run db:generate` | Creates SQL in `src/server/db/migrations` — **read the generated file** (rebuild? see [ERRORS.md](ERRORS.md) #14) |
| 3. Apply locally | `bun run db:migrate:local` | Verify against local D1 — populated, not empty, if the migration rebuilds a table |
| 4. Commit and open PR | `git commit && git push` | Tests rebuild an in-memory DB from the real migration files, so drift fails fast |
| 5. Apply remote | `bun run db:migrate:remote` | Targets `env.production` via `--env production` |
| 6. Deploy | `bun run deploy` | Always after the remote migration, never before |

**See**: [MIGRATIONS.md](MIGRATIONS.md) for `wrangler.jsonc` setup, renames, hand-edit cases, and common workflow failures.

---

## TypeScript Type Inference

```ts
import type { InferSelectModel, InferInsertModel } from "drizzle-orm";
import { users } from "./server/db/schema";

export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;
```

`InferSelectModel` is the row shape returned by `select`. `InferInsertModel` is the shape accepted by `insert`, with autoIncrement and defaulted columns marked optional.

---

## When to Load References

| Reference | Load when... |
|-----------|--------------|
| [ERRORS.md](ERRORS.md) | Debugging D1 errors, transaction failures, binding issues, migration failures |
| [SCHEMA-PATTERNS.md](SCHEMA-PATTERNS.md) | Designing schemas, naming, timestamps, UUIDs, soft deletes, indexes, relations |
| [MIGRATIONS.md](MIGRATIONS.md) | Setting up `wrangler.jsonc`, configuring `migrations_dir`, troubleshooting renames |
| [QUERIES.md](QUERIES.md) | Writing non-trivial queries, joins, relational queries, `db.batch`, prepared statements |

---

## Bundled Resources

**References**: [SCHEMA-PATTERNS.md](SCHEMA-PATTERNS.md), [MIGRATIONS.md](MIGRATIONS.md), [QUERIES.md](QUERIES.md), [ERRORS.md](ERRORS.md)

---

## Dependencies

```json
{
  "dependencies": {
    "drizzle-orm": "^0.45.2"
  },
  "devDependencies": {
    "drizzle-kit": "^0.31.10"
  }
}
```

---

## Official Documentation

- **Drizzle ORM**: https://orm.drizzle.team/
- **Drizzle with D1**: https://orm.drizzle.team/docs/connect-cloudflare-d1
- **Drizzle Kit**: https://orm.drizzle.team/docs/kit-overview
- **Cloudflare D1**: https://developers.cloudflare.com/d1/
- **wrangler d1**: https://developers.cloudflare.com/workers/wrangler/commands/#d1
- **GitHub**: https://github.com/drizzle-team/drizzle-orm

---

**Token Savings**: progressive disclosure via four sibling references
**Error Prevention**: top 5 inline, full catalog in [ERRORS.md](ERRORS.md)
