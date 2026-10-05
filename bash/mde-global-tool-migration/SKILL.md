---
name: mde-global-tool-migration
description: Use when migrating legacy global runtimes and CLIs into mise ownership, classifying current tool state, or validating that legacy installers are no longer the authority.
---

# MDE Global Tool Migration

Use this skill when moving global tooling from ad hoc installers into `mise` ownership.

## Goal

Shrink unmanaged global installs to zero or an explicit exception registry.

## Classification Rules

- `mise-owned`: global runtime or global CLI declared in `/Users/rmanaloto/.config/mise/config.toml`
- `native-manifest-owned`: library or repo dependency that belongs in project manifests
- `exception`: macOS/system tool in `configs/mde-install-exceptions.json`
- `removed`: obsolete or broken tool that should no longer be installed

## Workflow

1. Run `mise run mde:migrate:global-tools -- --dry-run`.
2. Review `reports/mde-migration/*-inventory.json` and `*-summary.md`.
3. If approved, run `mise run mde:migrate:global-tools -- --apply`.
4. Re-run with `--verify` and then run `mise run mde:drift`.

## Required Outcomes

- No agent should install repo-managed global tools with `brew`, `bun`, `uv`, `pipx`, `cargo`, or `go` directly.
- Legacy installer scripts may remain only as transitional wrappers or explicit exceptions.
- Every migration decision must be traceable through `reports/agent-policy/` telemetry.
