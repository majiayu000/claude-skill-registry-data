---
name: new-task
description: Turn an idea, backlog draft, or feature slice into a refined public task spec under docs/tasks/ with a per-milestone ID. Use for /new-task or when the owner wants something made buildable.
argument-hint: "[idea, backlog item, or feature id]"
---

# /new-task: write a task spec

1. **Find the source:** the argument, an inbox/backlog item (private notes), or a feature spec `docs/product/features/F-xx`. Read the linked requirements, ADRs, and `docs/roadmap.md`.
2. **Clarify with the owner** (AskUserQuestion: options + recommendation) whatever is ambiguous: scope, milestone, acceptance criteria, UX choices. Never fill gaps with silent assumptions.
3. **Pick the ID:** the next free `M<milestone>-NNN` from `docs/tasks/README.md`.
4. **Write** `docs/tasks/M?-NNN-<short-name>.md` from `docs/tasks/_template.md`:
   - small enough for one session
   - testable acceptance criteria
   - a test plan
   - the third-party load section
5. **Update** the board in `docs/tasks/README.md`. Mark the source as `→ promoted to M?-NNN` in the private inbox/backlog.
6. Summarize and stop. Don't commit.
