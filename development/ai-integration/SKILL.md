---
name: ai-integration
description: Specialized skill for integrating AI features using OpenAI API. Use when implementing chatbots, content generation, or AI-powered educational features.
---

# AI Integration Skill

This skill provides expertise in integrating AI features using OpenAI API in the Artiefy educational platform.

## When to Use This Skill

- Implementing AI chatbots or conversational interfaces
- Adding content generation features
- Creating AI-powered learning assistants
- Integrating OpenAI API calls
- Handling AI responses and error management

## Key Technologies

- **OpenAI API**: GPT models for text generation
- **Streaming Responses**: Real-time AI responses
- **Rate Limiting**: Upstash Redis for API rate limiting
- **Error Handling**: Robust error management for API calls

## Patterns and Conventions

### API Integration

- Use server-side API routes for OpenAI calls
- Implement proper error handling and fallbacks
- Use streaming for real-time responses

### Rate Limiting

- Implement with Upstash Redis
- Configure limits per user/role
- Handle rate limit errors gracefully

### Security

- Validate all inputs to AI prompts
- Sanitize AI responses before display
- Implement content moderation

## Examples

### OpenAI API Route

```ts
// src/app/api/chat/route.ts
import { OpenAI } from 'openai';
import { NextRequest, NextResponse } from 'next/server';
import { ratelimit } from '@/lib/ratelimit';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    const { messages, userId } = await request.json();

    // Rate limiting
    const { success } = await ratelimit.limit(userId);
    if (!success) {
      return NextResponse.json(
        { error: 'Rate limit exceeded' },
        { status: 429 }
      );
    }

    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages,
      stream: true,
    });

    return new Response(completion.toReadableStream(), {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
      },
    });
  } catch (error) {
    console.error('OpenAI API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Client-Side Chat Component

```tsx
// src/components/AIChat.tsx
'use client';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

export function AIChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      });

      if (!response.ok) throw new Error('API error');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiResponse = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') break;

            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices[0]?.delta?.content;
              if (content) {
                aiResponse += content;
                setMessages([
                  ...newMessages,
                  { role: 'assistant', content: aiResponse },
                ]);
              }
            } catch (e) {
              // Ignore parsing errors
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: 'Lo siento, hubo un error. Por favor intenta de nuevo.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs rounded-lg px-4 py-2 lg:max-w-md ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
      </div>

      <div className="border-t p-4">
        <div className="flex space-x-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu mensaje..."
            className="flex-1"
            onKeyPress={(e) =>
              e.key === 'Enter' && !e.shiftKey && sendMessage()
            }
          />
          <Button onClick={sendMessage} disabled={isLoading}>
            {isLoading ? 'Enviando...' : 'Enviar'}
          </Button>
        </div>
      </div>
    </div>
  );
}
```

### Rate Limiting Setup

```ts
// src/lib/ratelimit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { redis } from '@/lib/redis';

export const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
  analytics: true,
});
```

## Best Practices

- Always implement rate limiting
- Use streaming for better UX
- Handle API errors gracefully
- Validate and sanitize all inputs
- Monitor API usage and costs

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Upstash Redis Documentation](https://docs.upstash.com/)
- Project API routes: `src/app/api/`
- Environment config: `src/env.ts`
