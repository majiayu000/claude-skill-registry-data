---
name: autoplan
description: Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them
  sequentially with auto-decisions using 6 decision principles. (gstack)
category: workflows
sources:
- repository: gstack
  original_path: autoplan/SKILL.md
  sha256: 51f2788bcfb429864c9fa71e91e924d38ca91bd96698e942c7eae48fb55b0331
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Autoplan

Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisions using 6 decision principles. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; Step 0: Detect platform and base branch; Design Doc Check; Repo-local docs win when at least as fresh (#703): office-hours dual-writes; docs/designs/ alongside ~/.gstack, and the committed copy is what teammates; see. A stale old repo doc never shadows a newer private session.; Prerequisite Skill Offer; Repo-local docs win when at least as fresh (#703): office-hours dual-writes; docs/designs/ alongside ~/.gstack, and the committed copy is what teammates; see. A stale old repo doc never shadows a newer private session.; /autoplan — Auto-Review Pipeline; Section index — Read each section when its situation applies; The 6 Decision Principles; Decision Classification.

## Supporting material

See the [selective resource index](references/INDEX.md) for checklists, templates, examples, and reference implementations.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/gstack-operating-protocol](../../core/gstack-operating-protocol/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/office-hours](../../product/office-hours/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)

## Source provenance

- `gstack/autoplan/SKILL.md`
