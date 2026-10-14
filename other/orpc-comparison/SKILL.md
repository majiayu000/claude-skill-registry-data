---
name: oRPC Comparison
description: How oRPC differs from tRPC, ts-rest, and Hono.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Comparison

How oRPC differs from popular TypeScript RPC and REST solutions.

* ✅ First-class, built-in support
* 🟡 Lacks features, or requires third-party integrations
* 🛑 Not supported or not documented

| Feature                                  | oRPC | tRPC | ts-rest | Hono |
| ---------------------------------------- | ---- | ---- | ------- | ---- |
| End-to-end Typesafe Input/Output         | ✅   | ✅   | ✅      | ✅   |
| End-to-end Typesafe Errors               | ✅   | 🟡   | ✅      | ✅   |
| End-to-end Typesafe File/Blob            | ✅   | 🟡   | 🛑      | 🛑   |
| End-to-end Typesafe Streaming            | ✅   | ✅   | 🛑      | 🛑   |
| Tanstack Query (React)                   | ✅   | ✅   | 🟡      | 🛑   |
| Tanstack Query (Vue)                     | ✅   | 🛑   | 🟡      | 🛑   |
| Tanstack Query (Solid)                   | ✅   | 🛑   | 🟡      | 🛑   |
| Tanstack Query (Svelte)                  | ✅   | 🛑   | 🛑      | 🛑   |
| Tanstack Query (Angular)                 | ✅   | 🛑   | 🛑      | 🛑   |
| Vue Pinia Colada                         | ✅   | 🛑   | 🛑      | 🛑   |
| Contract-First                           | ✅   | 🛑   | ✅      | ✅   |
| Without Contract-First                   | ✅   | ✅   | 🛑      | ✅   |
| OpenAPI                                  | ✅   | 🟡   | 🟡      | ✅   |
| OpenAPI multiple schema                  | ✅   | 🛑   | 🛑      | ✅   |
| OpenAPI Bracket Notation                 | ✅   | 🛑   | 🛑      | 🛑   |
| Server Actions                           | ✅   | ✅   | 🛑      | 🛑   |
| Lazy Router                              | ✅   | ✅   | 🛑      | 🛑   |
| Native Types (Date, URL, Set, Maps)      | ✅   | 🟡   | 🛑      | 🛑   |
| Streaming response (SSE)                 | ✅   | ✅   | 🛑      | ✅   |
| Standard Schema (Zod, Valibot, ArkType)  | ✅   | ✅   | 🛑      | 🟡   |
| Built-in Plugins (CORS, CSRF, Retry)     | ✅   | 🛑   | 🛑      | ✅   |
| Batch Requests                           | ✅   | ✅   | 🛑      | 🛑   |
| WebSockets                               | ✅   | ✅   | 🛑      | 🛑   |
| Cloudflare Websocket Hibernation         | ✅   | 🛑   | 🛑      | 🛑   |
| Nest.js integration                      | ✅   | 🟡   | ✅      | 🛑   |
| Message Port (Electron, Browser, Workers) | ✅  | 🟡   | 🛑      | 🛑   |
