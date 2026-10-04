---
name: add-socket-event
description: Use when adding any new socket event to the Salem 1692 multiplayer system. Covers all four required touch points — protocol definition, server dispatch with role enforcement, Unity handler, and web client handler. Invoke any time a new game feature requires a new message between server and clients.
---

# Add Socket Event

Every socket event in this project touches four places in a specific order.
Missing any one of them produces a silent failure. Follow these steps exactly.

## Step 1 — Classify the Event

Before writing any code, determine:

**Direction:**
- `server → clients` (game state change, prompt, phase signal)
- `client → server` (player action, vote, confession)

**Recipient type** (for server → clients events):
- `broadcast` — public game state; goes to host, ALL mirrors, ALL players
- `role-filtered` — goes only to clients of a specific role
- `individual` — goes to one specific player's socket only
- `display` — goes to host + all mirrors only

**Is this a secret phase prompt?**
If yes, stop here and use the `/implement-secret-phase` skill instead.

## Step 2 — Define the Event in docs/protocol.md

Create `docs/protocol.md` if it doesn't exist. Add the event with:
- Event name (snake_case)
- Direction and recipient type
- Full payload shape with field names and types
- Conditions under which this event fires

Commit this before writing implementation code.

## Step 3 — Implement Server-Side Dispatch

```js
// Broadcast (all clients)
io.to(roomCode).emit('event_name', payload);

// Role-filtered (players only)
const targets = getRoomSockets(roomCode).filter(s => s.role === 'player');
targets.forEach(s => s.emit('event_name', payload));

// Individual player
const socket = getPlayerSocket(roomCode, playerId);
if (socket) socket.emit('event_name', payload);

// Display only (host + mirrors)
const targets = getRoomSockets(roomCode).filter(
  s => s.role === 'host' || s.role === 'mirror'
);
targets.forEach(s => s.emit('event_name', payload));
```

Role enforcement happens here at dispatch — never rely on the client to ignore data.

## Step 4 — Handle in Unity

Add a case in the Unity WebSocket message handler:
```csharp
case "event_name":
    var data = JsonUtility.FromJson<EventNamePayload>(message.payload);
    GameManager.Instance.HandleEventName(data);
    break;
```

## Step 5 — Handle in Web Client

```js
socket.on('event_name', (data) => {
  store.dispatch(handleEventName(data));
});
```

Do not log or cache payload fields containing private data.

## Step 6 — Handle Incoming Client → Server Events

```js
socket.on('event_name', (data) => {
  if (socket.role !== 'player') return;
  const game = getGame(socket.roomCode);
  if (!game.isValidAction(socket.playerId, 'event_name')) return;
  const hostSocket = getHostSocket(socket.roomCode);
  if (hostSocket) hostSocket.emit('player_action', {
    playerId: socket.playerId,
    action: 'event_name',
    data
  });
});
```

## Step 7 — Test

- [ ] Correct recipient receives the event
- [ ] Wrong-role client does NOT receive the event
- [ ] Payload shape matches protocol.md
- [ ] Server rejects if sender role is wrong

## Step 8 — Update CLAUDE.md Socket Event Table

Add the new event to the socket event names table in CLAUDE.md.