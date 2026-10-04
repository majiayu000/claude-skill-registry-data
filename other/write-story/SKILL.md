---
name: write-story
description: Write the complete prose story from approved brief, canon, architecture, beat sheet, and scene outline while preserving causality, character voice, and concrete human prose.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Write Story

## Workflow

1. Read core contract, style rules, brief, story bible, characters, world, beat sheet, and scene outline.
2. Draft scene by scene in outline order unless a deliberate nonlinear design is already approved.
3. Keep point of view stable within each scene.
4. Render conflict through action, perception, dialogue, choice, and consequence.
5. Do not explain the story's own theme to the reader.
6. Save `01_story/story.md`.
7. Run `story-state` after each settled scene batch when chronology, character knowledge, props, questions, promises, or life state changed.
8. Run `../../scripts/check_style.py` on the file.

## Done

The story reaches the planned ending, all scene turns are present, `story_state.json` matches mutable narrative facts when used, no canon facts drift, and the prose passes the style check.
