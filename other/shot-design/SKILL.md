---
name: shot-design
description: Design motivated shots from a screenplay scene and director book, giving every shot a purpose, framing, camera behavior, action, continuity state, duration, and sound plan.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Shot Design

## Workflow

1. Read core contract, `VISIBLE_DIALOGUE_SYNC.md`, dramaturgy rules, film grammar, prompt packet schema, screenplay scene, line manifest, breakdown, director book, continuity, production capabilities when present, performance blocking when present, and approved reference manifest.
2. Assign stable `SHOT-###` IDs within the project sequence.
3. Design the minimum coverage needed for the intended cut.
4. Write one model-neutral JSON object per shot to `04_generation/shot_briefs.jsonl`.
5. Each shot must include `line_ids` for the source production units it covers when a line manifest exists, plus purpose, dramatic job, beat, scene ID, duration, subjects, location, continuity, framing, composition, camera, movement reason, eye trace, action, environmental pressure, micro-action, anchor, lighting, dialogue, ambience, music, SFX, references, cut intent, and constraints.
6. Resolve applicable visual-bible capture behavior into `capture_behavior` without inventing camera hardware.
7. When the viewer must see a character speak an exact screenplay line, add the model-neutral `lip_sync` record with exact `LINE-###`, speaker, visibility, cut policy, and measured timing when available. Do not force lip sync onto off-screen dialogue. When approved audio exists, preserve its `MEDIA-###`, SHA-256 authority, and start time and run dialogue timing preflight before expensive generation.
8. Add `end_frame` only when chained generation, match on action, last-frame conditioning, or editorial continuity needs an explicit final state. When motion state also matters, add a temporal-continuity handoff that uses the approved previous shot and a visual-only tail; do not import prior-shot audio.
9. Add optional `frame_regions` only when multi-subject screen placement needs explicit control or the downstream route supports regional conditioning. Use semantic zones unless normalized bounds were deliberately planned.
10. Check screen direction, eyelines, eye trace, and geography across adjacent shots.
11. If the requested camera/action combination is unavailable or conditional in `production_capabilities.json`, redesign, split, or mark the blocker rather than pretending it is executable.
12. Delete shots that do not change a relationship or emotion, advance action or information, increase pressure, or satisfy an explicit practical coverage need.

## Done

Every shot earns its place in the edit and can be generated independently from its saved brief.
