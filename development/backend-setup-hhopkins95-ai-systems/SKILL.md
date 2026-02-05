---
name: Backend Setup
description: This skill should be used when the user asks to "create an agent runtime server", "set up agent runtime backend", "configure Modal sandbox", "implement PersistenceAdapter", "start WebSocket server", "create REST API for agents", or needs to build a Node.js backend using @hhopkins/agent-runtime.
---

# Backend Setup

## Overview

Setting up an agent runtime backend involves:
1. Configuring environment variables
2. Implementing a PersistenceAdapter
3. Creating the runtime with configuration
4. Starting REST and WebSocket servers

## Environment Variables

Required environment variables:

```bash
# Modal credentials (for sandbox creation)
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret

# Anthropic API key (for Claude agents)
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Obtain Modal credentials from [modal.com](https://modal.com).

## Minimal Server Example

```typescript
import { createServer } from "http";
import { createAgentRuntime, type PersistenceAdapter } from "@hhopkins/agent-runtime";

// 1. Implement PersistenceAdapter (see references/types.md for full interface)
const persistence: PersistenceAdapter = {
  // Session operations
  listAllSessions: async () => [],
  loadSession: async (sessionId) => null,
  createSessionRecord: async (session) => {},
  updateSessionRecord: async (sessionId, updates) => {},

  // Storage operations
  saveTranscript: async (sessionId, rawTranscript) => {},
  saveWorkspaceFile: async (sessionId, file) => {},
  deleteSessionFile: async (sessionId, path) => {},

  // Agent profile operations
  listAgentProfiles: async () => [{ id: "default", name: "Default Agent" }],
  loadAgentProfile: async (agentProfileId) => ({
    id: "default",
    name: "Default Agent",
    systemPrompt: "You are a helpful assistant.",
    tools: ["Read", "Write", "Edit", "Bash"],
  }),
};

async function main() {
  // 2. Create runtime
  const runtime = await createAgentRuntime({
    persistence,
    modal: {
      tokenId: process.env.MODAL_TOKEN_ID!,
      tokenSecret: process.env.MODAL_TOKEN_SECRET!,
      appName: "my-agent-app",
    },
    idleTimeoutMs: 15 * 60 * 1000, // 15 minutes
    syncIntervalMs: 30 * 1000,      // 30 seconds
  });

  // 3. Start runtime (loads sessions, starts background jobs)
  await runtime.start();

  // 4. Create REST API server
  const restApp = runtime.createRestServer({
    apiKey: "your-api-key",
  });

  // 5. Create HTTP server and attach REST routes
  const httpServer = createServer(async (req, res) => {
    const response = await restApp.fetch(
      new Request(`http://${req.headers.host}${req.url}`, {
        method: req.method,
        headers: req.headers as any,
        body: req.method !== "GET" && req.method !== "HEAD"
          ? await getRequestBody(req)
          : undefined,
      })
    );

    res.statusCode = response.status;
    response.headers.forEach((value, key) => res.setHeader(key, value));
    res.end(await response.text());
  });

  // 6. Create WebSocket server on same HTTP server
  const wsServer = runtime.createWebSocketServer(httpServer);

  // 7. Start listening
  httpServer.listen(3001, () => {
    console.log("Server running on http://localhost:3001");
  });

  // 8. Graceful shutdown
  process.on("SIGTERM", async () => {
    httpServer.close();
    wsServer.close();
    await runtime.shutdown();
    process.exit(0);
  });
}

function getRequestBody(req: any): Promise<string> {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk: any) => body += chunk.toString());
    req.on("end", () => resolve(body));
    req.on("error", reject);
  });
}

main();
```

## Runtime Configuration

```typescript
const runtime = await createAgentRuntime({
  // Required: persistence adapter implementation
  persistence: PersistenceAdapter,

  // Required: Modal credentials
  modal: {
    tokenId: string,
    tokenSecret: string,
    appName: string,  // Modal app name for sandboxes
  },

  // Optional: idle timeout before session cleanup (default: 15 min)
  idleTimeoutMs: number,

  // Optional: sync interval for persisting state (default: 30 sec)
  syncIntervalMs: number,
});
```

## REST API Endpoints

The runtime creates these REST endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions/create` | Create new session |
| GET | `/sessions/:id` | Get session data |
| POST | `/sessions/:id/message` | Send message to agent |
| GET | `/sessions` | List all sessions |
| GET | `/agent-profiles` | List available agent profiles |
| GET | `/health` | Health check |

## Lazy Sandbox Pattern

Sandboxes are created lazily - not when a session is created, but when the first message is sent. This optimizes resource usage:

1. `POST /sessions/create` - Creates session record, no sandbox yet
2. `POST /sessions/:id/message` - First message triggers sandbox creation
3. Subsequent messages reuse the running sandbox
4. Idle timeout eventually terminates the sandbox

## SessionManager Access

Access the session manager for advanced operations:

```typescript
// Get all loaded sessions
const sessions = runtime.sessionManager.getLoadedSessions();

// Get specific session
const session = runtime.sessionManager.getSession(sessionId);

// Unload a session (terminates sandbox, syncs state)
await runtime.sessionManager.unloadSession(sessionId);

// Get session state
const state = session.getState();
```

## WebSocket Events

The WebSocket server emits these events to connected clients:

**Block streaming:**
- `session:block:start` - New block begins
- `session:block:delta` - Incremental text update
- `session:block:update` - Block metadata changes
- `session:block:complete` - Block finishes

**Session lifecycle:**
- `session:status` - Runtime state changes
- `session:metadata:update` - Token/cost updates

**Files:**
- `session:file:created` - New file in workspace
- `session:file:modified` - File changed
- `session:file:deleted` - File removed

**Subagents:**
- `session:subagent:discovered` - New subagent started
- `session:subagent:completed` - Subagent finished

**Errors:**
- `error` - Error occurred

## PersistenceAdapter

The PersistenceAdapter is the main integration point. Implement this interface to connect the runtime to your storage layer. See `references/types.md` for the full interface.

Common implementations:
- **In-memory** - For development/testing
- **SQLite** - For single-server deployments
- **PostgreSQL/MySQL** - For production
- **Convex/Supabase** - For serverless

## Related Skills

- **overview** - Understanding the runtime architecture
- **react-integration** - Building React frontends
- **agent-design** - Configuring agent profiles
