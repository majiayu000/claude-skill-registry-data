---
name: track-change
description: After making any meaningful change, propagate it to the right vault notes and auto-memory. Use whenever you ship something — feature, fix, refactor, decision — so the knowledge base stays in sync without the user having to ask.
---

# track-change

This is the **automatic memory update** glue. It's the difference between a vault that decays and one that stays useful. Run this after any non-trivial change, *before* moving to the next task.

## When to use

After any of these:

- A new feature lands → update `Features/`
- A new endpoint added → update `Architecture/API Routes.md`
- A new model added → update `Architecture/Database Schema.md`
- A pattern changed → update relevant `Features/` or create an ADR
- A bug was fixed where the cause was non-obvious → save a feedback memory
- The user gave guidance ("always do X") → save a feedback memory
- The user shared context ("we're freezing merges Thursday") → save a project memory

## Steps

1. **Decide what kind of change this is** (feature / endpoint / model / pattern / bug / decision / guidance / context).
2. **Find the relevant vault notes** by listing `Aqarkom_Knowledge/Architecture/`, `Features/`, `Decisions/`. Don't create duplicates — update existing notes when possible.
3. **Read the target note** before editing.
4. **Edit** with a focused change — add a new bullet, update a table row, append a "Recent additions" line. Don't rewrite the whole file.
5. **Cross-link** — if the change touches multiple areas, add `[[wikilinks]]` so they're discoverable from each other.
6. **Auto-memory**: decide if this change deserves a memory entry. Use the rules from the `auto memory` system prompt:
   - **feedback** if the user corrected behavior or validated an unusual choice
   - **project** if you learned about goals, deadlines, or context
   - **reference** if you learned where info lives in an external system
   - **user** if you learned about the user's role or expertise
   - Skip if it's just code state (the code is the source of truth)
7. **Update MEMORY.md index** if you added a new memory file.

## Verification

- [ ] At least one vault note updated, OR a deliberate decision made not to (with reason)
- [ ] Memory entry added if guidance/context was learned
- [ ] No duplicate notes created
- [ ] Cross-links present where helpful

## Anti-patterns

- Don't dump the diff into the vault note — summarize the *intent*
- Don't save memories for things derivable from `git log` or current code
- Don't create a new note if an existing one already covers the topic
