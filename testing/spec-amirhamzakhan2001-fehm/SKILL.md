---
name: spec
description: Turn vague intent into a precise, executable spec in five phases. (gstack)
category: product
sources:
- repository: gstack
  original_path: spec/SKILL.md
  sha256: 709dfcd9dd2d364a44e79535b234a9a4b7fe007f0a046c14dc33ab75178727a5
principles: []
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Spec

Turn vague intent into a precise, executable spec in five phases. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; Third-Party Web Actions; /spec — Author a Backlog-Ready Spec (issue + optional agent spawn); Flag Reference (parse from the user's initial invocation); Section index — Read each section when its situation applies; Process (STRICT — do not skip or combine phases); Phase 1: Understand the "Why" (+ optional --dedupe); Phase 2: Scope and Boundaries; Phase 3: Technical Interrogation (HARD requirement: read code first); Phase 4: Draft Review; Phases 4.5 and 5: Quality Gate, then File the Spec (sequencing summary); How to Ask Questions; Issue Quality Standards; 1. Stakeholder Context ("Why This Matters").

## Supporting material

See the [selective resource index](references/INDEX.md) for checklists, templates, examples, and reference implementations.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/gstack-operating-protocol](../../core/gstack-operating-protocol/SKILL.md)
- [developer-experience/browse](../../developer-experience/browse/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/plan-eng-review](../../engineering/plan-eng-review/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/office-hours](../office-hours/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)
- [workflows/autoplan](../../workflows/autoplan/SKILL.md)

## Source provenance

- `gstack/spec/SKILL.md`
