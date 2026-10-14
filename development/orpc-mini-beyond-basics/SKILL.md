---
name: Mini oRPC Beyond the Basics
description: Advanced features you can implement in Mini oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Beyond the Basics of Mini oRPC

This section explores advanced features and techniques you can implement to enhance Mini oRPC's capabilities.

## Getting Started

The complete Mini oRPC implementation is available in the [Mini oRPC Repository](https://github.com/middleapi/mini-orpc), with a [playground](https://github.com/middleapi/mini-orpc/tree/main/playground).

## Feature Suggestions

Below are recommended features you can implement in Mini oRPC. Pick any order and you can import code from existing oRPC packages.

* Middleware Typed Input Support — [reference](https://github.com/middleapi/orpc/blob/main/packages/server/src/middleware.ts)
* Builder Variants — [reference](https://github.com/middleapi/orpc/blob/main/packages/server/src/builder-variants.ts)
  * Prevent redefinition of `.input` and `.output` methods
* Type-Safe Error Support — [reference](https://github.com/middleapi/orpc/blob/main/packages/server/src/procedure-client.ts#L113-L120)
* RPC Protocol Implementation — [reference](https://github.com/middleapi/orpc/blob/main/packages/client/src/adapters/standard/rpc-serializer.ts)
  * Support native types like `Date`, `Map`, `Set`, etc.
  * Support `File`/`Blob` types
  * Support Event Iterator types
* Multi-runtime support
  * Standard Server Concept
  * Fetch Adapter
  * Node HTTP Adapter
  * Peer Adapter (WebSocket, MessagePort, etc.)
* Contract First Support
  * Contract Builder
  * Contract Implementer
* OpenAPI Support
  * OpenAPI Handler
  * OpenAPI Generator
  * OpenAPI Link
* Tanstack Query Integration

Once implemented, submit a pull request to the repository for review.
