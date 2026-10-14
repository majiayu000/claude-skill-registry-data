---
name: oRPC Hey API Integration
description: Generate oRPC contracts from OpenAPI with Hey API or adapt a Hey API client.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Hey API Integration

[Hey API](https://heyapi.dev/) integrates two ways:

* Generate an oRPC contract from existing OpenAPI specification.
* Convert an existing Hey API client to an oRPC client.

> Integration is still unstable.

## Convert OpenAPI to an oRPC Contract

If you have an OpenAPI spec, use Hey API to generate an oRPC contract. See [OpenAPI to Contract](/docs/openapi/openapi-to-contract).

Use the generated contract to:

* Implement on your own server with [Implement Contract](/docs/contract-first/implement-contract).
* Create a type-safe client with [OpenAPILink](/docs/openapi/client/openapi-link).
* Use as a reference alongside [Define Contract](/docs/contract-first/define-contract).

## Convert a Hey API Client Directly to an oRPC Client

```ts
import { experimental_toORPCClient } from '@orpc/hey-api'
import * as sdk from 'src/client/sdk.gen'

export const client = experimental_toORPCClient(sdk)

const { body } = await client.listPlanets()
```

This client behaves like any standard oRPC server-side/client-side client.

### Error Handling

oRPC passes `throwOnError` to Hey API. If the Hey API client throws an error, oRPC forwards it as is.
