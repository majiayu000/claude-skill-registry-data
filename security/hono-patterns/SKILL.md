---
name: hono-patterns
description: This skill activates when writing Hono routes, handlers, middleware, or discussing Hono application architecture. It provides patterns for routing, middleware composition, error handling, and TypeScript integration.
---

# Hono Patterns

Core patterns for building Hono applications.

## Routing Patterns

### Modular Route Organization

Organize routes in separate files and compose with `app.route()`:

```typescript
// routes/users.ts
import { Hono } from 'hono'
import type { Env } from '../types/bindings'

const users = new Hono<Env>()

users.get('/', (c) => c.json({ users: [] }))
users.get('/:id', (c) => c.json({ id: c.req.param('id') }))
users.post('/', (c) => c.json({ created: true }, 201))

export { users }

// index.ts
import { users } from './routes/users'
import { posts } from './routes/posts'

app.route('/api/users', users)
app.route('/api/posts', posts)
```

### Route Groups with Shared Middleware

```typescript
const api = new Hono<Env>()

// Apply auth to all /api routes
api.use('*', authMiddleware)

api.route('/users', users)
api.route('/posts', posts)

app.route('/api', api)

// Public routes remain unprotected
app.get('/health', (c) => c.json({ status: 'ok' }))
```

### Chained Route Definition (for RPC)

```typescript
// Chain routes for proper type inference
const routes = app
  .get('/users', (c) => c.json({ users: [] }))
  .post('/users', (c) => c.json({ created: true }, 201))
  .get('/users/:id', (c) => c.json({ id: c.req.param('id') }))

export type AppType = typeof routes
```

## Handler Patterns

### Basic Handler

```typescript
app.get('/users', async (c) => {
  const users = await fetchUsers()
  return c.json(users)
})
```

### Handler with Validation

```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

app.post('/users',
  zValidator('json', z.object({
    email: z.string().email(),
    name: z.string().min(1)
  })),
  async (c) => {
    const data = c.req.valid('json')
    return c.json({ id: crypto.randomUUID(), ...data }, 201)
  }
)
```

### Factory Pattern for External Handlers

Use when handlers need to be defined outside route files:

```typescript
import { createFactory } from 'hono/factory'
import type { Env } from '../types/bindings'

const factory = createFactory<Env>()

// Define handler with proper types
export const listUsers = factory.createHandlers(
  zValidator('query', paginationSchema),
  async (c) => {
    const { page, limit } = c.req.valid('query')
    return c.json({ users: [], page, limit })
  }
)

// Use in routes
users.get('/', ...listUsers)
```

## Middleware Patterns

### Creating Typed Middleware

```typescript
import { createMiddleware } from 'hono/factory'
import type { Env } from '../types/bindings'

export const loggerMiddleware = createMiddleware<Env>(async (c, next) => {
  const start = Date.now()
  await next()
  console.log(`${c.req.method} ${c.req.url} - ${Date.now() - start}ms`)
})
```

### Middleware with Variables

```typescript
// Update types/bindings.ts
type Env = {
  Variables: {
    user: { id: string; email: string }
  }
}

// Middleware sets variable
const authMiddleware = createMiddleware<Env>(async (c, next) => {
  const user = await validateToken(c.req.header('Authorization'))
  c.set('user', user)  // Type-safe!
  await next()
})

// Handler accesses variable
app.get('/profile', authMiddleware, (c) => {
  const user = c.get('user')  // Type-safe!
  return c.json(user)
})
```

### Configurable Middleware Factory

```typescript
interface CacheOptions {
  maxAge: number
  public?: boolean
}

export const cache = (options: CacheOptions) => {
  return createMiddleware<Env>(async (c, next) => {
    await next()

    const directive = options.public ? 'public' : 'private'
    c.header('Cache-Control', `${directive}, max-age=${options.maxAge}`)
  })
}

// Usage
app.get('/static/*', cache({ maxAge: 86400, public: true }))
```

## Error Handling

### HTTPException

```typescript
import { HTTPException } from 'hono/http-exception'

app.get('/users/:id', async (c) => {
  const user = await getUser(c.req.param('id'))

  if (!user) {
    throw new HTTPException(404, { message: 'User not found' })
  }

  return c.json(user)
})
```

