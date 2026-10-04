---
name: write-book
description: Draft a novel, novella, or narrative book chapter by chapter from an approved book plan, maintaining POV, character voice, causality, continuity, and a compact running chapter-state record.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Write Book

## Workflow

1. Read core contract, style rules, book plan, canon, and the immediately relevant prior chapter state.
2. Draft one `CH-###` at a time under `01_story/chapters/CH-###.md`.
3. After the chapter, update `01_story/chapter_state.json` with a compact navigation summary, then run `story-state` for durable changes to location, injuries, possessions, character knowledge, relationships, questions, promises/payoffs, prop state, life state, and chronology.
4. Before the next chapter, re-read its plan entry plus the saved state. Do not reread the entire manuscript unless a revision or continuity problem requires it.
5. Use summaries only for navigation. Treat the actual chapter text and canon as authority when wording or facts matter.
6. Run the style checker on every completed chapter.

## Done

Every planned chapter exists through the ending, chapter state and `story_state.json` match the manuscript, and no chapter depends on unsaved conversational memory.
