---
name: oRPC Client-Side Clients
description: Call your oRPC procedures remotely as if they were local functions.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Client-Side Clients

Call your [procedures](/docs/procedure) remotely as if they were local functions.

## Installation

```sh
npm install @orpc/client@latest
```

## Creating a Client

Uses [RPCLink](/docs/client/rpc-link); ensure your server uses `RPCHandler` or follows the [RPC Protocol](/docs/advanced/rpc-protocol).

```ts
import { createORPCClient, onError } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import { RouterClient } from '@orpc/server'
import { ContractRouterClient } from '@orpc/contract'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  headers: () => ({ authorization: 'Bearer token' }),
  interceptors: [onError(error => console.error(error))],
})

const client: RouterClient<typeof router> = createORPCClient(link)
// or with a contract:
const client: ContractRouterClient<typeof contract> = createORPCClient(link)
```

## Calling Procedures

```ts
const planet = await client.planet.find({ id: 1 })
```

## Merging Clients

```ts
const clientA: RouterClient<typeof routerA> = createORPCClient(linkA)
const clientB: RouterClient<typeof routerB> = createORPCClient(linkB)

export const orpc = { a: clientA, b: clientB }
```

## Type Utilities

```ts
import type {
  InferClientInputs, InferClientBodyInputs,
  InferClientOutputs, InferClientBodyOutputs,
  InferClientErrors, InferClientErrorUnion,
  InferClientContext
} from '@orpc/client'

type Inputs = InferClientInputs<typeof client>
type BodyInputs = InferClientBodyInputs<typeof client>
type Outputs = InferClientOutputs<typeof client>
type BodyOutputs = InferClientBodyOutputs<typeof client>
type Errors = InferClientErrors<typeof client>
type AllErrors = InferClientErrorUnion<typeof client>
type Context = InferClientContext<typeof client>
```

- `InferClientInputs` / `InferClientOutputs`: full input/output types per endpoint
- `InferClientBodyInputs` / `InferClientBodyOutputs`: only the `body` portion
- `InferClientErrors`: type-safe error map per endpoint
- `InferClientErrorUnion`: union of all possible errors
- `InferClientContext`: client context type
