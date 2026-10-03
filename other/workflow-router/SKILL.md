---
name: workflow-router
description: Use when a request mentions a workflow, bug, project edit, continuation, phase change, or unclear workflow action in this repo.
---

# Workflow Router

This is the canonical workflow entry skill for this repo.

## Required Flow

1. Read `AGENTS.md`, `CONTEXT.md`, and `skills/control-repo-manager/SKILL.md`.
2. Identify the active project lane from the user's words and tracker status.
3. Route to exactly one next skill:
   - `skills/workflow-intake/SKILL.md` for new, continued, edited, or buggy
     workflow requests.
   - `skills/workflow-grilling/SKILL.md` when context is loaded and the next
     action is a question.
   - `skills/workflow-to-prd/SKILL.md`, `skills/workflow-to-issues/SKILL.md`,
     `skills/workflow-implement/SKILL.md`, or
     `skills/workflow-code-review/SKILL.md` only when the user explicitly asks
     to move to that phase.
4. Do not implement from the router.

## Hard Stops

- If tracker state is missing, use workflow intake.
- If the Matt Pocock phase skill has not been loaded, stop and load it.
- If the user asks "what can I do", use `skills/workflow-help/SKILL.md`.
