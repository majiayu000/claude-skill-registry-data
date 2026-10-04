---
name: cineops-shot-planning
description: Convert approved scenes into production-ready shot plans with purpose, blocking, timing, camera intent, continuity states, and sound. Use for shot lists, coverage plans, storyboard briefs, or generation prompts after story logic is approved.
---

# CineOps Shot Planning

## Purpose

Design shots that communicate story changes and can survive handoff to people or generation tools. Do not decorate every beat with camera movement. Give each shot one dominant job.

Read `references/blocking-and-timing.md` before planning complex movement. Use `assets/shot-plan.template.json` for machine-checkable output.

## Confirm Inputs

Require an approved scene or clearly mark the plan as exploratory. Confirm aspect ratio, target duration, existing assets, spatial layout, character entry states, and delivery format. Ask only for unknowns that would materially change blocking or continuity.

## Build The Plan

1. Map the scene's dramatic beats and identify the visual evidence for each beat.
2. Establish geography before relying on eyelines, screen direction, or off-screen action.
3. Assign each shot a unique ID, scene ID, order, purpose, duration, action, camera, characters, props, location, entry state, and exit state.
4. Describe action in observable sequence. Separate simultaneous action only when the frame can read it.
5. Motivate camera movement by revelation, pursuit, concealment, power shift, or attention. Prefer a stable frame when movement adds no story information.
6. Include sound cues that carry timing or off-screen causality.
7. Check that adjacent exit and entry states connect.

## Generation-Aware Rules

- Keep a shot's primary transformation singular and legible.
- Avoid contradictory lens, framing, and motion instructions.
- Name who acts, where they are, and what changes.
- Preserve stable identity and wardrobe references through ledger IDs.
- Split a shot when subject, location, time, or dominant action changes beyond reliable continuity.
- Record unknowns rather than filling them with plausible invention.

## Validate And Handoff

Save the plan as `shot-plan.json` alongside other CineOps artifacts and run:

```bash
cineops validate path/to/project
```

Fix all errors. Review warnings. Then pass the plan to `$cineops-continuity-ledger` if it introduces state changes and to `$cineops-generation-readiness-review` before paid generation.

Do not call a shot ready merely because its prompt sounds cinematic. Readiness depends on continuity, blocking, performance, camera logic, and generation clarity.
