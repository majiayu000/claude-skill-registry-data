---
name: cloudflare-bindings
description: This skill activates when working with Cloudflare Workers bindings like D1, KV, R2, Durable Objects, or environment variables. It provides patterns for database access, caching, file storage, and secrets management.
---

# Cloudflare Bindings

Patterns for Cloudflare Workers bindings in Hono.

## Type Definitions

Define all bindings in a central type:

```typescript
// types/bindings.ts
export type Env = {
  Bindings: {
    // D1 Database
    DB: D1Database

    // KV Namespace
    KV: KVNamespace

    // R2 Bucket
    BUCKET: R2Bucket

    // Durable Object
    COUNTER: DurableObjectNamespace

    // Environment Variables
    ENVIRONMENT: 'development' | 'staging' | 'production'
    API_KEY: string
    JWT_SECRET: string
  }
  Variables: {
    user: User
    requestId: string
  }
}
```

## D1 Database

### Basic Queries

```typescript
app.get('/users', async (c) => {
  const db = c.env.DB

  // Select all
  const { results } = await db
    .prepare('SELECT * FROM users WHERE deleted_at IS NULL')
    .all()

  return c.json({ data: results })
})

app.get('/users/:id', async (c) => {
  const db = c.env.DB
  const id = c.req.param('id')

  // Select one
  const user = await db
    .prepare('SELECT * FROM users WHERE id = ?')
    .bind(id)
    .first()

  if (!user) {
    return c.json({ error: 'User not found' }, 404)
  }

  return c.json({ data: user })
})
```

### Insert and Update

```typescript
app.post('/users', async (c) => {
  const db = c.env.DB
  const { email, name } = c.req.valid('json')
  const id = crypto.randomUUID()

  const result = await db
    .prepare('INSERT INTO users (id, email, name) VALUES (?, ?, ?)')
    .bind(id, email, name)
    .run()

  return c.json({ data: { id, email, name } }, 201)
})

app.put('/users/:id', async (c) => {
  const db = c.env.DB
  const id = c.req.param('id')
  const { name } = c.req.valid('json')

  await db
    .prepare('UPDATE users SET name = ?, updated_at = datetime("now") WHERE id = ?')
    .bind(name, id)
    .run()

  return c.json({ data: { id, name } })
})
```

### Transactions (Batch)

```typescript
app.post('/transfer', async (c) => {
  const db = c.env.DB
  const { fromId, toId, amount } = c.req.valid('json')

  // D1 batch for transaction-like behavior
  const results = await db.batch([
    db.prepare('UPDATE accounts SET balance = balance - ? WHERE id = ?')
      .bind(amount, fromId),
    db.prepare('UPDATE accounts SET balance = balance + ? WHERE id = ?')
      .bind(amount, toId),
    db.prepare('INSERT INTO transfers (from_id, to_id, amount) VALUES (?, ?, ?)')
      .bind(fromId, toId, amount)
  ])

  return c.json({ success: true })
})
```

### Pagination

```typescript
app.get('/users', async (c) => {
  const db = c.env.DB
  const { page, limit } = c.req.valid('query')
  const offset = (page - 1) * limit

  const [users, countResult] = await Promise.all([
    db.prepare('SELECT * FROM users LIMIT ? OFFSET ?')
      .bind(limit, offset)
      .all(),
    db.prepare('SELECT COUNT(*) as total FROM users')
      .first<{ total: number }>()
  ])

  return c.json({
    data: users.results,
    meta: {
      page,
      limit,
      total: countResult?.total || 0
    }
  })
})
```

## KV Namespace

### Basic Operations

```typescript
// Get
app.get('/cache/:key', async (c) => {
  const kv = c.env.KV
  const key = c.req.param('key')

  const value = await kv.get(key)

  if (!value) {
    return c.json({ error: 'Not found' }, 404)
  }

  return c.json({ data: value })
})

// Get as JSON
const data = await kv.get('config', 'json')

// Get with metadata
const { value, metadata } = await kv.getWithMetadata('key')

// Put
await kv.put('key', 'value')

// Put with TTL (seconds)
await kv.put('session', token, { expirationTtl: 3600 })

// Put with expiration (Unix timestamp)
await kv.put('temp', data, { expiration: Date.now() / 1000 + 3600 })

// Put with metadata
await kv.put('user:123', JSON.stringify(user), {
  metadata: { createdAt: Date.now() }
})

// Delete
await kv.delete('key')

// List keys
const { keys } = await kv.list({ prefix: 'user:' })
```

