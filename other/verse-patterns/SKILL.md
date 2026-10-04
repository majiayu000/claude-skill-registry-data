---
name: verse-patterns
description: Reusable Verse code idioms (state machines, multiplayer authority, centralized logging, timers, item pools, round progression) at high density. Read before writing a common gameplay pattern from scratch, so you adapt a known-good shape instead of re-deriving or re-reading old project files for it.
---

# Verse patterns

Generic Verse language/structure idioms — how to shape a state machine, how to write
multiplayer-safe shared-state code, and similar. NOT the same thing as the Obsidian second
brain's device/mechanic articles (see `second-brain-query` skill): those hold a specific,
validated, full device implementation with a history of which projects it ran on; this skill
holds language-level shapes with no project history attached. Check both when relevant — a
second-brain article for the specific device you're building, this skill for the general pattern
underneath it.

## How to use this

1. Before implementing a pattern that's likely generic (state machine, timer, item pool,
   round/phase progression, anything needing server/client authority reasoning), check the
   `references/` file matching it below.
2. Adapt the pattern to the task — these are shapes, not drop-in code for a specific device.
3. If you land on a cleaner shape than what's here, or a category isn't covered yet, update the
   matching reference file (or add a new one) with a short, dense entry — same discipline as
   `uefn-lessons`: one clear example beats a paragraph of explanation.

## References
- `references/multiplayer.md` — server/client authority shapes, replication gotchas.
- `references/state-machine.md` — phase/state transition patterns.
- `references/logging-timers.md` — the centralized logger pattern (see also
  `Claude/reference/logger-template.verse.txt`) and common timer/cooldown shapes.
- `references/item-pool-round-progression.md` — item pool rotation, round/phase progression
  loops.

Don't read all four for every task — only the one that matches what you're about to build.
