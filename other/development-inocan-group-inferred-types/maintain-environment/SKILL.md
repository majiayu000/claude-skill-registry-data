---
name: maintain-environment
description: Maintain the repo devcontainer environment and related workflow files. Use when changing .devcontainer or environment setup scripts.
---

# Maintain Environment

## Scope

- Single reproducible development environment.
- Definition files: `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, `scripts/devcontainer-post-create.sh`, `ai-forecasting-hackathon.code-workspace`.

## Change policy

- Environment changes require project owner approval and a devcontainer rebuild.
- Modify definition files directly, not ad-hoc local installs, to keep reproducibility and documentation.

## Available tools

- Base image: `mcr.microsoft.com/devcontainers/base:ubuntu`
- Node and npm
- Common CLIs: `git`, `gh`, `rg`, `jq`, `fd`, `curl`, `tree`, `inotifywait`, `entr`
- IDE for project owner: `code-tunnel`

## Host binds and worktrees

- Host binds are defined in `devcontainer.json` and must exist or rebuilds fail.
- Host binds persist caches, oauth tokens, and configs across rebuilds.
- Worktrees persist in `/workspaces/worktrees/`.
- Shared across worktrees: host binds and `/workspaces/worktrees/shared/`.

## Notes

- Toolchain usage is documented in package-level docs.
- All agents and the project owner use the same devcontainer on the same ubuntu 24.04 host OS.
- No other clones of the repo exist, so gitignored changes and caches persist unless removed during worktree removal.
