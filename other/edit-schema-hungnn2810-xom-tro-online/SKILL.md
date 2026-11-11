---
name: edit-schema
description: Change Vỉa Hè Online's synced Colyseus state (server/src/schema.ts) and regenerate the C# classes for Unity with npm run schema-cs. Use this skill whenever a field has to be added, removed or retyped on StreetState, Player, Stall or Customer, or when the user wants the client to "see" something new about the street ("cho hiện số khách đang xếp hàng", "thêm trạng thái nhân viên"). Forgetting the codegen step leaves client and server silently out of sync, which is miserable to track down.
---

# Edit the synced schema

`server/src/schema.ts` is the contract between server and client. Colyseus encodes state by
**field order and type**, and the client decodes it with C# classes generated from this very
file. When the two drift there is no compile error anywhere — the client just reads garbage:
jumping positions, empty strings, wrong product ids. That is why the regeneration step is not
optional.

## Order of work

### 1. Edit `server/src/schema.ts`

```ts
export class Stall extends Schema {
  @type('uint8') slot = 0;
  @type('uint16') queueLength = 0;   // new field: appended at the end of the class
}
```

- **Append new fields at the end of the class.** Inserting in the middle shifts the index of
  every field after it, so an already-built client (the APK on someone's phone) decodes
  everything wrongly.
- Pick the smallest type that fits — this state goes out continuously to everyone on the
  street: `uint8` (0–255), `uint16` (0–65535), `int8` for a ±1 direction, `float32` for
  coordinates, `float64` only for `Date.now()` timestamps, `boolean`, `string`.
- For several values of the same kind, join a comma-separated string the way `outfit` and
  `wants` already do, rather than adding an `ArraySchema` — it is lighter and the client
  already has the splitting code.
- Every field needs an initialiser.

### 2. Regenerate the C#

```bash
cd server && npm run schema-cs
```

This runs `schema-codegen` into `client/Assets/Scripts/Schema/` (namespace
`ViaHeOnline.Schema`). **Never hand-edit files in that folder** — the next run wipes them.

Verify: `git diff --stat client/Assets/Scripts/Schema/` must show the class you changed.
Nothing there means the command did not really run (common cause: dependencies not installed —
`cd server && npm install`).

### 3. Populate the field on the server

A new field holds no data by itself. Find where the object is created and updated in the room
(`server/src/rooms/StreetRoom.ts`) and set it on every branch that changes the value. A field that
is declared but never written leaves the client reading the initialiser forever — a symptom
that looks exactly like a broken schema, so rule this out before suspecting the codegen.

### 4. Consume it on the client

Read it from the state in `client/Assets/Scripts/StreetScene.cs` (the street scene) or
`Game.cs` (coordination plus UI). Both already observe state through the Colyseus SDK
callbacks; follow the existing `_stalls` / `StallView` path instead of adding a new loop that polls
the state.

### 5. Run it

```
cd server && npm start      # separate window
cd server && npm test
```

`test/simulation.ts` connects to the real server with the SDK and reads `room.state`, so it
catches a broken schema immediately. Add a `check(...)` assertion for the new field if it
carries a game rule.

## Know which channel you want: synced state vs. profile

These are two separate data paths, and picking the wrong one is expensive to undo:

| | `schema.ts` (street state) | `profile.ts` (player profile) |
|---|---|---|
| Holds | What everyone on the street must see: positions, stalls, customers | What belongs to one player: money, level, wardrobe, employees, log |
| Transport | Colyseus state, synced continuously | `profile` message / HTTP, sent on change |
| Persisted | No, gone when the room closes | SQLite `server/data/game.db` |
| Client type | Generated into `Scripts/Schema/` | Hand-written in `Models.cs` |

Putting private information (someone's cash, their stock) into street state leaks it to every
other player, because state is broadcast to the whole room. That belongs in `profile.ts`, and
when types change there the matching class in `Models.cs` is updated by hand — there is no
codegen on that path.
