---
name: openmontage
description: >-
  OpenMontage entry pack. Use for video pipelines (Rule Zero), HyperFrames runtime,
  and discovering nested craft skills under .agents/skills and .claude/skills.
---

# OpenMontage

## Required first read

1. [`AGENT_GUIDE.md`](AGENT_GUIDE.md) — Rule Zero, pipelines, quality gates  
2. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) — architecture (when producing)

**Do not invent packs.** After this entry, load only the nested `SKILL.md` paths listed on your **position** Skill packs table (or explicitly named in the stage director).

## Nested skill roots

| Root | Typical contents |
|------|------------------|
| `.agents/skills/` | HyperFrames, threejs-*, framer-motion, tailwind, web-design-guidelines, vercel-* |
| `.claude/skills/` | FLUX, BFL, remotion-best-practices, visual-style, duplicate threejs/vercel copies |

Prefer **`.agents/skills/`** for eng/UI threejs and HyperFrames. Prefer **`.claude/skills/`** for FLUX / BFL / remotion-best-practices when both exist.

## Org wiring

Position seats must list concrete nested packs they own. Listing only this entry is enough to enter OpenMontage for video; eng/design seats should list threejs / FLUX / web packs explicitly.
