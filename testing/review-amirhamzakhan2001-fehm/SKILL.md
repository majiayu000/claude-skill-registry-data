---
name: review
description: Pre-landing PR review. (gstack)
category: engineering
sources:
- repository: gstack
  original_path: review/SKILL.md
  sha256: cebbf9f8cbf1e230416559ad21ca3bf3de4cf0143917393303a0dfb0fa42e078
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Review

Pre-landing PR review. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; Step 0: Detect platform and base branch; Pre-Landing PR Review; Section index — Read each section when its situation applies; Step 1: Check branch; Step 1.5: Scope Drift Detection; Step 2: Read the checklist; Step 2.5: Check for Greptile review comments; Step 3: Get the diff; Step 3.4: Workspace-aware queue status (advisory); Step 3.5: Slop scan (advisory); Prior Learnings; Web research runs in Aside; Step 4: Critical pass (core review).

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
- [engineering/codex](../codex/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/spec](../../product/spec/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/document-release](../../release/document-release/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)

## Source provenance

- `gstack/review/SKILL.md`
