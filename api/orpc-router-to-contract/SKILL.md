---
name: oRPC Router to Contract
description: Convert a router into a contract, export it safely, and prevent internal exposure.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Router to Contract

A normal router works as a contract router as long as it doesn't include a [lazy router](/docs/router#lazy-router).

## Unlazy the Router

```ts
import { unlazyRouter } from '@orpc/server'

const resolvedRouter = await unlazyRouter(router)
```

## Minify & Export the Contract Router for the Client

1. **Minify and Export to JSON:**

```ts
import fs from 'node:fs'
import { minifyContractRouter } from '@orpc/contract'

const minifiedRouter = minifyContractRouter(router)

fs.writeFileSync('./contract.json', JSON.stringify(minifiedRouter))
```

> `minifyContractRouter` preserves only metadata and routing info. All other data is stripped.

2. **Import the Contract JSON on the Client:**

```ts
import contract from './contract.json'

const link = new OpenAPILink(contract as typeof router, {
  url: 'http://localhost:3000/api',
})
```

> Cast `contract` to `typeof router` for type safety, since standard schema types cannot be serialized.
