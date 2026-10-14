---
name: oRPC WebSocket Adapter
description: Use oRPC over WebSocket for low-latency, bidirectional RPC across browser, Node, Bun, Deno, Cloudflare, and CrossWS.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Websocket

oRPC provides built-in WebSocket support for low-latency, bidirectional RPC.

## Server Adapters

| Adapter     | Target                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| `websocket` | [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) (Browser, Deno, Cloudflare Worker, etc.) |
| `crossws`   | [Crossws](https://github.com/h3js/crossws) library (Node, Bun, Deno, SSE, etc.)                                          |
| `ws`        | [ws](https://github.com/websockets/ws) library (Node.js)                                                                 |
| `bun-ws`    | [Bun Websocket Server](https://bun.sh/docs/api/websockets)                                                               |

### WebSocket (Deno / Browser / Cloudflare)

```ts
import { RPCHandler } from '@orpc/server/websocket'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(error => console.error(error))],
})

Deno.serve((req) => {
  if (req.headers.get('upgrade') !== 'websocket') {
    return new Response(null, { status: 501 })
  }

  const { socket, response } = Deno.upgradeWebSocket(req)
  handler.upgrade(socket, { context: {} })
  return response
})
```

### CrossWS

```ts
import { experimental_RPCHandler as RPCHandler } from '@orpc/server/crossws'
import crossws from 'crossws/adapters/node'

const handler = new RPCHandler(router)

const ws = crossws({
  hooks: {
    message: (peer, message) => handler.message(peer, message, { context: {} }),
    close: (peer) => handler.close(peer),
  },
})
```

### ws Library (Node.js)

```ts
import { WebSocketServer } from 'ws'
import { RPCHandler } from '@orpc/server/ws'

const handler = new RPCHandler(router)
const wss = new WebSocketServer({ port: 8080 })

wss.on('connection', (ws) => {
  handler.upgrade(ws, { context: {} })
})
```

### Bun WebSocket

```ts
import { RPCHandler } from '@orpc/server/bun-ws'

const handler = new RPCHandler(router)

Bun.serve({
  fetch(req, server) {
    if (server.upgrade(req)) return
    return new Response('Upgrade failed', { status: 500 })
  },
  websocket: {
    message(ws, message) {
      handler.message(ws, message, { context: {} })
    },
    close(ws) {
      handler.close(ws)
    },
  },
})
```

### Cloudflare Durable Object (Hibernation)

```ts
export class ChatRoom extends DurableObject {
  async fetch() {
    const { 0: client, 1: server } = new WebSocketPair()
    this.ctx.acceptWebSocket(server)
    return new Response(null, { status: 101, webSocket: client })
  }

  async webSocketMessage(ws, message) {
    await handler.message(ws, message, { context: {} })
  }

  async webSocketClose(ws) {
    handler.close(ws)
  }
}
```

> Pair with the [Hibernation Plugin](/docs/plugins/hibernation) to fully leverage Cloudflare WebSocket Hibernation.

## Client

```ts
import { RPCLink } from '@orpc/client/websocket'

const websocket = new WebSocket('ws://localhost:3000')
const link = new RPCLink({ websocket })
```

> Use [partysocket](https://www.npmjs.com/package/partysocket) for automatic reconnect logic.
