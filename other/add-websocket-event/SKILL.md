---
name: add-websocket-event
description: Add a real-time WebSocket event with server emit, client hook, and org-scoped rooms. Use when adding live updates like new leads, deal changes, or chat messages.
---

# add-websocket-event

Adds a new real-time event to the socket.io infrastructure. Creates the server-side emit, client-side listener hook, and ensures proper org/user room scoping.

## Inputs to gather

- **Event name** — e.g., `lead:new`, `deal:stage-changed`, `message:new`
- **Payload shape** — what data the event carries (e.g., `{ leadId, name, score }`)
- **Scope** — who receives it: `user` (single user), `org` (all org members), `room` (specific deal/conversation)
- **Trigger point** — which API mutation emits this event

## Steps

1. **Check socket infrastructure exists.** Read `apps/api/socket.ts`. If missing, create:
   - `socket.io` server attached to Express HTTP server
   - JWT auth middleware on connection handshake
   - Room join: user joins `user:{userId}` and `org:{orgId}` rooms on connect

2. **Define the event type** in `packages/shared/src/socket-events.ts`:
   ```typescript
   export interface ServerToClientEvents {
     "lead:new": (payload: { leadId: string; name: string; score: number }) => void;
   }
   ```

3. **Emit from the API route.** In the mutation handler (e.g., POST /api/leads):
   ```typescript
   io.to(`org:${orgId}`).emit("lead:new", { leadId: lead.id, name, score });
   ```

4. **Create client hook** at `apps/web/src/hooks/useSocketEvent.ts`:
   ```typescript
   export function useSocketEvent<T>(event: string, handler: (data: T) => void) { ... }
   ```

5. **Consume in the component:**
   ```typescript
   useSocketEvent("lead:new", (data) => {
     queryClient.invalidateQueries({ queryKey: ["/api/leads"] });
     toast({ title: `عميل جديد: ${data.name}` });
   });
   ```

6. **Run `/typecheck`** to verify shared types compile.

## Verification checklist

- [ ] Event emits on the correct mutation
- [ ] Only users in the correct room receive the event
- [ ] Client hook triggers re-fetch or UI update
- [ ] Auth: unauthenticated sockets cannot connect
- [ ] Reconnection: client auto-reconnects on disconnect
- [ ] `/typecheck` passes

## Anti-patterns

- Don't broadcast to all sockets — always scope to user/org/room
- Don't send large payloads — send IDs, let client re-fetch details
- Don't create a new socket connection per component — use a single shared connection
- Don't forget to disconnect on component unmount