### Caching Pattern

```typescript
app.get('/expensive-data', async (c) => {
  const kv = c.env.KV
  const cacheKey = 'expensive-data'

  // Try cache first
  const cached = await kv.get(cacheKey, 'json')
  if (cached) {
    return c.json({ data: cached, cached: true })
  }

  // Compute expensive data
  const data = await computeExpensiveData()

  // Cache for 5 minutes
  await kv.put(cacheKey, JSON.stringify(data), { expirationTtl: 300 })

  return c.json({ data, cached: false })
})
```

### Rate Limiting

```typescript
const rateLimiter = createMiddleware<Env>(async (c, next) => {
  const kv = c.env.KV
  const ip = c.req.header('CF-Connecting-IP') || 'unknown'
  const key = `ratelimit:${ip}`

  const count = parseInt(await kv.get(key) || '0')

  if (count >= 100) {
    return c.json({ error: 'Rate limit exceeded' }, 429)
  }

  await kv.put(key, String(count + 1), { expirationTtl: 60 })

  await next()
})
```

## R2 Bucket

### Upload Files

```typescript
app.post('/upload', async (c) => {
  const bucket = c.env.BUCKET
  const body = await c.req.parseBody()
  const file = body['file'] as File

  if (!file) {
    return c.json({ error: 'No file provided' }, 400)
  }

  const key = `uploads/${crypto.randomUUID()}-${file.name}`

  await bucket.put(key, file.stream(), {
    httpMetadata: {
      contentType: file.type
    },
    customMetadata: {
      originalName: file.name,
      uploadedAt: new Date().toISOString()
    }
  })

  return c.json({ key }, 201)
})
```

### Download Files

```typescript
app.get('/files/:key', async (c) => {
  const bucket = c.env.BUCKET
  const key = c.req.param('key')

  const object = await bucket.get(key)

  if (!object) {
    return c.json({ error: 'File not found' }, 404)
  }

  const headers = new Headers()
  headers.set('Content-Type', object.httpMetadata?.contentType || 'application/octet-stream')
  headers.set('Content-Length', String(object.size))

  return new Response(object.body, { headers })
})
```

### List Files

```typescript
app.get('/files', async (c) => {
  const bucket = c.env.BUCKET
  const prefix = c.req.query('prefix') || ''

  const listed = await bucket.list({
    prefix,
    limit: 100
  })

  return c.json({
    data: listed.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded
    }))
  })
})
```

### Delete Files

```typescript
app.delete('/files/:key', async (c) => {
  const bucket = c.env.BUCKET
  const key = c.req.param('key')

  await bucket.delete(key)

  return c.body(null, 204)
})
```

## Environment Variables

### Access in Handlers

```typescript
app.get('/config', (c) => {
  const env = c.env.ENVIRONMENT

  return c.json({
    environment: env,
    features: {
      debug: env === 'development'
    }
  })
})
```

### Secrets in Middleware

```typescript
const authMiddleware = createMiddleware<Env>(async (c, next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '')

  if (!token) {
    throw new HTTPException(401, { message: 'Missing token' })
  }

  // Use secret from environment
  const payload = await verify(token, c.env.JWT_SECRET)
  c.set('user', payload)

  await next()
})
```

## wrangler.toml Configuration

```toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "production"

[[d1_databases]]
binding = "DB"
database_name = "my-app-db"
database_id = "xxxx-xxxx-xxxx"

[[kv_namespaces]]
binding = "KV"
id = "xxxx-xxxx-xxxx"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-app-bucket"

# Secrets are set via wrangler secret put
# wrangler secret put JWT_SECRET
```

## Local Development

**.dev.vars** (for local secrets):
```
JWT_SECRET=dev-secret-key
API_KEY=dev-api-key
```

```bash
# Run with local D1
wrangler d1 create my-app-db --local

# Run with local KV
wrangler kv:namespace create KV --local

# Start dev server
wrangler dev
```
