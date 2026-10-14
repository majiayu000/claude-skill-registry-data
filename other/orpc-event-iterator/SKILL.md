---
name: oRPC Event Iterator (SSE)
description: Streaming responses, real-time updates, and server-sent events using oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Event Iterator (SSE)

oRPC provides built-in support for streaming responses, real-time updates, and server-sent events (SSE) without any extra configuration.

## Overview

```ts
const example = os
  .handler(async function* ({ input, lastEventId }) {
    while (true) {
      yield { message: 'Hello, world!' }
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  })
```

## Validate Event Iterator

```ts
import { eventIterator } from '@orpc/server'

const example = os
  .output(eventIterator(z.object({ message: z.string() })))
  .handler(async function* ({ input, lastEventId }) {
    while (true) {
      yield { message: 'Hello, world!' }
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  })
```

## Last Event ID & Event Metadata

Using `withEventMeta`, attach metadata (event ID, retry interval) to events:

```ts
import { withEventMeta } from '@orpc/server'

const example = os
  .handler(async function* ({ input, lastEventId }) {
    if (lastEventId) {
      // Resume streaming from lastEventId
    } else {
      while (true) {
        yield withEventMeta({ message: 'Hello, world!' }, { id: 'some-id', retry: 10_000 })
        await new Promise(resolve => setTimeout(resolve, 1000))
      }
    }
  })
```

## Stop Event Iterator

Use `return` to signal end of stream:

```ts
const example = os
  .handler(async function* ({ input, lastEventId }) {
    while (true) {
      if (done) return

      yield { message: 'Hello, world!' }
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  })
```

## Cleanup Side-Effects

```ts
const example = os
  .handler(async function* ({ input, lastEventId }) {
    try {
      while (true) {
        yield { message: 'Hello, world!' }
        await new Promise(resolve => setTimeout(resolve, 1000))
      }
    } finally {
      console.log('Cleanup logic here')
    }
  })
```

## Publisher Helper

Build real-time features like chat with resume support:

```ts
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

## Event Publisher

Lightweight synchronous publisher (no resume support):

```ts
import { EventPublisher } from '@orpc/server'

const publisher = new EventPublisher<{
  'something-updated': { id: string }
}>()

const livePlanet = os
  .handler(async function* ({ input, signal }) {
    for await (const payload of publisher.subscribe('something-updated', { signal })) {
      // handle payload here
    }
  })

const update = os
  .input(z.object({ id: z.string() }))
  .handler(({ input }) => {
    publisher.publish('something-updated', { id: input.id })
  })
```
