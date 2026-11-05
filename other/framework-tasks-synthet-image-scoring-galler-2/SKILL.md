---
name: framework-tasks
description: "Explicit framework workflow: tasks"
disable-model-invocation: true
---

# /tasks — Generate implementation tasks from a plan

Use after `/spec` and `/plan` are approved, before `/implement`. This Spec Kit-inspired gate turns a product spec and technical plan into a traceable, ordered task list that another developer or coding agent can execute without reinterpreting requirements.

## Inputs

- Approved spec with stable `AC-n` acceptance criteria.
- Approved implementation plan.
- Relevant backlog item, issue, or project-tracking reference, when available.

## Output

Create an implementation task list with:

1. **Traceability matrix** — Map every `AC-n` to one or more task IDs and planned verification commands.
2. **Task table** — Numbered `T-n` tasks with:
   - owner role or agent role,
   - files / areas to touch,
   - dependency IDs,
   - exact acceptance criteria covered,
   - verification command or evidence.
3. **Execution order** — Group tasks into setup, test-first scaffolding, implementation, integration, validation, and documentation.
4. **Parallelization notes** — Identify tasks that can run concurrently and tasks that must stay serialized.
5. **Definition of done** — Checks that must be green before `/pr-ready`.

## Task quality rules

- Every `AC-n` from the spec must appear in the traceability matrix.
- Every implementation task must name at least one concrete file/path area or explain why discovery is required.
- Test or validation tasks must precede implementation tasks for the same behavior whenever feasible.
- Do not create vague tasks such as "improve UI" or "handle edge cases"; rewrite them as observable work.
- If a task would broaden scope beyond the spec, move it to **Out-of-scope follow-up**.

## Done when

- Another developer can execute the task list in order without guessing.
- No acceptance criterion is orphaned.
- Verification commands or evidence are listed for every acceptance criterion.
