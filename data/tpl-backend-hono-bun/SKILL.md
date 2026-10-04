---
name: tpl-backend-hono-bun
description: Template do pack (backend/08-hono-bun.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/08-hono-bun.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Hono + Bun REST API

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/08-hono-bun.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Runtime:** Bun 1.x
- **Framework:** Hono v4
- **Language:** TypeScript 5.x (strict)
- **ORM:** Drizzle ORM
- **Database:** SQLite (local) / Turso (production)
- **Validation:** Zod
- **Testing:** Vitest + @hono/testing
- **Deployment:** Cloudflare Workers / Fly.io edge

---

## PROJECT STRUCTURE
```
src/
├── index.ts                  # App entry, route mounting
├── env.ts                    # Zod-validated env vars
├── db/
│   ├── index.ts              # Drizzle client + connection
│   ├── schema.ts             # All table definitions
│   └── migrations/           # Drizzle generated migrations
├── routes/
│   ├── users.ts
│   ├── posts.ts
│   └── auth.ts
├── middleware/
│   ├── auth.ts               # JWT verification
│   ├── logger.ts
│   └── rate-limit.ts
├── lib/
│   ├── errors.ts             # Custom error classes
│   └── response.ts           # Typed response helpers
└── types.ts                  # Env + Variables types
tests/
├── routes/
│   └── users.test.ts
└── helpers/
    └── app.ts                # Test app factory
```

---

## ARCHITECTURE RULES
1. **Every route file exports a `Hono` instance** — never export raw handlers.
2. **Use `c.var` for typed middleware state** — define in `Variables` type; never use `c.set` with untyped keys.
3. **Zod validates all inputs** — body via `zValidator`, query via `zValidator('query', ...)`.
4. **Drizzle schema = single source of truth** — never use raw SQL except for complex aggregates.
5. **RPC mode is required** — export `AppType` from `index.ts` for type-safe client usage.
6. **No `any` types** — use `unknown` + zod parse at the boundary.
7. **Environment validated at startup** — app does not start with missing env vars.

---

## MIDDLEWARE PATTERN

```typescript
// src/types.ts
import type { Context } from 'hono'
import type { User } from './db/schema'

export type Variables = {
  user: User
  requestId: string
}
export type Env = {
  Variables: Variables
  Bindings: {
    DATABASE_URL: string
    JWT_SECRET: string
  }
}

// src/middleware/auth.ts
import { createMiddleware } from 'hono/factory'
import { HTTPException } from 'hono/http-exception'
import { verify } from 'hono/jwt'
import { db } from '../db'
import { users } from '../db/schema'
import { eq } from 'drizzle-orm'
import type { Env } from '../types'

export const authMiddleware = createMiddleware<Env>(async (c, next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '')
  if (!token) throw new HTTPException(401, { message: 'No token provided' })

  const payload = await verify(token, c.env.JWT_SECRET).catch(() => {
    throw new HTTPException(401, { message: 'Invalid token' })
  })

  const user = await db.select().from(users).where(eq(users.id, payload.sub as string)).get()
  if (!user) throw new HTTPException(401, { message: 'User not found' })

  c.set('user', user)
  await next()
})
```

---

## DRIZZLE SCHEMA + QUERIES

```typescript
// src/db/schema.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'
import { createId } from '@paralleldrive/cuid2'

export const users = sqliteTable('users', {
  id:        text('id').primaryKey().$defaultFn(() => createId()),
  email:     text('email').notNull().unique(),
  name:      text('name').notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
})

export const posts = sqliteTable('posts', {
  id:        text('id').primaryKey().$defaultFn(() => createId()),
  title:     text('title').notNull(),
  body:      text('body').notNull(),
  authorId:  text('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
})

// src/db/index.ts
import { drizzle } from 'drizzle-orm/bun-sqlite'
import { Database } from 'bun:sqlite'
import * as schema from './schema'

const sqlite = new Database(process.env.DATABASE_URL ?? 'dev.db')
export const db = drizzle(sqlite, { schema })
```

---

## ROUTE + RPC MODE

```typescript
// src/routes/users.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'
import { db } from '../db'
import { users } from '../db/schema'
import { eq } from 'drizzle-orm'
import { authMiddleware } from '../middleware/auth'
import type { Env } from '../types'

const createUserSchema = z.object({
  email: z.string().email(),
  name:  z.string().min(2).max(100),
})

export const usersRouter = new Hono<Env>()
  .get('/', authMiddleware, async (c) => {
    const all = await db.select().from(users).all()
    return c.json({ data: all })
  })
  .post('/', zValidator('json', createUserSchema), async (c) => {
    const body = c.req.valid('json')
    const user = await db.insert(users).values(body).returning().get()
    return c.json({ data: user }, 201)
  })
  .get('/:id', authMiddleware, async (c) => {
    const user = await db.select().from(users).where(eq(users.id, c.req.param('id'))).get()
    if (!user) return c.json({ error: 'Not found' }, 404)
    return c.json({ data: user })
  })

// src/index.ts
import { Hono } from 'hono'
import { logger } from 'hono/logger'
import { cors } from 'hono/cors'
import { usersRouter } from './routes/users'

const app = new Hono()
  .use('*', logger())
  .use('*', cors())
  .route('/api/users', usersRouter)

// RPC-safe export
export type AppType = typeof app
export default app
```

---

## HONO RPC CLIENT

```typescript
// client.ts (frontend/other service)
import { hc } from 'hono/client'
import type { AppType } from './src/index'

const client = hc<AppType>('http://localhost:3000')

// Fully typed — no manual types needed
const res = await client.api.users.$get()
const { data } = await res.json()
//      ^? User[]
```

---

## ROUTING TABLE

| Method | Path | Middleware | Action |
|--------|------|-----------|--------|
| GET | /api/users | auth | List all users |
| POST | /api/users | zod body | Create user |
| GET | /api/users/:id | auth | Get user by ID |
| PUT | /api/users/:id | auth + zod | Update user |
| DELETE | /api/users/:id | auth | Delete user |
| POST | /api/auth/login | zod body | Issue JWT |
| POST | /api/auth/refresh | — | Refresh token |
| GET | /api/posts | — | Public post list |
| POST | /api/posts | auth + zod | Create post |
| GET | /health | — | Liveness probe |

---

## QUALITY GATES
- [ ] `bun tsc --noEmit` passes with zero errors
- [ ] All route inputs validated by Zod (`zValidator`)
- [ ] `AppType` exported — client is fully type-safe
- [ ] No `any` casts in route handlers
- [ ] Every protected route uses `authMiddleware`
- [ ] All env vars validated in `env.ts` at startup
- [ ] Drizzle migrations committed and up-to-date
- [ ] `bun test` passes with ≥80% coverage on routes
- [ ] Error responses follow `{ error: string }` shape consistently

---

## FORBIDDEN
- ❌ Raw `fetch` inside route handlers — create a service layer
- ❌ `c.set('user', data as any)` — always type `Variables`
- ❌ Mutations without Zod validation on input
- ❌ `process.env.X` without the `env.ts` guard
- ❌ Returning raw Drizzle error messages to the client
- ❌ Embedding business logic directly in route handlers
- ❌ `console.log` in production code — use structured logger
