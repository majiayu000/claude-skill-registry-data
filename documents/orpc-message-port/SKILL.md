---
name: oRPC Message Port
description: Using oRPC with Message Ports for internal communication between processes.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Message Port

oRPC offers built-in support for common Message Port implementations, enabling easy internal communication between processes.

| Environment                     | Documentation                                    |
| ------------------------------- | ------------------------------------------------ |
| Electron Message Port           | [Adapter Guide](/docs/adapters/electron)         |
| Browser (extension, window-to-window) | [Adapter Guide](/docs/adapters/browser)    |
| Node.js Worker Threads Port     | [Adapter Guide](/docs/adapters/worker-threads)   |

## Basic Usage

**Bridge:**

```ts
const channel = new MessageChannel()
const serverPort = channel.port1
const clientPort = channel.port2
```

**Server:**

```ts
import { RPCHandler } from '@orpc/server/message-port'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

handler.upgrade(serverPort, { context: {} })

serverPort.start()
```

**Client:**

```ts
import { RPCLink } from '@orpc/client/message-port'

const link = new RPCLink({ port: clientPort })

clientPort.start()
```

## Transfer

By default, oRPC serializes messages to string/binary. Use `transfer` to leverage [`MessagePort.postMessage`](https://developer.mozilla.org/en-US/docs/Web/API/MessagePort/postMessage) for transferring ownership or unserializable objects:

**Handler:**

```ts
const handler = new RPCHandler(router, {
  experimental_transfer: (message, port) => {
    const transfer = deepFindTransferableObjects(message)
    return transfer.length ? transfer : null
  }
})
```

**Link:**

```ts
const link = new RPCLink({
  port: clientPort,
  experimental_transfer: (message) => {
    const transfer = deepFindTransferableObjects(message)
    return transfer.length ? transfer : null
  }
})
```

> When `transfer` returns an array, messages use [structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm), which doesn't support all data types like Event Iterator metadata. Only enable when needed.

> `transfer` runs after [RPC JSON Serializer](/docs/advanced/rpc-json-serializer) so you can combine them.
