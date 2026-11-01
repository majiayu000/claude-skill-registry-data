---
name: start-task
description: Implement one Pieceful task spec end to end (read context, build, test, review, Definition of Done) and stop for the owner's review. Use for /start-task <id>.
argument-hint: "<task id, e.g. M1-001>"
disable-model-invocation: true
---

# /start-task: build a task

1. **Load context:** `AGENTS.md`, the task file `docs/tasks/<id>-*.md`, and only the docs/ADRs/feature specs it links. Check that its dependencies are `done`. If not, stop and say so.
2. **Confirm the plan:** restate the goal, scope, and approach in a few lines. If anything in the spec is ambiguous or needs a design decision, **ask the owner first**. A real decision gets an ADR (`/adr`).
3. **Set the status** to `in-progress` (task file + board).
4. **Implement** within scope only. Put unrelated findings in the inbox (`/idea`), not in the diff.
5. **Test:** add or adjust tests per the test plan, and run the test, lint, and type commands from `AGENTS.md`.
6. **Review:** run the `design-reviewer` agent on the change and fix what it finds (or explain why not).
7. **Definition of Done:** go through `docs/process/definition-of-done.md`, updating docs and specs as needed.
8. **Set the status** to `review`. Give a summary: what changed, how it was tested, anything left open.
9. **Stop.** Don't commit or push. The owner reviews first. Offer `/handoff`.
