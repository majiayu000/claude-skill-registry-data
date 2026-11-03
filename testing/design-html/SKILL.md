---
name: design-html
description: 'Design finalization: generates production-quality Pretext-native HTML/CSS. (gstack)'
category: design
sources:
- repository: gstack
  original_path: design-html/SKILL.md
  sha256: eafc2c628deed9aa448ccd24f0476d7b88628514b82594df15b796c006e2a60b
principles: []
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Design Html

Design finalization: generates production-quality Pretext-native HTML/CSS. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; /design-html: Pretext-Native HTML Engine; Section index — Read each section when its situation applies; DESIGN SETUP (run this check BEFORE any design mockup command); Step 0: Input Detection; Case A: approved.json exists (design-shotgun ran); Case B: CEO plan and/or design variants exist, but no approved.json; Case C: Nothing found (clean slate); Context summary; Step 1: Design Analysis; Step 2: Smart Pretext API Routing; Step 2.5: Framework Detection; Step 3: Generate Pretext-Native HTML; Pretext Source Embedding.

## Supporting material

See the [selective resource index](references/INDEX.md) for checklists, templates, examples, and reference implementations.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/gstack-operating-protocol](../../core/gstack-operating-protocol/SKILL.md)
- [design/design-consultation](../design-consultation/SKILL.md)
- [design/design-shotgun](../design-shotgun/SKILL.md)
- [design/plan-design-review](../plan-design-review/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [product/plan-ceo-review](../../product/plan-ceo-review/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)

## Source provenance

- `gstack/design-html/SKILL.md`
