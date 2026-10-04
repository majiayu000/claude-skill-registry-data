---
name: review-and-update-project-docs
description: 'Review code or a Git range and update project Markdown documentation: README.md, ARCHITECTURE.md, docs/architecture/**, and existing Diataxis roots under wiki/** or docs/wiki/**. Use for project-doc audits, release-range wiki coverage, or syncing documentation with implementation changes. Restrict the review and targets when the prompt provides explicit scopes; otherwise review the full source tree and all existing target docs.'
user-invocable: true
metadata:
  - "This skill reviews source code and updates project markdown documentation."
  - "Target documents: README.md, ARCHITECTURE.md, docs/architecture/**, and existing Diataxis roots under wiki/** or docs/wiki/**."
  - "If the prompt names specific docs to update, only those docs are updated; otherwise all target docs are updated."
  - "If the prompt names a Git range, code files, or modules to review, only that scope is reviewed; otherwise a global code review is performed first."
argument-hint: 'Optionally specify docs or wiki roots to update and code, modules, or a Git range to review.'
---

[Instruction](../../../instructions/review-and-update-project-docs.md)
