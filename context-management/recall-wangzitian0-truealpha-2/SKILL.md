---
name: recall
description: Search persistent memory, git history, and dev_env SSOT before work. Use at session start, when taking a new task, or when investigating past decisions and rule rationale.
---

# recall: look up before you act

Never invent history or guess the rationale behind architecture and rules. Always retrieve physical evidence before acting or explaining past design decisions.

## Four-level deterministic retrieval protocol

When investigating past decisions, incident context, or rule rationale, execute this four-level retrieval chain:

```
Level 1: dev_env SSOT check (single source of truth in dev_env)
   ↓
Level 2: Global memory search (basic-memory across all projects)
   ↓
Level 3: Git commit archeology (git log -p / git log --grep)
   ↓
Level 4: Physical runtime verification (worker.log, live probes, exit codes)
```

### Level 1: dev_env SSOT check
- `dev_env` is the only editable source for root rules (`workspace-iac/etc/rules/subagents.md`) and common skills (`skills/common/*`).
- Always inspect the `dev_env` repository directly to verify current authoritative definitions rather than relying on projected worktree snapshots.

### Level 2: Global memory search
- Run `search_notes` with `search_all_projects: true`.
- Query exact keywords (e.g. `audit`, `swarm`, `decisions`, `sessions`, `handover`).
- Read full notes with `read_note` when relevant contracts or decisions match. Do not rely on short search excerpts.

### Level 3: Git commit archeology
- When the question asks "why is this designed this way" or "when did this change":
  - Run `git log -p -n 3 -- <target-file>` to read the exact diff and commit message.
  - Run `git log --grep="<keyword>" --oneline` to find the introducing PR and measured failure evidence.
  - Read the exact problem description. Do not synthesize or assume rationale.

### Level 4: Physical runtime verification
- When a tool, worker, or command fails:
  - Check live daemon logs: `tail -n 50 ~/.local/state/subagent-worker/worker.log`.
  - Check the LLM roles and the provider: `subagent-worker --check-models`.
  - Check physical git status and branch locks: `git status -s`, `git worktree list`.
  - Never classify a transient network or rate-limit failure as an architectural conflict.

## How to use results

1. **Empty result:** Continue silently. Report "no memory found" only when the owner asks.
2. **Cite briefly with anchors:** Cite the conclusion, date, commit SHA, note id, or exact line numbers (`file#Lxx-Lyy`). A statement without an anchor equals an invention.
3. **Code wins over memory:** Memory records a past decision. The live code is the present fact. On conflict, follow the code, cite both, and report the drift.
4. **Anchor small-model screening:** When a light model screens notes or a knowledge base, its output must carry anchors (`file#Lxx-Lyy` or note permalink).
