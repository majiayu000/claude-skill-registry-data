---
name: checkpoint
description: Create a safe checkpoint git commit on the current branch (auto-message; include agent log + safe untracked files; avoid secrets and bulky artifacts; track runs/**/{summary,report}.md only).
---

When invoked (or when the user says `checkpoint`), do this in order.

## 1) Preflight (must do; show output)
- `git status`
- `git diff --stat`

## 2) Sanity guardrails (must do)
- Never run: `git push`, `git commit --amend`, `git rebase`, `git reset --hard`, `git clean -fdx`, or modify git remotes.
- Never stage/commit secrets/credentials: `.env*`, `*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`, tokens.
- Never stage/commit bulky artifacts: `data/**` (except `data/README.md`), `secrets/**`, most of `runs/**` (except `runs/**/summary.md` and `runs/**/report.md`), and typical artifact payloads (`*.npz`, `*.parquet`, large `*.csv`).

## 3) Ensure runs markdown is link-only (must do)
- If any `runs/**/summary.md` or `runs/**/report.md` contain embedded images (`![](...)`), fix before committing:
  - Run: `python scripts/sanitize_runs_markdown.py --root runs --write`

## 4) Stage (default: include safe untracked files)
Stage:
- `agent_logs/current.md` if modified.
- All changed files under: `src/`, `scripts/`, `configs/`, `docs/`, plus small root-level `*.md`/`*.yml`/`*.toml`.
- `runs/**/summary.md` and `runs/**/report.md` (only those).

If there are new/untracked files:
- Include them only if they are clearly source/config/docs (no artifacts) and reasonably small.
- If there are “too many” files to stage (e.g., >50 paths) or anything looks suspicious, stop and ask before staging.

Before committing, show:
- `git diff --cached --stat`

## 5) Commit (auto message; no human message required)
- Create a message `checkpoint: <short summary>` derived from the staged paths (e.g., “checkpoint: add script + tweak plots”).
- If you can’t derive a meaningful summary, use `checkpoint: wip`.
- Run `git commit -m "<message>"`.

## 6) Postflight (must do; show output)
- `git status`
- Report the commit hash.

