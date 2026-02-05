---
name: ui-embed
description: Embed the chatbot UI inside Docusaurus and connect it to the FastAPI RAG backend. Use when building chat components, handling streaming responses, or integrating chat widgets into MDX pages.
---

# UI Embed Skill

## Instructions

1. **Build component**
   - Create React chat panel (`ChatbotPanel.tsx`) with:
     - Message list
     - Input field
     - Mode toggle (RAG vs Selected Text)
     - Source list display
   - Handle streaming responses (EventSource/fetch reader)
   - Include loading and error UI states

2. **API client**
   - Create fetch helpers for `/query` and `/query/selected`
   - Include page metadata (module/week/title) for logging
   - Debounce/trim inputs; enforce max length

3. **Integration**
   - Add to `src/theme/Layout` or dedicated `Chat` page
   - Optionally show floating button
   - Provide MDX shortcode to drop chat in specific chapters

4. **UX and accessibility**
   - Basic console logging for failures
   - Friendly fallback messages
   - Focus management, keyboard submit
   - Readable contrast

## Examples

```tsx
// ChatbotPanel.tsx
import React, { useState } from 'react';

export function ChatbotPanel({ apiUrl }: { apiUrl: string }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState<'rag' | 'selected'>('rag');
  
  // ... implementation
}
```

```mdx
{/* In any MDX page */}
import { ChatbotPanel } from '@site/src/components/ChatbotPanel';

<ChatbotPanel apiUrl={process.env.API_URL} />
```

## Definition of Done

- Widget renders in Docusaurus dev build; can query backend
- Selected-text path sends provided text and returns grounded answer
- Error/loading states visible; minimal styling but responsive
- Integration steps documented for future pages
