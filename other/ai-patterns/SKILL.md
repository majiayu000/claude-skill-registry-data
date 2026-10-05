---
name: TanStack AI Patterns (Alpha)
description: >-
  TanStack AI patterns for unified AI SDK integration. Activates when
  implementing AI chat, streaming responses, or AI-powered features.
  NOTE: Alpha library - API may change.
version: 1.0.0
---

# TanStack AI Patterns (Alpha)

> **Alpha Library**: TanStack AI is in alpha. APIs may change between versions.

TanStack AI provides a unified SDK for integrating AI capabilities into React applications.

## Core Concepts

- **Providers**: Backend AI providers (OpenAI, Anthropic, etc.)
- **Streams**: Real-time streaming responses
- **Chat**: Conversational interfaces
- **Completion**: Text completion
- **Hooks**: React hooks for AI interactions

## Basic Setup

```typescript
// lib/ai.ts
import { createAI } from '@tanstack/ai'

export const ai = createAI({
  provider: 'openai',
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  // Or use server-side proxy
  baseUrl: '/api/ai',
})
```

## Chat Interface

```typescript
import { useChat } from '@tanstack/ai-react'
import { ai } from '@/lib/ai'

function ChatInterface() {
  const {
    messages,
    input,
    setInput,
    sendMessage,
    isLoading,
    error,
  } = useChat({
    ai,
    model: 'gpt-4',
    systemPrompt: 'You are a helpful assistant.',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) {
      sendMessage(input)
      setInput('')
    }
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
          >
            {message.content}
          </div>
        ))}
        {isLoading && <div className="loading">Thinking...</div>}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>

      {error && <div className="error">{error.message}</div>}
    </div>
  )
}
```

## Streaming Responses

```typescript
import { useCompletion } from '@tanstack/ai-react'
import { ai } from '@/lib/ai'

function StreamingCompletion() {
  const {
    completion,
    complete,
    isLoading,
    stop,
  } = useCompletion({
    ai,
    model: 'gpt-4',
  })

  const handleGenerate = () => {
    complete('Write a short story about a robot learning to paint.')
  }

  return (
    <div>
      <button onClick={handleGenerate} disabled={isLoading}>
        Generate Story
      </button>
      {isLoading && (
        <button onClick={stop}>Stop</button>
      )}
      <div className="completion">
        {completion}
        {isLoading && <span className="cursor">|</span>}
      </div>
    </div>
  )
}
```

## Server-Side Proxy Pattern

```typescript
// For security, proxy AI calls through your server

// api/ai/chat.ts (server route)
import { OpenAI } from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(request: Request) {
  const { messages, model } = await request.json()

  const stream = await openai.chat.completions.create({
    model,
    messages,
    stream: true,
  })

  return new Response(stream.toReadableStream(), {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  })
}

// Client setup
export const ai = createAI({
  provider: 'openai',
  baseUrl: '/api/ai', // Use server proxy
})
```

## Chat with Context

```typescript
import { useChat } from '@tanstack/ai-react'

function ContextualChat({ documentContent }: { documentContent: string }) {
  const chat = useChat({
    ai,
    model: 'gpt-4',
    systemPrompt: `You are analyzing the following document. Answer questions about it.

Document:
${documentContent}`,
  })

  return <ChatUI {...chat} />
}
```

## Multi-Turn Conversation

```typescript
import { useChat } from '@tanstack/ai-react'
import { useState } from 'react'

function ConversationWithHistory() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversation, setActiveConversation] = useState<string | null>(null)

  const chat = useChat({
    ai,
    model: 'gpt-4',
    initialMessages: activeConversation
      ? conversations.find(c => c.id === activeConversation)?.messages
      : [],
    onFinish: (message) => {
      // Save conversation
      if (activeConversation) {
        setConversations(prev =>
          prev.map(c =>
            c.id === activeConversation
              ? { ...c, messages: [...c.messages, message] }
              : c
          )
        )
      }
    },
  })

  const startNewConversation = () => {
    const id = crypto.randomUUID()
    setConversations(prev => [...prev, { id, messages: [] }])
    setActiveConversation(id)
  }

  return (
    <div className="flex">
      <aside>
        <button onClick={startNewConversation}>New Chat</button>
        {conversations.map(conv => (
          <button
            key={conv.id}
            onClick={() => setActiveConversation(conv.id)}
            className={activeConversation === conv.id ? 'active' : ''}
          >
            Conversation {conv.id.slice(0, 8)}
          </button>
        ))}
      </aside>
      <main>
        <ChatUI {...chat} />
      </main>
    </div>
  )
}
```

## Function Calling

```typescript
import { useChat } from '@tanstack/ai-react'

const functions = [
  {
    name: 'get_weather',
    description: 'Get the current weather for a location',
    parameters: {
      type: 'object',
      properties: {
        location: { type: 'string', description: 'City name' },
      },
      required: ['location'],
    },
  },
]

function ChatWithFunctions() {
  const chat = useChat({
    ai,
    model: 'gpt-4',
    functions,
    onFunctionCall: async (name, args) => {
      if (name === 'get_weather') {
        const weather = await fetchWeather(args.location)
        return JSON.stringify(weather)
      }
      return null
    },
  })

  return <ChatUI {...chat} />
}
```

## Integration with Query

```typescript
import { useQuery } from '@tanstack/react-query'
import { useChat } from '@tanstack/ai-react'

function AIAssistedSearch({ query }: { query: string }) {
  // Fetch data with Query
  const { data: results } = useQuery({
    queryKey: ['search', query],
    queryFn: () => searchApi.search(query),
  })

  // Use AI to summarize results
  const { completion, complete } = useCompletion({
    ai,
    model: 'gpt-4',
  })

  useEffect(() => {
    if (results?.length) {
      complete(`Summarize these search results:\n${JSON.stringify(results)}`)
    }
  }, [results])

  return (
    <div>
      <h2>AI Summary</h2>
      <p>{completion}</p>
      <h2>Results</h2>
      <ResultsList results={results} />
    </div>
  )
}
```

## Conventions

1. **Server proxy** - Never expose API keys to client
2. **Streaming** - Use streaming for better UX
3. **Error handling** - Always handle AI errors gracefully
4. **Rate limiting** - Implement client-side throttling
5. **Token management** - Track and limit token usage
6. **Cancellation** - Allow users to stop generation

## Anti-Patterns

```typescript
// ❌ WRONG: API key in client
const ai = createAI({
  provider: 'openai',
  apiKey: 'sk-...', // Never do this!
})

// ✅ CORRECT: Use server proxy
const ai = createAI({
  provider: 'openai',
  baseUrl: '/api/ai',
})

// ❌ WRONG: No loading state
function Chat() {
  const { messages, sendMessage } = useChat({ ai })
  return <div>{messages.map(...)}</div>
}

// ✅ CORRECT: Show loading state
function Chat() {
  const { messages, sendMessage, isLoading } = useChat({ ai })
  return (
    <div>
      {messages.map(...)}
      {isLoading && <Typing />}
    </div>
  )
}

// ❌ WRONG: No error handling
const { completion } = useCompletion({ ai })

// ✅ CORRECT: Handle errors
const { completion, error } = useCompletion({ ai })
if (error) return <ErrorMessage error={error} />
```
