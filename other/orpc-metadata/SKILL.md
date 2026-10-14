---
name: oRPC Metadata
description: Enhance your procedures with metadata.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Metadata

oRPC procedures support metadata — simple key-value pairs that customize behavior.

## Basic Example

```ts
import { os } from '@orpc/server'

interface ORPCMetadata {
  cache?: boolean
}

const base = os
  .$meta<ORPCMetadata>({}) // require initial metadata
  .use(async ({ procedure, next, path }, input, output) => {
    if (!procedure['~orpc'].meta.cache) {
      return await next()
    }

    const cacheKey = path.join('/') + JSON.stringify(input)

    if (db.has(cacheKey)) {
      return output(db.get(cacheKey))
    }

    const result = await next()

    db.set(cacheKey, result.output)

    return result
  })

const example = base
  .meta({ cache: true })
  .handler(() => {
    // Implement your procedure logic
  })
```

> `.meta` can be called multiple times; each call spread-merges new metadata with existing.
