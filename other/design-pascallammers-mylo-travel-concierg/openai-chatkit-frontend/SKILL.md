---
name: openai-chatkit-frontend
description: >
  Patterns for building AI chatbot frontends using OpenAI ChatKit with
  Next.js App Router, including custom backend integration via ChatKit Python SDK.
version: 1.0.0
---

# OpenAI ChatKit Frontend Skill

## When to use this Skill

Use this Skill whenever you are:

- Building a **chat UI** for an AI-powered application.
- Integrating **OpenAI ChatKit** with a Next.js App Router frontend.
- Connecting ChatKit to a **custom FastAPI backend**.
- Implementing **real-time streaming** chat responses.
- Adding a **conversational interface** to an existing application.

This Skill works for any Next.js application that needs a production-ready
chat interface with AI capabilities.

## Core goals

- Build **polished, production-ready chat UIs** with minimal code.
- Integrate seamlessly with **custom backends** using ChatKit Python SDK.
- Maintain **responsive, accessible** chat interfaces.
- Follow **consistent patterns** for ChatKit configuration.
- Enable **real-time streaming** for natural conversations.

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend Framework | Next.js (App Router) | `>=16.0.0` |
| ChatKit React | @openai/chatkit-react | `latest` |
| ChatKit Core | chatkit.js (CDN) | `latest` |
| Backend SDK | chatkit (Python) | `latest` |
| Styling | Tailwind CSS | `>=3.0` |

## Installation

### Frontend (Next.js)

```bash
npm install @openai/chatkit-react
```

### Backend (FastAPI)

```bash
pip install chatkit openai
```

Required environment variable:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ChatKit Component                     │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │  Message    │    │  Composer   │    │  Thread     │  │   │
│  │  │  List       │    │  Input      │    │  Sidebar    │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  useChatKit Hook                                        │   │
│  │  - getClientSecret() → fetches token from backend       │   │
│  │  - control object → manages ChatKit state               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /api/chatkit/session                              │   │
│  │  - Creates ChatKit session                              │   │
│  │  - Returns client_secret for frontend                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ChatKit Python SDK                                     │   │
│  │  - Handles AI responses                                 │   │
│  │  - Processes tool calls                                 │   │
│  │  - Manages conversation state                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Two Integration Approaches

### Approach 1: OpenAI-Hosted Backend (Simpler)

Use OpenAI's infrastructure to host your chat backend. Best for:
- Quick prototypes
- Simple chatbots without custom business logic
- Agents built in OpenAI's Agent Builder

```typescript
// Frontend only - OpenAI handles the backend
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function Chat() {
  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        // Fetch from your API that calls OpenAI
        const res = await fetch('/api/chatkit/session', { method: 'POST' });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
  });

  return <ChatKit control={control} className="h-[600px]" />;
}
```

### Approach 2: Custom Backend (Recommended for Phase III)

Use ChatKit Python SDK with your own FastAPI backend. Best for:
- Custom business logic and tool execution
- Integration with existing databases
- Full control over AI behavior

This is the recommended approach for the hackathon Phase III.

## Frontend Implementation

### 1. Add ChatKit Script

In your `app/layout.tsx`:

```tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="beforeInteractive"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 2. ChatKit Component

```tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useSession } from 'next-auth/react'; // or your auth solution

interface ChatWidgetProps {
  className?: string;
}

