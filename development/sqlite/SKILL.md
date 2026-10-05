---
name: sqlite
description: SQLite patterns with better-sqlite3, libSQL, Turso local dev, WAL mode, migrations, embedded database use cases, and Drizzle ORM integration
layer: domain
category: database
triggers:
  - "sqlite"
  - "better-sqlite3"
  - "libsql"
  - "turso"
  - "embedded database"
  - "local database"
  - "WAL mode"
  - "drizzle sqlite"
  - "sqlite migration"
  - "serverless sqlite"
inputs:
  - Application type (CLI, server, edge, embedded)
  - Concurrency requirements
  - Data size and access patterns
  - Deployment target (local, Turso, Cloudflare D1, Fly.io LiteFS)
outputs:
  - SQLite configuration with optimal pragmas
  - Schema definitions and migrations
  - Drizzle ORM integration code
  - Connection management patterns
  - Backup and replication strategy
linksTo:
  - drizzle
  - nodejs
  - testing-patterns
  - performance-profiler
linkedFrom:
  - api-designer
  - microservices
preferredNextSkills:
  - drizzle
  - testing-patterns
fallbackSkills:
  - postgresql
  - mongodb
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - May add better-sqlite3 or @libsql/client dependencies
  - May create .sqlite or .db files in project
  - May modify build configuration for native module compilation
---

# SQLite Domain Skill

## Purpose

SQLite is the most deployed database engine in the world. This skill covers using SQLite as a serious application database -- not just a toy. Modern SQLite with WAL mode, proper pragmas, and tools like Turso/libSQL makes it viable for production web apps, CLI tools, edge deployments, and embedded systems.

## When to Use SQLite

| Use Case | SQLite? | Why |
|----------|---------|-----|
| CLI tools, desktop apps | Yes | Zero config, single file, no server |
| Edge/serverless (Cloudflare D1, Turso) | Yes | Low latency, embedded replicas |
| Read-heavy web apps (< 1000 req/s writes) | Yes | WAL mode handles concurrent reads well |
| Single-server deployments | Yes | Simpler than PostgreSQL if writes are moderate |
| Write-heavy, multi-server | No | Single-writer limitation; use PostgreSQL |
| Complex transactions across services | No | No network protocol; use PostgreSQL |
| Full-text search (simple) | Yes | Built-in FTS5 is excellent |
| Prototyping before PostgreSQL | Yes | Drizzle makes migration between DBs straightforward |

## Key Concepts

### Critical Pragmas (Always Set These)

```typescript
import Database from 'better-sqlite3';

function createDatabase(path: string): Database.Database {
  const db = new Database(path);

  // WAL mode: concurrent reads + writes, massive performance boost
  db.pragma('journal_mode = WAL');

  // Normal sync: safe with WAL, 10x faster than FULL
  db.pragma('synchronous = NORMAL');

  // Store temp tables in memory
  db.pragma('temp_store = MEMORY');

  // 64MB mmap for faster reads on large databases
  db.pragma('mmap_size = 67108864');

  // 20MB page cache (default is 2MB)
  db.pragma('cache_size = -20000');

  // Enable foreign keys (OFF by default!)
  db.pragma('foreign_keys = ON');

  // Busy timeout: wait 5s for locks instead of failing immediately
  db.pragma('busy_timeout = 5000');

  return db;
}
```

### WAL Mode Explained

```
Default (DELETE journal):
  Write -> Lock entire DB -> Write -> Unlock
  Reads block during writes. Writes block during reads.

WAL (Write-Ahead Log):
  Write -> Append to WAL file -> Readers see snapshot
  Multiple concurrent readers. One writer. No blocking between readers and writer.

Checkpointing:
  WAL file periodically merged back into main DB.
  Auto-checkpoint at 1000 pages (default). Manual: PRAGMA wal_checkpoint(TRUNCATE);
```

## Patterns

### 1. better-sqlite3 (Synchronous, Node.js)

