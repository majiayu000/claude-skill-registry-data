---
name: oRPC Dedupe Middleware
description: Enhance oRPC middleware performance by avoiding redundant executions.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Dedupe Middleware

Optimize middleware for fast and efficient repeated execution.

## Problem

When a procedure calls another procedure, overlapping middleware may run in both. Similarly, `.use(auth).router(router)` may run `auth` multiple times.

## Solution

Track middleware execution via `context` to prevent duplication:

```ts
const dbProvider = os
  .$context<{ db?: Awaited<ReturnType<typeof connectDb>> }>()
  .middleware(async ({ context, next }) => {
    const db = context.db ?? await connectDb()
    return next({ context: { db } })
  })
```

Now `dbProvider` can be safely applied multiple times without duplicating the connection:

```ts
const foo = os.use(dbProvider).handler(({ context }) => 'Hello World')

const bar = os.use(dbProvider).handler(({ context }) => {
  const result = call(foo, 'input', { context })
  return 'Hello World'
})

const router = os
  .use(dbProvider)
  .use(({ next }) => next())
  .router({ foo, bar })
```

## Built-in Dedupe

oRPC auto-dedupes middleware when the router's middlewares are a **subset** of the **leading** procedure middlewares and appear in the **same order**.

```ts
const router = os.use(logging).use(dbProvider).router({
  // ✅ Deduplicated:
  ping: os.use(logging).use(dbProvider).use(auth).handler(() => 'ping'),
  pong: os.use(logging).use(dbProvider).handler(() => 'pong'),

  // ⛔ Not deduplicated:
  diff_subset: os.use(logging).handler(() => 'ping'),
  diff_order: os.use(dbProvider).use(logging).handler(() => 'pong'),
  diff_leading: os.use(monitor).use(logging).use(dbProvider).handler(() => 'bar'),
})
```

### Configuration

Disable with `.$config`:

```ts
const base = os.$config({ dedupeLeadingMiddlewares: false })
```
