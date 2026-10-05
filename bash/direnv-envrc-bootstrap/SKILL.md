---
name: direnv-envrc-bootstrap
description: Create/update a standard direnv `.envrc` that seeds a worktree `.env` from `~/.config/{slug}/.env` or from another git worktree, then loads it via `dotenv_if_exists`. Use when bootstrapping new git worktrees, fixing missing env vars in Codex-created worktrees, or standardizing local secret loading with direnv.
---

# Direnv Envrc Bootstrap

## Quick start

Option A (recommended for Codex worktrees): generate `.envrc` plus a pasteable Codex Setup Script:

- `bash scripts/codex_env_clipboard.sh`
- Paste clipboard into Codex → Environment → Setup script (or run `./codex_setup_script.sh`)

Option B (repo-only): generate `.envrc` and allow/load env in your shell:

- `bash scripts/write_envrc.sh`
- `source scripts/bootstrap_direnv.sh`

## Defaults

- Seeds `./.env` from `~/.config/medicalassistant_mcp/.env` if present.
- Otherwise tries to copy `./.env` from another `git worktree` (first one found).
- If still missing and `./.env.template` exists, copies it to `./.env`.
- Loads env vars via `dotenv_if_exists` (direnv stdlib).

## Common variants

- Different app/config path:
  - `bash scripts/write_envrc.sh --config-slug my_app`
  - `source scripts/bootstrap_direnv.sh --config-slug my_app`

- Overwrite existing `.envrc`:
  - `bash scripts/write_envrc.sh --force`

- For Codex setup script generation with a custom config slug:
  - `CONFIG_SLUG=my_app bash scripts/codex_env_clipboard.sh`
