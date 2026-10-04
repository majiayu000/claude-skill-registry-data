---
name: thrunt-remove-phase
description: Remove a future phase from huntmap and renumber subsequent phases
argument-hint: "<phase-number>"
allowed-tools: Read, Write, Bash, Glob
---

<objective>
Remove an unstarted future phase from the huntmap and renumber all subsequent phases to maintain a clean, linear sequence.

Purpose: Clean removal of work you've decided not to do, without polluting context with cancelled/deferred markers.
Output: Phase deleted, all subsequent phases renumbered, git commit as historical record.
</objective>

<execution_context>
@.github/thrunt-god/workflows/remove-phase.md
</execution_context>

<context>
Phase: $ARGUMENTS

Huntmap and state are resolved in-workflow via `init phase-op` and targeted reads.
</context>

<process>
Execute the remove-phase workflow from @.github/thrunt-god/workflows/remove-phase.md end-to-end.
Preserve all validation gates (future phase check, work check), renumbering logic, and commit.
</process>
