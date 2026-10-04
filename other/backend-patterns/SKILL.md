---
name: backend-patterns
description: "Node.js / TypeScript backend patterns: REST API design, repository pattern, middleware, caching, and error handling for Express and Next.js API routes. Use when designing or implementing Node/TS server-side code — API endpoints, service/repository layers, auth middleware, caching, rate limiting, or background jobs. Do NOT use for Python/FastAPI service layers (fastapi-patterns skill) or React/frontend component work (frontend-design)."
origin: ECC
---

# Backend Development Patterns

> **Scope:** Node/TypeScript backends. For Python/FastAPI service layers, see the `fastapi-patterns` skill.

Backend architecture patterns and best practices for scalable server-side applications.

## When to use

- Designing REST or GraphQL API endpoints
- Implementing repository, service, or controller layers
- Optimizing database queries (N+1, indexing, connection pooling)
- Adding caching (Redis, in-memory, HTTP cache headers)
- Setting up background jobs or async processing
- Structuring error handling and validation for APIs
- Building middleware (auth, logging, rate limiting)

**When NOT to use:**

- Python/FastAPI service layers → `fastapi-patterns` skill
- React components, hooks, or client-side state → `frontend-design` / frontend skills
- WordPress/PHP backend (`wordpress-theme/`) → `skyyrose-wp-platform` skill
- Database schema design and SQL tuning beyond query-shape fixes → `postgres-patterns` skill

## Inputs

Required before applying any pattern below. **Absent input = stop — never proceed on a guess.**

1. **The target runtime, identified from the tree.** In this repo, Node/TS backend code lives in
   `frontend/app/api/**/route.ts` (Next.js App Router route handlers on Vercel), not a standalone
   Express app. If you cannot locate where the handler belongs, stop and find it before writing code.
2. **Every imported library declared.** Before writing code that imports a package (`zod`, `redis`,
   `jsonwebtoken`, …), verify it exists in `frontend/package.json` (`npm ls <pkg>` from `frontend/`).
   Undeclared import = stop and resolve the dependency first — never assume it is installed.
3. **Current docs for every non-stdlib API touched** — Context7 `resolve-library-id` → `query-docs`
   before writing against Next.js, Supabase, Redis client, etc. Training data is stale.
4. **The auth decision for any new API route.** In this repo every handler under `frontend/app/api/`
   is either wrapped (`export const GET = withAuth(getHandler)` via `frontend/lib/api-auth.ts`) or
   explicitly exempted in `frontend/lib/api-public-routes.ts` with a written reason. If you don't
   know which applies, stop and ask — an unwrapped route is unprotected (fail-open, bug-230 pattern).

## Procedure

1. Read the nearest existing handler before writing a new one (e.g.
   `frontend/app/api/products/route.ts`) and match its response envelope
   `{ success, data | error }` and its gating style. New code follows existing patterns, not memory.
