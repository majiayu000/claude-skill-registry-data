---
name: vercel-ai-sdk
description: "Use when building AI-powered web apps with Next.js, React, or Node.js — streaming chat, tool calling, structured output, multi-modal. Triggers on: 'vercel ai', 'ai sdk', 'streaming chat', 'useChat', 'generateText', 'streamText', 'ai chatbot nextjs', 'LLM in React', 'ai sdk tool use', 'provider agnostic LLM'."
---

# Vercel AI SDK Skill

Provider-agnostic TypeScript toolkit — streaming, tools, structured output, agents cho Next.js/React.
Source: [vercel/ai](https://github.com/vercel/ai) (MIT)

## Install

```bash
npm install ai
# Provider cụ thể
npm install @ai-sdk/anthropic @ai-sdk/openai @ai-sdk/google
```

## Core APIs

### generateText — one-shot

```typescript
import { generateText } from 'ai'
import { anthropic } from '@ai-sdk/anthropic'

const { text } = await generateText({
  model: anthropic('claude-sonnet-4-6'),
  prompt: 'Giải thích async/await trong 3 câu',
})
console.log(text)
```

### streamText — streaming response

```typescript
import { streamText } from 'ai'

const result = streamText({
  model: anthropic('claude-sonnet-4-6'),
  prompt: 'Viết một bài thơ về Hà Nội',
})

for await (const chunk of result.textStream) {
  process.stdout.write(chunk)
}
```

### generateObject — structured output (Zod)

```typescript
import { generateObject } from 'ai'
import { z } from 'zod'

const { object } = await generateObject({
  model: anthropic('claude-sonnet-4-6'),
  schema: z.object({
    title: z.string(),
    tags: z.array(z.string()),
    priority: z.enum(['low', 'medium', 'high']),
  }),
  prompt: 'Tạo một task: fix bug login timeout',
})
// object.title, object.tags, object.priority — type-safe
```

### Tool calling

```typescript
import { generateText, tool } from 'ai'
import { z } from 'zod'

const result = await generateText({
  model: anthropic('claude-sonnet-4-6'),
  tools: {
    getWeather: tool({
      description: 'Lấy thời tiết tại thành phố',
      parameters: z.object({ city: z.string() }),
      execute: async ({ city }) => {
        return { temp: 32, condition: 'sunny', city }
      },
    }),
  },
  maxSteps: 5,   // cho phép multi-turn tool calls
  prompt: 'Thời tiết Hà Nội hôm nay thế nào?',
})
console.log(result.text)
```

## React / Next.js integration

### Chat UI với useChat

```typescript
// app/api/chat/route.ts
import { anthropic } from '@ai-sdk/anthropic'
import { streamText } from 'ai'

export async function POST(req: Request) {
  const { messages } = await req.json()
  const result = streamText({
    model: anthropic('claude-sonnet-4-6'),
    messages,
  })
  return result.toDataStreamResponse()
}
```

```tsx
// app/page.tsx
'use client'
import { useChat } from 'ai/react'

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat()
  return (
    <div>
      {messages.map(m => (
        <div key={m.id}><b>{m.role}:</b> {m.content}</div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} placeholder="Nhập tin nhắn..." />
        <button type="submit">Gửi</button>
      </form>
    </div>
  )
}
```

### useObject — streaming structured data

```tsx
import { experimental_useObject as useObject } from 'ai/react'
import { taskSchema } from './schema'

export default function TaskGen() {
  const { object, submit, isLoading } = useObject({
    api: '/api/generate-task',
    schema: taskSchema,
  })
  return (
    <div>
      <button onClick={() => submit('Fix login bug')}>Generate</button>
      {isLoading && <p>Đang tạo...</p>}
      {object?.title && <h2>{object.title}</h2>}
    </div>
  )
}
```

## Multi-modal (image input)

```typescript
const { text } = await generateText({
  model: anthropic('claude-sonnet-4-6'),
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Mô tả ảnh này' },
      { type: 'image', image: new URL('https://example.com/image.png') },
    ],
  }],
})
```

## Provider switching (zero code change)

```typescript
// Đổi provider chỉ cần đổi 1 dòng
import { openai } from '@ai-sdk/openai'
import { google } from '@ai-sdk/google'

const model = process.env.PROVIDER === 'openai'
  ? openai('gpt-4o')
  : google('gemini-2.0-flash')
```

## Middleware (logging, caching, rate limit)

```typescript
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai'

const model = wrapLanguageModel({
  model: anthropic('claude-sonnet-4-6'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
})
```
