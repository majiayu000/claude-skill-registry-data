---
name: memory
description: "Manage the persistent memory layer in .claude/memory/ — list, search, save, update, delete, dedupe. Use to inspect what memories exist, write a new one, or clean up stale entries."
argument-hint: "[list | search <query> | save | delete <name> | dedupe]"
---

# /memory

Operate on `.claude/memory/`. Memory persists across sessions and is shared across all 12 toolkit agents.

## Subcommands

### `list` (default)

Print the current memory index, grouped by type. One line per entry: name, description, last-verified date.

```
## Project (4)
- monorepo-layout — apps/, packages/, infra/. Yarn workspaces. (2026-04-18)
- billing-flag-state — webhook still off in prod, on in staging. (2026-05-01)
- migration-plan-q3 — auth migration to Lucia, target 2026-07-01. (2026-04-30)
…

## User (2)
- role — senior eng, owns the platform team. (2026-04-15)
- preferences — terse responses; no emojis; vitest over jest. (2026-04-15)

## Feedback (1)
- no-mocks-in-integration — integration tests must hit real DB. (2026-04-22)

## Reference (1)
- linear-eng-board — pipeline bugs tracked in Linear project ENG. (2026-04-15)

## Inherited (0)
## Handoffs (3)
- 2026-05-01 — auth migration shipped; billing flag pending.
- 2026-04-30 — design system v2 RFC opened.
- 2026-04-29 — initial repo onboarding.
```

### `search <query>`

Find memories whose name, description, or body matches the query. Use to remind yourself of context before answering a related question.

### `save`

Walk through writing a new memory:

1. Ask which type: project / user / feedback / reference.
2. Ask for the title (slug becomes the filename).
3. Ask for the description (one line — used for relevance scoring later).
4. Ask for the body. For `project/` and `feedback/`, prompt for **Why:** and **How to apply:** explicitly.
5. Show the file you're about to write. Get confirmation.
6. Write the file.
7. Update `.claude/memory/MEMORY.md` index.

Frontmatter:

```markdown
---
name: <title>
type: project | user | feedback | reference
description: <one-line>
created: 2026-05-02
last-verified: 2026-05-02
---

<body>
```

### `update <name>`

Find the memory by name. Show its current contents. Ask what to change. Update the file and bump `last-verified`.

### `delete <name>`

Find the memory. Show what would be deleted. Ask for confirmation. Delete the file and remove the line from `MEMORY.md`.

### `dedupe`

Scan memories within each type for likely duplicates (same topic phrased differently). Surface candidates. Never auto-merge — always show pairs and ask which to keep.

## Behavioral rules (enforced by the auto-loaded `memory-discipline` rule)

- Never write a memory the user didn't volunteer.
- Always update over add when the topic overlaps.
- Always convert relative dates to absolute.
- Never put secrets, API keys, tokens, or PII into memory.
- Always update the `MEMORY.md` index when adding/removing.

## Output format

For `list`, render the grouped index above. For `search`, show matching memories with their full body. For `save` / `update` / `delete`, show before/after diffs and confirm before writing.