```typescript
import Database from 'better-sqlite3';

const db = createDatabase('./app.db');

// Prepared statements -- ALWAYS use these for repeated queries
const getUser = db.prepare('SELECT * FROM users WHERE id = ?');
const insertUser = db.prepare(
  'INSERT INTO users (id, name, email, created_at) VALUES (?, ?, ?, ?)'
);

// Single row
const user = getUser.get('user_123');

// Multiple rows
const allUsers = db.prepare('SELECT * FROM users WHERE active = ?').all(1);

// Insert
insertUser.run('user_456', 'Alice', 'alice@example.com', Date.now());

// Transactions -- 50-100x faster for bulk operations
const insertMany = db.transaction((users: Array<{ id: string; name: string; email: string }>) => {
  for (const u of users) {
    insertUser.run(u.id, u.name, u.email, Date.now());
  }
});

insertMany([
  { id: '1', name: 'Alice', email: 'a@test.com' },
  { id: '2', name: 'Bob', email: 'b@test.com' },
  // ... thousands of rows, still fast
]);

// Cleanup on shutdown
process.on('SIGTERM', () => {
  db.pragma('wal_checkpoint(TRUNCATE)');
  db.close();
});
```

### 2. libSQL / Turso (Remote + Embedded Replicas)

```typescript
import { createClient } from '@libsql/client';

// Local development -- file-based, no server needed
const localDb = createClient({
  url: 'file:./local.db',
});

// Production -- remote Turso database
const remoteDb = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!,
});

// Embedded replica -- local read, remote write (best of both worlds)
const replicaDb = createClient({
  url: 'file:./replica.db',
  syncUrl: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!,
  syncInterval: 60, // Sync every 60 seconds
});

// Queries
const result = await replicaDb.execute({
  sql: 'SELECT * FROM products WHERE category = ? AND price < ?',
  args: ['electronics', 500],
});

// Batch operations (single round-trip)
const batchResult = await remoteDb.batch([
  { sql: 'INSERT INTO orders (user_id, total) VALUES (?, ?)', args: ['u1', 99.99] },
  { sql: 'UPDATE inventory SET stock = stock - 1 WHERE product_id = ?', args: ['p1'] },
], 'write'); // 'write' = transactional batch

// Manual sync for embedded replicas
await replicaDb.sync();
```

### 3. Drizzle ORM + SQLite

```typescript
// schema.ts
import { sqliteTable, text, integer, real, index } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  role: text('role', { enum: ['admin', 'user', 'moderator'] }).default('user'),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
}, (table) => [
  index('users_email_idx').on(table.email),
]);

export const posts = sqliteTable('posts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  title: text('title').notNull(),
  content: text('content'),
  authorId: text('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  publishedAt: integer('published_at', { mode: 'timestamp' }),
  views: integer('views').default(0),
});

export const tags = sqliteTable('tags', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull().unique(),
});

export const postTags = sqliteTable('post_tags', {
  postId: integer('post_id').notNull().references(() => posts.id, { onDelete: 'cascade' }),
  tagId: integer('tag_id').notNull().references(() => tags.id, { onDelete: 'cascade' }),
}, (table) => [
  index('post_tags_post_idx').on(table.postId),
]);
```

```typescript
// db.ts -- better-sqlite3 driver
import { drizzle } from 'drizzle-orm/better-sqlite3';
import Database from 'better-sqlite3';
import * as schema from './schema';

const sqlite = new Database('./app.db');
sqlite.pragma('journal_mode = WAL');
sqlite.pragma('synchronous = NORMAL');
sqlite.pragma('foreign_keys = ON');
sqlite.pragma('busy_timeout = 5000');

export const db = drizzle(sqlite, { schema });

// db.ts -- libSQL driver (for Turso)
import { drizzle } from 'drizzle-orm/libsql';
import { createClient } from '@libsql/client';
import * as schema from './schema';

const client = createClient({
  url: process.env.DATABASE_URL!,
  authToken: process.env.DATABASE_AUTH_TOKEN,
});

export const db = drizzle(client, { schema });
```

