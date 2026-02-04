---
name: cloudflare-r2-d1
description: Use when working with Cloudflare R2 object storage, D1 SQLite database, KV, or Workers integration - covers bindings, limits, gotchas, and best practices
---

# Cloudflare R2, D1 & Storage Products

Comprehensive guide for Cloudflare's edge storage products: R2 (object storage), D1 (SQLite database), and KV (key-value store).

## Sources

- [Cloudflare Storage Options](https://developers.cloudflare.com/workers/platform/storage-options/)
- [D1 Limits](https://developers.cloudflare.com/d1/platform/limits/)
- [R2 Workers API](https://developers.cloudflare.com/r2/api/workers/workers-api-usage/)
- [Workers Limits](https://developers.cloudflare.com/workers/platform/limits/)

---

## When to Use What

| Product | Best For | Limits |
|---------|----------|--------|
| **R2** | Large files, media, user uploads, S3-compatible storage | No egress fees, 10GB free |
| **D1** | Relational data, per-tenant databases, SQLite workloads | 10GB per database max |
| **KV** | Session data, config, API keys, high-read caching | 1 write/sec per key |
| **Durable Objects** | Real-time coordination, WebSockets, counters | Single-threaded per object |

**Decision tree:**
- Need SQL queries? → **D1**
- Storing files/blobs? → **R2**
- High-read, low-write config? → **KV**
- Real-time state coordination? → **Durable Objects**

---

## D1 SQLite Database

### Critical Limitations

<EXTREMELY-IMPORTANT>
D1 has a **10GB maximum database size**. Design for horizontal sharding across multiple smaller databases (per-user, per-tenant).
</EXTREMELY-IMPORTANT>

| Limit | Value |
|-------|-------|
| Max database size | 10 GB |
| Max connections per Worker | 6 simultaneous |
| Max databases per Worker | ~5,000 bindings |
| Import file size | 5 GB |
| JavaScript number precision | 52-bit (int64 values may lose precision) |

### Performance Characteristics

- **Single-threaded**: Each D1 database processes queries sequentially
- **Throughput formula**: If avg query = 1ms → ~1,000 QPS; if 100ms → 10 QPS
- **Read queries**: < 1ms with proper indexes
- **Write queries**: Several ms (must be durably persisted)

### Gotchas

**1. No traditional transactions**
```javascript
// WRONG - BEGIN TRANSACTION not supported in Workers
await db.exec('BEGIN TRANSACTION');

// CORRECT - Use batch() for atomic operations
const results = await db.batch([
  db.prepare('INSERT INTO users (name) VALUES (?)').bind('Alice'),
  db.prepare('INSERT INTO logs (action) VALUES (?)').bind('user_created'),
]);
```

**2. Large migrations must be batched**
```javascript
// WRONG - Will exceed execution limits
await db.exec('DELETE FROM logs WHERE created_at < ?', oldDate);

// CORRECT - Batch in chunks
while (true) {
  const result = await db.prepare(
    'DELETE FROM logs WHERE id IN (SELECT id FROM logs WHERE created_at < ? LIMIT 1000)'
  ).bind(oldDate).run();
  if (result.changes === 0) break;
}
```

**3. Int64 precision loss**
```javascript
// JavaScript numbers are 53-bit precision
// Storing 9007199254740993 may return 9007199254740992
// Use TEXT for large integers if precision matters
```

**4. Cannot import MySQL/PostgreSQL dumps directly**
- Must convert to SQLite-compatible SQL
- Cannot import raw `.sqlite3` files
- Large string values (~500KB+) may fail due to SQL length limits

### wrangler.toml Configuration

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# For local development (auto-creates if missing in wrangler 4.45+)
[[d1_databases]]
binding = "DB"
database_name = "my-database"
```

### Common Patterns

**Schema migrations:**
```javascript
// migrations/0001_initial.sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

```bash
# Apply migrations
wrangler d1 migrations apply my-database
```

**Multi-tenant pattern:**
```javascript
// Create per-tenant database
// D1 allows thousands of databases at no extra cost
const tenantDb = env[`DB_${tenantId}`];
```

---

## R2 Object Storage

### Key Features

- **S3-compatible API** (with some differences)
- **No egress fees** (major cost advantage over S3)
- **Strong consistency** - reads immediately see writes
- **Workers integration** - direct binding, no network hop

### wrangler.toml Configuration

```toml
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

# With jurisdiction (data residency)
[[r2_buckets]]
binding = "EU_BUCKET"
bucket_name = "eu-data"
jurisdiction = "eu"
```

### Common Operations

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    switch (request.method) {
      case 'PUT': {
        // Upload object
        await env.BUCKET.put(key, request.body, {
          httpMetadata: {
            contentType: request.headers.get('content-type'),
          },
          customMetadata: {
            uploadedBy: 'user-123',
          },
        });
        return new Response('Uploaded', { status: 201 });
      }

      case 'GET': {
        // Download object
        const object = await env.BUCKET.get(key);
        if (!object) {
          return new Response('Not Found', { status: 404 });
        }
        return new Response(object.body, {
          headers: {
            'content-type': object.httpMetadata?.contentType || 'application/octet-stream',
            'etag': object.etag,
          },
        });
      }

      case 'DELETE': {
        await env.BUCKET.delete(key);
        return new Response('Deleted', { status: 200 });
      }

      case 'HEAD': {
        const object = await env.BUCKET.head(key);
        if (!object) {
          return new Response(null, { status: 404 });
        }
        return new Response(null, {
          headers: {
            'content-length': object.size.toString(),
            'etag': object.etag,
          },
        });
      }
    }
  },
};
```

### Gotchas

**1. Memory limits when processing large files**
```javascript
// WRONG - Loads entire file into memory (128MB Worker limit)
const object = await env.BUCKET.get(key);
const data = await object.text();

// CORRECT - Stream for large files
const object = await env.BUCKET.get(key);
return new Response(object.body); // Stream directly
```

**2. Request body can only be read once**
```javascript
// WRONG - Body already consumed
const data = await request.text();
await env.BUCKET.put(key, request.body); // Fails!

// CORRECT - Clone request first
const clone = request.clone();
const data = await request.text();
await env.BUCKET.put(key, clone.body);
```

**3. List operations return max 1000 keys**
```javascript
// Paginate through all objects
let cursor;
const allKeys = [];

do {
  const listed = await env.BUCKET.list({ cursor, limit: 1000 });
  allKeys.push(...listed.objects.map(o => o.key));
  cursor = listed.truncated ? listed.cursor : null;
} while (cursor);
```

### Presigned URLs (S3-compatible)

```javascript
import { AwsClient } from 'aws4fetch';

const r2 = new AwsClient({
  accessKeyId: env.R2_ACCESS_KEY,
  secretAccessKey: env.R2_SECRET_KEY,
});

// Generate presigned upload URL
const signedUrl = await r2.sign(
  new Request(`https://${env.R2_BUCKET}.r2.cloudflarestorage.com/${key}`, {
    method: 'PUT',
  }),
  { aws: { signQuery: true } }
);
```

---

## KV (Key-Value Store)

### When to Use KV

- Session tokens / auth data
- Feature flags / configuration
- Cached API responses
- Data with **high reads, low writes**

### Critical Limitation

<EXTREMELY-IMPORTANT>
KV has a **1 write per second per key** limit. Use D1 or Durable Objects for frequent writes.
</EXTREMELY-IMPORTANT>

### wrangler.toml Configuration

```toml
[[kv_namespaces]]
binding = "CACHE"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Common Operations

```javascript
// Write (with optional TTL)
await env.CACHE.put('user:123', JSON.stringify(userData), {
  expirationTtl: 3600, // 1 hour
});

// Read
const data = await env.CACHE.get('user:123', { type: 'json' });

// Delete
await env.CACHE.delete('user:123');

// List keys with prefix
const keys = await env.CACHE.list({ prefix: 'user:' });
```

---

## Automatic Resource Provisioning (2025)

As of wrangler 4.45+, resources are auto-created:

```toml
# wrangler.toml - No IDs needed for new resources
[[d1_databases]]
binding = "DB"
database_name = "my-app-db"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-app-files"

[[kv_namespaces]]
binding = "CACHE"
```

```bash
# First deploy auto-creates resources
wrangler deploy
```

---

## Full-Stack Pattern: D1 + R2 + KV

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // KV: Check cache first
    const cached = await env.CACHE.get(url.pathname);
    if (cached) return new Response(cached);

    // D1: Query database
    const { results } = await env.DB.prepare(
      'SELECT * FROM posts WHERE slug = ?'
    ).bind(url.pathname).all();

    if (!results.length) {
      return new Response('Not Found', { status: 404 });
    }

    const post = results[0];

    // R2: Get associated image
    const image = post.image_key
      ? await env.BUCKET.get(post.image_key)
      : null;

    // Cache the response
    const html = renderPost(post, image);
    await env.CACHE.put(url.pathname, html, { expirationTtl: 300 });

    return new Response(html, {
      headers: { 'content-type': 'text/html' },
    });
  },
};
```

---

## Cost Optimization

### Free Tier Limits

| Product | Free Tier |
|---------|-----------|
| R2 | 10 GB storage, 1M Class A ops, 10M Class B ops |
| D1 | 5M rows read/day, 100K rows written/day, 5 GB storage |
| KV | 100K reads/day, 1K writes/day, 1 GB storage |
| Workers | 100K requests/day |

### Tips

1. **Use KV for caching** to reduce D1 reads
2. **Batch D1 writes** to minimize write operations
3. **Stream R2 objects** instead of loading into memory
4. **Set TTLs on KV** to auto-expire stale data
5. **Shard D1 databases** per-tenant for horizontal scale

---

## Troubleshooting

### "D1_ERROR: too many SQL variables"
Split large IN clauses into batched queries.

### "R2: EntityTooLarge"
Files > 5GB must use multipart upload.

### "KV: Too many writes"
You're hitting 1 write/sec/key limit. Use D1 or Durable Objects.

### "Worker exceeded CPU time limit"
- Add indexes to D1 queries
- Stream R2 objects instead of buffering
- Split work across multiple requests
