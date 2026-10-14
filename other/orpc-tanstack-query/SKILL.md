---
name: oRPC TanStack Query Integration
description: Seamlessly integrate oRPC with TanStack Query (React, Vue, Solid, Svelte, Angular).
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Tanstack Query Integration

[TanStack Query](https://tanstack.com/query/latest) is a robust solution for asynchronous state management.

## Installation

```sh
npm install @orpc/tanstack-query@latest
```

## Setup

```ts
import { createTanstackQueryUtils } from '@orpc/tanstack-query'

export const orpc = createTanstackQueryUtils(client)
```

Avoiding key conflicts:

```ts
const userORPC = createTanstackQueryUtils(userClient, { path: ['user'] })
const postORPC = createTanstackQueryUtils(postClient, { path: ['post'] })
```

## Query Options

```ts
const query = useQuery(orpc.planet.find.queryOptions({
  input: { id: 123 },
  context: { cache: true },
}))
```

## Streamed Query Options

For Event Iterator — data is an array of events appended as they arrive:

```ts
const query = useQuery(orpc.streamed.experimental_streamedOptions({
  input: { id: 123 },
  context: { cache: true },
  queryFnOptions: { refetchMode: 'reset', maxChunks: 3 },
  retry: true,
}))
```

## Live Query Options

For Event Iterator — data is always the latest event:

```ts
const query = useQuery(orpc.live.experimental_liveOptions({
  input: { id: 123 },
  context: { cache: true },
  retry: true,
}))
```

## Infinite Query Options

```ts
const query = useInfiniteQuery(orpc.planet.list.infiniteOptions({
  input: (pageParam: number | undefined) => ({ limit: 10, offset: pageParam }),
  context: { cache: true },
  initialPageParam: undefined,
  getNextPageParam: lastPage => lastPage.nextPageParam,
}))
```

## Mutation Options

```ts
const mutation = useMutation(orpc.planet.create.mutationOptions({
  context: { cache: true },
}))

mutation.mutate({ name: 'Earth' })
```

## Query/Mutation Keys

* `.key`: **Partial matching** for revalidation/invalidation
* `.queryKey`: **Full matching** for Query Options
* `.streamedKey`, `.infiniteKey`, `.mutationKey`: full matching variants

```ts
const queryClient = useQueryClient()

queryClient.invalidateQueries({ queryKey: orpc.planet.key() })
queryClient.invalidateQueries({ queryKey: orpc.planet.key({ type: 'query' }) })
queryClient.invalidateQueries({ queryKey: orpc.planet.find.key({ input: { id: 123 } }) })

queryClient.setQueryData(orpc.planet.find.queryKey({ input: { id: 123 } }), (old) => {
  return { ...old, id: 123, name: 'Earth' }
})
```

## Calling Clients

```ts
const planet = await orpc.planet.find.call({ id: 123 })
```

## Reactive Options (Vue/Solid)

```ts
// Options as function
const query = useQuery(
  () => orpc.planet.find.queryOptions({ input: { id: id() } })
)

// Computed options
const query = useQuery(computed(
  () => orpc.planet.find.queryOptions({ input: { id: id.value } })
))
```

## Default Options

```ts
const orpc = createTanstackQueryUtils(client, {
  experimental_defaults: {
    planet: {
      find: {
        queryOptions: {
          staleTime: 60 * 1000,
          retry: 3,
        },
      },
      create: {
        mutationOptions: {
          onSuccess: (output, input, _, ctx) => {
            ctx.client.invalidateQueries({ queryKey: orpc.planet.key() })
          },
        },
      },
    },
  },
})
```

## Error Handling

```ts
import { isDefinedError } from '@orpc/client'

const mutation = useMutation(orpc.planet.create.mutationOptions({
  onError: (error) => {
    if (isDefinedError(error)) {
      // Handle type-safe error
    }
  }
}))
```

## `skipToken` for Disabling Queries

```ts
const query = useQuery(
  orpc.planet.list.queryOptions({
    input: search ? { search } : skipToken,
  })
)
```

## Hydration

To support SSR, extend the serializer:

```ts
import { StandardRPCJsonSerializer } from '@orpc/client/standard'

const serializer = new StandardRPCJsonSerializer({
  customJsonSerializers: [],
})

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryKeyHashFn(queryKey) {
        const [json, meta] = serializer.serialize(queryKey)
        return JSON.stringify({ json, meta })
      },
      staleTime: 60 * 1000,
    },
    dehydrate: {
      serializeData(data) {
        const [json, meta] = serializer.serialize(data)
        return { json, meta }
      }
    },
    hydrate: {
      deserializeData(data) {
        return serializer.deserialize(data.json, data.meta)
      }
    },
  }
})
```
