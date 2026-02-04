---
name: React Integration
description: This skill should be used when the user asks to "connect React to agent runtime", "use useAgentSession", "use useMessages", "set up AgentServiceProvider", "stream agent responses", "build agent chat UI", "render conversation blocks", or needs to build a React frontend with @hhopkins/agent-runtime-react.
---

# React Integration

## Overview

The `@hhopkins/agent-runtime-react` package provides React hooks and context for connecting to the agent runtime backend. It handles:
- WebSocket connection management
- Session lifecycle
- Real-time streaming updates
- State management via Context + Reducer

## Installation

```bash
pnpm add @hhopkins/agent-runtime-react
```

## Provider Setup

Wrap the application with `AgentServiceProvider`:

```tsx
import { AgentServiceProvider } from "@hhopkins/agent-runtime-react";

function App() {
  return (
    <AgentServiceProvider
      apiUrl="http://localhost:3001"      // REST API URL
      wsUrl="http://localhost:3001"       // WebSocket URL (same server)
      apiKey="your-api-key"               // API key for auth
      debug={false}                       // Enable debug logging
    >
      <YourApp />
    </AgentServiceProvider>
  );
}
```

The provider:
- Initializes REST client and WebSocket manager
- Connects WebSocket immediately
- Loads initial session list
- Sets up event listeners for all WebSocket events

## Hooks

### useAgentSession

Manage session lifecycle - create, load, destroy sessions:

```tsx
import { useAgentSession } from "@hhopkins/agent-runtime-react";

function SessionManager() {
  const {
    session,           // Current session state (null if not loaded)
    runtime,           // Runtime state (sandbox status)
    isLoading,         // Operation in progress
    error,             // Last error
    createSession,     // Create new session
    loadSession,       // Load existing session
    destroySession,    // Destroy current session
    syncSession,       // Manually sync to persistence
    updateSessionOptions,  // Update session options
  } = useAgentSession(sessionId);  // Optional: auto-load on mount

  // Create a new session
  const handleCreate = async () => {
    const newSessionId = await createSession(
      "agent-profile-id",     // Agent profile reference
      "claude-agent-sdk",     // Architecture type
      { model: "sonnet" }     // Optional session options
    );
  };

  return (
    <div>
      <p>Sandbox: {runtime?.sandbox.status}</p>
      <button onClick={handleCreate}>New Session</button>
    </div>
  );
}
```

**Important:** Call `useAgentSession` at the page/container level to ensure WebSocket room is joined regardless of which child components render.

### useMessages

Access conversation blocks and send messages:

```tsx
import { useMessages } from "@hhopkins/agent-runtime-react";

function Chat({ sessionId }: { sessionId: string }) {
  const {
    blocks,              // ConversationBlock[] - pre-merged with streaming
    streamingBlockIds,   // Set<string> - IDs currently streaming
    isStreaming,         // boolean - any block streaming
    metadata,            // Token/cost info
    error,               // Last error
    sendMessage,         // Send message to agent
    getBlock,            // Get block by ID
    getBlocksByType,     // Filter blocks by type
  } = useMessages(sessionId);

  const handleSend = async (text: string) => {
    await sendMessage(text);
    // Response arrives via WebSocket events
  };

  return (
    <div>
      {blocks.map((block) => (
        <BlockRenderer
          key={block.id}
          block={block}
          isStreaming={streamingBlockIds.has(block.id)}
        />
      ))}
      <MessageInput onSend={handleSend} disabled={isStreaming} />
    </div>
  );
}
```

**Streaming behavior:** Blocks are pre-merged with streaming content. A temporary block with ID `"streaming"` appears during active streaming.

### useSessionList

List all sessions:

```tsx
import { useSessionList } from "@hhopkins/agent-runtime-react";

function SessionList({ onSelect }: { onSelect: (id: string) => void }) {
  const { sessions, isLoading, error, refresh } = useSessionList();

  return (
    <ul>
      {sessions.map((session) => (
        <li key={session.sessionId} onClick={() => onSelect(session.sessionId)}>
          {session.sessionId} - {session.type}
        </li>
      ))}
    </ul>
  );
}
```

