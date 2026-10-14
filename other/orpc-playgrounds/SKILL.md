---
name: oRPC Playgrounds
description: Interactive development environments for exploring and testing oRPC functionality.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Playgrounds

Explore oRPC implementations through interactive playgrounds.

## Available Playgrounds

| Environment                      | GitHub Source                                                                                |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| Next.js                          | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/next)                         |
| TanStack Start                   | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/tanstack-start)               |
| Nuxt.js                          | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/nuxt)                         |
| Solid Start                      | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/solid-start)                  |
| Svelte Kit                       | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/svelte-kit)                   |
| Astro                            | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/astro)                        |
| Contract-First                   | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/contract-first)               |
| NestJS                           | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/nest)                         |
| Cloudflare Worker                | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/cloudflare-worker)            |
| Bun WebSocket + OpenTelemetry    | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/bun-websocket-otel)           |
| Electron                         | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/electron)                     |
| Browser Extension                | [View](https://github.com/middleapi/orpc/tree/main/playgrounds/browser-extension)            |
| Multiservice Monorepo            | [View](https://github.com/middleapi/orpc-multiservice-monorepo-playground)                   |

## Local Development

Clone any playground:

```bash
npx degit middleapi/orpc/playgrounds/next orpc-next-playground
npx degit middleapi/orpc/playgrounds/tanstack-start orpc-tanstack-start-playground
npx degit middleapi/orpc/playgrounds/nuxt orpc-nuxt-playground
npx degit middleapi/orpc/playgrounds/solid-start orpc-solid-start-playground
npx degit middleapi/orpc/playgrounds/svelte-kit orpc-svelte-kit-playground
npx degit middleapi/orpc/playgrounds/astro orpc-astro-playground
npx degit middleapi/orpc/playgrounds/contract-first orpc-contract-first-playground
npx degit middleapi/orpc/playgrounds/nest orpc-nest-playground
npx degit middleapi/orpc/playgrounds/cloudflare-worker orpc-cloudflare-worker-playground
npx degit middleapi/orpc/playgrounds/bun-websocket-otel orpc-bun-websocket-otel-playground
npx degit middleapi/orpc/playgrounds/electron orpc-electron-playground
npx degit middleapi/orpc/playgrounds/browser-extension orpc-browser-extension-playground
npx degit middleapi/orpc-multiservice-monorepo-playground orpc-multiservice-monorepo-playground
```

Then:

```bash
npm install
npm run dev
```
