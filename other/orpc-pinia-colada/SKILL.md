---
name: oRPC Pinia Colada Integration
description: Seamlessly integrate oRPC with Pinia Colada for Vue.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Pinia Colada Integration

[Pinia Colada](https://pinia-colada.esm.dev/) is the data fetching layer for Pinia and Vue.

> Pinia Colada is unstable. This integration may introduce breaking changes.

## Installation

```sh
npm install @orpc/vue-colada@latest @pinia/colada@latest
```

## Setup

```ts
import { createORPCVueColadaUtils } from '@orpc/vue-colada'

export const orpc = createORPCVueColadaUtils(client)

orpc.planet.find.queryOptions({ input: { id: 123 } })
```

## Avoiding Key Conflicts

```ts
const userORPC = createORPCVueColadaUtils(userClient, { path: ['user'] })
const postORPC = createORPCVueColadaUtils(postClient, { path: ['post'] })
```

## Query Options

```ts
const query = useQuery(orpc.planet.find.queryOptions({
  input: { id: 123 },
  context: { cache: true },
}))
```

## Mutation Options

```ts
const mutation = useMutation(orpc.planet.create.mutationOptions({
  context: { cache: true },
}))

mutation.mutate({ name: 'Earth' })
```

## Query/Mutation Key

```ts
const queryCache = useQueryCache()

queryCache.invalidateQueries({ key: orpc.planet.key() })
queryCache.invalidateQueries({ key: orpc.planet.find.key({ input: { id: 123 } }) })
```

## Calling Procedure Clients

```ts
const result = orpc.planet.find.call({ id: 123 })
```

## Error Handling

```ts
import { isDefinedError } from '@orpc/client'

const mutation = useMutation(orpc.planet.create.mutationOptions({
  onError: (error) => {
    if (isDefinedError(error)) {
      // Handle the error
    }
  },
}))

mutation.mutate({ name: 'Earth' })

if (mutation.error.value && isDefinedError(mutation.error.value)) {
  // Handle the error
}
```
