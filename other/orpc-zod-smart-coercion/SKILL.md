---
name: oRPC Zod Smart Coercion
description: Refined alternative to z.coerce — automatically coerces inputs to the expected type without modifying the schema.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Zod Smart Coercion

A plugin alternative to `z.coerce` that automatically converts inputs to the expected type without modifying the input schema.

> In Zod v4, this plugin only supports **discriminated unions**. Regular unions are not coerced.

## Installation

```sh
npm install @orpc/zod@latest
```

## Setup

```ts
import { OpenAPIHandler } from '@orpc/openapi/fetch'
import { ZodSmartCoercionPlugin } from '@orpc/zod' // Zod v3
import { experimental_ZodSmartCoercionPlugin as ZodSmartCoercionPlugin } from '@orpc/zod/zod4' // Zod v4

const handler = new OpenAPIHandler(router, {
  plugins: [new ZodSmartCoercionPlugin()],
})
```

> Do not use with [RPCHandler](/docs/rpc-handler) — it may negatively impact performance.

## Safe and Predictable Conversion

Coercion only happens when:

1. The schema expects a specific type and the input can be converted.
2. The input does not already match the schema.

For example:
- If input is `'true'` but the schema does not expect a boolean — no conversion.
- If the schema accepts both boolean and string — `'true'` is **not** coerced to a boolean.

## Conversion Rules

| Source                              | Target | Examples                                                       |
| ----------------------------------- | ------ | -------------------------------------------------------------- |
| `'true'`, `'on'`, `'t'`             | `true` | Boolean                                                        |
| `'false'`, `'off'`, `'f'`           | `false` | Boolean                                                       |
| `'42'`                              | `42`   | Number                                                         |
| `'12345678901234567890'`            | `BigInt` | BigInt                                                       |
| `'2024-11-27T00:00:00.000Z'`        | `Date` | ISO date/datetime                                              |
| `'/^abc$/i'`                        | `RegExp` | Regular expression                                           |
| `'https://example.com'`             | `URL`  | URL object                                                     |
| `['a', 'b', 'a']`                   | `Set`  | Deduped Set                                                    |
| `[['k1', 'v1'], ['k2', 'v2']]`      | `Map`  | Map from key/value pairs                                       |
