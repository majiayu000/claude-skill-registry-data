---
name: tpl-fullstack-t3-stack
description: Template do pack (fullstack/01-t3-stack.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/01-t3-stack.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: T3 Stack App (Next.js + tRPC + Prisma + NextAuth)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/01-t3-stack.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Framework:** Next.js 15 (App Router)
- **API Layer:** tRPC v11
- **ORM:** Prisma 5 + PostgreSQL
- **Auth:** NextAuth.js v5 (Auth.js)
- **Styling:** Tailwind CSS v3 + shadcn/ui
- **Language:** TypeScript 5.x (strict)
- **Testing:** Vitest + @testing-library/react
- **Deployment:** Vercel + Neon (DB)

---

## PROJECT STRUCTURE
```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── api/
│   │   ├── auth/
│   │   │   └── [...nextauth]/
│   │   │       └── route.ts         # NextAuth handler
│   │   └── trpc/
│   │       └── [trpc]/
│   │           └── route.ts         # tRPC HTTP handler
│   └── dashboard/
│       └── page.tsx
├── server/
│   ├── auth.ts                      # NextAuth config
│   ├── db.ts                        # Prisma client singleton
│   └── api/
│       ├── root.ts                  # AppRouter assembly
│       ├── trpc.ts                  # Context + procedure builders
│       └── routers/
│           ├── user.ts
│           └── post.ts
├── trpc/
│   ├── server.ts                    # Server-side caller
│   └── client.tsx                   # TRPCReactProvider + hooks
├── components/
│   └── ui/                          # shadcn/ui components
└── lib/
    └── utils.ts
prisma/
└── schema.prisma
```

---

## ARCHITECTURE RULES
1. **Context carries auth session** — `createTRPCContext` reads NextAuth session; attach to ctx for all procedures.
2. **`protectedProcedure` enforces auth** — every mutation that touches user data uses `protectedProcedure`, never `publicProcedure`.
3. **End-to-end type safety** — never use `as` casts on tRPC responses; let inference flow from router → client.
4. **Server Components call tRPC directly** — use server-side caller (`server.ts`), not fetch; do not hit HTTP in RSC.
5. **Prisma client is a singleton** — use `globalThis.__prisma` pattern to avoid hot-reload connection exhaustion.
6. **Input validated by Zod** — every router procedure has `.input(zSchema)`.
7. **No business logic in route handlers** — logic lives in tRPC routers; `app/api/` contains only minimal glue.

---

## tRPC SETUP

```typescript
// src/server/api/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server'
import { ZodError } from 'zod'
import superjson from 'superjson'
import type { Session } from 'next-auth'
import { auth } from '../auth'
import { db }   from '../db'

interface CreateContextOptions { session: Session | null }

export const createTRPCContext = async (): Promise<CreateContextOptions & { db: typeof db }> => {
  const session = await auth()
  return { session, db }
}

const t = initTRPC.context<typeof createTRPCContext>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError: error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    }
  },
})

export const createCallerFactory = t.createCallerFactory
export const createTRPCRouter   = t.router
export const publicProcedure    = t.procedure

export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' })
  }
  return next({ ctx: { ...ctx, session: ctx.session } })
})
```

---

## ROUTER DEFINITION

```typescript
// src/server/api/routers/post.ts
import { z } from 'zod'
import { createTRPCRouter, protectedProcedure, publicProcedure } from '../trpc'

export const postRouter = createTRPCRouter({
  list: publicProcedure
    .input(z.object({ limit: z.number().min(1).max(100).default(20), cursor: z.string().optional() }))
    .query(async ({ ctx, input }) => {
      const posts = await ctx.db.post.findMany({
        take:    input.limit + 1,
        cursor:  input.cursor ? { id: input.cursor } : undefined,
        orderBy: { createdAt: 'desc' },
        include: { author: { select: { id: true, name: true, image: true } } },
      })
      const nextCursor = posts.length > input.limit ? posts.pop()!.id : undefined
      return { posts, nextCursor }
    }),

  create: protectedProcedure
    .input(z.object({ title: z.string().min(1).max(200), body: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.post.create({
        data: { ...input, authorId: ctx.session.user.id },
      })
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string().cuid() }))
    .mutation(async ({ ctx, input }) => {
      const post = await ctx.db.post.findUnique({ where: { id: input.id } })
      if (!post) throw new TRPCError({ code: 'NOT_FOUND' })
      if (post.authorId !== ctx.session.user.id) throw new TRPCError({ code: 'FORBIDDEN' })
      return ctx.db.post.delete({ where: { id: input.id } })
    }),
})
```

---

## CLIENT USAGE (React Hooks)

```typescript
// src/trpc/client.tsx
'use client'
import { createTRPCReact } from '@trpc/react-query'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { httpBatchLink } from '@trpc/client'
import superjson from 'superjson'
import type { AppRouter } from '../server/api/root'

export const trpc = createTRPCReact<AppRouter>()

// In a component:
function PostList() {
  const { data, isLoading } = trpc.post.list.useQuery({ limit: 10 })
  const createPost = trpc.post.create.useMutation({
    onSuccess: () => utils.post.list.invalidate(),
  })
  const utils = trpc.useUtils()

  if (isLoading) return <p>Loading...</p>
  return (
    <ul>
      {data?.posts.map(p => <li key={p.id}>{p.title}</li>)}
    </ul>
  )
}

// Server Component (no HTTP — direct DB call)
// src/app/dashboard/page.tsx
import { createCaller } from '~/server/api/root'
import { createTRPCContext } from '~/server/api/trpc'

export default async function DashboardPage() {
  const ctx    = await createTRPCContext()
  const caller = createCaller(ctx)
  const { posts } = await caller.post.list({ limit: 5 })
  // posts is fully typed PostWithAuthor[]
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

---

## ROUTING TABLE

| Procedure | Type | Auth | Action |
|-----------|------|------|--------|
| `post.list` | query | No | Paginated post list |
| `post.byId` | query | No | Single post |
| `post.create` | mutation | Yes | Create post |
| `post.update` | mutation | Yes (owner) | Update post |
| `post.delete` | mutation | Yes (owner) | Delete post |
| `user.me` | query | Yes | Current user profile |
| `user.update` | mutation | Yes | Update profile |
| `user.listByAdmin` | query | Yes (admin) | Admin user list |
| `auth/signin` | HTTP GET | No | NextAuth sign-in page |
| `auth/callback` | HTTP GET | No | NextAuth OAuth callback |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors
- [ ] `trpc.post.create.useMutation` result type matches Prisma return type (no `as`)
- [ ] All mutations use `protectedProcedure`
- [ ] Prisma `schema.prisma` validated with `prisma validate`
- [ ] `pytest run` / `vitest run` — all tests pass
- [ ] No `fetch('/api/trpc/...')` calls — use tRPC hooks only
- [ ] Server Components use direct caller, not HTTP
- [ ] `.env` file has all vars declared in `env.js` (T3 env validation)
- [ ] `prisma migrate deploy` tested against staging DB

---

## FORBIDDEN
- ❌ Raw `fetch` to tRPC endpoints from client components — use `trpc.*` hooks
- ❌ Direct `db.*` calls in Server/Client components — go through tRPC
- ❌ Mutations without Zod `.input()` validation
- ❌ `protectedProcedure` in public API paths (naming confusion — use separate routers)
- ❌ `any` casts on tRPC return types
- ❌ Creating multiple Prisma clients — one singleton only
- ❌ Storing session data in localStorage — use NextAuth session cookies
- ❌ `"use client"` on pages that can be Server Components
