---
name: oRPC Middleware
description: Middleware enables reusable and extensible procedures in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Middleware in oRPC

Middleware is a powerful feature in oRPC that enables reusable and extensible procedures.

## Overview

```ts
const authMiddleware = os
  .$context<{ something?: string }>() // define dependent-context
  .middleware(async ({ context, next }) => {
    // before
    const result = await next({
      context: { user: { id: 1, name: 'John' } }
    })
    // after
    return result
  })

const example = os
  .use(authMiddleware)
  .handler(async ({ context }) => {
    const user = context.user
  })
```

## Inline Middleware

```ts
const example = os
  .use(async ({ context, next }) => {
    return next()
  })
  .handler(async ({ context }) => {
    // Handler logic
  })
```

## Middleware Context

```ts
const setting = os
  .use(async ({ context, next }) => {
    return next({
      context: { auth: await auth() }
    })
  })
  .use(async ({ context, next }) => {
    if (!context.auth) {
      throw new ORPCError('UNAUTHORIZED')
    }
    return next({ context: { auth: context.auth } })
  })
  .handler(async ({ context }) => {
    console.log(context.auth)
  })
```

## Middleware Input

```ts
const canUpdate = os.middleware(async ({ context, next }, input: number) => {
  return next()
})

const ping = os
  .input(z.number())
  .use(canUpdate)
  .handler(async ({ input }) => {})

// Mapping input
const pong = os
  .input(z.object({ id: z.number() }))
  .use(canUpdate, input => input.id)
  .handler(async ({ input }) => {})
```

Use `.mapInput` to adapt middleware:

```ts
const mappedCanUpdate = canUpdate.mapInput((input: { id: number }) => input.id)
```

## Middleware Output

```ts
const cacheMid = os.middleware(async ({ context, next, path }, input, output) => {
  const cacheKey = path.join('/') + JSON.stringify(input)

  if (db.has(cacheKey)) {
    return output(db.get(cacheKey))
  }

  const result = await next({})
  db.set(cacheKey, result.output)
  return result
})
```

## Concatenation

```ts
const concatMiddleware = aMiddleware
  .concat(os.middleware(async ({ next }) => next()))
  .concat(anotherMiddleware)
```

## Built-in Middlewares

```ts
import { onError, onFinish, onStart, onSuccess } from '@orpc/server'

const ping = os
  .use(onStart(() => {}))
  .use(onSuccess(() => {}))
  .use(onError(() => {}))
  .use(onFinish(() => {}))
  .handler(async ({ context }) => {})
```
