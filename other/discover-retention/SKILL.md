---
name: discover-retention
description: Concrete Fortnite Discover/retention signals (bounce rate, average playtime, QPTR) and patterns validated across real projects. Read during project-bootstrap's A4 step, before writing retention/evolutionary proposals, instead of reasoning about playtime from scratch.
---

# Discover / retention signals

Two references, read only the one you need:
- `references/discover-signals.md` — what Fortnite's Discover surfacing actually measures
  (curated facts, sourced from Epic's official docs, doesn't change often).
- `references/validated-patterns.md` — proposals that were actually tried on real projects and
  their outcome (grows over time as `project-bootstrap` and the owner learn what worked).

## How to use this in A4 (project-bootstrap's retention step)
1. Read `references/discover-signals.md` to ground proposals in what Discover measures, not
   generic "increase playtime" advice.
2. Before finalizing the proposal list, also query the Obsidian second brain (if configured —
   see the `second-brain-query` skill) for what's already been tried on other projects and its
   real outcome, and prefer a track-recorded proposal over a purely theoretical one when both
   apply.
3. When a proposal targets a specific signal, name it explicitly (e.g. "add a mid-session hook
   around minute 8 to reduce bounce past the 5-minute mark").
4. If a proposal's real outcome becomes known later (the owner reports back after using it),
   that's the kind of thing worth adding to `references/validated-patterns.md` — see that file's
   own instructions.
