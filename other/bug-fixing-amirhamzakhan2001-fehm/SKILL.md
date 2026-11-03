---
name: bug-fixing
description: Diagnose a reproducible defect, make the smallest repair, and prove the repair.
category: workflows
sources:
- repository: gstack
  original_path: investigate/SKILL.md
  sha256: a129ce67a04dca7dc75336109b879e56043dc99f7631ba62401e1291a1eed53e
- repository: agency-agents
  original_path: engineering/engineering-minimal-change-engineer.md
  sha256: 9999cc74e7b3936af892ef2c2793d105bb92f6c47789aa23db6df92bf68b45e5
- repository: ecc
  original_path: skills/tdd-workflow/SKILL.md
  sha256: f5d8543733c557f0c53b688d40f14e9b870a6b2c7e405bab07433954e363828a
- repository: ecc
  original_path: skills/verification-loop/SKILL.md
  sha256: f0d56107f79e607d4de6c5543b8edfb1b58ab9ae4019b39831689cd91116543e
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Bug Fixing

## When to use

Diagnose a reproducible defect, make the smallest repair, and prove the repair.

## Inputs

User objective, project constraints, relevant source or evidence, and explicit success criteria.

## Procedure and handoffs

1. Load [the investigate procedure](../../debugging/investigate/SKILL.md). Preserve the original failure and identify root cause before fixing.
2. Load [the minimal-change-engineer procedure](../../engineering/minimal-change-engineer/SKILL.md). Constrain the diff to the demonstrated cause and affected callers.
3. Load [the tdd-workflow procedure](../../testing/tdd-workflow/SKILL.md). Add a failing regression; implement the repair and refactor only within scope.
4. Load [the verification-loop procedure](../../verification/verification-loop/SKILL.md). Report regression and adjacent-check evidence, including unavailable checks.

## Verification and output

Produce the artifacts required by the selected procedures and an evidence-backed status: completed, failed, skipped with reason, or blocked on a named prerequisite. Carry unresolved findings forward. Do not treat an unavailable tool, an unrun check, or a reviewer failure as a pass.

## Scope and compatibility

Select stages proportionate to the task. Preserve required gates of the chosen variant; record exceptions. Read the [compatibility policy](../../COMPATIBILITY.md) before combining conflicting variants. These instructions do not grant tool access or authorize publishing, commits, deployment, or communications.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [debugging/investigate](../../debugging/investigate/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/minimal-change-engineer](../../engineering/minimal-change-engineer/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [security/unfreeze](../../security/unfreeze/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)
- [testing/tdd-workflow](../../testing/tdd-workflow/SKILL.md)
- [verification/verification-loop](../../verification/verification-loop/SKILL.md)

## Source provenance

- `gstack/investigate/SKILL.md`
- `agency-agents/engineering/engineering-minimal-change-engineer.md`
- `ecc/skills/tdd-workflow/SKILL.md`
- `ecc/skills/verification-loop/SKILL.md`
