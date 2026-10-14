---
name: oRPC Monorepo Setup
description: The most efficient way to set up a monorepo with oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Monorepo Setup

This guide shows how to efficiently set up a monorepo with oRPC while maintaining end-to-end type safety.

> See the [Multiservice Monorepo Playground](https://github.com/middleapi/orpc-multiservice-monorepo-playground) for a sample.

## TypeScript Project References

Some parts of the client may end up typed as `any` because the client doesn't have access to all types. Use [TypeScript Project References](https://www.typescriptlang.org/docs/handbook/project-references.html).

**Client tsconfig:**

```json
{
  "compilerOptions": {},
  "references": [
    { "path": "../server" }
  ]
}
```

**Server tsconfig:**

```json
{
  "compilerOptions": {
    "composite": true
  }
}
```

### Common `composite` constraint

If you encounter "The inferred type of X cannot be named without a reference to Y", install Y and add:

```ts
import type * as _A from '../../node_modules/detail_Y_path_here'
```

## Recommended Structure

* `/apps`: `references` dependencies
* `/packages`: Enable `composite`

Separate the server component into a dedicated package containing only necessary files.

> Avoid alias imports inside server components. Use linked workspace packages (e.g., [PNPM Workspace protocol](https://pnpm.io/workspaces#workspace-protocol-workspace)).

### Contract First

```
apps/
├─ api/    // Import `core-contract` and implement it
├─ web/    // Import `core-contract` and set up @orpc/client
packages/
├─ core-contract/  // Define contract with @orpc/contract
```

### Service First

```
apps/
├─ api/    // Import `core-service` and run it
├─ web/    // Import `core-service` and set up @orpc/client
packages/
├─ core-service/   // Define procedures with @orpc/server
```

### Hybrid

```
apps/
├─ api/    // Import `core-service` and set up @orpc/server
├─ web/    // Import `core-contract` and set up @orpc/client
packages/
├─ core-contract/  // Define contract
├─ core-service/   // Implement contract
```

## Related

* [Publish Client to NPM](/docs/advanced/publish-client-to-npm)
