---
name: nitro-testing
description: Test Nuxt 3 / Nitro API handlers with real PostgreSQL, transaction rollback isolation, and typed factories. No mocks, real SQL.
---

# Nitro API Testing Patterns

Test Nitro API handlers with a real PostgreSQL database using transaction rollback isolation. Each test runs in a transaction that auto-rolls back, providing complete isolation without cleanup overhead.

## When to Use This Skill

Use this skill when:
- Testing Nuxt 3 / Nitro API handlers
- Using Kysely or another query builder with PostgreSQL
- Need real database testing (not mocks)
- Want fast, isolated tests without truncation

## Reference Files

- [transaction-rollback.md](./transaction-rollback.md) - Core isolation pattern with Vitest fixtures
- [test-utils.md](./test-utils.md) - Mock events, stubs, and assertion helpers
- [factories.md](./factories.md) - Transaction-bound factory pattern
- [vitest-config.md](./vitest-config.md) - Vitest configuration for Nitro
- [ci-setup.md](./ci-setup.md) - GitHub Actions with PostgreSQL service
- [async-testing.md](./async-testing.md) - Testing background tasks and automations

## Example Files

- [test-utils-index.ts](./examples/test-utils-index.ts) - Complete test utilities module
- [global-setup.ts](./examples/global-setup.ts) - Database reset and migration
- [setup.ts](./examples/setup.ts) - Per-file setup with stubs
- [handler.test.ts](./examples/handler.test.ts) - Example API handler test
- [vitest.config.ts](./examples/vitest.config.ts) - Vitest configuration

## Core Concept: Transaction Rollback

Instead of truncating tables between tests, each test runs inside a database transaction that rolls back at the end:

```typescript
// Each test gets isolated factories and db access
test("creates user", async ({ factories, db }) => {
  const user = await factories.user({ email: "test@example.com" });

  // Test your handler
  const event = mockPost({}, { name: "New Item" });
  const result = await handler(event);

  // Verify in database
  const saved = await db.selectFrom("item").selectAll().execute();
  expect(saved).toHaveLength(1);
});
// Transaction auto-rolls back - no cleanup needed
```

Benefits:
- **Fast**: No DELETE/TRUNCATE between tests
- **Isolated**: Tests can't affect each other
- **Real SQL**: Catches actual database issues
- **Simple**: No manual cleanup

## Quick Setup

### 1. Install Dependencies

```bash
yarn add -D vitest @vitest/coverage-v8
```

### 2. Create Test Utils Structure

```
server/
  test-utils/
    index.ts        # Factories, fixtures, mock helpers
    global-setup.ts # Runs once: reset DB, run migrations
    setup.ts        # Runs per-file: stub auto-imports
```

### 3. Configure Vitest

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    globalSetup: ["./server/test-utils/global-setup.ts"],
    setupFiles: ["./server/test-utils/setup.ts"],
  },
  resolve: {
    alias: {
      "~": path.resolve(__dirname),
    },
  },
});
```

### 4. Write Tests

```typescript
// server/api/users/index.post.test.ts
import { describe, test, expect, mockPost, expectHttpError } from "~/server/test-utils";
import handler from "./index.post";

describe("POST /api/users", () => {
  test("creates user with valid data", async ({ factories: _, db }) => {
    const event = mockPost({}, {
      email: "new@example.com",
      name: "New User"
    });
    const result = await handler(event);

    expect(result.id).toBeDefined();
    expect(result.email).toBe("new@example.com");

    // Verify persisted
    const saved = await db
      .selectFrom("user")
      .where("id", "=", result.id)
      .selectAll()
      .executeTakeFirst();
    expect(saved?.name).toBe("New User");
  });

  test("throws 400 for missing email", async ({ factories: _ }) => {
    const event = mockPost({}, { name: "No Email" });
    await expectHttpError(handler(event), { statusCode: 400 });
  });
});
```

## Key Patterns

### Mock Event Helpers

```typescript
// GET with route params and query
const event = mockGet({ id: 123 }, { include: "details" });

// POST with body
const event = mockPost({}, { name: "Test", status: "active" });

// PATCH with route params and body
const event = mockPatch({ id: 123 }, { status: "completed" });

// DELETE with route params
const event = mockDelete({ id: 123 });
```

### Factory Pattern

```typescript
test("lists user's projects", async ({ factories }) => {
  // Factories are transaction-bound - auto-rolled back
  const user = await factories.user();
  const project1 = await factories.project({ ownerId: user.id });
  const project2 = await factories.project({ ownerId: user.id });

  const event = mockGet({ userId: user.id });
  const result = await handler(event);

  expect(result).toHaveLength(2);
});
```

### Testing with Related Data

```typescript
test("returns task with job details", async ({ factories }) => {
  // Factories auto-create dependencies
  const job = await factories.job(); // Creates project automatically
  const task = await factories.task({ jobId: job.id });

  const event = mockGet({ id: task.id });
  const result = await handler(event);

  expect(result.job.id).toBe(job.id);
  expect(result.job.project).toBeDefined();
});
```

### Testing Error Cases

```typescript
test("returns 404 for non-existent resource", async ({ factories: _ }) => {
  const event = mockGet({ id: 999999 });
  await expectHttpError(handler(event), {
    statusCode: 404,
    message: "Not found",
  });
});

test("returns 400 for invalid input", async ({ factories: _ }) => {
  const event = mockPost({}, { invalidField: true });
  await expectHttpError(handler(event), { statusCode: 400 });
});
```

## Auto-Import Stubs

The setup file stubs Nuxt/Nitro auto-imports:

| Stub | Purpose |
|------|---------|
| `defineEventHandler` | Unwraps to return handler directly |
| `getUserSession` | Returns test user (configurable) |
| `useDatabase` | Returns test transaction |
| `createError` | Creates H3-style errors |
| `getValidatedQuery` | Validates mock query params |
| `readValidatedBody` | Validates mock body |
| `getRouterParam` | Returns mock route params |

## Key Gotchas

1. **Always destructure `factories`** - Even if unused, it sets up the transaction:
   ```typescript
   test("...", async ({ factories: _ }) => { ... });
   ```

2. **Don't use top-level db imports** - Use the `db` fixture instead:
   ```typescript
   // ❌ Wrong - uses real db, not transaction
   import { db } from "../utils/db";

   // ✅ Right - uses test transaction
   test("...", async ({ db }) => { ... });
   ```

3. **Nested transactions work** - Code that calls `db.transaction()` works because we patch the prototype

4. **Test file location** - Co-locate with handlers: `handler.ts` → `handler.test.ts`

5. **Separate test database** - Always use a dedicated test DB (`myapp-test`, not `myapp`)

6. **CI needs PostgreSQL service** - See [ci-setup.md](./ci-setup.md) for GitHub Actions config
