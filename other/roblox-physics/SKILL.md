---
name: roblox-physics
description: "Design or review Roblox assemblies, constraints, collision, hit detection, and network ownership."
---

# Roblox physics

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md). Inspect the authored hierarchy, assemblies, roots, anchoring, attachments, constraints, collision groups, and current ownership code before changing behavior.

## Treat simulation as distributed and untrusted

- Decide network ownership at the assembly level as both a responsiveness and authority choice. Client ownership reduces input latency and server work, but the client can manipulate its simulation.
- Keep gameplay-critical assemblies server-owned when practical. For responsive player-controlled physics, assign ownership deliberately and validate server-observed position, speed, state transitions, and outcomes within game-specific tolerances.
- Reapply or release explicit ownership when seats, characters, tools, assemblies, or round state change. Anchoring and reconnecting parts can change the ownership model.
- Do not treat `Touched` alone as proof of authoritative damage, collection, or completion. Confirm server-side identity, spatial plausibility, state, cooldown, and duplicate behavior; use an appropriate ray or swept spatial query for fast motion.
- Prefer attachments and constraints for simulated mechanisms. Apply forces or impulses to the intended assembly instead of fighting physics with repeated per-frame transforms or velocity assignments.
- Make collision groups and query filters explicit. Exclude the source assembly, validate returned instances and ancestry, and separate physical collision from detection when gameplay requires different rules.
- Bound active simulated assemblies, query frequency, and per-frame work. Measure server physics cost, replication, and mobile client behavior before optimizing.

## Deliverable

State the assembly root, owner through each lifecycle state, authority checks, collision and query rules, constraint model, cleanup, and failure behavior. Verify pure hit-validation and state-transition logic locally. Give the user exact Studio checks for ownership visualization, multiple clients, latency, reset, and high-speed contact; never invoke the playtest through MCP.
