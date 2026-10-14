---
name: oRPC RPC JSON Serializer
description: Extend or override the standard RPC JSON serializer.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# RPC JSON Serializer

Handles JSON payloads for the [RPC Protocol](/docs/advanced/rpc-protocol) and supports [native data types](/docs/rpc-handler#supported-data-types).

## Extending Native Data Types

1. **Define Your Custom Serializer:**

```ts
import type { StandardRPCCustomJsonSerializer } from '@orpc/client/standard'

export class User {
  constructor(
    public readonly id: string,
    public readonly name: string,
    public readonly email: string,
    public readonly age: number,
  ) {}

  toJSON() {
    return { id: this.id, name: this.name, email: this.email, age: this.age }
  }
}

export const userSerializer: StandardRPCCustomJsonSerializer = {
  type: 21,
  condition: data => data instanceof User,
  serialize: data => data.toJSON(),
  deserialize: data => new User(data.id, data.name, data.email, data.age),
}
```

> Ensure `type` is unique and greater than `20` to avoid conflicts with built-in types.

2. **Use Your Custom Serializer:**

```ts
import { RPCHandler } from '@orpc/server/fetch'
import { RPCLink } from '@orpc/client/fetch'

const handler = new RPCHandler(router, {
  customJsonSerializers: [userSerializer],
})

const link = new RPCLink({
  url: 'https://example.com/rpc',
  customJsonSerializers: [userSerializer],
})
```

## Overriding Built-in Types

Match `type` with [built-in types](/docs/advanced/rpc-protocol#supported-types).

Example: oRPC ignores `undefined` in objects. To override:

```ts
export const undefinedSerializer: StandardRPCCustomJsonSerializer = {
  type: 3, // Match built-in undefined type
  condition: data => data === undefined,
  serialize: data => null,
  deserialize: data => undefined,
}
```
