---
name: oRPC Scalar (Swagger)
description: Create a beautiful API client for your oRPC with Scalar.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Scalar (Swagger)

Generate a stunning API client for your oRPC using [Scalar](https://github.com/scalar/scalar) and the [OpenAPI Specification](/docs/openapi/openapi-specification).

> For simpler setup, see [OpenAPI Reference Plugin](/docs/openapi/plugins/openapi-reference).

## Basic Example

```ts
import { createServer } from 'node:http'
import { OpenAPIGenerator } from '@orpc/openapi'
import { OpenAPIHandler } from '@orpc/openapi/node'
import { CORSPlugin } from '@orpc/server/plugins'
import { ZodSmartCoercionPlugin, ZodToJsonSchemaConverter } from '@orpc/zod'

const openAPIHandler = new OpenAPIHandler(router, {
  plugins: [new CORSPlugin(), new ZodSmartCoercionPlugin()],
})

const openAPIGenerator = new OpenAPIGenerator({
  schemaConverters: [new ZodToJsonSchemaConverter()],
})

const server = createServer(async (req, res) => {
  const { matched } = await openAPIHandler.handle(req, res, { prefix: '/api' })
  if (matched) return

  if (req.url === '/spec.json') {
    const spec = await openAPIGenerator.generate(router, {
      info: { title: 'My Playground', version: '1.0.0' },
      servers: [{ url: '/api' }],
      security: [{ bearerAuth: [] }],
      components: {
        securitySchemes: {
          bearerAuth: { type: 'http', scheme: 'bearer' },
        },
      },
    })

    res.writeHead(200, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify(spec))
    return
  }

  const html = `
    <!doctype html>
    <html>
      <head>
        <title>My Client</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <div id="app"></div>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
        <script>
          Scalar.createApiReference('#app', {
            url: '/spec.json',
            authentication: {
              securitySchemes: {
                bearerAuth: { token: 'default-token' },
              },
            },
          })
        </script>
      </body>
    </html>
  `

  res.writeHead(200, { 'Content-Type': 'text/html' })
  res.end(html)
})

server.listen(3000, () => console.log('Playground at http://localhost:3000'))
```
