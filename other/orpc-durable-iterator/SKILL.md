---
name: oRPC Durable Iterator Integration
description: Extends Event Iterator with durable event streams, automatic reconnections, and event recovery.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Durable Iterator Integration

Durable Iterator extends [Event Iterator](/docs/event-iterator) by offloading streaming to a separate service that provides durable event streams, automatic reconnections, and event recovery.

> Currently supports only [Cloudflare Durable Objects](https://developers.cloudflare.com/durable-objects/).

## Installation

```sh
npm install @orpc/experimental-durable-iterator@latest
```

## Durable Object

### Define your Durable Object

```ts
import { DurableIteratorObject } from '@orpc/experimental-durable-iterator/durable-object'

export class ChatRoom extends DurableIteratorObject<{ message: string }> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env, {
      signingKey: 'secret-key',
      interceptors: [onError(e => console.error(e))],
      onSubscribed: (websocket, lastEventId) => {
        console.log(`WebSocket Ready id=${websocket['~orpc'].deserializeId()}`)
      }
    })
  }

  someMethod() {
    this.publishEvent({ message: 'Hello, world!' })
  }
}
```

### Upgrade Durable Iterator Request

```ts
import { upgradeDurableIteratorRequest } from '@orpc/experimental-durable-iterator/durable-object'

export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    if (url.pathname === '/chat-room') {
      return upgradeDurableIteratorRequest(request, {
        signingKey: 'secret-key',
        namespace: env.CHAT_ROOM,
      })
    }

    return new Response('Not Found', { status: 404 })
  },
}

export { ChatRoom }
```

### Publish Events

```ts
this.publishEvent({ message: 'Hello, world!' }, {
  tags: ['tag1', 'tag2'],
  targets: ws => ws['~orpc'].deserializeTokenPayload().att.role === 'admin',
  exclude: [senderWs],
})
```

### Resume Events After Connection Loss

Enable by configuring `resumeRetentionSeconds`:

```ts
super(ctx, env, {
  signingKey: 'secret-key',
  resumeRetentionSeconds: 60 * 2, // 2 minutes
})
```

## Server Side

```ts
import { DurableIterator } from '@orpc/experimental-durable-iterator'

export const router = {
  onMessage: base.handler(({ context }) => {
    return new DurableIterator<ChatRoom>('some-room', {
      tags: ['tag1', 'tag2'],
      signingKey: 'secret-key',
    })
  }),

  sendMessage: base
    .input(z.object({ message: z.string() }))
    .handler(async ({ context, input }) => {
      const id = context.env.CHAT_ROOM.idFromName('some-room')
      const stub = context.env.CHAT_ROOM.get(id)
      await stub.publishEvent(input)
    }),
}
```

Enable the handler plugin:

```ts
import { DurableIteratorHandlerPlugin } from '@orpc/experimental-durable-iterator'

const handler = new RPCHandler(router, {
  plugins: [
    new CORSPlugin({ exposeHeaders: ['x-orpc-durable-iterator'] }),
    new DurableIteratorHandlerPlugin(),
  ],
})
```

## Client Side

```ts
import { DurableIteratorLinkPlugin } from '@orpc/experimental-durable-iterator/client'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  plugins: [
    new DurableIteratorLinkPlugin({
      url: 'ws://localhost:3000/chat-room',
      interceptors: [onError(e => console.error(e))],
    }),
  ],
})
```

### Example

```ts
const iterator = await client.onMessage()

for await (const { message } of iterator) {
  console.log('Received message:', message)
}

await client.sendMessage({ message: 'Hello, world!' })
```

### Auto Refresh Token

```ts
new DurableIteratorLinkPlugin({
  url: 'ws://localhost:3000/chat-room',
  refreshTokenBeforeExpireInSeconds: 10 * 60, // 10 minutes
})
```

## Method RPC

Define methods that accept a `DurableIteratorWebsocket` instance:

```ts
import { DurableIteratorWebsocket } from '@orpc/experimental-durable-iterator/durable-object'

export class ChatRoom extends DurableIteratorObject<{ message: string }> {
  singleClient(ws: DurableIteratorWebsocket) {
    return base
      .input(z.object({ message: z.string() }))
      .handler(({ input, context }) => {
        this.publishEvent(input, { exclude: [ws] })
      })
      .callable()
  }

  routerClient(ws: DurableIteratorWebsocket) {
    return {
      ping: base.handler(() => 'pong').callable(),
      echo: base.input(z.object({ text: z.string() }))
        .handler(({ input }) => `Echo: ${input.text}`)
        .callable(),
    }
  }
}
```

Server side:

```ts
export const onMessage = base.handler(({ context }) => {
  return new DurableIterator<ChatRoom>('some-room', {
    signingKey: 'secret-key',
    att: { userId: 'user-123' },
  }).rpc('singleClient', 'routerClient')
})
```

Client side:

```ts
const iterator = await client.onMessage()

await iterator.singleClient({ message: 'Hello, world!' })

const response = await iterator.routerClient.ping()
const echo = await iterator.routerClient.echo({ text: 'Hello' })
```

## Contract First

```ts
import type { ContractRouterClient } from '@orpc/contract'
import { oc, type } from '@orpc/contract'
import type { ClientDurableIterator } from '@orpc/experimental-durable-iterator/client'
import type { DurableIteratorObject } from '@orpc/experimental-durable-iterator'

export const publishMessageContract = oc.input(z.object({ message: z.string() }))

export interface ChatRoom extends DurableIteratorObject<{ message: string }> {
  publishMessage(...args: any[]): ContractRouterClient<typeof publishMessageContract>
}

export const contract = {
  onMessage: oc.output(type<ClientDurableIterator<ChatRoom, 'publishMessage'>>()),
}
```
