---
name: oRPC DynamicLink
description: Dynamically switch between multiple oRPC's links.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# DynamicLink

`DynamicLink` lets you dynamically choose between different oRPC links based on your client context.

## Example

```ts
import { createORPCClient, DynamicLink } from '@orpc/client'

interface ClientContext {
  cache?: boolean
}

const cacheLink = new RPCLink({
  url: 'https://cache.example.com/rpc',
})

const noCacheLink = new RPCLink({
  url: 'https://example.com/rpc',
})

const link = new DynamicLink<ClientContext>((options, path, input) => {
  if (options.context?.cache) {
    return cacheLink
  }

  return noCacheLink
})

const client: RouterClient<typeof router, ClientContext> = createORPCClient(link)
```

> Any oRPC link is supported, not limited to `RPCLink`.
