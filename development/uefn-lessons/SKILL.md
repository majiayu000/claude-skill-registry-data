---
name: uefn-lessons
description: Shared cross-project knowledge base of recurring Verse/UEFN gotchas, MCP quirks, and coding mistakes, accumulated across every project set up with this kit. Read it before writing or debugging Verse code, or when investigating a compile/runtime error, to check whether it's already a known issue. Also the place to add a new entry when you discover something non-obvious that would help on future projects too, not just this one.
---

# UEFN / Verse lessons learned

This file is shared across every project set up with this kit — unlike per-project agent
memory (`memory: project` in `coder`/`qa-regression`, which resets on every new island),
entries here persist and apply everywhere. It only becomes useful if agents are disciplined
about reading it before starting work and adding to it when they learn something new. Read it
directly (`~/.claude/skills/uefn-lessons/SKILL.md`) at the start of a coding or debugging task,
the same way you'd read `CLAUDE.md`.

## When to add an entry here vs. per-project memory

- **Here** (this file): the lesson is about Verse, UEFN, or the MCP tooling itself — it would
  apply on any island, not just this one. Example: "`@editable` on a field whose type isn't
  `<persistable>` fails to compile with a misleading 'Unknown identifier' error."
- **Per-project memory** (`coder`'s or `qa-regression`'s own memory, see
  `~/.claude/CLAUDE.md` rule 10): the lesson is specific to THIS project's devices, assets, or
  design decisions and wouldn't mean anything on a different island. Example: "this project's
  RespawnManager ignores calls made before BeginPlay finishes."

If in doubt, ask: "would this save me time on a different island?" If yes, it goes here, not in
per-project memory.

## How to add an entry

One line per lesson: symptom/cause, then how to recognize or avoid it. No long write-ups — the
point is to save tokens and rediscovery time across 50 projects, not to build another document
to maintain. Add new entries under the closest matching category below (add a new category if
none fits — keep the same one-line style). Never delete or rewrite someone else's entry without
being sure it's wrong; if a later project seems to contradict an existing entry, add a note
next to it rather than silently overwriting it — the contradiction itself might be useful
information (e.g. "only true for devices placed before v3x.x").

Remove the "(example — replace)" placeholder entries below once real ones are added; they're
only there to show the expected format, not to be kept as real lessons.

## Verse syntax gotchas
- (example — replace) `@editable` on a field whose type isn't marked `<persistable>` fails to
  compile with "Unknown identifier" instead of a clear type error — check the type's
  persistability first whenever this error shows up on an `@editable` line.

## Device behavior surprises
Device-TYPE-specific quirks (exact sizing math, orientation gotchas, and similar for
`DemoDisplay`, Elimination Manager, Item Granter, Storm Controller, Player Spawner, and others)
now live in `~/.claude/skills/uefn-device-gotchas/` instead of growing here — read that skill for
device-specific behavior. Keep this category for genuinely generic device-handling surprises that
don't fit a single device type.

## MCP / tooling quirks
- (example — replace) `mcp__unreal-mcp__call_tool` is a single dispatcher tool for every
  action — if a call behaves unexpectedly, check the JSON payload you're sending, not just the
  tool name.
- `get_actor_bounds` can be skewed by asymmetric components (e.g. a spotlight's cone), stretching
  the bounding box well past the actor's physical footprint on one side only. Don't trust it
  blindly for footprint/collision math — compute the "real" footprint from the actor's own set
  `width`/`depth`/`height` (symmetric around its location) instead, and use `get_actor_bounds`
  only to sanity-check the side you expect to be unaffected.
- **Don't use `AssetTools.find_assets` on `/Game` to look for a project's own custom content** —
  in this kit's MCP/UEFN setup, that path never exposes the project's actual custom Verse/assets,
  even with the right project open in UEFN (it silently returns nothing useful instead of erroring,
  which is what makes this easy to miss and mistake for "the project has no custom content" or
  "MCP isn't seeing the right project"). The tool that actually lists the real project content is
  **`ValkyrieToolset.VerseToolset.ListFiles`** — use that whenever you need to see what Verse/
  assets genuinely exist in the currently-open project, not `AssetTools.find_assets`. Confirmed by
  the owner directly testing both against the same open project.

## Performance pitfalls
- (example — replace) ...

## Multiplayer pitfalls
- (example — replace) ...

## Discover / retention signals
Moved to the dedicated `~/.claude/skills/discover-retention/` skill (which also tracks validated
proposal outcomes across projects, not just the static signal facts) — read that instead.
