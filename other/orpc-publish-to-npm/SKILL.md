---
name: oRPC Publish Client to NPM
description: How to publish your oRPC client to NPM as an SDK.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Publish Client to NPM

Publishing your oRPC client to NPM allows users to easily consume your APIs as an SDK.

## Prerequisites

A project already set up with oRPC. [Contract First](/docs/contract-first/define-contract) is the preferred approach.

## Export & Scripts

```ts
// src/index.ts
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import type { ContractRouterClient } from '@orpc/contract'

export function createMyApi(apiKey: string): ContractRouterClient<typeof contract> {
  const link = new RPCLink({
    url: 'https://example.com/rpc',
    headers: { 'x-api-key': apiKey }
  })

  return createORPCClient(link)
}
```

```json
{
  "name": "<package-name>",
  "type": "module",
  "version": "0.0.0",
  "publishConfig": { "access": "public" },
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "default": "./dist/index.js"
    }
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsdown --dts src/index.ts",
    "release": "pnpm publish"
  },
  "dependencies": {
    "@orpc/client": "...",
    "@orpc/contract": "..."
  },
  "devDependencies": {
    "tsdown": "latest",
    "typescript": "latest"
  }
}
```

## Build & Publish

```bash
pnpm login
pnpm run build
pnpm run release
```

## Install & Use

```bash
pnpm add "<package-name>"
```

```ts
import { createMyApi } from '<package-name>'

const myApi = createMyApi('your-api-key')

const output = await myApi.someMethod('input')
```
