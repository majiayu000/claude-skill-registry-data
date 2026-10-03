---
name: roblox-networking
description: "Design or review Roblox remotes, replication protocols, payloads, reliability, and server validation."
---

# Roblox networking

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md). Inventory the existing remotes and both endpoints before changing a protocol.

## Define the protocol first

For each message, name its direction, purpose, sender, recipients, reliability, expected rate, payload type, validation, authoritative mutation, response, and compatibility behavior.

- Send player intent and stable identifiers, not client-computed outcomes, prices, ownership, arbitrary instance paths, or whole mutable objects. The server resolves identifiers against authoritative state.
- Use RemoteEvent for asynchronous one-way messages. Use RemoteFunction only when the caller truly needs an immediate reply and the handler is bounded. Never make authoritative server progress depend on a synchronous client callback.
- Use UnreliableRemoteEvent only for high-frequency, supersedable presentation data. Never use it for inventory, currency, rewards, purchases, permissions, or authoritative combat outcomes.
- Validate shape, size, range, class, ancestry, ownership, permission, rate, and current game state before mutation. Reject unknown fields when accepting them would broaden authority.
- Rate-limit per player and action. Bound payload size and fanout; coalesce cosmetic updates instead of emitting redundant state.
- Replicate authoritative snapshots or deltas with a revision when messages can race. Clients discard stale revisions and reconcile prediction without becoming authoritative.
- Keep remote connections and pending requests tied to a lifecycle owner. Handle player departure, character replacement, round reset, and protocol version mismatch.

Use `$roblox-security` when the task is an adversarial audit rather than protocol design.

## Deliverable

Return the protocol table or typed payload definitions, server validation order, authority and mutation path, rate policy, stale-message behavior, and compatibility plan. Verify codecs, validators, reducers, and sequencing locally; leave multiplayer and latency checks to the user's Studio playtest.
