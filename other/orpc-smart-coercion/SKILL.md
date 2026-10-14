---
name: oRPC Smart Coercion Plugin
description: Automatically converts input values to match schema types without manual coercion logic.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Smart Coercion Plugin

Automatically converts input values to match schema types.

> Impacts performance. For high-performance applications, manually define coercion in your schema validation.

## Installation

```sh
npm install @orpc/json-schema@latest
```

## Setup

```ts
import { OpenAPIHandler } from '@orpc/openapi/fetch'
import { SmartCoercionPlugin } from '@orpc/json-schema'

const handler = new OpenAPIHandler(router, {
  plugins: [
    new SmartCoercionPlugin({
      schemaConverters: [
        new ZodToJsonSchemaConverter(),
      ],
    })
  ]
})
```

## How It Works

1. **Schema-guided** — Only converts when the schema specifies type
2. **Safe only** — Only safe conversions like `'123'` to `123`
3. **Keep original** — Unsafe conversions keep the original value
4. **Smart unions** — Picks the best for union types
5. **Deep conversion** — Works inside nested structures

## Native Type Support

For non-JSON-native types, oRPC uses `x-native-type` metadata:

* `x-native-type: 'bigint'` for BigInt
* `x-native-type: 'date'` for Date
* `x-native-type: 'regexp'` for RegExp
* `x-native-type: 'url'` for URL
* `x-native-type: 'set'` for Set
* `x-native-type: 'map'` for Map

## Conversion Rules

### String → Boolean

* `'true'`, `'on'` → `true`
* `'false'`, `'off'` → `false`

### String → Number

* `'123'` → `123`
* `'3.14'` → `3.14`

### String/Number → BigInt

* `'12345678901234567890'` → `12345678901234567890n`

### String → Date

* ISO format: `'2023-10-01'`, `'2020-01-01T06:15:00Z'`, etc.

### String → RegExp

* `'/^\\d+$/i'` → `new RegExp('^\\d+$', 'i')`

### String → URL

* `'https://example.com'` → `new URL('https://example.com')`

### Array → Set

* `['apple', 'banana']` → `new Set(['apple', 'banana'])`

### Array → Object

* `['apple', 'banana']` → `{ 0: 'apple', 1: 'banana' }`

### Array → Map

* `[['key1', 'value1'], ['key2', 'value2']]` → `new Map(...)`
