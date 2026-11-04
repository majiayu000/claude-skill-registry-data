---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

Create or update skills using progressive disclosure. Keep this file focused on the workflow and load references only when needed.

## Workflow

Follow these steps in order unless there is a clear reason to skip one:

1. Understand the skill with concrete examples.
2. Identify which reusable resources belong in `scripts/`, `references/`, or `assets/`.
3. Initialize the skill if it does not already exist.
4. Edit the skill contents and bundled resources.
5. Package and validate the skill.
6. Iterate based on real usage.

## Read These References As Needed

- `references/principles.md`: skill anatomy, frontmatter rules, what belongs in resources, and what not to include
- `references/progressive-disclosure.md`: how to split a large skill into a lean `SKILL.md` plus targeted references
- `references/process.md`: step-by-step guidance for understanding, initializing, editing, packaging, and iterating

## Working Rules

- Keep `SKILL.md` lean and procedural. Move detailed examples, variant-specific material, and large reference content into `references/`.
- Prefer scripts when the same code would otherwise be rewritten repeatedly or when deterministic behavior matters.
- Do not create extra documentation files like `README.md` or `CHANGELOG.md` inside a skill.
- When editing an existing skill, preserve the resource layout if it already reflects clear progressive disclosure.
