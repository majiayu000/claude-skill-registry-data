---
name: oRPC Response Validation Plugin
description: Validate server responses against the contract schema.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Response Validation Plugin

Validates server responses against your contract schema, ensuring data matches the expected types.

> Best suited for [Contract-First Development](/docs/contract-first/define-contract). [Minified Contract](/docs/contract-first/router-to-contract#minify-export-the-contract-router-for-the-client) is **not supported**.

## Setup

```ts
import { RPCLink } from '@orpc/client/fetch'
import { ResponseValidationPlugin } from '@orpc/contract/plugins'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  plugins: [
    new ResponseValidationPlugin(contract),
  ],
})

const client: ContractRouterClient<typeof contract> = createORPCClient(link)
```

## Limitations

Schemas that transform data into different types than the expected schema types are not supported.

```ts
// Unsupported:
const unsupported = z.number().transform(value => value.toString())
```

The server transforms `number` to `string`, but the client receives a `string` that no longer matches the schema, causing validation to fail.

## Advanced Usage

Also useful for [Expanding Type Support for OpenAPI Link](/docs/openapi/advanced/expanding-type-support-for-openapi-link).
