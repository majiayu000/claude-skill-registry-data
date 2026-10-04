---
name: project-core-dev
description: Project overlay for discovering and reporting repository-specific completion checks for routine repo-owned changes. Use when the validation path is unclear; prefer specialized project overlays for config, platform, release, or vendor concerns.
---

# Project Core Dev

This is a thin project overlay, not a standalone implementation workflow.
Use it with matching implementation guidance only when repository-specific
checks or gaps remain unclear. Omit it when another selected skill plus repo
context already supplies exact commands and reporting obligations.

## When to use

The task is a routine repo-owned change whose completion path is not yet
concrete.

## Not for

Use `project-config-and-tests`, `project-platform-diagnose`,
`project-release-maintainer`, or `project-vendor-boundary` when that specialized
concern leads. Do not use this skill to restate a generic validation checklist.

## Completion Workflow

1. Read the applicable repository instructions, README, CI configuration,
   contributor docs, and presets. Identify authoritative commands and mandatory
   gates; do not invent a second workflow.
2. Map the touched surface to the narrowest honest repo-defined proof. Do not run
   broad checks merely because they exist.
3. Execute within the task's authority. Prefer check modes for read-only work;
   do not install tools, start services, or mutate the environment just to close
   a checklist.
4. Report exact commands, outcomes, gaps, and the narrowest next command that
   would close each material gap without implying it passed.
