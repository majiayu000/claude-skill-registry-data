---
name: oRPC Testing & Mocking
description: Test oRPC procedures using server-side clients, and mock implementations for frontend testing.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Testing & Mocking

Strategies for testing and mocking oRPC routers and procedures.

## Testing

Use [Server-Side Clients](/docs/client/server-side) to invoke procedures directly in tests, no additional setup required:

```ts
import { call } from '@orpc/server'

it('works', async () => {
  await expect(
    call(router.planet.list, { page: 1, size: 10 })
  ).resolves.toEqual([
    { id: '1', name: 'Earth' },
    { id: '2', name: 'Mars' },
  ])
})
```

> You can also use the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) to create production-like clients. See [Optimize SSR](/docs/best-practices/optimize-ssr#alternative-approach).

## Mocking

The [Implementer](/docs/contract-first/implement-contract#the-implementer) is designed for contract-first development, but it can also create alternative versions of routers/procedures for testing.

```ts
import { implement, unlazyRouter } from '@orpc/server'

const fakeListPlanet = implement(router.planet.list).handler(() => [])
```

Use `fakeListPlanet` to replace the actual `listPlanet` implementation during tests.

> `implement` is also useful for creating mock servers for frontend testing scenarios.

> `implement` doesn't yet support [lazy routers](/docs/router#lazy-router) — use the `unlazyRouter` utility to convert before implementing.