```typescript
// queries.ts
import { eq, like, desc, sql, and, gt } from 'drizzle-orm';
import { db } from './db';
import { users, posts, tags, postTags } from './schema';

// Basic queries
const user = await db.select().from(users).where(eq(users.id, 'u1')).get();
const recentPosts = await db
  .select()
  .from(posts)
  .where(gt(posts.publishedAt, new Date('2025-01-01')))
  .orderBy(desc(posts.publishedAt))
  .limit(10)
  .all();

// Join
const postsWithAuthors = await db
  .select({
    postTitle: posts.title,
    authorName: users.name,
    views: posts.views,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .orderBy(desc(posts.views))
  .all();

// Insert
await db.insert(users).values({
  id: 'u2',
  name: 'Bob',
  email: 'bob@example.com',
});

// Upsert (INSERT OR REPLACE)
await db.insert(users)
  .values({ id: 'u2', name: 'Bob Updated', email: 'bob@example.com' })
  .onConflictDoUpdate({
    target: users.id,
    set: { name: 'Bob Updated' },
  });

// Transaction
await db.transaction(async (tx) => {
  const [post] = await tx.insert(posts)
    .values({ title: 'New Post', authorId: 'u1', content: '...' })
    .returning();

  await tx.insert(postTags).values([
    { postId: post.id, tagId: 1 },
    { postId: post.id, tagId: 3 },
  ]);
});
```

### 4. Migrations

```typescript
// drizzle.config.ts
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'sqlite',
  dbCredentials: {
    url: './app.db',
  },
} satisfies Config;
```

```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Open Drizzle Studio (GUI)
npx drizzle-kit studio
```

```typescript
// Programmatic migration (for production)
import { migrate } from 'drizzle-orm/better-sqlite3/migrator';
import { db } from './db';

migrate(db, { migrationsFolder: './drizzle' });
```

### 5. Full-Text Search with FTS5

```sql
-- Create FTS virtual table
CREATE VIRTUAL TABLE posts_fts USING fts5(
  title,
  content,
  content='posts',
  content_rowid='id',
  tokenize='porter unicode61'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER posts_ai AFTER INSERT ON posts BEGIN
  INSERT INTO posts_fts(rowid, title, content)
  VALUES (new.id, new.title, new.content);
END;

CREATE TRIGGER posts_ad AFTER DELETE ON posts BEGIN
  INSERT INTO posts_fts(posts_fts, rowid, title, content)
  VALUES ('delete', old.id, old.title, old.content);
END;

CREATE TRIGGER posts_au AFTER UPDATE ON posts BEGIN
  INSERT INTO posts_fts(posts_fts, rowid, title, content)
  VALUES ('delete', old.id, old.title, old.content);
  INSERT INTO posts_fts(rowid, title, content)
  VALUES (new.id, new.title, new.content);
END;
```

```typescript
// Search with ranking
const results = db.prepare(`
  SELECT posts.*, rank
  FROM posts_fts
  JOIN posts ON posts.id = posts_fts.rowid
  WHERE posts_fts MATCH ?
  ORDER BY rank
  LIMIT 20
`).all('typescript AND database');

// Snippet extraction
const snippets = db.prepare(`
  SELECT
    posts.id,
    posts.title,
    snippet(posts_fts, 1, '<mark>', '</mark>', '...', 32) as content_snippet,
    rank
  FROM posts_fts
  JOIN posts ON posts.id = posts_fts.rowid
  WHERE posts_fts MATCH ?
  ORDER BY rank
  LIMIT 10
`).all('sqlite performance');
```

### 6. JSON Support

```typescript
// SQLite has built-in JSON functions
const db = new Database('./app.db');

// Store JSON
db.prepare(`
  CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    payload TEXT NOT NULL, -- JSON stored as TEXT
    created_at INTEGER DEFAULT (unixepoch())
  )
