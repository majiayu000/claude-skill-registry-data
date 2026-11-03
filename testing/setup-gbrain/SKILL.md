---
name: setup-gbrain
description: 'Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain,
  register MCP, capture per-remote trust policy. (gstack)'
category: memory
sources:
- repository: gstack
  original_path: setup-gbrain/SKILL.md
  sha256: be2be0393b60927594b11c6aa94de277bda92422c1fa90b49ee2f0a8662286f2
principles: []
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Setup Gbrain

Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain, register MCP, capture per-remote trust policy. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; /setup-gbrain — Coding-Agent Onboarding for gbrain; User-invocable; Section index — Read each section when its situation applies; Step 1: Detect current state; Step 1.5: Broken-local-engine remediation (plan D4); Step 1.7: Code-intelligence provider choice (Step 0 of indexing); Step 2: Pick a path (AskUserQuestion); Step 3: Install gbrain CLI (if missing); Step 4: Initialize the brain; Step 5: Verify gbrain doctor; Step 5a: Register gbrain as Claude Code MCP (D18); Path 4 (Remote MCP — HTTP transport with bearer); Paths 1, 2a, 2b, 3 (Local stdio).

## Supporting material

See the [selective resource index](references/INDEX.md) for checklists, templates, examples, and reference implementations.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/gstack-operating-protocol](../../core/gstack-operating-protocol/SKILL.md)
- [debugging/investigate](../../debugging/investigate/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../context-restore/SKILL.md)
- [memory/context-save](../context-save/SKILL.md)
- [memory/learn](../learn/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)

## Source provenance

- `gstack/setup-gbrain/SKILL.md`
