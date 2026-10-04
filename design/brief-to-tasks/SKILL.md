---
name: brief-to-tasks
description: "Break a design brief into executable time-boxed tasks, each with a done-when line. Use immediately before a build session."
---

You are breaking a design brief into executable work. Vague tasks produce vague output. Every task here must be completable by one person in one focused session.

Start by reading the design brief and the information architecture document if they exist. If neither exists, ask the user to complete `/design-brief` and `/information-architecture` first. Tasks cannot be accurate without this foundation.

Produce a task list with these four phases:

**Phase 1: Foundation**
Tasks that must happen before screens can be built. Includes: design tokens (if not done), setting up the file structure, confirming the component library, documenting any existing patterns being reused.

**Phase 2: Structure**
IA and wireframe tasks. Each screen in the inventory gets a wireframe task. Navigation flows get their own task. These are low-fidelity; the goal is structure, not polish.

**Phase 3: Build**
High-fidelity screen and component tasks. One task per major screen or component. Include variant tasks separately (error state, empty state, responsive layout).

**Phase 4: Review**
Critique, accessibility check, edge case review. These are not optional phases; list them as real tasks with time estimates.

For each task, include:
- A clear title starting with a verb (Design, Write, Build, Review, Define)
- A "done when" definition: the specific condition that marks this task complete
- Dependencies: which prior tasks must be complete before this one starts

Format as a markdown checklist. Show dependencies inline as "(requires: Task X)". Order tasks within each phase by dependency, not by importance. A task with no dependencies can run in parallel with others; call that out explicitly.
