---
name: krea-2
description: Adapt still-image briefs for Krea 2, using exploratory prompting for open visual search and locked prompting plus style references for production-consistent look development.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Krea 2 Prompting

Krea 2 is useful when style and aesthetic exploration are part of the task.

## Modes

### Explore

Use when the user wants possibilities. Start from a short concrete subject or scene plus only the essential constraint. Let the first batch explore style space. On later passes, add the selected style direction and production facts.

### Lock

Use when continuity matters. Write a compact but specific description of subject, composition, environment, lighting, material, palette, and selected style. Name style or moodboard references and their intended influence.

## Workflow

1. Read image brief and canon.
2. Choose `explore` or `lock` from the brief intent.
3. Keep subject and action clear before style language.
4. In lock mode, preserve the exact recurring character and environment identifiers used elsewhere.
5. Use reference images for style instead of trying to encode every stylistic property as adjectives when references exist.
6. Save under `04_generation/prompts/krea-2/<source-id>.md`.

## Done

Explore mode leaves room for deliberate variation. Lock mode removes accidental variation in facts the project already decided.
