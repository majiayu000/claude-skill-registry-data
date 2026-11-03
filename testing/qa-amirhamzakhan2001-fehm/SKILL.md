---
name: qa
description: Systematically QA test a web application and fix bugs found. (gstack)
category: testing
sources:
- repository: gstack
  original_path: qa/SKILL.md
  sha256: fe583b1beca3f62629e69def5c632cc65005978aa0482a69042381e163743c18
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Qa

Systematically QA test a web application and fix bugs found. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; Step 0: Detect platform and base branch; /qa: Test → Fix → Verify; Section index — Read each section when its situation applies; Setup; BROWSER SETUP (Aside — run this check BEFORE any browser step); Rules for driving a real browser; Browser fallback: gstack's own headless browser; Find the `$B` binary; Translate the Aside scripts step by step; What changes without Aside; Prior Learnings; Test Plan Context; Phases 1-6: QA Baseline.

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
- [developer-experience/browse](../../developer-experience/browse/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [developer-experience/setup-browser-cookies](../../developer-experience/setup-browser-cookies/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/plan-eng-review](../../engineering/plan-eng-review/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/plan-ceo-review](../../product/plan-ceo-review/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../qa-only/SKILL.md)

## Source provenance

- `gstack/qa/SKILL.md`
