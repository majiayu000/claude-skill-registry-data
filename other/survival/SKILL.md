---
genre_slug: survival
status: draft
variants_draft: [loop-100, loop-infinito, space-war-2team]
last_updated: 2026-09-30
pattern_counts: proven=0 confirmed=0 hypothesis=0 contested=0
---

# Genre Skill: Survival

This file is read by the kit whenever a project has `Claude/docs/.genre = survival`.

## How this skill learns (Skill Harness)

This skill starts EMPTY on purpose and is never pre-written from general knowledge. It learns from
the maps the owner actually builds, one map at a time — no need to wait for 3 maps:

- After a playtest (or on request) the `skill-reflector` agent QUEUES lessons. Nothing is learned
  until the owner approves it on the **Skills** page of the Agent Console.
- Every pattern carries a confidence level computed from the owner's own maps:
  **hypothesis** (1 map) → **confirmed** (2 maps) → **proven** (3+ maps, or 2 + a retention metric).
  A map that does the opposite turns it into **contested**; nothing is silently overwritten.
- How to use the list below: PROVEN = follow as a rule. CONFIRMED = follow by default, say why if you
  deviate. HYPOTHESIS = only a suggestion, tell the owner it is unproven. CONTESTED = show both options
  and ask. If the list is empty, there is simply nothing learned yet — do not invent patterns.
- Private vs shareable: map names, task IDs and notes live in `local/` (never exported, never
  committed). `pack/patterns.json` holds only generalized patterns + support counts and is the one
  part that can be shared or merged from the community. Do not edit the block below by hand
  (`python Claude/hooks/skills_lib.py ...` regenerates it).

## Known variants (working labels; pattern `variant` field uses these slugs, or `*` for the whole genre)

See `references/variants.md`: **loop-100** (structured cycle/wave loop with a fixed count), **loop-infinito**
(continuous loop, no ending), **space-war-2team** (space setting, two opposing teams). These are the
creator's labels, not official Epic tags (see `~/.claude/skills/genre/fortnite-tags-known.json`).


## Dependencies (one-way, never the reverse)

This skill can read/cite the Device Library (second-brain) and the retention skill
(`fortnite-retention-gamedesign`). Those must NEVER contain logic specific to this genre.

<!-- PATTERNS:BEGIN -->
## Learned patterns (generated — do not edit by hand)

These come from maps the owner actually built and approved. Patterns the owner has not approved are not listed. Match the confidence to how you use each one.

_Nothing learned yet. Patterns appear here only after the owner approves a lesson from a real map._
<!-- PATTERNS:END -->
