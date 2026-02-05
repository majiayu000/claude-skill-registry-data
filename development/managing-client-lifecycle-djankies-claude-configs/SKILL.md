---
name: managing-client-lifecycle
description: Manage PrismaClient lifecycle with graceful shutdown, proper disconnect timing, and logging configuration. Use when setting up application shutdown handlers, configuring logging for development or production, or implementing proper connection cleanup in Node.js servers, serverless functions, or test suites.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# PrismaClient Lifecycle Management

Teaches proper PrismaClient lifecycle patterns for connection cleanup and logging following Prisma 6 best practices.

**Activates when:** Setting up shutdown handlers (SIGINT, SIGTERM), configuring PrismaClient logging, implementing connection cleanup in servers/serverless/tests, writing test teardown logic, or user mentions "shutdown", "disconnect", "cleanup", "logging", "graceful exit".

**Why it matters:** Proper lifecycle management ensures clean connection closure on shutdown, prevents hanging connections from exhausting database resources, provides development/production visibility through logging, and prevents connection leaks in tests.

---

## Implementation Patterns

### Long-Running Servers (Express, Fastify, Custom HTTP)

```typescript
import express from 'express'
import { prisma } from './lib/prisma'

const app = express()
const server = app.listen(3000)

async function gracefulShutdown(signal: string) {
  console.log(`Received ${signal}, closing gracefully...`)
  server.close(async () => {
    await prisma.$disconnect()
    process.exit(0)
  })
  setTimeout(() => { process.exit(1) }, 10000) // Force exit if hung
}

process.on('SIGINT', () => gracefulShutdown('SIGINT'))
process.on('

SIGTERM', () => gracefulShutdown('SIGTERM'))
```

Close HTTP server first (stops new requests), then $disconnect() database, add 10s timeout to force exit if cleanup hangs. Fastify simplifies this with `fastify.addHook('onClose', () => prisma.$disconnect())`.

### Test Suites (Jest, Vitest, Mocha)

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

afterAll(async () => {
  await prisma.$disconnect();
});

beforeEach(async () => {
  await prisma.user.deleteMany(); // Clean data, NOT connections
});

test('creates user', async () => {
  const user = await prisma.user.create({
    data: { email: 'test@example.com', name: 'Test' },
  });
  expect(user.email).toBe('test@example.com');
});
```

Use single PrismaClient instance across all tests; $disconnect() only in afterAll(); clean database state between tests, not connections.

For Vitest setup configuration (setupFiles, global hooks), see `vitest-4/skills/configuring-vitest-4/SKILL.md`.

### Serverless Functions (AWS Lambda, Vercel, Cloudflare Workers)

**Do NOT disconnect in handlers** — breaks warm starts (connection setup every invocation). Use global singleton pattern with connection pooling managed by CLIENT-serverless-config. Exception: RDS Proxy with specific requirements may benefit from explicit $disconnect().

### Next.js

Development: No explicit disconnect needed; Next.js manages lifecycle. Production: Depends on deployment—follow CLIENT-serverless-config for serverless, server pattern for traditional deployment.

---

## Logging Configuration

| Environment     | Config                                    | Output                                                              |
| --------------- | ----------------------------------------- | ------------------------------------------------------------------- |
| **Development** | `log: ['query', 'info', 'warn', 'error']` | Every SQL query with parameters, connection events, warnings/errors |
| **Production**  | `log: ['warn                              |

', 'error']`| Only warnings and errors; reduced log volume, better performance |
| **Environment-based** |`log: process.env.NODE_ENV === 'production' ? ['warn', 'error'] : ['query', 'info', 'warn', 'error']` | Conditional verbosity |

**Custom event handling:**

```typescript
const prisma = new PrismaClient({
  log: [
    { emit: 'event', level: 'query' },
    { emit: 'event', level: 'error' },
    { emit: 'stdout', level: 'warn' },
  ],
});

prisma.$on('query', (e) => {
  console.log(`Query: ${e.query} (${e.duration}ms)`);
});

prisma.$on('error', (e) => {
  console.error('Prisma Error:', e);
});
```

---

## Constraints & Validation

**MUST:**

- Call $disconnect() in server shutdown handlers (SIGINT, SIGTERM); in test afterAll/global teardown; await completion before process.exit()
- Use environment-based logging (verbose dev, minimal prod)

**SHOULD:**

- Add 10s timeout to force exit if shutdown hangs
- Close HTTP server before disconnecting database
- Use framework hooks when available (Fastify onClose, NestJS onModuleDestroy)
- Log shutdown progress

**NEVER:**

- Disconnect in serverless function handlers (breaks warm starts)
- Disconnect between test cases (only in afterAll)
- Forget await on $disconnect()
- Exit process before $disconnect() completes

**Validation:**

- Manual: Start server, Ctrl+C, verify "Database connections closed" log and clean exit
- Tests: Run `npm test` — expect no "jest/vitest did not exit" warnings, no connection errors
- Leak detection: Run tests 10x — no "Too many connections" errors or timing degradation
- Logging dev: NODE_ENV=development, verify query logs appear on DB operations
- Logging prod: NODE_ENV=production, verify only warn/error logs appear, successful queries silent

---

## Common Issues & Solutions

| Issue                              | Cause                               | Solution                                                   |
| ---------------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| "jest/vitest did not exit" warning | Missing $disconnect() in afterAll() | Add `afterAll(async () => { await prisma.$disconnect() })` |

| "

Too many connections" in tests | New PrismaClient created per test file | Use global singleton pattern (see Vitest setup above) |
| Process hangs on shutdown | Forgot await on $disconnect() | Always `await prisma.$disconnect()` |
| Serverless cold starts very slow | Disconnecting in handler breaks warm starts | Remove $disconnect() from handler; use connection pooling |
| Connection pool exhausted after shutdown | $disconnect() called before server.close() | Reverse order: close server first, then disconnect |

---

## Framework-Specific Notes

**Express.js:** Use `server.close()` before `$disconnect()`; handle SIGINT + SIGTERM; add timeout for forced exit.

**Fastify:** Use `onClose` hook—framework handles signal listeners and ordering automatically.

**NestJS:** Implement `onModuleDestroy` lifecycle hook; use `@nestjs/terminus` for health checks; automatic cleanup via module system.

**Next.js:** Dev mode—no explicit disconnect needed. Production—depends on deployment (serverless: see CLIENT-serverless-config; traditional: use server pattern). Server Actions/API Routes—follow serverless pattern.

**Serverless (Lambda, Vercel, Cloudflare):** Default—do NOT disconnect in handlers. Exception—RDS Proxy with specific config. See CLIENT-serverless-config for connection management.

**Test Frameworks:** Jest—`afterAll()` in files or global teardown. Vitest—global `setupFiles`. Mocha—`after()` in root suite. Playwright—`globalTeardown` for E2E.

---

## Related Skills

- **CLIENT-singleton-pattern:** Ensuring single PrismaClient instance
- **CLIENT-serverless-config:** Serverless-specific connection management
- **PERFORMANCE-connection-pooling:** Optimizing connection pool size

**Next.js Integration:**

- If implementing data access layers with session verification, use the securing-data-access-layer skill from nextjs-16 for authenticated database patterns
