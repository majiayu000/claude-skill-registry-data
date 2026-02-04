---
name: devcontainer-maintenance
description: Maintain or change the devcontainer environment for this repo. Use when editing .devcontainer files, changing toolchains, or requesting environment rebuilds.
---

# Devcontainer Maintenance

## Source of truth

- `.devcontainer/Dockerfile`
- `.devcontainer/devcontainer.json`
- `scripts/devcontainer-post-create.sh`
- `msc-viterbo.code-workspace`

## Policy

- Environment changes must be approved by the project owner.
- Make changes in the devcontainer definition files (no ad-hoc local installs).
- Rebuild required after changes.

## Environment notes

- Single canonical devcontainer on Ubuntu 24.04.
- Shared host binds and caches persist across worktrees.
- Worktrees: `/workspaces/worktrees/`
- Shared cache: `/workspaces/worktrees/shared/` (Rust `target/`).
