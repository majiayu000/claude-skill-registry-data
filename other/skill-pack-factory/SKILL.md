---
name: skill-pack-factory
description: >
  Create non-overlapping Codex skills or a local plugin from repos, workflows,
  PDFs, APIs, or repeated tasks. Use when the user asks to make many skills,
  convert GitHub learnings into skills, build a skill catalog, or package a
  workflow into reusable Codex instructions.
---

# Skill Pack Factory

Make fewer, sharper skills. Use references for breadth.

## Creation Flow

1. Cluster source material into workflow patterns.
2. For multiple local source clones, run
   `$auto-skill-build-source-pattern-synthesis` before creating skill files.
3. Remove duplicates and generic advice.
4. For each skill, define one job and skip conditions.
5. Keep `SKILL.md` short; move examples and catalogs to references.
6. Add scripts only for repeated deterministic mechanics.
7. Validate with `$skill-quality-gate`.

When source material is an external skill pack, slash-command pack, hook plugin,
or upstream prompt catalogue, run `$auto-skill-safety-external-skill-intake`
before creating or installing local skills from it.

## Candidate Skill Card

```md
Name:
Trigger:
Inputs:
Workflow:
Tools:
References:
Skip when:
Validation:
```

## Quality Bar

A skill is worth creating only if it changes Codex behavior in one of these ways:

- chooses better files/tools
- prevents a risky action
- saves repeated tokens
- preserves durable project knowledge
- turns a domain workflow into a checklist
- makes validation more reliable

Read `references/skill-patterns.md` before generating large batches.

## Validation

- Each skill has one job, trigger language, skip conditions, and validation.
- Long catalogs/examples live in references, not `SKILL.md`.
- Run `$skill-quality-gate` before installing or relying on the pack.
