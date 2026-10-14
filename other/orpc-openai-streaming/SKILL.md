---
name: oRPC OpenAI Streaming Example
description: Combine oRPC with the OpenAI Streaming API to build a chatbot.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# OpenAI Streaming Example

Integrate oRPC with the OpenAI Streaming API to build a chatbot.

## Basic Example

```ts
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import { os, RouterClient } from '@orpc/server'
import * as z from 'zod'
import OpenAI from 'openai'

const openai = new OpenAI()

const complete = os
  .input(z.object({ content: z.string() }))
  .handler(async function* ({ input }) {
    const stream = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: input.content }],
      stream: true,
    })

    yield* stream
  })

const router = { complete }

// --------------- CLIENT ---------------

const link = new RPCLink({
  url: 'https://example.com/rpc',
})

const client: RouterClient<typeof router> = createORPCClient(link)

const stream = await client.complete({ content: 'Hello, world!' })

for await (const chunk of stream) {
  console.log(chunk.choices[0]?.delta?.content || '')
}
```
