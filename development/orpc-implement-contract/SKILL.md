---
name: oRPC Implement Contract
description: Implement a contract for contract-first development in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Implement Contract

After defining your contract, implement it in your server code. oRPC enforces your contract at runtime.

## Installation

```sh
npm install @orpc/server@latest
```

## The Implementer

The `implement` function converts your contract into an implementer instance.

```ts
import { implement } from '@orpc/server'

const os = implement(contract) // fully replaces the os from @orpc/server
```

## Implementing Procedures

```ts
export const listPlanet = os.planet.list
  .handler(({ input }) => {
    return []
  })
```

## Building the Router

```ts
const router = os.router({
  planet: {
    list: listPlanet,
    find: findPlanet,
    create: createPlanet,
  },
})
```

## Full Implementation Example

```ts
const os = implement(contract)

export const listPlanet = os.planet.list
  .handler(({ input }) => [])

export const findPlanet = os.planet.find
  .handler(({ input }) => ({ id: 123, name: 'Planet X' }))

export const createPlanet = os.planet.create
  .handler(({ input }) => ({ id: 123, name: 'Planet X' }))

export const router = os.router({
  planet: {
    list: listPlanet,
    find: findPlanet,
    create: createPlanet,
  },
})
```
