---
name: uefn-device-gotchas
description: High-frequency UEFN device quirks and edge cases (Elimination Manager, Item Granter timing, Storm Controller, Player Spawner multiplayer behavior, DemoDisplay sizing/placement rules) at high density. Read before configuring one of these devices to avoid rediscovering a known trap.
---

# UEFN device gotchas

Device-specific quirks and edge cases — the "this device does something non-obvious" layer.
Complementary to `~/.claude/skills/uefn-lessons/SKILL.md`, which stays for generic
Verse/UEFN/MCP tooling gotchas (syntax, the MCP dispatcher, and similar) — this skill is
specifically about individual device TYPES behaving in ways their name/UI doesn't suggest.

## How to use this

Before configuring a device this skill has a file for, check it first. After hitting a
non-obvious device behavior, add a one-line entry to the matching reference file (or create a
new one for a device not covered yet) — same discipline as `uefn-lessons`: short, dense,
symptom + how to recognize/avoid it, not a paragraph.

## References
- `references/elimination-item-devices.md` — Elimination Manager, Item Granter, Accolade, Timer.
- `references/storm-spawner-position-critical.md` — Storm Controller/Beacon, Player Spawner, and
  other devices whose WORLD POSITION is itself gameplay-functional (never move these onto a
  DemoDisplay stand — see `~/.claude/CLAUDE.md` rule 7's gameplay-critical-position exception).
- `references/demodisplay-sizing.md` — the full DemoDisplay sizing/orientation/placement math
  (width/depth/height via `ObjectTools`, yaw-based relative positioning, the `get_actor_bounds`
  asymmetry gotcha). `~/.claude/CLAUDE.md` rule 7 keeps only the summary; read this file when
  you're actually about to size or place a stand, not for the general rule.

Read only the file matching the device you're touching, not all three.
