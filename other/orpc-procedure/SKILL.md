---
name: oRPC Procedure
description: Understanding procedures in oRPC — standard functions with validation, middleware, and DI.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Procedure in oRPC

A procedure is like a standard function with built-in support for:

* Input/output validation
* Middleware
* Dependency injection
* Other extensibility features

## Overview

```ts
import { os } from '@orpc/server'

const example = os
  .use(aMiddleware)
  .input(z.object({ name: z.string() }))
  .use(aMiddlewareWithInput, input => input.name)
  .output(z.object({ id: z.number() }))
  .handler(async ({ input, context }) => {
    return { id: 1 }
  })
  .callable() // Make callable
  .actionable() // Server Action compatibility
```

> Only `.handler` is required.

## Input/Output Validation

Supports [Zod](https://github.com/colinhacks/zod), [Valibot](https://github.com/fabian-hiller/valibot), [Arktype](https://github.com/arktypeio/arktype), and any [Standard Schema](https://github.com/standard-schema/standard-schema) library.

> Explicitly specifying `.output` or handler return type dramatically improves type-checking speed.

### `type` Utility

```ts
import { os, type } from '@orpc/server'

const example = os
  .input(type<{ value: number }>())
  .output(type<{ value: number }, number>(({ value }) => value))
  .handler(async ({ input }) => input)
```

## Using Middleware

```ts
const aMiddleware = os.middleware(async ({ context, next }) => next())

const example = os
  .use(aMiddleware)
  .use(async ({ context, next }) => next())
  .handler(async ({ context }) => {})
```

## Initial Configuration

```ts
const base = os.$input(z.void())
const base = os.$input<Schema<void, unknown>>()
```

`.$input` lets you redefine the input schema after initial configuration.

## Reusability

Each modification creates a new instance:

```ts
const pub = os.use(logMiddleware)
const authed = pub.use(authMiddleware)

const pubExample = pub.handler(async ({ context }) => {})
const authedExample = pubExample.use(authMiddleware)
```
