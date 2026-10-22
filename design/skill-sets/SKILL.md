---
name: skill-sets
description: Select and coordinate reusable skill sets from the Innovator skills collection for cross-cutting engineering tasks.
---

# Skill Sets Router

Use this entry point when a task spans multiple engineering domains or would benefit from a coordinated set of reusable workflows rather than one isolated skill.

## Reference-driven engineering skill set

Start with the [Reference-Driven Engineering Skill Set](README.md) for tasks involving frontend/UI/UX, multi-application architecture, source inspection, testing, or reverse engineering. It coordinates these focused skills:

- [Reference-driven engineering](../reference-driven-engineering/SKILL.md) — repository-first planning, source inspection, safe changes, verification, and evidence-backed reporting.
- [ArtCraft-inspired frontend UX](../artcraft-frontend-ux/SKILL.md) — editor layouts, reusable components, canvas interactions, responsive design, and accessibility.
- [Multi-application architecture](../multi-application-architecture/SKILL.md) — app discovery, navigation contracts, shared infrastructure, and boundaries.
- [Evidence-driven reverse engineering](../evidence-driven-reverse-engineering/SKILL.md) — authorized behavior investigation with explicit observations, inferences, and unknowns.
- [Reverse-engineering tool selection](../reverse-engineering-tool-selection/SKILL.md) — task-based selection and verification of appropriate tools.

## How to route

1. Identify the concrete output and target repository.
2. Use the narrowest specialist skill that fits. Add the reference-driven router for tasks with several stages or competing considerations.
3. Inspect the target repository and relevant upstream documentation before adopting patterns.
4. Verify the output through tests, builds, accessibility/responsive checks, or controlled experiments according to the task.
5. Report actual evidence and unresolved limitations. Do not claim unrun checks or uninspected source.

The upstream repositories are references, not required dependencies. Adapt their ideas to the target stack and do not copy their implementation without an explicit need.
