---
name: oRPC tRPC Integration
description: Use oRPC features (OpenAPI specs, OpenAPIHandler) inside existing tRPC applications via @orpc/trpc.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# tRPC Integration

Integrate oRPC with tRPC to leverage oRPC features in your existing tRPC applications.

## Installation

```sh
npm install @orpc/trpc@latest
```

## OpenAPI Support

Convert a [tRPC router](https://trpc.io/docs/server/routers) to an [oRPC router](/docs/router) to access most oRPC features.

```ts
import { ORPCMeta, toORPCRouter } from '@orpc/trpc'

export const t = initTRPC.context<Context>().meta<ORPCMeta>().create()

const orpcRouter = toORPCRouter(trpcRouter)
```

> Set the `.meta` type to `ORPCMeta` when creating your tRPC builder for OpenAPI features to function.

```ts
const example = t.procedure
  .meta({ route: { path: '/hello', summary: 'Hello procedure' } })
  .input(z.object({ name: z.string() }))
  .query(({ input }) => `Hello, ${input.name}!`)
```

## Specification Generation

```ts
const openAPIGenerator = new OpenAPIGenerator({
  schemaConverters: [
    new ZodToJsonSchemaConverter(),
    new ValibotToJsonSchemaConverter(),
    new ArkTypeToJsonSchemaConverter(),
  ],
})

const spec = await openAPIGenerator.generate(orpcRouter, {
  info: { title: 'My App', version: '0.0.0' },
})
```

## Request Handling

```ts
const handler = new OpenAPIHandler(orpcRouter, {
  plugins: [new CORSPlugin()],
  interceptors: [onError(error => console.error(error))],
})

export async function fetch(request: Request) {
  const { matched, response } = await handler.handle(request, {
    prefix: '/api',
    context: {},
  })

  return response ?? new Response('Not Found', { status: 404 })
}
```

## Error Formatting

`toORPCRouter` does not support [tRPC Error Formatting](https://trpc.io/docs/server/error-formatting). Catch and format errors via interceptors:

```ts
const handler = new OpenAPIHandler(orpcRouter, {
  interceptors: [
    onError((error) => {
      if (
        error instanceof ORPCError
        && error.cause instanceof TRPCError
        && error.cause.cause instanceof ZodError
      ) {
        throw new ORPCError('INPUT_VALIDATION_FAILED', {
          status: 422,
          data: error.cause.cause.flatten(),
          cause: error.cause.cause,
        })
      }
    })
  ],
})
```
