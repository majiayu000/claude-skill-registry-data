---
name: tdd
description: Use tests to define behavior, implement minimally, then verify the resulting change.
category: workflows
sources:
- repository: ecc
  original_path: agents/tdd-guide.md
  sha256: 979afbb40c42bfdd02fc308c130d7e257f5d6dd5f6531ef2562644862f6b7771
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

# Tdd

## When to use

Use tests to define behavior, implement minimally, then verify the resulting change.

## Inputs

User objective, project constraints, relevant source or evidence, and explicit success criteria.

## Procedure and handoffs

1. Load [the tdd-guide procedure](../../testing/tdd-guide/SKILL.md). Define behavior and failure cases; choose language-specific testing skills.
2. Load [the tdd-workflow procedure](../../testing/tdd-workflow/SKILL.md). Capture RED evidence, implement GREEN, and refactor with tests remaining green.
3. Load [the verification-loop procedure](../../verification/verification-loop/SKILL.md). Verify broader project checks; report the selected coverage target and actual result.

## Verification and output

Produce the artifacts required by the selected procedures and an evidence-backed status: completed, failed, skipped with reason, or blocked on a named prerequisite. Carry unresolved findings forward. Do not treat an unavailable tool, an unrun check, or a reviewer failure as a pass.

## Scope and compatibility

Select stages proportionate to the task. Preserve required gates of the chosen variant; record exceptions. Read the [compatibility policy](../../COMPATIBILITY.md) before combining conflicting variants. These instructions do not grant tool access or authorize publishing, commits, deployment, or communications.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [testing/tdd-guide](../../testing/tdd-guide/SKILL.md)
- [testing/tdd-workflow](../../testing/tdd-workflow/SKILL.md)
- [verification/verification-loop](../../verification/verification-loop/SKILL.md)

## Source provenance

- `ecc/agents/tdd-guide.md`
- `ecc/skills/tdd-workflow/SKILL.md`
- `ecc/skills/verification-loop/SKILL.md`
