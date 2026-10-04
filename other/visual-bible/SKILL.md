---
name: visual-bible
description: Define and maintain a film or story project's visual language, moodboard briefs, palette, contrast, lighting logic, texture, composition, camera behavior, location treatment, costume treatment, and recurring motifs.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Visual Bible

## Workflow

1. Read the standalone contract, core contract, brief, canon, world bible, screenplay or story scope, director book if present, and approved visual references.
2. Write or update `03_preproduction/visual_bible.md`.
3. Define only production-useful rules: aspect intent, palette roles, contrast range, saturation behavior, texture, material emphasis, lighting logic, camera behavior, capture behavior, composition tendencies, environment treatment, costume treatment, recurring motifs, and visual change across the story.
4. When the story spans visually distinct eras or periods, define an `Era / Period Treatments` section with palette, light, material, environment, wardrobe, and capture behavior for each applicable period. World facts remain in `world.md`; this file owns depiction.
5. Distinguish global rules from scene or sequence exceptions. Describe visible capture behavior instead of inventing camera brands or hardware.
6. Write `03_preproduction/references/moodboard_briefs.jsonl` when moodboard images are useful. Give each frame a job such as palette, material, lighting, composition, architecture, wardrobe, or texture.
7. Use `reference-assets` to assign stable reference roles to approved moodboard or style images.
8. Do not use vague taste words when a visible property can be specified.

## Done

A separate artist, director, or generation agent can reproduce the intended visual language without relying on named-film imitation or chat context.
