---
name: sync-gbrain
description: Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. (gstack)
category: memory
sources:
- repository: gstack
  original_path: sync-gbrain/SKILL.md
  sha256: 8d61083e7d34dc89a3aff8a75b94904f99347b84a12187af199dd11a8e3b714a
principles: []
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

# Sync Gbrain

Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. (gstack)

## Required procedure

Read [the complete methodology](references/methodology.md) before performing this skill. It retains the full procedure, examples, constraints, and failure handling.

Procedure topics: When to invoke this skill; /sync-gbrain — Keep gbrain current and teach the agent to use it; User-invocable; Step 1: State probe; Step 1.5: Local engine pre-flight (plan D12); Step 2: Run the orchestrator; Step 3: Code-index health check; Step 3.5: Call-graph health check (offer `--dream`); index($id) = literal substring (NOT test() regex), matching the lib reader in; cycleCompleted(). A fail/warn that doesn't name this source → "unknown" (don't; mask other-source failures).; Step 4: Refresh `## GBrain Search Guidance` block in CLAUDE.md; #2503: on worktree-pinned brains `gbrain put` can materialize the page as; <slug>.md in the CURRENT directory (the user's repo), and `gbrain delete`.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/gstack-operating-protocol](../../core/gstack-operating-protocol/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/plan-eng-review](../../engineering/plan-eng-review/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../context-restore/SKILL.md)
- [memory/context-save](../context-save/SKILL.md)
- [memory/learn](../learn/SKILL.md)
- [memory/setup-gbrain](../setup-gbrain/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)
- [workflows/gstack-workflow-router](../../workflows/gstack-workflow-router/SKILL.md)

## Source provenance

- `gstack/sync-gbrain/SKILL.md`
