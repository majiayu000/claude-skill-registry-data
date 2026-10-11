---
name: brainstorm
description: Shape an unclear feature or design with the user before any plan exists — one question at a time, 2-3 approaches, and a local browser companion for mockups and diagrams. Use when the user says "brainstorm", "explore this idea", "show me options", or asks for something whose intent or design is still open. Skip it when the task is already specified.
---

# Brainstorm

Turn an open idea into an approved design through dialogue. The output is a design
the user approved, handed to `/big-feature` as its task. No code, no plan.

## Steps

1. Read the project context: CLAUDE.md, the relevant files, recent commits.
2. If upcoming questions are visual (layouts, mockups, diagrams), offer the visual
   companion in its own message and wait for the answer:
   > "Some of this is easier to show than describe. I can put mockups and diagrams
   > in a local browser page as we go. It costs extra tokens. Want to try it?"
3. Ask clarifying questions, one per message, multiple choice when possible:
   purpose, constraints, success criterion.
4. If the request spans several independent subsystems, say so first and pick one
   to design.
5. Propose 2-3 approaches with trade-offs. Lead with your recommendation and why.
6. Present the design in sections sized to their complexity, and confirm each one:
   components, data flow, error handling, how it is tested.
7. Write the approved design to the project's plans directory (`docs/plans/` unless
   its CLAUDE.md says otherwise). Commit only if the user asks.
8. Hand off: propose `/big-feature` with the design file as the task. Do not plan or
   implement here.

## Visual companion

Use the browser only when seeing beats reading: mockups, layout comparisons,
architecture diagrams. Text choices, scope and trade-offs stay in the terminal.

Once the user accepts, read `visual-companion.md` in this skill's directory before
starting the server. Scripts live in `scripts/`. Pass `--project-dir` so mockups
persist in `.superpowers/brainstorm/`, and check that `.superpowers/` is gitignored.

Visual companion: copied from obra/superpowers (MIT, see LICENSE).
