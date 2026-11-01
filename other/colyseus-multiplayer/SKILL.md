---
name: colyseus-multiplayer
description: >-
  Build authoritative real-time multiplayer servers with Colyseus 0.17+. Use when implementing rooms, schema state sync, client message validation, matchmaking, authentication, reconnection handling, or server-side anti-cheat constraints. Keywords: colyseus, room lifecycle, schema, multiplayer, websocket, matchmaking, onJoin, onLeave, onDrop, allowReconnection.
allowed-tools: Read, Write, Edit, Bash
---

> **CampusCove note.** Vendored from [pantheon-org/tekhne](https://github.com/pantheon-org/tekhne) @ 659d0a6 (`skills/specialized/colyseus-multiplayer/`, SKILL.md and references only; its audits and evals were left out), MIT (`_third-party/LICENSE-tekhne.txt`); only this note was added.
>
> **API to trust:** CampusCove runs `colyseus` 0.17.10 / `@colyseus/core` 0.17.42 and `@colyseus/sdk` 0.17 on the client. In 0.17 a dropped socket calls `onDrop(client, code)`, where you call `this.allowReconnection(client, seconds)`; a return calls `onReconnect(client)`; `onLeave(client, code)` is the final leave. The room implementation example and `onLeave(client, consented)` in this skill are the older API, and `setState` is outdated: follow `references/room-lifecycle-and-state.md` and `node_modules/@colyseus/core/build/Room.d.ts`. The SDK reconnects automatically by default.
>
> **Different architecture:** `socket/` is plain ESM JavaScript (no TypeScript, no decorators, no Zod) and does **not** use Schema state: `CityRoom` keeps players in a `Map` and syncs with explicit messages to visible clients (`forEachVisibleClient`), and positions are absolute but checked by `socket/src/movement.ts`. Do not migrate to Schema or deltas unless asked; take the principles (validate, authorize, rate-limit, bounded reconnection). Known gap: `CityRoom` has no `onDrop`, so a network blip ends the session; reconnection must also keep `sessionByAccountId` and the one-session-per-account rule (close 4001) consistent. Ignore the scaffold / Bun / `pantheon-skill-auditor` / `rumdl` commands. Message recipe: skill `socket-message`.
>
> Advisory reference: CampusCove's own skills (`game-feature`, `socket-message`, `playtest-game`, ...) win on any conflict.

# Colyseus Multiplayer

## Philosophy

- Treat every client as untrusted: the server decides, the client only asks.
- Validate before you mutate: parse the payload, check ownership and rules, then change state.
- Plan for dropped connections as the normal case, not the exception.
- Keep synchronised state in Schema and keep matchmaking metadata honest about the room.

## When to Use

- Building server-authoritative multiplayer game backends with Colyseus 0.17+.
- Defining rooms, Schema state and lifecycle hooks (`onCreate`, `onJoin`, `onLeave`, `onDrop`).
- Writing message handlers that must validate client payloads and resist cheating.
- Configuring matchmaking metadata, authentication or reconnection policy.

## When Not to Use

- Peer-to-peer networking, where there is no authoritative server.
- Single-player game architecture with no networked state.
- Client-side rendering or prediction code that never touches room logic.

## Core Principles

1. Server is authoritative for all game state.
2. Room state changes must be validated before applying.
3. Reconnection and drop handling must be explicit.
4. Matchmaking metadata must reflect real room capability.

## Deterministic Workflow

1. Define state models in Schema.
2. Implement room lifecycle hooks (`onCreate`, `onJoin`, `onLeave`, `onDrop`).
3. Register message handlers with payload validation.
4. **Checkpoint:** Verify schema sync with a test client before proceeding — confirm field changes propagate and no plain properties are used for game-critical state.
5. Wire matchmaking and metadata filters.
6. Add reconnection policy and timeout behavior.
7. **Checkpoint:** Simulate a transient disconnect and confirm `allowReconnection` restores session — verify the player is not ejected prematurely.
8. Verify full room behavior with local multi-client runs.

## Quick Commands

### Scaffold a Colyseus app

```bash
npm create colyseus-app@latest server
```

Expected result: runnable Colyseus project in `server/`.

### Install and run with Bun

```bash
cd server && bun install && bun run src/index.ts
```

Expected result: server listening on configured port.

### Run with Node scripts

```bash
cd server && npm install && npm run start
```

Expected result: room handlers and matchmaker initialized.

### Evaluate this skill quality

```bash
pantheon-skill-auditor evaluate specialized/colyseus-multiplayer --json
```

Expected result: updated dimension score breakdown.

### Lint this skill docs

```bash
rumdl check specialized/colyseus-multiplayer
```

Expected result: no rumdl violations.

## Room Implementation Example

The following shows lifecycle hooks, Schema state, and reconnection handling together:

```typescript
import { Room, Client } from "@colyseus/core";
import { Schema, type, MapSchema } from "@colyseus/schema";

class Player extends Schema {
  @type("string") sessionId: string = "";
  @type("number") x: number = 0;
  @type("number") score: number = 0;
}

class GameState extends Schema {
  @type({ map: Player }) players = new MapSchema<Player>();
}

export class GameRoom extends Room<GameState> {
  maxClients = 4;

  onCreate(options: any) {
    this.setState(new GameState());

    this.onMessage("move", (client, payload: { dx: number; dy: number }) => {
      const player = this.state.players.get(client.sessionId);
      if (!player) return;

      // Server-side validation: cap movement delta
      const dx = Math.max(-5, Math.min(5, payload.dx));
      const dy = Math.max(-5, Math.min(5, payload.dy));
      player.x += dx;
      player.y += dy;
    });
  }

  onJoin(client: Client, options: any) {
    const player = new Player();
    player.sessionId = client.sessionId;
    this.state.players.set(client.sessionId, player);
  }

  async onLeave(client: Client, consented: boolean) {
    if (!consented) {
      // Hold the slot for up to 20 seconds on transient disconnect
      const reconnection = await this.allowReconnection(client, 20);
      if (!reconnection) {
        this.state.players.delete(client.sessionId);
      }
    } else {
      this.state.players.delete(client.sessionId);
    }
  }

  onDispose() {
    console.log("Room disposed");
  }
}
```

## Anti-Patterns

### NEVER trust client position or score updates directly

**WHY:** Clients are untrusted and can be modified for cheating.

**BAD:** Apply `payload.x` and `payload.score` without server checks.

**GOOD:** Validate movement delta and compute score on server.

```typescript
// BAD
this.onMessage("move", (client, payload) => {
  player.x = payload.x;
  player.score = payload.score;
});

// GOOD
this.onMessage("move", (client, payload: { dx: number }) => {
  const player = this.state.players.get(client.sessionId);
  if (!player) return;
  const dx = Math.max(-5, Math.min(5, payload.dx)); // clamp server-side
  player.x += dx;
  // score computed exclusively by server logic, never from client
});
```

**Consequence:** Competitive integrity is lost and leaderboard data is corrupted.

### NEVER mutate non-Schema fields expecting automatic sync

**WHY:** Only Schema-decorated fields are synchronized to clients.

**BAD:** Store gameplay-critical values in plain class properties.

**GOOD:** Keep synchronized values in Schema fields and collections.

```typescript
// BAD
class Player extends Schema {
  hp: number = 100; // plain property — not synced
}

// GOOD
class Player extends Schema {
  @type("number") hp: number = 100; // decorated — synced automatically
}
```

**Consequence:** Clients desync and render stale or inconsistent state.

### NEVER skip reconnection handling for transient disconnects

**WHY:** Mobile and unstable networks frequently drop short-lived connections.

**BAD:** Remove player immediately in `onLeave` for all disconnects.

**GOOD:** Use `allowReconnection` with a bounded timeout, falling back to removal only on expiry.

```typescript
// BAD
async onLeave(client: Client, consented: boolean) {
  this.state.players.delete(client.sessionId);
}

// GOOD
async onLeave(client: Client, consented: boolean) {
  if (!consented) {
    const reconnection = await this.allowReconnection(client, 20);
    if (!reconnection) {
      this.state.players.delete(client.sessionId);
    }
  } else {
    this.state.players.delete(client.sessionId);
  }
}
```

**Consequence:** Players are ejected from active matches unnecessarily.

### NEVER expose privileged room messages to all clients

**WHY:** Admin or host-only actions must be authorization-gated.

**BAD:** Let any client trigger `startMatch` or `kickPlayer`.

**GOOD:** Verify role/ownership before privileged actions.

```typescript
// BAD
this.onMessage("startMatch", (client) => {
  this.startMatch();
});

// GOOD
this.onMessage("startMatch", (client) => {
  if (client.sessionId !== this.hostSessionId) return; // guard
  this.startMatch();
});
```

**Consequence:** Match flow can be hijacked by unauthorized clients.

### NEVER skip payload validation on message handlers

**WHY:** Malformed or hostile payloads can crash the handler or corrupt shared state.

**BAD:** Read `payload.dx` without checking its shape.

**GOOD:** Parse the payload with a schema validator and return early when it fails.

```typescript
const parsed = moveSchema.safeParse(payload);
if (!parsed.success) return;
```

**Consequence:** One bad message can break the room for every player.

### NEVER accept absolute client coordinates

**WHY:** Absolute positions let a modified client teleport; deltas can be clamped and range-checked on the server.

**BAD:** `player.x = payload.x`.

**GOOD:** Accept a delta, clamp it server-side and apply it to the stored position.

**Consequence:** Players can move anywhere instantly and bypass level geometry.

### NEVER hardcode matchmaking metadata

**WHY:** Metadata drives room discovery, so values that do not reflect the room's real mode and capacity send players to the wrong rooms.

**BAD:** `this.setMetadata({ mode: "ranked" })` regardless of the options the room was created with.

**GOOD:** Derive `mode`, region or skill values from the creation `options` in `onCreate` and keep them consistent with runtime state.

**Consequence:** Players are matched into rooms that do not match their request.

### NEVER leave spam-prone messages without rate limiting

**WHY:** Unthrottled message types allow one client to flood the room and starve other players.

**BAD:** Process every `move` message the moment it arrives.

**GOOD:** Enforce a cooldown or per-client message budget on spam-prone message types.

**Consequence:** A single client can degrade latency for the whole room.

### NEVER use an unbounded or mismatched reconnection window

**WHY:** Seats held too long block other players, and a window too short for the mode ejects players unfairly.

**BAD:** Hold a ranked slot for minutes, or pass no timeout to `allowReconnection`.

**GOOD:** Use a bounded grace period for the mode: 20-30 seconds casual, 10-15 seconds ranked, strict for tournaments.

**Consequence:** Rooms stay half empty, or players lose matches to brief network drops.

## References

| Topic | Reference | When to Use |
| --- | --- | --- |
| Room lifecycle and state | [references/room-lifecycle-and-state.md](references/room-lifecycle-and-state.md) | Schema setup, lifecycle hook order, state synchronisation |
| Message validation and security | [references/message-validation-and-security.md](references/message-validation-and-security.md) | Server-side payload validation and anti-cheat patterns |
| Matchmaking and reconnection | [references/matchmaking-and-reconnection.md](references/matchmaking-and-reconnection.md) | `allowReconnection`, metadata filters and timeout policy |
