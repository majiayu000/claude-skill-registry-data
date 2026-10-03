---
name: how
description: "Trace how a Roblox subsystem works across Instances, Luau modules, remotes, server authority, replication, persistence, and client presentation."
---

# Explain how the Roblox system works

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md). Answer from evidence, not naming conventions.

Trace the narrowest complete path:

1. Find the entry point from UI, input, lifecycle callback, tag, attribute, binder, service startup, or remote.
2. Follow requires and calls across client, shared, and server code. Identify the authoritative mutation and every trust boundary.
3. Track the data shape through creation, replication, persistence, cleanup, and failure.
4. Inspect referenced project mappings and authored Instances when source alone cannot establish placement or metadata. If Repository mode is unavailable, use the contract's Studio fallback mode for scoped non-playtest edits when the task explicitly requires them. Never control a playtest.
5. Explain the runtime sequence, key modules, invariants, and extension points. Cite exact paths and symbols.
6. Separate observed behavior from intended behavior and call out conflicts with repository design documents.

Keep the explanation proportional. A small function needs one trace, not a subsystem report.
