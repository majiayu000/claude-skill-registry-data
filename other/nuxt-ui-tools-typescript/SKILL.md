---
name: nuxt-ui-tools-typescript
description: Use this skill for internal TypeScript work in the nuxt-ui-tools repository. Covers the repository's inference-first style, forbidden escape hatches, public API typing rules, schema-driven type design, and how to keep complex types powerful without making the codebase harder to maintain.
---

# nuxt-ui-tools TypeScript

Use this skill when the task is primarily about:

- schema typing
- public API typing
- inference problems
- builder typing
- unsafe casts or `any`
- complex generic cleanup

## Read First

- `AGENTS.md`
- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`
- `.agents/skills/nuxt-ui-tools-typescript/references/rules.md`
- `.agents/skills/nuxt-ui-tools-typescript/references/public-api.md`
- `.agents/skills/nuxt-ui-tools-typescript/references/jsdoc.md`
- `.agents/skills/nuxt-ui-tools-typescript/references/schema-patterns.md`

## Purpose

This skill exists to keep the repository strongly typed without turning the type system into a second codebase that is hard to evolve.

The goal is:

- strong guarantees
- strong inference
- low duplication
- consumer-friendly API shapes

## Load When Needed

For deeper topic-specific guidance, use:

- `.agents/skills/nuxt-ui-tools-typescript/references/ref-patterns.md`
- `.agents/skills/nuxt-ui-tools-typescript/references/anti-patterns.md`
