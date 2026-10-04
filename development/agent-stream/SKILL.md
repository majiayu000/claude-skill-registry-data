---
name: agent-stream
description: Work on SSE streaming, plain-text transport, ChatKit events, and session continuity. Use when debugging or modifying agent streaming behavior.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, mcp__openai-docs__search_openai_docs, mcp__openai-docs__fetch_openai_doc
---

Work on agent streaming: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for streaming patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK streaming" for RunStreamEvent types
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK RunStreamEvent" for event shape reference
2. Read the streaming infrastructure across repos:
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/shared/chatkit-bridge.ts` — `createStreamResponse()` (SSE) + `createPlainTextStreamResponse()` (text)
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/shared/stream-utils.ts` — `extractTextDelta()` from RunStreamEvent
   - `src/agents/shared/enhanced-agent-bridge.ts` — bridge streaming pipeline
   - `src/agents/shared/chatkit-bridge.ts` — local ChatKit bridge
3. Read the client-side transport:
   - `src/hooks/custom/use-standalone-chat.ts` — `TextStreamChatTransport`, session ID capture, 90s timeout fallback

## Dual Stream Formats

### SSE (Server-Sent Events) — Primary
`Content-Type: text/event-stream`

```typescript
function createStreamResponse(generator: AsyncGenerator<ChatKitEvent>): Response {
  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();
      for await (const event of generator) {
        const data = JSON.stringify(event);
        controller.enqueue(encoder.encode(`data: ${data}\n\n`));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

### Plain Text — Vercel AI SDK compatibility
`Content-Type: text/plain` (triggered by `?format=text` or `Accept: text/plain`)

```typescript
function createPlainTextStreamResponse(generator: AsyncGenerator<ChatKitEvent>): Response {
  // Concatenates only text_delta content, strips event metadata
  // Appends __AILAB_SESSION_ID__:uuid at the end for session capture
}
```

## ChatKit Event Types

```typescript
type ChatKitEvent =
  | { type: 'text_delta'; content: string }
  | { type: 'tool_call'; name: string; params: Record<string, unknown> }
  | { type: 'tool_complete'; name: string; result: unknown; duration: number }
  | { type: 'image'; url: string; alt?: string }
  | { type: 'done'; sessionId: string; finalOutput?: string }
  | { type: 'error'; message: string; code?: string }
  | ProgressEvent;

type ProgressEvent = {
  type: 'progress';
  phase: 'initializing' | 'context' | 'agent' | 'thinking' | 'tool_call' | 'generating' | 'complete';
  message?: string;
};
```

## Extracting Text Deltas from SDK Events

The `extractTextDelta()` function handles multiple event shapes from `RunStreamEvent`:

```typescript
function extractTextDelta(event: RunStreamEvent): string | null {
  // Searches multiple paths:
  // - event.delta
  // - event.data.delta
  // - event.data.output_text_delta
  // - Recursively flattens nested objects/arrays
  // Returns the first string content found, or null
}
```

## Session Continuity

### Server side
1. Request carries `conversationId` (or `sessionId` alias)
2. Response `done` event includes `sessionId` (generated UUID or from request)
3. Conversation persisted to `ai_lab_lite_conversations` table

### Client side
1. `useStandaloneChat` captures `__AILAB_SESSION_ID__:uuid` from plain-text stream
2. Stores sessionId in hook state
3. Sends sessionId on next request for multi-turn continuity

```typescript
// Client-side session extraction
const sessionMarker = '__AILAB_SESSION_ID__:';
const markerIndex = text.indexOf(sessionMarker);
if (markerIndex !== -1) {
  const sessionId = text.slice(markerIndex + sessionMarker.length).trim();
  setSessionId(sessionId);
  // Strip marker from displayed text
  text = text.slice(0, markerIndex);
}
```

## Message Windowing

```typescript
function windowMessages(messages: Message[], max: number = 50): Message[] {
  return messages.slice(-max); // Keep only latest N to avoid token overflow
}
```

## Debugging Streams

Common issues and how to investigate:

1. **Stream hangs/stalls**: Check for unresolved promises in the generator. The client has a 90s timeout fallback.
2. **Events out of order**: SSE guarantees ordering. If using plain-text, events are concatenated sequentially.
3. **Missing session ID**: Check that `done` event includes sessionId. In plain-text mode, verify the `__AILAB_SESSION_ID__` marker is appended.
4. **Tool events not rendering**: Verify the client-side SourcesPanel is parsing `tool_call` and `tool_complete` events.
5. **CORS errors**: Check the API route returns proper CORS headers for OPTIONS preflight.

## Rules

- Always include `Cache-Control: no-cache` and `Connection: keep-alive` on SSE responses
- The `done` event MUST include `sessionId` for conversation continuity
- Plain-text format must append `__AILAB_SESSION_ID__:uuid` marker for client extraction
- Window messages to prevent token overflow (default max 50)
- Handle stream errors gracefully — emit an `error` event, then close the stream
- Never buffer the entire response before streaming — send events as they arrive
- Test both SSE and plain-text formats when modifying stream behavior
- Check OpenAI docs MCP for any changes to RunStreamEvent types or streaming patterns
