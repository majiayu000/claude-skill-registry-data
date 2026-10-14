---
name: oRPC Router
description: Understanding routers in oRPC — nestable objects composed of procedures.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Router in oRPC

Routers are simple, nestable objects composed of procedures.

## Overview

```ts
import { os } from '@orpc/server'

const ping = os.handler(async () => 'ping')
const pong = os.handler(async () => 'pong')

const router = {
  ping,
  pong,
  nested: { ping, pong }
}
```

## Extending Router

```ts
const router = os.use(requiredAuth).router({
  ping,
  pong,
  nested: { ping, pong }
})
```

> Avoid duplicate middleware execution. See [Dedupe Middleware](/docs/best-practices/dedupe-middleware).

## Lazy Router

```ts
// router.ts
const router = {
  ping,
  pong,
  planet: os.lazy(() => import('./planet'))
}
```

```ts
// planet.ts
export const listPlanet = os
  .input(z.object({ limit: z.number().optional() }))
  .handler(async ({ input }) => [{ id: 1, name: 'name' }])

export default {
  list: listPlanet,
}
```

Alternative using the standalone `lazy` helper (faster type inference):

```ts
import { lazy } from '@orpc/server'

const router = {
  ping,
  pong,
  planet: lazy(() => import('./planet'))
}
```

## Utilities

```ts
import type {
  InferRouterInputs, InferRouterOutputs,
  InferRouterInitialContexts, InferRouterCurrentContexts
} from '@orpc/server'

type Inputs = InferRouterInputs<typeof router>
type Outputs = InferRouterOutputs<typeof router>
type InitialContexts = InferRouterInitialContexts<typeof router>
type CurrentContexts = InferRouterCurrentContexts<typeof router>

type FindPlanetInput = Inputs['planet']['find']
type FindPlanetOutput = Outputs['planet']['find']
```
