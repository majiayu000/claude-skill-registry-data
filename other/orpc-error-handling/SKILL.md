---
name: oRPC Error Handling
description: Manage errors in oRPC using both traditional and type-safe strategies.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Error Handling in oRPC

oRPC offers a robust error handling system. You can throw standard JavaScript errors or use the specialized `ORPCError` class.

> The `ORPCError.data` property is sent to the client. Avoid including sensitive information.

## Normal Approach

```ts
const rateLimit = os.middleware(async ({ next }) => {
  throw new ORPCError('RATE_LIMITED', {
    message: 'You are being rate limited',
    data: { retryAfter: 60 }
  })
  return next()
})

const example = os
  .use(rateLimit)
  .handler(async ({ input }) => {
    throw new ORPCError('NOT_FOUND')
    throw new Error('Something went wrong') // → INTERNAL_SERVER_ERROR
  })
```

## Type-Safe Error Handling

```ts
import { os } from '@orpc/server'
import * as z from 'zod'

const base = os.errors({
  RATE_LIMITED: {
    data: z.object({ retryAfter: z.number() }),
  },
  UNAUTHORIZED: {},
})

const rateLimit = base.middleware(async ({ next, errors }) => {
  throw errors.RATE_LIMITED({
    message: 'You are being rate limited',
    data: { retryAfter: 60 }
  })
  return next()
})

const example = base
  .use(rateLimit)
  .errors({
    NOT_FOUND: { message: 'The resource was not found' },
  })
  .handler(async ({ input, errors }) => {
    throw errors.NOT_FOUND()
  })
```

## Combining Both Approaches

When you throw an `ORPCError` and `code`, `status`, and `data` match a defined error, oRPC treats it as if you used `errors.[code]`.

```ts
const rateLimit = base.middleware(async ({ next, errors }) => {
  // Both are equivalent:
  throw errors.RATE_LIMITED({ data: { retryAfter: 60 } })
  throw new ORPCError('RATE_LIMITED', { data: { retryAfter: 60 } })
  return next()
})
```
