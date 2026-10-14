---
name: oRPC Exceeds Maximum Length Problem
description: How to address the Exceeds the Maximum Length Problem in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Exceeds the Maximum Length Problem

```ts
// @error: The inferred type of this node exceeds the maximum length the compiler will serialize.
export const router = {
  // many procedures here
}
```

## Why It Happens

TypeScript enforces this to keep your IDE suggestions fast. It appears when:

1. Your project uses `"declaration": true` in `tsconfig.json`.
2. Your project is large or your types are very complex.
3. You export your router as a single, large object.

## How to Fix It

### 1. Disable `"declaration": true`

Simplest option, though may not be ideal.

### 2. Define the `.output` Type for Your Procedures

By specifying `.output` or your handler's return type, TypeScript can infer the output without parsing the handler. Dramatically improves performance.

> Use the [type](/docs/procedure#type-utility) utility for specifying output without validation.

### 3. Export the Router in Parts

```ts
// Server (declaration: true)
export const userRouter = { /** ... */ }
export const planetRouter = { /** ... */ }
export const publicRouter = { /** ... */ }
```

```ts
// Client (declaration: false)
interface Router {
  user: typeof userRouter
  planet: typeof planetRouter
  public: typeof publicRouter
}

export const client: RouterClient<Router> = createORPCClient(link)
```
