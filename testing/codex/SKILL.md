---
name: codex
description: OpenAI Codex CLI wrapper — three modes. (gstack)
category: engineering
sources:
- repository: gstack
  original_path: codex/SKILL.md
  sha256: 55096ae9e0c9db09fdfa7289eafc63f278dc0d03060e87208f85856f7f257eff
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Codex

OpenAI Codex CLI wrapper — three modes. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; Step 0: Detect platform and base branch; /codex — Multi-AI Second Opinion; Section index — Read each section when its situation applies; Step 0.4: Check codex binary; Step 0.5: Auth probe + model probe + version check; GSTACK_ACTIVE_HOST names the harness, never the model.; Step 0.6: Resolve portable roots; Step 1: Detect mode; Filesystem Boundary; Synthesis recommendation (REQUIRED) — all modes; Plan File Review Report; Detect the plan file; Generate the report.

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
- [design/plan-design-review](../../design/plan-design-review/SKILL.md)
- [developer-experience/devex-review](../../developer-experience/devex-review/SKILL.md)
- [developer-experience/plan-devex-review](../../developer-experience/plan-devex-review/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/plan-eng-review](../plan-eng-review/SKILL.md)
- [engineering/review](../review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/plan-ceo-review](../../product/plan-ceo-review/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)
- [workflows/autoplan](../../workflows/autoplan/SKILL.md)

## Source provenance

- `gstack/codex/SKILL.md`
