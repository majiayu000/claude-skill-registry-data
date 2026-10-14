---
name: oRPC Publisher
description: Listen and publish events with resuming support in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Publisher

The Publisher helper enables listening to and publishing events to subscribers. Combined with [Event Iterator](/docs/client/event-iterator), it allows you to build streaming responses with minimal effort.

## Installation

```sh
npm install @orpc/experimental-publisher@latest
```

## Basic Usage

```ts
import { MemoryPublisher } from '@orpc/experimental-publisher/memory'

const publisher = new MemoryPublisher<{
  'something-updated': { id: string }
}>()

const live = os
  .handler(async function* ({ input, signal }) {
    const iterator = publisher.subscribe('something-updated', { signal })
    for await (const payload of iterator) {
      yield payload
    }
  })

const publish = os
  .input(z.object({ id: z.string() }))
  .handler(async ({ input }) => {
    await publisher.publish('something-updated', { id: input.id })
  })
```

Supports both static and dynamic event names:

```ts
const publisher = new MemoryPublisher<Record<string, { message: string }>>()
```

## Resume Feature

Uses `lastEventId` to resume after disconnection.

### Server

```ts
const live = os
  .handler(async function* ({ input, signal, lastEventId }) {
    const iterator = publisher.subscribe('something-updated', { signal, lastEventId })
    for await (const payload of iterator) {
      yield payload
    }
  })
```

> Publisher automatically manages event IDs when resume is enabled.

### Client

Use the [Client Retry Plugin](/docs/plugins/client-retry) or manually:

```ts
import { getEventMeta } from '@orpc/client'

let lastEventId: string | undefined

while (true) {
  try {
    const iterator = await client.live('input', { lastEventId })
    for await (const payload of iterator) {
      lastEventId = getEventMeta(payload)?.id
      console.log(payload)
    }
  } catch {
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
}
```

## Available Adapters

| Name                     | Resume | Description                          |
| ------------------------ | ------ | ------------------------------------ |
| `MemoryPublisher`        | ✅     | Simple in-memory publisher           |
| `IORedisPublisher`       | ✅     | [ioredis](https://github.com/redis/ioredis) adapter |
| `UpstashRedisPublisher`  | ✅     | [Upstash Redis](https://github.com/upstash/redis-js) adapter |
| `PublisherDurableObject` | ✅     | [Cloudflare Durable Objects](https://developers.cloudflare.com/durable-objects/) adapter |

### Memory

```ts
const publisher = new MemoryPublisher<{
  'something-updated': { id: string }
}>({
  resumeRetentionSeconds: 60 * 2,
})
```

### IORedis

```ts
import { Redis } from 'ioredis'
import { IORedisPublisher } from '@orpc/experimental-publisher/ioredis'

const publisher = new IORedisPublisher({
  commander: new Redis(),
  listener: new Redis(),
  resumeRetentionSeconds: 60 * 2,
  prefix: 'orpc:publisher:',
})
```

### Upstash Redis

```ts
import { Redis } from '@upstash/redis'
import { UpstashRedisPublisher } from '@orpc/experimental-publisher/upstash-redis'

const redis = Redis.fromEnv()

const publisher = new UpstashRedisPublisher(redis, {
  resumeRetentionSeconds: 60 * 2,
  prefix: 'orpc:publisher:',
})
```

### Cloudflare Durable Object

```ts
import { DurablePublisher, PublisherDurableObject } from '@orpc/experimental-publisher-durable-object'

export class PublisherDO extends PublisherDurableObject {
  constructor(ctx, env) {
    super(ctx, env, {
      resume: {
        retentionSeconds: 60 * 2,
        cleanupIntervalSeconds: 12 * 60 * 60,
      },
    })
  }
}

export default {
  async fetch(request, env) {
    const publisher = new DurablePublisher(env.PUBLISHER_DO, {
      prefix: 'publisher1',
    })
  },
}
```

> Enable `enable_request_signal` compatibility flag in workers to support abort signals.