2. Fetch Context7 docs for each external library the change touches (Inputs #3).
3. Pick the **minimal** pattern from the library below that solves the problem — repository +
   service layers for real data-access complexity, a plain handler for a simple read. No
   speculative abstraction.
4. Implement with the non-negotiables: validate input at the boundary (Zod), narrow `unknown`
   errors (`error instanceof Error`), generic message to the client + detailed log server-side,
   immutable updates, no hardcoded secrets (env only).
5. Wire the auth gate: wrap the exported handler with `withAuth(...)`, or add an exact-match
   exemption to `frontend/lib/api-public-routes.ts` with the reason written next to it.
6. Run the Verification block below. A red check means fix the cause — never weaken the check.

## API Design Patterns

### RESTful API Structure

```typescript
// ✅ Resource-based URLs
GET    /api/markets                 # List resources
GET    /api/markets/:id             # Get single resource
POST   /api/markets                 # Create resource
PUT    /api/markets/:id             # Replace resource
PATCH  /api/markets/:id             # Update resource
DELETE /api/markets/:id             # Delete resource

// ✅ Query parameters for filtering, sorting, pagination
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### Repository Pattern

```typescript
// Abstract data access logic
interface MarketRepository {
  findAll(filters?: MarketFilters): Promise<Market[]>
  findById(id: string): Promise<Market | null>
  create(data: CreateMarketDto): Promise<Market>
  update(id: string, data: UpdateMarketDto): Promise<Market>
  delete(id: string): Promise<void>
}

class SupabaseMarketRepository implements MarketRepository {
  async findAll(filters?: MarketFilters): Promise<Market[]> {
    let query = supabase.from('markets').select('*')

    if (filters?.status) {
      query = query.eq('status', filters.status)
    }

    if (filters?.limit) {
      query = query.limit(filters.limit)
    }

    const { data, error } = await query

    if (error) throw new Error(error.message)
    return data
  }

  // Other methods...
}
```

### Service Layer Pattern

```typescript
// Business logic separated from data access
class MarketService {
  constructor(private marketRepo: MarketRepository) {}

  async searchMarkets(query: string, limit: number = 10): Promise<Market[]> {
    // Business logic
    const embedding = await generateEmbedding(query)
    const results = await this.vectorSearch(embedding, limit)

    // Fetch full data
    const markets = await this.marketRepo.findByIds(results.map(r => r.id))

    // Sort by similarity
    return markets.sort((a, b) => {
      const scoreA = results.find(r => r.id === a.id)?.score || 0
      const scoreB = results.find(r => r.id === b.id)?.score || 0
      return scoreA - scoreB
    })
  }

  private async vectorSearch(embedding: number[], limit: number) {
    // Vector search implementation
  }
}
```

### Middleware Pattern

```typescript
// Request/response processing pipeline
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const token = req.headers.authorization?.replace('Bearer ', '')

    if (!token) {
      return res.status(401).json({ error: 'Unauthorized' })
    }

    try {
      const user = await verifyToken(token)
      req.user = user
      return handler(req, res)
    } catch (error) {
      return res.status(401).json({ error: 'Invalid token' })
    }
  }
}

// Usage
export default withAuth(async (req, res) => {
  // Handler has access to req.user
})
```

## Database Patterns

### Query Optimization

```typescript
// ✅ GOOD: Select only needed columns
const { data } = await supabase
  .from('markets')
  .select('id, name, status, volume')
  .eq('status', 'active')
  .order('volume', { ascending: false })
  .limit(10)

// ❌ BAD: Select everything
const { data } = await supabase
  .from('markets')
  .select('*')
```

### N+1 Query Prevention

```typescript
// ❌ BAD: N+1 query problem
const markets = await getMarkets()
for (const market of markets) {
  market.creator = await getUser(market.creator_id)  // N queries
}

// ✅ GOOD: Batch fetch
const markets = await getMarkets()
const creatorIds = markets.map(m => m.creator_id)
const creators = await getUsers(creatorIds)  // 1 query
const creatorMap = new Map(creators.map(c => [c.id, c]))

markets.forEach(market => {
  market.creator = creatorMap.get(market.creator_id)
})
```

### Transaction Pattern

```typescript
async function createMarketWithPosition(
  marketData: CreateMarketDto,
  positionData: CreatePositionDto
) {
  // Use Supabase transaction
  const { data, error } = await supabase.rpc('create_market_with_position', {
    market_data: marketData,
    position_data: positionData
  })

  if (error) throw new Error('Transaction failed')
  return data
}

// SQL function in Supabase
CREATE OR REPLACE FUNCTION create_market_with_position(
  market_data jsonb,
  position_data jsonb
)
RETURNS jsonb
LANGUAGE plpgsql
AS $$
BEGIN
  -- Start transaction automatically
  INSERT INTO markets VALUES (market_data);
  INSERT INTO positions VALUES (position_data);
  RETURN jsonb_build_object('success', true);
