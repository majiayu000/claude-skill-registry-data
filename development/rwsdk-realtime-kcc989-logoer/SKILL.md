---
name: rwsdk-realtime
description: Use when building realtime features with rwsdk/RedwoodSDK on Cloudflare - covers WebSocket setup, Durable Objects configuration, bidirectional client-server updates, and scoped realtime groups. Triggers include collaborative editing, live updates, multi-user sync, or any feature needing push updates without polling.
---

# rwsdk Realtime

Real-time bidirectional updates using Cloudflare Durable Objects and WebSockets. No polling required.

## Setup (4 Parts Required)

### 1. Client Initialization

```tsx
import { initRealtimeClient } from 'rwsdk/realtime/client';

initRealtimeClient({ key: window.location.pathname });
```

The `key` determines which clients share updates (see Scoping below).

### 2. Export Durable Object

In your worker entry file:

```ts
export { RealtimeDurableObject } from 'rwsdk/realtime/durableObject';
```

### 3. Wire Up Route

```ts
import { realtimeRoute } from 'rwsdk/realtime/worker';
import { env } from 'cloudflare:workers';

export default defineApp([
  realtimeRoute(() => env.REALTIME_DURABLE_OBJECT),
  // ... your routes
]);
```

### 4. Configure wrangler.jsonc

```jsonc
{
  "durable_objects": {
    "bindings": [
      {
        "name": "REALTIME_DURABLE_OBJECT",
        "class_name": "RealtimeDurableObject",
      },
    ],
  },
}
```

## How It Works

rwsdk builds on React Server Components: when state changes, the server re-renders UI and sends it to clients.

1. Event occurs (user action or external trigger)
2. App state updates via RSC action handlers
3. Re-render triggers automatically (from action) or explicitly via `renderRealtimeClients()`
4. Each connected client receives updated UI

No subscriptions or manual diff tracking needed.

## Scoping Updates with Keys

The `key` groups clients into the same Durable Object instance:

```ts
// Only room-42 clients receive these updates
initRealtimeClient({ key: '/chat/room-42' });
```

All clients with matching keys share updates. Different keys = isolated groups.

## Update Patterns

### Client → Server → Client

Standard RSC pattern. When one client triggers an action, all clients with the same `key` re-run server logic:

```tsx
const Note = async ({ ctx }: RequestInfo) => {
  return <Editor content={ctx.content} />;
};
```

When any client edits, all clients re-render with fresh data.

### Server → Client (Push Updates)

For updates not triggered by user action (background jobs, admin triggers, external events):

```ts
import { renderRealtimeClients } from 'rwsdk/realtime/worker';
import { env } from 'cloudflare:workers';

await renderRealtimeClients({
  durableObjectNamespace: env.REALTIME_DURABLE_OBJECT,
  key: '/note/some-id',
});
```

## API Reference

| Function                                                  | Purpose                                                        |
| --------------------------------------------------------- | -------------------------------------------------------------- |
| `initRealtimeClient({ key? })`                            | Initialize WebSocket client. `key` scopes which group to join. |
| `realtimeRoute((env) => namespace)`                       | Connect WebSocket route to Durable Object.                     |
| `renderRealtimeClients({ durableObjectNamespace, key? })` | Push re-render to all clients in a key group.                  |

## Common Patterns

**Collaborative editing**: Use document ID as key (`/doc/${docId}`)

**Chat rooms**: Use room identifier as key (`/chat/${roomId}`)

**User-specific updates**: Use user ID as key (`/user/${userId}`)

**Global broadcasts**: Use shared key (`/global`)

## Why WebSockets + Durable Objects?

WebSockets provide persistent bidirectional connections—reused for both pushing updates and receiving actions. Durable Objects persist across requests, maintain state, and coordinate connected clients.
