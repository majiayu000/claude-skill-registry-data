---
name: tpp
description: Work a Technical Project Plan to completion — read the plan, start from its current phase, work through its tasks until their acceptance tests pass, and update the plan as each task lands. Use when starting or resuming multi-session work tracked in a plan file.
metadata:
  website: "https://photostructure.com/coding/claude-code-tpp/"
---

# Work on TPP

> Documented in depth: [Claude Code has amnesia. So do PRs, changelogs, and your future self.](https://photostructure.com/coding/claude-code-tpp/)

A Technical Project Plan (TPP) is a living handoff document: it carries research,
design decisions, failed approaches, and next steps across sessions, so the next
session (or the next engineer) continues instead of restarting.

Work the referenced TPP to completion: start from its current phase and keep
going until every task's acceptance test passes and every box under **Current
phase** is checked.

## Required Reading First

Before any work, you MUST read:

- The project's instructions: `AGENTS.md`, plus `CLAUDE.md` when present
- The project's TPP guide: `docs/TPP-GUIDE.md` if it exists; otherwise the
  bundled reference [TPP-GUIDE.md](TPP-GUIDE.md)

## Process

1. Read the referenced TPP. It will live in `_todo/`, in a priority folder
   (`_active/`, `_p1/`…`_p4/`), or in a documented feature integration queue
   matching `_feat-<name>/` if this project uses them.
2. Identify the current phase from its `Next:` line and unchecked boxes.
3. Work through the open tasks and phases without checking in. Put status notes
   in the same message as your next action.
4. As each task's acceptance test passes, tick it in the TPP and record
   discoveries — gotchas, rejected approaches, and the _why_ behind decisions,
   not a transcript.

Stop and ask the user only when:

- a decision is open that neither the TPP nor the code settles;
- the TPP contradicts what you find in the code;
- the next action deletes data, force-pushes, or changes anything outside the
  repository.

When context runs low before the work is done, invoke the `handoff` skill rather than
letting the session end silently. When the TPP is complete, move it to `_done/`.

## Adapting for your project

- **Create a project `docs/TPP-GUIDE.md`** (start from the bundled reference)
  and tailor the layout, frontmatter fields, and template to your conventions —
  the project guide always takes precedence over the bundled copy.
- **Extend the required reading list** with your high-value docs
  (`DESIGN-PRINCIPLES.md`, `TDD.md`, architecture decisions). Every listed file
  is read on every invocation, so keep it short.
- **Automate durable reminders portably.** Put the TPP update requirement in
  the repository's `AGENTS.md`, or use a supported project hook or automation
  that prompts the coding agent to update the active TPP before a task ends.
