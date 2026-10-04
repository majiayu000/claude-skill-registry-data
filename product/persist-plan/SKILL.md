---
name: persist-plan
description: Persist an internal plan to docs/product/plans/. Use when exiting plan mode, when the user says "save the plan", or when you notice a plan exists in .claude/plans/ that hasn't been copied to docs/product/plans/ yet.
user-invocable: true
---

# Persist Plan

Save the current plan from `.claude/plans/` to the project's permanent docs folder.

## When to Use

- After exiting plan mode (ExitPlanMode)
- When the user says "save the plan" or "persist the plan"
- When you notice a plan in `.claude/plans/` that doesn't have a corresponding file in `docs/product/plans/`

## Steps

1. **Find the plan file.** Check the context for a plan file path (usually mentioned in system messages like "A plan file exists from plan mode at: ..."). If not found, glob `.claude/plans/*.md` and pick the most recently modified.

2. **Determine the filename.** Use this priority:
   - If there's a Linear ticket (e.g., `BIK-12`), use: `<ticket-id>-<slug>.md` (e.g., `bik-12-feature-plan.md`)
   - If there's a sprint number, use: `sprint-<N>-plan.md`
   - Otherwise, ask the user what to name it

3. **Copy to docs.** Write the plan content to `docs/product/plans/<filename>`. If the file already exists, ask before overwriting.

4. **Commit** the plan file with message: `docs: persist plan for [ticket-id or context]`

5. **Confirm.** Tell the user where the plan was saved.

## Notes

- Plans in `.claude/plans/` are ephemeral (internal to Claude Code sessions)
- Plans in `docs/product/plans/` are permanent and version-controlled
