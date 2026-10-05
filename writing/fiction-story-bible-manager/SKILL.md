---
name: fiction-story-bible-manager
description: Build and maintain a story bible for complex fiction. Use when the user needs to remember characters, terms, locations, world rules, canon, timelines, scene history, relationship changes, plot threads, foreshadowing, payoffs, continuity issues, or revision queues while writing a novel or series.
---

# Fiction Story Bible Manager

## Workflow

Use explicit project documents instead of chat memory. The story bible is the source of truth for canon, terms, characters, locations, timelines, scenes, plot threads, setup/payoff, world rules, relationships, style, continuity issues, and revision queue.

Read:

- `references/story-bible-operations.md` before creating or updating a story bible
- `references/continuity-checks.md` before checking drafted material
- `references/setup-payoff-ledger.md` when handling clues, foreshadowing, red herrings, twists, and payoffs

Use `assets/story-bible-template/` as the copy source for new projects.

## State Rules

- Use `canon` only for established manuscript facts or explicit writer decisions.
- Use `proposed` for candidate ideas.
- Use `uncertain` for implied but unconfirmed facts.
- Use `retconned` for replaced canon.
- Use `cut` for removed material.
- Never silently overwrite canon; record continuity impact and revision needs.

## Update Loop

1. Before drafting, read `00-index.md`, `canon-ledger.md`, and relevant character, timeline, scene, plot, and setup/payoff files.
2. During drafting, mark new entities, rules, clues, relationship shifts, and important phrases.
3. After drafting, produce update candidates for each affected bible file.
4. Check for unsupported payoff, orphan setup, timeline contradiction, knowledge-state contradiction, voice drift, term drift, and world-rule contradiction.
5. Add required manuscript changes to `revision-queue.md`.

## Output Contract

End with the relevant subset:

```markdown
## Story Bible Index
## Canon Ledger
## Entity Update Log
## Timeline Update
## Scene Ledger Update
## Setup-Payoff Ledger
## Continuity Issue Report
## Revision Queue
```