### Global Error Handler

```typescript
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status)
  }

  console.error(err)
  return c.json({ error: 'Internal server error' }, 500)
})
```

### Custom Error Classes

```typescript
class NotFoundError extends HTTPException {
  constructor(resource: string) {
    super(404, { message: `${resource} not found` })
  }
}

class ValidationError extends HTTPException {
  constructor(errors: Record<string, string>) {
    super(400, { message: 'Validation failed', cause: errors })
  }
}
```

## Response Patterns

### JSON Responses

```typescript
// Success
c.json({ data: users })
c.json({ data: user }, 200)
c.json({ data: newUser }, 201)

// Errors
c.json({ error: 'Not found' }, 404)
c.json({ error: 'Validation failed', details: errors }, 400)

// No content
c.body(null, 204)
```

### Consistent Response Format

```typescript
interface ApiResponse<T> {
  data?: T
  error?: string
  meta?: {
    page?: number
    limit?: number
    total?: number
  }
}

// Helper
function success<T>(c: Context, data: T, status = 200) {
  return c.json({ data } as ApiResponse<T>, status)
}

function error(c: Context, message: string, status = 400) {
  return c.json({ error: message } as ApiResponse<never>, status)
}
```

## Context Access

### Request Data

```typescript
// Path params
const id = c.req.param('id')
const { id, slug } = c.req.param()

// Query params
const page = c.req.query('page')
const { page, limit } = c.req.query()

// Headers
const auth = c.req.header('Authorization')

// Body (validated)
const data = c.req.valid('json')
const form = c.req.valid('form')
const query = c.req.valid('query')
```

### Environment and Bindings

```typescript
// Environment variables
const secret = c.env.JWT_SECRET

// Cloudflare bindings
const db = c.env.DB
const kv = c.env.KV
const bucket = c.env.BUCKET
```

### Request Testing via CLI and `app.request`

Test endpoints directly without launching a background server:

```typescript
// Fast in-memory request testing (Bun test / Vitest)
import { describe, it, expect } from 'bun:test'
import app from '../src/index'

describe('User API', () => {
  it('GET /api/users returns 200', async () => {
    const res = await app.request('/api/users')
    expect(res.status).toBe(200)
    expect(await res.json()).toEqual({ users: [] })
  })

  it('POST /api/users validates payload', async () => {
    const res = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@example.com' }),
    })
    expect(res.status).toBe(201)
  })
})
```

Using the Hono CLI:
```bash
# Test endpoints directly from terminal
npx hono request http://localhost:8787/api/users
```

### OpenAPI & Swagger via `@hono/zod-openapi`

```typescript
import { createRoute, OpenAPIHono, z } from '@hono/zod-openapi'
import { swaggerUI } from '@hono/swagger-ui'

const app = new OpenAPIHono()

const getUserRoute = createRoute({
  method: 'get',
  path: '/users/{id}',
  request: {
    params: z.object({ id: z.string() }),
  },
  responses: {
    200: {
      content: { 'application/json': { schema: UserSchema } },
      description: 'Retrieve user by ID',
    },
  },
})

app.openapi(getUserRoute, (c) => {
  const { id } = c.req.valid('param')
  return c.json({ id, name: 'John Doe' }, 200)
})

// Auto-generated Swagger UI docs
app.doc('/doc', { openapi: '3.1.0', info: { title: 'API', version: 'v1' } })
app.get('/ui', swaggerUI({ url: '/doc' }))
```

### AI Streaming & Server-Sent Events (SSE)

```typescript
import { streamText, streamSSE } from 'hono/streaming'

app.get('/api/chat', (c) => {
  return streamText(c, async (stream) => {
    for (const chunk of ['Hello', ' from', ' edge!']) {
      await stream.write(chunk)
      await stream.sleep(100)
    }
  })
})
```

## Best Practices

1. **Always type your app**: `new Hono<Env>()`
2. **Validate all inputs** with Zod
3. **Use `createMiddleware`** for type-safe middleware
4. **Export `AppType`** for RPC client
5. **Handle errors** with HTTPException
6. **Use proper status codes**: 200, 201, 204, 400, 401, 404, 500
7. **Organize routes** in separate files
8. **Keep handlers small** - delegate to services
