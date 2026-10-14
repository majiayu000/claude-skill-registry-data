---
name: oRPC OpenAPI Reference Plugin
description: Plugin that serves API reference documentation (Scalar/Swagger) and the OpenAPI specification.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# OpenAPI Reference Plugin (Swagger/Scalar)

Provides API reference documentation powered by [Scalar](https://github.com/scalar/scalar) or [Swagger UI](https://swagger.io/tools/swagger-ui/), along with the OpenAPI specification.

> Relies on the [OpenAPI Generator](/docs/openapi/openapi-specification).

## Setup

```ts
import { ZodToJsonSchemaConverter } from '@orpc/zod/zod4'
import { OpenAPIReferencePlugin } from '@orpc/openapi/plugins'

const handler = new OpenAPIHandler(router, {
  plugins: [
    new OpenAPIReferencePlugin({
      docsProvider: 'swagger', // default: 'scalar'
      schemaConverters: [
        new ZodToJsonSchemaConverter(),
      ],
      specGenerateOptions: {
        info: {
          title: 'ORPC Playground',
          version: '1.0.0',
        },
        servers: [
          { url: 'https://api.example.com/v1' },
        ],
      },
    }),
  ]
})
```

> Default paths: client at `/`, OpenAPI spec at `/spec.json`. Customize via `docsPath` and `specPath` options.
