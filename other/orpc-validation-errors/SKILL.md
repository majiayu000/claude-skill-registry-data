---
name: oRPC Validation Errors
description: Customize built-in input/output validation errors using client interceptors or middleware, with type-safe error mapping.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Validation Errors

oRPC provides built-in validation errors that work well by default. You can customize them when needed.

## Customizing with Client Interceptors (Preferred)

[Client Interceptors](/docs/rpc-handler#lifecycle) run before error validation, ensuring custom errors are properly validated.

```ts
import { onError, ORPCError, ValidationError } from '@orpc/server'
import * as z from 'zod'

const handler = new RPCHandler(router, {
  clientInterceptors: [
    onError((error) => {
      if (
        error instanceof ORPCError
        && error.code === 'BAD_REQUEST'
        && error.cause instanceof ValidationError
      ) {
        const zodError = new z.ZodError(error.cause.issues as z.core.$ZodIssue[])

        throw new ORPCError('INPUT_VALIDATION_FAILED', {
          status: 422,
          message: z.prettifyError(zodError),
          data: z.flattenError(zodError),
          cause: error.cause,
        })
      }

      if (
        error instanceof ORPCError
        && error.code === 'INTERNAL_SERVER_ERROR'
        && error.cause instanceof ValidationError
      ) {
        throw new ORPCError('OUTPUT_VALIDATION_FAILED', {
          cause: error.cause,
        })
      }
    }),
  ],
})
```

## Customizing with Middleware

```ts
const base = os.use(onError((error) => {
  if (
    error instanceof ORPCError
    && error.code === 'BAD_REQUEST'
    && error.cause instanceof ValidationError
  ) {
    const zodError = new z.ZodError(error.cause.issues as z.core.$ZodIssue[])

    throw new ORPCError('INPUT_VALIDATION_FAILED', {
      status: 422,
      message: z.prettifyError(zodError),
      data: z.flattenError(zodError),
      cause: error.cause,
    })
  }
}))
```

> Middleware applied before `.input`/`.output` catches validation errors by default — this behavior is configurable.

## Type-Safe Validation Errors

When you throw an `ORPCError` whose `code`, `status`, and `data` match the `.errors` map, oRPC treats it as if you had thrown `errors.[code]` in the type-safe approach.

```ts
const base = os.errors({
  INPUT_VALIDATION_FAILED: {
    status: 422,
    data: z.object({
      formErrors: z.array(z.string()),
      fieldErrors: z.record(z.string(), z.array(z.string()).optional()),
    }),
  },
})

const example = base
  .input(z.object({ id: z.uuid() }))
  .handler(() => { /** ... */ })

const handler = new RPCHandler({ example }, {
  clientInterceptors: [
    onError((error) => {
      if (
        error instanceof ORPCError
        && error.code === 'BAD_REQUEST'
        && error.cause instanceof ValidationError
      ) {
        const zodError = new z.ZodError(error.cause.issues as z.core.$ZodIssue[])

        throw new ORPCError('INPUT_VALIDATION_FAILED', {
          status: 422,
          message: z.prettifyError(zodError),
          data: z.flattenError(zodError),
          cause: error.cause,
        })
      }
    }),
  ],
})
```
