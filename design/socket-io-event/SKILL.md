---
name: socket-io-event
description: "World Pulse: When adding new real-time event types, modifying the WebSocket layer, or wiring new collectors to the frontend."
---

# Socket.io Event

**When to use:** When adding new real-time event types, modifying the WebSocket layer, or wiring new collectors to the frontend.

---

## Contract (from `src/shared/types.ts`)

All Socket.io payloads use this structure:

```ts
interface WSMessage {
  events: Event[];
  timestamp: number;
}
```

**Server → Client events:**

| Event name | Payload | When |
|---|---|---|
| `events:initial` | `{ events: Event[], timestamp }` | On client connect |
| `events:new` | `{ events: Event[], timestamp }` | When collector emits new data |

Do not invent new event names without adding them to `src/shared/types.ts`.

---

## Naming Convention

Event names use `domain:action` kebab format:
- `events:initial` — domain `events`, action `initial`
- `events:new` — domain `events`, action `new`

New events follow the same pattern: `events:expired`, `collector:status`, etc.

---

## Client-Side Handling (`src/renderer/hooks/useSocket.ts`)

```ts
socket.on('events:initial', (data: EventsPayload) => {
  setEvents(data.events);
  setInitialized(true);
});

socket.on('events:new', (data: EventsPayload) => {
  addEvents(data.events);
});
```

- Always type the payload — do not use `any`.
- Always destructure with the typed interface (`EventsPayload`), not raw `data.events`.

---

## Connection Config

```ts
const socket = io(SERVER_URL, {
  transports: ['websocket', 'polling'],
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 1000,
});
```

After Socket.io exhausts `reconnectionAttempts`, the `reconnect_failed` event triggers dormant-retry mode (every 30 s) — see `useSocket.ts`. Do not change this value without updating the dormant-retry logic.

---

## ConnectionStatus States (from `src/shared/types.ts`)

```ts
type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error' | 'dormant-reconnecting';
```

Always use these exact strings when calling `setConnectionStatus`. Never add new states without updating the type.

---

## Event Cache

The server caches max **100 events** in memory. The `addEvents` action in the Zustand store deduplicates by `id` and trims to 100. TTL is enforced by each collector's `expiresAt` field.

---

## Adding a New Event Type

1. Add `EventType` to the union in `src/shared/types.ts`.
2. Create a typed interface extending `Event` in the same file.
3. Register the collector in `src/server/index.ts`.
4. The frontend receives it automatically through `events:new` — no Socket.io code changes needed unless you need a separate channel.

---

## Anti-Patterns

- Do not call `socket.emit()` from the renderer — this is a server-push-only architecture.
- Do not create per-component socket connections — the single `useSocket` hook in `App.tsx` owns the connection lifecycle.
- Do not hold socket references in Zustand state — keep them in `useRef`.
- Do not use `socket.once()` for recurring events — use `socket.on()` with cleanup in `useEffect` return.
