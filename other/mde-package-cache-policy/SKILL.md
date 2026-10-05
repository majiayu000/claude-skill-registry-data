---
name: mde-package-cache-policy
description: Cross-ecosystem cache policy for mise-managed tooling, including preferred cache locations, warming, reuse, and bounded pruning rules.
---

# MDE Package Cache Policy

Use this skill when changing setup, migration, verification, automation, or host-tool cache behavior.

## Preferred Cache Locations

- `UV_CACHE_DIR`: `~/Library/Caches/uv` on macOS, `~/.cache/uv` elsewhere.
- `PIPX_HOME`: `~/.local/pipx`
- `PIPX_BIN_DIR`: `~/.local/bin`
- `BUN_INSTALL`: `~/.bun`
- `GOCACHE`: `~/Library/Caches/go-build` on macOS, `~/.cache/go-build` elsewhere.
- `GOMODCACHE`: `~/go/pkg/mod`
- `CARGO_HOME`: `~/.cargo`
- `RUSTUP_HOME`: `~/.rustup`

## Policy

1. Reuse backend-native caches by default.
2. Warm caches with declarative `mise install`, `mise run`, or backend-native read-only commands.
3. Do not delete caches during normal setup, verification, or automation.
4. Cache pruning is allowed only in bounded maintenance flows with explicit commands such as `uv cache prune`, `bun pm cache rm`, or `go clean -cache -modcache`.
5. Record cache behavior in `configs/mde-modernization-matrix.json` and never rely on shell-only tribal knowledge.

## cache pruning

- cache pruning is never the default path.
- cache pruning must be explicit, bounded, and recorded in maintenance guidance.

## Drift Rules

- Treat hardcoded alternate cache paths as drift unless the matrix or exception registry declares them.
- Treat cold-install guidance as drift unless an exception explicitly allows it.
- Preflight should verify cache directories are writable before automation starts.
