---
name: oRPC Server-Side Clients
description: Call your oRPC procedures in the same environment as your server like native functions.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Server-Side Clients

Call your [procedures](/docs/procedure) in the same environment as your server, no proxies required, like native functions.

## Calling Procedures

### Using `.callable`

```ts
import { os } from '@orpc/server'
import * as z from 'zod'

const getProcedure = os
  .input(z.object({ id: z.string() }))
  .handler(async ({ input }) => ({ id: input.id }))
  .callable({
    context: {} // Initial context if needed
  })

const result = await getProcedure({ id: '123' })
```

### Using the `call` Utility

```ts
import * as z from 'zod'
import { call, os } from '@orpc/server'

const getProcedure = os
  .input(z.object({ id: z.string() }))
  .handler(async ({ input }) => ({ id: input.id }))

const result = await call(getProcedure, { id: '123' }, {
  context: {}
})
```

## Router Client

```ts
import { createRouterClient, os } from '@orpc/server'

const ping = os.handler(() => 'pong')
const pong = os.handler(() => 'ping')

const client = createRouterClient({ ping, pong }, {
  context: {}
})

const result = await client.ping()
```

### Client Context

```ts
interface ClientContext { cache?: boolean }

const ping = os.handler(() => 'pong')
const pong = os.handler(() => 'ping')

const client = createRouterClient({ ping, pong }, {
  context: ({ cache }: ClientContext) => {
    if (cache) return {} // context when cache enabled
    return {} // context when cache disabled
  }
})

const result = await client.ping(undefined, { context: { cache: true } })
```

## Lifecycle

```mermaid
sequenceDiagram
  actor A1 as Client
  participant P1 as Error Validator
  participant P2 as Input/Output Validator
  participant P3 as Handler

  A1 ->> P2: input, signal, lastEventId
  P2 ->> P2: Validate Input
  P2 ->> P3: validated input
  P3 ->> P3: handle
  P3 ->> P2: error/output
  P2 ->> P2: validate output
  P2 ->> P1: validate error
  P1 ->> A1: validated error/output
```

### Middlewares Order

Apply this to ensure all middlewares run after input validation and before output validation:

```ts
const base = os.$config({
  initialInputValidationIndex: Number.NEGATIVE_INFINITY,
  initialOutputValidationIndex: Number.NEGATIVE_INFINITY,
})
```
