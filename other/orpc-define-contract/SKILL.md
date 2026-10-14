---
name: oRPC Define Contract
description: Define a contract for contract-first development in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Define Contract

**Contract-first development** is a design pattern where you define the API contract before writing implementation code.

## Installation

```sh
npm install @orpc/contract@latest
```

## Procedure Contract

```ts
import { oc } from '@orpc/contract'
import * as z from 'zod'

export const exampleContract = oc
  .input(z.object({ name: z.string(), age: z.number().int().min(0) }))
  .output(z.object({ id: z.number().int().min(0), name: z.string(), age: z.number().int().min(0) }))
```

## Contract Router

```ts
export const routerContract = {
  example: exampleContract,
  nested: { example: exampleContract },
}
```

## Full Example

```ts
import * as z from 'zod'
import { oc } from '@orpc/contract'

export const PlanetSchema = z.object({
  id: z.number().int().min(1),
  name: z.string(),
  description: z.string().optional(),
})

export const listPlanetContract = oc
  .input(z.object({
    limit: z.number().int().min(1).max(100).optional(),
    cursor: z.number().int().min(0).default(0),
  }))
  .output(z.array(PlanetSchema))

export const findPlanetContract = oc
  .input(PlanetSchema.pick({ id: true }))
  .output(PlanetSchema)

export const createPlanetContract = oc
  .input(PlanetSchema.omit({ id: true }))
  .output(PlanetSchema)

export const contract = {
  planet: {
    list: listPlanetContract,
    find: findPlanetContract,
    create: createPlanetContract,
  },
}
```

## Utilities

```ts
import type { InferContractRouterInputs, InferContractRouterOutputs } from '@orpc/contract'

export type Inputs = InferContractRouterInputs<typeof contract>
export type Outputs = InferContractRouterOutputs<typeof contract>

type FindPlanetInput = Inputs['planet']['find']
type FindPlanetOutput = Outputs['planet']['find']
```