`).run();

// Query JSON fields
const clickEvents = db.prepare(`
  SELECT id, json_extract(payload, '$.page') as page,
         json_extract(payload, '$.x') as x,
         json_extract(payload, '$.y') as y
  FROM events
  WHERE type = 'click'
    AND json_extract(payload, '$.page') = ?
`).all('/dashboard');

// JSON aggregation
const stats = db.prepare(`
  SELECT type,
         COUNT(*) as count,
         json_group_array(json_extract(payload, '$.page')) as pages
  FROM events
  GROUP BY type
`).all();
```

## Deployment Patterns

### Turso (Multi-Region, Edge)

```
Architecture:
  Primary DB (one region) <- All writes
  Embedded Replicas (each edge server) <- Local reads, sync periodically

Benefits:
  - Reads are local (< 1ms)
  - Writes go to primary (may have latency)
  - Automatic sync keeps replicas fresh
  - Works offline, syncs when connected

Setup:
  turso db create myapp --group default
  turso db tokens create myapp
  turso db replicas create myapp --region nrt  # Tokyo
  turso db replicas create myapp --region fra  # Frankfurt
```

### Cloudflare D1

```typescript
// wrangler.toml
// [[d1_databases]]
// binding = "DB"
// database_name = "myapp"
// database_id = "xxx"

export default {
  async fetch(request: Request, env: Env) {
    const { results } = await env.DB.prepare(
      'SELECT * FROM users WHERE id = ?'
    ).bind(userId).all();
    return Response.json(results);
  },
};
```

### Fly.io LiteFS (Replicated SQLite)

```
Architecture:
  Primary node: reads + writes
  Replica nodes: reads only (replicated via FUSE filesystem)
  Automatic failover with consul lease

Benefits:
  - True SQLite file, all tools work
  - FUSE-based replication (transparent to app)
  - Sub-millisecond reads
```

## Best Practices

1. **Always enable WAL mode** -- the single biggest performance win for concurrent access
2. **Use prepared statements** -- 2-5x faster than raw SQL strings; prevents SQL injection
3. **Wrap bulk inserts in transactions** -- inserting 1000 rows: 50ms with transaction, 5000ms without
4. **Set busy_timeout** -- prevents `SQLITE_BUSY` errors under concurrent writes
5. **Enable foreign_keys pragma** -- it is OFF by default, which silently ignores FK constraints
6. **Use INTEGER PRIMARY KEY for rowid alias** -- avoids extra index, fastest possible lookups
7. **Avoid AUTOINCREMENT unless required** -- plain `INTEGER PRIMARY KEY` auto-generates IDs faster
8. **Checkpoint WAL before backup** -- `PRAGMA wal_checkpoint(TRUNCATE)` ensures clean backup
9. **Use `.wal` and `.shm` awareness** -- three files (`.db`, `.db-wal`, `.db-shm`) must travel together
10. **Profile with EXPLAIN QUERY PLAN** -- check that indexes are being used

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Not enabling WAL mode | All reads blocked during writes | `PRAGMA journal_mode = WAL` at connection open |
| Missing `foreign_keys = ON` | FK constraints silently ignored | Set pragma on every new connection |
| Bulk inserts without transaction | 100x slower performance | Wrap in `db.transaction()` |
| Using LIKE for search | Full table scan | Use FTS5 for text search, indexes for prefix match |
| Storing dates as strings | Cannot sort/compare correctly | Use INTEGER (unix timestamp) or TEXT (ISO 8601) consistently |
| Not handling SQLITE_BUSY | Crashes under concurrent writes | Set `busy_timeout` pragma (5000ms+) |
| Deploying .db without .wal/.shm | Data loss or corruption | Always copy all three files together |
| Using SQLite across NFS/network drives | Silent corruption risk | Only use local filesystems |
| No connection pooling awareness | better-sqlite3 is synchronous, blocks event loop | Use worker threads for heavy queries |
| Forgetting vacuum | Database file grows indefinitely | Schedule periodic `VACUUM` or use `auto_vacuum = INCREMENTAL` |
