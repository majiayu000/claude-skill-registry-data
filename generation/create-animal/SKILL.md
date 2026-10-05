---
name: create-animal
description: Generate one specified real species or original animal creature in an anatomically and ecologically coherent scene. Use for standalone animal creation from a brief; do not use for a portrait of the user's supplied pet, a humanoid character, an NPC, or animating an existing animal image.
---
# Create Animal

## Catalog

- Display name: Create Animal
- Categories: Character
- Status: Ready
- Route label: Z-Image photorealistic animal generation
- Tone: green
- Short description: Generate one specified real or original animal in an anatomically and ecologically coherent scene.
## What this skill does

- Creates a real species, plausible hybrid or original animal from a concrete description.
- Matches anatomy, habitat, behavior, lens and lighting instead of relying on a random-animal prompt.

## How to use

Specify species or original anatomy, age, behavior, habitat, realism, framing and mood.

#### Example

```text
Create one red panda crossing a mossy branch after rain; candid wildlife photography, accurate paws and tail, 3:2.
```

## Workflow

1. Resolve real species versus fictional creature and gather anatomy and habitat constraints.
2. Write one observable action and camera plan; forbid duplicate limbs or mixed traits.
3. Generate directly with Z-Image for a pure photorealistic text-to-image animal brief. Use GPT Image 2 Medium instead when readable text, controlled layout, or non-photographic general image work becomes a hard requirement. Never treat `random-animal-generator` as a model.
4. Verify limb count, joints, eyes, fur or scales, habitat plausibility and subject count.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One animal image
- Default quantity: 1
- Content per image: One animal or coherent group in a plausible scene
- Default layout: User-requested or source-preserving format
- Model policy: Z-Image by default for pure photorealistic text-to-image; GPT Image 2 Medium only when its documented hard constraints apply
- Downstream use: Wildlife visuals and original creature concepts
