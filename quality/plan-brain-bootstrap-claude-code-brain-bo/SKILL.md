---
name: plan
description: Plan a non-trivial task before implementing. Use when the task requires 3+ steps, multiple files, or an architectural decision. Writes a checkable plan to claude/tasks/todo.md.
---

# Plan Skill

Create a structured, checkable implementation plan before writing any code.

## When to use
- Task requires 3 or more steps
- Task touches multiple files or layers
- Task involves an architectural decision
- Any time the path forward is not immediately obvious

## Protocol

### 1. Read mandatory context first
- `claude/tasks/todo.md` — current task state (are we resuming?)
- `claude/tasks/lessons.md` — relevant past lessons
- `claude/architecture.md` — project structure
- `claude/rules.md` — golden rules

### 2. Understand the full scope
- What is the exact goal? What does done look like?
- What layers does this touch (schema, service, API, tests, docs)?
- What already exists that is relevant?
- What are the failure modes?

### 3. Write the plan to claude/tasks/todo.md

Format:
```markdown
# Task: <Clear, concise title>

**Goal:** <One sentence. What is done when this is complete?>
**Branch:** <git branch name, if applicable>
**Loaded docs:** <which claude/*.md files you read>

## Steps
- [ ] 1. <First action — specific file or command>
- [ ] 2. <Second action>
- [ ] 3. <Third action>
...

## Review Checklist
- [ ] Tests pass
- [ ] Linter passes
- [ ] No new warnings
- [ ] PR description ready (if applicable)

## Notes
<Any constraints, risks, or decisions to track>
```

### 4. Validate the plan (optional — for complex tasks)
Spawn a plan-challenger subagent:
> "Spawn plan-challenger to review this plan. Here is the plan: [paste plan]"

### 5. Get approval for non-trivial plans
Present the plan to the user. Wait for "proceed" or revisions before implementing.

## Rules
- NEVER start implementing before the plan is written
- NEVER mark a step complete without proof (test result, output, etc.)
- If something goes wrong mid-execution: STOP, re-read the plan, update it, then continue
