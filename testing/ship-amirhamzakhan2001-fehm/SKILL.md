---
name: ship
description: 'Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG,
  commit, push, create PR. (gstack)'
category: release
sources:
- repository: gstack
  original_path: ship/SKILL.md
  sha256: 895538116120c7ca60f4eabafd47b3267fc0396ee3344028d0d2f6302fc5538d
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Ship

Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; Third-Party Web Actions; Ship: Fully Automated Ship Workflow; Section index — Read each section when its situation applies; Step 0: Detect platform and base branch; Step 0.9: Apple target detection; Step 1: Pre-flight; Review Readiness Dashboard; Step 2: Distribution Pipeline Check; Step 3: Merge the base branch (BEFORE tests); Step 12: Version bump (auto-decide); Step 14: TODOS.md (auto-update); Step 15: Commit (bisectable chunks); Step 15.0: Preserve checkpoint context.

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
- [design/live-design-review](../../design/live-design-review/SKILL.md)
- [design/plan-design-review](../../design/plan-design-review/SKILL.md)
- [developer-experience/browse](../../developer-experience/browse/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/plan-eng-review](../../engineering/plan-eng-review/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/plan-ceo-review](../../product/plan-ceo-review/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/document-release](../document-release/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)
- [workflows/autoplan](../../workflows/autoplan/SKILL.md)

## Source provenance

- `gstack/ship/SKILL.md`
