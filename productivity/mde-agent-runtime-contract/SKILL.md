---
name: mde-agent-runtime-contract
description: Mandatory runtime and tool ownership contract for agent work in this repo. Use for setup, installation, migration, automation, and research tasks so agents stay mise-first and avoid unmanaged global installs.
---

# MDE Agent Runtime Contract

Load this skill before any setup, installation, migration, automation, or research task in this repository.

## Canonical Rule Set

- This repo defines the MacBook host setup contract for agent-run tooling work.
- Global runtimes, global CLIs, and SDK CLIs are `mise`-owned.
- Repo libraries are native-manifest-owned.
- macOS or system exceptions must be listed in `configs/mde-install-exceptions.json`.
- Reuse backend-native caches by default; cold installs and cache clears are exception-only behaviors.

## Required Inputs

Read these before making changes:

- `configs/mde-tool-ownership.json`
- `configs/mde-modernization-matrix.json`
- `configs/mde-install-exceptions.json`
- `configs/mde-skill-registry.json`
- `.agents/skills/mde-package-cache-policy/SKILL.md`
- `.agents/AGENTS.md`
- `AGENTS.md`

## Required Entry Points

- `mise run mde:agent:preflight`
- `mise run mde:agent:verify`
- `mise run mde:migrate:global-tools -- --dry-run|--apply|--verify|--report`
- `mise run mde:research:autoimprove -- --incremental|--full|--report`

## Hard Prohibitions

Unless an explicit exception is present and break-glass override is enabled, do not use:

- `brew install`
- `npm -g`
- `bun add -g`
- `uv tool install`
- `pip install --user`
- `pipx install`
- `cargo install`
- `go install`
- curl-based installer flows

## Decision Rule

If the problem is a missing import, missing package, or missing library, fix the manifest.
If the problem is a missing global executable, fix `mise` ownership.
Never solve either class of problem with an unmanaged global install.