export function ChatWidget({ className = '' }: ChatWidgetProps) {
  const { data: session } = useSession();

  const { control } = useChatKit({
    api: {
      async getClientSecret(existingSecret) {
        // Handle token refresh if existing secret is provided
        if (existingSecret) {
          // Optionally refresh the session
        }

        // Fetch new client secret from your backend
        const response = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session?.accessToken}`,
          },
          body: JSON.stringify({
            user_id: session?.user?.id,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to create chat session');
        }

        const { client_secret } = await response.json();
        return client_secret;
      },
    },
  });

  return (
    <ChatKit
      control={control}
      className={`rounded-lg shadow-lg ${className}`}
    />
  );
}
```

### 3. Chat Page

```tsx
// app/chat/page.tsx
import { ChatWidget } from '@/components/ChatWidget';

export default function ChatPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Chat Assistant</h1>
      <ChatWidget className="h-[600px] w-full max-w-2xl" />
    </div>
  );
}
```

### 4. Toggle Button Integration

Add chat to existing pages with a toggle button:

```tsx
'use client';

import { useState } from 'react';
import { ChatWidget } from '@/components/ChatWidget';
import { MessageCircle, X } from 'lucide-react';

export function ChatToggle() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating chat button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 p-4 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-[380px] h-[500px] z-40">
          <ChatWidget className="h-full w-full" />
        </div>
      )}
    </>
  );
}
```

## Backend Implementation (FastAPI)

### Session Endpoint

```python
# app/routers/chatkit.py
from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from pydantic import BaseModel
import os

router = APIRouter(prefix="/api/chatkit", tags=["chatkit"])

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class SessionRequest(BaseModel):
    user_id: str | None = None


class SessionResponse(BaseModel):
    client_secret: str


@router.post("/session", response_model=SessionResponse)
async def create_session(
    request: SessionRequest,
    current_user = Depends(get_current_user),
):
    """Create a ChatKit session and return client secret."""
    try:
        session = client.chatkit.sessions.create(
            # Configure your ChatKit session
            # This depends on your ChatKit setup
        )
        return SessionResponse(client_secret=session.client_secret)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Custom Backend with ChatKit Python SDK

For full control, implement your own chat handling:

```python
# app/routers/chat_custom.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user = Depends(get_current_user),
):
    """Process chat message through AI agent."""
    # Your existing chat implementation
    # (See openai-agents-sdk-mcp-backend skill)
    pass
```

## Styling ChatKit

### Custom Theming

```css
/* styles/chatkit.css */

/* Container styling */
openai-chatkit {
  --chatkit-primary-color: #3b82f6;
  --chatkit-background: #ffffff;
  --chatkit-text-color: #1f2937;
  --chatkit-border-radius: 0.5rem;
}

/* Dark mode support */
.dark openai-chatkit {
  --chatkit-background: #1f2937;
  --chatkit-text-color: #f3f4f6;
}
```

### Responsive Design

```tsx
export function ChatWidget() {
  return (
    <ChatKit
      control={control}
      className="
        h-[400px] w-full
        sm:h-[500px]
        md:h-[600px]
        lg:h-[700px]
      "
    />
  );
}
```

## Error Handling

### Frontend Error States

```tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useState } from 'react';

export function ChatWidget() {
  const [error, setError] = useState<string | null>(null);

  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        try {
          const res = await fetch('/api/chatkit/session', { method: 'POST' });
          if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
          }
          const { client_secret } = await res.json();
          setError(null);
          return client_secret;
        } catch (e) {
          setError('Failed to connect to chat service');
          throw e;
        }
      },
    },
  });

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-700 rounded-lg">
        <p>{error}</p>
        <button
          onClick={() => setError(null)}
          className="mt-2 text-sm underline"
        >
          Try again
        </button>
      </div>
    );
  }

  return <ChatKit control={control} className="h-[600px]" />;
}
```

## Authentication Integration

### With Better Auth

```tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useAuth } from '@/lib/auth-client';

export function AuthenticatedChat() {
  const { session, token } = useAuth();

  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        if (!token) {
          throw new Error('Not authenticated');
        }

        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        const { client_secret } = await res.json();
        return client_secret;
      },
    },
  });

  if (!session) {
    return <p>Please log in to use the chat assistant.</p>;
  }

  return <ChatKit control={control} className="h-[600px]" />;
}
```

## Best Practices

### DO:

1. **Load ChatKit script early** - Use `strategy="beforeInteractive"` in Next.js.
2. **Handle authentication** - Pass JWT tokens to your session endpoint.
3. **Implement error states** - Show user-friendly messages on failures.
4. **Make it responsive** - Adjust chat dimensions for different screens.
5. **Provide loading states** - Show spinners while connecting.

### DON'T:

1. **Expose API keys** - Never put OPENAI_API_KEY in frontend code.
2. **Skip error handling** - Always catch and display errors gracefully.
3. **Hardcode dimensions** - Use responsive classes for sizing.
4. **Ignore accessibility** - Ensure chat is keyboard navigable.
5. **Block the main thread** - Use async/await properly.

## Testing

### Component Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { ChatWidget } from '@/components/ChatWidget';

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ client_secret: 'test-secret' }),
  })
) as jest.Mock;

describe('ChatWidget', () => {
  it('renders without crashing', async () => {
    render(<ChatWidget />);
    await waitFor(() => {
      expect(screen.getByRole('region')).toBeInTheDocument();
    });
  });

  it('handles session creation error', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));
    render(<ChatWidget />);
    await waitFor(() => {
      expect(screen.getByText(/failed/i)).toBeInTheDocument();
    });
  });
});
```

## References

- [OpenAI ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)
- [ChatKit.js Documentation](https://openai.github.io/chatkit-js/)
- [ChatKit React NPM](https://www.npmjs.com/package/@openai/chatkit-react)
- [ChatKit Advanced Samples](https://github.com/openai/openai-chatkit-advanced-samples)
- [Next.js App Router](https://nextjs.org/docs/app)
