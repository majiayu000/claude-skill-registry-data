---
name: socket-message
description: Add or change real-time multiplayer behaviour in CampusCove's Colyseus server (socket/) and its client (front useGameRealtime) — a new client→server message, a broadcast/sync, zone visibility, movement or reach checks, a socket→Laravel call. Use for anything shared live between players (doors, positions, furniture, held items, emotes).
---

# CampusCove real-time message

One Colyseus room, `CityRoom` (`socket/src/CityRoom.ts`), holds the town **and** every interior: a player's
`zone` (`city`, `apartment`, `work:<key>`) only decides who sees whom (`players.ts` `visibilityKey`,
`forEachVisibleClient`). The socket is plain ESM JavaScript (no TypeScript), 2-space, no semicolons.

| File | Owns |
|---|---|
| `CityRoom.ts` | `onMessage` registry (all in `onCreate`), join/leave, move, doors, housing polling |
| `players.ts` | player record, `publicPlayer`, input normalizers (`normalizeNumber`, ...) |
| `movement.ts` | `moveRejection`: speed, world bounds, locked houses → `position_correction` |
| `doors.ts` | reach (`DOOR_REACH = 3`), `canUseDoor`, door ids (`work:<key>` / unit public id) |
| `world.ts` | parses `world.manifest.json` at boot (spawn, bounds, houses, work doors) |
| `apartments.ts` | furniture placement, forwarded to the API |
| `backend.ts` | `callBackendJson(token, path, method, body)`, `errorPayload` |

## Server side

1. Register in `onCreate`: `this.onMessage('verb_noun', (client, payload) => this.onVerbNoun(client, payload))`.
   Names are `snake_case`; replies/errors follow `<thing>_sync`, `<thing>_error`, `<thing>_updated`.
2. Treat `payload` as hostile: look the player up (`this.players.get(client.sessionId)`), return silently if
   missing; validate every field's type; derive identity, owner, position and zone **from server state**, never
   from the payload. When merging a payload into a backend body, spread it **first** and put server fields last
   (`{ ...payload, owner_account_id: house.ownerAccountId }`) — the reverse was a real exploit.
3. Check the rule the client also checks: reach (`isWithinReach`), zone, lock (`canUseDoor`), cooldown
   (see `HOUSING_REFRESH_COOLDOWN_MS` pattern: per-player timestamp).
4. Persistent effects go through the API with the player's own token: `callBackendJson(player.token, '/housing/...')`.
   The API stays authoritative for money, items, ownership; on failure send `errorPayload(err, msg, code)`
   to that client only. Wrap async handlers so a rejection is `warn(...)`-logged, never crashes the room.
5. Broadcast to the smallest audience: `this.forEachVisibleClient(player, fn, client)` (same zone, excluding
   sender) or `{ zone: 'city' }` for town-wide state. Send full small state (`doors_sync` sends the whole set)
   rather than deltas unless the payload is large. Skip no-op broadcasts.
6. Anything that must also be known by the front (positions, door points) belongs in `world.manifest.json`,
   not hard-coded in `config.ts`.

`socket/` is mounted with `node --watch`: saving restarts the server (all players reconnect). Only
`package.json` changes need `make rebuild-socket`. Logs: `docker logs -f campuscove-socket`.

## Client side

1. Type the payload in `front/src/types/gameRealtime.ts` (interface, no `any`).
2. Handle it in `front/src/composables/game/useGameRealtime.ts` next to the others:
   `room.onMessage('doors_sync', (data: { openDoors: string[] }) => deps.onDoorsSync(data.openDoors))` — the
   realtime composable only routes; the feature composable (`useCityHousing`, `useHouseFurniture`, ...) owns
   the logic through a `deps.onX` callback.
3. Send with `room.send('verb_noun', payload)` from the feature composable via a function exposed by
   `useGameRealtime`; throttle anything per-frame (movement already throttles).
4. Apply corrections from the server (`position_correction`) instead of fighting them; clamp frame `dt` so a
   background tab does not produce a rejected jump.

For room lifecycle, reconnection (`onDrop` / `allowReconnection`, not implemented yet) and general anti-cheat
principles, see the vendored `colyseus-multiplayer` skill; its CampusCove note says which of its APIs match 0.17.

## Verify

Two browser tabs with two different accounts (one session per account: a second tab of the same account
kicks the first with code 4001). Check: both see the change, a player in another zone does not, an
out-of-reach or forged message is ignored (send it from the console: `window` has no room handle, so test
by walking away first). Skill `playtest-game` has the setup.
