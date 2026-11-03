---
name: qa-only
description: Report-only QA testing. (gstack)
category: testing
sources:
- repository: gstack
  original_path: qa-only/SKILL.md
  sha256: f9b4dd55879882b78e1127e8681da1bef12a26891aa6b32ec9bd65fb1f5bed31
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Qa Only

Report-only QA testing. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; /qa-only: Report-Only QA Testing; Setup; BROWSER SETUP (Aside — run this check BEFORE any browser step); Rules for driving a real browser; Browser fallback: gstack's own headless browser; Find the `$B` binary; Translate the Aside scripts step by step; What changes without Aside; Prior Learnings; Test Plan Context; Modes; Diff-aware (automatic when on a feature branch with no URL); Full (default when URL is provided).

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

## Source provenance

- `gstack/qa-only/SKILL.md`
