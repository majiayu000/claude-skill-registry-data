---
name: oRPC Worker Threads Adapter
description: Type-safe oRPC communication between Node.js worker threads via the Message Port adapter.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Worker Threads Adapter

Use [Node.js Worker Threads](https://nodejs.org/api/worker_threads.html) with oRPC for type-safe inter-thread communication via the [Message Port Adapter](/docs/adapters/message-port).

## Worker Thread

Listen for a `MessagePort` sent from the main thread and upgrade it:

```ts
import { parentPort } from 'node:worker_threads'
import { RPCHandler } from '@orpc/server/message-port'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(error => console.error(error))],
})

parentPort.on('message', (message) => {
  if (message instanceof MessagePort) {
    handler.upgrade(message, {
      context: {},
    })

    message.start()
  }
})
```

## Main Thread

Create a `MessageChannel`, send one port to the worker, use the other to initialize the client link:

```ts
import { MessageChannel, Worker } from 'node:worker_threads'
import { RPCLink } from '@orpc/client/message-port'

const { port1: clientPort, port2: serverPort } = new MessageChannel()

const worker = new Worker('some-worker.js')
worker.postMessage(serverPort, [serverPort])

const link = new RPCLink({
  port: clientPort,
})

clientPort.start()
```

For full client examples, see [Client-Side Clients](/docs/client/client-side).
