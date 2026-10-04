---
name: multiplayer-sync
description: Owns deterministic multiplayer synchronisation — protocol, ordering, state hashes, reconnect, desync detection, match lifecycle. Use for anything touching the wire or the authority model.
---

# multiplayer-sync

## Purpose

Own everything between the two clients and the server. Keep two simulations in agreement, detect
it immediately when they are not, and make sure the server can always prove what happened.

## When to invoke

- Protocol or message-schema changes
- Authority, prediction or reconciliation changes
- Reconnect, session resumption or disconnect policy
- Any desync investigation
- When a battle mechanic needs to survive latency

## Inputs

- The change, and its effect on the wire
- Current protocol version
- Desync reports with seeds and action logs

## Responsibilities

Protocol messages · ordering · sequence numbers · state hashes · reconnects · latency · desync
detection · reconciliation · match lifecycle.

## Process

1. Express the change as **actions and events**, never as a state snapshot.
2. Confirm the server can validate it by re-simulating with the same core.
3. Add sequence numbers and, on actions, a state hash.
4. Test under hostile conditions before trusting it: duplicated, reordered, dropped, delayed.
5. Verify the reconnect path still works.

## Constraints

- **Never let rendering or UI concerns become authoritative game state.** This is the rule this
  skill exists to enforce.
- **Never trust the client.** Competitive clients are untrusted, full stop.
- Messages carry actions and events, not giant state snapshots.
- Every message: sequence number, turn, protocol version. Actions also carry a state hash.
- All timing in engine ticks. A client's wall clock must never influence simulation.
- Malformed messages are rejected, never partially applied — this is a security boundary.
- The server re-simulates using the **identical `/core` package**. Not a port, not a
  reimplementation, the same package.
- Match seeds are server-issued and unpredictable.

## The hard case

**An attack resolves while the player is mid-drag.**

This is where the game feels unfair if handled badly. The board must not move under their
finger, the drag must not be cancelled, and the feedback must still be clear. Whatever
resolution is chosen must be expressible in **engine ticks** — "defer until the drag ends" is a
client-timing concept and cannot leak into the simulation.

## Desync handling

1. Detect via periodic hash comparison
2. Locate the first divergent turn (checkpoint hashes make this a binary search)
3. Reconcile: the server is authoritative; the client rolls back and re-applies
4. The player should experience a correction, not a crash — ideally not notice at all
5. **Log enough context to distinguish our bug from a cheater.** Early on it will almost always
   be our bug, and a system that cannot tell them apart will accuse honest players.

## Outputs

- Protocol change with a version bump, client and server types generated from one source
- Multiplayer simulation tests covering the hostile conditions
- A note to `game-security` for anything touching validation or seeds

## Testing expectations

Deterministic network simulation — a seeded scheduler deciding drops, reorders and delays, so
every failure reproduces exactly from its seed. Both clients and the server in-process. Cover:
duplicates, reordering, drops, asymmetric latency, mid-match disconnect and reconnect, a client
that stops responding, messages after match end, both players acting in the same tick, and a
deliberately malicious client.

## Consults

`game-rules-engine` (validation) · `game-security` (threat model) ·
`replay-debugger` (divergence) · `game-test-engineer` (simulation harness) ·
`battle-system` (timing under latency) · `game-performance` (network traffic)

## Definition of done

The change survives every hostile network condition in simulation, the server can independently
validate it, desync is detected and located, and no UI concern has become authoritative.
