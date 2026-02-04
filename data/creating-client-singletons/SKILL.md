---
name: creating-client-singletons
description: Prevent multiple PrismaClient instances that exhaust connection pools causing P1017 errors. Use when creating PrismaClient, exporting database clients, setting up Prisma in new files, or encountering connection pool errors. Critical for serverless environments.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# PrismaClient Singleton Pattern

Teaches global singleton pattern to prevent multiple PrismaClient instances from exhausting database connection pools.

---

**Role:** Teach proper PrismaClient instantiation and export via global singleton pattern to prevent connection pool exhaustion, P1017 errors, and serverless deployment failures.

**When to Activate:** Creating PrismaClient instances, setting up database clients/exports, encountering P1017 errors, working with serverless environments (Next.js, Lambda, Vercel), or reviewing @prisma/client code.

---

## Problem & Solution

**Problem:** Creating multiple `new PrismaClient()` instances (the #1 Prisma violation) creates separate connection pools causing: pool exhaustion/P1017 errors, performance degradation, serverless failures (Lambda instances × pool size = disaster), and memory waste. Critical: 80% of AI agents in testing created multiple instances causing production failures.

**Solution:** Use global singleton pattern with module-level export: (1) check if PrismaClient exists globally, (2) create if none exists, (3) export for module reuse, (4) never instantiate in functions/classes. Supports module-level singletons (Node.js), global singletons (serverless/hot-reload), test patterns, and pool configuration.

---

## Implementation Workflow

**Phase 1 — Assess:** Grep for `@prisma/client` imports and `new PrismaClient()` calls; identify environment type (hot-reload vs. serverless vs. traditional Node.js vs. tests).

**Phase 2 — Implement:** Choose pattern based on environment; create/update client export (`lib/db.ts` or `lib/prisma.ts`) using global singleton check; update all imports to use singleton; remove duplicate instantiations.

**Phase 3 — Validate:** Grep for `new PrismaClient()` (

should appear once only); test hot reload; verify no P1017 errors; check database connection count; monitor production deployment and logs.

---

## Examples

### Module-Level Singleton (Traditional Node.js)

**File: `lib/db.ts`**

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();
export default prisma;
```

**Usage:** `import prisma from '@/lib/db'` — works because module loads once in Node.js, creating single shared instance.

---

### Global Singleton (Next.js/Hot Reload)

**File: `lib/prisma.ts`**

```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined };
export const prisma = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

**Why:** `globalThis` survives hot module reload; development reuses client across reloads; production creates clean instance per deployment; prevents "too many clients" during development.

---

### Anti-Pattern: Function-Scoped Creation

**WRONG:**

```typescript
async function getUsers() {
  const prisma = new PrismaClient(); // ❌ New pool every call
  const users = await prisma.user.findMany();
  await prisma.$disconnect();
  return users;
}
```

**Problems:** New connection pool per function call; connection overhead kills performance; pool never warms up; exhausts connections under load.

**Fix:** `import prisma from '@/lib/db'` and use it directly without creating new instances.

---

## Reference Files

- **Serverless Pattern:** `references/serverless-pattern.md` — Next.js App Router, Vercel, AWS Lambda configurations
- **Test Pattern:** `references/test-pattern.md` — test setup, mocking, isolation strategies
- **Common Scenarios:** `references/common-scenarios.md` — codebase conversion, P1017 troubleshooting, configuration

Load when working with serverless, writing tests, or troubleshooting specific issues.

---

## Constraints

**MUST:** Create PrismaClient exactly

once; export from centralized module (`lib/db.ts`); use global singleton in hot-reload environments; import singleton in all database-access files; never instantiate inside functions or classes.

**SHOULD:** Place in `lib/db.ts`, `lib/prisma.ts`, or `src/db.ts`; configure logging based on NODE_ENV; set connection pool size for deployment; use TypeScript; document connection configuration.

**NEVER:** Create PrismaClient in route handlers, API endpoints, service functions, test files, utility functions; create multiple instances "just to be safe"; disconnect/reconnect repeatedly.

---

## Validation

After implementing:

| Check              | Command/Method                                                   | Expected                                                                         | Issue                                    |
| ------------------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------- |
| Multiple instances | `grep -r "new PrismaClient()" --include="*.ts" --include="*.js"` | Exactly one occurrence (singleton file only)                                     | Consolidate to single singleton          |
| Import patterns    | `grep -r "from '@prisma/client'"`                                | Most imports from singleton module; only singleton imports from `@prisma/client` | Update imports to use singleton          |
| Connection pool    | Monitor during development hot reload                            | Connection count stays constant (not growing)                                    | Global singleton pattern not working     |
| Production errors  | Check logs for P1017                                             | Zero connection pool errors                                                      | Check serverless connection_limit config |
| Test isolation     | Run test suite                                                   | Tests pass; no connection errors                                                 | Ensure tests import singleton            |

---

## Standard Client Export

**TypeScript:**

```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined };
export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

**JavaScript:**

```javascript
const { PrismaClient } = require('@prisma/client');
const globalForPrisma = globalThis;
const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
module.exports = prisma;
```

---

## Quick Reference

**Setup Checklist:**

- [ ] Create `lib/db.ts` or `lib/prisma.ts`; use global singleton pattern (hot reload environments); export single instance; configure logging by NODE_ENV; set connection_limit for serverless; import singleton in all files; never create PrismaClient elsewhere; validate with grep (one instance); test hot reload; monitor production connections

**Red Flags (Implement Singleton Immediately):**

- Multiple `new PrismaClient()` in grep results; P1017 errors in logs; growing connection count during development; different files importing from `@prisma/client`; PrismaClient creation inside functions; test files creating own clients

## Related Skills

**TypeScript Type Safety:**

- If using type guards for singleton validation, use the using-type-guards skill from typescript for type narrowing patterns
