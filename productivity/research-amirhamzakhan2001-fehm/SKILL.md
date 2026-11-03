---
name: research
description: Search, evaluate, and synthesize evidence before recommending implementation.
category: workflows
sources:
- repository: ecc
  original_path: skills/search-first/SKILL.md
  sha256: d66d744228b9cf860acf35f8a90cbbe8195e61367860da9d3632f9fc65706733
- repository: agency-agents
  original_path: research/research-synthesist.md
  sha256: 3618b4a2a73523147731ae38ac4096cea0e83a7de930f55ea9ea6c69e3c77f30
- repository: ecc
  original_path: skills/deep-research/SKILL.md
  sha256: 72e184f5d0f31ca4d45286753409d8c8431b025e8ac3800dcc9f32d9e930f58a
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Research

## When to use

Search, evaluate, and synthesize evidence before recommending implementation.

## Inputs

User objective, project constraints, relevant source or evidence, and explicit success criteria.

## Procedure and handoffs

1. Load [the search-first procedure](../../research/search-first/SKILL.md). Search existing code and documented alternatives relevant to the task.
2. Load [the research-synthesist procedure](../../research/research-synthesist/SKILL.md). Record scope, source quality, disagreements, and uncertainty.
3. Load [the deep-research procedure](../../research/deep-research/SKILL.md). Use deeper research when needed; deliver supported findings and explicit gaps.

## Verification and output

Produce the artifacts required by the selected procedures and an evidence-backed status: completed, failed, skipped with reason, or blocked on a named prerequisite. Carry unresolved findings forward. Do not treat an unavailable tool, an unrun check, or a reviewer failure as a pass.

## Scope and compatibility

Select stages proportionate to the task. Preserve required gates of the chosen variant; record exceptions. Read the [compatibility policy](../../COMPATIBILITY.md) before combining conflicting variants. These instructions do not grant tool access or authorize publishing, commits, deployment, or communications.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [research/deep-research](../../research/deep-research/SKILL.md)
- [research/research-synthesist](../../research/research-synthesist/SKILL.md)
- [research/search-first](../../research/search-first/SKILL.md)

## Source provenance

- `ecc/skills/search-first/SKILL.md`
- `agency-agents/research/research-synthesist.md`
- `ecc/skills/deep-research/SKILL.md`
