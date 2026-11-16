---
name: codebase-recon
description: Understand an unfamiliar repository before making changes. Use when the task touches code whose architecture, conventions, or test setup are not already clear.
---

# Codebase Reconnaissance

Start read-only. Establish what the repository is, how it is organized, and how it is expected to work before editing.

## Workflow

1. Inspect the working tree, current branch, root files, local agent instructions, package manifests, and recent relevant history.
2. Trace the user-visible entry point through the main modules and data/control flow. Read the smallest set of files that explains the behavior.
3. Locate tests, fixtures, build scripts, formatters, linters, type checks, and documented developer commands. Prefer repository-defined commands.
4. Identify conventions for naming, errors, logging, configuration, dependencies, and public interfaces.
5. Run a safe baseline check when useful. Record existing failures rather than attributing them to later work.
6. Summarize the likely change surface, constraints, unknowns, and best verification command.

Do not dump entire repositories or secrets into context. Do not modify files during reconnaissance unless asked to combine investigation with implementation. Never infer architecture from filenames alone.
