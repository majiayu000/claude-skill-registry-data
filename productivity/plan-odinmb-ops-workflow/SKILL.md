---
name: plan
description: Create an ops work plan for a new task. Proposes steps and success criteria for user approval before execution.
argument-hint: <brief task description>
allowed-tools: Read, Glob, Grep, Write, Bash(ls *), Bash(mv *)
---

Create a work plan for the following task: $ARGUMENTS

## Instructions

1. **Research first.** Read `MEMORY.md`, `backlog/INDEX.md`, and any relevant `state/` or `references/` files to understand current state and prior work. Check `plans/completed/` for related past tasks. Check `backlog/` for an existing draft plan that matches this task.

2. **Create or activate the plan file.** If a draft plan exists in `backlog/`, move it to `plans/`, update its date to today, and set status to `active`. Refine the plan based on your research. If no draft exists, write a new file at `plans/YYYY-MM-DD-<slug>.md` where the slug is a short kebab-case name derived from the task. Use today's date. Use this format:

```markdown
# Task: <Descriptive Name>

- **Date**: YYYY-MM-DD
- **Status**: active

## Objective
What we're trying to accomplish and why. Be specific.

## Plan
1. Step one
2. Step two
3. ...

**Artifacts:** Where deliverables will be stored (e.g. `artifacts/`, `artifacts/<subfolder>/`).

**Files to create/modify:** List every file and folder expected to be created, moved, or significantly changed — including which `INDEX.md` files will need updating.

**Success criteria:**
- [ ] Criterion A
- [ ] Criterion B
```

Leave the sections below the plan blank — they get filled in during and after execution:

```markdown
## Outcome
_Fill in when completed._

## Key Decisions
_Fill in when completed._

## Artifacts
_Fill in when completed._

## Session Log
_Fill in when completed._
```

3. **Present and clarify.** Assume the user hasn't read the research and doesn't know this corner of the project. One or two sentences each: what the situation is, what the work will produce, and what it deliberately won't cover. No numbered walkthrough of the steps and no success-criteria checklist — those stay in the plan file for the executor.

   Then surface the scope decisions, trade-offs, and assumptions that genuinely need the user. Use the **AskUserQuestion** tool with concrete options — don't ask open-ended questions when specific choices are available, and make every option differ in something the user can judge without opening a file: what the deliverable achieves, who it's for, what it costs, what it rules out later. Group related decisions (up to 4 per question).

   Decide artifact placement yourself using the Whole-File Test in `CLAUDE.md` and state where things will land in a clause — never ask which folder. Skip clarification if the task is absolutely straightforward. Update the plan file with the user's answers. Wait for approval before any work begins.

4. **Do NOT execute the plan.** This skill only creates and proposes the plan. Execution happens via the `/execute` skill after the user approves.

5. **Scope check.** Plans in non-code repos must never include implementing code changes. This workflow produces content, research, specs, and briefs — not code. If a task involves building something in an app, the plan should cover producing the content/spec/brief that the user takes to the coding repo.
