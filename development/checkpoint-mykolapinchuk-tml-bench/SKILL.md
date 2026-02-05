---
name: checkpoint
description: Create a safe checkpoint git commit on the current branch (avoid competition data, runs, artifacts, secrets).
---

When invoked (or when the user says `checkpoint`), do this in order.

## 1) Preflight (must do; show output)
- `git status`
- `git diff --stat`

## 2) Sanity guardrails (must do)
- Never run: `git push`, `git commit --amend`, `git rebase`, `git reset --hard`, `git clean -fdx`, or modify git remotes.
- Never stage/commit secrets/credentials: `.env*`, `*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`, tokens.
- Never stage/commit competition data or run artifacts:
  - `competitions/**/{public,private,raw,downloads}/**`
  - `runs/**`
  - sqlite/db files

## 3) Stage (default: include safe tracked files)
Stage only source/docs/config files and small markdown:
- root `*.md`, `*.yml`
- `docs/**`
- `local_context_enrichments/**`
- `.codex/**`

If anything looks suspicious (bulk files, data-like payloads), stop and report before staging.

Before committing, show:
- `git diff --cached --stat`

## 4) Commit (auto message)
- Create a structured message that includes the agent id:
  - `agentNN: checkpoint(<area>): <short summary>`
  - Derive `agentNN` from `agent_logs/current.md` (field `id:`). If missing, stop and ask the human.
  - Choose `<area>` from: `workflow`, `docs`, `orchestrator`, `competitions`, `prompts`, `ci`, `misc`.
- Run `git commit -m "<message>"`.

## 5) Postflight (must do; show output)
- `git status`
- Report the commit hash.
