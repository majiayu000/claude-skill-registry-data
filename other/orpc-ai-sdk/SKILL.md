---
name: oRPC AI SDK Integration
description: Seamlessly use AI SDK inside your oRPC projects without any extra overhead.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# AI SDK Integration

[AI SDK](https://ai-sdk.dev/) is a free open-source library for building AI-powered products. You can seamlessly integrate it with oRPC without any extra overhead.

> Requires AI SDK v5.0.0 or later.

## Server

Use `streamToEventIterator` to convert AI SDK streams to [oRPC Event Iterators](/docs/event-iterator).

```ts
import { os, streamToEventIterator, type } from '@orpc/server'
import { convertToModelMessages, streamText, UIMessage } from 'ai'
import { google } from '@ai-sdk/google'

export const chat = os
  .input(type<{ chatId: string, messages: UIMessage[] }>())
  .handler(async ({ input }) => {
    const result = streamText({
      model: google('gemini-1.5-flash'),
      system: 'You are a helpful assistant.',
      messages: await convertToModelMessages(input.messages),
    })

    return streamToEventIterator(result.toUIMessageStream())
  })
```

## Client

Convert the event iterator back to a stream using `eventIteratorToStream` or `eventIteratorToUnproxiedDataStream`.

```tsx
import { useChat } from '@ai-sdk/react'
import { eventIteratorToUnproxiedDataStream } from '@orpc/client'

export function Example() {
  const { messages, sendMessage, status } = useChat({
    transport: {
      async sendMessages(options) {
        return eventIteratorToUnproxiedDataStream(await client.chat({
          chatId: options.chatId,
          messages: options.messages,
        }, { signal: options.abortSignal }))
      },
      reconnectToStream() {
        throw new Error('Unsupported')
      },
    },
  })
  // render UI...
}
```

> Prefer `eventIteratorToUnproxiedDataStream` because AI SDK uses `structuredClone`, which doesn't support proxied data.

## `implementTool` helper

Implements a procedure contract as an [AI SDK tool](https://ai-sdk.dev/docs/foundations/tools).

```ts
import { oc } from '@orpc/contract'
import { AI_SDK_TOOL_META_SYMBOL, AiSdkToolMeta, implementTool } from '@orpc/ai-sdk'
import { z } from 'zod'

interface ORPCMeta extends AiSdkToolMeta {}
const base = oc.$meta<ORPCMeta>({})

const getWeatherContract = base
  .meta({ [AI_SDK_TOOL_META_SYMBOL]: { title: 'Get Weather' } })
  .route({ summary: 'Get the weather in a location' })
  .input(z.object({ location: z.string() }))
  .output(z.object({ location: z.string(), temperature: z.number() }))

const getWeatherTool = implementTool(getWeatherContract, {
  execute: async ({ location }) => ({
    location,
    temperature: 72 + Math.floor(Math.random() * 21) - 10,
  }),
})
```

## `createTool` helper

Converts a procedure into an AI SDK Tool.

```ts
import { os } from '@orpc/server'
import { AI_SDK_TOOL_META_SYMBOL, AiSdkToolMeta, createTool } from '@orpc/ai-sdk'
import { z } from 'zod'

const getWeatherProcedure = os
  .meta({ [AI_SDK_TOOL_META_SYMBOL]: { title: 'Get Weather' } })
  .route({ summary: 'Get the weather in a location' })
  .input(z.object({ location: z.string() }))
  .output(z.object({ location: z.string(), temperature: z.number() }))
  .handler(async ({ input }) => ({
    location: input.location,
    temperature: 72,
  }))

const getWeatherTool = createTool(getWeatherProcedure, { context: {} })
```
