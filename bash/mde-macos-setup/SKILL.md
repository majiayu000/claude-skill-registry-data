---
name: mde-macos-setup
description: MacBook dev-environment runbook for this repo with mise-managed global tools, repo-native dependency ownership, secrets handling, telemetry, and verification.
---

# MDE macOS Setup

Use this skill when installing, repairing, or validating the MacBook dev setup maintained by this repo.

## Ownership Model

- `mise` owns global runtimes, global CLIs, SDK CLIs, and developer tooling commands.
- Bun and uv are ecosystem package managers under `mise`-managed runtimes; they are not alternative global authorities.
- Bun and uv are ecosystem package managers under mise-managed runtimes; they are not alternative global authorities.
- Repository libraries stay in `package.json`, `pyproject.toml`, `uv.lock`, `pixi`, `Cargo.toml`, `go.mod`, or devcontainer/image manifests.
- Homebrew is exception-only and must be justified through `configs/mde-install-exceptions.json`.
- Reuse backend-native caches by default through declared cache directories such as `UV_CACHE_DIR`, `BUN_INSTALL`, `GOCACHE`, `GOMODCACHE`, `CARGO_HOME`, and `RUSTUP_HOME`.

## Canonical Entry Points

- Preflight: `mise run mde:agent:preflight`
- Verification: `mise run mde:verify` and `mise run mde:drift`
- Migration: `mise run mde:migrate:global-tools -- --dry-run|--apply|--verify|--report`
- Research: `mise run mde:research:autoimprove -- --incremental|--full|--report`

## Setup Rules

- Keep PATH ordered with `mise` shims first.
- Keep `mise` as the source of truth for global tools, with `/Users/rmanaloto/.config/mise/config.toml` plus `configs/mde-modernization-matrix.json` defining whether each tool uses a direct `mise` declaration or a backend-native declarative config.
- Do not use direct global package-manager installs to fix missing tools for this repo.
- Do not force cold installs or clear package-manager caches unless an explicit maintenance flow allows it.
- Treat legacy installer scripts as transitional wrappers only; they are not the authority.

## Validation

Run these after any setup or policy change:

```bash
mise run mde:agent:preflight
mise run mde:verify
mise run mde:drift
mise run mde:status
```

## Telemetry

- Policy, migration, and research events are written under `reports/agent-policy/`.
- OpenLIT and LangSmith integration remain the higher-level observability targets, but local event logs are the minimum proof surface.
