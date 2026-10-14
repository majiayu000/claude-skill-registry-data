---
name: oRPC Hibernation Plugin
description: Plugin to fully leverage Hibernation APIs in oRPC server (Cloudflare Websocket Hibernation, etc).
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Hibernation Plugin

Helps you fully leverage Hibernation APIs, especially useful for [Cloudflare Websocket Hibernation](https://developers.cloudflare.com/durable-objects/examples/websocket-hibernation-server/).

## Setup

```ts
import { HibernationPlugin } from '@orpc/server/hibernation'

const handler = new RPCHandler(router, {
  plugins: [new HibernationPlugin()],
})
```

## Event Iterator

`HibernationEventIterator` and `encodeHibernationRPCEvent` help return event iterators that utilize Hibernation APIs.

1. Return `HibernationEventIterator` from your handler:

```ts
import { HibernationEventIterator } from '@orpc/server/hibernation'

export const onMessage = os.handler(async ({ context }) => {
  return new HibernationEventIterator<{ message: string }>((id) => {
    context.ws.serializeAttachment({ id })
  })
})
```

2. Send events with `encodeHibernationRPCEvent`:

```ts
import { encodeHibernationRPCEvent } from '@orpc/server/hibernation'

export const sendMessage = os.handler(async ({ input, context }) => {
  const websockets = context.getWebSockets()

  for (const ws of websockets) {
    const { id } = ws.deserializeAttachment()

    // yield an event
    ws.send(encodeHibernationRPCEvent(id, { message: input.message }, {
      customJsonSerializers: []
    }))

    // return and stop event iterator
    ws.send(encodeHibernationRPCEvent(id, { message: input.message }, { event: 'done' }))

    // throw and stop event iterator
    ws.send(encodeHibernationRPCEvent(id, new ORPCError('INTERNAL_SERVER_ERROR'), { event: 'error' }))
  }
})
```

## Cloudflare Durable Object Chat Room Example

```ts
import { RPCHandler } from '@orpc/server/websocket'
import { encodeHibernationRPCEvent, HibernationEventIterator, HibernationPlugin } from '@orpc/server/hibernation'
import { DurableObject } from 'cloudflare:workers'

const base = os.$context<{
  handler: RPCHandler<any>
  ws: WebSocket
  getWebsockets: () => WebSocket[]
}>()

export const router = {
  send: base.input(z.object({ message: z.string() })).handler(async ({ input, context }) => {
    const websockets = context.getWebsockets()
    for (const ws of websockets) {
      const data = ws.deserializeAttachment()
      if (typeof data !== 'object' || data === null) continue
      ws.send(encodeHibernationRPCEvent(data.id, input.message))
    }
  }),
  onMessage: base.handler(async ({ context }) => {
    return new HibernationEventIterator<string>((id) => {
      context.ws.serializeAttachment({ id })
    })
  }),
}

const handler = new RPCHandler(router, {
  plugins: [new HibernationPlugin()],
})

export class ChatRoom extends DurableObject {
  async fetch(): Promise<Response> {
    const { '0': client, '1': server } = new WebSocketPair()
    this.ctx.acceptWebSocket(server)
    return new Response(null, { status: 101, webSocket: client })
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer) {
    await handler.message(ws, message, {
      context: { handler, ws, getWebsockets: () => this.ctx.getWebSockets() },
    })
  }

  async webSocketClose(ws: WebSocket) {
    handler.close(ws)
  }
}
```
