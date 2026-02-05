---
name: configuring-serverless-clients
description: Configure PrismaClient for serverless (Next.js, Lambda, Vercel) with connection_limit=1 and global singleton pattern.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Serverless PrismaClient Configuration

Configure PrismaClient for serverless platforms to prevent connection pool exhaustion using connection limits and global singleton patterns.

## Activation Triggers

Deploy to Next.js (App/Pages Router), AWS Lambda, Vercel, or similar serverless platforms; encountering P1017 errors; files in app/, pages/api/, lambda/ directories.

## Problem & Solution

**Problem:** Each Lambda instance creates its own connection pool. Default unlimited pool × instances exhausts database (e.g., 10 instances × 10 connections = 100 connections).

**Solution:** Set `connection_limit=1` in DATABASE_URL; use global singleton to reuse client across invocations; consider PgBouncer for high concurrency.

## Configuration Workflow

**Phase 1—Environment:** Add `connection_limit=1` and `pool_timeout=20` to DATABASE_URL in .env; configure in Vercel dashboard if applicable.

**Phase 2—Client Singleton:** Create single global PrismaClient in `lib/prisma.ts`; use `globalThis` pattern (Next.js 13+ App Router), `global.prisma` pattern (Pages Router/Lambda), or initialize outside handler (Lambda standalone).

**Phase 3—Validation:** Verify DATABASE_URL contains connection parameters; confirm `new PrismaClient()` appears only in `lib/prisma.ts`; test with 10+ concurrent requests; monitor connection count.

## Implementation Patterns

### Next.js App Router (`lib/prisma.ts`)

```typescript
import { PrismaClient } from '@prisma/client';

const prismaClientSingleton = () => new PrismaClient();

declare const globalThis: {
  prismaGlobal: ReturnType<typeof prismaClientSingleton>;
} & typeof global;

const prisma = globalThis.prismaGlobal ?? prismaClientSingleton();

export default prisma;

if (process.env.NODE_ENV !== 'production') globalThis.prismaGlobal = prisma;
```

**Environment:** `DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=1&pool_timeout=20"`

**Usage in Server Action:**

```typescript
import prisma from '@/lib/prisma';

export async function createUser(formData: FormData) {
  'use server';
  return await prisma.user.create({
    data: {
      email: formData.get('email') as string,
      name: formData.get('name') as string,
    },
  });
}
```

### Next.js Pages Router / AWS Lambda (`lib/prisma.ts`)

```typescript
import { PrismaClient } from '@prisma/client';

declare global {
  var prisma: PrismaClient | undefined;
}

const prisma = global.prisma || new PrismaClient();
if (process.env.NODE_ENV !== 'production') global.prisma = prisma;

export default prisma;
```

**Lambda Handler:**

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

export const handler = async (event: any) => {
  const users = await prisma.user.findMany();
  return { statusCode: 200, body: JSON.stringify(users) };
  // Never call prisma.$disconnect() – reuse Lambda container connections
};
```

### With PgBouncer (High Concurrency)

Use when >50

concurrent requests or connection limits still cause issues.

```bash
DATABASE_URL="postgresql://user:pass@pgbouncer-host:6543/db?connection_limit=10&pool_timeout=20"
DIRECT_URL="postgresql://user:pass@direct-host:5432/db"
```

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

DATABASE_URL → PgBouncer (queries); DIRECT_URL → database (migrations).

## Requirements

**MUST:** Set `connection_limit=1` in DATABASE_URL; use global singleton (never `new PrismaClient()` in functions); create single `lib/prisma.ts` imported throughout; add `pool_timeout`.

**SHOULD:** Use PgBouncer for high concurrency (>50); monitor production connection count; set limit via URL parameter; reuse Lambda connections.

**NEVER:** Create `new PrismaClient()` in routes/handlers; use default pool size in serverless; call `$disconnect()` in handlers; deploy without limits; split instances across files.

## Common Mistakes

| Issue                          | Wrong                                                     | Right                                      |
| ------------------------------ | --------------------------------------------------------- | ------------------------------------------ |
| Connection in Constructor      | `new PrismaClient({ datasources: { db: { url: ... } } })` | Set `connection_limit=1` in DATABASE_URL   |
| Multiple Instances             | `const prisma = new PrismaClient()` inside functions      | Import singleton from `lib/prisma`         |
| Handler Disconnect             | `await prisma.$disconnect()` after query                  | Remove disconnect – reuse containers       |
| Missing TypeScript Declaration | `const prisma = global.prisma \|\| ...`                   | `declare global { var prisma: ... }` first |

## Validation Checklist

1. **Environment:** DATABASE_URL contains `connection_limit=1` and `pool_timeout`; verified in Vercel dashboard.
2. **Code:** `new PrismaClient()` appears exactly once in `lib/prisma.ts`; all other files import from it.
3. **Testing:** 10+ concurrent requests to staging; connection count stays ≤10-15; no P1017 errors.
4. **Monitoring:** Production alerts for connection exhaustion and timeout errors.

## Platform-Specific Notes

**Vercel:** Set environment variables in dashboard (

auto-encrypted); connection pooling shared across invocations; consider Vercel Postgres for built-in pooling.

**AWS Lambda:** Container reuse varies by traffic; cold starts create new instances; use provisioned concurrency for consistency; Lambda layers optimize Prisma binary size.

**Cloudflare Workers:** Standard PrismaClient unsupported (V8 isolates, not Node.js); use Data Proxy or D1.

**Railway/Render:** Apply `connection_limit=1` pattern; check platform docs for built-in pooling.

## Related Skills

**Next.js Integration:**

- If implementing authenticated data access layers in Next.js, use the securing-data-access-layer skill from nextjs-16 for verifySession() DAL patterns
- If securing server actions with database operations, use the securing-server-actions skill from nextjs-16 for authentication patterns

## References

- Next.js patterns: `references/nextjs-patterns.md`
- Lambda optimization: `references/lambda-patterns.md`
- PgBouncer setup: `references/pgbouncer-guide.md`