### useWorkspaceFiles

Track files modified by the agent:

```tsx
import { useWorkspaceFiles } from "@hhopkins/agent-runtime-react";

function FileExplorer({ sessionId }: { sessionId: string }) {
  const { files, getFile } = useWorkspaceFiles(sessionId);

  return (
    <ul>
      {files.map((file) => (
        <li key={file.path}>
          {file.path}
          <pre>{file.content}</pre>
        </li>
      ))}
    </ul>
  );
}
```

### useSubagents

Track subagent transcripts:

```tsx
import { useSubagents } from "@hhopkins/agent-runtime-react";

function SubagentViewer({ sessionId }: { sessionId: string }) {
  const { subagents, getSubagent } = useSubagents(sessionId);

  return (
    <div>
      {subagents.map((subagent) => (
        <div key={subagent.id}>
          <h4>{subagent.name}</h4>
          <p>Status: {subagent.status}</p>
        </div>
      ))}
    </div>
  );
}
```

### useEvents

Access debug event log for monitoring WebSocket events:

```tsx
import { useEvents } from "@hhopkins/agent-runtime-react";

function DebugPanel() {
  const { events, clearEvents } = useEvents();

  return (
    <div>
      <button onClick={clearEvents}>Clear</button>
      {events.map((event, i) => (
        <pre key={i}>{JSON.stringify(event, null, 2)}</pre>
      ))}
    </div>
  );
}
```

## Rendering Blocks

Handle different block types when rendering:

```tsx
function BlockRenderer({ block, isStreaming }) {
  switch (block.type) {
    case "user_message":
      return <UserMessage content={block.content} />;

    case "assistant_text":
      return (
        <AssistantMessage
          content={block.content}
          isStreaming={isStreaming}
        />
      );

    case "tool_use":
      return (
        <ToolCall
          name={block.toolName}
          input={block.input}
        />
      );

    case "tool_result":
      return (
        <ToolResult
          content={block.content}
          isError={block.isError}
        />
      );

    case "thinking":
      return <ThinkingBlock content={block.content} />;

    case "subagent":
      return (
        <SubagentCall
          name={block.name}
          status={block.status}
        />
      );

    case "error":
      return <ErrorMessage message={block.message} />;

    default:
      return null;
  }
}
```

## Streaming Patterns

### Show typing indicator

```tsx
function Chat({ sessionId }) {
  const { blocks, isStreaming } = useMessages(sessionId);

  return (
    <div>
      {blocks.map((block) => <BlockRenderer key={block.id} block={block} />)}
      {isStreaming && <TypingIndicator />}
    </div>
  );
}
```

### Animated text streaming

```tsx
function AssistantMessage({ content, isStreaming }) {
  return (
    <div className={isStreaming ? "streaming" : ""}>
      {content}
      {isStreaming && <span className="cursor">|</span>}
    </div>
  );
}
```

### Optimistic updates

User messages appear immediately via optimistic updates. The hook dispatches `OPTIMISTIC_USER_MESSAGE`, then replaces it with the real message when `block_complete` arrives.

## Error Handling

Errors are surfaced in multiple ways:

```tsx
function Chat({ sessionId }) {
  const { error: sessionError } = useAgentSession(sessionId);
  const { error: messageError, blocks } = useMessages(sessionId);

  // Check hook-level errors
  if (sessionError) return <Error message={sessionError.message} />;

  // ErrorBlocks appear inline in the conversation
  const errorBlocks = blocks.filter((b) => b.type === "error");

  return <div>...</div>;
}
```

## Related Skills

- **overview** - Understanding the runtime architecture
- **backend-setup** - Setting up the backend server
- **agent-design** - Configuring agent profiles
