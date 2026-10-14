---
name: oRPC Web Workers Adapter
description: Type-safe oRPC communication between the main thread and Web Workers via the Message Port adapter.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Web Workers Adapter

[Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Worker) run JavaScript in background threads, preventing UI blocking. Modern runtimes ([Bun](https://bun.com/docs/api/workers), [Deno](https://docs.deno.com/examples/web_workers/)) also support them.

With oRPC, you get type-safe communication channels between threads. See the [Message Port Adapter](/docs/adapters/message-port) for more context.

## Web Worker

```ts
import { RPCHandler } from '@orpc/server/message-port'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(error => console.error(error))],
})

handler.upgrade(self, {
  context: {},
})
```

## Main Thread

```ts
import { RPCLink } from '@orpc/client/message-port'

export const link = new RPCLink({
  port: new Worker('some-worker.ts'),
})
```

### Vite Web Workers

Vite has [first-class Web Workers support](https://vite.dev/guide/features.html#web-workers):

```ts
import SomeWorker from './some-worker.ts?worker'
import { RPCLink } from '@orpc/client/message-port'

export const link = new RPCLink({
  port: new SomeWorker(),
})
```

For full client examples, see [Client-Side Clients](/docs/client/client-side).
