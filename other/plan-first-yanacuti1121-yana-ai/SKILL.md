---
name: plan-first
description: "Use before touching any code when user gives a task, spec, or feature request. Forces writing a plan before implementation. Examples: 'implement X', 'add feature Y', 'fix Z and also update A', any multi-step task that would touch 2+ files."
---

# Plan First Skill

Before writing code, write a plan. This exists to stop the pattern of AI jumping
straight into editing files without understanding what should and should not change.

## When to use this skill

- User describes a feature, task, or fix that touches 2+ files
- Task has unclear scope — what NOT to change is as important as what to change
- Agent is about to run a bash command that modifies files without a written plan
- User says "implement", "add", "refactor", "migrate", "update"

Do NOT use for: single-file typo fixes, running a specific command the user named,
answering a question.

## Workflow

### Step 1 — Write the plan (before any file edits)

Output a plan with this structure:

```markdown
## Plan: [task name]

**Goal:** [one sentence — what this achieves when done]

**Files to change:**
- `path/to/file.ts` — [why it changes]
- `path/to/other.ts` — [why it changes]

**Files NOT to touch:**
- `app/` — product code, out of YAMTAM scope
- [any other explicit boundary]

**Steps:**
1. [concrete action]
2. [concrete action]
3. ...

**Verify after:**
- [command to run that proves it worked]
- [expected output]

**Risks:**
- [anything that could go wrong or needs human decision]
```

### Step 2 — Wait for approval

Do not proceed to code until the user confirms or modifies the plan.
If user says "go" or "ok" or "looks good" — proceed to Step 3.
If user modifies the plan — update it, confirm, then proceed.

### Step 3 — Execute step by step

Work through the plan steps in order.
After each step: show what changed (`git diff --stat` or file path).
Do not bundle multiple steps into one edit.

### Step 4 — Verify

Run the verify commands from the plan.
Show actual output — do not summarise.
Only claim done after output confirms it.

## Constraints

- Never edit files before the plan is written and approved.
- Never expand scope mid-task without writing a plan amendment.
- If a step reveals unexpected complexity, stop and update the plan.
- "I'll plan as I go" is not a plan.
