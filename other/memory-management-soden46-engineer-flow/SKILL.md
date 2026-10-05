---
name: memory-management
description: Framework-agnostic project memory infrastructure for engineering tasks. Use for sparse recall, stale-memory handling, secret-safe durable checkpoints, and MCP/CLI fallback without consuming specialist slots.
metadata:
  internal: true
---

# Memory Management

Use memory as conditional infrastructure, not specialist expertise.

## Preflight

Run memory preflight only when prior project/session/workflow context could materially affect correctness. Skip self-contained tasks.

Prefer an active MCP memory tool when the host provides one. Otherwise use:

```bash
node skills/engineer-flow/infrastructure/memory-management/scripts/memory.mjs auto --cwd <project-root> --query "<task intent>" --limit 5
```

The command prints `decision: RUN` or `decision: SKIP`. On `RUN`, use only sparse relevant memory and verify it against current code/config.

## Rules

- Memory never consumes primary or support specialist slots.
- Current code/config beats old memory.
- Do not store secrets, `.env` values, raw credentials, or personal data.
- Preserve provenance and status.
- Checkpoint only durable reusable knowledge.

## Checkpoint

After meaningful work, checkpoint only when durable knowledge changed:

```bash
node skills/engineer-flow/infrastructure/memory-management/scripts/memory.mjs checkpoint --project <alias> --summary "<durable summary>"
```
