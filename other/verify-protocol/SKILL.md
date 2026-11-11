---
name: verify-protocol
description: Check that Vỉa Hè Online's server and Unity client agree on message names, payload keys and HTTP routes. Use this skill after changing server/src/rooms/StreetRoom.ts, server/src/index.ts, Network.cs or any _net.Send call, before calling a feature finished, and when the user says "bấm không có tác dụng", "server không nhận", "client không nhận message", "lệch message" or a button silently does nothing. A wrong name fails silently at runtime, so run the script instead of reading the code by eye.
---

# Verify the client-server protocol

Run from the repository root:

```bash
node .agents/skills/verify-protocol/scripts/check-protocol.mjs
```

It exits 1 and prints `MISMATCH` lines when:

- the client sends or requests a message the server has no handler for
- a client payload lacks a required key, or has a key missing from the handler's inline `m: { ... }` type
- the server pushes a message the client does not listen for, or the reverse
- the client calls an `api/` route that `server/src/index.ts` does not define

Lines starting with `note:` do not fail the check. They mark payloads built elsewhere, such as
`WithDressTarget`, and server messages no client code sends yet. Read those by hand when your
change touches them.

## Fixing a mismatch

The server is the source of truth for game rules. Fix the side that drifted, in both the handler
and the client call, then run the script again. Message names and keys are English identifiers;
only the text shown to players is Vietnamese.

## What it does not check

- Fields of `Profile`, `Catalog` and other response classes in `Models.cs`
- Payloads whose handler has a named type, such as `Partial<Appearance>`
- Value types, and helpers that wrap `_net.Send` under another name

For synced state in `server/src/schema.ts`, use the `edit-schema` skill.
