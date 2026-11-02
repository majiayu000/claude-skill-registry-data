---
name: hermes-runtime
description: "Use for Hermes runtime: crons, memory, inference, recall."
version: 1.0.0
author: Vesper
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, cron, memory, qdrant, inference, session-recall, self-management]
---

# Hermes Runtime — Autonomy, Memory, Inference, Recall

Class-level umbrella for running and maintaining Hermes itself: config flags,
cron check-ins, vector memory, local inference providers, and session recall.
Deep detail lives in the reference files below; archived originals retain full
session history.

## When to Use

- Configuring or maintaining Hermes autonomy systems (crons, flags, backups)
- Building state-aware cron check-ins that speak only when wanted
- Setting up or troubleshooting Qdrant vector memory
- Switching to a local inference provider or wiring local voice
- Finding or interpreting past conversation sessions

## Self-Management (distilled)

- Autonomy flags: `cron.allow_agent_scheduling`, `approvals.mode: smart`,
  `curator.consolidate`, `checkpoints.enabled`.
- Back up before self-modification; use checkpoints/rollback.
- Plan and autonomy notes were absorbed into this skill; manage statuses here.
- Full procedures remain in the archived `self-management` skill.

## Cron Check-ins (distilled)

- Open-door style: read live state, decide whether to reach out, stay silent
  if not wanted.
- Two models: Initiative (self-contained prompt, preferred) and Script-based
  (external Python reads SQLite).
- Cron sessions dominate browse results — filter `source != 'cron'`.
- Full prompt templates and examples are in the archived `cron-checkins` skill.

## Vector Memory (distilled)

- Qdrant native binary on localhost:6333; Hermes memory plugin connects to it.
- fastembed `BAAI/bge-small-en-v1.5`, 384-dim, local ONNX.
- Health check uses root `/` (v1.17+ removed `/health`).
- Point IDs must be UUIDs or unsigned integers.
- API patterns: `references/qdrant-api-patterns.md`.

## Local Inference (distilled)

- Configure custom OpenAI-compatible providers (LM Studio, Ollama, vLLM) via
  `custom_providers` in config; supports `/model` toggling.
- VM/agent and inference server may need SSH tunnel/Tailscale topology.
- Per-model `context_length` overrides; verify with a test completion.
- Full provider config examples are in the archived `local-inference` skill.

## Session Recall (distilled)

- `session_search` queries FTS5 over `state.db`; timestamps are UTC — convert
  to Mountain Time (UTC-7) before conclusions.
- Short terms/acronyms may fail FTS5; fall back to SQLite `LIKE`.
- Session resets are normal, not data loss.
- Cron sessions dominate results; filter them out.
- Schema and diagnostic queries: `references/state-db-schema.md`.

## Reference Files

- `references/state-db-schema.md` — state.db schema and diagnostic queries
- `references/qdrant-api-patterns.md` — Qdrant REST API patterns

## Related

- `devops/hermes-ops` — bundled Hermes ops skill (do not modify)

*-memory holds, the recall true-*