EXCEPTION
  WHEN OTHERS THEN
    -- Rollback happens automatically
    RETURN jsonb_build_object('success', false, 'error', SQLERRM);
END;
$$;
```

## Caching Strategies

### Redis Caching Layer

```typescript
class CachedMarketRepository implements MarketRepository {
  constructor(
    private baseRepo: MarketRepository,
    private redis: RedisClient
  ) {}

  async findById(id: string): Promise<Market | null> {
    // Check cache first
    const cached = await this.redis.get(`market:${id}`)

    if (cached) {
      return JSON.parse(cached)
    }

    // Cache miss - fetch from database
    const market = await this.baseRepo.findById(id)

    if (market) {
      // Cache for 5 minutes
      await this.redis.setex(`market:${id}`, 300, JSON.stringify(market))
    }

    return market
  }

  async invalidateCache(id: string): Promise<void> {
    await this.redis.del(`market:${id}`)
  }
}
```

### Cache-Aside Pattern

```typescript
async function getMarketWithCache(id: string): Promise<Market> {
  const cacheKey = `market:${id}`

  // Try cache
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)

  // Cache miss - fetch from DB
  const market = await db.markets.findUnique({ where: { id } })

  if (!market) throw new Error('Market not found')

  // Update cache
  await redis.setex(cacheKey, 300, JSON.stringify(market))

  return market
}
```

## Error Handling Patterns

### Centralized Error Handler

```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message)
    Object.setPrototypeOf(this, ApiError.prototype)
  }
}

export function errorHandler(error: unknown, req: Request): Response {
  if (error instanceof ApiError) {
    return NextResponse.json({
      success: false,
      error: error.message
    }, { status: error.statusCode })
  }

  if (error instanceof z.ZodError) {
    return NextResponse.json({
      success: false,
      error: 'Validation failed',
      details: error.errors
    }, { status: 400 })
  }

  // Log unexpected errors
  console.error('Unexpected error:', error)

  return NextResponse.json({
    success: false,
    error: 'Internal server error'
  }, { status: 500 })
}

// Usage
export async function GET(request: Request) {
  try {
    const data = await fetchData()
    return NextResponse.json({ success: true, data })
  } catch (error) {
    return errorHandler(error, request)
  }
}
```

### Retry with Exponential Backoff

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error

      if (i < maxRetries - 1) {
        // Exponential backoff: 1s, 2s, 4s
        const delay = Math.pow(2, i) * 1000
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }

  throw lastError!
}

// Usage
const data = await fetchWithRetry(() => fetchFromAPI())
```

## Authentication & Authorization

### JWT Token Validation

```typescript
import jwt from 'jsonwebtoken'

interface JWTPayload {
  userId: string
  email: string
  role: 'admin' | 'user'
}

export function verifyToken(token: string): JWTPayload {
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload
    return payload
  } catch (error) {
    throw new ApiError(401, 'Invalid token')
  }
}

export async function requireAuth(request: Request) {
  const token = request.headers.get('authorization')?.replace('Bearer ', '')

  if (!token) {
    throw new ApiError(401, 'Missing authorization token')
  }

  return verifyToken(token)
}

// Usage in API route
export async function GET(request: Request) {
  const user = await requireAuth(request)

  const data = await getDataForUser(user.userId)

  return NextResponse.json({ success: true, data })
}
```

### Role-Based Access Control

```typescript
type Permission = 'read' | 'write' | 'delete' | 'admin'

interface User {
  id: string
  role: 'admin' | 'moderator' | 'user'
}

const rolePermissions: Record<User['role'], Permission[]> = {
  admin: ['read', 'write', 'delete', 'admin'],
  moderator: ['read', 'write', 'delete'],
  user: ['read', 'write']
}

export function hasPermission(user: User, permission: Permission): boolean {
  return rolePermissions[user.role].includes(permission)
}

export function requirePermission(permission: Permission) {
  return (handler: (request: Request, user: User) => Promise<Response>) => {
    return async (request: Request) => {
      const user = await requireAuth(request)

      if (!hasPermission(user, permission)) {
        throw new ApiError(403, 'Insufficient permissions')
      }

      return handler(request, user)
    }
  }
}

// Usage - HOF wraps the handler
export const DELETE = requirePermission('delete')(
  async (request: Request, user: User) => {
    // Handler receives authenticated user with verified permission
    return new Response('Deleted', { status: 200 })
  }
)
```

