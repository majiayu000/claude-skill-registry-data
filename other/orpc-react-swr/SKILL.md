---
name: oRPC React SWR Integration
description: Integrate oRPC with React SWR for efficient data fetching and caching.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# React SWR Integration

[SWR](https://swr.vercel.app/) is a React Hooks library for data fetching.

## Installation

```sh
npm install @orpc/experimental-react-swr@latest
```

## Setup

```ts
import { createSWRUtils } from '@orpc/experimental-react-swr'

export const orpc = createSWRUtils(client)
```

Avoiding key conflicts:

```ts
const userORPC = createSWRUtils(userClient, { path: ['user'] })
const postORPC = createSWRUtils(postClient, { path: ['post'] })
```

## Data Fetching

```ts
import useSWR from 'swr'

const { data, error, isLoading } = useSWR(
  orpc.planet.find.key({ input: { id: 123 } }),
  orpc.planet.find.fetcher({ context: { cache: true } }),
)
```

## Infinite Queries

```ts
import useSWRInfinite from 'swr/infinite'

const { data, error, isLoading, size, setSize } = useSWRInfinite(
  (index, previousPageData) => {
    if (previousPageData && !previousPageData.nextCursor) return null
    return orpc.planet.list.key({ input: { cursor: previousPageData?.nextCursor } })
  },
  orpc.planet.list.fetcher({ context: { cache: true } }),
)
```

## Subscriptions

```ts
import useSWRSubscription from 'swr/subscription'

const { data, error } = useSWRSubscription(
  orpc.streamed.key({ input: { id: 3 } }),
  orpc.streamed.subscriber({ context: { cache: true }, maxChunks: 10 }),
)
```

Use `.liveSubscriber` for the latest event without chunking:

```ts
const { data, error } = useSWRSubscription(
  orpc.streamed.key({ input: { id: 3 } }),
  orpc.streamed.liveSubscriber({ context: { cache: true } }),
)
```

## Mutations

```ts
import useSWRMutation from 'swr/mutation'

const { trigger, isMutating } = useSWRMutation(
  orpc.planet.list.key(),
  orpc.planet.create.mutator({ context: { cache: true } }),
)

trigger({ name: 'New Planet' }) // auto revalidate on success
```

## Manual Revalidation

```ts
import { mutate } from 'swr'

mutate(orpc.matcher()) // invalidate all orpc data
mutate(orpc.planet.matcher()) // invalidate all planet data
mutate(orpc.planet.find.matcher({ input: { id: 123 }, strategy: 'exact' }))
```

## Operation Context

```ts
import {
  SWR_OPERATION_CONTEXT_SYMBOL,
  SWROperationContext,
} from '@orpc/experimental-react-swr'

interface ClientContext extends SWROperationContext {}

const GET_OPERATION_TYPE = new Set(['fetcher', 'subscriber', 'liveSubscriber'])

const link = new RPCLink<ClientContext>({
  url: 'http://localhost:3000/rpc',
  method: ({ context }, path) => {
    const operationType = context[SWR_OPERATION_CONTEXT_SYMBOL]?.type
    if (operationType && GET_OPERATION_TYPE.has(operationType)) return 'GET'
    return 'POST'
  },
})
```
