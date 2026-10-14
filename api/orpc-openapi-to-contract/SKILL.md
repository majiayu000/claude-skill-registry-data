---
name: oRPC OpenAPI to Contract
description: Generate an oRPC contract from an existing OpenAPI specification with Hey API.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# OpenAPI to Contract

If you have an [OpenAPI Specification](https://swagger.io/specification/), use [Hey API](https://heyapi.dev/)'s `orpc` plugin to generate an oRPC contract.

> The Hey API `orpc` plugin is currently beta.

## Example

```sh
npm install -D @hey-api/openapi-ts
```

```ts
// openapi-ts.config.ts
import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  input: 'https://get.heyapi.dev/hey-api/backend',
  output: 'src/client',
  plugins: [
    {
      name: 'orpc',
      validator: { input: 'zod' },
    },
  ],
})
```

Then run:

```sh
npx @hey-api/openapi-ts
```

## What To Do Next

* Implement the contract on your own server with [Implement Contract](/docs/contract-first/implement-contract).
* Create a type-safe client with [OpenAPILink](/docs/openapi/client/openapi-link).
* Use as reference alongside [Define Contract](/docs/contract-first/define-contract).