## Rate Limiting

### Simple In-Memory Rate Limiter

```typescript
class RateLimiter {
  private requests = new Map<string, number[]>()

  async checkLimit(
    identifier: string,
    maxRequests: number,
    windowMs: number
  ): Promise<boolean> {
    const now = Date.now()
    const requests = this.requests.get(identifier) || []

    // Remove old requests outside window
    const recentRequests = requests.filter(time => now - time < windowMs)

    if (recentRequests.length >= maxRequests) {
      return false  // Rate limit exceeded
    }

    // Add current request
    recentRequests.push(now)
    this.requests.set(identifier, recentRequests)

    return true
  }
}

const limiter = new RateLimiter()

export async function GET(request: Request) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown'

  const allowed = await limiter.checkLimit(ip, 100, 60000)  // 100 req/min

  if (!allowed) {
    return NextResponse.json({
      error: 'Rate limit exceeded'
    }, { status: 429 })
  }

  // Continue with request
}
```

## Background Jobs & Queues

### Simple Queue Pattern

```typescript
class JobQueue<T> {
  private queue: T[] = []
  private processing = false

  async add(job: T): Promise<void> {
    this.queue.push(job)

    if (!this.processing) {
      this.process()
    }
  }

  private async process(): Promise<void> {
    this.processing = true

    while (this.queue.length > 0) {
      const job = this.queue.shift()!

      try {
        await this.execute(job)
      } catch (error) {
        console.error('Job failed:', error)
      }
    }

    this.processing = false
  }

  private async execute(job: T): Promise<void> {
    // Job execution logic
  }
}

// Usage for indexing markets
interface IndexJob {
  marketId: string
}

const indexQueue = new JobQueue<IndexJob>()

export async function POST(request: Request) {
  const { marketId } = await request.json()

  // Add to queue instead of blocking
  await indexQueue.add({ marketId })

  return NextResponse.json({ success: true, message: 'Job queued' })
}
```

## Logging & Monitoring

### Structured Logging

```typescript
interface LogContext {
  userId?: string
  requestId?: string
  method?: string
  path?: string
  [key: string]: unknown
}

class Logger {
  log(level: 'info' | 'warn' | 'error', message: string, context?: LogContext) {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...context
    }

    console.log(JSON.stringify(entry))
  }

  info(message: string, context?: LogContext) {
    this.log('info', message, context)
  }

  warn(message: string, context?: LogContext) {
    this.log('warn', message, context)
  }

  error(message: string, error: Error, context?: LogContext) {
    this.log('error', message, {
      ...context,
      error: error.message,
      stack: error.stack
    })
  }
}

const logger = new Logger()

// Usage
export async function GET(request: Request) {
  const requestId = crypto.randomUUID()

  logger.info('Fetching markets', {
    requestId,
    method: 'GET',
    path: '/api/markets'
  })

  try {
    const markets = await fetchMarkets()
    return NextResponse.json({ success: true, data: markets })
  } catch (error) {
    logger.error('Failed to fetch markets', error as Error, { requestId })
    return NextResponse.json({ error: 'Internal error' }, { status: 500 })
  }
}
```

## Verification

Run from the frontend workspace after any backend TS change. Each check can return "no" — that is
the point. A check that errors or times out is an artifact, not a pass (bug-230): re-run it, don't
report its silence as green.

1. Type safety across the whole workspace:

