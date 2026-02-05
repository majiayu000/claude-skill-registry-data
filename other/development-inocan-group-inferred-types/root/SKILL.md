---
name: root
description: Manage and guide Hikaze-Model-Manager-2 Codex project work via the .codex governance system. Use when the user says "root skill" or asks to start development based on the root skill, or when asked to set up or operate .codex constitution/workflows/guidelines/jobs, manage jobs/phases/tasks with Markdown checklists, or migrate project prompts from conductor/ into .codex/.
---

# Root

## Overview

Use this skill to govern Codex project work for Hikaze-Model-Manager-2 using the .codex directory structure, keeping immutable sources of truth stable while tracking jobs and design details.

## Sources of truth and load order

1. Read `.codex/constitution/` for project principles, tech stack, and code standards.
2. Read `.codex/workflows/` for the static workflow framework.
3. Read `.codex/guidelines/` for implementation details and decisions.
4. Read `.codex/jobs/activated.md` and the active job file to understand current work.

## Hard rules

- Do not edit `.codex/constitution/` or `.codex/workflows/` unless the user explicitly requests changes.
- Propose suggestions for constitution/workflows only; do not modify without explicit user instruction.
- Record new or changed design details in `.codex/guidelines/` during design discussions.
- Record designed but not implemented items in `.codex/guidelines/not_implemented.md`.
- Keep all .codex content in Markdown.
- Use a single file per job to carry phases and tasks.
- The last task of every phase must be user manual verification.
- Track branches as indented checklist items; complete same-indent branch items before returning to the parent flow.
- Update `.codex/jobs/activated.md` whenever the active job changes.
- If required .codex paths are missing, ask before creating them.

## Job file format

Use `jobs/<job>/<job>.md` with Markdown checklists:

```markdown
# Job: <job-name>

## Phase 1: <phase-name>
- [ ] Task: <task>
  - [ ] Branch: <subtask>
  - [ ] Branch: <subtask>
- [ ] User manual verification

## Phase 2: <phase-name>
- [ ] Task: <task>
- [ ] User manual verification
```

## Workflow usage

- Treat workflows as the static guidance framework that governs each job and phase.
- Record workflow branches in the job file as indented checklists.
- Return to the parent flow after all items at the branch indent are complete.

## Conductor migration (only if requested)

Migrate prompts from `custom_nodes/Hikaze-Model-Manager-2/conductor/` to `.codex/` only when the user asks:

- `conductor/product.md` -> `.codex/constitution/product.md`
- `conductor/tech-stack.md` -> `.codex/constitution/tech-stack.md`
- `conductor/code_styleguides/*` -> `.codex/constitution/code_styleguides/*`
- `conductor/workflow.md` -> `.codex/workflows/default.md`
- `conductor/product-guidelines.md` -> `.codex/guidelines/product-guidelines.md`
- `conductor/archive/*` -> `.codex/jobs/archive/*`
- Do not migrate `conductor/discrepancies/*` unless the user explicitly requests it.

## Language policy

Accept any input language. Choose output language by accuracy first, then token efficiency.
