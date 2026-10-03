---
name: roblox-security
description: "Review or design Roblox remotes, server authority, purchases, rewards, RNG, persistence, and anti-abuse behavior."
---

# Roblox security review

For every externally triggered action, write the server-side contract:

- caller identity and allowed state;
- payload type, bounds, ownership, permissions, and rate;
- authoritative lookup and mutation;
- replay, duplicate, retry, reconnect, and race behavior;
- persisted outcome and failure handling;
- response data safe to replicate.

Inspect every path to the protected mutation, not only the named RemoteEvent or RemoteFunction. Consequential RNG stays server-side and survives retries without offering a reroll. Purchase fulfillment and rewards are idempotent. DataStore updates preserve session ownership and schema compatibility. Fail closed without corrupting or silently deleting player data.

Return exploitable paths first, with exact evidence and a concrete server-side correction. Separate real security findings from defense-in-depth suggestions.
