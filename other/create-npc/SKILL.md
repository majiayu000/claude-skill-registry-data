---
name: create-npc
description: Create one original non-player character image whose occupation, faction, world function, and gameplay role are visually legible. Use for game-ready NPC concepts tied to a setting and role; do not use for generic standalone characters, multi-view reference sheets, player avatars, or portraits of real people.
---
# Create NPC

## Catalog

- Display name: Create NPC
- Categories: Character
- Status: Ready
- Route label: GPT Image 2 game-character concept
- Tone: violet
- Short description: Create one original non-player character image whose occupation, faction and gameplay role are visually legible.
- Similar skills: casting, create-character
## What this skill does

- Translates gameplay function, world, faction and personality into one NPC concept.
- Keeps the character original and separates visual storytelling from a full character-sheet workflow.

## How to use

Provide game genre, NPC role, faction, personality, equipment, environment and art direction.

#### Example

```text
Create one original fantasy harbor quartermaster with weathered clothing, inventory ledger and brass whistle; painterly game concept art.
```

## Workflow

1. Define gameplay function, social role, faction cues and encounter context.
2. Choose one pose and environment that communicate function without a multi-panel sheet.
3. Generate one image with GPT Image 2 Medium.
4. Verify originality, role readability, prop logic, anatomy and one-character count.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One NPC concept image
- Default quantity: 1
- Content per image: One original NPC with role-defining context
- Default layout: User-requested or source-preserving format
- Model policy: GPT Image 2 game-character concept
- Downstream use: Games and interactive fiction
