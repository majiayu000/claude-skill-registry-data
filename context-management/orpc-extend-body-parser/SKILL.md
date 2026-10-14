---
name: oRPC Extend Body Parser
description: Extend the body parser for larger payloads or additional data types.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Extend Body Parser

In some cases, you may need to extend the body parser to handle larger payloads or additional data types.

```ts
import { RPCHandler } from '@orpc/server/fetch'
import { getFilenameFromContentDisposition } from '@orpc/standard-server'

const OVERRIDE_BODY_CONTEXT = Symbol('OVERRIDE_BODY_CONTEXT')

interface OverrideBodyContext {
  fetchRequest: Request
}

const handler = new RPCHandler(router, {
  adapterInterceptors: [
    (options) => {
      return options.next({
        ...options,
        context: {
          ...options.context,
          [OVERRIDE_BODY_CONTEXT as any]: {
            fetchRequest: options.request,
          },
        },
      })
    },
  ],
  rootInterceptors: [
    (options) => {
      const { fetchRequest } = (options.context as any)[OVERRIDE_BODY_CONTEXT] as OverrideBodyContext

      return options.next({
        ...options,
        request: {
          ...options.request,
          async body() {
            const contentDisposition = fetchRequest.headers.get('content-disposition')
            const contentType = fetchRequest.headers.get('content-type')

            if (contentDisposition === null && contentType?.startsWith('multipart/form-data')) {
              // Custom multipart parsing (e.g., streaming with @mjackson/form-data-parser)
              return fetchRequest.formData()
            }

            if (
              contentDisposition !== null || (
                !contentType?.startsWith('application/json')
                && !contentType?.startsWith('application/x-www-form-urlencoded')
              )
            ) {
              // Streaming file to disk to reduce memory
              const fileName = getFilenameFromContentDisposition(contentDisposition ?? '') ?? 'blob'
              const blob = await fetchRequest.blob()
              return new File([blob], fileName, { type: blob.type })
            }

            // fallback to default
            return options.request.body()
          },
        },
      })
    },
  ],
})
```

> `adapterInterceptors` differ per adapter. This example is for Fetch.
