---
name: save-plan
description: After generating a plan for the user, use this skill to save the plan to the project.
---

# Save Plan

Claude will generate a plan and save it to the user's `~/.claude/plans/` directory with a random name (e.g. `uncommon-plaited-fruitfly.md`).

Save the generated plan to the current project's `.claude/plans/` directory. Give the plan a meaningful, succinct name based on the task (e.g. `graph-rag-visualization.md`).

Claude should copy the plan from `~/.claude/plans/` and rename the file.

```bash
cp ~/.claude/plans/random-generated-filename.md .claude/plans/meaningful-filename.md
```

## Why use this skill?

Saving the plan in the project directory allows for easy retrieval and reference in future sessions. It helps maintain organization and ensures that plans are contextually linked to the relevant project.

Copy and rename is used because this is a faster operation and less error-prone than rewriting the file from scratch, especially for longer plans.
