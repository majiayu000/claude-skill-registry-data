---
name: phxstack-plan
description: Write a concise local implementation spec with non-goals. Use when a task is clear but unplanned, or after phxstack-nail confirms the task.
---

# phxstack-plan

Write a local spec that survives the session. Do not implement it.

1. Inspect the relevant code and `LEARNED.md` when present.
2. Choose a short kebab-case slug and write
   `.phxstack/specs/<slug>.md`.
3. Include exactly these sections:

```markdown
## What we're doing

## Steps

## What we're NOT doing

## How we'll know it works
```

Keep it to one page. Each step must be independently implementable and
verifiable. Name concrete commands or observable behaviour in the final
section.

Show the completed spec and stop for developer approval. Specs stay local;
publish a named spec to GitHub only after the developer explicitly gives the
green light.
