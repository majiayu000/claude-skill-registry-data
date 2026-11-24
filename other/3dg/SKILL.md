---
name: 3dg
description: Start the 3d-generalist skill from a slash command, with an optional mode first and then the subject, for example "/3dg cutaway muddy puddle to village well" or "/3dg story porta-potty in a windstorm". With no request it shows the menu of modes.
argument-hint: "[cutaway|story|world|character|asset] <subject>"
disable-model-invocation: true
---

# 3dg

The user started `3dg` (`3d-generalist`) with this request:

$ARGUMENTS

In tools that do not fill in the line above, the request is the rest of the user's message.

1. If the request is empty or is `help`, show the menu below as it is, then ask one question: what 3D content do you
   want to build? Stop there.
2. Otherwise load the `3d-generalist` skill (`../3d-generalist/SKILL.md`) and follow it from the start.
3. Read the request from the left: if the first word matches a mode (`cutaway`, `story`, `world`, `character`, `asset`),
   use that mode and drop the word from the subject. Otherwise pick the mode from the subject.
4. Before building, run the intent brief from that skill (`references/intent-brief.md`). A mode and a subject do not say the purpose, format or look: ask about whichever of those the request leaves open, with options and a recommended default, in one round.

## Menu

| Mode | What it builds | Example |
|---|---|---|
| `cutaway` | 60 s perspective cutaway Short built problem by problem (`But <failure> -> So <fix>`) | `/3dg cutaway how a muddy puddle becomes a village well` |
| `story` | Character-driven 3D storytelling Short with kitbashed set, facial expressions and slapstick timing | `/3dg story a man inside a porta-potty in a windstorm` |
| `world` | Rich 3D environment or diorama with scanned PBR textures, grass, water, fire and ambient motion | `/3dg world 14th-century English grain windmill valley` |
| `character` | Rigged 3D character (realistic worker, HumanGen or retro low-poly) with grounded IK clips | `/3dg character a worker shoveling snow and carrying blocks` |
| `asset` | Hero 3D model, kitbashed prop or reference-matched PBR material exported to GLB | `/3dg asset weathered stone well curb with wooden winch` |
