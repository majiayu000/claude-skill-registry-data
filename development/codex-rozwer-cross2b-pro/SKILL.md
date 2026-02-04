---
name: codex
description: Use when operating Codex CLI itself (config, profiles, sandbox, approvals, and safe usage patterns).
---

## Operating guidelines

1. Prefer safe defaults: `--sandbox workspace-write` and approvals `on-request` unless the user explicitly asks otherwise.
2. Make config changes explicit and minimal (document what changed and why).
3. When troubleshooting CLI behavior, capture:
   - `codex --version`
   - `/status` output
   - relevant config files (e.g., `config.toml`)
4. Avoid leaking secrets into logs; redact tokens and API keys.

## Common actions

- Validate configuration quickly via `codex exec --help` and `codex features list`.
- Use `CODEX_HOME` to switch between global and project-local setups.
