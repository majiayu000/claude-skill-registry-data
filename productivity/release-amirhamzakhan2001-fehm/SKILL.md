---
name: release
description: Prepare, document, land, deploy, and monitor a verified change.
category: workflows
sources:
- repository: ecc
  original_path: skills/verification-loop/SKILL.md
  sha256: f0d56107f79e607d4de6c5543b8edfb1b58ab9ae4019b39831689cd91116543e
- repository: gstack
  original_path: ship/SKILL.md
  sha256: 895538116120c7ca60f4eabafd47b3267fc0396ee3344028d0d2f6302fc5538d
- repository: gstack
  original_path: document-release/SKILL.md
  sha256: 7f01fd8dc6e963d38f224e09301bf320fa5ae45b9b2f92f08687f674331dd3d8
- repository: gstack
  original_path: land-and-deploy/SKILL.md
  sha256: f623d7b9285a907245cd5bfbea0429fabcba05bbfc57e23bc72e87c91cf169a4
- repository: gstack
  original_path: canary/SKILL.md
  sha256: fb059f32349eb7fe55181d90d9af461f5a02ceae8ee906a321195b217c150a2e
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Release

## When to use

Prepare, document, land, deploy, and monitor a verified change.

## Inputs

User objective, project constraints, relevant source or evidence, and explicit success criteria.

## Procedure and handoffs

1. Load [the verification-loop procedure](../../verification/verification-loop/SKILL.md). Record acceptance evidence for the candidate revision.
2. Load [the ship procedure](../../release/ship/SKILL.md). Prepare PR/release artifacts within authorization.
3. Load [the document-release procedure](../../release/document-release/SKILL.md). Reconcile documentation with the actual shipped behavior.
4. Load [the land-and-deploy procedure](../../release/land-and-deploy/SKILL.md). If authorized, land and deploy; retain rollback and production-verification evidence.
5. Load [the canary procedure](../../release/canary/SKILL.md). Monitor scoped health signals and report incidents or regressions.

## Verification and output

Produce the artifacts required by the selected procedures and an evidence-backed status: completed, failed, skipped with reason, or blocked on a named prerequisite. Carry unresolved findings forward. Do not treat an unavailable tool, an unrun check, or a reviewer failure as a pass.

## Scope and compatibility

Select stages proportionate to the task. Preserve required gates of the chosen variant; record exceptions. Read the [compatibility policy](../../COMPATIBILITY.md) before combining conflicting variants. These instructions do not grant tool access or authorize publishing, commits, deployment, or communications.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [release/canary](../../release/canary/SKILL.md)
- [release/document-release](../../release/document-release/SKILL.md)
- [release/land-and-deploy](../../release/land-and-deploy/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [verification/verification-loop](../../verification/verification-loop/SKILL.md)
- [workflows/dev-context](../dev-context/SKILL.md)

## Source provenance

- `ecc/skills/verification-loop/SKILL.md`
- `gstack/ship/SKILL.md`
- `gstack/document-release/SKILL.md`
- `gstack/land-and-deploy/SKILL.md`
- `gstack/canary/SKILL.md`
