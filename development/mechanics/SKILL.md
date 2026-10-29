---
genre_slug: mechanics
status: draft
kind: technique
markers: rank system, leaderboard, stand-alone device, mechanic, Fab device, template
file_markers: Mechanics, Devices
last_updated: 2026-10-26
pattern_counts: proven=0 confirmed=0 hypothesis=0 reference=0 contested=0
---

# Technique Skill: Mechanics (devices, game mechanics, map templates)

A recipe here says how to REBUILD something you already built and sold or used: a stand-alone device for Fab (for
example a rank system), a game mechanic made of devices and Verse, or a whole map template. Anyone using the kit can
then have it rebuilt without starting from zero. Nothing is learned without the owner's approval; a recipe saved from a
Fab product counts as confirmed at once, from a map it needs a second map.

## Rebuild from a recipe

1. `python Claude/hooks/skills_lib.py recipes mechanics <keyword>` (in a Fab product: the same command from the profile hooks folder).
2. Take the closest recipe. Follow its `steps` in order: place the `devices`, set the `settings`, connect the `wiring`, create the `files` (Verse) exactly as given,
   gather the `assets`, then do what `verify` says. Use the UEFN MCP for what it can do; give the owner the steps for the rest.
3. Say what you changed from the recipe and why. If nothing is close, build it and save a new recipe afterwards.

## Save a recipe (when the owner confirms the mechanic works)

Fab product: `python fab_lab.py draft-recipe <project> "<recipe name>"` writes a draft JSON (Verse files with their code, the
editor calls that worked in order, TODO fields). Fill every TODO from what really happened, then
`python skills_lib.py recipe-add mechanics <file.json> "<product or map name>"`.

JSON fields: `name`, `kind` (device | mechanic | template), `use` (what it is for, one or two sentences), `steps` (ordered, each one a
sentence), `devices` (list of "name: what it does"), `settings` (what to set on which device), `wiring` (what is connected to what),
`files` (list of {name, code} for Verse), `assets` (what it needs, with where it comes from), `verify` (how to see that it works).

The kit also prepares a recipe by itself from the Verse code (a Fab product, or every folder with a device in a map); refine it when you know more. The owner decides on the Skills page whether a recipe is shared in the kit.

No map names, personal paths, links or task ids in the text.

<!-- PATTERNS:BEGIN -->
<!-- PATTERNS:END -->