```bash
cd /Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/frontend && npm run type-check
```

   **PASS:** exits 0 with no `error TS` lines. `[repro]` — observed exiting 0 on this tree 2026-07-29.

2. Lint (flags `console.log` in production code, unsafe patterns):

```bash
cd /Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/frontend && npm run lint
```

   **PASS:** exits 0.

3. Unit suite — includes the auth-coverage gate:

```bash
cd /Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/frontend && npm test
```

   **PASS:** exits 0. `[test]` `frontend/tests/api-auth-coverage.test.ts` walks
   `app/api/**/route.ts` on disk and fails on any exported handler that is neither
   `withAuth`-wrapped nor exempted in `lib/api-public-routes.ts` — this is what makes per-handler
   auth fail CLOSED. A new route that skips step 5 of the Procedure turns this red.

4. Envelope + gate spot-check on the touched route (replace the path with yours):

```bash
grep -n "withAuth\|success" /Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon/frontend/app/api/products/route.ts
```

   **PASS:** output shows both `import { withAuth }` and `export const GET = withAuth(...)` (or the
   route's documented exemption), and every `NextResponse.json` body carries `success:`. `[repo]`

## Worked example

Applying Procedure step 1 + Verification step 4 to the real catalog route, 2026-07-29:

```bash
$ grep -n "withAuth\|success" frontend/app/api/products/route.ts
14:import { withAuth } from '@/lib/api-auth';
89:          { success: false, error: 'Product not found' },
93:      return NextResponse.json({ success: true, data: shape(product) });
101:      success: true,
111:      { success: false, error: message },
117:export const GET = withAuth(getHandler);
```

Reading the full file shows the reference shape a new handler should match: a plain `getHandler`
function, boundary handling of `sku`/`collection` query params, 404 as `{ success: false, error }`,
errors narrowed with `error instanceof Error` before the message reaches the client (line 109), and
the auth gate applied only at the export (line 117) so the handler stays testable. Verification
step 1 on the same tree:

```bash
$ cd frontend && npm run type-check
> tsc --noEmit
$ echo $?
0
```

Both observed this session. `[repro]`

## Failure modes

- **Unwrapped route ships unprotected (fail-open auth).** Per-handler auth is fail-open by nature —
  a new route is public until someone remembers the wrapper. `tests/api-auth-coverage.test.ts` is
  the fail-closed backstop; never add to `PUBLIC_API_ROUTES` without a written reason. (bug-230
  pattern, ×6 in this repo.)
- **Redirect-to-login from an API route.** A 302 to `/login` gets followed transparently by `fetch`,
  handing the caller an HTML page with status 200 that parses as success. API handlers must return
  **401 JSON**, never a redirect.
- **Gating new routes via an edge matcher.** There is none: `frontend/proxy.ts` (`config.matcher`)
  was removed 2026-07-28 — gate with `withAuth()` per handler (`frontend/lib/api-auth.ts`), never by
  adding a proxy or `middleware.ts`. (bug-162 history: the admin-renders gate lived in that matcher.)
- **In-memory state on serverless.** The `RateLimiter` and `JobQueue` patterns above hold state in a
  per-process `Map` — on Vercel each instance has its own, reset on every cold start. Single
  long-lived Node process only; serverless needs Redis or a real queue.
- **Cache write path without invalidation.** Cache-aside reads plus a write path that never calls
  `invalidateCache()` serves stale data until TTL. Every mutation of a cached entity invalidates its
  key in the same change.
- **Retry wrapping a non-idempotent call.** `fetchWithRetry` around a POST that creates a record
  duplicates the record on transient failure. Retry GETs and idempotent PUTs only, or add an
  idempotency key.
- **Next.js dynamic APIs inside cached scopes.** Admin catalog editor broke under `cacheComponents`
  until the handler awaited `connection()` before dynamic work (bug-161).

**Remember**: Backend patterns enable scalable, maintainable server-side applications. Choose patterns that fit your complexity level.
