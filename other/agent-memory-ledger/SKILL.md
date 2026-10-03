---
name: agent-memory-ledger
description: >
  Create or use lightweight persistent project memory for Codex. Use when the
  user wants Codex to remember decisions, naming, architecture rules, progress,
  experiment results, or prior debugging across sessions. Also use with
  memsearch-style markdown memory.
---

# Agent Memory Ledger

Use markdown as the durable source of truth. Semantic indexes are optional
derived caches.

## Default Files

Create only the files needed:

```text
.codex-memory/
  decisions.md
  architecture.md
  glossary.md
  experiments.md
  todo.md
```

## Entry Format

```md
## 2026-05-19 - Short Title

- Context:
- Decision:
- Evidence:
- Follow-up:
```

## Recall Workflow

1. Search `.codex-memory/`, project docs, and recent task briefs.
2. If `.memsearch/memory/` exists and `memsearch` is installed, prefer `$auto-skill-build-memsearch-codex-memory` for progressive recall.
3. Return a short answer with source file/date.
4. Update memory only for stable decisions, not every transient observation.

## Rules

- Do not store secrets.
- Do not store full logs unless they are compacted.
- Keep each memory file skimmable; archive old details into dated files.
- Prefer "why we chose X" over "we talked about X".

Use with `$low-token-context` for long projects.

## Validation

- Memory entries cite a source file, command result, or user decision.
- Secrets and raw bulky logs are not stored.
- A future session can answer "what changed and why?" from the memory files.
